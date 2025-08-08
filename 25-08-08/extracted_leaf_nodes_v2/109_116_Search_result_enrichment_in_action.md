# 11.6 Search result enrichment in action

**메타데이터:**
- ID: 109
- 레벨: 2
- 페이지: 262-271
- 페이지 수: 10
- 부모 ID: 102
- 텍스트 길이: 13966 문자

---

lt enrichment in action
Joe Can you write the steps of the enrichment data flow?
Theo Sure.
Theo goes to the whiteboard. He takes a moment to gather his thoughts, and then erases
enough space so there’s room to list the steps.
The steps for the search result enrichment data flow
1 Receive a request from a client.
2 Extract from the client’s request the query and the fields to fetch from Open
Library.
3 Retrieve from the database the books that match the query.
4 Fetch information from Open Library for each ISBN that match the query.
5 Extract from Open Library responses for the required fields.
6 Combine book information from the database with information from Open
Library.
7 Send the response to the client.
Joe Perfect! Would you like to try to implement it?
Theo I think I’ll start with the implementation of the book retrieval from the data-
base. It’s quite similar to what we did last month.
 NOTE See chapter 10 for last month’s lesson.
Joe Actually, it’s even simpler because you don’t need to join tables.
Theo That’s right, I need values only for the isbn and available columns.
Theo works for a bit in his IDE. He begins with the book retrieval from the database.
Listing11.14 Retrieving books whose title matches a query
var dbSearchResultSchema = {
"type": "array",
"items": {

11.6 Search result enrichment in action 235
"type": "object",
"required": ["isbn", "available"],
"properties": {
"isbn": {"type": "string"},
"available": {"type": "boolean"}
}
}
};
class CatalogDB {
static matchingBooks(title) {
var matchingBooksQuery = `
SELECT isbn, available
FROM books
WHERE title = like '%$1%';
`;
var books = dbClient.query(catalogDB, matchingBooksQuery, [title]);
if(!ajv.validate(dbSearchResultSchema, books)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from the database: " +
errors;
}
return books;
}
}
Joe So far, so good...
Theo Next, I’ll go with the implementation of the retrieval of book information from
Open Library for several books. Unfortunately, the Open Library Books API
doesn’t support querying several books at once. I’ll need to send one request
per book.
Joe That’s a bit annoying. Let’s make our life easier and pretend that _.map works
with asynchronous functions. In real life, you’d need something like Promise
.all in order to send the requests in parallel and combine the responses.
Theo OK, then it’s quite straightforward. I’ll take the book retrieval code and add a
multipleBookInfo function that maps over bookInfo.
Theo looks over the book retrieval code in listing 11.9 and then concentrates as he types
into his IDE. When he’s done, he shows the result in listing 11.15 to Joe.
Listing11.15 Retrieving book information from Open Library for several books
class OpenLibraryDataSource {
static rawBookInfo(isbn) {
var url = `https:/ /openlibrary.org/isbn/${isbn}.json`;
var jsonString = fetchResponseBody(url);
return JSON.parse(jsonString);
}
static bookInfo(isbn, requestedFields) {
var relevantFields = ["title", "full_title",
"subtitle", "publisher",
"publish_date", "weight",

236 CHAPTER 11 Web services
"physical_dimensions", "genre",
"subjects", "number_of_pages"];
var rawInfo = rawBookInfo(isbn);
if(!ajv.validate(dbSearchResultSchema, bookInfoSchema)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from Open Books API: " +
errors;
}
var relevantInfo =
_.pick(_.pick(rawInfo, relevantFields), requestedFields);
return _.set(relevantInfo, "isbn", isbn);
}
static multipleBookInfo(isbns, fields) {
return _.map(function(isbn) {
return bookInfo(isbn, fields);
}, isbns);
}
}
Joe Nice! Now comes the fun part: combining information from several data sources.
Theo Yeah. I have two arrays in my hands: one with book information from the data-
base and one with book information from Open Library. I somehow need to
join the arrays, but I’m not sure I can assume that the positions of the book
information are the same in both arrays.
Joe What would you like to have in your hands?
Theo I wish I had two hash maps.
Joe And what would the keys in the hash maps be?
Theo Book ISBNs.
Joe Well, I have good news for you: your wish is granted!
Theo How?
Joe Lodash provides a function named _.keyBy that transforms an array into a map.
Theo I can’t believe it. Can you show me an example?
Joe Sure. Let’s call _.keyBy on an array with two books.
Listing11.16 Transforming an array into a map with _.keyBy
var books = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"available": true
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"available": false
}
];
_.keyBy(books, "isbn");

