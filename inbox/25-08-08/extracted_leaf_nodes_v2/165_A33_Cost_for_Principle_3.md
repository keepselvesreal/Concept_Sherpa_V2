# A.3.3 Cost for Principle #3

**메타데이터:**
- ID: 165
- 레벨: 2
- 페이지: 382-381
- 페이지 수: 0
- 부모 ID: 161
- 텍스트 길이: 1266 문자

---

rinciple #3
As with the previous principles, applying Principle #3 comes at a price. The following
sections look at these costs:
 Performance hit
 Required library for persistent data structures
COST #1: PERFORMANCE HIT
As mentioned earlier, implementations of persistent data structures exist in most pro-
gramming languages. But even the most efficient implementation is a bit slower than
the in-place mutation of the data. In most applications, the performance hit and the
additional memory consumption involved in using immutable data structures is not
significant. But this is something to keep in mind.
COST #2: REQUIRED LIBRARY FOR PERSISTENT DATA STRUCTURES
In a language like Clojure, the native data structures of the language are immutable. How-
ever, in most programming languages, adhering to data immutability requires the inclu-
sion a third-party library that provides an implementation of persistent data structures.
The fact that the data structures are not native to the language means that it is dif-
ficult (if not impossible) to enforce the usage of immutable data across the board.
Also, when integrating with third-party libraries (e.g., a chart library), persistent data
structures must be converted into equivalent native data structures.