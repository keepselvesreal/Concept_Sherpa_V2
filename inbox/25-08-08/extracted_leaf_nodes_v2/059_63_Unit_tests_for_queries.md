# 6.3 Unit tests for queries

**메타데이터:**
- ID: 59
- 레벨: 2
- 페이지: 149-153
- 페이지 수: 5
- 부모 ID: 51
- 텍스트 길이: 8549 문자

---

or queries 121
Table 6.2 The correlation between the depth of a function in the tree of function calls and the
quality and quantity of the test cases
Depth in the tree Complexity of the data Number of test cases
Lower Higher Lower
Higher Lower Higher
6.3 Unit tests for queries
In the previous section, we saw how to write unit tests for utility functions like Catalog
.bookInfo and Catalog.authorNames. Now, we are going to see how to write unit tests
for the nodes of a query tree of function calls that are close to the root of the tree.
Joe Theo, how would you write a unit test for the code of the entry point of the
search query?
To recall the particulars, Theo checks the code for Library.searchBooksByTitleJSON.
Although Joe was right about today’s topic being easy enough to enjoy the ambience of a
coffee shop, he has been doing quite a lot of coding this morning.
Listing6.12 The code of Library.searchBooksByTitleJSON
Library.searchBooksByTitleJSON = function (libraryData, query) {
var catalogData = _.get(libraryData, "catalog");
var results = Catalog.searchBooksByTitle(catalogData, query);
var resultsJSON = JSON.stringify(results);
return resultsJSON;
};
He then takes a moment to think about how he’d write a unit test for that code. After
another Aha! moment, now he’s got it.
Theo The inputs of Library.searchBooksByTitleJSON are library data and a
query string, and the output is a JSON string (see figure 6.4). So, I would cre-
ate a library data record with a single book and write tests with query strings
that match the name of the book and ones that don’t match.
libraryData query
Library.searchBooksByTitleJSON()
Figure 6.4 The input and output of
resultsJSON Library.searchBooksByTitleJSON
Joe What about the expected results of the test cases?

122 CHAPTER 6 Unit tests
Theo In cases where the query string matches, the expected result is a JSON string
with the book info. In cases where the query string doesn’t match, the
expected result is a JSON string with an empty array.
Joe Hmm...
Theo What?
Joe I don’t like your answer.
Theo Why?
Joe Because your test case relies on a string comparison instead of a data comparison.
Theo What difference does it make? After all, the strings I’m comparing come from
the serialization of data.
Joe It’s inherently much more complex to compare JSON strings than it is to com-
pare data. For example, two different strings might be the serialization of the
same piece of data.
Theo Really? How?
Joe Take a look at these two strings. They are the serialization of the same data.
They’re different strings because the fields appear in a different order, but in
fact, they serialize the same data!
Joe turns his laptop to Theo. As Theo looks at the code, he realizes that, once again, Joe
iscorrect.
Listing6.13 Two different strings that serialize the same data
var stringA = "{\"title\":\"Watchmen\",\"publicationYear\":1987}";
var stringB = "{\"publicationYear\":1987,\"title\":\"Watchmen\"}";
TIP Avoid using a string comparison in unit tests for functions that deal with data.
Theo I see.... Well, what can I do instead?
Joe Instead of comparing the output of Library.searchBooksByTitleJSON with
a string, you could deserialize the output and compare it to the expected data.
Theo What do you mean by deserialize a string?
Joe Deserializing a string s, for example, means to generate a piece of data whose
serialization is s.
Theo Is there a Lodash function for string deserialization?
Joe Actually, there is a native JavaScript function for string deserialization; it’s
called JSON.parse.
Joe retrieves his laptop and shows Theo an example of string deserialization. The code
illustrates a common usage of JSON.parse.
Listing6.14 Example of string deserialization
var myString = "{\"publicationYear\":1987,\"title\":\"Watchmen\"}";
var myData = JSON.parse(myString);

