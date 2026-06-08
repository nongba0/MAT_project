import urllib.request
import urllib.parse
import re
import json
import time

bakeries = [
    "동탄 리얼브레드", "수영 비비비", "분당 부부제과", "부평 밀곳",
    "논현 외계인방앗간 본점", "신사 폼드팡베이커리", "청담 타르틴베이커리", "압구정 헤이즈밀베이커리",
    "서면 퍼프베이커리", "방배 바게틴", "도산 자연도소금빵", "연산 디저트시네마",
    "광안리 서희와제과", "동탄 몽스베이커리"
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

with open("naver_links_47_60.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to naver_links_47_60.json")
