# 12.1 Function arguments validation

**메타데이터:**
- ID: 116
- 레벨: 2
- 페이지: 276-282
- 페이지 수: 7
- 부모 ID: 114
- 텍스트 길이: 12741 문자

---

guments validation
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

250 CHAPTER 12 Advanced data validation
Theo Dave, please remind me of the expected shapes for catalogData and query.
Dave Sure. query should be a string, and catalogData should be a map that con-
forms to the catalog data model.
Theo What is the catalog data model?
Dave Let me see. I have seen a diagram of it somewhere.
Dave rummages around a bit in his folder for Klafim’s Library Management System. Find-
ing what he’s looking for, he draws the diagram in figure 12.1 on the whiteboard.
C Catalog
booksByIsbn: {Book}
authorsById: {Author}
C Book
C Author
title : String
publicationYear: Number id: String
isbn: String name: String
authorlds: [String] booklsbns: [String]
bookltems: [Bookltem]
C Bookltem
id: String
libld: String
purchaseDate: String
isLent: Boolean
Figure 12.1 The catalog data model
 NOTE The schemas for this book use JSON Schema version 2020-12.
Theo Can you write a JSON Schema for the catalog data model?
Dave Am I allowed to use internal variables for book and author schemas, or do I
have to nest all the schemas inside the catalog schema?
Theo JSON Schema is part of the code. If you feel that using internal variables would
make the code more readable, go for it.
Dave OK. Now I need the JSON Schema gift that Joe gave you.
Theo picks up a well-worn piece of paper that is a bit torn and quite wrinkled. He gives
Dave the JSON Schema cheat sheet.
Listing12.2 JSON Schema cheat sheet
At the root level,
{
data is an array.
"type": "array",
"items": { Each element of the array is a map.
"type": "object",
The properties of each field in the map
"properties": {

12.1 Function arguments validation 251
"myNumber": {"type": "number"},
myNumber
"myString": {"type": "string"}, myEnum is an enumeration
is a number.
"myEnum": {"enum": ["myVal", "yourVal"]}, value with two possibilities,
myString is "myBool": {"type": "boolean"} "myVal" and "yourVal".
a string. },
"required": ["myNumber", "myString"], myBool is a boolean.
"additionalProperties": false
} The mandatory fields in the map
} We don’t allow fields that are not are myNumber and myString.
explicitly mentioned in the schema. Other fields are optional.
Dave I think I’ll start with the author schema. It seems simpler than the book schema.
Quickly composing the code, Dave shows Theo the author schema. Dave, still new to DOP,
looks for Theo’s reaction.
Listing12.3 The author schema
var authorSchema = {
"type": "object",
"required": ["id", "name", "bookIsbns"],
"properties": {
"id": {"type": "string"},
"name": {"type": "string"},
"bookIsbns": {
"type": "array",
"items": {"type": "string"}
}
}
};
Theo Well done! Let’s move on to the book schema now.
Dave I think I am going to store the book item schema in a variable.
Listing12.4 The book item schema
var bookItemSchema = {
"type": "object",
"properties":{
"id": {"type": "string"},
"libId": {"type": "string"},
"purchaseDate": {"type": "string"},
"isLent": {"type": "boolean"}
},
"required": ["id", "libId", "purchaseDate", "isLent"]
};
var bookSchema = {
"type": "object",
"required": ["title", "isbn", "authorIds", "bookItems"],
"properties": {
"title": {"type": "string"},
"publicationYear": {"type": "integer"},

252 CHAPTER 12 Advanced data validation
"isbn": {"type": "string"},
"authorIds": {
"type": "array",
"items": {"type": "string"}
},
"bookItems": {
"type": "array",
"items": bookItemSchema
}
}
};
TIP When you define a complex data schema, it is advisable to store nested schemas
in variables to make the schemas easier to read.
Theo Why didn’t you include publicationYear in the list of required fields in the
book schema?
Dave Because, for some books, the publication year is missing. Unlike in OOP, it will
then be easy to deal with nullable fields.
Theo Excellent! And now, please tackle the final piece, the catalog schema.
Dave Here I have a problem. The catalog should be a map with two fields, books-
ByIsbn and authorsById. Both values should be indexes, represented in the
model diagram with curly braces. I have no idea how to define the schema for
an index.
Theo Do you remember how we represent indexes in DOP?
Dave Yes, indexes are represented as maps.
Theo Right, and what’s the difference between those maps and the maps that we use
for records?
Dave For records, we use maps where the names of the fields are known and the val-
ues can have different shapes. For indexes, we use maps where the names of
the fields are unknown and the values have a common shape.
Theo Right. We call the maps for records heterogeneous maps and the maps for
indexes homogeneous maps.
TIP In DOP, records are represented as heterogeneous maps, whereas indexes are repre-
sented as homogeneous maps.
Dave Then how do we define the schema of an homogeneous map in JSON Schema?
Theo I don’t know. Let’s check the JSON Schema online documentation.
 NOTE See https://json-schema.org/ to access the online documentation for JSON
