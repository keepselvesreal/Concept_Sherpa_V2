# Appendix A—Principles of data-oriented programming

**Level:** 0
**페이지 범위:** 361 - 391
**총 페이지 수:** 31
**ID:** 147

---

=== 페이지 361 ===
appendix A
Principles of data-oriented
programming
Data-oriented programming (DOP) is a programming paradigm aimed at simplify-
ing the design and implementation of software systems, where information is at the
center in systems such as frontend or backend web applications and web services,
for example. Instead of designing information systems around software constructs
that combine code and data (e.g., objects instantiated from classes), DOP encour-
ages the separation of code from data. Moreover, DOP provides guidelines about
how to represent and manipulate data.
TIP In DOP, data is treated as a first-class citizen.
The essence of DOP is that it treats data as a first-class citizen. It gives developers
the ability to manipulate data inside a program with the same simplicity as they
manipulate numbers or strings. Treating data as a first-class citizen is made possible
by adhering to four core principles:
 Separating code (behavior) from data.
 Representing data with generic data structures.
 Treating data as immutable.
 Separating data schema from data representation.
When these four principles are combined, they form a cohesive whole as figure A.1
shows. Systems built using DOP are simpler and easier to understand, so the devel-
oper experience is significantly improved.
TIP In a data-oriented system, code is separated from data. Data is represented
with generic data structures that are immutable and have a separate schema.
333

=== 페이지 362 ===
334 APPENDIX A Principles of data-oriented programming
Principle #2: Represent Immutable
data with generic data
structures.
Generic
Mutable
Representation
Principle #3:
Specific
Data is
Data immutable.
Schema
Principle #4: Separate
data schema from data
Data-oriented
representation.
programming
Functional
Code
Principle #1: programming
Separate code
from data.
Object-oriented
programming
Figure A.1 The principles of DOP
Notice that DOP principles are language-agnostic. They can be adhered to (or bro-
ken) in
 Object-oriented programming (OOP) languages such as Java, C#, C++, etc.
 Functional programming (FP) languages such as Clojure, OCaml, Haskell, etc.
 Languages that support both OOP and FP such as JavaScript, Python, Ruby,
Scala, etc.
TIP DOP principles are language-agnostic.
 NOTE For OOP developers, the transition to DOP might require more of a mind
shift than for FP developers because DOP prohibits the encapsulation of data in state-
ful classes.
This appendix succinctly illustrates how these principles can be applied or broken in
JavaScript. Mentioned briefly are the benefits of adherence to each principle, and the
costs paid to enjoy those benefits. This appendix also illustrates the principles of DOP
via simple code snippets. Throughout the book, the application of DOP principles to
production information systems is explored in depth.

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

=== 페이지 373 ===
A.2 Principle #2: Represent data with generic data structures 345
A.2 Principle #2: Represent data with generic data
structures
When adhering to Principle #1, code is separated from data. DOP is not opinionated
about the programming constructs to use for organizing the code, but it has a lot to
say about how the data should be represented. This is the theme of Principle #2.
The most common generic data structures are maps (aka dictionaries) and arrays
(or lists). But other generic data structures (e.g., sets, trees, and queues) can be used
as well. Principle #2 does not deal with the mutability or the immutability of the data.
That is the theme of Principle #3.
PRINCIPLE #2 Represent application data with generic data structures.
A.2.1 Illustration of Principle #2
In DOP, data is represented with generic data structures (like maps and arrays)
instead of instantiating data via specific classes. In fact, most of the data entities that
appear in a typical application can be represented with maps and arrays (or lists). But
there exist other generic data structures (e.g., sets, lists, queues, etc.) that might be
required in some use cases. Let’s look at the same simple example we used to illustrate
Principle #1 (data that represents an author).
An author is a data entity with a firstName, a lastName, and the number of books
they have written. Principle #2 is broken when we use a specific class to represent an
author as this listing reveals.
ListingA.12 Breaking Principle #2 in OOP
class AuthorData {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
}
Principle #2 is followed when using a map (a dictionary or an associative array) as a
generic data structure that represents an author. The following listing illustrates how
we can follow this principle in OOP.
ListingA.13 Following Principle #2 in OOP
function createAuthorData(firstName, lastName, books) {
var data = new Map;
data.firstName = firstName;
data.lastName = lastName;

=== 페이지 374 ===
346 APPENDIX A Principles of data-oriented programming
data.books = books;
return data;
}
In a language like JavaScript, we can also instantiate a map via a data literal, which is a
bit more convenient. The following listing shows an example.
ListingA.14 Following Principle #2 with map literals
function createAuthorData(firstName, lastName, books) {
return {
firstName: firstName,
lastName: lastName,
books: books
};
}
A.2.2 Benefits of Principle #2
Using generic data structures to represent data has multiple benefits. We cover these
benefits in greater detail in the following sections:
 The ability to use generic functions that are not limited to our specific use case
 A flexible data model
