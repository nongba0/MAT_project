import urllib.request
import json

url = 'http://localhost:8080/api/match/bakery'
data = {'searchType': 'BREAD', 'keyword': '소금빵'}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    print(json.dumps(result, ensure_ascii=False, indent=2))
