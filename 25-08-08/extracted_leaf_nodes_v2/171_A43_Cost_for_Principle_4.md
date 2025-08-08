# A.4.3 Cost for Principle #4

**메타데이터:**
- ID: 171
- 레벨: 2
- 페이지: 389-389
- 페이지 수: 1
- 부모 ID: 167
- 텍스트 길이: 1417 문자

---

rinciple #4
Applying Principle #4 comes with a price. The following sections look at these costs:
 Weak connection between data and its schema
 Small performance hit
COST #1: WEAK CONNECTION BETWEEN DATA AND ITS SCHEMA
By definition, when data schema and data representation are separated, the connec-
tion between data and its schema is weaker than when data is represented with classes.
Moreover, the schema definition language (e.g., JSON Schema) is not part of the

362 APPENDIX A Principles of data-oriented programming
programming language. It is up to the developer to decide where data validation is
necessary and where it is superfluous. As the idiom says, with great power comes great
responsibility.
COST #2: LIGHT PERFORMANCE HIT
As mentioned earlier, implementations of JSON schema validation exist in most
programming languages. In DOP, data validation occurs at run time, and it takes
some time to run the data validation. In OOP, data validation usually occurs at com-
pile time.
This drawback is mitigated by the fact that, even in OOP, some parts of data valida-
tion occur at run time. For instance, the conversion of a request JSON payload into an
object occurs at run time. Moreover, in DOP, it is quite common to have some data val-
idation parts enabled only during development and to disable them when the system
runs in production. As a consequence, this performance hit is not significant.