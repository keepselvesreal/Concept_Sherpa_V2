# Summary

**Level:** 1
**페이지 범위:** 414 - 414
**총 페이지 수:** 1
**ID:** 215

---

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
