# B.2.2 Accessing nested map fields with value getters

**페이지**: 367-368
**계층**: Data-Oriented Programming (node0) > Appendix B—Generic data access in statically-typed languages (node1)
**추출 시간**: 2025-08-06 19:47:37

---


--- 페이지 367 ---

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

--- 페이지 367 끝 ---


--- 페이지 368 ---

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

--- 페이지 368 끝 ---
