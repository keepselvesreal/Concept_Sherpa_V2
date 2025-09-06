# 6 Unit tests

**Level:** 1
**페이지 범위:** 138 - 164
**총 페이지 수:** 27
**ID:** 51

---

=== 페이지 138 ===
Unit tests
Programming at a coffee shop
This chapter covers
 Generation of the minimal data input for a
test case
 Comparison of the output of a function with
the expected output
 Guidance about the quality and the quantity
of the test cases
In a data-oriented system, our code deals mainly with data manipulation: most of
our functions receive data and return data. As a consequence, it’s quite easy to
write unit tests to check whether our code behaves as expected. A unit test is made
of test cases that generate data input and compare the data output of the function
with the expected data output. In this chapter, we write unit tests for the queries
and mutations that we wrote in the previous chapters.
6.1 The simplicity of data-oriented test cases
Theo and Joe are seated around a large wooden table in a corner of “La vie est belle,” a
nice little French coffee shop, located near the Golden Gate Bridge. Theo orders a café
au lait with a croissant, and Joe orders a tight espresso with a pain au chocolat. Instead
of the usual general discussions about programming and life when they’re out of the
110

=== 페이지 139 ===
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

=== 페이지 140 ===
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

=== 페이지 141 ===
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

=== 페이지 142 ===
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

=== 페이지 143 ===
6.2 Unit tests for data manipulation code 115
Joe The tree of function calls guides us about the quality and the quantity of test
cases we should write.
Theo How?
Joe You’ll see in a moment.
6.2.2 Unit tests for functions down the tree
Joe Let’s start from the function that appears in the deepest node in our tree:
Catalog.authorNames. Take a look at the code for Catalog.authorNames
and tell me what are the input and the output of Catalog.authorNames.
Joe turns his laptop so Theo can a closer look at the code. Theo takes a sip of his café au
lait as he looks over what’s on Joe’s laptop.
Listing6.5 The code of Catalog.authorNames
Catalog.authorNames = function (catalogData, authorIds) {
return _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
};
Theo The input of Catalog.authorNames is catalogData and authorIds. The
output is authorNames.
Joe Would you do me a favor and express it visually?
Theo Sure.
It’s Theo’s turn to grab a napkin. He draws a small rectangle with two inward arrows and
one outward arrow as in figure 6.2.
catalogData authorIds
Catalog.authorNames()
Figure 6.2 Visualization of the input
authorNames and output of Catalog.authorNames
Joe Excellent! Now, how many combinations of input would you include in the
unit test for Catalog.authorNames?
Theo Let me see.
Theo reaches for another napkin. This time he creates a table to gather his thoughts
(table 6.1).

=== 페이지 144 ===
116 CHAPTER 6 Unit tests
Table 6.1 The table of test cases for Catalog.authorNames
catalogData authorIds authorNames
Catalog with two authors Empty array Empty array
Catalog with two authors Array with one author ID Array with one author name
Catalog with two authors Array with two author IDs Array with two author names
Theo To begin with, I would have a catalogData with two author IDs and call
Catalog.authorNames with three arguments: an empty array, an array with a
single author ID, and an array with two author IDs.
Joe How would you generate the catalogData?
Theo Exactly as we generated it before.
Turning to his laptop, Theo writes the code for catalogData. He shows it to Joe.
Listing6.6 A complete catalogData map
var catalogData = {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore", "dave-gibbons"],
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
};

