# B.4.0 Introduction (사용자 추가)

**페이지**: 370-371
**계층**: Data-Oriented Programming (node0) > Appendix B—Generic data access in statically-typed languages (node1)
**추출 시간**: 2025-08-06 19:47:39

---


--- 페이지 370 ---

342 APPENDIX A Principles of data-oriented programming
this in the sense that it is hard to understand. The system is hard to understand because
there are many dependencies between the entities that compose the system.
The most complex entity of the system in figure A.2 is the Librarian entity, which
is connected via six relations to other entities. Some relations are data relations (asso-
ciation and composition), and some relations are code relations (inheritance and
dependency). But in this design, the Librarian entity mixes code and data, and there-
fore, it has to be involved in both data and code relations. If each entity of the system
is split into a code entity and a data entity without making any further modification to the
system, the result (see figure A.3) is made of two disconnected parts:
 The left part is made only of data entities and data relations: association and
composition.
 The right part is made only of code entities and code relations: dependency
and inheritance.
C LibraryData * C LibrarianData C CatalogCode
*
C MemberData C CatalogData C LibrarianCode
*
C BookData C MemberCode C BookLendingCode C BookItemCode
*
* *
C BookItemData C AuthorData C UserCode C BookItem
*
C BookLendingData
Figure A.3 A class diagram where every class is split into code and data entities
The new system, where code and data are separate, is easier to understand than the
original system, where code and data are mixed. Thus, the data part of the system and
the code part of the system can each be understood on its own.
TIP A system made of disconnected parts is less complex than a system made of a sin-
gle part.
One could argue that the complexity of the original system, where code and data are
mixed, is due to a bad design and that an experienced OOP developer would have
designed a simpler system using smart design patterns. That is true, but in a sense, it is

--- 페이지 370 끝 ---


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
