# C.2.4 Principle #4: Separate data schema from data representation

**메타데이터:**
- ID: 209
- 레벨: 2
- 페이지: 413-412
- 페이지 수: 0
- 부모 ID: 204
- 텍스트 길이: 626 문자

---

#4: Separate data schema from data representation
One of the more virulent critiques against dynamically-typed programming languages
was related to the lack of data validation. The answer that dynamically-typed lan-
guages used to give to this critique was that you trade data safety for data flexibility.
Since the development of data schema languages like JSON Schema (https://json-
schema.org/), it is natural to validate data even when data is represented as hash
maps. As we saw in chapters 7 and 12, data validation is not only possible, but in some
sense, it is more powerful than when data is represented with classes.