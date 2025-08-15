# C.2 DOP principles as best practices

**Level:** 1
**페이지 범위:** 411 - 412
**총 페이지 수:** 2
**ID:** 204

---

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
