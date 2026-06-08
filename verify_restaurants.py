import csv
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import os
import ssl

# SSL 인증서 검증 무시 (일부 환경에서 발생할 수 있는 에러 방지)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def verify_restaurant(name, location):
    query = f"{location} {name}"
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )
    
    try:
        response = urllib.request.urlopen(req, context=ctx)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        text = soup.get_text()
        
        # 이름의 띄어쓰기를 없앤 버전도 검색에 포함
        name_no_space = name.replace(" ", "")
        
        count = text.count(name) + text.count(name_no_space)
        return count
    except Exception as e:
        print(f"Error fetching {name}: {e}")
        return -1

def main():
    tsv_path = "src/main/resources/restaurants.tsv"
    suspicious_list = []
    
    print("Starting verification of 71 restaurants...")
    
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        
        for idx, row in enumerate(reader):
            if not row or len(row) < 2:
                continue
                
            name = row[0]
            location = row[1]
            
            # 검색
            count = verify_restaurant(name, location)
            print(f"[{idx+1}/71] {name} ({location}): {count} matches")
            
            # 검색 결과 내 언급 횟수가 2번 이하면 의심
            if count <= 2:
                suspicious_list.append((name, location, count))
                
            time.sleep(1.5)  # rate limit 방지
            
    print("\n--- Verification Complete ---")
    print(f"Found {len(suspicious_list)} suspicious restaurants:")
    for s in suspicious_list:
        print(f"- {s[0]} ({s[1]}) : {s[2]} matches")
        
    with open("suspicious_restaurants.txt", "w", encoding="utf-8") as out:
        for s in suspicious_list:
            out.write(f"{s[0]}\t{s[1]}\t{s[2]}\n")

if __name__ == "__main__":
    main()
