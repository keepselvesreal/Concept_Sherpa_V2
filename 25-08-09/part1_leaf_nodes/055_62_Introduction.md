# 6.2 Introduction

**ID**: 55  
**Level**: 3  
**추출 시간**: 2025-08-09 10:09:52 KST

---

6.2 Unit tests for data manipulation code
A waiter in an elegant bow tie brings Theo his croissant and Joe his pain au chocolat. The
two friends momentarily interrupt their discussion to savor their French pastries. When
they’re done, they ask the waiter to bring them their drinks. Meanwhile, they resume the
discussion.
Joe Do you remember the code flow of the implementation of the search query?
Theo Let me look again at the code that implements the search query.
Theo brings up the implementation of the search query on his laptop. Noticing that Joe is
chewing on his nails again, he quickly checks out the code.

## 페이지 141

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
