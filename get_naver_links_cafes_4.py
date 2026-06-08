import urllib.request
import urllib.parse
import re
import json
import time

cafes = [
    "용인 롱드메이 리뷰", "노량진 지지엔엔 베이크 샵 리뷰", "성산동 하프베이글 리뷰",
    "전주 히포파운드 리뷰", "성남 카페여기 리뷰", "동탄 레이지오븐 리뷰",
    "삼각지 스쿠퍼젤라또 리뷰", "용리단길 스푼업 리뷰", "동탄 카페레이들 리뷰",
    "더노벰버라운지 동탄점 리뷰"
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

with open("naver_links_cafes_61_70.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_cafes_61_70.json")