Schema version 2020-12.
After a couple of minutes of digging into the JSON Schema online documentation, Theo
finds a piece about additionalProperties. He studies the information for a while before
making up his mind.

12.1 Function arguments validation 253
Theo I think we could use additionalProperties. Here’s the JSON Schema for an
homogeneous map where the values are numbers.
Listing12.5 The JSON Schema for an homogeneous map with values as numbers
{
"type": "object",
"additionalProperties": {"type": "number"}
}
Dave I thought that additionalProperties was supposed to be a boolean and that
it was used to allow or forbid properties not mentioned in the schema.
Theo That’s correct. Usually additionalProperties is a boolean, but the documen-
tation says it could also be a map that defines a schema. In that case, it means
properties not mentioned in the schema should have the value of the schema
associated with additionalProperties.
Dave I see. But what does that have to do with homogeneous maps?
Theo Well, a homogeneous map could be seen as a map with no predefined proper-
ties, where all the additional properties are of an expected type.
Dave Tricky!
TIP In JSON Schema, homogeneous string maps have type: object with no
properties and additionalProperties associated to a schema.
Theo Indeed. Now, let me show you what the catalog schema looks like.
Theo types briefly on his laptop. He shows Dave the catalog schema.
Listing12.6 The schema for catalog data
var catalogSchema = {
"type": "object",
"properties": {
"booksByIsbn": {
"type": "object",
"additionalProperties": bookSchema
},
"authorsById": {
"type": "object",
"additionalProperties": authorSchema
}
},
"required": ["booksByIsbn", "authorsById"]
};
Dave Are we ready to plug the catalog and the query schema into the Catalog
.searchBooksByTitle implementation?
Theo We could, but I think we can do better by defining a single schema that com-
bines both the catalog and query schemas.
Dave How would we combine two schemas into a single schema?

254 CHAPTER 12 Advanced data validation
Theo Do you know what a tuple is?
Dave I think I know, but I can’t define it formally.
Theo A tuple is an array where the size is fixed, and the elements can be of different
shapes.
Dave OK. So, how do we define tuples in JSON Schema?
Once again, Theo explores the JSON Schema online documentation. Fortunately, he has
bookmarked the page, and in no time at all, finds the information he needs.
Theo I found it! We use prefixItems in the definition of a tuple made of a string
and a number, for instance.
Theo types more code on his laptop. When he finishes, he shows Dave the schema for a
tuple.
Listing12.7 The schema for a tuple made of a string and a number
{
"type": "array",
"prefixItems": [
{ "type": "string" },
{ "type": "number" }
]
}
Dave I see. And how would you define the schema for the arguments of Catalog
.searchBooksByTitle?
Theo Well, it’s a tuple of size 2, where the first element is a catalog and the second
element is a string.
Dave Something like this schema?
Listing12.8 The schema for the arguments of Catalog.searchBooksByTitle
var searchBooksArgsSchema = {
"type": "array",
"prefixItems": [
catalogSchema,
{ "type": "string" },
]
};
Theo Exactly!
Dave Now that we have the schema for the arguments, how do we plug it into the
implementation of search books?
Theo That’s similar to the way we validate data at system boundaries. The main dif-
ference is that the data validation for data that flows inside the system should
run only at development time, and it should be disabled when the code runs in
production.
Dave Why?