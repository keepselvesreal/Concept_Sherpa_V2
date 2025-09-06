# C.1 Time line

**Level:** 1
**페이지 범위:** 409 - 410
**총 페이지 수:** 2
**ID:** 196

---

=== 페이지 409 ===
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

=== 페이지 410 ===
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
