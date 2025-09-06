# A.1.4 Summary of Principle #1

**페이지**: 349-350
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:29

---


--- 페이지 349 ---

15.4 Unit tests 321
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

--- 페이지 349 끝 ---


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
