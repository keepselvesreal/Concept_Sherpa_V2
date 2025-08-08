# 1.1 Introduction

**메타데이터:**
- ID: 5
- 레벨: 3
- 페이지: 32-33
- 페이지 수: 2
- 부모 ID: 4
- 텍스트 길이: 6705 문자

---

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

=== Page 33 ===
1.1 OOP design: Classic or classical? 5
The main classes of the library management system
 Library—The central part of the system design.
 Book—A book.
 BookItem—A book can have multiple copies, and each copy is considered as
a book item.
 BookLending—When a book is lent, a book lending object is created.
 Member—A member of the library.
 Librarian—A librarian.
 User—A base class for Librarian and Member.
 Catalog—Contains a list of books.
 Author—A book author.
That was the easy part. Now comes the difficult part: the relations between the classes.
After two hours or so, Theo comes up with a first draft of a design for the Global Library
Management System. It looks like the diagram in figure 1.1.
 NOTE The design presented here doesn’t pretend to be the smartest OOP design:
experienced OOP developers would probably use a couple of design patterns to sug-
gest a much better design. This design is meant to be naive and by no means covers all
the features of the system. It serves two purposes:
 For Theo, the developer, it is rich enough to start coding.
 For me, the author of the book, it is rich enough to illustrate the complexity of a
typical OOP system.
Theo feels proud of himself and of the design diagram he just produced. He definitely
deserves a cup of coffee!
Near the coffee machine, Theo meets Dave, a junior software developer who joined
Albatross a couple of weeks ago. Theo and Dave appreciate each other, as Dave’s curiosity
leads him to ask challenging questions. Meetings near the coffee machine often turn into
interesting discussions about programming.
Theo Hey Dave! How’s it going?
Dave Today? Not great. I’m trying to fix a bug in my code! I can’t understand why
the state of my objects always changes. I’ll figure it out though, I’m sure. How’s
your day going?
Theo I just finished the design of a system for a new customer.
Dave Cool! Would it be OK for me to see it? I’m trying to improve my design skills.
Theo Sure! I have the diagram on my desk. We can take a look now if you like.

=== Page 34 ===
6 CHAPTER 1 Complexity of object-orientedprogramming
C Library
name : String
address : String
C Catalog
search(searchCriteria, queryStr) : List<Book>
addBookItem(librarian: Librarian, bookItem: BookItem) : BookItem
*
* C Librarian
C Book
blockMember(member: Member) : Bool
id : String unblockMember(member: Member) : Bool
title : String addBookItem(bookItem: BookItem) : BookItem
getBookLendingsOfMember(member: Member) : List<BookLending>
*
*
C Member
*
C Author isBlocked() : Bool
id : String block() : Bool
fullName: String unblock() : Bool
returnBook(bookLending: BookLending) : Bool
checkout(bookItem: BookItem) : BookLending
*
C User
C BookItem
id : String
id : String
email : String
libId: String
password : String
checkout(member: Member) : BookLending
login() : Bool
C BookLending
id : String
lendingDate : date *
dueDate : date
isLate() : Bool
returnBook() : Bool
Figure 1.1 A class diagram for Klafim’s Global Library Management System
1.1.2 UML 101
Latte in hand, Dave follows Theo to his desk. Theo proudly shows Dave his piece of art: the
UML diagram for the Library Management System (figure 1.1). Dave seems really excited.
Dave Wow! Such a detailed class diagram.
Theo Yeah. I’m pretty happy with it.