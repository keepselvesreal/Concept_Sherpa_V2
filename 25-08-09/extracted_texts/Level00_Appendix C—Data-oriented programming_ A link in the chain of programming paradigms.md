# Appendix C—Data-oriented programming: A link in the chain of programming paradigms

**Level:** 0
**페이지 범위:** 409 - 414
**총 페이지 수:** 6
**ID:** 194

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

=== 페이지 411 ===
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

=== 페이지 412 ===
384 APPENDIX C Data-oriented programming: A link in the chain of programming paradigms
DOP is the combination of those principles into a cohesive whole. In this section, we
put each of the four DOP principles into its broader scope.
C.2.1 Principle #1: Separate code from data
Separating code from data used to be the main point of contention between OOP and
FP. Traditionally, in OOP we encapsulate data together with code in stateful objects,
while in FP, we write stateless functions that receive data they manipulate as an explicit
argument.
This tension has been reduced over the years as it is possible in FP to write stateful
functions with data encapsulated in their lexical scope (https://developer.mozilla
.org/en-US/docs/Web/JavaScript/Closures). Moreover, OOP languages like Java and
C# have added support for anonymous functions (lambdas).
C.2.2 Principle #2: Represent data with generic data structures
One of the main innovations of JavaScript when it was released in December 1995
was the ease of creating and manipulating hash maps via object literals. The increas-
ing popularity of JavaScript over the years as a language used everywhere (frontend,
backend, and desktop) has influenced the developer community to represent data
with hash maps when possible. It feels more natural in dynamically-typed program-
ming languages, but as we saw in appendix B, it is applicable also in statically-typed
programming languages.
C.2.3 Principle #3: Data is immutable
Data immutability is considered a best practice as it makes the behavior of our pro-
gram more predictable. For instance, in the book Effective Java (O’Reilly, 2017; http://
mng.bz/5K81), Joshua Bloch mentions “minimize mutability” as one of Java best prac-
tices. There is a famous quote from Alan Kay, who is considered by many as the inven-
tor of OOP, about the value of immutability:
The last thing you wanted any programmer to do is mess with internal state even if presented
figuratively. Instead, the objects should be presented as sites of higher level behaviors more
appropriate for use as dynamic components....It is unfortunate that much of what is called
"object-oriented programming" today is simply old style programming with fancier constructs.
Many programs are loaded with “assignment-style” operations now done by more expensive
attached procedures.
—Alan C. Kay (“The Early History of Smalltalk,” 1993)
Unfortunately, until 2007 and the implementation of efficient persistent data struc-
tures in Clojure, immutability was not applicable for production applications at scale.
As we mentioned in chapter 9, nowadays, efficient persistent data structures are avail-
able in most programming languages. These are summarized in table C.1.

=== 페이지 413 ===
C.3 DOP and other data-related paradigms 385
Table C.1 Persistent data structure libraries
Language Library
Java Paguro (https://github.com/GlenKPeterson/Paguro)
C# Provided by the language (http://mng.bz/y4Ke)
JavaScript Immutable.js (https://immutable-js.com/)
Python Pyrsistent (https://github.com/tobgu/pyrsistent)
Ruby Hamster (https://github.com/hamstergem/hamster)
In addition, many languages provide support for read-only objects natively. Java added
record classes in Java 14 (http://mng.bz/q2q2). C# introduced a record type in C# 9.
There is a ECMAScript proposal for supporting immutable records and tuples in
JavaScript (https://github.com/tc39/proposal-record-tuple). Finally, Python 3.7 intro-
duced immutable data classes (https://docs.python.org/3/library/dataclasses.html).
C.2.4 Principle #4: Separate data schema from data representation
One of the more virulent critiques against dynamically-typed programming languages
was related to the lack of data validation. The answer that dynamically-typed lan-
guages used to give to this critique was that you trade data safety for data flexibility.
Since the development of data schema languages like JSON Schema (https://json-
schema.org/), it is natural to validate data even when data is represented as hash
maps. As we saw in chapters 7 and 12, data validation is not only possible, but in some
sense, it is more powerful than when data is represented with classes.
C.3 DOP and other data-related paradigms
In this section, we clarify the distinction between DOP and two other programming
paradigms whose names also contain the word data: data-oriented design and data-
driven programming.
There are only two hard things in Computer Science: cache invalidation and naming things.
—Phil Karlton
Each paradigm has a its own objective and pursues it by focusing on a different aspect
of data. Table C.2 summarizes the objectives, and we’ll dive into each a bit more in the
following sections.
Table C.2 Data-related paradigms: Objectives and main data aspect focus
Paradigm Objective Main data aspect focus
Data-oriented design Increase performance Data layout
Data-driven programming Increase clarity Behavior described by data
Data-oriented programming Reduce complexity Data representation

=== 페이지 414 ===
386 APPENDIX C Data-oriented programming: A link in the chain of programming paradigms
C.3.1 Data-oriented design
Data-oriented design is a program optimization approach motivated by efficient usage
of the CPU cache. It’s used mostly in video game development. This approach focuses
on the data layout, separating and sorting fields according to when they are needed,
and encourages us to think about data transformations. In this context, what’s import-
ant is how the data resides in memory. The objective of this paradigm is to improve
the performance of the system.
C.3.2 Data-driven programming
Data-driven programming is the idea that you create domain specific languages (DSLs)
made out of descriptive data. It is a branch of declarative programming. In this context,
what’s important is to describe the behavior of a program in terms of data. The objective
of this paradigm is to increase code clarity and to reduce the risk of bugs related to mis-
takes in the implementation of the expected behavior of the program.
C.3.3 Data-oriented programming (DOP)
As we have illustrated in this book, DOP is a paradigm that treats system data as a first-
class citizen. Data is represented by generic immutable data structures like maps and
vectors that are manipulated by general-purpose functions like map, filter, select, group,
sort, and so forth. In this context, what’s important is the representation of data by the
program. The objective of this paradigm is to reduce the complexity of the system.
Summary
In this appendix, we have explored the ideas and trends that have inspired DOP. We
looked at the discoveries that made it applicable in production systems at scale in
most programming languages.
