import urllib.request
import urllib.parse
import re
import json
import time

bakeries = [
    "분당 블랑제리 드 빌라주", "수원 느긋한제빵소", "동탄 다스브로트", "망원 리브인오후",
    "동탄 핸즈베이커리", "진주 알곡점빵", "동래 쿠루미 과자점", "강남 꼼다비뛰드",
    "성수 밀스", "타르틴베이커리 판교점", "방배 컨트리보이", "공덕 수더분"
]

results = {}

for b in bakeries:
    print(f"Searching Naver for {b}...")
    try:
        q = urllib.parse.quote(b + " 빵집 리뷰")
        req = urllib.request.Request(f"https://search.naver.com/search.naver?query={q}", headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Extract blog.naver.com links
        links = list(set(re.findall(r'href="(https://blog\.naver\.com/[^"]+)"', html)))
        
        # Filter out generic ones
        clean_links = [l for l in links if "PostView.naver" in l or "PostList.naver" not in l]
        
        results[b] = clean_links[:3]
    except Exception as e:
        print(f"Error for {b}: {e}")
        results[b] = []
    time.sleep(1)

with open("naver_links_35_46.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_35_46.json")
