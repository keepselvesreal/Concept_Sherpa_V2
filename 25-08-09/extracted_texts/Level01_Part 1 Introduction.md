# Part 1 Introduction

**Level:** 1
**페이지 범위:** 29 - 31
**총 페이지 수:** 3
**ID:** 1

---

=== 페이지 29 ===
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

=== 페이지 30 ===
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

=== 페이지 31 ===
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
