import urllib.request
import urllib.parse
import re
import json
import time

bakeries = [
    "전주 낸시베이크샵", "동탄 디허케이크룸", "동탄 늘브레드", "문정 더 브레드레지던스",
    "모란 오프베이크룸", "동탄 수향진베이커리카페", "동탄 디저트굽는 모카곰", "문정 파브리케",
    "망원 졸리파이마켓", "망원 밀로밀", "노원 샛별제과", "문정 플라워아티장베이커리",
    "신사 플라워아티장베이커리", "동탄 아나브", "동탄 쿠다산도"
]

results = {}

for b in bakeries:
    print(f"Searching Naver for {b}...")
    try:
        q = urllib.parse.quote(b + " 리뷰")
        req = urllib.request.Request(f"https://search.naver.com/search.naver?query={q}", headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        links = list(set(re.findall(r'href="(https://blog\.naver\.com/[^"]+)"', html)))
        clean_links = [l for l in links if "PostView.naver" in l or "PostList.naver" not in l]
        
        results[b] = clean_links[:3]
    except Exception as e:
        print(f"Error for {b}: {e}")
        results[b] = []
    time.sleep(1)

with open("naver_links_81_95.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_81_95.json")
