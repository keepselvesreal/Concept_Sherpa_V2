# 12 Introduction

**메타데이터:**
- ID: 115
- 레벨: 2
- 페이지: 275-276
- 페이지 수: 2
- 부모 ID: 114
- 텍스트 길이: 5898 문자

---

=== Page 274 ===
246 PART 3 Maintainability
Joe You see, DOP is such a simple paradigm that it’s fertile material for innovation.
Part of the material I taught you I learned from others, and part of it was an
invention of mine. If you keep practicing DOP, I’m quite sure you, too, will
come up with some inventions of your own.
Theo What do you say Dave? Are you willing to learn DOP from me?
Dave Definitely!
Theo Joe, will you be continue to be available if we need your help from time to time?
Joe Of course!

=== Page 275 ===
Advanced data
validation
A self-made gift
This chapter covers
 Validating function arguments
 Validating function return values
 Data validation beyond static types
 Automatic generation of data model diagrams
 Automatic generation of schema-based unit tests
As the size of a code base grows in a project that follows DOP principles, it becomes
harder to manipulate functions that receive and return only generic data. It is hard
to figure out the expected shape of the function arguments, and when we pass
invalid data, we don’t get meaningful errors.
Until now, we have illustrated how to validate data at system boundaries. In this
chapter, we will illustrate how to validate data when it flows inside the system by
defining data schemas for function arguments and their return values. This allows
us to make explicit the expected shape of function arguments, and it eases develop-
ment. We gain some additional benefits from this endeavor, such as automatic gen-
eration of data model diagrams and schema-based unit tests.
247

=== Page 276 ===
248 CHAPTER 12 Advanced data validation
12.1 Function arguments validation
Dave’s first task is to implement a couple of new HTTP endpoints to download the catalog
as a CSV file, search books by author, and rate the books. Once he is done with the tasks,
Dave calls Theo for a code review.
 NOTE The involvement of Dave in the Klafim project is explained in the opener for
part 3. Please take a moment to read the opener if you missed it.
Theo Was it difficult to get your head around the DOP code?
Dave Not so much. I read your notes of the meetings with Joe, and I must admit, the
code is quite simple to grasp.
Theo Cool!
Dave But there is something that I can’t get used to.
Theo What’s that?
Dave I’m struggling with the fact that all the functions receive and return generic
data. In OOP, I know the expected shape of the arguments for each and every
function.
Theo Did you validate data at system boundaries, like I have done?
Dave Absolutely. I defined a data schema for every additional user request, database
query, and external service response.
Theo Nice!
Dave Indeed, when the system runs in production, it works well. When data is valid,
the data flows through the system, and when data is invalid, we are able to dis-
play a meaningful error message to the user.
Theo What’s the problem then?
Dave The problem is that during development, it’s hard to figure out the expected
shape of the function arguments. And when I pass invalid data by mistake, I
don’t get clear error messages.
Theo I see. I remember that when Joe showed me how to validate data at system
boundaries, I raised this concern about the development phase. Joe told me
then that we validate data as it flows inside the system exactly like we validate data
at system boundaries: we separate between data schema and data representation.
Dave Are we going to use JSON Schema also?
Theo Yes.
Dave Cool.... I like JSON Schema.
Theo The main purpose of data validation at system boundaries is to prevent invalid
data from getting into the system, whereas the main purpose of data validation
inside the system is to make it easier to develop the system. Here, let me draw a
table on the whiteboard for you to visualize this (table 12.1).
Table 12.1 Two kinds of data validation
Kind of data validation Purpose Environment
Boundaries Guardian Production
Inside Ease of development Dev

=== Page 277 ===
12.1 Function arguments validation 249
Dave By making it easier to develop the system, do you mean to help the developers
understand the expected shape of function arguments as in OOP?
Theo Exactly.
Dave But I’m impatient.... Will you help me figure out how to validate the argu-
ments of the function that implements a book search?
Theo Let me see the code of the implementation, and I’ll do my best.
Dave We have two implementations of a book search: one where library data lives
in memory from the prototype phase and one where library data lives in the
database.
Theo I think that the schema for library data in memory is going to be more interest-
ing than the schema for library data in the database, as the book search func-
tion receives catalog data in addition to the query.
Dave When you say more interesting data schema, you mean more difficult to write?
Theo More difficult to write, but it’s also more insightful.
Dave Then let’s go with library data in memory. The code for Catalog.search-
BooksByTitle from the prototype phase would look like this.
Dave pulls up some code on his laptop. He shows it to Theo.
Listing12.1 The implementation of search without data validation
class Catalog {
static authorNames(catalogData, book) {
var authorIds = _.get(book, "authorIds");
var names = _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
return names;
}
static bookInfo(catalogData, book) {
var bookInfo = {
"title": _.get(book, "title"),
"isbn": _.get(book, "isbn"),
"authorNames": Catalog.authorNames(catalogData, book)
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