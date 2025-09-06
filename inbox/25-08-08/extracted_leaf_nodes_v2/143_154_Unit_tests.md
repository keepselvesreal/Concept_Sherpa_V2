# 15.4 Unit tests

**메타데이터:**
- ID: 143
- 레벨: 2
- 페이지: 349-356
- 페이지 수: 8
- 부모 ID: 138
- 텍스트 길이: 14860 문자

---

321
Listing15.13 Testing searchBooksByTitle again
Catalog.searchBooksByTitle(catalogData, 'Habit');
// → [ { "title": "7 Habits of Highly Effective People", …}]
Dave It works!
Theo Let’s try more queries: abit and bit should not return any book, but habit
and 7 Habits should return only one book.
In the REPL, Dave tries the four queries that Theo suggested. For abit and bit, the code
works as expected, but for habit and 7 Habits it fails.
Dave Let me try to fix that code.
Theo I suggest that you instead write a couple of unit tests that check the various inputs.
Dave Good idea. Is there a way to use reproducibility in the context of unit tests?
Theo Absolutely!
15.4 Unit tests
Dave How do we use reproducibility in a unit test?
Theo As Joe told showed me so many times, in DOP, unit tests are really simple. They
call a function with some data, and they check that the data returned by the
function is the same as we expect.
Dave I remember that! I have written many unit tests for the Library Management
System following this approach. But sometimes, I struggled to provide input
data for the functions under test. For instance, building catalog data with all its
nested fields was not a pleasure.
Theo Here’s where reproducibility can help. Instead of building data manually, you
put the system under the conditions you’d like to test, and then capture data
inside the function under test. Once data is captured, you use it in your unit test.
Dave Nice! Let me write a unit test for Catalog.searchBooksByTitle following
this approach.
Dave triggers the search endpoint once again. Then, he opens the console and copies the
line with the captured catalog data to the clipboard. Finally, he pastes it inside the code of
the unit test.
Listing15.14 A unit test with captured data
var catalogData =
{"booksByIsbn":{"978-1982137274":{"isbn":"978-1982137274",
"title":"7 Habits of Highly Effective People","authorIds":["sean-covey",
"stephen-covey"]},"978-1779501127":{"isbn":"978-1779501127","title":
"Watchmen","publicationYear":1987,"authorIds":["alan-moore",
"dave-gibbons"]}},"authorsById":{"stephen-covey":{"name":
"Stephen Covey","bookIsbns":["978-1982137274"]},"sean-covey":
{"name":"Sean Covey","bookIsbns":["978-1982137274"]},"dave-gibbons":
{"name":"Dave Gibbons","bookIsbns":["978-1779501127"]},"alan-moore":
{"name":"Alan Moore","bookIsbns":["978-1779501127"]}}};
var query = "Habit";

322 CHAPTER 15 Debugging
var result = Catalog.searchBooksByTitle(catalogData, query);
var expectedResult = [
{
"authorNames": [
"Sean Covey",
"Stephen Covey",
],
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
}
];
_.isEqual(result, expectedResult);
// → true
Theo Well done! Now, would you like me to show you how to do the same without
copying and pasting?
Dave Definitely.
Theo Instead of displaying the captured data to the console, we’re going to write it to
a file and read data from that file inside the unit test.
Dave Where are you going to save the files that store captured data?
Theo Those files are part of the unit tests. They need to be under the same file tree
as the unit tests.
Dave There are so many files! How do we make sure a file doesn’t override an exist-
ing file?
Theo By following a simple file-naming convention. A name for a file that stores cap-
tured data is made of two parts: a context (for example, the name of the func-
tion where data was captured) and a universal unique identifier (a UUID).
Dave How do you generate a UUID?
Theo In some languages it’s part of the language, but in other languages like Java-
Script, you need a third-party library like uuid. Let me bookmark its site for you.
I also happen to have a list of libraries for UUIDs. I’ll send that table to you too.
Theo bookmarks the site for the third-party library uuid (https://github.com/uuidjs/
uuid) on Dave’s computer. Then, using his laptop, he finds his list and sends that to Dave.
Dave receives the email, and he takes a moment to quickly glance through the table 15.2
before turning his attention back to Theo.
Table 15.2 Libraries for UUID generation
Language UUID library
JavaScript https://github.com/uuidjs/uuid
Java java.util.UUID
C# Guid.NewGuid
Python uuid
Ruby SecureRandom

