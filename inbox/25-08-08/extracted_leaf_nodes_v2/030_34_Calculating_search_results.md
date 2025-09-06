# 3.4 Calculating search results

**메타데이터:**
- ID: 30
- 레벨: 2
- 페이지: 86-92
- 페이지 수: 7
- 부모 ID: 25
- 텍스트 길이: 11211 문자

---

search results
Theo Interesting. I’m starting to feel the power of expression of DOP!
Joe Wait, that’s just the beginning. Let me show you how simple it is to write code
that retrieves book information and displays it in search results. Can you tell
me exactly what information has to appear in the search results?
Theo Searching for book information should return isbn, title, and author-
Names.
Joe And what would a BookInfo record look like for Watchmen?
Theo quickly enters the code on his laptop. He then shows it to Joe.
Listing3.10 A BookInfo record for Watchmen in the context of search result
{
"title": "Watchmen",
"isbn": "978-1779501127",
"authorNames": [
"Alan Moore",
"Dave Gibbons",
]
}

3.4 Calculating search results 59
Joe Now I’ll show you step by step how to write a function that returns search
results matching a title in JSON format. I’ll use generic data manipulation
functions from Lodash.
Theo I’m ready!
Joe Let’s start with an authorNames function that calculates the author names of a
Book record by looking at the authorsById index. Could you tell me what’s
the information path for the name of an author whose ID is authorId?
Theo It’s ["authorsById", authorId, "name"].
Joe Now, let me show you how to retrieve the name of several authors using _.map.
Joe types the code to map the author IDs to the author names. Theo nonchalantly peeks
over Joe’s shoulder.
Listing3.11 Mapping author IDs to author names
_.map(["alan-moore", "dave-gibbons"],
function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
// → [ "Alan Moore", "Dave Gibbons"]
Theo What’s this _.map function? It smells like functional programming! You said I
wouldn’t have to learn FP to implement DOP!
Joe No need to learn functional programming in order to use _.map, which is a
function that transforms the values of a collection. You can implement it with
a simple for loop.
Theo spends a couple of minutes in front of his computer figuring out how to implement
_.map. Now he’s got it!
Listing3.12 Custom implementation of map
function map(coll, f) {
var res = [];
for(var i = 0; i < coll.length; i++) {
We could use
res[i] = f(coll[i]);
forEach instead
}
of a for loop.
return res;
}
After testing Theo’s implementation of map, Joe shows Theo the test. Joe again compli-
ments Theo.
Listing3.13 Testing the custom implementation of map
map(["alan-moore", "dave-gibbons"],
function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
// → [ "Alan Moore", "Dave Gibbons"]

60 CHAPTER 3 Basic data manipulation
Joe Well done!
Theo You were right! It wasn’t hard.
Joe Now, let’s implement authorNames using _.map.
It takes a few minutes for Theo to come up with the implementation of authorNames.
When he’s finished, he turns his laptop to Joe.
Listing3.14 Calculating the author names of a book
function authorNames(catalogData, book) {
var authorIds = _.get(book, "authorIds");
var names = _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
return names;
}
Joe We also need a bookInfo function that converts a Book record into a Book-
Info record. Let me show you the code for that.
Listing3.15 Converting a Book record into a BookInfo record
function bookInfo(catalogData, book) {
var bookInfo = {
"title": _.get(book, "title"),
"isbn": _.get(book, "isbn"),
"authorNames": authorNames(catalogData, book)
};
There’s no need to create
return bookInfo;
a class for bookInfo.
}
Theo Looking at the code, I see that a BookInfo record has three fields: title,
isbn, and authorNames. Is there a way to get this information without looking
at the code?
Joe You can either add it to the data entity diagram or write it in the documenta-
tion of the bookInfo function, or both.
Theo I have to get used to the idea that in DOP, the record field information is not
part of the program.
Joe Indeed, it’s not part of the program, but it gives us a lot of flexibility.
Theo Is there any way for me to have my cake and eat it too?
Joe Yes, and someday I’ll show you how to make record field information part of a
DOP program (see chapters 7 and 12).
Theo Sounds intriguing!
Joe Now that we have all the pieces in place, we can write our searchBooksBy-
Title function, which returns the book information about the books that
match the query. First, we find the Book records that match the query with
_.filter and then we transform each Book record into a BookInfo record
with _.map and bookInfo.

3.4 Calculating search results 61
Listing3.16 Searching books that match a query
function searchBooksByTitle(catalogData, query) {
var allBooks = _.values(_.get(catalogData, "booksByIsbn"));
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title").includes(query);
The includes JavaScript
});
function checks whether
a string includes a string
var bookInfos = _.map(matchingBooks, function(book) { as a substring.
return bookInfo(catalogData, book);
});
return bookInfos;
}
Theo You’re using Lodash functions without any explanation again!
Joe Sorry about that. I am so used to basic data manipulation functions that I con-
sider them as part of the language. What functions are new to you?
Theo _.values and _.filter
Joe Well, _.values returns a collection made of the values of a map, and _.filter
returns a collection made of the values that satisfy a predicate.
Theo _.values seems trivial. Let me try to implement _.filter.
The implementation of _.filter takes a bit more time. Eventually, Theo manages to get
it right, then he is able to test it.
Listing3.17 Custom implementation of filter
function filter(coll, f) {
var res = [];
for(var i = 0; i < coll.length; i++) {
We could use
if(f(coll[i])) {
forEach instead
res.push(coll[i]);
of a for loop.
}
}
return res;
}
Listing3.18 Testing the custom implementation of filter
filter(["Watchmen", "Batman"], function (title) {
return title.includes("Watch");
});
// → ["Watchmen"]
Theo To me, it’s a bit weird that to access the title of a book record, I need to write
_.get(book, "title"). I’d expect it to be book.title in dot notation or
book["title"] in bracket notation.
Joe Remember that book is a record that’s not represented as an object. It’s a map.
Indeed, in JavaScript, you can write _.get(book, "title"), book.title, or
book["title"]. But I prefer to use Lodash’s _.get function. In some lan-
guages, the dot and the bracket notations might not work on maps.

