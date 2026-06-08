import csv
import time
from duckduckgo_search import DDGS

def verify_restaurant(name, location):
    query = f"{location} {name}"
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(r)
    except Exception as e:
        print(f"Error fetching {name}: {e}")
        return -1
    
    count = 0
    # 이름의 띄어쓰기를 없앤 버전도 검색에 포함
    name_no_space = name.replace(" ", "")
    
    for r in results:
        title = r.get('title', '')
        body = r.get('body', '')
        text = title + " " + body
        count += text.count(name) + text.count(name_no_space)
        
    return count

def main():
    tsv_path = "src/main/resources/restaurants.tsv"
    suspicious_list = []
    
    print("Starting verification using DDGS...")
    
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
            
            # 검색 결과 내 언급 횟수가 부족하면 의심
            if count <= 0:
                suspicious_list.append((name, location, count))
                
            time.sleep(1.0)
            
    print("\n--- Verification Complete ---")
    print(f"Found {len(suspicious_list)} suspicious restaurants:")
    for s in suspicious_list:
        print(f"- {s[0]} ({s[1]}) : {s[2]} matches")
        
    with open("suspicious_restaurants2.txt", "w", encoding="utf-8") as out:
        for s in suspicious_list:
            out.write(f"{s[0]}\t{s[1]}\t{s[2]}\n")

if __name__ == "__main__":
    main()
