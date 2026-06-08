import urllib.request
import urllib.parse
import re
import json
import time

cafes = [
    "동탄 라몽슈슈 리뷰", "용인 서천 키친 드 마망 리뷰", "동탄 아르밀베이크샵 리뷰",
    "망원 키오스크 리뷰", "동탄 91brick 리뷰", "해운대 밀창고 리뷰",
    "야탑 아라리오브네 리뷰", "모란역 이아이모란 리뷰", "성남 공세계 리뷰",
    "신사 따우전드 리뷰"
]

results = {}

for c in cafes:
    print(f"Searching Naver for {c}...")
    try:
        q = urllib.parse.quote(c)
        req = urllib.request.Request(f"https://search.naver.com/search.naver?query={q}", headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        links = list(set(re.findall(r'href="(https://blog\.naver\.com/[^"]+)"', html)))
        clean_links = [l for l in links if "PostView.naver" in l or "PostList.naver" not in l]
        
        results[c] = clean_links[:3]
    except Exception as e:
        print(f"Error for {c}: {e}")
        results[c] = []
    time.sleep(1)

with open("naver_links_cafes_81_90.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_cafes_81_90.json")
