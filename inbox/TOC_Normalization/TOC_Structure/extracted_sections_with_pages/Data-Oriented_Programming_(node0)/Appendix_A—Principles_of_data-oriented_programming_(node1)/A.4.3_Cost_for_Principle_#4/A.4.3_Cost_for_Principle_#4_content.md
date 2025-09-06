# A.4.3 Cost for Principle #4

**페이지**: 360-361
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:34

---


--- 페이지 360 ---

332 CHAPTER 15 Debugging
 Reproducibility allows us to reproduce a scenario in a pristine environment.
 The two conditions for reproducibility in programming are immutability and
ease of (de)serialization.
Lodash functions introduced in this chapter
Function Description
find(coll, pred) Iterates over elements of coll, returning the first element for which pred
returns true

--- 페이지 360 끝 ---


--- 페이지 361 ---

appendix A
Principles of data-oriented
programming
Data-oriented programming (DOP) is a programming paradigm aimed at simplify-
ing the design and implementation of software systems, where information is at the
center in systems such as frontend or backend web applications and web services,
for example. Instead of designing information systems around software constructs
that combine code and data (e.g., objects instantiated from classes), DOP encour-
ages the separation of code from data. Moreover, DOP provides guidelines about
how to represent and manipulate data.
TIP In DOP, data is treated as a first-class citizen.
The essence of DOP is that it treats data as a first-class citizen. It gives developers
the ability to manipulate data inside a program with the same simplicity as they
manipulate numbers or strings. Treating data as a first-class citizen is made possible
by adhering to four core principles:
 Separating code (behavior) from data.
 Representing data with generic data structures.
 Treating data as immutable.
 Separating data schema from data representation.
When these four principles are combined, they form a cohesive whole as figure A.1
shows. Systems built using DOP are simpler and easier to understand, so the devel-
oper experience is significantly improved.
TIP In a data-oriented system, code is separated from data. Data is represented
with generic data structures that are immutable and have a separate schema.
333

--- 페이지 361 끝 ---
