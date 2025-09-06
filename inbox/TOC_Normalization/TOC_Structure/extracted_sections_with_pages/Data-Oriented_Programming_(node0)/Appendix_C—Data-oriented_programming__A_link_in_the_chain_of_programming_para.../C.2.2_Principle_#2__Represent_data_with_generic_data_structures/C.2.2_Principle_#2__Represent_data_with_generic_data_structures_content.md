# C.2.2 Principle #2: Represent data with generic data structures

**페이지**: 382-383
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:44

---


--- 페이지 382 ---

354 APPENDIX A Principles of data-oriented programming
TIP Adherence to data immutability eliminates the need for a concurrency mecha-
nism. The data you have in hand never changes!
A.3.3 Cost for Principle #3
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
A.3.4 Summary of Principle #3
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

--- 페이지 382 끝 ---


--- 페이지 383 ---

A.4 Principle #4: Separate data schema from data representation 355
 Benefits include
– Data access to all with confidence
– Predictable code behavior
– Fast equality checks
– Concurrency safety for free
 The cost for implementing Principle #3 includes
– A performance hit
– Required library for persistent data structures
A.4 Principle #4: Separate data schema from data
representation
With data separated from code and represented with generic and immutable data
structures, now comes the question of how do we express the shape of the data? In
DOP, the expected shape is expressed as a data schema that is kept separated from the
data itself. The main benefit of Principle #4 is that it allows developers to decide
which pieces of data should have a schema and which pieces of data should not.
PRINCIPLE #4 Separate data schema from data representation.
A.4.1 Illustration of Principle #4
Think about handling a request for the addition of an author to the system. To keep things
simple, imagine that such a request contains only basic information about the author:
their first name and last name and, optionally, the number of books they have written. As
seen in Principle #2 (represent data with generic data structures), in DOP, request data
is represented as a string map, where the map is expected to have three fields:
 firstName—a string
 lastName—a string
 books—a number (optional)
In DOP, the expected shape of data is represented as data that is kept separate from the
request data. For instance, JSON schema (https://json-schema.org/) can represent the
data schema of the request with a map. The following listing provides an example.
ListingA.28 The JSON schema for an addAuthor request data
Data is expected to be a map (in JSON,
a map is called an object).
Only firstName and
var addAuthorRequestSchema = {
lastName fields are
"type": "object",
required.
"required": ["firstName", "lastName"],

--- 페이지 383 끝 ---
