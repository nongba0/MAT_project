import urllib.request
import urllib.parse
import re
import json
import time

bakeries = [
    "서촌 마사마드레", "수원 고미베이커에프앤비", "화성 도나의식탁", "평택 폴디드",
    "서산 NNN BAKERY", "동탄 블랑제리 르가르쏭", "수원 라라베이커리", "서면 허대빵",
    "파이인더샵 용산점", "망원동 투떰즈업", "동탄 솔트앤멜로우"
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

with open("naver_links_24_34.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_24_34.json")
