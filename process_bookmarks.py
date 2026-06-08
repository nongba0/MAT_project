import json
import os
import time
from duckduckgo_search import DDGS

JSON_PATH = r"C:\Users\sangw\OneDrive\바탕 화면\hong_bookmarks.json"
CAFES_TSV = "src/main/resources/cafes.tsv"
BAKERIES_TSV = "src/main/resources/bakeries.tsv"

def read_tsv(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_tsv(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def is_bakery(name, memo, cidPath):
    keywords = ["베이커리", "빵", "제과", "케이크", "디저트", "과자", "bakery", "스콘", "도넛"]
    name_memo = f"{name} {memo}".lower() if memo else name.lower()
    for kw in keywords:
        if kw in name_memo:
            return True
    if cidPath and ("221161" in cidPath or "220564" in cidPath):
        return True
    return False

def search_ddg(query):
    try:
        results = DDGS().text(query, max_results=3)
        return results if results else []
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def heuristic_extract(name, address, results, is_bakery_flag):
    import re
    corpus = " ".join([r.get('body', '') for r in results]).replace('\n', ' ').replace('\t', ' ')
    links = "|".join([r.get('href', '') for r in results])
    if not links:
        links = f"https://search.naver.com/search.naver?query={name.replace(' ', '+')}"
    if len(links) > 400:
        links = links[:400]

    def extract_sentences(corp, keywords):
        sentences = re.split(r'[.!?\n]+', corp)
        matches = []
        for s in sentences:
            s = s.strip()
            if any(kw in s for kw in keywords) and len(s) > 5:
                matches.append(s)
        return list(dict.fromkeys(matches))

    # 1. pos_reviews
    pos_kws = ["맛있", "좋", "친절", "최고", "추천", "완벽", "훌륭"]
    pos_sentences = extract_sentences(corpus, pos_kws)
    pos_reviews = "|".join(pos_sentences[:3]) if pos_sentences else "리뷰 정보 없음"

    # 2. neg_reviews
    neg_kws = ["아쉽", "비싸", "불친절", "대기", "웨이팅", "시끄럽", "좁", "오래"]
    neg_sentences = extract_sentences(corpus, neg_kws)
    neg_reviews = neg_sentences[0] if neg_sentences else "부정적 리뷰 없음"

    # 3. sig_menu
    common_items = ["라떼", "아메리카노", "크로플", "스콘", "케이크", "소금빵", "마카롱", "빙수", "밀크티", "크루아상", "드립커피", "디카페인", "베이글"]
    sig_menu = "정보 없음"
    match = re.search(r'(.{0,15})(시그니처|대표|인기)(.{0,15})', corpus)
    if match:
        found = [item for item in common_items if item in match.group(0)]
        if found: sig_menu = found[0]
    if sig_menu == "정보 없음":
        found = [item for item in common_items if item in corpus]
        if found: sig_menu = found[0]

    # 4. menu_feat
    menu_kws = ["수제", "로스팅", "원두", "유기농", "신선", "크림", "시럽", "비건", "글루텐프리"]
    menu_sentences = extract_sentences(corpus, menu_kws)
    menu_feat = menu_sentences[0] if menu_sentences else "특징 정보 없음"

    # 5. ambiance
    ambiance_kws = ["분위기", "인테리어", "감성", "뷰", "조명", "음악", "테라스", "조용", "아늑", "힙"]
    ambiance_sentences = extract_sentences(corpus, ambiance_kws)
    ambiance = ambiance_sentences[0] if ambiance_sentences else "분위기 정보 없음"

    # 6. wait
    if "캐치테이블" in corpus: wait = "캐치테이블"
    elif "테이블링" in corpus: wait = "테이블링"
    elif any(w in corpus for w in ["웨이팅", "대기", "줄서"]): wait = "현장 대기 (웨이팅 있음)"
    else: wait = "정보 없음"

    # 7. park
    if any(w in corpus for w in ["주차 불가", "주차 안"]): park = "주차 불가"
    elif any(w in corpus for w in ["발렛", "발렏"]): park = "발렛 가능"
    elif any(w in corpus for w in ["공영 주차장", "공영주차장"]): park = "인근 공영주차장 이용"
    elif any(w in corpus for w in ["주차 가능", "주차장"]): park = "주차 가능"
    else: park = "주차 정보 없음"

    # 8. comp (Dynamic Synthesis)
    if "스타벅스" in corpus: comp = "스타벅스|언급됨|리뷰에서 스타벅스와 비교 언급됨"
    elif "투썸" in corpus: comp = "투썸플레이스|언급됨|리뷰에서 투썸플레이스와 비교 언급됨"
    elif is_bakery_flag: comp = f"일반 빵집|메뉴 구성|{sig_menu} 등 특색있는 메뉴 제공" if sig_menu != "정보 없음" else "일반 빵집|메뉴|정보 부족으로 비교 어려움"
    else: comp = f"일반 카페|분위기|{ambiance[:20]}..." if ambiance != "분위기 정보 없음" else "일반 카페|특징|정보 부족으로 비교 어려움"

    # 9. Other Booleans
    plugs = "True" if any(w in corpus for w in ["콘센트", "노트북", "카공"]) else "False"
    decaf = "True" if "디카페인" in corpus else "False"
    large = "True" if any(w in corpus for w in ["대형", "넓은", "3층", "2층"]) else "False"
    pet = "True" if any(w in corpus for w in ["애견", "반려동물", "펫", "강아지"]) else "False"
    sold_out = "조기 품절 가능성 있음" if any(w in corpus for w in ["품절", "마감", "솔드아웃"]) else "정보 없음"
    has_dine = "False" if "테이크아웃 전문" in corpus or "포장 전문" in corpus else "True"

    return {
        "ambiance": ambiance, "sig_menu": sig_menu, "menu_feat": menu_feat,
        "pos_reviews": pos_reviews, "neg_reviews": neg_reviews, "wait": wait,
        "plugs": plugs, "park": park, "decaf": decaf, "large": large,
        "pet": pet, "comp": comp, "sold_out": sold_out, "has_dine": has_dine,
        "links": links
    }

def main():
    print("Loading JSON bookmarks...")
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return

    bookmarks = data.get("bookmarkList", [])
    bookmark_names = {bm.get("name", "") for bm in bookmarks}
    
    cafe_lines = read_tsv(CAFES_TSV)
    bakery_lines = read_tsv(BAKERIES_TSV)
    
    # 1. Clean fake entries
    cleaned_cafes = [cafe_lines[0]] if cafe_lines else []
    for line in cafe_lines[1:]:
        parts = line.split('\t')
        if len(parts) > 0 and parts[0].strip() not in bookmark_names:
            cleaned_cafes.append(line)
            
    cleaned_bakeries = [bakery_lines[0]] if bakery_lines else []
    for line in bakery_lines[1:]:
        parts = line.split('\t')
        if len(parts) > 0 and parts[0].strip() not in bookmark_names:
            cleaned_bakeries.append(line)

    print(f"Cleaned TSVs. Cafes left: {len(cleaned_cafes)-1}, Bakeries left: {len(cleaned_bakeries)-1}")
    
    # 2. Process bookmarks
    added_cafes = 0
    added_bakeries = 0

    for bm in bookmarks:
        name = bm.get("name", "").strip()
        mcid = bm.get("mcid", "")
        mcidName = bm.get("mcidName", "")
        
        bakery_flag = is_bakery(name, bm.get("memo"), bm.get("cidPath"))
        
        # Only process cafe/bakery
        if mcid != "CAFE" and mcidName != "카페" and not bakery_flag:
            continue
            
        address = bm.get("address", "")
        lat = str(bm.get("py", ""))
        lng = str(bm.get("px", ""))
        
        print(f"Fetching data for: {name}")
        query = f"{name} {address} 리뷰"
        results = search_ddg(query)
        time.sleep(1) # delay to avoid rate limit
        
        ext = heuristic_extract(name, address, results, bakery_flag)
        
        if bakery_flag:
            # Bakery format: name, exact_address, store_features, signature_menu, menu_features, sold_out_info, waiting_system, has_dine_in, positive_reviews, negative_review, review_links, comparisons, latitude, longitude
            row = f"{name}\t{address}\t{ext['ambiance']}\t{ext['sig_menu']}\t{ext['menu_feat']}\t{ext['sold_out']}\t{ext['wait']}\t{ext['has_dine']}\t{ext['pos_reviews']}\t{ext['neg_reviews']}\t{ext['links']}\t{ext['comp']}\t{lat}\t{lng}\n"
            cleaned_bakeries.append(row)
            added_bakeries += 1
        else:
            # Cafe format: name, exactAddress, ambiance, signatureMenu, menuFeatures, positiveReviews, negativeReview, reviewLinks, waitingSystem, hasPlugs, parkingInfo, hasDecaf, isLargeCafe, isPetFriendly, comparisons, latitude, longitude
            row = f"{name}\t{address}\t{ext['ambiance']}\t{ext['sig_menu']}\t{ext['menu_feat']}\t{ext['pos_reviews']}\t{ext['neg_reviews']}\t{ext['links']}\t{ext['wait']}\t{ext['plugs']}\t{ext['park']}\t{ext['decaf']}\t{ext['large']}\t{ext['pet']}\t{ext['comp']}\t{lat}\t{lng}\n"
            cleaned_cafes.append(row)
            added_cafes += 1

    write_tsv(CAFES_TSV, cleaned_cafes)
    write_tsv(BAKERIES_TSV, cleaned_bakeries)
    
    print(f"Finished processing! Added {added_cafes} cafes and {added_bakeries} bakeries.")

if __name__ == '__main__':
    main()
