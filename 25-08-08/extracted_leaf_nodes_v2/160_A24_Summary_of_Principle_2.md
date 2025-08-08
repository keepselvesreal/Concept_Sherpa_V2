# A.2.4 Summary of Principle #2

**메타데이터:**
- ID: 160
- 레벨: 2
- 페이지: 378-378
- 페이지 수: 1
- 부모 ID: 155
- 텍스트 길이: 1264 문자

---

Principle #2
DOP uses generic data structures to represent data. This might cause a (small) perfor-
mance hit and impose the need to manually document the shape of data because the
compiler cannot validate it statically. Adherence to this principle enables the manipu-
lation of data with a rich set of generic functions (provided by the language and by
third-party libraries). Additionally, our data model is flexible. At this point, the data
can be either mutable or immutable. The next principle (Principle #3) illustrates the
value of immutability.
DOP Principle #2: Represent data with generic data structures
To comply with this principle, we represent application data with generic data struc-
tures, mostly maps and arrays (or lists). The following diagram shows a visual repre-
sentation of this principle.
DOPPrinciple #2: Represent data with generic data structures
Specific
Data
Generic
 Benefits include
– Using generic functions that are not limited to our specific use case
– A flexible data model
 The cost for implementing this principle includes
– There is a slight performance hit.
– No data schema is required.
– No compile time check that the data is valid is necessary.
– In some statically-typed languages, explicit type casting is needed.