# 9.4 Introduction

**메타데이터:**
- ID: 89
- 레벨: 3
- 페이지: 216-217
- 페이지 수: 2
- 부모 ID: 88
- 텍스트 길이: 6775 문자

---

=== Page 215 ===
9.3 Persistent data structures libraries 187
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
}
});
Theo Do you mean that the catalog value in libraryData map is itself an immutable
map?
Joe Yes, and the same for booksByIsbn, authorIds, and so forth.
Theo Cool! So how do I access a field inside an immutable map?
Joe As I told you, Immutable.js provides its own API for data access. For instance,
in order to access a field inside an immutable map, you use Immutable.get()
or Immutable.getIn() like the following.
Listing9.10 Accessing a field and a nested field in an immutable map
Immutable.get(libraryData, "catalog");
Immutable.getIn(libraryData,
["catalog", "booksByIsbn", "978-1779501127", "title"]);
// → "Watchmen"
Theo How do I make a modification to a map?
Joe Similar to what we did with Lodash FP, you use an Immutable.set() or
Immutable.setIn() map to create a new version of the map where a field is
modified. Here’s how.
Listing9.11 Creating a new version of a map where a field is modified
Immutable.setIn(libraryData,
["catalog", "booksByIsbn",
"978-1779501127", "publicationYear"],
1988);
Theo What happens when I try to access a field in the map using JavaScript’s dot or
bracket notation?
Joe You access the internal representation of the map instead of accessing a map
field.
Theo Does that mean that we can’t pass data from Immutable.js to Lodash for data
manipulation?
Joe Yes, but it’s quite easy to convert any immutable collection into a native Java-
Script object back and forth.
Theo How?
Joe Immutable.js provides a toJS() method to convert an arbitrary deeply nested
immutable collection into a JavaScript object.

=== Page 216 ===
188 CHAPTER 9 Persistent data structures
Theo But if I have a huge collection, it could take lots of time to convert it, right?
Joe True. We need a better solution. Hopefully, Immutable.js provides its own set
of data manipulation functions like map(), filter(), and reduce().
Theo What if I need more data manipulation like Lodash’s _.groupBy()?
Joe You could write your own data manipulation functions that work with the
Immutable.js collections or use a library like mudash, which provides a port of
Lodash to Immutable.js.
 NOTE You can access the mudash library at https://github.com/brianneisler/mudash.
Theo What would you advise?
Joe A cup of coffee, then I’ll show you how to port functions from Lodash to
Immutable.js and how to adapt the code from your Library Management System.
You can decide on whichever approach works best for your current project.
9.4 Persistent data structures in action
Joe Let’s start with our search query. Can you look at the current code and tell me
the Lodash functions that we used to implement the search query?
Theo Including the code for the unit tests?
Joe Of course!
 NOTE See chapter 6 for the unit test of the search query.
9.4.1 Writing queries with persistent data structures
Theo The Lodash functions we used were get, map, filter, and isEqual.
Joe Here’s the port of those four functions from Lodash to Immutable.js.
Listing9.12 Porting some functions from Lodash to Immutable.js
Immutable.map = function(coll, f) {
return coll.map(f);
};
Immutable.filter = function(coll, f) {
if(Immutable.isMap(coll)) {
return coll.valueSeq().filter(f);
}
return coll.filter(f);
};
Immutable.isEqual = Immutable.is;
Theo The code seems quite simple. But can you explain it to me, function by function?
Joe Sure. Let’s start with get. For accessing a field in a map, Immutable.js provides
two functions: get for direct fields and getIn for nested fields. It’s different
from Lodash, where _.get works both on direct and nested fields.

=== Page 217 ===
9.4 Persistent data structures in action 189
Theo What about map?
Joe Immutable.js provides its own map function. The only difference is that it is a
method of the collection, but it is something that we can easily adapt.
Theo What about filter? How would you make it work both for arrays and maps
like Lodash’s filter?
Joe Immutable.js provides a valueSeq method that returns the values of a map.
Theo Cool. And what about isEqual to compare two collections?
Joe That’s easy. Immutable.js provides a function named is that works exactly as
isEqual.
Theo So far, so good. What do I need to do now to make the code of the search
query work with Immutable.js?
Joe You simply replace each occurrence of an _ with Immutable; _.map becomes
Immutable.map, _.filter becomes Immutable.filter, and _.isEqual
becomes Immutable.isEqual.
Theo I can’t believe it’s so easy!
Joe Try it yourself; you’ll see. Sometimes, it’s a bit more cumbersome because
you need to convert the JavaScript objects to Immutable.js objects using
Immutable.fromJS.
Theo copies and pastes the snippets for the code and the unit tests of the search query.
Then, he uses his IDE to replace the _ with Immutable. When Theo executes the tests and
they pass, he is surprised but satisfied. Joe smiles.
Listing9.13 Implementing book search with persistent data structures
class Catalog {
static authorNames(catalogData, authorIds) {
return Immutable.map(authorIds, function(authorId) {
return Immutable.getIn(
catalogData,
["authorsById", authorId, "name"]);
});
}
static bookInfo(catalogData, book) {
var bookInfo = Immutable.Map({
"title": Immutable.get(book, "title"),
"isbn": Immutable.get(book, "isbn"),
"authorNames": Catalog.authorNames(
catalogData,
Immutable.get(book, "authorIds"))
});
return bookInfo;
}
static searchBooksByTitle(catalogData, query) {
var allBooks = Immutable.get(catalogData, "booksByIsbn");
var queryLowerCased = query.toLowerCase();
var matchingBooks = Immutable.filter(allBooks, function(book) {

=== Page 218 ===
190 CHAPTER 9 Persistent data structures
return Immutable.get(book, "title").
toLowerCase().
includes(queryLowerCased);
});
var bookInfos = Immutable.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
}
}
Listing9.14 Testing book search with persistent data structures
var catalogData = Immutable.fromJS({
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore",
"dave-gibbons"]
}
},
"authorsById": {
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
});
var bookInfo = Immutable.fromJS({
"isbn": "978-1779501127",
"title": "Watchmen",
"authorNames": ["Alan Moore",
"Dave Gibbons"]
});
Immutable.isEqual(
Catalog.searchBooksByTitle(catalogData, "Watchmen"),
Immutable.fromJS([bookInfo]));
// → true
Immutable.isEqual(
Catalog.searchBooksByTitle(catalogData, "Batman"),
Immutable.fromJS([]));
// → true