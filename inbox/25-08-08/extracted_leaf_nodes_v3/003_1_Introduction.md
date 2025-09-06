### 1 Introduction

=== Page 31 ===
Complexity of object-
oriented programming
A capricious entrepreneur
This chapter covers
 The tendency of OOP to increase system
complexity
 What makes OOP systems hard to understand
 The cost of mixing code and data together into
objects
In this chapter, we’ll explore why object-oriented programming (OOP) systems tend to
be complex. This complexity is not related to the syntax or the semantics of a specific
OOP language. It is something that is inherent to OOP’s fundamental insight—
programs should be composed from objects, which consist of some state, together
with methods for accessing and manipulating that state.
Over the years, OOP ecosystems have alleviated this complexity by adding new
features to the language (e.g., anonymous classes and anonymous functions) and
by developing frameworks that hide some of this complexity, providing a simpler
interface for developers (e.g., Spring and Jackson in Java). Internally, the frame-
works rely on the advanced features of the language such as reflection and custom
annotations.
3

=== Page 32 ===
4 CHAPTER 1 Complexity of object-orientedprogramming
This chapter is not meant to be read as a critical analysis of OOP. Its purpose is to
raise your awareness of the tendency towards OOP’s increased complexity as a pro-
gramming paradigm. Hopefully, it will motivate you to discover a different program-
ming paradigm, where system complexity tends to be reduced. This paradigm is
known as data-oriented programming (DOP).
1.1 OOP design: Classic or classical?
 NOTE Theo, Nancy, and their new project were introduced in the opener for part 1.
Take a moment to read the opener if you missed it.
Theo gets back to the office with Nancy’s napkin in his pocket and a lot of anxiety in his
heart because he knows he has committed to a tough deadline. But he had no choice! Last
week, Monica, his boss, told him quite clearly that he had to close the deal with Nancy no
matter what.
Albatross, where Theo works, is a software consulting company with customers all over
the world. It originally had lots of customers among startups. Over the last year, however,
many projects were badly managed, and the Startup department lost the trust of its cus-
tomers. That’s why management moved Theo from the Enterprise department to the
Startup department as a Senior Tech lead. His job is to close deals and to deliver on time.
1.1.1 The design phase
Before rushing to his laptop to code the system, Theo grabs a sheet of paper, much big-
ger than a napkin, and starts to draw a UML class diagram of the system that will imple-
ment the Klafim prototype. Theo is an object-oriented programmer. For him, there is no
question—every business entity is represented by an object, and every object is made
from a class.
The requirements for the Klafim prototype
 There are two kinds of users: library members and librarians.
 Users log in to the system via email and password.
 Members can borrow books.
 Members and librarians can search books by title or by author.
 Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
 Librarians can list the books currently lent to a member.
 There can be several copies of a book.
 A book belongs to a physical library.
Theo spends some time thinking about the organization of the system. He identifies the
main classes for the Klafim Global Library Management System.