6.3 Unit tests for queries 123
_.get(myData, "title");
// → "Watchmen"
Theo Cool! Let me try writing a unit test for Library.searchBooksByTitleJSON
using JSON.parse.
It doesn’t take Theo too much time to come up with a piece of code. Using his laptop, he
inputs the unit test.
Listing6.15 Unit test for Library.searchBooksByTitleJSON
var libraryData = {
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
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
}
};
var bookInfo = {
"isbn": "978-1779501127",
"title": "Watchmen",
"authorNames": ["Alan Moore",
"Dave Gibbons"]
};
_.isEqual(JSON.parse(Library.searchBooksByTitleJSON(libraryData,
"Watchmen")),
[bookInfo]);
_.isEqual(JSON.parse(Library.searchBooksByTitleJSON(libraryData,
"Batman")),
[]);
Joe Well done! I think you’re ready to move on to the last piece of the puzzle and
write the unit test for Catalog.searchBooksByTitle.

124 CHAPTER 6 Unit tests
Because Theo and Joe have been discussing unit tests for quite some time, he asks Joe if he
would like another espresso. They call the waiter and order, then Theo looks again at the
code for Catalog.searchBooksByTitle.
Listing6.16 The code of Catalog.searchBooksByTitle
Catalog.searchBooksByTitle = function(catalogData, query) {
var allBooks = _.get(catalogData, "booksByIsbn");
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title").includes(query);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
};
Writing the unit test for Catalog.searchBooksByTitle is a more pleasant experience for
Theo than writing the unit test for Library.searchBooksByTitleJSON. He appreciates
this for two reasons:
 It’s not necessary to deserialize the output because the function returns data.
 It’s not necessary to wrap the catalog data in a library data map.
Listing6.17 Unit test for Catalog.searchBooksByTitle
var catalogData = {
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
};
var bookInfo = {
"isbn": "978-1779501127",
"title": "Watchmen",
"authorNames": ["Alan Moore",
"Dave Gibbons"]
};

6.3 Unit tests for queries 125
_.isEqual(Catalog.searchBooksByTitle(catalogData, "Watchmen"), [bookInfo]);
_.isEqual(Catalog.searchBooksByTitle(catalogData, "Batman"), []);
Joe That’s a good start!
Theo I thought I was done. What did I miss?
Joe You forgot to test cases where the query string is all lowercase.
Theo You’re right! Let me quickly add one more test case.
In less than a minute, Theo creates an additional test case and shows it to Joe. What a dis-
appointment when Theo discovers that the test case with "watchmen" in lowercase fails!
Listing6.18 Additional test case for Catalog.searchBooksByTitle
_.isEqual(Catalog.searchBooksByTitle(catalogData, "watchmen"),
[bookInfo]);
Joe Don’t be too upset, my friend. After all, the purpose of unit tests is to find bugs
in the code so that you can fix them. Can you fix the code of Catalog-
Data.searchBooksByTitle?
Theo Sure. All I need to do is to lowercase both the query string and the book title
before comparing them. I’d probably do something like this.
Listing6.19 Fixed code of Catalog.searchBooksByTitle
Catalog.searchBooksByTitle = function(catalogData, query) {
var allBooks = _.get(catalogData, "booksByIsbn");
var queryLowerCased = query.toLowerCase();
Converts the query
var matchingBooks = _.filter(allBooks, function(book) {
to lowercase
return _.get(book, "title")
.toLowerCase()
Converts the book
.includes(queryLowerCased);
title to lowercase
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
};
After fixing the code of Catalog.searchBooksByTitle, Theo runs all the test cases
again. This time, all of them pass—what a relief!
Listing6.20 Additional test case for Catalog.searchBooksByTitle
_.isEqual(Catalog.searchBooksByTitle(catalogData, "watchmen"),
[bookInfo]);
Joe It’s such good feeling when all the test cases pass.
Theo Sure is.
Joe I think we’ve written unit tests for all the search query code, so now we’re ready
to write unit tests for mutations. Thank goodness the waiter just brought our
coffee orders.

126 CHAPTER 6 Unit tests