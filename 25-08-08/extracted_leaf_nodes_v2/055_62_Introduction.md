# 6.2 Introduction

**메타데이터:**
- ID: 55
- 레벨: 3
- 페이지: 140-141
- 페이지 수: 2
- 부모 ID: 54
- 텍스트 길이: 6973 문자

---

=== Page 139 ===
6.1 The simplicity of data-oriented test cases 111
office, Joe leads the discussion towards a very concrete topic—unit tests. Theo asks Joe for
an explanation.
Theo Are unit tests such a simple topic that we can tackle it here in a coffee shop?
Joe Unit tests in general, no. But unit tests for data-oriented code, yes!
Theo Why does that make a difference?
Joe The vast majority of the code base of a data-oriented system deals with data
manipulation.
Theo Yeah. I noticed that almost all the functions we wrote so far receive data and
return data.
TIP Most of the code in a data-oriented system deals with data manipulation.
Joe Writing a test case for functions that deal with data is only about generating
data input and expected output, and comparing the output of the function
with the expected output.
The steps of a test case
1 Generate data input: dataIn
2 Generate expected output: dataOut
3 Compare the output of the function with the expected output: f(dataIn) and
dataOut
Theo That’s it?
Joe Yes. As you’ll see in a moment, in DOP, there’s usually no need for mock
functions.
Theo I understand how to compare primitive values like strings or numbers, but I’m
not sure how I would compare data collections like maps.
Joe You compare field by field.
Theo Recursively?
Joe Yes!
Theo Oh no! I’m not able to write any recursive code in a coffee shop. I need the
calm of my office for that kind of stuff.
Joe Don’t worry. In DOP, data is represented in a generic way. There is a generic
function in Lodash called _.isEqual for recursive comparison of data collec-
tions. It works with both maps and arrays.
Joe opens his laptop. He is able to convince Theo by executing a few code snippets with
_.isEqual to compare an equal data collection with a non-equal one.
Listing6.1 Comparing an equal data collection recursively
_.isEqual({
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]

=== Page 140 ===
112 CHAPTER 6 Unit tests
}, {
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
});
// → true
Listing6.2 Comparing a non-equal data collection recursively
_.isEqual({
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
}, {
"name": "Alan Moore",
"bookIsbns": ["bad-isbn"]
});
// → false
Theo Nice!
Joe Most of the test cases in DOP follow this pattern.
Theo decides he wants to try this out. He fires up his laptop and types a few lines of
pseudocode.
Listing6.3 The general pattern of a data-oriented test case
var dataIn = {
// input
};
var dataOut = {
// expected output
};
_.isEqual(f(dataIn), dataOut);
TIP It’s straightforward to write unit tests for code that deals with data manipulation.
Theo Indeed, this looks like something we can tackle in a coffee shop!
6.2 Unit tests for data manipulation code
A waiter in an elegant bow tie brings Theo his croissant and Joe his pain au chocolat. The
two friends momentarily interrupt their discussion to savor their French pastries. When
they’re done, they ask the waiter to bring them their drinks. Meanwhile, they resume the
discussion.
Joe Do you remember the code flow of the implementation of the search query?
Theo Let me look again at the code that implements the search query.
Theo brings up the implementation of the search query on his laptop. Noticing that Joe is
chewing on his nails again, he quickly checks out the code.

=== Page 141 ===
6.2 Unit tests for data manipulation code 113
Listing6.4 The code involved in the implementation of the search query
class Catalog {
static authorNames(catalogData, authorIds) {
return _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
}
static bookInfo(catalogData, book) {
var bookInfo = {
"title": _.get(book, "title"),
"isbn": _.get(book, "isbn"),
"authorNames": Catalog.authorNames(catalogData,
_.get(book, "authorIds"))
};
return bookInfo;
}
static searchBooksByTitle(catalogData, query) {
var allBooks = _.get(catalogData, "booksByIsbn");
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title").includes(query);
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
return resultsJSON;
}
}
6.2.1 The tree of function calls
The waiter brings Theo his café au lait and Joe his tight espresso. They continue their dis-
cussion while enjoying their coffees.
Joe Before writing a unit test for a code flow, I find it useful to visualize the tree of
function calls of the code flow.
Theo What do you mean by a tree of function calls?
Joe Here, I’ll draw the tree of function calls for the Library.searchBooksBy-
TitleJSON code flow.
Joe puts down his espresso and takes a napkin from the dispenser. He carefully places it
flat on the table and starts to draw. When he is done, he shows the illustration to Theo (see
figure 6.1).

=== Page 142 ===
114 CHAPTER 6 Unit tests
Library.searchBooksByTitleJSON
_.get JSON.stringify Catalog.searchBooksByTitle
_.get _.map _.filter Catalog.bookInfo
_.get Catalog.authorNames
_.get _.map
Figure 6.1 The tree of function calls for the search query code flow
Theo Nice! Can you teach me how to draw a tree of function calls like that?
Joe Sure. The root of the tree is the name of the function for which you draw the
tree, in our case, Library.searchBooksByTitleJSON. The children of a
node in the tree are the names of the functions called by the function. For exam-
ple, if you look again at the code for Library.searchBooksByTitleJSON (list-
ing 6.4), you’ll see that it calls Catalog.searchBooksByTitle, _.get, and
JSON.stringify.
Theo How long would I continue to recursively expand the tree?
Joe You continue until you reach a function that doesn’t belong to the code base
of your application. Those nodes are the leaves of our tree; for example, the
functions from Lodash: _.get, _.map, and so forth.
Theo What if the code of a function doesn’t call any other functions?
Joe A function that doesn’t call any other function would be a leaf in the tree.
Theo What about functions that are called inside anonymous functions like Catalog
.bookInfo?
Joe Catalog.bookInfo appears in the code of Catalog.searchBooksByTitle.
Therefore, it is considered to be a child node of Catalog.searchBooksBy-
Title. The fact that it is nested inside an anonymous function is not relevant
in the context of the tree of function calls.
 NOTE A tree of function calls for a function f is a tree where the root is f, and the
children of a node g in the tree are the functions called by g. The leaves of the tree are
functions that are not part of the code base of the application. These are functions
that don’t call any other functions.
Theo It’s very cool to visualize my code as a tree, but I don’t see how it relates to
unittests.