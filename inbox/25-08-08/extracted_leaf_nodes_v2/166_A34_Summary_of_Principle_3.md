# A.3.4 Summary of Principle #3

**메타데이터:**
- ID: 166
- 레벨: 2
- 페이지: 382-382
- 페이지 수: 1
- 부모 ID: 161
- 텍스트 길이: 617 문자

---

Principle #3
DOP considers data as a value that never changes. Adherence to this principle results
in code that is predictable even in a multi-threaded environment, and equality checks
are fast. However, a non-negligible mind shift is required, and in most programming
languages, a third-party library is needed to provide an efficient implementation of
persistent data structures.
DOP Principle #3: Data is immutable
To adhere to this principle, data is represented with immutable structures. The fol-
lowing diagram provides a visual representation of this.
DOPPrinciple #3: Data is immutable
Mutable
Data
Immutable