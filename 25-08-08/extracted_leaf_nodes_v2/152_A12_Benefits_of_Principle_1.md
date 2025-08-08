# A.1.2 Benefits of Principle #1

**메타데이터:**
- ID: 152
- 레벨: 2
- 페이지: 365-370
- 페이지 수: 6
- 부모 ID: 149
- 텍스트 길이: 10572 문자

---

f Principle #1
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

A.1 Principle #1: Separate code from data 343
irrelevant. The point of Principle #1 is that a system made of entities that do not com-
bine code and data tends to be simpler than a system made of entities that do combine
code and data.
It has been said many times that simplicity is hard. According to the first principle of
DOP, simplicity is easier to achieve when separating code and data.
TIP Simplicity is easier to achieve when code is separated from data.