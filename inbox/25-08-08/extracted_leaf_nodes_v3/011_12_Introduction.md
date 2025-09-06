#### 1.2 Introduction

alleviate complexity. The purpose of this book is not be critical of OOP, but rather
to present a programming paradigm called data-oriented programming (DOP) that
tends to build systems that are less complex. In fact, the DOP paradigm is compati-
ble with OOP.
If one chooses to build an OOP system that adheres to DOP principles, the system
will be less complex. According to DOP, the main sources of complexity in Theo’s sys-
tem (and of many traditional OOP systems) are that
 Code and data are mixed.
 Objects are mutable.
 Data is locked in objects as members.
 Code is locked into classes as methods.
This analysis is similar to what functional programming (FP) thinks about traditional
OOP. However, as we will see throughout the book, the data approach that DOP takes
in order to reduce system complexity differs from the FP approach. In appendix A, we
illustrate how to apply DOP principles both in OOP and in FP styles.
TIP DOP is compatible both with OOP and FP.

14 CHAPTER 1 Complexity of object-orientedprogramming
In the remaining sections of this chapter, we will illustrate each of the previous
aspects, summarized in table 1.1. We’ll look at this in the context of the Klafim project
and explain in what sense these aspects are a source of complexity.
Table 1.1 Aspects of OOP and their impact on system complexity
Aspect Impact on complexity
Code and data are mixed. Classes tend to be involved in many relations.
Objects are mutable. Extra thinking is needed when reading code.
Objects are mutable. Explicit synchronization is required on multi-threaded environments.
Data is locked in objects. Data serialization is not trivial.
Code is locked in classes. Class hierarchies are complex.