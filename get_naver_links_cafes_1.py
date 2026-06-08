import urllib.request
import urllib.parse
import re
import json
import time

cafes = [
    "수원 오하하하우스 카페 리뷰", "을지로 1020룸 카페 리뷰", "건대 윤숲 후르츠산도점 리뷰",
    "동탄 카케야 카페 리뷰", "성수 사운드프로바이더 카페 리뷰", "선릉 텟어텟 리뷰",
    "천호 헤르츠로그 리뷰", "동탄 카페 바솔트 리뷰", "평택 디오미오 카페 리뷰",
    "평택 원스타임오프 평택점 리뷰"
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

with open("naver_links_cafes_31_40.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_cafes_31_40.json")