=== 페이지 145 ===
6.2 Unit tests for data manipulation code 117
Joe You could use your big catalogData map for the unit test, but you could also
use a smaller map in the context of Catalog.authorNames. You can get rid of
the booksByIsbn field of the catalogData and the bookIsbns fields of the
authors.
Joe deletes a few lines from catalogData and gets a much smaller map. He shows the revi-
sion to Theo.
Listing6.7 A minimal version of catalogData
var catalogData = {
"authorsById": {
"alan-moore": {
"name": "Alan Moore"
},
"dave-gibbons": {
"name": "Dave Gibbons"
}
}
};
Theo Wait a minute! This catalogData is not valid.
Joe In DOP, data validity depends on the context. In the context of Library
.searchBooksByTitleJSON and Catalog.searchBooksByTitle, the mini-
mal version of catalogData is indeed not valid. However, in the context of
Catalog.bookInfo and Catalog.authorNames, it is perfectly valid. The reason
is that those two functions access only the authorsById field of catalogData.
TIP The validity of the data depends on the context.
Theo Why is it better to use a minimal version of the data in a test case?
Joe For a very simple reason—the smaller the data, the easier it is to manipulate.
TIP The smaller the data, the easier it is to manipulate.
Theo I’ll appreciate that when I write the unit tests!
Joe Definitely! One last thing before we start coding: how would you check that the
output of Catalog.authorNames is as expected?
Theo I would check that the value returned by Catalog.authorNames is an array
with the expected author names.
Joe How would you handle the array comparison?
Theo Let me think. I want to compare by value, not by reference. I guess I’ll have to
check that the array is of the expected size and then check member by mem-
ber, recursively.
Joe That’s too much of a mental burden when you’re in a coffee shop. As I showed
you earlier (see listing 6.1), we can recursively compare two data collections by
value with _.isEqual from Lodash.

=== 페이지 146 ===
118 CHAPTER 6 Unit tests
TIP We can compare the output and the expected output of our functions with
_.isEqual.
Theo Sounds good! Let me write the test cases.
Theo starts typing on his laptop. After a few minutes, he has some test cases for Catalog
.authorNames, each made from a function call to Catalog.authorNames wrapped in
_.isEqual.
Listing6.8 Unit test for Catalog.authorNames
var catalogData = {
"authorsById": {
"alan-moore": {
"name": "Alan Moore"
},
"dave-gibbons": {
"name": "Dave Gibbons"
}
}
};
_.isEqual(Catalog.authorNames(catalogData, []), []);
_.isEqual(Catalog.authorNames(
catalogData,
["alan-moore"]),
["Alan Moore"]);
_.isEqual(Catalog.authorNames(catalogData, ["alan-moore", "dave-gibbons"]),
["Alan Moore", "Dave Gibbons"]);
Joe Well done! Can you think of more test cases?
Theo Yes. There are test cases where the author ID doesn’t appear in the catalog
data, and test cases with empty catalog data. With minimal catalog data and
_.isEqual, it’s really easy to write lots of test cases!
Theo really enjoys this challenge. He creates a few more test cases to present to Joe.
Listing6.9 More test cases for Catalog.authorNames
_.isEqual(Catalog.authorNames({}, []), []);
_.isEqual(Catalog.authorNames({}, ["alan-moore"]), [undefined]);
_.isEqual(Catalog.authorNames(catalogData, ["alan-moore",
"albert-einstein"]), ["Alan Moore", undefined]);
_.isEqual(Catalog.authorNames(catalogData, []), []);
_.isEqual(Catalog.authorNames(catalogData, ["albert-einstein"]),
[undefined]);
Theo How do I run these unit tests?
Joe You use your preferred test framework.

=== 페이지 147 ===
6.2 Unit tests for data manipulation code 119
 NOTE We don’t deal here with test runners and test frameworks. We deal only with
the logic of the test cases.
6.2.3 Unit tests for nodes in the tree
Theo I’m curious to see what unit tests for an upper node in the tree of function calls
look like.
Joe Sure. Let’s write a unit test for Catalog.bookInfo. How many test cases would
you have for Catalog.bookInfo?
Listing6.10 The code of Catalog.bookInfo
Catalog.bookInfo = function (catalogData, book) {
return {
"title": _.get(book, "title"),
"isbn": _.get(book, "isbn"),
"authorNames": Catalog.authorNames(catalogData,
_.get(book, "authorIds"))
};
};
Theo takes another look at the code for Catalog.bookInfo on his laptop. Then, reaching
for another napkin, he draws a diagram of its input and output (see figure 6.3).
catalogData book
Catalog.bookInfo()
Figure 6.3 Visualization of the input
bookInfo and output of Catalog.bookInfo
Theo I would have a similar number of test cases for Catalog.authorNames: a book
with a single author, with two authors, with existing authors, with non-existent
authors, with...
Joe Whoa! That’s not necessary. Given that we have already written unit tests for
Catalog.authorNames, we don’t need to check all the cases again. We simply
need to write a minimal test case to confirm that the code works.
TIP When we write a unit test for a function, we assume that the functions called by
this function are covered by unit tests and work as expected. It significantly reduces
the quantity of test cases in our unit tests.
Theo That makes sense.
Joe How would you write a minimal test case for Catalog.bookInfo?
Theo once again takes a look at the code for Catalog.bookInfo (see listing 6.10). Now he
can answer Joe’s question.

