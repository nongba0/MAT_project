import urllib.request
import urllib.parse
import re
import json
import time

bakeries = [
    "부산 덕선제과 리뷰", "부산 초량온당 리뷰", "송파 하츠베이커리 리뷰"
]

results = {}

for b in bakeries:
    print(f"Searching Naver for {b}...")
    try:
        q = urllib.parse.quote(b)
        req = urllib.request.Request(f"https://search.naver.com/search.naver?query={q}", headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        links = list(set(re.findall(r'href="(https://blog\.naver\.com/[^"]+)"', html)))
        clean_links = [l for l in links if "PostView.naver" in l or "PostList.naver" not in l]
        
        results[b] = clean_links[:3]
    except Exception as e:
        print(f"Error for {b}: {e}")
        results[b] = []
    time.sleep(1)

with open("naver_links_111_114.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_111_114.json")
