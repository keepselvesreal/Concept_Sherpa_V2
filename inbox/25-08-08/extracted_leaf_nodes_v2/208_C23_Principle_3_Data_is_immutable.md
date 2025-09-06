# C.2.3 Principle #3: Data is immutable

**메타데이터:**
- ID: 208
- 레벨: 2
- 페이지: 412-412
- 페이지 수: 1
- 부모 ID: 204
- 텍스트 길이: 2069 문자

---

#3: Data is immutable
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