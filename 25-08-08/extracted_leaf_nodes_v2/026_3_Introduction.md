# 3 Introduction

**메타데이터:**
- ID: 26
- 레벨: 2
- 페이지: 71-72
- 페이지 수: 2
- 부모 ID: 25
- 텍스트 길이: 6338 문자

---

=== Page 70 ===
42 CHAPTER 2 Separation between code and data
Theo It takes a big mindset shift to learn how to separate code from data!
Joe What was the most challenging thing to accept?
Theo The fact that data is not encapsulated in objects.
Joe It was the same for me when I switched from OOP to DOP.
Now it’s time to eat! Theo takes Joe for lunch at Simple, a nice, small restaurant near the
office.
Summary
 DOP principles are language-agnostic.
 DOP principle #1 is to separate code from data.
 The separation between code and data in DOP systems makes them simpler
(easier to understand) than traditional OOP systems.
 Data entities are the parts of your system that hold information.
 DOP is against data encapsulation.
 The more flexible a system is, the easier it is to adapt to changing requirements.
 The separation between code and data in DOP systems makes them more flexi-
ble than traditional OOP systems.
 When code is separated from data, we have the freedom to design code and
data in isolation.
 We represent data as data entities.
 We discover the data entities of our system and sort them into high-level groups,
either as a nested list or as a mind map.
 A DOP system is easier to understand than a traditional OOP system because
the system is split into two parts: data entities and code modules.
 In DOP, a code module is an aggregation of stateless functions.
 DOP systems are flexible. Quite often they adapt to changing requirements
without changing the system design.
 In traditional OOP, the state of the object is an implicit argument to the meth-
ods of the object.
 Stateless functions receive data they manipulate as an explicit argument.
 The high-level modules of a DOP system correspond to high-level data entities.
 The only kind of relation between code modules is the usage relation.
 The only kinds of relation between data entities are the association and the compo-
sition relation.
 For a discussion of polymorphism in DOP, see chapter 13.

=== Page 71 ===
Basic data manipulation
Meditation and programming
This chapter covers
 Representing records with string maps to improve
flexibility
 Manipulating data with generic functions
 Accessing each piece of information via its
information path
 Gaining JSON serialization for free
After learning why and how to separate code from data in the previous chapter,
let’s talk about data on its own. In contrast to traditional OOP, where system design
tends to involve a rigid class hierarchy, DOP prescribes that we represent our data
model as a flexible combination of maps and arrays (or lists), where we can access
each piece of information via an information path. This chapter is a deep dive into
the second principle of DOP.
PRINCIPLE #2 Represent data entities with generic data structures.
43

=== Page 72 ===
44 CHAPTER 3 Basic data manipulation
We increase system flexibility when we represent records as string maps and not as
objects instantiated from classes. This liberates data from the rigidity of a class-based sys-
tem. Data becomes a first-class citizen powered by generic functions to add, remove, or
rename fields.
 NOTE We refer to maps that have strings as keys as string maps.
The dependency between the code that manipulates data and the data is a weak
dependency. The code only needs to know the keys of specific fields in the record it
wants to manipulate. The code doesn’t even need to know about all the keys in the
record, only the ones relevant to it. In this chapter, we’ll deal only with data query.
We’ll discuss managing changes in system state in the next chapter.
3.1 Designing a data model
During lunch at Simple, Theo and Joe don’t talk about programming. Instead, they start
getting to know each other on a personal level. Theo discovers that Joe is married to Kay,
who has just opened her creative therapy practice after many years of studying various
fields related to well-being. Neriah, their 14-year-old son, is passionate about drones, whereas
Aurelia, their 12-year-old daughter, plays the transverse flute.
Joe tells Theo that he’s been practicing meditation for 10 years. Meditation, he says, has
taught him how to break away from being continually lost in a “storm thought” (especially
negative thoughts, which can be the source of great suffering) to achieve a more direct
relationship with reality. The more he learns to experience reality as it is, the calmer his
mind. When he first started to practice meditation, it was sometimes difficult and even
weird, but by persevering, he has increased his feeling of well-being with each passing year.
When they’re back at the office, Joe tells Theo that his next step in their DOP journey
will be about data models. This includes data representation.
Joe When we design the data part of our system, we’re free to do it in isolation.
Theo What do you mean by isolation?
Joe I mean that you don’t have to bother with code, only data.
Theo Oh, right. I remember you telling me how that makes a DOP system simpler
than OOP. Separation of concerns is a design principle I’m used to in OOP.
Joe Indeed.
Theo And, when we think about data, the only relations we have to think about are
association and composition.
Joe Correct.
Theo Will the data model design be significantly different than the data model I’m
used to designing as an OOP developer?
Joe Not so much.
Theo OK. Let me see if I can draw a DOP-style data entity diagram.
Theo takes a look at the data mind map that he drew earlier in the morning. He then
draws the diagram in figure 3.1.
He refines the details of the fields of each data entity and the kind of relations between
entities. Figure 3.2 shows the result of this redefined data entity diagram.

=== Page 73 ===
3.1 Designing a data model 45
Books
Authors
Catalog
Book items
Library data Book lendings
Users
User management Members
Librarians Figure 3.1 A data mind map of
the Library Management System
CC Library
name: String
address: String
CC Catalog CC UserManagement
* * *
CC Book CC Librarian CC Member
email: String email: String
title : String
password: String password: String
publicationYear: Number
*
ISBN: String
publisher: String
* *
CC Author CC BookLending
name: String lendingDate: String
CC BookItem
* libld: String
purchaseDate: String
Figure 3.2 A data model of the Library Management System