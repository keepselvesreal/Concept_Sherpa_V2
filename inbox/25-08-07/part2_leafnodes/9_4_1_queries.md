# 9.4.1 Writing queries with persistent data structures

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

## 페이지 217

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

## 페이지 218

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

## 페이지 219

9.4 Persistent data structures in action 191