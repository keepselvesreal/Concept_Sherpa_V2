# 2 Separation between code and data

**Level:** 1
**페이지 범위:** 54 - 70
**총 페이지 수:** 17
**ID:** 17

---

=== 페이지 54 ===
Separation between
code and data
A whole new world
This chapter covers
 The benefits of separating code from data
 Designing a system where code and data are
separate
 Implementing a system that respects the
separation between code and data
The first insight of DOP is that we can decrease the complexity of our systems by
separating code from data. Indeed, when code is separated from data, our systems
are made of two main pieces that can be thought about separately: data entities and
code modules. This chapter is a deep dive in the first principle of DOP (summa-
rized in figure 2.1).
PRINCIPLE #1 Separate code from data such that the code resides in functions,
whose behavior doesn’t depend on data that is somehow encapsulated in the func-
tion’s context.
26

=== 페이지 55 ===
2.1 The two parts of a DOP system 27
Stateless (static)
Functions
Data asfirst argument
Code modules
Usage
Relations
No inheritance
Separate code from data
Only members
Data entities No code
Association
Relations
Composition
Figure 2.1 DOP principle #1 summarized: Separate code from data.
In this chapter, we’ll illustrate the separation between code and data in the context of
Klafim’s Library Management System that we introduced in chapter 1. We’ll also unveil
the benefits that this separation brings to the system:
 The system is simple. It is easy to understand.
 The system is flexible and extensible. Quite often, it requires no design changes to
adapt to changing requirements.
This chapter focuses on the design of the code in a system where code and data are
separate. In the next chapter, we’ll focus on the design of the data. As we progress in
the book, we’ll discover other benefits of separating code from data.
2.1 The two parts of a DOP system
While Theo is driving home after delivering the prototype, he asks himself whether the
Klafim project was a success or not. Sure, he was able to satisfy the customer, but it was
more luck than brains. He wouldn’t have made it on time if Nancy had decided to keep
the Super members feature. Why was it so complicated to add tiny features to the system?
Why was the system he built so complex? He thought there should be a way to build more
flexible systems!
The next morning, Theo asks on Hacker News and on Reddit for ways to reduce system
complexity and build flexible systems. Some folks mention using different programming
languages, while others talk about advanced design patterns. Finally, Theo’s attention gets
captured by a comment from a user named Joe. He mentions data-oriented programming and
claims that its main goal is to reduce system complexity. Theo has never heard this term
before. Out of curiosity, he decides to contact Joe by email. What a coincidence! Joe lives
in San Francisco too. Theo invites him to a meeting in his office.
Joe is a 40-year-old developer. He was a Java developer for nearly a decade before adopt-
ing Clojure around 7 years ago. When Theo tells Joe about the Library Management System

=== 페이지 56 ===
28 CHAPTER 2 Separation between code and data
he designed and built, and about his struggles to adapt to changing requirements, Joe is
not surprised.
Joe tells Theo that the systems that he and his team have built in Clojure over the last 7
years are less complex and more flexible than the systems he used to build in Java. Accord-
ing to Joe, the systems they build now tend to be much simpler because they follow the
principles of DOP.
Theo I’ve never heard of data-oriented programming. Is it a new concept?
Joe Yes and no. Most of the foundational ideas of data-oriented programming, or
DOP as we like to call it, are well known to programmers as best practices. The
novelty of DOP, however, is that it combines best practices into a cohesive
whole.
Theo That’s a bit abstract for me. Can you give me an example?
Joe Sure! Take, for instance, the first insight of DOP. It’s about the relations between
code and data.
Theo You mean the encapsulation of data in objects?
Joe Actually, DOP is against data encapsulation.
Theo Why is that? I thought data encapsulation was a positive programming paradigm.
Joe Data encapsulation has both merits and drawbacks. Think about the way you
designed the Library Management System. According to DOP, the main cause
of complexity and inflexibility in systems is that code and data are mixed
together in objects.
TIP DOP is against data encapsulation.
Theo It sounds similar to what I’ve heard about functional programming. So, if I
want to adopt DOP, do I need to get rid of object-oriented programming and
learn functional programming?
Joe No, DOP principles are language-agnostic. They can be applied in both object-
oriented and functional programming languages.
Theo That’s a relief! I was afraid that you were going to teach me about monads,
algebraic data types, and higher order functions.
Joe No, none of that is required in DOP.
TIP DOP principles are language-agnostic.
Theo What does the separation between code and data look like in DOP then?
Joe Data is represented by data entities that only hold members. Code is aggre-
gated into modules where all functions are stateless.
Theo What do you mean by stateless functions?
Joe Instead of having the state encapsulated in the object, the data entity is passed
as an argument.
Theo I don’t get that.
Joe Here, let’s make it visual.

