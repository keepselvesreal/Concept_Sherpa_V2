#### 1.2 Introduction

1.2 Sources of complexity
While Theo is getting himself another cup of coffee (a cappuccino this time), I
would like to challenge his design. It might look beautiful and clear on the paper,
but I claim that this design makes the system hard to understand. It’s not that Theo
picked the wrong classes or that he misunderstood the relations among the classes.
It goes much deeper:
 It’s about the programming paradigm he chose to implement the system.
 It’s about the object-oriented paradigm.
 It’s about the tendency of OOP to increase the complexity of a system.
TIP OOP has a tendency to create complex systems.
Throughout this book, the type of complexity I refer to is that which makes systems
hard to understand as defined in the paper, “Out of the Tar Pit,” by Ben Moseley
and Peter Marks (2006), available at http://mng.bz/enzq. It has nothing to do with
the type of complexity that deals with the amount of resources consumed by a pro-
gram. Similarly, when I refer to simplicity, I mean not complex (in other words, easy
to understand).
Keep in mind that complexity and simplicity (like hard and easy) are not absolute
but relative concepts. We can compare the complexity of two systems and determine
whether system A is more complex (or simpler) than system B.
 NOTE Complexity in the context of this book means hard to understand.
As mentioned in the introduction of this chapter, there are many ways in OOP to
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

## 페이지 42

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