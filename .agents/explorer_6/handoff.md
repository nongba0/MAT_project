# Handoff Report

## 1. Observation
- The Forensic Auditor reported an **INTEGRITY VIOLATION** because `process_bookmarks.py` hardcodes dummy strings for qualitative fields (`menuFeatures`, `positiveReviews`, `negativeReview`, `comparisons`, `waitingSystem` defaults) and injects them unconditionally into `cafes.tsv` and `bakeries.tsv` for all newly processed entries.
- Review of `process_bookmarks.py` (lines 47-60 and 87) confirms that the function `heuristic_extract` assigns fabricated values such as `pos_reviews = "분위기가 좋아요|커피가 맛있어요|직원이 친절해요"`, `comp = "스타벅스|접근성|동네 카페만의 아늑함과 개성이 돋보임"`, and `ambiance = "깔끔하고 모던한 인테리어"`.
- Review of the output TSVs (`cafes.tsv`, `bakeries.tsv`) confirms that these identical dummy strings are populated across dozens of entries, bypassing genuine data extraction for these columns.

## 2. Logic Chain
- The user explicitly requested that no fake/dummy data or test results be hardcoded.
- Hardcoding qualitative reviews and descriptive features for real places misrepresents the data and violates the integrity of the information retrieval process.
- To resolve this while ensuring the TSV structure is maintained, the fallback logic should default these text fields to empty strings (`""`) or neutral indicators (`"없음"`).
- Boolean columns (`hasPlugs`, `hasDecaf`, `isLargeCafe`, `isPetFriendly`, `has_dine`) can retain `"False"` or `"True"` as their default values since they represent strict binary data rather than fabricated qualitative text.
- Any conditional extraction (e.g., `if "소금빵" in corpus: sig_menu = "소금빵"`) can remain, as it is based on actual search snippet content, but the unconditional fabricated defaults must be removed entirely.

## 3. Caveats
- By defaulting missing fields to `""`, the resulting TSV files will have many blank columns for newly added places. This is a necessary tradeoff to maintain strict data integrity.
- The `heuristic_extract` logic relies on basic keyword matching in DuckDuckGo search snippets. It may fail to capture nuanced information, resulting in many blank fields. The proposed strategy strictly addresses the integrity violation (removing fake data) but does not upgrade the extraction mechanism itself.

## 4. Conclusion
The failure was caused by the unconditional assignment of fabricated strings to qualitative text fields in `process_bookmarks.py`.

**Fix Strategy**:
1. Modify `heuristic_extract` in `process_bookmarks.py` to initialize all qualitative text variables (`ambiance`, `sig_menu`, `menu_feat`, `pos_reviews`, `neg_reviews`, `wait`, `park`, `comp`, `sold_out`) to an empty string `""` by default.
2. Remove the hardcoded `comp = "파리바게뜨|빵 퀄리티|프랜차이즈와 비교할 수 없는 수제 베이커리의 깊은 맛"` in the `is_bakery_flag` condition block.
3. Retain the default `"False"` / `"True"` values for strictly boolean-type fields (`plugs`, `decaf`, `large`, `pet`, `has_dine`).
4. Keep the TSV formatting logic exactly the same. Empty strings will naturally result in consecutive tabs (e.g., `\t\t`), cleanly leaving the TSV columns empty.

## 5. Verification Method
- After the implementer modifies the code, inspect `process_bookmarks.py:47-60` to ensure no dummy Korean text remains and text fields default to `""`.
- Run `python process_bookmarks.py` to re-process the bookmarks.
- Inspect the output using `cat src/main/resources/cafes.tsv | grep "분위기가 좋아요"` – there should be no output for the newly processed lines, confirming the fabricated data is no longer injected. Newly appended rows should display empty columns for missing data.
