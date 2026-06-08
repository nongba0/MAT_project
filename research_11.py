import json
from duckduckgo_search import DDGS

bakeries = [
    "소울브레드", "르뱅룰즈 선릉점", "에삐 선릉본점", "담밀 화성 봉담",
    "대구 미힐", "대구 랑잠", "대구 윈드윈", "퀸즈베이커리 삼청점",
    "프루케 생과일케이크 본점", "화성 동경빵집", "대구 메종드빵"
]

results = {}
with DDGS() as ddgs:
    for bakery in bakeries:
        print(f"Searching for {bakery}...")
        try:
            # Get top 5 text results
            search_results = list(ddgs.text(f"{bakery} 리뷰 OR 후기", max_results=5))
            results[bakery] = search_results
        except Exception as e:
            print(f"Error searching {bakery}: {e}")
            results[bakery] = []

with open("research_11_bakeries.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Research saved to research_11_bakeries.json")
