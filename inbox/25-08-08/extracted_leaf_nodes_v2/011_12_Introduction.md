# 1.2 Introduction

**메타데이터:**
- ID: 11
- 레벨: 3
- 페이지: 41-42
- 페이지 수: 2
- 부모 ID: 10
- 텍스트 길이: 6292 문자

---

=== Page 40 ===
12 CHAPTER 1 Complexity of object-orientedprogramming
C Book
id : String
*
title : String
* *
C BookItem C Author
id : String id : String
Iibld: String fullName: String
BookLending checkout(member: Member)
C BookLending
id : String
lendingDate : date
dueDate : date
Bool isLate()
Bool returnBook() Figure 1.9 The Book class
THE BOOKITEM CLASS
The BookItem class represents a book copy, and a book could have many copies. In
terms of data, a BookItem object
 Should have as its bare minimum data for members: an id and a libId (for its
physical library ID).
 Owns multiple BookLending objects, one for each time the book is lent.
In terms of code, a BookItem object can be checked out via checkout.
1.1.4 The implementation phase
After this detailed investigation of Theo’s diagrams, Dave lets it sink in as he slowly sips his
coffee. He then expresses his admiration to Theo.
Dave Wow! That’s amazing!
Theo Thank you.
Dave I didn’t realize people were really spending the time to write down their design
in such detail before coding.
Theo I always do that. It saves me lot of time during the coding phase.
Dave When will you start coding?
Theo When I finish my latte.
Theo grabs his coffee mug and notices that his hot latte has become an iced latte. He was
so excited to show his class diagram to Dave that he forgot to drink it!

=== Page 41 ===
1.2 Sources of complexity 13
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

=== Page 42 ===
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
1.2.1 Many relations between classes
One way to assess the complexity of a class diagram is to look only at the entities and
their relations, ignoring members and methods, as in figure 1.10. When we design a
system, we have to define the relations between different pieces of code and data.
That’s unavoidable.
C Library
C Catalog
* *
C Book C Librarian
*
*
C Member
*
C Author
C BookItem C User
Figure 1.10 A class
diagram overview for
C BookLending * Klafim’s Library
Management System
TIP In OOP, code and data are mixed together in classes: data as members and code as
methods.

=== Page 43 ===
1.2 Sources of complexity 15
From a system analysis perspective, the fact that code and data are mixed together
makes the system complex in the sense that entities tend to be involved in many rela-
tions. In figure 1.11, we take a closer look at the Member class. Member is involved in five
relations: two data relations and three code relations.
 Data relations:
– Library has many Members.
– Member has many BookLendings.
 Code relations:
– Member extends User.
– Librarian uses Member.
– Member uses BookItem.
C Librarian
C Library * C Member
*
C User C BookLending C BookItem Figure 1.11 The class Member is
involved in five relations.
Imagine for a moment that we were able, somehow, to split the Member class into two
separate entities:
 MemberCode for the code
 MemberData for the data
Instead of a Member class with five relations, we would have the diagram shown in fig-
ure 1.12 with:
 A MemberCode entity and three relations.
 A MemberData entity and two relations.
C Library C Librarian
*
C MemberData C MemberCode
*
C BookLending C User C BookItem Figure 1.12 A class diagram where Member
is split into code and data entities