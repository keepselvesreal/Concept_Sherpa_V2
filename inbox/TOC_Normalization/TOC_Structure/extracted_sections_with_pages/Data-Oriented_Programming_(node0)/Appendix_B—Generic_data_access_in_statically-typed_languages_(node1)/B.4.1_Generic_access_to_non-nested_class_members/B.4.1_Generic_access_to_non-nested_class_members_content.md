# B.4.1 Generic access to non-nested class members

**페이지**: 371-372
**계층**: Data-Oriented Programming (node0) > Appendix B—Generic data access in statically-typed languages (node1)
**추출 시간**: 2025-08-06 19:47:39

---


--- 페이지 371 ---

A.1 Principle #1: Separate code from data 343
irrelevant. The point of Principle #1 is that a system made of entities that do not com-
bine code and data tends to be simpler than a system made of entities that do combine
code and data.
It has been said many times that simplicity is hard. According to the first principle of
DOP, simplicity is easier to achieve when separating code and data.
TIP Simplicity is easier to achieve when code is separated from data.
A.1.3 Cost for Principle #1
This section looks at the cost involved when we implement Principle #1. The price we
pay in order to benefit from the separation between code and data is threefold:
 There is no control on what code can access what data.
 There is no packaging.
 Our systems are made from more entities.
COST #1: THERE IS NO CONTROL ON WHAT CODE CAN ACCESS WHAT DATA
When code and data are mixed, it is easy to understand what pieces of code can access
what kinds of data. For example, in OOP, the data is encapsulated in an object, which
guarantees that the data is accessible only by the object’s methods. In DOP, data
stands on its own. It is transparent if you like, and as a consequence, it can be accessed
by any piece of code.
When refactoring the shape of some data, every place in our code that accesses this
kind of data must be known. Moreover, without the application of Principle #3 (enforc-
ing data immutability), which we discuss later, accessing data by any piece of code is
inherently unsafe. In that case, it would be hard to guarantee the validity of our data.
TIP Data safety is ensured by another principle (Principle #3) that enforces data
immutability.
COST #2: THERE IS NO PACKAGING
One of the benefits of mixing code and data is that when you have an object in hand,
it is a package that contains both the code (via methods) and the data (via members).
As a consequence, it is easy to discover how to manipulate the data: you look at the
methods of the class.
In DOP, the code that manipulates the data could be anywhere. For example,
createAuthorData might be in one file and fullName in another file. This makes it
difficult for developers to discover that the fullName function is available. In some sit-
uations, it could lead to wasted time and unnecessary code duplication.
COST #3: OUR SYSTEMS ARE MADE FROM MORE ENTITIES
Let’s do simple arithmetic. Imagine a system made of N classes that combine code and
data. When you split the system into code entities and data entities, you get a system
made of 2N entities. This calculation is not accurate, however, because usually when
you separate code and data, the class hierarchy tends to get simpler as we need less

--- 페이지 371 끝 ---


--- 페이지 372 ---

344 APPENDIX A Principles of data-oriented programming
class inheritance and composition. Therefore, the number of classes in the resulting
system will probably be somewhere between N and 2N.
On one hand, when adhering to Principle #1, the entities of the system are sim-
pler. On the other hand, there are more entities. This cost is mitigated by Principle
#2, which guides us to represent our data with generic data structures.
TIP When adhering to Principle #1, systems are made of simpler entities, but there
are more of them.
A.1.4 Summary of Principle #1
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

--- 페이지 372 끝 ---
