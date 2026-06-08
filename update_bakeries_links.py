import sys
import json

bakeries_file = r"C:\Users\sangw\.gemini\antigravity\scratch\web-service\src\main\resources\bakeries.tsv"
json_file = r"C:\Users\sangw\.gemini\antigravity\scratch\web-service\naver_links.json"

with open(json_file, "r", encoding="utf-8") as f:
    real_links = json.load(f)

# The keys in JSON are:
# 소울브레드, 르뱅룰즈 선릉점, 에삐 선릉본점, 담밀, 대구 미힐, 대구 랑잠, 대구 윈드윈, 퀸즈베이커리 삼청점, 프루케 생과일케이크, 화성 동경빵집, 메종드빵 칠곡

key_map = {
    13: "소울브레드",
    14: "르뱅룰즈 선릉점",
    15: "에삐 선릉본점",
    16: "담밀",
    17: "대구 미힐",
    18: "대구 랑잠",
    19: "대구 윈드윈",
    20: "퀸즈베이커리 삼청점",
    21: "프루케 생과일케이크",
    22: "화성 동경빵집",
    23: "메종드빵 칠곡"
}

with open(bakeries_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(13, 24):
    line_idx = i - 1
    t = lines[line_idx].strip('\n').split('\t')
    
    # Update column 11 (index 10) with real links
    key = key_map[i]
    links = real_links.get(key, [])
    if links:
        t[10] = "|".join(links)
    
    new_line = "\t".join(t) + "\n"
    lines[line_idx] = new_line

with open(bakeries_file, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Updated review_links with REAL URLs successfully.")
