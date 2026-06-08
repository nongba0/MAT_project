# Project: WebService Cafe/Bakery Data Enhancement
# Scope: Global

## Architecture
- `hong_bookmarks.json` contains 214 bookmarks (cafes and bakeries).
- `cafes.tsv` and `bakeries.tsv` currently hold 30 valid entries + 214 fake generated entries.
- We need a single Python script (`process_bookmarks.py`) to:
  1. Data Cleaning: Identify and remove the 214 fake entries from cafes.tsv and bakeries.tsv.
  2. Web Research: Read `hong_bookmarks.json`, fetch real web data using `duckduckgo_search` for the 214 entries, summarize reviews, generate comparisons, and format them to match TSV columns.
  3. Merge: Append the 214 new rows to the TSVs.
- After processing, run `mvnw.cmd clean test` to ensure successful DB seeding without parsing errors.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Data Pipeline | Create process_bookmarks.py, execute it to update TSVs, and verify with tests. | none | IN_PROGRESS |

## Interface Contracts
- TSV format must exactly match the original 15 (cafes) and 12 (bakeries) columns.
- `comparisons` column must use `[비교대상]|[비교특징]|[상세설명]` format.
- Output TSV must have the last 2 columns as latitude and longitude.
- Fake entries identification: match with lists used in `import_bookmarks.py`.
