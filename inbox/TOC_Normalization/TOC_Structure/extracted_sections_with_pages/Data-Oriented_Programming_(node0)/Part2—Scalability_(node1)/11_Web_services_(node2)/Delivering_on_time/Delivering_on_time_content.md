# Delivering on time

**페이지**: 266-267
**계층**: Data-Oriented Programming (node0) > Part2—Scalability (node1) > 11 Web services (node2)
**추출 시간**: 2025-08-06 19:47:15

---


--- 페이지 266 ---

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

--- 페이지 266 끝 ---


--- 페이지 267 ---

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

--- 페이지 267 끝 ---
