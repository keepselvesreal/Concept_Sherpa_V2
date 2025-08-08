# Summary

**메타데이터:**
- ID: 122
- 레벨: 2
- 페이지: 298-299
- 페이지 수: 2
- 부모 ID: 114
- 텍스트 길이: 1333 문자

---

ine data schemas using a language like JSON Schema for function argu-
ments and return values.
 Function argument schemas allow developers to figure out the expected shape of
the function arguments they want to call.
 When invalid data is passed, data validation third-party libraries give meaning-
ful errors with detailed information about the data parts that are not valid.

Summary 271
 Unlike data validation at system boundaries, data validation inside the system is
supposed to run only at development time and should be disabled in production.
 We visualize a data schema by generating a data model diagram out of a JSON
Schema.
 For functions that have data schemas for their arguments and return values, we
can automatically generate schema-based unit tests.
 Data validation is executed at run time.
 We can define advanced data validation conditions that go beyond static types,
like checking whether a number is within a range or if a string matches a regu-
lar expression.
 Data validation inside the system should be disabled in production.
 Records are represented as heterogeneous maps, and indexes are represented as
homogeneous maps.
 When you define a complex data schema, it is advised to store nested schemas
in variables to make the schemas easier to read.
 We treat data validation like unit tests.