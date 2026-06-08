$body = @{
    searchType = "LOCATION"
    keyword = "마포구"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8080/api/match/bakery" -Method Post -ContentType "application/json; charset=utf-8" -Body $body

$response | ConvertTo-Json -Depth 5
