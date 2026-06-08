# Data Pipeline Strategy Handoff

## 1. Observation
- `PROJECT.md` specifies creating `process_bookmarks.py` to clean fake entries from `cafes.tsv` and `bakeries.tsv`, perform web research using `duckduckgo_search` for 214 entries from `hong_bookmarks.json`, format the data, and append it.
- `import_bookmarks.py` generated the fake data by randomly picking from lists like `AMBIANCES`, `CAFE_SIG_MENUS`, `MENU_FEATURES`, `POS_REVIEWS`, `CAFE_COMPS`, etc.
- `cafes.tsv` currently has 151 lines and `bakeries.tsv` has 118 lines. The columns are tab-separated.
- `cafes.tsv` has 17 columns (15 original + `latitude` + `longitude`).
- `bakeries.tsv` has 14 columns (12 original + `latitude` + `longitude`).
- `hong_bookmarks.json` contains a `bookmarkList` object with items having `name`, `mcid`, `mcidName`, `address`, `py` (lat), `px` (lng), `memo`, `cidPath`.
- User interaction prompts for `run_command` and `view_file` (for files outside the workspace) are timing out, indicating the user is not actively approving actions.

## 2. Logic Chain
- **Data Cleaning**: Because the fake data is generated from static lists in `import_bookmarks.py`, we can identify and remove fake rows by checking if the `menuFeatures` (or `menu_features`) column exactly matches any item in the `MENU_FEATURES` list, or if the `comparisons` column matches any item in `CAFE_COMPS` / `BAKERY_COMPS`. Removing these will leave only the genuine 30 entries + headers.
- **Web Research (DDGS)**: 
  - Read `hong_bookmarks.json` and iterate over the `bookmarkList`.
  - Use `is_bakery` logic (from `import_bookmarks.py`) to classify each bookmark as cafe or bakery.
  - Skip existing genuine entries.
  - Use the `duckduckgo-search` library (`DDGS().text(f"{name} {address} 리뷰", max_results=3)`) to fetch real reviews.
- **Summarization & Generation**: 
  - Since formatting requirements like `comparisons` (`[비교대상]|[비교특징]|[상세설명]`) and summarizing reviews are complex, `process_bookmarks.py` should ideally use an LLM API (e.g., `google.generativeai` with `GEMINI_API_KEY`) to parse the DDGS snippets into the exact TSV format.
  - If no LLM is available, the script must implement a fallback heuristic to populate the columns reasonably (e.g., extracting sentences with positive/negative keywords).
- **Merge**: Append the formatted 214 rows to the cleaned TSV lists and write back to `cafes.tsv` and `bakeries.tsv`.
- **Testing**: Run `mvnw.cmd clean test`. Since `run_command` is timing out, the Implementer should focus on writing a robust `process_bookmarks.py` and potentially simulating the execution or documenting how to run it when the user returns.

## 3. Caveats
- `hong_bookmarks.json` is located outside the workspace (`C:\Users\sangw\OneDrive\바탕 화면\hong_bookmarks.json`). Agent tools timed out trying to read it, but Python's `open()` within `process_bookmarks.py` should work if local OS permissions allow.
- DuckDuckGo Search (`duckduckgo-search`) is rate-limited. Making 214 requests in a tight loop might result in HTTP 429 errors. The script should include `time.sleep()` between requests.
- Summarizing into specific TSV formats programmatically without an LLM is error-prone and might cause `mvnw` test failures if formats (like booleans or `comparisons` pipe separation) are violated. The Implementer should handle this carefully.
- I was unable to test `python` execution locally because `run_command` timed out waiting for user approval.

## 4. Conclusion
The Data Pipeline implementation should proceed with `process_bookmarks.py` containing three main phases:
1. **Filter**: Read TSVs and discard rows where `menu_features` is in the known fake lists from `import_bookmarks.py`.
2. **Fetch & Summarize**: Read JSON, classify items, search DDGS with a delay, and format the output (preferably via an LLM call or a solid heuristic) to strictly match the 17-col (cafe) and 14-col (bakery) structure.
3. **Write & Verify**: Append new rows, ensuring no formatting drift. Testing must rely on `mvnw.cmd clean test`.

## 5. Verification Method
- **Cleaning**: Inspect the output of TSVs to ensure line counts drop to 16 (15 cafes + header) and 16 (15 bakeries + header) before the new 214 entries are added.
- **Test Command**: `.\mvnw.cmd clean test` will verify that the final TSVs have no parsing errors and seed the DB successfully.