=== 페이지 57 ===
2.2 Data entities 29
Joe steps up to a whiteboard and quickly draws a diagram to illustrate his comment. Fig-
ure 2.2 shows Joe’s drawing.
Code modules Stateless functions
Separate code from data
Data entities Only members
Figure 2.2 The separation between code and data
Theo It’s still not clear.
Joe It will become clearer when I show you how it looks in the context of your
Library Management System.
Theo OK. Shall we start with code or with data?
Joe Well, it’s data-oriented programming, so let’s start with data.
2.2 Data entities
In DOP, we start the design process by discovering the data entities of our system.
Here’s what Joe and Theo have to say about data entities.
Joe What are the data entities of your system?
Theo What do you mean by data entities?
Joe I mean the parts of your system that hold information.
 NOTE Data entities are the parts of your system that hold information.
Theo Well, it’s a Library Management System, so we have books and members.
Joe Of course, but there are more. One way to discover the data entities of a system
is to look for nouns and noun phrases in the requirements of the system.
Theo looks at Nancy’s requirement napkin. He highlights the nouns and noun phrases
that seem to represent data entities.
Highlighting terms in the requirements that correspond to data entities
 There are two kinds of users: library members and librarians.
 Users log in to the system via email and password.
 Members can borrow books.
 Members and librarians can search books by title or by author.
 Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
 Librarians can list the books currently lent to a member.
 There could be several copies of a book.

=== 페이지 58 ===
30 CHAPTER 2 Separation between code and data
Joe Excellent. Can you see a natural way to group these entities?
Theo Not sure, but it seems to me that users, members, and librarians form one
group, whereas books, authors, and book copies form another group.
Joe Sounds good to me. What would you call each group?
Theo Probably user management for the first group and catalog for the second
group.
The data entities of the system organized in a nested list
 The catalog data
– Data about books
– Data about authors
– Data about book items
– Data about book lendings
 The user management data
– Data about users
– Data about members
– Data about librarians
Theo I’m not sure about the relations between books and authors. Should it be asso-
ciation or composition?
Joe Don’t worry too much about the details for the moment. We’ll refine our data
entity design later. For now, let’s visualize the two groups in a mind map.
Theo and Joe confer for a bit. Figure 2.3 shows the mind map they come up with.
Books
Authors
Catalog
Book items
Library data Book lendings
Users
User management Members
Librarians Figure 2.3 The data entities of the
system organized in a mind map

=== 페이지 59 ===
2.3 Code modules 31
The most precise way to visualize the data entities of a DOP system is to draw a data
entity diagram with different arrows for association and composition. We will come
back to data entity diagrams later.
TIP Discover the data entities of your system and then sort them into high-level
groups, either as a nested list or as a mind map.
We will dive deeper into the design and representation of data entities in the next
chapter. For now, let’s simplify things and say that the data of our library system is
made of two high-level groups: user management and catalog.
2.3 Code modules
The second step of the design process in DOP is to define the code modules. Let’s lis-
ten in on Joe and Theo again.
Joe Now that you have identified the data entities of your system and have
arranged them into high-level groups, it’s time to think about the code part of
your system.
Theo What do you mean by the code part?
Joe One way to think about that is to identity the functionality of your system.
Theo looks again at Nancy’s requirements. This time he highlights the verb phrases that
represent functionality.
Highlighting terms in the requirements that correspond to functionality
 There are two kinds of users: library members and librarians.
 Users log in to the system via email and password.
 Members can borrow books.
 Members and librarians can search books by title or by author.
 Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
 Librarians can list the books currently lent to a member.
 There could be several copies of a book.
In addition, it’s obvious to Theo that members can also return a book. Moreover, there
should be a way to detect whether a user is a librarian or not. He adds those to the require-
ments and then lists the functionality of the system.
The functionality of the library system
 Search for a book.
 Add a book item.
 Block a member.

