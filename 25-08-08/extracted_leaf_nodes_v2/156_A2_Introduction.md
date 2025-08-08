# A.2 Introduction

**메타데이터:**
- ID: 156
- 레벨: 2
- 페이지: 373-374
- 페이지 수: 2
- 부모 ID: 155
- 텍스트 길이: 8353 문자

---

=== Page 372 ===
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

=== Page 373 ===
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

=== Page 374 ===
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

=== Page 375 ===
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