# C.3 DOP and other data-related paradigms

**Level:** 1
**페이지 범위:** 413 - 413
**총 페이지 수:** 1
**ID:** 210

---

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
