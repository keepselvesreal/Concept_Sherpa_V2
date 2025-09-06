# 9.3.2 Persistent data structures in JavaScript

Joe In a language like JavaScript, it’s a bit more cumbersome to integrate per-
sistent data structures.
Theo How so?
Joe Because JavaScript objects and arrays don’t expose any interface.
Theo Bummer.
Joe It’s not as terrible as it sounds because Immutable.js exposes its own set of
functions to manipulate its data structures.
Theo What do you mean?
Joe I’ll show you in a moment. But first, let me show you how to initiate Immutable.js
persistent data structures.
Theo OK!
Joe Immutable.js provides a handy function that recursively converts a native data
object to an immutable one. It’s called Immutable.fromJS().
Theo What do you mean by recursively?
Joe Consider the map that holds library data from our Library Management Sys-
tem: it has values that are themselves maps. Immutable.fromJS() converts the
nested maps into immutable maps.
Theo Could you show me some code?
Joe Absolutely. Take a look at this JavaScript code for library data.
Listing9.9 Conversion to immutable data
var libraryData = Immutable.fromJS({
"catalog": {
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

## 페이지 215

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

## 페이지 216

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