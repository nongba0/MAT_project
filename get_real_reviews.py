import json
from ddgs import DDGS
import time

bakeries = [
    "소울브레드", "르뱅룰즈 선릉점", "에삐 선릉본점", "담밀 화성",
    "대구 미힐", "대구 랑잠", "대구 윈드윈", "퀸즈베이커리 삼청점",
    "프루케 생과일케이크", "화성 동경빵집", "대구 메종드빵"
]

results = {}

with DDGS() as ddgs:
    for bakery in bakeries:
        print(f"Searching for {bakery}...")
        try:
            # Get top 3 text results for reviews
            query = f"site:blog.naver.com {bakery} 빵집 리뷰"
            search_results = list(ddgs.text(query, max_results=3))
            
            # Extract links and snippets
            links = [res['href'] for res in search_results if 'href' in res]
            snippets = [res['body'] for res in search_results if 'body' in res]
            
            results[bakery] = {
                "links": links,
                "snippets": snippets
            }
        except Exception as e:
            print(f"Error searching {bakery}: {e}")
            results[bakery] = {"links": [], "snippets": []}
        time.sleep(1)

with open("real_links_11.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to real_links_11.json")
