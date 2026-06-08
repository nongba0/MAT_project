import urllib.request
import urllib.parse
import re
import json
import time

cafes = [
    "오산 픽베이크 리뷰", "동탄 유밀정 케이커리 리뷰", "동탄 카페홀로 리뷰",
    "동탄 스트레스드 리뷰", "치즈당 동탄카림센텀점 리뷰", "서촌 비지터 리뷰",
    "유월커피 역삼 리뷰", "동탄 오르또커피하우스 리뷰", "용인 아리랑도원 리뷰",
    "동탄 아워시즌 장지점 리뷰"
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

with open("naver_links_cafes_71_80.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_cafes_71_80.json")