11.6 Search result enrichment in action 237
Joe And here’s the result.
Listing11.17 The result of keyBy
{
"978-0812981605": {
"available": false,
"isbn": "978-0812981605",
"title": "The Power of Habit"
},
"978-1982137274": {
"available": true,
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
}
}
Theo keyBy is awesome!
Joe Don’t exaggerate, my friend; _.keyBy is quite similar to _.groupBy. The
only difference is that _.keyBy assumes that there’s only one element in
each group.
Theo I think that, with _.keyBy, I’ll be able to write a generic joinArrays function.
Joe I’m glad to see you thinking in terms of implementing business logic through
generic data manipulation functions.
TIP Many parts of the business logic can be implemented through generic data
manipulation functions.
Theo The joinArrays function needs to receive the arrays and the field name for
which we decide the two elements that need to be combined, for instance,
isbn.
Joe Remember, in general, it’s not necessarily the same field name for both arrays.
Theo Right, so joinArrays needs to receive four arguments: two arrays and two
field names.
Joe Go for it! And, please, write a unit test for joinArrays.
Theo Of course...
Theo works for a while and produces the code in listing 11.18. He then types the unit test
in listing 11.19.
Listing11.18 A generic function for joining arrays
function joinArrays(a, b, keyA, keyB) {
var mapA = _.keyBy(a, keyA);
var mapB = _.keyBy(b, keyB);
var mapsMerged = _.merge(mapA, mapB);
return _.values(mapsMerged);
}

238 CHAPTER 11 Web services
Listing11.19 A unit test for joinArrays
var dbBookInfos = [
{
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"available": true
},
{
"isbn": "978-0812981605",
"title": "The Power of Habit",
"available": false
}
];
var openLibBookInfos = [
{
"isbn": "978-0812981605",
"title": "7 Habits of Highly Effective People",
"subtitle": "Powerful Lessons in Personal Change",
"number_of_pages": 432,
},
{
"isbn": "978-1982137274",
"title": "The Power of Habit",
"subtitle": "Why We Do What We Do in Life and Business",
"subjects": [
"Social aspects",
"Habit",
"Change (Psychology)"
],
}
];
var joinedArrays = [
{
"available": true,
"isbn": "978-1982137274",
"subjects": [
"Social aspects",
"Habit",
"Change (Psychology)",
],
"subtitle": "Why We Do What We Do in Life and Business",
"title": "The Power of Habit",
},
{
"available": false,
"isbn": "978-0812981605",
"number_of_pages": 432,
"subtitle": "Powerful Lessons in Personal Change",
"title": "7 Habits of Highly Effective People",
},
]

