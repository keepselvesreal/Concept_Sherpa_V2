# Appendix B Introduction

**메타데이터:**
- ID: 175
- 레벨: 1
- 페이지: 392-393
- 페이지 수: 2
- 부모 ID: 174
- 텍스트 길이: 906 문자

---

ic data access in
statically-typed languages
Representing data with generic data structures fits naturally in dynamically-typed
programming languages like JavaScript, Ruby, or Python. However, in statically-
typed programming languages like Java or C#, representing data as string maps
with values of an unspecified type is not natural for several reasons:
 Accessing map fields requires a type cast.
 Map field names are not validated at compile time.
 Autocompletion and other convenient IDE features are not available.
This appendix explores various ways to improve access to generic data in statically-
typed languages. We’ll look at:
 Value getters for maps to avoid type casting when accessing map fields
 Typed getters for maps to benefit from compile-time checks for map field
names
 Generic access for classes using reflection to benefit from autocompletion
and other convenient IDE features