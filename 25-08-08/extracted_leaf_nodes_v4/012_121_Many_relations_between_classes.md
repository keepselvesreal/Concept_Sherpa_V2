#### 1.2.1 Many relations between classes

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

## 페이지 43

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