=== 페이지 60 ===
32 CHAPTER 2 Separation between code and data
(continued)
 Unblock a member.
 Log a user into the system.
 List the books currently lent to a member.
 Borrow a book.
 Return a book.
 Check whether a user is a librarian.
Joe Excellent! Now, tell me what functionality needs to be exposed to the outside
world?
Theo What do you mean by exposed to the outside world?
Joe Imagine that the Library Management System exposes an API over HTTP.
What functionality would be exposed by the HTTP endpoints?
Theo Well, all system functionality would be exposed except checking to see if a user
is a librarian.
Joe OK. Now give each exposed function a short name and gather them together
in a module box called Library.
That takes Theo less than a minute. Figure 2.4 shows the module that contains the
exposed functions of the library devised by Theo.
C Library
searchBook()
addBookItem()
blockMember()
unblockMember()
getBookLendings() Figure 2.4 The Library module
checkoutBook() contains the exposed functions of the
returnBook() Library Management System.
TIP The first step in designing the code part of a DOP system is to aggregate the
exposed functions into a single module.
Joe Beautiful! You just created your first code module.
Theo To me it looks like a class. What’s the difference between a module and a class?
Joe A module is an aggregation of functions. In OOP, a module is represented
bya class, but in other programming languages, it might be a package or a
namespace.
Theo I see.
Joe The important thing about DOP code modules is that they contain only state-
less functions.
Theo You mean like static methods in Java?
Joe Yes, and the classes of these static methods should not have any data members.

=== 페이지 61 ===
2.3 Code modules 33
Theo So, how do the functions know what piece of information they operate on?
Joe Easy. We pass that as the first argument to the function.
Theo OK. Can you give me an example?
Joe, biting his nails, takes a look at the list of functions of the Library module in figure 2.4.
He spots a likely candidate.
Joe Let’s take, for example, getBookLendings. In classic OOP, what would its
arguments be?
Theo A librarian ID and a member ID.
Joe So, in traditional OOP, getBookLendings would be a method of a Library
class that receives two arguments: librarianId and memberId.
Theo Yep.
Joe Now comes the subtle part. In DOP, getBookLendings is part of the Library
module, and it receives the LibraryData as an argument.
Theo Could you show me what you mean?
Joe Sure.
Joe goes over to Theo’s keyboard and starts typing. He enters an example of what a class
method looks like in OOP:
class Library {
catalog
userManagement
getBookLendings(userId, memberId) {
// accesses library state via this.catalog and this.userManagement
}
}
Theo Right! The method accesses the state of the object (in our case, the library
data) via this.
Joe Would you say that the object’s state is an argument of the object’s methods?
Theo I’d say that the object’s state is an implicit argument to the object’s methods.
TIP In traditional OOP, the state of the object is an implicit argument to the meth-
ods of the object.
Joe Well, in DOP, we pass data as an explicit argument. The signature of getBook-
Lendings would look like this.
Listing2.1 The signature of getBookLendings
class Library {
static getBookLendings(libraryData, userId, memberId) {
}
}

=== 페이지 62 ===
34 CHAPTER 2 Separation between code and data
Joe The state of the library is stored in libraryData, and libraryData is passed
to the getBookLendings static method as an explicit argument.
Theo Is that a general rule?
Joe Absolutely! The same rule applies to the other functions of the Library mod-
ule and to other modules as well. All of the modules are stateless—they receive
the library data that they manipulate as an argument.
TIP In DOP, functions of a code module are stateless. They receive the data that they
manipulate as an explicit argument, which is usually the first argument.
 NOTE A module is an aggregation of functions. In DOP, the module functions are
stateless.
Theo It reminds me of Python and the way the self argument appears in method
signatures. Here, let me show you an example.
Listing2.2 A Python object as an explicit argument in method signatures
class Library:
catalog = {}
userManagement = {}
def getBookLendings(self, userId, memberId):
# accesses library state via self.catalog and self.userManagement
Joe Indeed, but the difference I’m talking about is much deeper than a syntax
change. It’s about the fact that data lives outside the modules.
Theo I got that. As you said, module functions are stateless.
Joe Exactly! Would you like to try and apply this principle across the whole
Library module?
Theo Sure.
Theo refines the design of the Library module by including the details about the func-
tions’ arguments. He presents the diagram in figure 2.5 to Joe.
C Library
searchBook(libraryData, searchQuery)
addBookItem(libraryData, bookItemInfo)
blockMember(libraryData, memberId)
unblockMember(libraryData, memberId)
login(libraryData, loginInfo)
getBookLendings(libraryData, userId)
checkoutBook(libraryData, userId, bookItemId) Figure 2.5 The Library module
returnBook(libraryData, userId, bookItemId)
with the functions’ arguments
Joe Perfect. Now, we’re ready to tackle the high-level design of our system.
Theo What’s a high-level design in DOP?

