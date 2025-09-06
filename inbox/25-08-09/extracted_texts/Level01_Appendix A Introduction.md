# Appendix A Introduction

**Level:** 1
**페이지 범위:** 361 - 363
**총 페이지 수:** 3
**ID:** 148

---

=== 페이지 361 ===
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

=== 페이지 362 ===
334 APPENDIX A Principles of data-oriented programming
Principle #2: Represent Immutable
data with generic data
structures.
Generic
Mutable
Representation
Principle #3:
Specific
Data is
Data immutable.
Schema
Principle #4: Separate
data schema from data
Data-oriented
representation.
programming
Functional
Code
Principle #1: programming
Separate code
from data.
Object-oriented
programming
Figure A.1 The principles of DOP
Notice that DOP principles are language-agnostic. They can be adhered to (or bro-
ken) in
 Object-oriented programming (OOP) languages such as Java, C#, C++, etc.
 Functional programming (FP) languages such as Clojure, OCaml, Haskell, etc.
 Languages that support both OOP and FP such as JavaScript, Python, Ruby,
Scala, etc.
TIP DOP principles are language-agnostic.
 NOTE For OOP developers, the transition to DOP might require more of a mind
shift than for FP developers because DOP prohibits the encapsulation of data in state-
ful classes.
This appendix succinctly illustrates how these principles can be applied or broken in
JavaScript. Mentioned briefly are the benefits of adherence to each principle, and the
costs paid to enjoy those benefits. This appendix also illustrates the principles of DOP
via simple code snippets. Throughout the book, the application of DOP principles to
production information systems is explored in depth.

=== 페이지 363 ===
A.1 Principle #1: Separate code from data 335
A.1 Principle #1: Separate code from data
Principle #1 is a design principle that recommends a clear separation between code
(behavior) and data. This may appear to be a FP principle, but in fact, one can adhere
to it or break it either in FP or in OOP:
 Adherence to this principle in OOP means aggregating the code as methods of
a static class.
 Breaking this principle in FP means hiding state in the lexical scope of a function.
Also, this principle does not relate to the way data is represented. Data representation
is addressed by Principle #2.
PRINCIPLE #1 Separate code from data in a way that the code resides in functions
whose behavior does not depend on data that is encapsulated in the function’s
context.
A.1.1 Illustration of Principle #1
Our exploration of Principle #1 begins by illustrating how it can be applied to OOP
and FP. The following sections illustrate how this principle can be adhered to or bro-
ken in a simple program that deals with:
 An author entity with a firstName, a lastName, and the number of books they
wrote.
 A piece of code that calculates the full name of the author.
 A piece of code that determines if an author is prolific, based on the number of
books they wrote.
BREAKING PRINCIPLE #1 IN OOP
Breaking Principle #1 in OOP happens when we write code that combines data and
code together in an object. The following listing demonstrates what this looks like.
ListingA.1 Breaking Principle #1 in OOP
class Author {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
fullName() {
return this.firstName + " " + this.lastName;
}
isProlific() {
return this.books > 100;
}
}
