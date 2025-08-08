# C.1 Introduction

**메타데이터:**
- ID: 197
- 레벨: 2
- 페이지: 409-410
- 페이지 수: 2
- 부모 ID: 196
- 텍스트 길이: 6687 문자

---

=== Page 408 ===
380 APPENDIX B Generic data access in statically-typed languages
Summary
This appendix has presented various ways to provide generic data access in statically-
typed programming languages. Table B.1 summarizes the benefits and drawbacks of
each approach. As you incorporate DOP practices in your programs, remember that
data can be represented either as string maps or as classes (or records) and benefits
from generic data access via:
 Dynamic getters
 Value getters
 Typed getters
 Reflection
Table B.1 Various ways to provide generic data access in statically-typed programming languages
Approach Representation Benefits Drawbacks
Dynamic getters Map Generic access Requires type casting
Value getters Map No type casting Implementation per type
Typed getters Map Compile-time validation on No compile-time validation
usage on creation
Reflection Class Full compile-time validation Not modifiable

=== Page 409 ===
appendix C
Data-oriented programming:
A link in the chain of
programming paradigms
Data-oriented programming (DOP) has its origins in the 1950s with the invention
of the programming language Lisp. DOP is based on a set of best practices that can
be found in both functional programming (FP) and object-oriented programming
(OOP). However, this paradigm has only been applicable in production systems at
scale since the 2010s with the implementation of efficient persistent data struc-
tures. This appendix traces the major ideas and discoveries which, over the years,
have led to the emergence of DOP (see figure C.1).
C.1 Time line
C.1.1 1958: Lisp
With Lisp, John McCarthy had the ingenious idea to represent data as generic
immutable lists and to invent a language that made it natural to create lists and to
access any part of a list. That’s the reason why Lisp stands for LISt Processing.
In a way, Lisp lists are the ancestors of JavaScript object literals. The idea that it
makes sense to represent data with generic data structures (DOP Principle #2) defi-
nitely comes from Lisp.
The main limitation of Lisp lists is that when we update a list, we need to create
a new version by cloning it. This has a negative impact on performance both in
terms of CPU and memory.
381

=== Page 410 ===
382 APPENDIX C Data-oriented programming: A link in the chain of programming paradigms
LISP
John McCarthy invents a
1958
language designed for
processing immutable lists.
Values and Objects
In his beautiful paper“Values and Objects
1981 in Programming Languages,”Bruce
MacLennan clarifies the distinction between
values (immutable) and objects (stateful).
Ideal Hash Trees
Phil Bagwell invents a data
2000
structure with nearly ideal
characteristics.
Out of the Tar Pit
Ben Moseley and Peter Marks define
complexity as“what makes a system
2006
hard to understand”and suggest
various ways to reduce complexity in
Clojure software systems.
Rich Hickey invents a
language designed for reducing
2007
complexity of information
systems with immutability
at its core.
Immutability for all
Persistent data structures
2009
are ported from Clojure to
other languages.
Figure C.1 DOP time line
C.1.2 1981: Values and objects
In a short and easy-to-read paper, named “Values and Objects in Programming Lan-
guages,” Bruce MacLennan clarifies the distinction between values and objects. In a
nutshell,
 Values (for instance, numbers) are timeless abstractions for which the concepts
of updating, sharing, and instantiation have no meaning.
 Objects (for instance, an employee object in a human resource software system)
exist in time and, hence, can be created, destroyed, copied, shared, and updated.
 NOTE The meaning of the term object in this paper is not exactly the same as in the
context of OOP.
The author explains why it’s much simpler to write code that deals with values than to
write code that deals with objects. This paper has been a source of inspiration for DOP
as it encourages us to implement our systems in such a way that most of our code deals
with values. You can read the full text of this paper at http://mng.bz/7WNy.

=== Page 411 ===
C.2 DOP principles as best practices 383
C.1.3 2000: Ideal hash trees
Phil Bagwell invented a data structure called Hash Array Mapped Trie (HAMT). In his
paper, “Ideal Hash Trees,” he used HAMT to implement hash maps with nearly ideal
characteristics both in terms of computation and memory usage. As we illustrated in
chapter 9, HAMT and ideal hash trees are the foundation of efficient persistent data
structures. See https://lampwww.epfl.ch/papers/idealhashtrees.pdf to read his tech-
nical paper.
C.1.4 2006: Out of the Tar Pit
In their paper, “Out of the Tar Pit,” Ben Moseley and Peter Marks claim that complex-
ity is the single major difficulty in the development of large-scale software systems. In
the context of their paper, complexity means “that which makes large systems hard to
understand.”
The main insight of the authors is that most of the complexity of software systems
in not essential but accidental: the complexity doesn’t come from the problem we
have to solve but from the software constructs we use to solve the problem. They sug-
gest various ways to reduce complexity of software systems.
In a sense, DOP is a way to get us out of the tar pit. See http://mng.bz/mxq2 to
download a copy of this term paper.
C.1.5 2007: Clojure
Rich Hickey, an OOP expert, invented Clojure to make it easier to develop informa-
tion systems at scale. Rich Hickey likes to summarize Clojure’s core value with the
phrase, “Just use maps!” By maps, he means immutable maps to be manipulated effi-
ciently by generic functions. Those maps were implemented using the data structures
presented by Phil Bagwell in his paper, “Ideal Hash Trees.”
Clojure has been the main source of inspiration for DOP. In a sense, this book is a
formalization of the underlying principles of Clojure and how to apply them in other
programming languages.
C.1.6 2009: Immutability for all
Clojure’s efficient implementation of persistent data structures has been attractive for
developers from other programming languages. In 2009, these structures were ported
to Scala. Over the years, they have been ported to other programming languages as
well, either by organizations like Facebook for Immutable.js, or by individual contrib-
utors like Glen Peterson for Paguro in Java. Nowadays, DOP is applicable in virtually
any programming language!
C.2 DOP principles as best practices
The principles of DOP as we have presented them through the book (and formalized
in appendix A) are not new. They come from best practices that are well known
among software developers from various programming languages. The innovation of