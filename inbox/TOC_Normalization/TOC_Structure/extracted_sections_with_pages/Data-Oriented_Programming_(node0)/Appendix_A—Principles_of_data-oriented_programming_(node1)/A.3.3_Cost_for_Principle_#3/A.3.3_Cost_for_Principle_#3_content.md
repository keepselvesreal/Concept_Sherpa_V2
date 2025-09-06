# A.3.3 Cost for Principle #3

**페이지**: 356-357
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:33

---


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


--- 페이지 357 ---

15.5 Dealing with external data sources 329
Dave What is _.every?
Theo It’s a Lodash function that receives a collection and a predicate and returns
true if the predicate returns true for every element of the collection.
Dave Nice!
Dave runs the unit tests and they pass. He then enjoys a sip of his espresso.
Dave Now, am I allowed to trigger the search endpoint with 7 Habit in order to con-
firm that the improved search works as expected?
Theo Of course. It’s only during the multiple iterations of code improvements that I
advise you not to trigger the system from the outside in order to benefit from a
shorter feedback loop. Once you’re done with the debugging and fixing, you
must then test the system from end to end.
Dave triggers the search endpoint with 7 Habit. It returns the details about 7 Habits of
Highly Effective People as expected.
15.5 Dealing with external data sources
Dave Can we also use reproducibility when the code involves fetching data from an
external data source like a database or an external service?
Theo Why not?
Dave The function context might be exactly the same, but the behavior might be dif-
ferent if the function fetches data from a data source that returns a different
response for the same query.
Theo Well, it depends on the data source. Some databases are immutable in the
sense that the same query always returns the same response.
Dave I have never heard about immutable databases.
Theo Sometimes, they are called functional databases or append-only databases.
Dave Never heard about them either. Did you mean read-only databases?
Theo Read-only databases are immutable for sure, but they are not useful for storing
the state of an application.
Dave How could a database be both writable and immutable?
Theo By embracing time.
Dave What does time have to do with immutability?
Theo In an immutable database, a record has an automatically generated timestamp,
and instead of updating a record, we create a new version of it with a new time-
stamp. Moreover, a query always has a time range in addition to the query
parameters.
Dave Why does that guarantee that the same query will always return the same
response?
Theo In an immutable database, queries don’t operate on the database itself. Instead,
they operate on a database snapshot, which never changes. Therefore, queries
with the same parameters are guaranteed to return the same response.

--- 페이지 357 끝 ---
