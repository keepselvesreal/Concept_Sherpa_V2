# Summary

**메타데이터:**
- ID: 193
- 레벨: 1
- 페이지: 408-408
- 페이지 수: 1
- 부모 ID: 174
- 텍스트 길이: 2103 문자

---

endix has presented various ways to provide generic data access in statically-
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