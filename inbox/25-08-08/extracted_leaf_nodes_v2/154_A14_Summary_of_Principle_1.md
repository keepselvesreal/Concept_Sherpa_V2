# A.1.4 Summary of Principle #1

**메타데이터:**
- ID: 154
- 레벨: 2
- 페이지: 372-372
- 페이지 수: 1
- 부모 ID: 149
- 텍스트 길이: 1265 문자

---

Principle #1
DOP requires the separation of code from data. In OOP languages, aggregate code in
static methods and data in classes with no methods. In FP languages, avoid hiding data
in the lexical scope of functions.
Separating code from data comes at a price. It reduces control over what pieces of
code access our data and can cause our systems to be made of more entities. But it’s
worth paying the price because, when adhering to this principle, our code can be
reused in different contexts in a straightforward way and tested in isolation. Moreover,
a system made of separate entities for code and data tends to be easier to understand.
DOP Principle #1: Separate code from data
To follow this principle, we separate code from data in such a way that the code
resides in functions whose behavior does not depend on data that is encapsulated
in the function’s context. The following diagram provides a visual representation
of this.
DOPPrinciple #1: Separate code from data
FP
Code
System OOP
Data
 Benefits include
– Code can be reused in different contexts.
– Code can be tested in isolation.
– Systems tend to be less complex.
 The cost for implementing Principle #1 includes
– No control on what code accesses which data.
– No packaging.
– More entities.