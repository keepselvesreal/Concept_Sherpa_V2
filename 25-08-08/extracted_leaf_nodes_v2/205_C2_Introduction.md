# C.2 Introduction

**메타데이터:**
- ID: 205
- 레벨: 2
- 페이지: 412-413
- 페이지 수: 2
- 부모 ID: 204
- 텍스트 길이: 9371 문자

---

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

=== Page 412 ===
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

=== Page 413 ===
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

=== Page 414 ===
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