62 CHAPTER 3 Basic data manipulation
Theo Being language-agnostic has a price!
Joe Right, would you like to test searchBooksByTitle?
Theo Absolutely! Let me call searchBooksByTitle to search the books whose title
contain the string Watch.
Listing3.19 Testing searchBooksByTitle
searchBooksByTitle(catalogData, "Wat");
//[
// {
// "authorNames": [
// "Alan Moore",
// "Dave Gibbons"
// ],
// "isbn": "978-1779501127",
// "title": "Watchmen"
// }
//]
Theo It seems to work! Are we done with the search implementation?
Joe Almost. The searchBooksByTitle function we wrote is going to be part of the
Catalog module, and it returns a collection of records. We have to write a
function that’s part of the Library module, and that returns a JSON string.
Theo You told me earlier that JSON serialization was straightforward in DOP.
Joe Correct. The code for searchBooksByTitleJSON retrieves the Catalog record,
passes it to searchBooksByTitle, and converts the results to JSON with
JSON.stringify. That’s part of JavaScript. Here, let me show you.
Listing3.20 Implementation of searching books in a library as JSON
function searchBooksByTitleJSON(libraryData, query) {
var results = searchBooksByTitle(_.get(libraryData, "catalog"), query);
var resultsJSON = JSON.stringify(results);
return resultsJSON;
}
Joe In order to test our code, we need to create a Library record that contains our
Catalog record. Could you do that for me, please?
Theo Should the Library record contain all the Library fields (name, address,
and UserManagement)?
Joe That’s not necessary. For now, we only need the catalog field, then the test
for searching books.
Listing3.21 A Library record
var libraryData = {
"catalog": {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",

3.4 Calculating search results 63
"publicationYear": 1987,
"authorIds": ["alan-moore",
"dave-gibbons"],
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
},
{
"id": "book-item-2",
"libId": "nyc-central-lib",
"isLent": false
}
]
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
}
};
Listing3.22 Test for searching books in a library as JSON
searchBooksByTitleJSON(libraryData, "Wat");
Theo How are we going to combine the four functions that we’ve written so far?
Joe The functions authorNames, bookInfo, and searchBooksByTitle go into
the Catalog module, and searchBooksByTitleJSON goes into the Library
module.
Theo looks at the resulting code of the two modules, Library and Catalog. He’s quite
amazed by its conciseness.
Listing3.23 Calculating search results for Library and Catalog
class Catalog {
static authorNames(catalogData, book) {
var authorIds = _.get(book, "authorIds");
var names = _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
return names;
}

64 CHAPTER 3 Basic data manipulation
static bookInfo(catalogData, book) {
var bookInfo = {
"title": _.get(book, "title"),
"isbn": _.get(book, "isbn"),
"authorNames": Catalog.authorNames(catalogData, book)
};
There’s no need
return bookInfo;
to create a class
}
for bookInfo.
static searchBooksByTitle(catalogData, query) {
var allBooks = _.get(catalogData, "booksByIsbn");
When _.filter is
var matchingBooks = _.filter(allBooks,
passed a map, it
function(book) {
goes over the values
return _.get(book, "title").includes(query);
of the map.
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
}
}
class Library {
static searchBooksByTitleJSON(libraryData, query) {
var catalogData = _.get(libraryData, "catalog");
var results = Catalog.searchBooksByTitle(catalogData, query);
var resultsJSON = JSON.stringify(results);
Converts data
return resultsJSON;
to JSON (part
}
of JavaScript)
}
After testing the final code in listing 3.24, Theo looks again at the source code from list-
ing 3.23. After a few seconds, he feels like he’s having another Aha! moment.
Listing3.24 Search results in JSON
Library.searchBooksByTitleJSON(libraryData, "Watchmen");
// → "[{\"title\":\"Watchmen\",\"isbn\":\"978-1779501127\",
// → \"authorNames\":[\"Alan Moore\",\"Dave Gibbons\"]}]"
Theo The important thing is not that the code is concise, but that the code contains
no abstractions. It’s just data manipulation!
Joe responds with a smile that says, “You got it, my friend!”
Joe It reminds me of what my first meditation teacher told me 10 years ago:
meditation guides the mind to grasp the reality as it is without the abstractions
created by our thoughts.
TIP In DOP, many parts of our code base tend to be just about data manipulation
with no abstractions.