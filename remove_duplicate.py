import sys

bakeries_file = r"C:\Users\sangw\.gemini\antigravity\scratch\web-service\src\main\resources\bakeries.tsv"

with open(bakeries_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

if "솔트앤멜로우" in lines[33] and "솔트앤멜로우" in lines[34]:
    del lines[34]
    
    with open(bakeries_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Deleted duplicate Salt & Mellow at index 34.")
else:
    print("No duplicate found at index 33 and 34.")
