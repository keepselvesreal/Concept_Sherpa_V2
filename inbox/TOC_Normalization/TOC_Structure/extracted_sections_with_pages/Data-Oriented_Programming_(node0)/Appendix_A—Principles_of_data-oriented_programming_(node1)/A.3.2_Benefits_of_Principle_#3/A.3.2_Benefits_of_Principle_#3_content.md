# A.3.2 Benefits of Principle #3

**페이지**: 355-356
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:32

---


--- 페이지 355 ---

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

--- 페이지 355 끝 ---


--- 페이지 356 ---

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

--- 페이지 356 끝 ---
