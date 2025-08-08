# B.1.1 Accessing non-nested map fields with dynamic getters

**페이지**: 364-365
**계층**: Data-Oriented Programming (node0) > Appendix B—Generic data access in statically-typed languages (node1)
**추출 시간**: 2025-08-06 19:47:36

---


--- 페이지 364 ---

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

--- 페이지 364 끝 ---


--- 페이지 365 ---

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

--- 페이지 365 끝 ---