=== 페이지 63 ===
2.3 Code modules 35
Joe A high-level design in DOP is the definition of modules and the interaction
between them.
Theo I see. Are there any guidelines to help me define the modules?
Joe Definitely. The high-level modules of the system correspond to the high-level
data entities.
Theo You mean the data entities that appear in the data mind map?
Joe Exactly!
Theo looks again at the data mind map (figure 2.6). He focuses on the high-level data enti-
ties library, catalog, and user management. This means that in the system, besides the
Library module, we have two high-level modules:
 The Catalog module deals with catalog data.
 The UserManagement module deals with user management data.
Catalog
Library data Figure 2.6 A mind map of the high-
level data entities of the Library
User management
Management System
Theo then draws the high-level design of the Library Management System with the Catalog
and UserManagement modules. Figure 2.7 shows the addition of these modules, where:
 Functions of Catalog receive catalogData as their first argument.
 Functions of UserManagement receive userManagementData as their first argument.
C Library
searchBook(libraryData, searchQuery)
addBookItem(libraryData, bookItemInfo)
blockMember(libraryData, memberId)
unblockMember(libraryData, memberId)
login(libraryData, loginInfo)
getBookLendings(libraryData, userId)
checkoutBook(libraryData, userId, bookItemId)
returnBook(libraryData, userId, bookItemId)
C Catalog
C UserManagement
searchBook(catalogData, searchQuery)
blockMember(userManagementData, memberId)
addBookItem(catalogData, bookItemInfo)
unblockMember(userManagementData, memberId)
checkoutBook(catalogData, bookItemId)
login(userManagementData, loginInfo)
returnBook(catalogData, bookItemId)
isLibrarian(userManagementData, userId)
getBookLendings(catalogData, userId)
Figure 2.7 The modules of the Library Management System with their functions’ arguments

=== 페이지 64 ===
36 CHAPTER 2 Separation between code and data
It’s not 100% clear for Theo at this point how the data entities get passed between mod-
ules. For the moment, he thinks of libraryData as a class with two members:
 catalog holds the catalog data.
 userManagement holds the user management data.
Theo also sees that the functions of Library share a common pattern. (Later on in this
chapter, we’ll see the code for some functions of the Library module.)
 They receive libraryData as an argument.
 They pass libraryData.catalog to the functions of Catalog.
 They pass libraryData.userManagement to the functions of UserManagement.
TIP The high-level modules of a DOP system correspond to the high-level data enti-
ties.
2.4 DOP systems are easy to understand
Theo takes a look at the two diagrams that represent the high-level design of his system:
 The data entities in the data mind map in figure 2.8
 The code modules in the module diagram in figure 2.9
A bit perplexed, Theo asks Joe:
Theo I’m not sure that this system is better than a traditional OOP system where
objects encapsulate data.
Joe The main benefit of a DOP system over a traditional OOP system is that it’s eas-
ier to understand.
Theo What makes it easier to understand?
Joe The fact that the system is split cleanly into code modules and data entities.
Theo How does that help?
Joe When you try to understand the data entities of the system, you don’t have to
think about the details of the code that manipulates the data entities.
Theo So, when I look at the data mind map of my Library Management System, I can
understand it on its own?
Joe Exactly, and similarly, when you try to understand the code modules of the sys-
tem, you don’t have to think about the details of the data entities manipulated
by the code. There is a clear separation of concerns between the code and the
data.
Theo looks again at the data mind map in figure 2.8. He has kind of an Aha! moment:
Data lives on its own!
 NOTE A DOP system is easier to understand because the system is split into two
parts: data entities and code modules.

=== 페이지 65 ===
2.4 DOP systems are easy to understand 37
Books
Authors
Catalog
Book items
Library data Book lendings
Users
User management Members
Figure 2.8 A data mind map of the
Librarians
Library Management System
Now, Theo looks at the module diagram in figure 2.9. He feels a bit confused and asks Joe
for clarification:
 On one hand, the module diagram looks similar to the class diagrams from classic
