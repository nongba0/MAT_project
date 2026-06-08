# Handoff Report

## Observation
- `import_bookmarks.py` added 214 fake rows to `cafes.tsv` and `bakeries.tsv` by reading `hong_bookmarks.json` and adding entries where `name` was not already in the TSVs.
- The headers for `cafes.tsv` have 17 columns (15 original + latitude + longitude). The headers for `bakeries.tsv` have 14 columns (12 original + latitude + longitude).
- Existing valid rows in `cafes.tsv` (first 30 lines) have exactly 15 columns (no lat/long), and `bakeries.tsv` has 12 columns. The Java seeders `CafeSeeder.java` and `BakerySeeder.java` use `String[] data = line.split("\t", -1);` and safely check length (e.g., `data.length > 15`) before parsing latitude and longitude, preventing `ArrayIndexOutOfBoundsException`.
- The `comparisons` column format is strictly `[비교대상]|[비교특징]|[상세설명]`.
- Positive reviews are separated by `|`.
- Booleans in `cafes.tsv` are Title case (`True/False`) while in `bakeries.tsv` they are lowercase (`true/false`), though `Boolean.parseBoolean` is case-insensitive.
- We tested `mvnw.cmd clean test` which ran successfully, inserting seeded data into the database.

## Logic Chain
1. **Data Cleaning Strategy**: To remove the 214 fake entries, we can read the `name` values from `hong_bookmarks.json` and filter out any TSV rows (excluding headers) that match these names. This leaves precisely the 30 valid entries.
2. **Web Research Strategy**: For the 214 JSON bookmarks, we determine category using the `is_bakery(name, memo, cidPath)` logic. We query `duckduckgo-search` using the name and address to get snippets. We use an LLM (e.g., `google.generativeai`) to structure the data to fit the exact columns.
3. **Format Alignment**: We must map extracted data to 17 fields for cafes and 14 for bakeries. We use `py` for latitude and `px` for longitude from the JSON to populate the final two columns.
4. **Edge Case Handling**: 
   - TSV corruption: We must replace any `\n` or `\t` in the LLM output with spaces.
   - Missing columns: We must ensure all 17/14 fields are printed with `\t`, even if empty.
   - Strict formats: We must validate that `comparisons` contains exactly two `|` characters, and `positive_reviews` uses `|` as a delimiter. If the LLM fails, we fallback to a default structure to avoid breaking the Java split logic.

## Caveats
- `duckduckgo_search` may occasionally fail or rate-limit. We need error handling (try/except) and a default fallback row for failed searches.
- The Java parser expects `data.length >= 12` for bakeries. If the TSV writer produces fewer tabs, it skips the row. We must guarantee the correct number of tabs.

## Conclusion
The data pipeline script `process_bookmarks.py` should implement the following steps:
1. Load `hong_bookmarks.json` and extract the 214 target names.
2. Filter `cafes.tsv` and `bakeries.tsv` to remove rows matching those names, leaving the valid entries.
3. Loop through the 214 bookmarks, use `is_bakery` to classify them, search web snippets, and format data using LLM.
4. Sanitize the output (strip `\t` and `\n`), ensure `|` delimiters are correct for `comparisons` and reviews, and append `py` and `px` as the final two columns.
5. Append the generated rows to the TSVs.

## Verification Method
1. Run `python process_bookmarks.py`.
2. Inspect `cafes.tsv` and `bakeries.tsv` visually to ensure lines do not break into unexpected newlines.
3. Run `.\mvnw.cmd clean test` in `C:\Users\sangw\.gemini\antigravity\scratch\web-service`. If the DB seeders load the entries without `ArrayIndexOutOfBoundsException` or `NumberFormatException`, the pipeline format is correct.