15.4 Unit tests 323
Theo The code for the dataFilePath function that receives a context and returns a
file path is fairly simple. Check this out.
Listing15.15 Computing the file path for storing captured data
var capturedDataFolder = "test-data";
The root folder
function dataFilePath(context) {
for captured data
var uuid = generateUUID();
return capturedDataFolder
UUID generation is language-
+ "/" + context
dependent (see table 15.2).
+ "-" + ".json";
}
Uses json as a file extension
because we serialize data to JSON
Dave How do we store a piece of data in a JSON file?
Theo We serialize it and write it to disk.
Dave Synchronously or asynchronously?
Theo I prefer to write to the disk asynchronously or in a separate thread in run times
that support multithreading to avoid slowing down the real work. Here’s my
implementation of dumpData.
Listing15.16 Dumping data in JSON format
function dumpData(data, context) {
var path = dataFilePath(context); Writes asynchronously
to prevent blocking
var content = JSON.stringify(data);
the real work
fs.writeFile(path, content, function () {
The third argument is a
console.log("Data for " +
callback function, called
context +
when write completes.
"stored in: " +
path);
Displays a message once
});
data is written to the file
}
Dave Let me see if I can use dumpData inside Catalog.searchBooksByTitle and
capture the context to a file. I think that something like this should work.
Listing15.17 Capturing the context into a file
Catalog.searchBooksByTitle = function(catalogData, query) {
dumpData([catalogData, query], 'searchBooksByTitle');
var allBooks = _.get(catalogData, "booksByIsbn");
var queryLowerCased = query.toLowerCase();
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title")
.toLowerCase()
.startsWith(queryLowerCased);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});

324 CHAPTER 15 Debugging
return bookInfos;
};
Theo Trigger the endpoint to see if it works.
Dave triggers the search endpoint once again and views the output in the console. When he
opens the file mentioned in the log message, he sees a single line that is hard to decipher.
Listing15.18 Console output when triggering the search endpoint
Data for searchBooksByTitle stored in
test-data/searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json
Listing15.19 The content of the JSON file that captured the context
[{"booksByIsbn":{"978-1982137274":{"isbn":"978-1982137274",
"title":"7 Habits of Highly Effective People","authorIds":
["sean-covey","stephen-covey"]},"978-1779501127":{"isbn":
"978-1779501127","title":"Watchmen","publicationYear":1987,
"authorIds":["alan-moore","dave-gibbons"]}},"authorsById":
{"stephen-covey":{"name":"Stephen Covey","bookIsbns":
["978-1982137274"]},"sean-covey":{"name":"Sean Covey",
"bookIsbns":["978-1982137274"]},"dave-gibbons":
{"name":"Dave Gibbons","bookIsbns":["978-1779501127"]},
"alan-moore":{"name":"Alan Moore","bookIsbns":
["978-1779501127"]}}},"Habit"]
Dave Reading this JSON file is very difficult!
Theo We can beautify the JSON string if you want.
Dave How?
Theo By passing to JSON.stringify the number of space characters to use for
indentation. How many characters would you like to use for indentation?
Dave Two.
After adding the number of indentation characters to the code of dumpData, Dave then
opens the JSON file mentioned in the log message (it’s a different file name!). He now
sees a beautiful JSON array with two elements.
Listing15.20 Dumping data in JSON format with indentation
The second argument to
function dumpData(data, context) {
JSON.stringify is ignored.
var path = dataFilePath(context);
The third argument to
var content = JSON.stringify(data, null, 2);
JSON.stringify specifies the
number of characters to
use for indentation.
fs.writeFile(path, content, function () {
console.log("Data for " + context + "stored in: " + path);
});
}

15.4 Unit tests 325
Listing15.21 The captured context with indentation in the JSON file
[
{
"booksByIsbn": {
"978-1982137274": {
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"authorIds": [
"sean-covey",
"stephen-covey"
]
},
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": [
"alan-moore",
"dave-gibbons"
]
}
},
"authorsById": {
"stephen-covey": {
"name": "Stephen Covey",
"bookIsbns": [
"978-1982137274"
]
},
"sean-covey": {
"name": "Sean Covey",
"bookIsbns": [
"978-1982137274"
]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": [
"978-1779501127"
]
},
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": [
"978-1779501127"
]
}
}
},
"Habit"
]

