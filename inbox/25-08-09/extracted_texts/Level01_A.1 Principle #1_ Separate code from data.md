# A.1 Principle #1: Separate code from data

**Level:** 1
**페이지 범위:** 363 - 372
**총 페이지 수:** 10
**ID:** 149

---

=== 페이지 363 ===
A.1 Principle #1: Separate code from data 335
A.1 Principle #1: Separate code from data
Principle #1 is a design principle that recommends a clear separation between code
(behavior) and data. This may appear to be a FP principle, but in fact, one can adhere
to it or break it either in FP or in OOP:
 Adherence to this principle in OOP means aggregating the code as methods of
a static class.
 Breaking this principle in FP means hiding state in the lexical scope of a function.
Also, this principle does not relate to the way data is represented. Data representation
is addressed by Principle #2.
PRINCIPLE #1 Separate code from data in a way that the code resides in functions
whose behavior does not depend on data that is encapsulated in the function’s
context.
A.1.1 Illustration of Principle #1
Our exploration of Principle #1 begins by illustrating how it can be applied to OOP
and FP. The following sections illustrate how this principle can be adhered to or bro-
ken in a simple program that deals with:
 An author entity with a firstName, a lastName, and the number of books they
wrote.
 A piece of code that calculates the full name of the author.
 A piece of code that determines if an author is prolific, based on the number of
books they wrote.
BREAKING PRINCIPLE #1 IN OOP
Breaking Principle #1 in OOP happens when we write code that combines data and
code together in an object. The following listing demonstrates what this looks like.
ListingA.1 Breaking Principle #1 in OOP
class Author {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
fullName() {
return this.firstName + " " + this.lastName;
}
isProlific() {
return this.books > 100;
}
}

=== 페이지 364 ===
336 APPENDIX A Principles of data-oriented programming
var obj = new Author("Isaac", "Asimov", 500);
Isaac Asimov really
obj.fullName();
wrote around 500
// → "Isaac Asimov" books!
BREAKING PRINCIPLE #1 IN FP
Breaking this principle without classes in FP means hiding data in the lexical scope of
a function. The next listing provides an example of this.
ListingA.2 Breaking Principle #1 in FP
function createAuthorObject(firstName, lastName, books) {
return {
fullName: function() {
return firstName + " " + lastName;
},
isProlific: function () {
return books > 100;
}
};
}
var obj = createAuthorObject("Isaac", "Asimov", 500);
obj.fullName();
// → "Isaac Asimov"
ADHERING TO PRINCIPLE #1 IN OOP
Listing A.3 shows an example that adheres to Principle #1 in OOP. Compliance with
this principle may be achieved even with classes by writing programs such that:
 The code consists of static methods.
 The data is encapsulated in data classes (classes that are merely containers of
data).
ListingA.3 Following Principle #1 in OOP
class AuthorData {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
}
class NameCalculation {
static fullName(data) {
return data.firstName + " " + data.lastName;
}
}
class AuthorRating {
static isProlific (data) {
return data.books > 100;
}
}

=== 페이지 365 ===
A.1 Principle #1: Separate code from data 337
var data = new AuthorData("Isaac", "Asimov", 500);
NameCalculation.fullName(data);
// → "Isaac Asimov"
ADHERING TO PRINCIPLE #1 IN FP
Listing A.4 shows an example that adheres to Principle #1 in FP. Compliance with this
principle means separating code from data.
ListingA.4 Following Principle #1 in FP
function createAuthorData(firstName, lastName, books) {
return {
firstName: firstName,
lastName: lastName,
books: books
};
}
function fullName(data) {
return data.firstName + " " + data.lastName;
}
function isProlific (data) {
return data.books > 100;
}
var data = createAuthorData("Isaac", "Asimov", 500);
fullName(data);
// → "Isaac Asimov"
A.1.2 Benefits of Principle #1
Having illustrated how to follow or break Principle #1 both in OOP and FP, let’s look
at the benefits that Principle #1 brings to our programs. Careful separation of code
from data benefits our programs in the following ways:
 Code can be reused in different contexts.
 Code can be tested in isolation.
 Systems tend to be less complex.