USING FUNCTIONS THAT ARE NOT LIMITED TO A SPECIFIC USE CASE
Using generic data structures to represent data makes it possible to manipulate data
with a rich set of functions that are available on those data structures natively in our
programming language. Additionally, third-party libraries also provide more of these
functions. For instance, JavaScript natively provides some basic functions on maps and
arrays, and third-party libraries like Lodash (https://lodash.com/) extend the func-
tionality with even more functions. There is a famous quote by Alan Perlis that sum-
marizes this benefit:
It is better to have 100 functions operate on one data structure than to have 10 functions
operate on 10 data structures.
—Alan Perlis (“Epigrams on Programming,” 1982)
When an author is represented as a map, the author can be serialized into JSON
using JSON.stringify(), which is part of JavaScript. The following listing provides
an example.
ListingA.15 [#serialize-klipse-js],reftext="A.1"
var data = createAuthorData("Isaac", "Asimov", 500);
JSON.stringify(data);
// → "{\"firstName\":\"Isaac\",\"lastName\":\"Asimov\",\"books\":500}"
Serializing author data without the number of books can be accomplished via Lodash’s
_.pick() function. The following listing uses _.pick() to create an object with a sub-
set of keys.

=== 페이지 375 ===
A.2 Principle #2: Represent data with generic data structures 347
ListingA.16 Manipulating data with generic functions
var data = createAuthorData("Isaac", "Asimov", 500);
var dataWithoutBooks = _.pick(data, ["firstName", "lastName"]);
JSON.stringify(dataWithoutBooks);
// → "{\"firstName\":\"Isaac\",\"lastName\":\"Asimov\"}"
TIP When adhering to Principle #2, a rich set of functionality is available for data
manipulation.
FLEXIBLE DATA MODEL
When using generic data structures, the data model is flexible, and data is not forced
into a specific shape. Data can be created with no predefined shape, and its shape can
be modified at will.
In classic OOP, when not adhering to Principle #2, each piece of data is instanti-
ated via a class and must follow a rigid shape. When a slightly different data shape is
needed, a new class must be defined. Take, for example, AuthorData, a class that rep-
resents an author entity made of three fields: firstName, lastName, and books. Sup-
pose that you want to add a field called fullName with the full name of the author. If
we fail to adhere to Principle #2, a new class, AuthorDataWithFullName, must be
defined. However, when using generic data structures, fields can be added to (or
removed from) a map on the fly as the following listing shows.
ListingA.17 Adding a field on the fly
var data = createAuthorData("Isaac", "Asimov", 500);
data.fullName = "Isaac Asimov";
TIP Working with a flexible data model is particularly useful in applications where
the shape of the data tends to be dynamic (e.g., web apps and web services).
Part 1 of the book explores in detail the benefits of a flexible data model in real-world
applications. Next, let’s explore the cost for adhering to Principle #2.
A.2.3 Cost for Principle #2
As with any programming principle, using this principle comes with its own set of trade-
offs. The price paid for representing data with generic data structures is as follows:
 There is a slight performance hit.
 No data schema is required.
 No compile-time check that the data is valid is necessary.
 In some statically-typed languages, type casting is needed.
COST #1: PERFORMANCE HIT
When specific classes are used to instantiate data, retrieving the value of a class mem-
ber is fast because the compiler knows how the data will look and can do many optimi-
zations. With generic data structures, it is harder to optimize, so retrieving the value

=== 페이지 376 ===
348 APPENDIX A Principles of data-oriented programming
associated to a key in a map, for example, is a bit slower than retrieving the value of a
class member. Similarly, setting the value of an arbitrary key in a map is a bit slower
than setting the value of a class member. In most programming languages, this perfor-
mance hit is not significant, but it is something to keep in mind.
TIP Retrieving and storing the value associated to an arbitrary key from a map is a bit
slower than with a class member.
COST #2: NO DATA SCHEMA
When data is instantiated from a class, the information about the data shape is in the
class definition. Every piece of data has an associated data shape. The existence of
data schema at a class level is useful for developers and for IDEs because
 Developers can easily discover the expected data shape.
 IDEs provide features like field name autocompletion.
When data is represented with generic data structures, the data schema is not part of
the data representation. As a consequence, some pieces of data might have an associ-
ated data schema and other pieces of data do not (see Principle #4).
TIP When generic data structures are used to store data, the data shape is not part of
the data representation.
COST #3: NO COMPILE-TIME CHECK THAT THE DATA IS VALID
Look again at the fullName function in the following listing, which was created to
explore Principle #1. This function receives the data it manipulates as an argument.
ListingA.18 Declaring the fullName function
function fullName(data) {
return data.firstName + " " + data.lastName;
}
When data is passed to fullName that does not conform to the shape fullName
expects, an error occurs at run time. With generic data structures, mistyping the field
storing the first name (e.g., fistName instead of firstName) does not result in a
compile-time error or an exception. Rather, firstName is mysteriously omitted from
the result. The following listing shows this unexpected behavior.
ListingA.19 Unexpected behavior with invalid data
fullName({fistName: "Issac", lastName: "Asimov"});
// → "undefined Asimov"
When we instantiate data via classes with a rigid data shape, this type of error is caught
at compile time. This drawback is mitigated by the application of Principle #4 that
deals with data validation.

=== 페이지 377 ===
A.2 Principle #2: Represent data with generic data structures 349
TIP When data is represented with generic data structures, data shape errors are
caught only at run time.
COST #4: THE NEED FOR EXPLICIT TYPE CASTING
In some statically-typed languages, explicit type casting is needed. This section takes a
look at explicit type casting in Java and at dynamic fields in C#.
In a statically-typed language like Java, author data can be represented as a map
whose keys are of type string and whose values are of types Object. For example, in
Java, author data is represented by a Map<String, Object> as the following listing
illustrates.
ListingA.20 Author data as a string map in Java
var asimov = new HashMap<String, Object>();
asimov.put("firstName", "Isaac");
asimov.put("lastName", "Asimov");
asimov.put("books", 500);
Because the information about the exact type of the field values is not available at
compile time, when accessing a field, an explicit type cast is required. For instance, in
order to check whether an author is prolific, the value of the books field must be type
cast to an integer as the next listing shows.
ListingA.21 Type casting is required when accessing a field in Java
class AuthorRating {
static boolean isProlific (Map<String, Object> data) {
return (int)data.get("books") > 100;
}
}
Some Java JSON serialization libraries like Gson (https://github.com/google/gson)
support serialization of maps of type Map<String, Object>, without requiring the user
to do any type casting. All the magic happens behind the scenes!
C# supports a dynamic data type called dynamic (see http://mng.bz/voqJ), which
allows type checking to occur at run time. Using this feature, author data is repre-
sented as a dictionary, where the keys are of type string, and the values are of type
dynamic. The next listing provides this representation.
ListingA.22 Author data as a dynamic string map in C#
var asimov = new Dictionary<string, dynamic>();
asimov["name"] = "Isaac Asimov";
asimov["books"] = 500;
The information about the exact type of the field values is resolved at run time. When
accessing a field, no type cast is required. For instance, when checking whether an

=== 페이지 378 ===
350 APPENDIX A Principles of data-oriented programming
author is prolific, the books field can be accessed as though it were declared as an
integer as in this listing.
ListingA.23 Type casting is not needed when accessing dynamic fields in C#
class AuthorRating {
public static bool isProlific (Dictionary<String, dynamic> data) {
return data["books"] > 100;
}
}
A.2.4 Summary of Principle #2
DOP uses generic data structures to represent data. This might cause a (small) perfor-
mance hit and impose the need to manually document the shape of data because the
compiler cannot validate it statically. Adherence to this principle enables the manipu-
lation of data with a rich set of generic functions (provided by the language and by
third-party libraries). Additionally, our data model is flexible. At this point, the data
can be either mutable or immutable. The next principle (Principle #3) illustrates the
value of immutability.
DOP Principle #2: Represent data with generic data structures
To comply with this principle, we represent application data with generic data struc-
tures, mostly maps and arrays (or lists). The following diagram shows a visual repre-
sentation of this principle.
DOPPrinciple #2: Represent data with generic data structures
Specific
Data
Generic
 Benefits include
– Using generic functions that are not limited to our specific use case
– A flexible data model
 The cost for implementing this principle includes
– There is a slight performance hit.
– No data schema is required.
– No compile time check that the data is valid is necessary.
– In some statically-typed languages, explicit type casting is needed.

=== 페이지 379 ===
A.3 Principle #3: Data is immutable 351
A.3 Principle #3: Data is immutable
With data separated from code and represented with generic data structures, how are
changes to the data managed? DOP is very strict on this question. Mutation of data is
not allowed! In DOP, changes to data are accomplished by creating new versions of
the data. The reference to a variable may be changed so that it refers to a new version of
the data, but the value of the data itself must never change.
PRINCIPLE #3 Data is immutable.
A.3.1 Illustration of Principle #3
Think about the number 42. What happens to 42 when you add 1 to it? Does it
become 43? No, 42 stays 42 forever! Now, put 42 inside an object: {num: 42}. What
happens to the object when you add 1 to 42? Does it become 43? It depends on the
programming language.
 In Clojure, a programming language that embraces data immutability, the value
of the num field stays 42 forever, no matter what.
 In many programming languages, the value of the num field becomes 43.
For instance, in JavaScript, mutating the field of a map referred by two variables has
an impact on both variables. The following listing demonstrates this.
ListingA.24 Mutating data referred by two variables impact both variables
var myData = {num: 42};
var yourData = myData;
yourData.num = yourData.num + 1;
console.log(myData.num);
// → 43
Now, myData.num equals 43. According to DOP, however, data should never change!
Instead of mutating data, a new version of it is created. A naive (and inefficient) way
to create a new version of data is to clone it before modifying it. For instance, in list-
ing A.25, there is a function that changes the value of a field inside an object by clon-
ing the object via Object.assign, provided natively by JavaScript. When changeValue
is called on myData, myData is not affected; myData.num remains 42. This is the essence
of data immutability!
ListingA.25 Data immutability via cloning
function changeValue(obj, k, v) {
var res = Object.assign({}, obj);
res[k] = v;

=== 페이지 380 ===
352 APPENDIX A Principles of data-oriented programming
return res;
}
var myData = {num: 42};
var yourData = changeValue(myData, "num", myData.num + 1);
console.log(myData.num);
// → 43
Embracing immutability in an efficient way, both in terms of computation and mem-
ory, requires a third-party library like Immutable.js (https://immutable-js.com/), which
provides an efficient implementation of persistent data structures (aka immutable
data structures). In most programming languages, libraries exist that provide an effi-
cient implementation of persistent data structures.
With Immutable.js, JavaScript native maps and arrays are not used, but rather,
immutable maps and immutable lists are instantiated via Immutable.Map and Immutable
.List. An element of a map is accessed using the get method. A new version of the
map is created when a field is modified with the set method.
Listing A.26 shows how to create and manipulate immutable data efficiently with a
third-party library. In the output, yourData.get("num") is 43, but myData.get("num")
remains 42.
ListingA.26 Creating and manipulating immutable data
var myData = Immutable.Map({num: 42})
var yourData = myData.set("num", 43);
console.log(yourData.get("num"));
// → 43
console.log(myData.get("num"));
// → 42
TIP When data is immutable, instead of mutating data, a new version of it is created.
A.3.2 Benefits of Principle #3
When programs are constrained from mutating data, we derive benefit in numerous
ways. The following sections detail these benefits:
 Data access to all with confidence
 Predictable code behavior
 Fast equality checks
 Concurrency safety for free
BENEFIT #1: DATA ACCESS TO ALL WITH CONFIDENCE
According to Principle #1 (separate code from data), data access is transparent. Any
function is allowed to access any piece of data. Without data immutability, we must be
careful when passing data as an argument to a function. We can either make sure the
function does not mutate the data or clone the data before it is passed to the function.
When adhering to data immutability, none of this is required.

=== 페이지 381 ===
A.3 Principle #3: Data is immutable 353
TIP When data is immutable, it can be passed to any function with confidence
because data never changes.
BENEFIT #2: PREDICTABLE CODE BEHAVIOR
As an illustration of what is meant by predictable, here is an example of an unpredictable
piece of code that does not adhere to data immutability. Take a look at the piece of
asynchronous JavaScript code in the following listing. When data is mutable, the behav-
ior of asynchronous code is not predictable.
ListingA.27 Unpredictable asynchronous code when data is mutable
var myData = {num: 42};
setTimeout(function (data){
console.log(data.num);
}, 1000, myData);
myData.num = 0;
The value of data.num inside the timeout callback is not predictable. It depends on
whether the data is modified by another piece of code during the 1,000 ms of the
timeout. However, with immutable data, it is guaranteed that data never changes and
that data.num is always 42 inside the callback.
TIP When data is immutable, the behavior of code that manipulates data is predictable.
BENEFIT #3: FAST EQUALITY CHECKS
With UI frameworks like React.js, there are frequent checks to see what portion of the
UI data has been modified since the previous rendering cycle. Portions that did not
change are not rendered again. In fact, in a typical frontend application, most of the
UI data is left unchanged between subsequent rendering cycles.
In a React application that does not adhere to data immutability, it is necessary to
check every (nested) part of the UI data. However, in a React application that follows
data immutability, it is possible to optimize the comparison of the data for the case
where data is not modified. Indeed, when the object address is the same, then it is cer-
tain that the data did not change.
Comparing object addresses is much faster than comparing all the fields. In part 1
of the book, fast equality checks are used to reconcile between concurrent mutations
in a highly scalable production system.
TIP Immutable data enables fast equality checks by comparing data by reference.
BENEFIT #4: FREE CONCURRENCY SAFETY
In a multi-threaded environment, concurrency safety mechanisms (e.g., mutexes)
are often used to prevent the data in thread A from being modified while it is accessed
in thread B. In addition to the slight performance hit they cause, concurrency safety
mechanisms impose a mental burden that makes code writing and reading much
more difficult.

=== 페이지 382 ===
354 APPENDIX A Principles of data-oriented programming
TIP Adherence to data immutability eliminates the need for a concurrency mecha-
nism. The data you have in hand never changes!
A.3.3 Cost for Principle #3
As with the previous principles, applying Principle #3 comes at a price. The following
sections look at these costs:
 Performance hit
 Required library for persistent data structures
COST #1: PERFORMANCE HIT
As mentioned earlier, implementations of persistent data structures exist in most pro-
gramming languages. But even the most efficient implementation is a bit slower than
the in-place mutation of the data. In most applications, the performance hit and the
additional memory consumption involved in using immutable data structures is not
significant. But this is something to keep in mind.
COST #2: REQUIRED LIBRARY FOR PERSISTENT DATA STRUCTURES
In a language like Clojure, the native data structures of the language are immutable. How-
ever, in most programming languages, adhering to data immutability requires the inclu-
sion a third-party library that provides an implementation of persistent data structures.
The fact that the data structures are not native to the language means that it is dif-
ficult (if not impossible) to enforce the usage of immutable data across the board.
Also, when integrating with third-party libraries (e.g., a chart library), persistent data
structures must be converted into equivalent native data structures.
A.3.4 Summary of Principle #3
DOP considers data as a value that never changes. Adherence to this principle results
in code that is predictable even in a multi-threaded environment, and equality checks
are fast. However, a non-negligible mind shift is required, and in most programming
languages, a third-party library is needed to provide an efficient implementation of
persistent data structures.
DOP Principle #3: Data is immutable
To adhere to this principle, data is represented with immutable structures. The fol-
lowing diagram provides a visual representation of this.
DOPPrinciple #3: Data is immutable
Mutable
Data
Immutable

=== 페이지 383 ===
A.4 Principle #4: Separate data schema from data representation 355
 Benefits include
– Data access to all with confidence
– Predictable code behavior
– Fast equality checks
– Concurrency safety for free
 The cost for implementing Principle #3 includes
– A performance hit
– Required library for persistent data structures
A.4 Principle #4: Separate data schema from data
representation
With data separated from code and represented with generic and immutable data
structures, now comes the question of how do we express the shape of the data? In
DOP, the expected shape is expressed as a data schema that is kept separated from the
data itself. The main benefit of Principle #4 is that it allows developers to decide
which pieces of data should have a schema and which pieces of data should not.
PRINCIPLE #4 Separate data schema from data representation.
A.4.1 Illustration of Principle #4
Think about handling a request for the addition of an author to the system. To keep things
simple, imagine that such a request contains only basic information about the author:
their first name and last name and, optionally, the number of books they have written. As
seen in Principle #2 (represent data with generic data structures), in DOP, request data
is represented as a string map, where the map is expected to have three fields:
 firstName—a string
 lastName—a string
 books—a number (optional)
In DOP, the expected shape of data is represented as data that is kept separate from the
request data. For instance, JSON schema (https://json-schema.org/) can represent the
data schema of the request with a map. The following listing provides an example.
ListingA.28 The JSON schema for an addAuthor request data
Data is expected to be a map (in JSON,
a map is called an object).
Only firstName and
var addAuthorRequestSchema = {
lastName fields are
"type": "object",
required.
"required": ["firstName", "lastName"],

=== 페이지 384 ===
356 APPENDIX A Principles of data-oriented programming
"properties": {
"firstName": {"type": "string"},
firstName must
"lastName": {"type": "string"},
be a string.
"books": {"type": "integer"}
}
books must be a number lastName must
};
(when it is provided). be a string.
A data validation library is used to check whether a piece of data conforms to a data
schema. For instance, we could use Ajv JSON schema validator (https://ajv.js.org/) to
validate data with the validate function that returns true when data is valid and
false when data is invalid. The following listing shows this approach.
ListingA.29 Data validation with Ajv
var validAuthorData = {
firstName: "Isaac",
lastName: "Asimov",
books: 500
};
ajv.validate(addAuthorRequestSchema,
validAuthorData); //
Data is
// → true
valid.
var invalidAuthorData = {
firstName: "Isaac",
lastNam: "Asimov",
books: "five hundred"
};
Data has lastNam instead
of lastName, and books is a
ajv.validate(addAuthorRequestSchema,
string instead of a number.
invalidAuthorData);
// → false
When data is invalid, the details about data validation failures are available in a human
readable format. The next listing shows this approach.
ListingA.30 Getting details about data validation failure
var invalidAuthorData = {
firstName: "Isaac", By default, Ajv stores only
the first data validation
lastNam: "Asimov",
error. Set allErrors: true
books: "five hundred"
to store all errors.
};
var ajv = new Ajv({allErrors: true}); Data validation errors are
stored internally as an
ajv.validate(addAuthorRequestSchema, invalidAuthorData);
array. In order to get a
ajv.errorsText(ajv.errors);
human readable string, use
// → "data should have required property 'lastName',
the errorsText function.
// → data.books should be number"

=== 페이지 385 ===
A.4 Principle #4: Separate data schema from data representation 357
A.4.2 Benefits of Principle #4
Separation of data schema from data representation provides numerous benefits. The
following sections describe these benefits in detail:
 Freedom to choose what data should be validated
 Optional fields
 Advanced data validation conditions
 Automatic generation of data model visualization
BENEFIT #1: FREEDOM TO CHOOSE WHAT DATA SHOULD BE VALIDATED
When data schema is separated from data representation, we can instantiate data with-
out specifying its expected shape. Such freedom is useful in various situations. For
example,
 Rapid prototyping or experimentation
 Code refactoring and data validation
Consider rapid prototyping. In classic OOP, we need to instantiate every piece of data
through a class. During the exploration phase of coding, when the final shape of our
data is not yet known, being forced to update the class definition each time the data
model changes slows us down. DOP enables a faster pace during the exploration
phase by delaying the data schema definition to a later phase.
One common refactoring pattern is split phase refactoring (https://refactoring
.com/catalog/splitPhase.html), where a single large function is split into multiple
smaller functions with private scope. We call these functions with data that has already
been validated by the larger function. In DOP, it is not necessary to specify the shape
of the arguments of the inner functions, relying on the data validation that has
already occurred.
Consider how to display some information about an author, such as their full name
and whether they are considered prolific. Using the code shown earlier to illustrate
Principle #2 to calculate the full name and the prolificity level of the author, one
might come up with a displayAuthorInfo function as the following listing shows.
ListingA.31 Displaying author information
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
var authorSchema = {
"type": "object",

=== 페이지 386 ===
358 APPENDIX A Principles of data-oriented programming
"required": ["firstName", "lastName"],
"properties": {
"firstName": {"type": "string"},
"lastName": {"type": "string"},
"books": {"type": "integer"}
}
};
function displayAuthorInfo(authorData) {
if(!ajv.validate(authorSchema, authorData)) {
throw "displayAuthorInfo called with invalid data";
};
console.log("Author full name is: ",
NameCalculation.fullName(authorData));
if(authorData.books == null) {
console.log("Author has not written any book");
} else {
if (AuthorRating.isProlific(authorData)) {
console.log("Author is prolific");
} else {
console.log("Author is not prolific");
}
}
}
Notice that the first thing done inside the body of displayAuthorInfo is to validate
that the argument passed to the function. Now, apply the split phase refactoring pat-
tern to this simple example and split the body of displayAuthorInfo into two inner
functions:
 displayFullName displays the author’s full name.
 displayProlificity displays whether the author is prolific or not.
The next listing shows the resulting code.
ListingA.32 Application of split phase refactoring pattern
function displayFullName(authorData) {
console.log("Author full name is: ",
NameCalculation.fullName(authorData));
}
function displayProlificity(authorData) {
if(authorData.books == null) {
console.log("Author has not written any book");
} else {
if (AuthorRating.isProlific(authorData)) {
console.log("Author is prolific");
} else {
console.log("Author is not prolific");
}
}
}

=== 페이지 387 ===
A.4 Principle #4: Separate data schema from data representation 359
function displayAuthorInfo(authorData) {
if(!ajv.validate(authorSchema, authorData)) {
throw "displayAuthorInfo called with invalid data";
};
displayFullName(authorData);
displayProlificity(authorData);
}
Having the data schema separated from data representation eliminates the need to
specify a data schema for the arguments of the inner functions displayFullName and
displayProlificity. It makes the refactoring process a bit smoother. In some cases,
the inner functions are more complicated, and it makes sense to specify a data schema
for their arguments. DOP gives us the freedom to choose!
BENEFIT #2: OPTIONAL FIELDS
In OOP, allowing a class member to be optional is not easy. For instance, in Java one
needs a special construct like the Optional class introduced in Java 8 (http://mng.bz/
4jWa). In DOP, it is natural to declare a field as optional in a map. In fact, in JSON
Schema, by default, every field is optional.
In order to make a field not optional, its name must be included in the required
array as, for instance, in the author schema in listing A.33, where only firstName and
lastName are required, and books is optional. Notice that when an optional field is
defined in a map, its value is validated against the schema.
ListingA.33 A schema with an optional field
var authorSchema = { books is not included
in required, as it is an
"type": "object",
optional field.
"required": ["firstName", "lastName"],
"properties": {
"firstName": {"type": "string"},
"lastName": {"type": "string"}, When present, books
must be a number.
"books": {"type": "number"}
}
};
Let’s illustrate how the validation function deals with optional fields. A map without a
books field is considered to be valid as listing A.34 shows. Alternatively, a map with a
books field, where the value is not a number, is considered to be invalid as listing A.35
shows.
ListingA.34 A valid map without an optional field
var authorDataNoBooks = {
"firstName": "Yehonathan",
"lastName": "Sharvit"
}; The validation
passes, as books is
an optional field.
ajv.validate(authorSchema, authorDataNoBooks);
// → true

=== 페이지 388 ===
360 APPENDIX A Principles of data-oriented programming
ListingA.35 An invalid map with an invalid optional field
var authorDataInvalidBooks = {
"firstName": "Albert",
"lastName": "Einstein",
"books": "Five"
}; The validation fails,
as books is not a
number.
validate(authorSchema, authorDataInvalidBooks);
// → false
BENEFIT #3: ADVANCED DATA VALIDATION CONDITIONS
In DOP, data validation occurs at run time. It allows the definition of data validation
conditions that go beyond the type of a field. For example, validating that a field is not
only a string, but a string with a maximal number of characters or a number com-
prised in a range of numbers as well.
JSON Schema supports many other advanced data validation conditions such as
regular expression validation for string fields or number fields that should be a multi-
ple of a given number. The author schema in listing A.36 expects firstName and
lastName to be strings of less than 100 characters, and books to be a number between
0 and 10,000.
ListingA.36 A schema with advanced data validation conditions
var authorComplexSchema = {
"type": "object",
"required": ["firstName", "lastName"],
"properties": {
"firstName": {
"type": "string",
"maxLength": 100
},
"lastName": {
"type": "string",
"maxLength": 100
},
"books": {
"type": "integer",
"minimum": 0,
"maximum": 10000
}
}
};
BENEFIT #4: AUTOMATIC GENERATION OF DATA MODEL VISUALIZATION
With the data schema defined as data, we can use several tools to generate data model
visualizations. With tools like JSON Schema Viewer (https://navneethg.github.io/
jsonschemaviewer/) and Malli (https://github.com/metosin/malli), a UML diagram
can be generated from a JSON schema.

=== 페이지 389 ===
A.4 Principle #4: Separate data schema from data representation 361
For instance, the JSON schema in listing A.37 defines the shape of a bookList
field, which is an array of books where each book is a map, and in figure A.4, it is visu-
alized as a UML diagram. These tools generate the UML diagram from the JSON
schema.
ListingA.37 A JSON schema with an array of objects
{
"type": "object",
"required": ["firstName", "lastName"],
"properties": {
"firstName": {"type": "string"},
"lastName": {"type": "string"},
"bookList": {
"type": "array",
"items": {
"type": "object",
"properties": {
"title": {"type": "string"},
"publicationYear": {"type": "integer"}
}
}
}
}
}
C Author
firstName: String
lastName: String
bookList: <Book>
C Book
title : String
Figure A.4 A UML visualization of the
publicationYear: Int
JSON schema in listing A.37
A.4.3 Cost for Principle #4
Applying Principle #4 comes with a price. The following sections look at these costs:
 Weak connection between data and its schema
 Small performance hit
COST #1: WEAK CONNECTION BETWEEN DATA AND ITS SCHEMA
By definition, when data schema and data representation are separated, the connec-
tion between data and its schema is weaker than when data is represented with classes.
Moreover, the schema definition language (e.g., JSON Schema) is not part of the

=== 페이지 390 ===
362 APPENDIX A Principles of data-oriented programming
programming language. It is up to the developer to decide where data validation is
necessary and where it is superfluous. As the idiom says, with great power comes great
responsibility.
COST #2: LIGHT PERFORMANCE HIT
As mentioned earlier, implementations of JSON schema validation exist in most
programming languages. In DOP, data validation occurs at run time, and it takes
some time to run the data validation. In OOP, data validation usually occurs at com-
pile time.
This drawback is mitigated by the fact that, even in OOP, some parts of data valida-
tion occur at run time. For instance, the conversion of a request JSON payload into an
object occurs at run time. Moreover, in DOP, it is quite common to have some data val-
idation parts enabled only during development and to disable them when the system
runs in production. As a consequence, this performance hit is not significant.
A.4.4 Summary of Principle #4
In DOP, data is represented with immutable generic data structures. When additional
information about the shape of the data is required, a data schema can be defined
(e.g., using JSON Schema). Keeping the data schema separate from the data repre-
sentation gives us the freedom to decide where data should be validated.
Moreover, data validation occurs at run time. As a consequence, data validation
conditions that go beyond the static data types (e.g., the string length) can be expressed.
However, with great power comes great responsibility, and it is up to the developer to
remember to validate data.
DOP Principle #4: Separate between data schema and data representation
To adhere to this principle, separate between data schema and data representation.
The following diagram illustrates this.
DOPPrinciple #4: Separate between data
schema and data representation
Representation
Data
Schema
 Benefits include
– Freedom to choose what data should be validated
– Optional fields
– Advanced data validation conditions
– Automatic generation of data model visualization

=== 페이지 391 ===
Conclusion 363
 The cost for implementing Principle #4 includes
– Weak connection between data and its schema
– A small performance hit
Conclusion
DOP simplifies the design and implementation of information systems by treating
data as a first-class citizen. This is made possible by adhering to four language-agnostic
core principles (see figure A.5):
 Separating code from data.
 Representing application data with generic data structures.
 Treating data as immutable.
 Separating data schema from data representation.
Principle #2: Represent Immutable
data with generic data
structures.
Generic
Mutable
Representation
Principle #3:
Specific
Data is
Data immutable.
Schema
Principle #4: Separate
data schema from data
Data-oriented
representation.
programming
Functional
Code
Principle #1: programming
Separate code
from data.
Object-oriented
programming
Figure A.5 The principles of DOP
This appendix has illustrated how each principle can be applied both in FP and OOP
languages. It also describes at a high level the benefits of each principle and the costs
of adherence to it.
