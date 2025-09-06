# C.2.1 Principle #1: Separate code from data

**메타데이터:**
- ID: 206
- 레벨: 2
- 페이지: 412-411
- 페이지 수: 0
- 부모 ID: 204
- 텍스트 길이: 603 문자

---

#1: Separate code from data
Separating code from data used to be the main point of contention between OOP and
FP. Traditionally, in OOP we encapsulate data together with code in stateful objects,
while in FP, we write stateless functions that receive data they manipulate as an explicit
argument.
This tension has been reduced over the years as it is possible in FP to write stateful
functions with data encapsulated in their lexical scope (https://developer.mozilla
.org/en-US/docs/Web/JavaScript/Closures). Moreover, OOP languages like Java and
C# have added support for anonymous functions (lambdas).