326 CHAPTER 15 Debugging
Dave While looking at the contents of the JSON file, I thought about the fact that we
write data to the file in an asynchronous way. It means that data is written con-
currently to the execution of the function code, right?
Theo Right! As I told you, we don’t want to slow down the real work.
Dave I get that. What happens if the code of the function modifies the data that we
are writing? Will we write the original data to the file or the modified data?
Theo I’ll let you think about that while I get a cup of tea at the museum coffee shop.
Would you like some coffee?
Dave What, you’re not having coffee?
Theo I finally found the time to read the book The Power of Habit by Charles Duhigg.
Joe read the book and quit biting his fingernails, so I decided to read it to cut
down on my habit of going for yet another cup of coffee.
Dave That’s impressive, but I’d like an espresso, please.
While Theo goes to the coffee shop, Dave explores the Wind Arrows exhibit outside the
auditorium. He’s hoping that his mind will be inspired by the beauty of science. He takes a
few breaths to relax, and after a couple of minutes, Dave has an Aha! moment. He knows
the answer to his question about the function changing data.
Theo comes back, gingerly carrying the hot beverages, and finds Dave in the audito-
rium. Dave smiles at Theo and says:
Dave In DOP, we never mutate data. Therefore, my question is no longer a ques-
tion: the code of the function cannot modify the data while we are writing it
to the file.
Theo You’ve got it! Now, let me show you how to use data from the JSON file in a
unit test. First, we need a function that reads data from a JSON file and deseri-
alizes it, probably something like readData.
Listing15.22 Reading data from a JSON file
function readData(path) {
return JSON.parse(fs.readFileSync(path));
}
Dave Why are you reading synchronously and not asynchronously like you did when
we captured the data?
Theo Because readData is meant to be used inside a unit test, and we cannot run
the test before the data is read from the file.
Dave That makes sense. Using readData inside a unit test seems straightforward. Let
me use it to read our captured data.
Listing15.23 A unit test that reads captured data from a file
var data = readData("test-data/" +
"searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json");
var catalogData = data[0];
var query = data[1];

15.4 Unit tests 327
var result = Catalog.searchBooksByTitle(catalogData, query);
var expectedResult = [
{
"authorNames": [
"Sean Covey",
"Stephen Covey",
],
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
}
];
_.isEqual(result, expectedResult);
// → false
Theo Do you prefer the version of the unit test with the inline data or with the data
read from the file?
Dave It depends. When data is minimal, I prefer to have the data inline because it
allows me to see the data. But when data is substantial, like the catalog data,
having the data inline makes the code hard to read.
Theo OK. Let’s fix the code of the improved search so that it works with the two que-
ries that return an empty result.
Dave I completely forgot about that. Do you remember those two queries?
Theo Yes, it was habit and 7 Habits.
Dave The first query doesn’t work because the code leaves the strings in their origi-
nal case. I can easily fix that by converting both the book title and the query to
lowercase.
Theo And what about the second query?
Dave It’s much harder to deal with because it’s made of two words. I somehow need
to check whether the title subsequently contains those two prefixes.
Theo Are you familiar with the \b regular expression metacharacter?
Dave No.
Theo \b matches a position that is called a word boundary. It allows us to perform pre-
fix matching.
Dave Cool. Can you give me an example?
Theo Sure. For instance, \bHabits and \b7 Habits match 7 Habits of Highly
Effective People, but abits won’t match.
Dave What about \bHabits of?
Theo It also matches.
Dave Excellent. This is exactly what I need! Let me fix the code of hasWordStart-
ingWith so that it does a case-insensitive prefix match.
Listing15.24 A revised version of hasWordStartingWith
function hasWordStartingWith(sentence, prefix) {
var sentenceLowerCase = sentence.toLowerCase();
var prefixLowerCase = prefix.toLowerCase();

328 CHAPTER 15 Debugging
var prefixRegExp = new RegExp("\\b" +
When passing \b to the
prefixLowerCase);
RegExp constructor, we
return sentenceLowerCase.match(prefixRegExp) != null; need an extra backslash.
}
Theo Now, let me write unit tests for all the cases.
Dave One test per query?
Theo You could, but it’s more efficient to have a unit test for all the queries that
should return a book and another one for all the queries that should return no
books. Give me a minute.
Theo codes for a while and produces two unit tests. He then shows the tests to Dave and
enjoys another sip of his tea.
Listing15.25 A unit test for several queries that should return a book
var data =
readData("test-data/" +
"searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json");
var catalogData = data[0];
var queries = ["Habit", "habit", "7 Habit", "habits of"];
var expectedResult = [
{
"authorNames": [
"Sean Covey",
"Stephen Covey",
],
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
}
];
_.every(queries, function(query) {
var result = Catalog.searchBooksByTitle(catalogData, query);
return _.isEqual(result, expectedResult);
});
// → [true, true, true, true]
Listing15.26 A unit test for several queries that should return no book
var data =
readData("test-data/" +
"searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json");
var catalogData = data[0];
var queries = ["abit", "bit", "7 abit", "habit of"];
var expectedResult = [ ];
_.every(queries, function(query) {
var result = Catalog.searchBooksByTitle(catalogData, query);
return _.isEqual(result, expectedResult);
});
// → [true, true, true, true]