import urllib.request
import urllib.parse
import re
import json
import time

cafes = [
    "서촌 스태픽스 리뷰", "양재 브레드앤워크 리뷰", "양재 카페 마몽드 리뷰",
    "향남 서울치아바타 카페 리뷰", "동탄 밀랩커피하우스 리뷰", "성남 원스타임오프 리뷰",
    "서면 아니버 카페 리뷰", "잠실 아벡쉐리 롯데월드몰점 리뷰", "성남 송미방앗간 리뷰",
    "전포 크리미 리뷰"
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

with open("naver_links_cafes_51_60.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_cafes_51_60.json")