=== 페이지 148 ===
120 CHAPTER 6 Unit tests
Theo I would use the same catalog data as for Catalog.authorNames and a book
record. I’d test that the function behaves as expected by comparing its return
value with a book info record using _.isEqual. Here, let me show you.
It takes Theo a bit more time to write the unit test. The reason is that the input and the
output of Catalog.authorNames are both records. Dealing with a record is more complex
than dealing with an array of strings (as it was the case for Catalog.authorNames). Theo
appreciates the fact that _.isEqual saves him from writing code that compares the two
maps property by property. When he’s through, he shows the result to Joe and takes a nap-
kin to wipe his forehead.
Listing6.11 Unit test for Catalog.bookInfo
var catalogData = {
"authorsById": {
"alan-moore": {
"name": "Alan Moore"
},
"dave-gibbons": {
"name": "Dave Gibbons"
}
}
};
var book = {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore", "dave-gibbons"]
};
var expectedResult = {
"authorNames": ["Alan Moore", "Dave Gibbons"],
"isbn": "978-1779501127",
"title": "Watchmen",
};
var result = Catalog.bookInfo(catalogData, book);
_.isEqual(result, expectedResult);
Joe Perfect! Now, how would you compare the kind of unit tests for Catalog
.bookInfo with the unit tests for Catalog.authorNames?
Theo On one hand, there is only a single test case in the unit test for Catalog.book-
Info. On the other hand, the data involved in the test case is more complex
than the data involved in the test cases for Catalog.authorNames.
Joe Exactly! Functions that appear in a deep node in the tree of function calls tend
to require more test cases, but the data involved in the test cases is less complex.
TIP Functions that appear in a lower level in the tree of function calls tend to
involve less complex data than functions that appear in a higher level in the tree
(see table 6.2).

=== 페이지 149 ===
6.3 Unit tests for queries 121
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

=== 페이지 150 ===
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

=== 페이지 151 ===
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

=== 페이지 152 ===
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

=== 페이지 153 ===
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

=== 페이지 154 ===
126 CHAPTER 6 Unit tests
6.4 Unit tests for mutations
Joe Before writing unit tests for the add member mutation, let’s draw the tree of
function calls for System.addMember.
Theo I can do that.
Theo takes a look at the code for the functions involved in the add member mutation. He
notices the code is spread over three classes: System, Library, and UserManagement.
Listing6.21 The functions involved in the add member mutation
System.addMember = function(systemState, member) {
var previous = systemState.get();
var next = Library.addMember(previous, member);
systemState.commit(previous, next);
};
Library.addMember = function(library, member) {
var currentUserManagement = _.get(library, "userManagement");
var nextUserManagement = UserManagement.addMember(
currentUserManagement, member);
var nextLibrary = _.set(library, "userManagement", nextUserManagement);
return nextLibrary;
};
UserManagement.addMember = function(userManagement, member) {
var email = _.get(member, "email");
var infoPath = ["membersByEmail", email];
if(_.has(userManagement, infoPath)) {
throw "Member already exists.";
}
var nextUserManagement = _.set(userManagement,
infoPath,
member);
return nextUserManagement;
};
Theo grabs another napkin. Drawing the tree of function calls for System.addMember is
now quite easy (see figure 6.5).
System.addMember
SystemState.get SystemState.commit Library.addMember
_.get _.set UserManagement.addMember
_.has _.set
Figure 6.5 The tree of function calls for System.addMember

