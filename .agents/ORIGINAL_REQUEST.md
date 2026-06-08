# Original User Request

## Initial Request — 2026-06-08T18:44:36+09:00

네이버 지도 즐겨찾기(`hong_bookmarks.json`)에 있는 214곳의 카페와 빵집에 대해 개별 웹 검색을 수행하고, 엄격한 방법론(실제 리뷰, 대조군 비교 등)을 적용하여 진짜 데이터가 담긴 TSV 파일을 생성합니다.

Working directory: `C:\Users\sangw\.gemini\antigravity\scratch\web-service`

## Requirements

### R1. 데이터 정제 및 초기화
기존 `cafes.tsv` 및 `bakeries.tsv`에 들어가 있는 214개의 가짜/추론 데이터를 식별하여 삭제하고, 초기의 30개 검증된 데이터만 남겨둡니다.

### R2. 실제 데이터 웹 리서치 (Web Research)
`hong_bookmarks.json`에서 추출된 214개의 장소 각각에 대해 웹 검색(DuckDuckGo 등)을 수행하여 다음 정보를 수집합니다:
- 실제 긍정/부정 리뷰 요약
- 실제 시그니처 메뉴 및 매장/메뉴 특징
- 네이버 블로그, 유튜브 등의 실제 리뷰 링크 (파이프(|) 구분)
- 적절한 비교군(Target)과의 객관적 비교 평가 (예: "A카페|커피맛|A카페보다 원두 풍미가 깊음")
- 주차, 콘센트, 웨이팅 시스템 등 실제 방문 정보

### R3. TSV 파일 병합 및 업데이트
수집된 진짜 데이터를 `cafes.tsv`와 `bakeries.tsv`의 기존 포맷(15개 및 12개 컬럼, 마지막 위도/경도 포함)에 정확하게 맞추어 덧붙입니다.

## Acceptance Criteria

### Format & Data Integrity
- [ ] 214개의 장소 데이터가 모두 `cafes.tsv` 또는 `bakeries.tsv`에 성공적으로 병합되어야 합니다.
- [ ] 모든 데이터의 `comparisons` 컬럼은 `[비교대상]|[비교특징]|[상세설명]` 포맷을 엄격히 준수해야 합니다.
- [ ] 빈칸(Empty) 데이터가 최소화되어야 하며, 특히 시그니처 메뉴와 리뷰는 실제 검색 결과를 바탕으로 작성되어야 합니다.

### Programmatic Verification
- [ ] 데이터 병합 후 `.\mvnw.cmd clean test` 명령어를 실행하여, 새로 갱신된 TSV 파일들이 `CafeSeeder`와 `BakerySeeder`에서 파싱 에러 없이 정상적으로 데이터베이스에 적재되는지 검증을 통과해야 합니다.
