# 6.2.3 Unit tests for nodes in the tree

**메타데이터:**
- ID: 58
- 레벨: 3
- 페이지: 147-148
- 페이지 수: 2
- 부모 ID: 54
- 텍스트 길이: 3514 문자

---

for nodes in the tree
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