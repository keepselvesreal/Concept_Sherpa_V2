# Part 1 Introduction

**메타데이터:**
- ID: 1
- 레벨: 1
- 페이지: 29-31
- 페이지 수: 3
- 부모 ID: 0
- 텍스트 길이: 6349 문자

---

=== Page 28 ===
dramatis personae
THEO, senior developer
NANCY, entrepreneur
MONICA, manager, Theo’s boss
DAVE, junior developer, Theo’s colleague
JOE, independent programmer
KAY, therapist, Joe’s wife
JANE, Theo’s wife
NERIAH, Joe’s son
AURELIA, Joe’s daughter
The story takes place in San Francisco.
xxvi

=== Page 29 ===
Part 1
Flexibility
I
t’s Monday morning. Theodore is sitting with Nancy on the terrace of La Vita è
Bella, an Italian coffee shop near the San Francisco Zoo. Nancy is an entrepreneur
looking for a development agency for her startup company, Klafim. Theo works for
Albatross, a software development agency that seeks to regain the trust of startups.
Nancy and her business partner have raised seed money for Klafim, a social net-
work for books. Klafim’s unique value proposition is to combine the online world
with the physical world by allowing users to borrow books from local libraries and
then to meet online to discuss the books. Most parts of the product rely on the inte-
gration of already existing online services. The only piece that requires software
development is what Nancy calls a Global Library Management System. Their discus-
sion is momentarily interrupted by the waiter who brings Theo his tight espresso and
Nancy her Americano with milk on the side.
Theo In your mind, what’s a Global Library Management System?
Nancy It’s a software system that handles the basic housekeeping functions of a
library, mainly around the book catalog and the library members.
Theo Could you be a little bit more specific?
Nancy Sure. For the moment, we need a quick prototype. If the market response
to Klafim is positive, we will move forward with a big project.
Theo What features do you need for the prototype phase?
Nancy grabs the napkin under her coffee mug and writes down a couple of bulleted
points on the napkin.

=== Page 30 ===
2 PART 1 Flexibility
The requirements for the Klafim prototype
 Two kinds of library users are members and librarians.
 Users log in to the system via email and password.
 Members can borrow books.
 Members and librarians can search books by title or by author.
 Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
 Librarians can list the books currently lent to a member.
 There could be several copies of a book.
 The book belongs to a physical library.
Theo Well, that’s pretty clear.
Nancy How much time would it take for your company to deliver the prototype?
Theo I think we should be able to deliver within a month. Let’s say Wednesday the
30th.
Nancy That’s too long. We need it in two weeks!
Theo That’s tough! Can you cut a feature or two?
Nancy Unfortunately, we cannot cut any feature, but if you like, you can make the
search very basic.
(Theo really doesn’t want to lose this contract, so he’s willing to work hard and sleep later.)
Theo I think it should be doable by Wednesday the 16th.
Nancy Perfect!

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