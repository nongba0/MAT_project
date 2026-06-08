import urllib.request
import urllib.parse
import re
import json
import time

cafes = [
    "대구 베이크오이 리뷰", "인사동 토오베 리뷰", "삼청동 포스톤즈 카페 리뷰",
    "북촌 로우루프 카페 리뷰", "안국 공공재 커피클럽 리뷰", "북촌 이오이 카페 리뷰",
    "북촌 굴림 카페 리뷰", "동탄 파티드 카페 리뷰", "서촌 굴림 카페 리뷰",
    "서촌 베란다 카페 리뷰"
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

with open("naver_links_cafes_41_50.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_cafes_41_50.json")