=== 페이지 155 ===
6.4 Unit tests for mutations 127
Joe Excellent! So which functions of the tree should be unit tested for the add
member mutation?
Theo I think the functions we need to test are System.addMember, SystemState
.get, SystemState.commit, Library.addMember, and UserManagement
.addMember. That right?
Joe You’re totally right. Let’s defer writing unit tests for functions that belong to
SystemState until later. Those are generic functions that should be tested
outside the context of a specific mutation. Let’s assume for now that we’ve
already written unit tests for the SystemState class. We’re left with three func-
tions: System.addMember, Library.addMember, and UserManagement.add-
Member.
Theo In what order should we write the unit tests, bottom up or top down?
Joe Let’s start where the real meat is—in UserManagement.addMember. The two
other functions are just wrappers.
Theo OK.
Joe Writing a unit test for the main function of a mutation requires more effort
than writing the test for a query. The reason is that a query returns a response
based on the system data, whereas a mutation computes a new state of the system
based on the current state of the system and some arguments (see figure 6.6).
SystemData Argument Argument SystemData
Mutation Query
NextSystemData ResponseData
Figure 6.6 The output of a mutation is more complex than
the output of a query.
TIP Writing a unit test for the main function of a mutation requires more effort than
for a query.
Theo It means that in the test cases of UserManagement.addMember, both the input
and the expected output are maps that describe the state of the system.
Joe Exactly. Let’s start with the simplest case, where the initial state of the system
is empty.
Theo You mean that userManagementData passed to UserManagement.addMember
is an empty map?
Joe Yes.
Once again, Theo places his hands over his laptop keyboard, thinks for a moment, and
begins typing. He reminds himself that the code needs to add a member to an empty user

=== 페이지 156 ===
128 CHAPTER 6 Unit tests
management map and to check that the resulting map is as expected. When he’s finished,
he shows his code to Joe.
Listing6.22 Test case for Catalog.addMember without members
var member = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var userManagementStateBefore = {};
var expectedUserManagementStateAfter = {
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
}
}
};
var result = UserManagement.addMember(userManagementStateBefore, member);
_.isEqual(result, expectedUserManagementStateAfter);
Joe Very nice! Keep going and write a test case when the initial state is not empty.
Theo knows this requires a few more lines of code but nothing complicated. When he fin-
ishes, he once again shows the code to Joe.
Listing6.23 Test case for Catalog.addMember with existing members
var jessie = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var franck = {
"email": "franck@gmail.com",
"password": "my-top-secret"
};
var userManagementStateBefore = {
"membersByEmail": {
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
};
var expectedUserManagementStateAfter = {
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",

=== 페이지 157 ===
6.4 Unit tests for mutations 129
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
};
var result = UserManagement.addMember(userManagementStateBefore, jessie);
_.isEqual(result, expectedUserManagementStateAfter);
Joe Awesome! Can you think of other test cases for UserManagement.addMember?
Theo No.
Joe What about cases where the mutation fails?
Theo Right! I always forget to think about negative test cases. I assume that relates to
the fact that I’m an optimistic person.
TIP Don’t forget to include negative test cases in your unit tests.
Joe Me too. The more I meditate, the more I’m able to focus on the positive side of
life. Anyway, how would you write a test case where the mutation fails?
Theo I would pass to UserManagement.addMember a member that already exists in
userManagementStateBefore.
Joe And how would you check that the code behaves as expected in case of a failure?
Theo Let me see. When a member already exists, UserManagement.addMember
throws an exception. Therefore, what I need to do in my test case is to wrap the
code in a try/catch block.
Joe Sounds good to me.
Once again, it doesn’t require too much of an effort for Theo to create a new test case.
When he’s finished, he eagerly turns his laptop to Joe.
Listing6.24 Test case for UserManagement.addMember if it’s expected to fail
var jessie = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var userManagementStateBefore = {
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
}
}
};

