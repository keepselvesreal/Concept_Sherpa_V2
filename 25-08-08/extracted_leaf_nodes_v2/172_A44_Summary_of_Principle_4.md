# A.4.4 Summary of Principle #4

**메타데이터:**
- ID: 172
- 레벨: 2
- 페이지: 390-390
- 페이지 수: 1
- 부모 ID: 167
- 텍스트 길이: 1085 문자

---

Principle #4
In DOP, data is represented with immutable generic data structures. When additional
information about the shape of the data is required, a data schema can be defined
(e.g., using JSON Schema). Keeping the data schema separate from the data repre-
sentation gives us the freedom to decide where data should be validated.
Moreover, data validation occurs at run time. As a consequence, data validation
conditions that go beyond the static data types (e.g., the string length) can be expressed.
However, with great power comes great responsibility, and it is up to the developer to
remember to validate data.
DOP Principle #4: Separate between data schema and data representation
To adhere to this principle, separate between data schema and data representation.
The following diagram illustrates this.
DOPPrinciple #4: Separate between data
schema and data representation
Representation
Data
Schema
 Benefits include
– Freedom to choose what data should be validated
– Optional fields
– Advanced data validation conditions
– Automatic generation of data model visualization