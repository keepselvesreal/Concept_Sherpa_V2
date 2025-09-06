# 11.4 Representing a server response as a map

**메타데이터:**
- ID: 107
- 레벨: 2
- 페이지: 255-258
- 페이지 수: 4
- 부모 ID: 102
- 텍스트 길이: 5919 문자

---

g a server response as a map 227
Joe Nice! You marked the elements in the fields array as enums and not as
strings. Where did you get the list of allowed values?
Theo Nancy gave me the list of the fields that she wants to expose to the users. Here,
let me show you her list.
Listing11.5 The important fields from the Open Library Books API
- title
- full_title
- subtitle
- publisher
- publish_date
- weight
- physical_dimensions
- number_of_pages
- subjects
- publishers
- genre
11.4 Representing a server response as a map
Joe What does the Open Library Books API look like?
Theo It’s quite straightforward. We create a GET request with the book ISBN, and it
gives us a JSON string with extended information about the book. Take a look
at this.
When Theo executes the code snippet, it displays a JSON string with the extended infor-
mation about 7 Habits of Highly Effective People.
Listing11.6 Fetching data from the Open Library Books API
fetchAndLog(
"https:/ /openlibrary.org/isbn/978-1982137274.json"
);
A utility function
//{
that fetches JSON
// "authors": [
and displays it to
// {
the console
// "key": "/authors/OL383159A",
// },
// {
// "key": "/authors/OL30179A",
// },
// {
// "key": "/authors/OL1802361A",
// },
// ],
// "created": {
// "type": "/type/datetime",
// "value": "2020-08-17T14:26:27.274890",
// },
// "full_title": "7 Habits of Highly Effective
// People : Revised and Updated Powerful
// Lessons in Personal Change",

228 CHAPTER 11 Web services
// "isbn_13": [
// "9781982137274",
// ],
// "key": "/books/OL28896586M",
// "languages": [
// {
// "key": "/languages/eng",
// },
// ],
// "last_modified": {
// "type": "/type/datetime",
// "value": "2021-09-08T19:07:57.049009",
// },
// "latest_revision": 3,
// "lc_classifications": [
// "",
// ],
// "number_of_pages": 432,
// "publish_date": "2020",
// "publishers": [
// "Simon & Schuster, Incorporated",
// ],
// "revision": 3,
// "source_records": [
// "bwb:9781982137274",
// ],
// "subtitle": "Powerful Lessons in Personal Change",
// "title": "7 Habits of Highly Effective
// People : Revised and Updated",
// "type": {
// "key": "/type/edition",
// },
// "works": [
// {
// "key": "/works/OL2629977W",
// },
// ],
//}
Joe Did Nancy ask for any special treatment of the fields returned by the API?
Theo Nothing special besides keeping only the fields I showed you.
Joe That’s it?
Theo Yes. For example, here’s the JSON string returned by the Open Library Books
API for 7 Habits of Highly Effective People after having kept only the necessary
fields.
Listing11.7 Open Library response for 7 Habits of Highly Effective People
{
"title":"7 Habits of Highly Effective People : Revised and Updated",
"subtitle":"Powerful Lessons in Personal Change",
"number_of_pages":432,
"full_title":"7 Habits of Highly Effective People : Revised and Updated

11.4 Representing a server response as a map 229
Powerful Lessons in Personal Change",
"publish_date":"2020",
"publishers":["Simon & Schuster, Incorporated"]
}
Theo Also, Nancy wants us to keep only the fields that appear in the client request.
Joe Do you know how to implement the double field filtering?
Theo Yeah, I’ll parse the JSON string from the API into a hash map, like we parsed a
client request, and then I’ll use _.pick twice to keep only the required fields.
Joe It sounds like a great plan to me. Can you code it, including validating the data
that is returned by the Open Library API?
Theo Sure! Let me first write the JSON schema for the Open Library API response.
Theo needs to refresh his memory with the materials about schema composition in order
to express the fact that either isbn_10 or isbn_13 are mandatory. After a few moments,
he shows the JSON schema to Joe.
Listing11.8 The JSON schema for the Open Library Books API response
var basicBookInfoSchema = {
"type": "object",
"required": ["title"],
"properties": {
"title": {"type": "string"},
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

230 CHAPTER 11 Web services
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
Theo Now, assuming that I have a fetchResponseBody function that sends a request
and retrieves the body of the response as a string, let me code up the how to do
the retrieval. Give me a sec.
Theo types away in his IDE for several minutes. He shows the result to Joe.
Listing11.9 Retrieving book information from the Open Library Books API
var ajv = new Ajv({allErrors: true});
class OpenLibraryDataSource {
static rawBookInfo(isbn) {
var url = `https:/ /openlibrary.org/isbn/${isbn}.json`;
var jsonString = fetchResponseBody(url);
Fetches JSON in
return JSON.parse(jsonString);
the body of a
}
response
static bookInfo(isbn, requestedFields) {
var relevantFields = ["title", "full_title",
"subtitle", "publisher",
"publish_date", "weight",
"physical_dimensions", "genre",
"subjects", "number_of_pages"];
var rawInfo = rawBookInfo(isbn);
if(!ajv.validate(bookInfoSchema, rawInfo)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from Open Books API: " +
errors;
}
var relevantInfo =
_.pick(_.pick(rawInfo, relevantFields), requestedFields);
return _.set(relevantInfo, "isbn", isbn);
}
}
 NOTE The JavaScript snippets of this chapter are written as if JavaScript were deal-
ing with I/O in a synchronous way. In real life, we need to use async and await around
I/O calls.