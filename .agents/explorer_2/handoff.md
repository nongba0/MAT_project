# Handoff Report: Code-Only Web Research Strategy

## 1. Observation
- `PROJECT.md` mandates that `process_bookmarks.py` fetches real web data using `duckduckgo_search` to replace 214 randomly generated fake entries in `cafes.tsv` and `bakeries.tsv`. 
- The target TSVs require strictly formatted columns (15 for cafes, 14 for bakeries), notably a `comparisons` column in the `[비교대상]|[비교특징]|[상세설명]` format.
- `import_bookmarks.py` reveals that the currently injected fake data relies on a finite set of hardcoded strings and `random.choice()`.
- The user restriction explicitly prohibits "external non-code tools," meaning we cannot utilize external LLM APIs (e.g., OpenAI, Anthropic) or SaaS products for semantic text parsing.

## 2. Logic Chain
1. **Constraint on Parsing**: Without LLM APIs, we cannot rely on generative AI to implicitly understand and summarize natural language into structured tables. We must rely entirely on deterministic, rule-based Python execution.
2. **Data Acquisition**: The `duckduckgo_search` library (e.g., `DDGS().text("{name} {address} 리뷰", max_results=5)`) returns JSON results containing `title`, `body` (snippets), and `href`.
3. **Corpus Generation**: By concatenating the `body` texts, we get a localized text corpus representing public opinion about the cafe/bakery. The `href` list can be directly collapsed into the `reviewLinks` column.
4. **Heuristic Keyword Extraction**: To extract structured fields (like `positiveReviews`, `ambiance`, `parkingInfo`) from unstructured text, we can apply keyword-based heuristic functions:
   - *Sentiment Splitting*: Split the corpus into clauses. Score them against a Korean positive keyword list (e.g., "맛있다", "친절") and negative keyword list (e.g., "웨이팅", "좁다", "불편"). 
   - *Boolean Feature Flags*: Search for substrings like "디카페인" (hasDecaf), "콘센트/노트북" (hasPlugs), "반려동물/애견" (isPetFriendly). If found, map to `True`, otherwise `False`.
   - *Menu Extraction*: Use basic regex to find nouns adjacent to words like "시그니처" or "대표".
5. **Template-based Comparisons**: Without generative AI, the `comparisons` column cannot be safely synthesized dynamically from scratch. Instead, the strategy maps the highest-frequency ambiance/menu keywords found in the snippet to predefined comparison templates (e.g., if "디저트" is highly mentioned -> `투썸플레이스|디저트|투썸 못지않게 디저트 퀄리티가 훌륭하고 수제 느낌이 강함`).

## 3. Caveats
- Search snippets (`body`) are truncated and may not contain complete sentences, making regex matching sometimes brittle or resulting in false negatives for features like parking and decaf.
- Simple substring matching for Korean text can lead to false positives due to conjugations or negations (e.g., "주차장이 없지 않다").
- This strategy heavily relies on the assumption that DuckDuckGo search snippets will consistently surface the needed attributes. Fallback default values (e.g., "정보 없음") will be strictly required to prevent the pipeline from crashing.

## 4. Conclusion
The most robust alternative for the Data Pipeline is a **Heuristic NLP Extraction Strategy**. The script should fetch DuckDuckGo snippets, aggregate them, and route the text through a series of deterministic Python functions utilizing predefined keyword lists, regex, and static templates. This guarantees adherence to the strict TSV formats and completely eliminates the need for external APIs.

## 5. Verification Method
1. Write a prototype Python script using `duckduckgo_search`.
2. Execute `DDGS().text("소울브레드 서울 서초구 바우뫼로7길 27 리뷰", max_results=5)`.
3. Pass the concatenated `body` results to the heuristic extractor functions.
4. Assert that the output dictionary successfully contains all keys (e.g., `hasPlugs`, `comparisons`, `positiveReviews`) without throwing exceptions.
5. Assert that the generated `comparisons` field strictly matches the required regex pattern `^.+\|.+\|.*$`.
