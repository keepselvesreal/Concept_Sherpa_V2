# A.2.1 Illustration of Principle #2

**메타데이터:**
- ID: 157
- 레벨: 2
- 페이지: 373-373
- 페이지 수: 1
- 부모 ID: 155
- 텍스트 길이: 1688 문자

---

on of Principle #2
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