OOP, boxes for classes and arrows for relations between classes.
 On the other hand, the code module diagram looks much simpler than the class
diagrams from classic OOP, but he cannot explain why.
C Library
searchBook(libraryData, searchQuery)
addBookItem(libraryData, bookItemInfo)
blockMember(libraryData, memberId)
unblockMember(libraryData, memberId)
login(libraryData, loginInfo)
getBookLendings(libraryData, userId)
checkoutBook(libraryData, userId, bookItemId)
returnBook(libraryData, userId, bookItemId)
C Catalog
C UserManagement
searchBook(catalogData, searchQuery)
blockMember(userManagementData, memberId)
addBookItem(catalogData, bookItemInfo)
unblockMember(userManagementData, memberId)
checkoutBook(catalogData, bookItemId)
login(userManagementData, loginInfo)
returnBook(catalogData, bookItemId)
isLibrarian(userManagementData, userId)
getBookLendings(catalogData, userId)
Figure 2.9 The modules of the Library Management System with the function arguments
Theo The module diagram seems much simpler than the class diagrams I am used to
in OOP. I feel it, but I can’t put it into words.
Joe The reason is that module diagrams have constraints.

=== 페이지 66 ===
38 CHAPTER 2 Separation between code and data
Theo What kind of constraints?
Joe Constraints on the functions we saw before. All the functions are static (or
stateless), but there’s also constraints on the relations between the modules.
TIP All the functions in a DOP module are stateless.
Theo In what way are the relations between modules constrained?
Joe There is a single kind of relation between DOP modules—the usage relation. A
module uses code from another module. There’s no association, no composi-
tion, and no inheritance between modules. That’s what makes a DOP module
diagram easy to understand.
Theo I understand why there is no association and no composition between DOP
modules. After all, association and composition are data relations. But why no
inheritance relation? Does that mean that DOP is against polymorphism?
Joe That’s a great question! The quick answer is that in DOP, we achieve polymor-
phism with a different mechanism than class inheritance. We will talk about it
some day.
 NOTE For a discussion of polymorphism in DOP, see chapter 13.
Theo Now, you’ve piqued my curiosity. I thought inheritance was the only way to
achieve polymorphism.
Theo looks again at the module diagram in figure 2.9. Now he not only feels that this dia-
gram is simpler than traditional OOP class diagrams, he understands why it’s simpler: all
the functions are static, and all the relations between modules are of type usage. Table 2.1
summarizes Theo’s perception.
TIP The only kind of relation between DOP modules is the usage relation.
Table 2.1 What makes each part of a DOP system easy to understand
System part Constraint on entities Constraints on relations
Data entities Members only (no code) Association and composition
Code modules Stateless functions (no members) Usage (no inheritance)
TIP Each part of a DOP system is easy to understand because it provides constraints.
2.5 DOP systems are flexible
Theo I see how a sharp separation between code and data makes DOP systems easier
to understand than classic OOP systems. But what about adapting to changes
in requirements?
Joe Another benefit of DOP systems is that it is easy to extend them and to adapt to
changing requirements.

=== 페이지 67 ===
2.5 DOP systems are flexible 39
Theo I remember that, when Nancy asked me to add Super members and VIP mem-
bers to the system, it was hard to adapt my OOP system. I had to introduce a
few base classes, and the class hierarchy became really complex.
Joe I know exactly what you mean. I’ve experienced the same kind of struggle so
many times. Describe the changes in the requirements for Super members and
VIP members, and I’m quite sure that you’ll see how easy it would be to extend
your DOP system.
The requirements for Super members and VIP members
 Super members are members that are allowed to list the book lendings to
other members.
 VIP members are members that are allowed to add book items to the library.
Theo opens his IDE and starts to code the getBookLendings function of the Library
module (see listing 2.3), first without addressing the requirements for Super members.
Theo remembers what Joe told him about module functions in DOP:
 Functions are stateless.
 Functions receive the data they manipulate as their first argument.
In terms of functionality, getBookLendings has two parts:
 Checks that the user is a librarian.
 Retrieves the book lendings from the catalog.
Basically, the code of getBookLendings has two parts as well:
 Calls the isLibrarian function from the UserManagement module and passes it
the UserManagementData.
 Calls the getBookLendings function from the Catalog module and passes it the
