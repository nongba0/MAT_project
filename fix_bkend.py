import urllib.request
import urllib.parse
import re
import json
import time

c = "망원동 비캔드 리뷰"
try:
    q = urllib.parse.quote(c)
    req = urllib.request.Request(f"https://search.naver.com/search.naver?query={q}", headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    links = list(set(re.findall(r'href="(https://blog\.naver\.com/[^"]+)"', html)))
    clean_links = [l for l in links if "PostView.naver" in l or "PostList.naver" not in l]
    print("Links:", clean_links[:3])
except Exception as e:
    print(f"Error for {c}: {e}")
