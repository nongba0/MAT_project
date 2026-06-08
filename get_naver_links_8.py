import urllib.request
import urllib.parse
import re
import json
import time

bakeries = [
    "동탄 아쌍트베이커리 리뷰", "동탄 아이엠브래드 본점 리뷰", "압구정 투아투아 리뷰",
    "부산 콩지니빵 리뷰", "동탄 조각달과자점 리뷰", "오산 컴인디저트 리뷰",
    "망원 두두리두팡 리뷰", "잠실 에낭 리뷰", "송파 하프파운드 리뷰",
    "망원 동명양과자점 리뷰", "망원 후와후와 빵집 리뷰", "망원 어글리베이커리 리뷰",
    "부산 더베이베이커리 리뷰", "부산 희와제과 리뷰", "송파 르빵 리뷰"
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

with open("naver_links_96_110.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_96_110.json")
