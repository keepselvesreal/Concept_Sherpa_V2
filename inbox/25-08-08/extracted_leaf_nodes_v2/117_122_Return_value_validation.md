# 12.2 Return value validation

**메타데이터:**
- ID: 117
- 레벨: 2
- 페이지: 283-284
- 페이지 수: 2
- 부모 ID: 114
- 텍스트 길이: 3482 문자

---

e validation 255
Theo Because that data has been already validated up front at a system boundary.
Validating it again on a function call is superfluous, and it would impact
performance.
Dave When you say development time, does that include testing and staging
environments?
Theo Yes, all the environments besides production.
Dave I see. It’s like assertions in Java. They are disabled in production code.
TIP Data validation inside the system should be disabled in production.
Theo Exactly. For now, I am going to assume that we have a dev function that returns
true when the code runs in the development environment and false when it
runs in production. Having said that, take a look at this code.
Listing12.9 Implementation of search with validation of function arguments
Catalog.searchBooksByTitle = function(catalogData, query) {
if(dev()) {
var args = [catalogData, query];
if(!ajv.validate(searchBooksArgsSchema, args)) {
var errors = ajv.errorsText(ajv.errors);
throw ("searchBooksByTitle called with invalid arguments: " +
errors);
The implementation of dev() depends on the run-time
}
environment: it returns true when the code runs in dev
}
environments and false when it runs in production.
var allBooks = _.get(catalogData, "booksByIsbn");
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title").includes(query);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
};
Dave Do you think we should validate the arguments of all the functions?
Theo No. I think we should treat data validation like we treat unit tests. We should
validate function arguments only for functions for whom we would write unit
tests.
TIP Treat data validation like unit tests.
12.2 Return value validation
Dave Do you think it would make sense to also validate the return value of functions?
Theo Absolutely.
Dave Cool. Let me try to write the JSON Schema for the return value of Catalog
.searchBooksByTitle.

256 CHAPTER 12 Advanced data validation
After a few minutes, Dave comes up with the schema. Taking a deep breath, then releasing
it, he shows the code to Theo.
Listing12.10 The schema for the return value of Catalog.searchBooksByTitle
var searchBooksResponseSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["title", "isbn", "authorNames"],
"properties": {
"title": {"type": "string"},
"isbn": {"type": "string"},
"authorNames": {
"type": "array",
"items": {"type": "string"}
}
}
}
};
Theo Well done! Now, would you like to try adding return value validation to the
code of Catalog.searchBooksByTitle?
Dave Sure.
Dave works for a bit in his IDE. A bit more confident this time, he shows the result to Theo.
Listing12.11 Search with data validation for both input and output
Catalog.searchBooksByTitle = function(catalogData, query) {
if(dev()) {
if(!ajv.validate(searchBooksArgsSchema, [catalogData, query])) {
var errors = ajv.errorsText(ajv.errors);
throw ("searchBooksByTitle called with invalid arguments: " +
errors);
}
}
var allBooks = _.get(catalogData, "booksByIsbn");
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title").includes(query);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
if(dev()) {
if(!ajv.validate(searchBooksResponseSchema, bookInfos)) {
var errors = ajv.errorsText(ajv.errors);
throw ("searchBooksByTitle returned an invalid value: " +
errors);
}
}