BENEFIT #1: CODE CAN BE REUSED IN DIFFERENT CONTEXTS
Imagine that besides the author entity, there is a user entity that has nothing to do
with authors but has two of the same data fields as the author entity: firstName and
lastName. The logic of calculating the full name is the same for authors and users—
retrieving the values of two fields with the same names. However, in traditional OOP
as in the version with createAuthorObject in listing A.5, the code of fullName cannot
be reused on a user in a straightforward way because it is locked inside the Author class.
ListingA.5 The code of fullName is locked in the Author class
class Author {
constructor(firstName, lastName, books) {

=== 페이지 366 ===
338 APPENDIX A Principles of data-oriented programming
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
fullName() {
return this.firstName + " " + this.lastName;
}
isProlific() {
return this.books > 100;
}
}
One way to achieve code reusability when code and data are mixed is to use OOP
mechanisms like inheritance or composition to let the User and Author classes use
the same fullName method. These techniques are adequate for simple use cases, but
in real-world systems, the abundance of classes (either base classes or composite
classes) tends to increase complexity.
Listing A.6 shows a simple way to avoid inheritance. In this listing, we duplicate the
code of fullName inside a createUserObject function.
ListingA.6 Duplicating code in OOP to avoid inheritance
function createAuthorObject(firstName, lastName, books) {
var data = {firstName: firstName, lastName: lastName, books: books};
return {
fullName: function fullName() {
return data.firstName + " " + data.lastName;
}
};
}
function createUserObject(firstName, lastName, email) {
var data = {firstName: firstName, lastName: lastName, email: email};
return {
fullName: function fullName() {
return data.firstName + " " + data.lastName;
}
};
}
var obj = createUserObject("John", "Doe", "john@doe.com");
obj.fullName();
// → "John Doe"
In DOP, no modification to the code that deals with author entities is necessary in
order to make it available to user entities, because:
 The code that deals with full name calculation is separate from the code that
deals with the creation of author data.
 The function that calculates the full name works with any hash map that has a
firstName and a lastName field.

=== 페이지 367 ===
A.1 Principle #1: Separate code from data 339
It is possible to leverage the fact that data relevant to the full name calculation for a
user and an author has the same shape. With no modifications, the fullName function
works properly both on author data and on user data as the following listing shows.
ListingA.7 The same code on data entities of different types (FP style)
function createAuthorData(firstName, lastName, books) {
return {firstName: firstName, lastName: lastName, books: books};
}
function fullName(data) {
return data.firstName + " " + data.lastName;
}
function createUserData(firstName, lastName, email) {
return {firstName: firstName, lastName: lastName, email: email};
}
var authorData = createAuthorData("Isaac", "Asimov", 500);
fullName(authorData);
var userData = createUserData("John", "Doe", "john@doe.com");
fullName(userData);
// → "John Doe"
When Principle #1 is applied in OOP, code reuse is straightforward even when classes
are used. In statically-typed OOP languages like Java or C, we would have to create a
common interface for AuthorData and UserData. In a dynamically-typed language
like JavaScript, however, that is not required. The code of NameCalculation.full-
Name() works both with author data and user data as the next listing demonstrates.
ListingA.8 The same code on data entities of different types (OOP style)
class AuthorData {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
}
class NameCalculation {
static fullName(data) {
return data.firstName + " " + data.lastName;
}
}
class UserData {
constructor(firstName, lastName, email) {
this.firstName = firstName;
this.lastName = lastName;
this.email = email;

=== 페이지 368 ===
340 APPENDIX A Principles of data-oriented programming
}
}
var userData = new UserData("John", "Doe", "john@doe.com");
NameCalculation.fullName(userData);
var authorData = new AuthorData("Isaac", "Asimov", 500);
NameCalculation.fullName(authorData);
// → "John Doe"
TIP When code is separate from data, it is straightforward to reuse code in different
contexts. This benefit is achievable both in FP and in OOP.
BENEFIT #2: CODE CAN BE TESTED IN ISOLATION
A similar benefit is the ability to test code in an isolated context. When code is not sep-
arate from data, it is necessary to instantiate an object to test its methods. For instance,
in order to test the fullName code that lives inside the createAuthorObject function,
we need to instantiate an author object as the following listing shows.
ListingA.9 Testing code when code and data are mixed
var author = createAuthorObject("Isaac", "Asimov", 500);
author.fullName() === "Isaac Asimov"
// → true
In this simple scenario, it is not overly burdensome. We only load (unnecessarily) the
code for isProlific. Although in a real-world situation, instantiating an object might
involve complex and tedious setup.
In the DOP version, where createAuthorData and fullName are separate, we can
create the data to be passed to fullName in isolation, testing fullName in isolation as
well. The following listing provides an example.
ListingA.10 Testing code in isolation (FP style)
var author = {
firstName: "Isaac",
lastName: "Asimov"
};
fullName(author) === "Isaac Asimov"
// → true
If classes are used, it is only necessary to instantiate a data object. We do not need to
load the code for isProlific, which lives in a separate class than fullName, in order
to test fullName. The next listing lays out an example of this approach.
ListingA.11 Testing code in isolation (OOP style)
var data = new AuthorData("Isaac", "Asimov");
NameCalculation.fullName(data) === "Isaac Asimov"
// → true

=== 페이지 369 ===
A.1 Principle #1: Separate code from data 341
TIP Writing tests is easier when code is separated from data.
BENEFIT #3: SYSTEMS TEND TO BE LESS COMPLEX
The third benefit of applying Principle #1 to our programs is that systems tend to be less
complex. This benefit is the deepest one but also the one that is most subtle to explain.
The type of complexity I refer to is the one that makes systems hard to understand
as defined in the paper, “Out of the Tar Pit,” by Ben Moseley and Peter Marks (http://
mng.bz/enzq). It has nothing to do with the complexity of the resources consumed by
a program. Similarly, references to simplicity mean not complex (in other words, easy to
understand).
 NOTE Complex in the context of this book means hard to understand.
Keep in mind that complexity and simplicity (like hard and easy) are not absolute but
relative concepts. The complexity of two systems can be compared to determine
whether system A is more complex (or simpler) than system B. When code and data
are kept separate, the system tends to be easier to understand for two reasons:
 The scope of a data entity or a code entity is smaller than the scope of an entity that com-
bines code and data. Each entity is therefore easier to understand.
 Entities of the system are split into disjoint groups: code and data. Entities therefore
have fewer relations to other entities.
This insight is illustrated in a class diagram of our fictitious Library Management Sys-
tem, where code and data are mixed. It is not necessary to know the details of the
classes of this system to see that the diagram in figure A.2 represents a complex system;
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
Figure A.2 A class
diagram overview for the
C BookLending * Library Management
System

=== 페이지 370 ===
342 APPENDIX A Principles of data-oriented programming
this in the sense that it is hard to understand. The system is hard to understand because
there are many dependencies between the entities that compose the system.
The most complex entity of the system in figure A.2 is the Librarian entity, which
is connected via six relations to other entities. Some relations are data relations (asso-
ciation and composition), and some relations are code relations (inheritance and
dependency). But in this design, the Librarian entity mixes code and data, and there-
fore, it has to be involved in both data and code relations. If each entity of the system
is split into a code entity and a data entity without making any further modification to the
system, the result (see figure A.3) is made of two disconnected parts:
 The left part is made only of data entities and data relations: association and
composition.
 The right part is made only of code entities and code relations: dependency
and inheritance.
C LibraryData * C LibrarianData C CatalogCode
*
C MemberData C CatalogData C LibrarianCode
*
C BookData C MemberCode C BookLendingCode C BookItemCode
*
* *
C BookItemData C AuthorData C UserCode C BookItem
*
C BookLendingData
Figure A.3 A class diagram where every class is split into code and data entities
The new system, where code and data are separate, is easier to understand than the
original system, where code and data are mixed. Thus, the data part of the system and
the code part of the system can each be understood on its own.
TIP A system made of disconnected parts is less complex than a system made of a sin-
gle part.
One could argue that the complexity of the original system, where code and data are
mixed, is due to a bad design and that an experienced OOP developer would have
designed a simpler system using smart design patterns. That is true, but in a sense, it is

=== 페이지 371 ===
A.1 Principle #1: Separate code from data 343
irrelevant. The point of Principle #1 is that a system made of entities that do not com-
bine code and data tends to be simpler than a system made of entities that do combine
code and data.
It has been said many times that simplicity is hard. According to the first principle of
DOP, simplicity is easier to achieve when separating code and data.
TIP Simplicity is easier to achieve when code is separated from data.
A.1.3 Cost for Principle #1
This section looks at the cost involved when we implement Principle #1. The price we
pay in order to benefit from the separation between code and data is threefold:
 There is no control on what code can access what data.
 There is no packaging.
 Our systems are made from more entities.
COST #1: THERE IS NO CONTROL ON WHAT CODE CAN ACCESS WHAT DATA
When code and data are mixed, it is easy to understand what pieces of code can access
what kinds of data. For example, in OOP, the data is encapsulated in an object, which
guarantees that the data is accessible only by the object’s methods. In DOP, data
stands on its own. It is transparent if you like, and as a consequence, it can be accessed
by any piece of code.
When refactoring the shape of some data, every place in our code that accesses this
kind of data must be known. Moreover, without the application of Principle #3 (enforc-
ing data immutability), which we discuss later, accessing data by any piece of code is
inherently unsafe. In that case, it would be hard to guarantee the validity of our data.
TIP Data safety is ensured by another principle (Principle #3) that enforces data
immutability.
COST #2: THERE IS NO PACKAGING
One of the benefits of mixing code and data is that when you have an object in hand,
it is a package that contains both the code (via methods) and the data (via members).
As a consequence, it is easy to discover how to manipulate the data: you look at the
methods of the class.
In DOP, the code that manipulates the data could be anywhere. For example,
createAuthorData might be in one file and fullName in another file. This makes it
difficult for developers to discover that the fullName function is available. In some sit-
uations, it could lead to wasted time and unnecessary code duplication.
COST #3: OUR SYSTEMS ARE MADE FROM MORE ENTITIES
Let’s do simple arithmetic. Imagine a system made of N classes that combine code and
data. When you split the system into code entities and data entities, you get a system
made of 2N entities. This calculation is not accurate, however, because usually when
you separate code and data, the class hierarchy tends to get simpler as we need less

=== 페이지 372 ===
344 APPENDIX A Principles of data-oriented programming
class inheritance and composition. Therefore, the number of classes in the resulting
system will probably be somewhere between N and 2N.
On one hand, when adhering to Principle #1, the entities of the system are sim-
pler. On the other hand, there are more entities. This cost is mitigated by Principle
#2, which guides us to represent our data with generic data structures.
TIP When adhering to Principle #1, systems are made of simpler entities, but there
are more of them.
A.1.4 Summary of Principle #1
DOP requires the separation of code from data. In OOP languages, aggregate code in
static methods and data in classes with no methods. In FP languages, avoid hiding data
in the lexical scope of functions.
Separating code from data comes at a price. It reduces control over what pieces of
code access our data and can cause our systems to be made of more entities. But it’s
worth paying the price because, when adhering to this principle, our code can be
reused in different contexts in a straightforward way and tested in isolation. Moreover,
a system made of separate entities for code and data tends to be easier to understand.
DOP Principle #1: Separate code from data
To follow this principle, we separate code from data in such a way that the code
resides in functions whose behavior does not depend on data that is encapsulated
in the function’s context. The following diagram provides a visual representation
of this.
DOPPrinciple #1: Separate code from data
FP
Code
System OOP
Data
 Benefits include
– Code can be reused in different contexts.
– Code can be tested in isolation.
– Systems tend to be less complex.
 The cost for implementing Principle #1 includes
– No control on what code accesses which data.
– No packaging.
– More entities.