11.6 Search result enrichment in action 239
_.isEqual(joinedArrays,
joinArrays(dbBookInfos, openLibBookInfos, "isbn", "isbn"));
Joe Excellent! Now, you are ready to adjust the last piece of the extended search
result endpoint.
Theo That’s quite easy. We fetch data from the database and from Open Library and
join them.
Theo works quite rapidly. He then shows Joe the code.
Listing11.20 Search books and enriched book information
class Catalog {
static enrichedSearchBooksByTitle(searchPayload) {
if(!ajv.validate(searchBooksRequestSchema, searchPayload)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid request:" + errors;
}
var title = _.get(searchPayload, "title");
var fields = _.get(searchPayload, "fields");
var dbBookInfos = CatalogDataSource.matchingBooks(title);
var isbns = _.map(dbBookInfos, "isbn");
var openLibBookInfos =
OpenLibraryDataSource.multipleBookInfo(isbns, fields);
var res = joinArrays(dbBookInfos, openLibBookInfos);
if(!ajv.validate(searchBooksResponseSchema, request)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid response:" + errors;
}
return res;
}
}
Now comes the tricky part. Theo takes a few moments to meditate about the simplicity of
the code that implements the extended search endpoint. He thinks about how classes are
much less complex when we use them only to aggregate stateless functions that operate on
similar domain entities and then goes to work plotting the code.
Listing11.21 Schema for the extended search endpoint (Open Books API part)
var basicBookInfoSchema = {
"type": "object",
"required": ["title"],
"properties": {
"title": {"type": "string"},
"publishers": {
"type": "array",
"items": {"type": "string"}
},

240 CHAPTER 11 Web services
"number_of_pages": {"type": "integer"},
"weight": {"type": "string"},
"physical_format": {"type": "string"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn_13": {
"type": "array",
"items": {"type": "string"}
},
"isbn_10": {
"type": "array",
"items": {"type": "string"}
},
"publish_date": {"type": "string"},
"physical_dimensions": {"type": "string"}
}
};
var mandatoryIsbn13 = {
"type": "object",
"required": ["isbn_13"]
};
var mandatoryIsbn10 = {
"type": "object",
"required": ["isbn_10"]
};
var bookInfoSchema = {
"allOf": [
basicBookInfoSchema,
{
"anyOf": [mandatoryIsbn13, mandatoryIsbn10]
}
]
};
Listing11.22 Extended search endpoint (Open Books API part)
var ajv = new Ajv({allErrors: true});
class OpenLibraryDataSource {
static rawBookInfo(isbn) {
var url = `https:/ /openlibrary.org/isbn/${isbn}.json`;
var jsonString = fetchResponseBody(url);
return JSON.parse(jsonString);
}
static bookInfo(isbn, requestedFields) {
var relevantFields = ["title", "full_title",
"subtitle", "publisher",
"publish_date", "weight",

11.6 Search result enrichment in action 241
"physical_dimensions", "genre",
"subjects", "number_of_pages"];
var rawInfo = rawBookInfo(isbn);
if(!ajv.validate(bookInfoSchema, rawInfo)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from Open Books API: " +
errors;
}
var relevantInfo = _.pick(
_.pick(rawInfo, relevantFields),
requestedFields);
return _.set(relevantInfo, "isbn", isbn);
}
static multipleBookInfo(isbns, fields) {
return _.map(function(isbn) {
return bookInfo(isbn, fields);
}, isbns);
}
}
Listing11.23 Extended search endpoint (database part)
var dbClient;
var dbSearchResultSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["isbn", "available"],
"properties": {
"isbn": {"type": "string"},
"available": {"type": "boolean"}
}
}
};
class CatalogDB {
static matchingBooks(title) {
var matchingBooksQuery = `
SELECT isbn, available
FROM books
WHERE title = like '%$1%';
`;
var books = dbClient.query(catalogDB, matchingBooksQuery, [title]);
if(!ajv.validate(dbSearchResultSchema, books)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from the database: "
+ errors;
}
return books;
}
}

242 CHAPTER 11 Web services
Listing11.24 Schema for the implementation of the extended search endpoint
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {
"type": [
"title",
"full_title",
"subtitle",
"publisher",
"publish_date",
"weight",
"physical_dimensions",
"number_of_pages",
"subjects",
"publishers",
"genre"
]
}
}
},
"required": ["title", "fields"]
};
var searchBooksResponseSchema = {
"type": "object",
"required": ["title", "isbn", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"publishers": {
"type": "array",
"items": {"type": "string"}
},
"number_of_pages": {"type": "integer"},
"weight": {"type": "string"},
"physical_format": {"type": "string"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn": {"type": "string"},
"publish_date": {"type": "string"},
"physical_dimensions": {"type": "string"}
}
};
Listing11.25 Schema for the extended search endpoint (combines the pieces)
class Catalog {
static enrichedSearchBooksByTitle(request) {

11.6 Search result enrichment in action 243
if(!ajv.validate(searchBooksRequestSchema, request)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid request:" + errors;
}
var title = _.get(request, "title");
var fields = _.get(request, "fields");
var dbBookInfos = CatalogDataSource.matchingBooks(title);
var isbns = _.map(dbBookInfos, "isbn");
var openLibBookInfos =
OpenLibraryDataSource.multipleBookInfo(isbns, fields);
var response = joinArrays(dbBookInfos, openLibBookInfos);
if(!ajv.validate(searchBooksResponseSchema, request)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid response:" + errors;
}
return response;
}
}
class Library {
static searchBooksByTitle(payloadBody) {
var payloadData = JSON.parse(payloadBody);
var results = Catalog.searchBooksByTitle(payloadData);
return JSON.stringify(results);
}
}
TIP Classes are much less complex when we use them as a means to aggregate state-
less functions that operate on similar domain entities.
Joe interrupts Theo’s meditation moment. After looking over the code in the previous list-
ings, he congratulates Theo.
Joe Excellent job, my friend! By the way, after reading The Power of Habit, I quit
chewing my nails.
Theo Wow! That’s terrific! Maybe I should read that book to overcome my habit of
drinking too much coffee.
Joe Thanks, and good luck with the coffee habit.
Theo I was supposed to call Nancy later today with an ETA for the Open Library
Book milestone. I wonder what her reaction will be when I tell her the feature
is ready.
Joe Maybe you should tell her it’ll be ready in a week, which would give you time to
begin work on the next milestone.

244 CHAPTER 11 Web services