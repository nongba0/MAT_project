import urllib.request
import urllib.parse
import re
import json
import time

bakeries = [
    "대전 로로네베이커리", "대전 콜드버터베이크샵 본점", "대전 성심당 케익부띠끄", "대전 성심당 본점",
    "대전 몽심 한남대점", "대전 몽심 대흥점", "대전 하레하레 둔산점", "성수 자연도소금빵",
    "전주 뭉실베이커리", "강남 팡뮤제 베이커리"
]

results = {}

for b in bakeries:
    print(f"Searching Naver for {b}...")
    try:
        q = urllib.parse.quote(b + " 빵집 리뷰")
        req = urllib.request.Request(f"https://search.naver.com/search.naver?query={q}", headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        links = list(set(re.findall(r'href="(https://blog\.naver\.com/[^"]+)"', html)))
        clean_links = [l for l in links if "PostView.naver" in l or "PostList.naver" not in l]
        
        results[b] = clean_links[:3]
    except Exception as e:
        print(f"Error for {b}: {e}")
        results[b] = []
    time.sleep(1)

with open("naver_links_71_80.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_71_80.json")
