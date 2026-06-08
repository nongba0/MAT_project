import urllib.request
import urllib.parse
import re
import json
import time

bakeries = [
    "소울브레드", "르뱅룰즈 선릉점", "에삐 선릉본점", "담밀",
    "대구 미힐", "대구 랑잠", "대구 윈드윈", "퀸즈베이커리 삼청점",
    "프루케 생과일케이크", "화성 동경빵집", "메종드빵 칠곡"
]

results = {}

for b in bakeries:
    print(f"Searching Naver for {b}...")
    try:
        q = urllib.parse.quote(b + " 빵집 리뷰")
        req = urllib.request.Request(f"https://search.naver.com/search.naver?query={q}", headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Extract blog.naver.com links
        links = list(set(re.findall(r'href="(https://blog\.naver\.com/[^"]+)"', html)))
        
        # Filter out generic ones
        clean_links = [l for l in links if "PostView.naver" in l or "PostList.naver" not in l]
        
        results[b] = clean_links[:3]
    except Exception as e:
        print(f"Error for {b}: {e}")
        results[b] = []
    time.sleep(1)

with open("naver_links.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links.json")