=== 페이지 158 ===
130 CHAPTER 6 Unit tests
var expectedException = "Member already exists.";
var exceptionInMutation;
try {
UserManagement.addMember(userManagementStateBefore, jessie);
} catch (e) {
exceptionInMutation = e;
}
_.isEqual(exceptionInMutation, expectedException);
Theo Now, I think I’m ready to move forward and write unit tests for Library.add-
Member and System.addMember.
Joe I agree with you. Please start with Library.addMember.
Theo Library.addMember is quite similar to UserManagement.addMember. So I
guess I’ll write similar test cases.
Joe In fact, that won’t be required. As I told you when we wrote unit tests for a
query, when you write a unit test for a function, you can assume that the func-
tions down the tree work as expected.
Theo Right. So I’ll just write the test case for existing members.
Joe Go for it!
Theo starts with a copy-and-paste of the code from the UserManagement.addMember test
case with the existing members in listing 6.23. After a few modifications, the unit test for
Library.addMember is ready.
Listing6.25 Unit test for Library.addMember
var jessie = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var franck = {
"email": "franck@gmail.com",
"password": "my-top-secret"
};
var libraryStateBefore = {
"userManagement": {
"membersByEmail": {
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
}
};
var expectedLibraryStateAfter = {
"userManagement": {
"membersByEmail": {

=== 페이지 159 ===
6.4 Unit tests for mutations 131
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
}
};
var result = Library.addMember(libraryStateBefore, jessie);
_.isEqual(result, expectedLibraryStateAfter);
Joe Beautiful! Now, we’re ready for the last piece. Write a unit test for System
.addMember. Before you start, could you please describe the input and the out-
put of System.addMember?
Theo takes another look at the code for System.addMember and hesitates; he’s a bit con-
fused. The function doesn’t seem to return anything!
Listing6.26 The code of System.addMember
System.addMember = function(systemState, member) {
var previous = systemState.get();
var next = Library.addMember(previous, member);
systemState.commit(previous, next);
};
Theo The input of System.addMember is a system state instance and a member. But,
I’m not sure what the output of System.addMember is.
Joe In fact, System.addMember doesn’t have any output. It belongs to this stateful
part of our code that doesn’t deal with data manipulation. Although DOP
allows us to reduce the size of the stateful part of our code, it still exists. Here is
how I visualize it.
Joe calls the waiter to see if he can get more napkins. With that problem resolved, he draws
the diagram in figure 6.7.
SystemData Member
Mutation Change system state
Figure 6.7 System.addMember
doesn’t return data—it changes the
Nothing system state!

=== 페이지 160 ===
132 CHAPTER 6 Unit tests
Theo Then how do we validate that the code works as expected?
Joe We’ll retrieve the system state after the code is executed and compare it to the
expected value of the state.
Theo OK. I’ll try to write the unit test.
Joe Writing unit tests for stateful code is more complicated than for data manipula-
tion code. It requires the calm of the office.
Theo Then let’s go back to the office. Waiter! Check, please.
Theo picks up the tab, and he and Joe take the cable car back to Albatross. When they’re
back at the office, Theo starts coding the unit test for Library.addMember.
Theo Can we use _.isEqual with system state?
Joe Definitely. The system state is a map like any other map.
TIP The system state is a map. Therefore, in the context of a test case, we can com-
pare the system state after a mutation is executed to the expected system state using
_.isEqual
Theo copies and pastes the code for Library.addMember (listing 6.21), which initializes
the data for the test. Then, he passes a SystemState object that is initialized with
libraryStateBefore to System.addMember. Finally, to complete the test, he compares
the system state after the mutation is executed with the expected value of the state.
class SystemState {
systemState;
get() {
return this.systemState;
}
commit(previous, next) {
this.systemState = next;
}
}
window.SystemState = SystemState;
Listing6.27 Unit test for System.addMember
var jessie = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var franck = {
"email": "franck@gmail.com",
"password": "my-top-secret"
};
var libraryStateBefore = {
"userManagement": {
"membersByEmail": {

=== 페이지 161 ===
6.4 Unit tests for mutations 133
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
}
};
var expectedLibraryStateAfter = {
"userManagement": {
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
Creates an empty
}
SystemState object
}
(see chapter 4)
}
};
Initializes the system
state with the library
data before the
var systemState = new SystemState();
mutation
systemState.commit(null, libraryStateBefore);
System.addMember(systemState, jessie);
Executes the
mutation on the
_.isEqual(systemState.get(),
SystemState object
expectedLibraryStateAfter);
Validates the state after the
mutation is executed
Joe Wow, I’m impressed; you did it! Congratulations!
Theo Thank you. I’m so glad that in DOP most of our code deals with data manipu-
lation. It’s definitely more pleasant to write unit tests for stateless code that
only deals with data manipulation.
Joe Now that you know the basics of DOP, would you like to refactor the code of
your Klafim prototype according to DOP principles?
Theo Definitely. Nancy told me yesterday that Klafim is getting nice market traction.
I’m supposed to have a meeting with her in a week or so about the next steps.
Hopefully, she’ll be willing to work with Albatross for the long term.
Joe Exciting! Do you know what might influence Nancy’s decision?
Theo Our cost estimate, certainly, but I know she’s in touch with other software com-
panies. If we come up with a competitive proposal, I think we’ll get the deal.
Joe I’m quite sure that after refactoring to DOP, features will take much less time
to implement. That means you should be able to quote Nancy a lower total cost
than the competition, right?
Theo I’ll keep my fingers crossed!

=== 페이지 162 ===
134 CHAPTER 6 Unit tests
Moving forward
The meeting with Nancy went well. Albatross got the deal, Monica (Theo’s boss) is
pleased, and it’s going to be a long-term project with a nice budget. They’ll need to hire a
team of developers in order to meet the tough deadlines. While driving back to the office,
Theo gets a phone call from Joe.
Joe How was your meeting with Nancy?
Theo We got the deal!
Joe Awesome! I told you that with DOP the cost estimation would be lower.
Theo In fact, we are not going to use DOP for this project.
Joe Why?
Theo After refactoring the Library Management System prototype to DOP, I did a
deep analysis with my engineers. We came to the conclusion that DOP might
be a good fit for the prototype phase, but it won’t work well at scale.
Joe Could you share the details of your analysis?
Theo I can’t right now. I’m driving.
Joe Could we meet in your office later today?
Theo I’m quite busy with the new project and the tough deadlines.
Joe Let’s meet at least in order to have a proper farewell.
Theo OK. Let’s meet at 4 PM, then.
 NOTE The story continues in the opener of part 2.
Summary
 Most of the code in a data-oriented system deals with data manipulation.
 It’s straightforward to write unit tests for code that deals with data manipulation.
 Test cases follow the same simple general pattern:
a Generate data input
b Generate expected data output
c Compare the output of the function with the expected data output
 In order to compare the output of a function with the expected data output, we
need to recursively compare the two pieces of data.
 The recursive comparison of two pieces of data is implemented via a generic
function.
 When a function returns a JSON string, we parse the string back to data so that
we deal with data comparison instead of string comparison.
 A tree of function calls for a function f is a tree where the root is f, and the chil-
dren of a node g in the tree are the functions called by g.
 The leaves of the tree are functions that are not part of the code base of the
application and are functions that don’t call any other functions.
 The tree of function calls visualization guides us regarding the quality and
quantity of the test cases in a unit test.

=== 페이지 163 ===
Summary 135
 Functions that appear in a lower level in the tree of function calls tend to involve
less complex data than functions that appear in a higher level in the tree.
 Functions that appear in a lower level in the tree of function calls usually need
to be covered with more test cases than functions that appear in a higher level
in the tree.
 Unit tests for mutations focus on the calculation phase of the mutation.
 The validity of the data depends on the context.
 The smaller the data, the easier it is to manipulate.
 We compare the output and the expected output of our functions with a generic
function that recursively compares two pieces of data (e.g., _.isEqual).
 When we write a unit test for a function, we assume that the functions called by
this function are covered by the unit tests and work as expected. This signifi-
cantly reduces the quantity of test cases in our unit tests.
 We avoid using string comparison in unit tests for functions that deal with data.
 Writing a unit test for the main function of a mutation requires more effort
than for a query.
 Remember to include negative test cases in your unit tests.
 The system state is a map. Therefore, in the context of a test case, we can com-
pare the system state after a mutation is executed to the expected system state
using a generic function like _.isEqual.
