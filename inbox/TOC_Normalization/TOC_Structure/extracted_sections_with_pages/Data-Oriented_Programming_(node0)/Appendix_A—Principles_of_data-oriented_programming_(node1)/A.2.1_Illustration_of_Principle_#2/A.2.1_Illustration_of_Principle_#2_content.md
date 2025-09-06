# A.2.1 Illustration of Principle #2

**페이지**: 350-351
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:30

---


--- 페이지 350 ---

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

--- 페이지 350 끝 ---


--- 페이지 351 ---

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

--- 페이지 351 끝 ---