CatalogData.
Listing2.3 Getting the book lendings of a member
class Library {
static getBookLendings(libraryData, userId, memberId) {
if(UserManagement.isLibrarian(libraryData.userManagement, userId)) {
return Catalog.getBookLendings(libraryData.catalog, memberId);
} else {
throw "Not allowed to get book lendings";
There are other
}
ways to manage
}
errors.
}
class UserManagement {
static isLibrarian(userManagementData, userId) {
// will be implemented later
In chapter 3, we will see how
}
to manage permissions with
}
generic data collections.

=== 페이지 68 ===
40 CHAPTER 2 Separation between code and data
class Catalog {
static getBookLendings(catalogData, memberId) {
// will be implemented later
In chapter 3, we will see how
}
to query data with generic
}
data collections.
It’s Theo’s first piece of DOP code and passing around all those data objects—library-
Data, libraryData.userManagement, and libraryData.catalog—feels a bit awkward.
But he did it! Joe looks at Theo’s code and seems satisfied.
Joe Now, how would you adapt your code to Super members?
Theo I would add a function isSuperMember to the UserManagement module and
call it from Library.getBookLendings.
Joe Exactly! It’s as simple as that.
Theo types the code on his laptop so that he can show it to Joe. Here’s how Theo adapts
his code for Super members.
Listing2.4 Allowing Super members to get the book lendings of a member
class Library {
static getBookLendings(libraryData, userId, memberId) {
if(Usermanagement.isLibrarian(libraryData.userManagement, userId) ||
Usermanagement.isSuperMember(libraryData.userManagement, userId)) {
return Catalog.getBookLendings(libraryData.catalog, memberId);
} else {
throw "Not allowed to get book lendings";
There are other
}
ways to manage
}
errors.
}
class UserManagement {
static isLibrarian(userManagementData, userId) {
// will be implemented later
In chapter 3, we will see how
}
to manage permissions with
static isSuperMember(userManagementData, userId) {
generic data collections.
// will be implemented later
}
}
class Catalog {
static getBookLendings(catalogData, memberId) {
// will be implemented later
In chapter 3, we will see how
}
to query data with generic
}
data collections.
Now, the awkward feeling caused by passing around all those data objects is dominated by
a feeling of relief. Adapting to this change in requirements takes only a few lines of code
and requires no changes in the system design. Once again, Joe seems satisfied.
TIP DOP systems are flexible. Quite often they adapt to changing requirements with-
out changing the system design.

=== 페이지 69 ===
2.5 DOP systems are flexible 41
Theo starts coding addBookItem. He looks at the signature of Library.addBookItem,
and the meaning of the third argument bookItemInfo isn’t clear to him. He asks Joe for
clarification.
Listing2.5 The signature of Library.addBookItem
class Library {
static addBookItem(libraryData, userId, bookItemInfo) {
}
}
Theo What is bookItemInfo?
Joe Let’s call it the book item information. Imagine we have a way to represent this
information in a data entity named bookItemInfo.
Theo You mean an object?
Joe For now, it’s OK to think about bookItemInfo as an object. Later on, I will
show you how to we represent data in DOP.
Besides this subtlety about how the book item information is represented by book-
ItemInfo, the code for Library.addBookItem in listing 2.6 is quite similar to the code
Theo wrote for Library.getBookLendings in listing 2.4. Once again, Theo is amazed by
the fact that adding support for VIP members requires no design change.
Listing2.6 Allowing VIP members to add a book item to the library
class Library {
static addBookItem(libraryData, userId, bookItemInfo) {
if(UserManagement.isLibrarian(libraryData.userManagement, userId) ||
UserManagement.isVIPMember(libraryData.userManagement, userId)) {
return Catalog.addBookItem(libraryData.catalog, bookItemInfo);
} else {
throw "Not allowed to add a book item";
There are other
}
ways to manage
}
errors.
}
class UserManagement {
static isLibrarian(userManagementData, userId) {
// will be implemented later
In chapter 3, we will see how
}
to manage permissions with
static isVIPMember(userManagementData, userId) {
generic data collections.
// will be implemented later
}
}
class Catalog {
static addBookItem(catalogData, memberId) {
// will be implemented later
In chapter 4, we will see how
}
to manage state of the system
}
with immutable data.

=== 페이지 70 ===
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
