# B.3.1 Accessing non-nested map fields with typed getters

**페이지**: 369-370
**계층**: Data-Oriented Programming (node0) > Appendix B—Generic data access in statically-typed languages (node1)
**추출 시간**: 2025-08-06 19:47:38

---


--- 페이지 369 ---

A.1 Principle #1: Separate code from data 341
TIP Writing tests is easier when code is separated from data.
BENEFIT #3: SYSTEMS TEND TO BE LESS COMPLEX
The third benefit of applying Principle #1 to our programs is that systems tend to be less
complex. This benefit is the deepest one but also the one that is most subtle to explain.
The type of complexity I refer to is the one that makes systems hard to understand
as defined in the paper, “Out of the Tar Pit,” by Ben Moseley and Peter Marks (http://
mng.bz/enzq). It has nothing to do with the complexity of the resources consumed by
a program. Similarly, references to simplicity mean not complex (in other words, easy to
understand).
 NOTE Complex in the context of this book means hard to understand.
Keep in mind that complexity and simplicity (like hard and easy) are not absolute but
relative concepts. The complexity of two systems can be compared to determine
whether system A is more complex (or simpler) than system B. When code and data
are kept separate, the system tends to be easier to understand for two reasons:
 The scope of a data entity or a code entity is smaller than the scope of an entity that com-
bines code and data. Each entity is therefore easier to understand.
 Entities of the system are split into disjoint groups: code and data. Entities therefore
have fewer relations to other entities.
This insight is illustrated in a class diagram of our fictitious Library Management Sys-
tem, where code and data are mixed. It is not necessary to know the details of the
classes of this system to see that the diagram in figure A.2 represents a complex system;
C Library
C Catalog
* *
C Book C Librarian
*
*
C Member
*
C Author
C BookItem C User
Figure A.2 A class
diagram overview for the
C BookLending * Library Management
System

--- 페이지 369 끝 ---


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
