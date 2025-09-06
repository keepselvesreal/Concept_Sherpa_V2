# C.3 Introduction

**메타데이터:**
- ID: 211
- 레벨: 2
- 페이지: 413-414
- 페이지 수: 2
- 부모 ID: 210
- 텍스트 길이: 7941 문자

---

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

=== Page 415 ===
appendix D
Lodash reference
Throughout the book, we have used Lodash (https://lodash.com/) to illustrate
how to manipulate data with generic functions. But there is nothing unique about
Lodash. The exact same approach could be implemented via other data manipula-
tion libraries or custom code.
Moreover, we used Lodash FP (https://github.com/lodash/lodash/wiki/FP-
Guide) to manipulate data without mutating it. By default, the order of the argu-
ments in immutable functions is shuffled. The code in listing D.1 is needed when
configuring Lodash in order to ensure the signature of the immutable functions is
exactly the same as the mutable functions.
ListingD.1 Configuring immutable functions
_ = fp.convert({
"cap": false,
"curry": false,
"fixed": false,
"immutable": true,
"rearg": false
});
This short appendix lists the 28 Lodash functions used in the book to help you, in
case you are looking at a code snippet in the book that uses a Lodash function that
you want to understand. The functions are split in to three categories:
 Functions on maps in table D.1
 Functions on arrays in table D.2
 Function on collections (both arrays and maps) in table D.3
387