## 1. Observation
- The Forensic Auditor found that `process_bookmarks.py` fails the integrity check because it injects completely hardcoded strings (e.g. `"분위기가 좋아요|커피가 맛있어요|직원이 친절해요"`, `"신선한 재료로 만든 디저트"`) for fields like `menuFeatures`, `positiveReviews`, `negativeReview`, `comparisons`, and `waitingSystem`.
- The DDG search correctly gathers a textual `corpus` from web search results (lines 39-44 of `process_bookmarks.py`), but the existing `heuristic_extract()` function ignores this corpus for several key fields and unconditionally returns the hardcoded defaults (lines 46-60).

## 2. Logic Chain
1. To pass the integrity check, we must stop using fake/hardcoded default data and actually populate the required TSV fields by processing the fetched web `corpus`.
2. Given that the `corpus` consists of unstructured text from search results, an NLP heuristic approach using Python's `re` module is appropriate to extract sentences and keywords.
3. **Extraction Strategy for `positiveReviews` and `negativeReview`**: Split the corpus into sentences. Filter sentences by checking against a list of positive keywords (e.g., "맛있", "좋", "친절") and negative keywords ("아쉽", "대기", "비싸"). Join the top matching sentences with `|`.
4. **Extraction Strategy for `sig_menu` and `menuFeatures`**: Search for a predefined list of common cafe/bakery items (like "아메리카노", "라떼", "소금빵") near the word "시그니처" or "대표" in the corpus. For features, find sentences containing words like "수제", "로스팅", "원두".
5. **Extraction Strategy for `comparisons`**: Synthesize a dynamic comparison using actual extracted features (e.g. comparing to a generic cafe based on the dynamically extracted `ambiance` or `sig_menu`) or search for explicit mentions of competitor brands like "스타벅스" in the text.
6. **Extraction Strategy for `waitingSystem`, `parkingInfo`, `has_dine`, `sold_out`**: Map specific keywords ("캐치테이블", "발렛", "테이크아웃", "품절") to dynamic boolean or string values based on their presence in the corpus, returning "정보 없음" if none are found.

## 3. Caveats
- The extraction is purely heuristic and keyword-based. It does not use an LLM model, so the accuracy depends entirely on the presence of the keywords in the DuckDuckGo search snippets.
- The `corpus` size is limited by `DDGS().text(query, max_results=3)` which may not contain sufficient text for all fields. Some fields may legitimately evaluate to "정보 없음" (No info) rather than a populated string, which is standard for missing real data and acceptable compared to using fabricated data.

## 4. Conclusion
The integrity violation can be resolved by replacing the hardcoded variable block in `process_bookmarks.py:46-60` with dynamic regex-based sentence extraction and keyword matching against the DuckDuckGo search `corpus`. 
Below is the proposed Python code replacement for the `heuristic_extract` function to be implemented by the next agent:

<details>
<summary>Proposed Code Replacement for `heuristic_extract`</summary>

```python
import re

def heuristic_extract(name, address, results, is_bakery_flag):
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
```
</details>

## 5. Verification Method
- **Method**: Modify `process_bookmarks.py` with the proposed replacement code.
- **Run**: Delete any generated test TSV lines in `src/main/resources/cafes.tsv` and `bakeries.tsv`, then run `python process_bookmarks.py`.
- **Validation**: Run `cat src/main/resources/cafes.tsv` and `cat src/main/resources/bakeries.tsv` and inspect the newly appended rows. Ensure that fields such as `positiveReviews`, `ambiance`, and `comparisons` are diverse and correspond to the actual search snippets, or say "정보 없음", rather than repeating a hardcoded generic string for every row.
