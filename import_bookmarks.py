import json
import os
import random

# File paths
JSON_PATH = r"C:\Users\sangw\OneDrive\바탕 화면\hong_bookmarks.json"
CAFES_TSV = "src/main/resources/cafes.tsv"
BAKERIES_TSV = "src/main/resources/bakeries.tsv"

def load_existing_names(tsv_path):
    if not os.path.exists(tsv_path):
        return set()
    names = set()
    with open(tsv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.split('\t')
            if len(parts) > 0:
                names.add(parts[0].strip())
    return names

def read_tsv(tsv_path):
    with open(tsv_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_tsv(tsv_path, lines):
    with open(tsv_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

# Fake data generators
AMBIANCES = [
    "깔끔하고 모던한 인테리어", "우드톤의 따뜻하고 아늑한 분위기", "넓고 쾌적한 대형 카페 느낌",
    "힙하고 트렌디한 감성", "조용하고 차분하여 대화하기 좋은 공간", "채광이 좋고 사진이 잘 나오는 분위기",
    "레트로 빈티지 감성이 물씬 풍기는 곳", "식물이 많아 자연 친화적인 플랜테리어"
]

CAFE_SIG_MENUS = ["시그니처 크림라떼", "바닐라빈 라떼", "아인슈페너", "핸드드립 커피", "플랫화이트", "말차 라떼", "아메리카노"]
BAKERY_SIG_MENUS = ["소금빵", "크루아상", "몽블랑", "앙버터", "바게트", "에그타르트", "치아바타", "수제 케이크"]

MENU_FEATURES = [
    "매일 아침 직접 구워내는 신선한 맛", "고급 원두를 사용하여 깊은 풍미", 
    "좋은 재료를 아끼지 않은 풍성한 맛", "많이 달지 않아 부담 없이 즐길 수 있는 디저트",
    "독창적인 레시피로 만든 시그니처 메뉴들", "건강하고 담백한 맛이 일품"
]

POS_REVIEWS = [
    "분위기가 너무 예쁘고 커피가 맛있어요|직원분들이 친절합니다|재방문 의사 100%",
    "디저트가 환상적입니다|공간이 넓어서 쾌적해요|사진 찍기 좋은 포토존이 많아요",
    "동네 숨은 맛집입니다|조용해서 작업하기 좋아요|시그니처 메뉴는 꼭 드셔보세요",
    "오랜만에 진짜 맛있는 곳을 찾았어요|인테리어가 감각적입니다|친구 데려가기 좋아요"
]

NEG_REVIEWS = [
    "주말 피크타임에는 대기가 길어질 수 있습니다.", "매장이 골목에 있어 주차가 약간 불편합니다.",
    "인기가 많아 늦게 가면 빵이 품절됩니다.", "매장 내부 소리가 조금 울리는 편입니다.",
    "좌석 간격이 다소 좁게 느껴질 수 있습니다."
]

WAITING_SYS = ["현장 대기 후 입장", "웨이팅 어플 사용", "평일은 여유로우나 주말 대기 발생", "주문 시 약간의 대기열 있음"]
PARKING_INFO = ["매장 앞 2~3대 주차 가능", "인근 공영주차장 이용 권장", "전용 주차장 완비", "주차 불가 (대중교통 권장)"]

CAFE_COMPS = ["스타벅스|접근성 및 개성|스타벅스보다 개성 있는 메뉴와 아늑한 동네 카페 감성", "투썸플레이스|디저트|투썸 못지않게 디저트 퀄리티가 훌륭하고 수제 느낌이 강함"]
BAKERY_COMPS = ["파리바게뜨|빵 퀄리티|프랜차이즈와 비교할 수 없는 깊은 버터 풍미와 쫄깃한 식감", "뚜레쥬르|종류 및 맛|기본 빵의 퀄리티가 훨씬 높고 소화가 잘 됨"]

def is_bakery(name, memo, cidPath):
    keywords = ["베이커리", "빵", "제과", "케이크", "디저트", "과자", "bakery"]
    name_memo = f"{name} {memo}".lower()
    for kw in keywords:
        if kw in name_memo:
            return True
    if cidPath and ("221161" in cidPath or "220564" in cidPath):
        return True
    return False

def main():
    print("Loading JSON bookmarks...")
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    bookmarks = data.get("bookmarkList", [])
    
    cafe_lines = read_tsv(CAFES_TSV)
    bakery_lines = read_tsv(BAKERIES_TSV)
    
    # Check headers and add lat/lng if not present
    cafe_header = cafe_lines[0].strip().split('\t')
    if cafe_header[-1] != "longitude":
        if cafe_header[-1] == "comparisons":
            cafe_lines[0] = cafe_lines[0].strip() + "\tlatitude\tlongitude\n"
        else:
            print("Cafe header doesn't end with comparisons. Please fix manually.")
            
    bakery_header = bakery_lines[0].strip().split('\t')
    if bakery_header[-1] != "longitude":
        if bakery_header[-1] == "comparisons":
            bakery_lines[0] = bakery_lines[0].strip() + "\tlatitude\tlongitude\n"
        else:
            print("Bakery header doesn't end with comparisons. Please fix manually.")
            
    existing_cafes = load_existing_names(CAFES_TSV)
    existing_bakeries = load_existing_names(BAKERIES_TSV)
    
    added_cafes = 0
    added_bakeries = 0
    
    for bm in bookmarks:
        name = bm.get("name", "")
        if name in existing_cafes or name in existing_bakeries:
            continue
            
        mcid = bm.get("mcid", "")
        mcidName = bm.get("mcidName", "")
        # Only process cafe/bakery
        if mcid != "CAFE" and mcidName != "카페" and not is_bakery(name, bm.get("memo"), bm.get("cidPath")):
            continue
            
        address = bm.get("address", "")
        lat = str(bm.get("py", ""))
        lng = str(bm.get("px", ""))
        
        # Determine category
        bakery_flag = is_bakery(name, bm.get("memo"), bm.get("cidPath"))
        
        # Generate fake data
        ambiance = random.choice(AMBIANCES)
        menu_feat = random.choice(MENU_FEATURES)
        pos = random.choice(POS_REVIEWS)
        neg = random.choice(NEG_REVIEWS)
        wait = random.choice(WAITING_SYS)
        has_dine = str(random.choice([True, True, True, False])) # mostly true
        
        if bakery_flag:
            sig = random.choice(BAKERY_SIG_MENUS)
            comp = random.choice(BAKERY_COMPS)
            sold_out = "주말 오후 3시 이후 인기 빵 품절 가능성 높음" if random.choice([True, False]) else "오후 늦게 방문 시 일부 품목 소진"
            links = f"https://search.naver.com/search.naver?query={name.replace(' ', '+')}"
            
            # Bakery format: name, exact_address, store_features, signature_menu, menu_features, sold_out_info, waiting_system, has_dine_in, positive_reviews, negative_review, review_links, comparisons, latitude, longitude
            row = f"{name}\t{address}\t{ambiance}\t{sig}\t{menu_feat}\t{sold_out}\t{wait}\t{has_dine}\t{pos}\t{neg}\t{links}\t{comp}\t{lat}\t{lng}\n"
            bakery_lines.append(row)
            added_bakeries += 1
        else:
            sig = random.choice(CAFE_SIG_MENUS)
            comp = random.choice(CAFE_COMPS)
            links = f"https://search.naver.com/search.naver?query={name.replace(' ', '+')}"
            plugs = str(random.choice([True, False]))
            park = random.choice(PARKING_INFO)
            decaf = str(random.choice([True, False]))
            large = str(random.choice([True, False]))
            pet = str(random.choice([True, False]))
            
            # Cafe format: name, exactAddress, ambiance, signatureMenu, menuFeatures, positiveReviews, negativeReview, reviewLinks, waitingSystem, hasPlugs, parkingInfo, hasDecaf, isLargeCafe, isPetFriendly, comparisons, latitude, longitude
            row = f"{name}\t{address}\t{ambiance}\t{sig}\t{menu_feat}\t{pos}\t{neg}\t{links}\t{wait}\t{plugs}\t{park}\t{decaf}\t{large}\t{pet}\t{comp}\t{lat}\t{lng}\n"
            cafe_lines.append(row)
            added_cafes += 1
            
    # Update files
    write_tsv(CAFES_TSV, cafe_lines)
    write_tsv(BAKERIES_TSV, bakery_lines)
    
    print(f"Import complete! Added {added_cafes} cafes and {added_bakeries} bakeries.")

if __name__ == "__main__":
    main()
