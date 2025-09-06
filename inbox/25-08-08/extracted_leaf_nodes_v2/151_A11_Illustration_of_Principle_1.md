# A.1.1 Illustration of Principle #1

**메타데이터:**
- ID: 151
- 레벨: 2
- 페이지: 363-364
- 페이지 수: 2
- 부모 ID: 149
- 텍스트 길이: 2984 문자

---

on of Principle #1
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