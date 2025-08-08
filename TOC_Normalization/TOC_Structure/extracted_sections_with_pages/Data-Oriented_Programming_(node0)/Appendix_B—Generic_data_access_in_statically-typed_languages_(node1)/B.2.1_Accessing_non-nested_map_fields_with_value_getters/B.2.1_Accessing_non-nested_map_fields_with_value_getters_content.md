# B.2.1 Accessing non-nested map fields with value getters

**페이지**: 366-367
**계층**: Data-Oriented Programming (node0) > Appendix B—Generic data access in statically-typed languages (node1)
**추출 시간**: 2025-08-06 19:47:37

---


--- 페이지 366 ---

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

--- 페이지 366 끝 ---


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
