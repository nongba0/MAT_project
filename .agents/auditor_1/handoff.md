## Forensic Audit Report

**Work Product**: `process_bookmarks.py`, `src/main/resources/cafes.tsv`, `src/main/resources/bakeries.tsv`
**Profile**: General Project
**Verdict**: CLEAN

### Phase Results
- [Hardcoded string detection]: PASS — Verified `process_bookmarks.py` `heuristic_extract()` uses regex and keyword matching against `corpus` using `extract_sentences()`. It falls back to `"리뷰 정보 없음"`, `"정보 없음"`, `"부정적 리뷰 없음"` rather than hardcoded fake reviews.
- [TSV Duplicate Dummy Review detection]: PASS — Checked `cafes.tsv` and `bakeries.tsv`. The newly added entries have either extracted sentences from DuckDuckGo search or `"리뷰 정보 없음"`, `"정보 없음"` etc. The previous `"분위기가 좋아요|커피가 맛있어요|직원이 친절해요"` strings no longer exist in the TSV outputs or the python script.
- [Fallback behavior check]: PASS — When the extraction logic (`extract_sentences`) fails to find matching keywords, it falls back to `"리뷰 정보 없음"` etc., which gracefully handles missing information without circumventing the extraction step.

### Evidence
1. **Observation 1**: `process_bookmarks.py:47-54`
   ```python
    def extract_sentences(corp, keywords):
        sentences = re.split(r'[.!?\n]+', corp)
        matches = []
        for s in sentences:
            s = s.strip()
            if any(kw in s for kw in keywords) and len(s) > 5:
                matches.append(s)
        return list(dict.fromkeys(matches))
   ```
   This performs genuine keyword matching and extraction.
2. **Observation 2**: `process_bookmarks.py:56-64`
   ```python
    pos_kws = ["맛있", "좋", "친절", "최고", "추천", "완벽", "훌륭"]
    pos_sentences = extract_sentences(corpus, pos_kws)
    pos_reviews = "|".join(pos_sentences[:3]) if pos_sentences else "리뷰 정보 없음"

    neg_kws = ["아쉽", "비싸", "불친절", "대기", "웨이팅", "시끄럽", "좁", "오래"]
    neg_sentences = extract_sentences(corpus, neg_kws)
    neg_reviews = neg_sentences[0] if neg_sentences else "부정적 리뷰 없음"
   ```
   This implements the required fallback mechanism cleanly.
3. **Observation 3**: `cafes.tsv`
   Row 31: `비캔드	서울 마포구 포은로 71-12	분위기 정보 없음	정보 없음	특징 정보 없음	리뷰 정보 없음	부정적 리뷰 없음`
   Row 32: `오하하하우스	경기 수원시 팔달구 덕영대로895번길 9-6	오늘은 수원에서 두쫀쿠로 아주 유명한 ‘오하하하우스’의 두쫀쿠 리뷰를 들고 왔셔요	정보 없음	특징 정보 없음	오하하하우스...`
   These show that fallback works and real extractions exist instead of dummy strings.
4. **Observation 4**: `grep` check
   Searching for `분위기가 좋아요|커피가 맛있어요|직원이 친절해요` and `신선한 재료로 만든 디저트` across the project files yielded 0 matches in the source code (`process_bookmarks.py`) or the TSVs (`cafes.tsv`, `bakeries.tsv`).

### Conclusion
The code legitimately parses external corpus for target information using heuristic parsing rules and uses graceful fallback flags when data is absent. Integrity violation resolved. The project is CLEAN.
