# 12 Advanced data validation

**Level:** 1
**페이지 범위:** 275 - 299
**총 페이지 수:** 25
**ID:** 114

---

=== 페이지 275 ===
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

=== 페이지 276 ===
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

=== 페이지 277 ===
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

=== 페이지 278 ===
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

=== 페이지 279 ===
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

=== 페이지 280 ===
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

=== 페이지 281 ===
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

=== 페이지 282 ===
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

=== 페이지 283 ===
12.2 Return value validation 255
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

=== 페이지 284 ===
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

=== 페이지 285 ===
12.3 Advanced data validation 257
return bookInfos;
};
Theo Excellent! Now we need to figure out how to deal with advanced data validation.
12.3 Advanced data validation
Dave What do you mean by advanced data validation?
Theo I mean going beyond static types.
Dave Could you give me an example?
Theo Sure. Take, for instance, the publication year of a book. It’s an integer, but
what else could you say about this number?
Dave It has to be positive. It would say it’s a positive integer.
Theo Come on, Dave! Be courageous, go beyond types.
Dave I don’t know. I would say it’s a number that should be higher than 1900. I
don’t think it makes sense to have a book that is published before 1900.
Theo Exactly. And what about the higher limit?
Dave I’d say that the publication year should be less than the current year.
Theo Very good! I see that JSON Schema supports number ranges. Here is how we
can write the schema for an integer that represents a year and should be
between 1900 and 2021.
Listing12.12 The schema for an integer between 1900 and 2021
var publicationYearSchema = {
"type": "integer",
"minimum": 1900,
"maximum": 2021
};
Dave Why isn’t this kind of data validation possible in OOP?
Theo I’ll let you think about that for a moment.
Dave I think have it! In DOP, data validation is executed at run time, while static
type validation in OOP is executed at compile time. At compile time, we only
have information about static types; at run time, we have the data itself. That’s
why in DOP data validation, it’s possible to go beyond types.
 NOTE Of course, it’s also possible in traditional OOP to write custom run-time data
validation. Here, though, we are comparing data schema with static types.
Theo You got it! Now, let me show you how to write the schema for a string that
should match a regular expression.
 NOTE See http://mng.bz/OGNP for the JavaScript Guide to regular expressions.
Theo Let’s take for example the book ID. I am assuming it must be a UUID.
Dave Right.
Theo Can you write the regular expression for a valid UUID?

=== 페이지 286 ===
258 CHAPTER 12 Advanced data validation
Dave googles “UUID regex” and finds something he thinks just might work. He shows the
regular expression to Theo.
Listing12.13 The regular expression for a valid UUID
[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}
Dave Now, how do we plug a regular expression into a JSON Schema?
Theo While you were looking for the UUID regular expression, I read about the
pattern field. Here’s how we can plug the UUID regular expression into a
JSON Schema.
Listing12.14 The schema for a UUID
var uuidSchema = {
"type": "string",
"pattern": "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}" +
"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
};
Dave Nice! Let me improve the catalog schema and refine the schema for purchase-
Date, isbn, libId, and authorId with regular expressions.
Theo Before you do that, though, let me tell you something I read about regular
expressions: some of them are predefined. For example, there is a predefined
regular expression for dates.
Dave How does it work?
Theo With the help of the format field.
 NOTE According to JSON Schema specification, format is just for annotation and
doesn’t affect validation. But in practice, JSON Schema validation libraries use format
also for validation.
Theo moves to his laptop. He inputs the schema for a date and shows it to Dave.
Listing12.15 The schema for a date
{
"type": "string",
"format": "date"
}
TIP In DOP, data validation goes beyond static types (e.g., number ranges, regular
expressions, and so on).
Dave Very cool! Do I have all the information I need in order to refine the catalog
schema?
Theo Yes, go for it!
It takes Dave a bit of time to write the regular expressions for isbn, authorId, and libId.
But with the help of Google (again) and a bit of simplification, Dave comes up with the
schema in listings 12.16 and 12.17.

=== 페이지 287 ===
12.3 Advanced data validation 259
Listing12.16 The refined schema of the catalog data (Part 1)
var isbnSchema = {
"type": "string",
"pattern": "^[0-9-]{10,20}$"
};
var libIdSchema = {
"type": "string",
"pattern": "^[a-z0-9-]{3,20}$"
};
var authorIdSchema ={
"type": "string",
"pattern": "[a-z-]{2,50}"
};
var bookItemSchema = {
"type": "object",
"additionalProperties": {
"id": uuidSchema,
"libId": libIdSchema,
"purchaseDate": {
"type": "string",
"format": "date"
},
"isLent": {"type": "boolean"}
}
};
Listing12.17 The refined schema of the catalog data (Part 2)
var bookSchema = {
"type": "object",
"required": ["title", "isbn", "authorIds", "bookItems"],
"properties": {
"title": {"type": "string"},
"publicationYear": publicationYearSchema,
"isbn": isbnSchema,
"publisher": {"type": "string"},
"authorIds": {
"type": "array",
"items": authorIdSchema
},
"bookItems": bookItemSchema
}
};
var authorSchema = {
"type": "object",
"required": ["id", "name", "bookIsbns"],
"properties": {
"id": {"type": "string"},
"name": {"type": "string"},

=== 페이지 288 ===
260 CHAPTER 12 Advanced data validation
"bookIsbns": {
"items": isbnSchema
}
}
};
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
12.4 Automatic generation of data model diagrams
Before going home, Theo phones Joe to tell him about how he and Dave used data valida-
tion inside the system. Joe tells Theo that that’s exactly how he recommends doing it and
suggests he come and visit Theo and Dave at the office tomorrow. He wants to show them
some cool advanced stuff related to data validation. The next day, with coffee in hand, Joe
starts the discussion.
Joe Are you guys starting to feel the power of data validation à la DOP?
Dave Yes, it’s a bit less convenient to validate a JSON Schema than it is to write the
class of function arguments, but this drawback is compensated by the fact that
JSON Schema supports conditions that go beyond static types.
Theo We also realized that we don’t have to validate data for each and every function.
Joe Correct. Now, let me show you another cool thing that we can do with JSON
Schema.
Dave What’s that?
Joe Generate a data model diagram.
Dave Wow! How does that work?
Joe There are tools that receive a JSON Schema as input and produce a diagram in
a data model format.
Dave What is a data model format?
Joe It’s a format that allows you to define a data model in plain text. After that, you
can generate an image from the text. My favorite data format is PlantUML.
 NOTE For more on PlantUML, see https://plantuml.com/.
Dave Do you know of other tools that generate data model diagrams?
Joe I have used JSON Schema Viewer and Malli.

=== 페이지 289 ===
12.4 Automatic generation of data model diagrams 261
 NOTE You can find information on the JSON Schema Viewer at https://navneethg
.github.io/jsonschemaviewer/ and on Malli at https://github.com/metosin/malli.
Joe shows Dave and Theo the PlantUML diagram that Malli generated (listing 12.18) from
the catalog schema in listings 12.16 and 12.17.
Listing12.18 A PlantUML diagram generated from the catalog data schema
@startuml
Entity1 *-- Entity2
Entity1 *-- Entity4
Entity2 *-- Entity3
class Entity1 {
+ booksByIsbn: {Entity2}
+ authorsById: {Entity4}
}
class Entity2 {
+ title : String
+ publicationYear: Number
+ isbn: String
+ authorIds: [String]
+ bookItems: [Entity3]
}
class Entity3 {
+ id: String
+ libId: String
+ purchaseDate: String
+ isLent: Boolean
}
class Entity4 {
+ id: String
+ name: String
+ bookIsbns: [String]
}
@enduml
Dave Is it possible to visualize this diagram?
Joe Absolutely. Let me copy and paste the diagram text into the PlantText online
tool.
 NOTE See https://www.planttext.com/ for more on the PlantText online tool.
Dave opens his web browser and types the URL for PlantText. After copying and pasting
the text, he steps aside so that Theo and Dave can view the diagram that looks like the
image in figure 12.2.

=== 페이지 290 ===
262 CHAPTER 12 Advanced data validation
C Entity1
booksByIsbn: {Entity2}
authorsById: {Entity3}
C Entity2 C Entity4
title : String id: String
publicationYear: Number name: String
isbn: String booklsbns: [String]
authorlds: [String]
bookltems: [Entity3]
C Entity3
id: String
libld: String
Figure 12.2 A visualization of
purchaseDate: String
the PlantUML diagram generated
isLent: Boolean
from the catalog data schema
Dave That’s cool! But why are the diagram entities named Entity1, Entity2, and
so on?
Joe Because in JSON Schema, there’s no way to give a name to a schema. Malli has
to autogenerate random names for you.
Theo Also, I see that the extra information we have in the schema, like the number
range for publicationYear and string regular expression for isbn, is missing
from the diagram.
Joe Right, that extra information is not part of the data model. That’s why it’s not
included in the generated data model diagram.
Dave Anyway, it’s very cool!
Joe If you guys like the data model generation feature, I’m sure you’re going to
like the next feature.
Dave What’s it about?
Joe Automatic generation of unit tests.
Theo Wow, sounds exciting!
12.5 Automatic generation of schema-based unit tests
Joe Once you’ve defined a data schema for function arguments and for its return
value, it’s quite simple to generate a unit test for this function.
Dave How?
Joe Well, think about it. What’s the essence of a unit test for a function?
Dave A unit test calls a function with some arguments and checks whether the func-
tion returns the expected value.
Joe Exactly! Now, let’s adapt it to the context of data schema and DOP. Let’s say you
have a function with a schema for their arguments and for their return value.

=== 페이지 291 ===
12.5 Automatic generation of schema-based unit tests 263
Dave OK.
Joe Here’s the flow of a schema-based unit test. We call the function with random
arguments that conform to the schema of the function arguments. Then, we
check whether the function returns a value that conforms to the schema of the
return value. Here, let me diagram it.
Joe goes to the whiteboard. He draws the diagram in figure 12.3.
Generaterandom datathat conforms toinput schema
Execute the function The input
is random.
Yes No
Output conforms to output schema
Test passes Test fails
Figure 12.3 The flow of
a schema-based unit test
Dave How do you generate random data that conforms to a schema?
Joe Using a tool like JSON Schema Faker. For example, let’s start with a simple
schema: the schema for a UUID. Let me show you how to generate random
data that conforms to the schema.
 NOTE You’ll find more information about JSON Schema Faker at https://github
.com/json-schema-faker/json-schema-faker.
Joe types on the keyboard for a bit. He then shows the code to generate random data to
Dave and Theo.
Listing12.19 Generating random data that conforms to a UUID schema
var uuidSchema = {
"type": "string",
"pattern": "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}" +
"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
};
JSONSchemaFaker.generate(uuidSchema);
// → "7aA8CdF3-14DF-9EF5-1A19-47dacdB16Fa9"
Dave executes the code snippet a couple of times, and indeed, on each evaluation, it returns
a different UUID.
Dave Very cool! Let me see how it works with more complex schemas like the cata-
log schema.

=== 페이지 292 ===
264 CHAPTER 12 Advanced data validation
When Dave calls JSONSchemaFaker.generate with the catalog schema, he gets some
quite long random data. He’s a bit surprised by the results.
Listing12.20 Generating random data that conforms to the catalog schema
{
"booksByIsbn": {
"Excepteur7": {
"title": "elit veniam anim",
"isbn": "5419903-3563-7",
"authorIds": [
"vfbzqahmuemgdegkzntfhzcjhjrbgfoljfzogfuqweggchum",
"inxmqh-",
],
"bookItems": {
"ullamco5": {
"id": "f7dac8c3-E59D-bc2E-7B33-C27F3794E2d6",
"libId": "4jtbj7q7nrylfu114m",
"purchaseDate": "2001-08-01",
"isLent": false
},
"culpa_3e": {
"id": "423DCdDF-CDAe-2CAa-f956-C6cd9dA8054b",
"libId": "6wcxbh",
"purchaseDate": "1970-06-24",
"isLent": true
}
},
"publicationYear": 1930,
"publisher": "sunt do nisi"
},
"aliquip_d7": {
"title": "aute",
"isbn": "348782167518177",
"authorIds": ["owfgtdxjbiidsobfgvjpjlxuabqpjhdcqmmmrjb-ezrsz-u"],
"bookItems": {
"ipsum__0b": {
"id": "6DfE93ca-DB23-5856-56Fd-82Ab8CffEFF5",
"libId": "bvjh0p2p2666vs7dd",
"purchaseDate": "2018-03-30",
"isLent": false
}
},
"publisher": "ea anim ut ex id",
"publicationYear": 1928
}
},
"authorsById": {
"labore_b88": {
"id": "adipisicing nulla proident",
"name": "culpa in minim",
"bookIsbns": [
"6243029--7",
"5557199424742986"
]

=== 페이지 293 ===
12.5 Automatic generation of schema-based unit tests 265
},
"ut_dee": {
"id": "Lorem officia culpa qui in",
"name": "aliquip eiusmod",
"bookIsbns": [
"0661-8-5772"
]
}
}
}
Joe I see that you have some bugs in your regular expressions.
Theo How can you see that?
Joe Some of the generated ISBNs don’t seem to be valid ISBNs.
Dave You’re right. I hate regular expressions!
Joe Dave, I don’t think you’re the only one with that sentiment. Let me show you
how to implement the flow of a schema-based unit test for Catalog.search-
BooksByTitle.
Listing12.21 Implementation of the flow of a schema-based unit test
function searchBooksTest () {
var catalogRandom = JSONSchemaFaker.generate(catalogSchema);
var queryRandom = JSONSchemaFaker.generate({ "type": "string" });
Catalog.searchBooksByTitle(catalogRandom, queryRandom);
}
Dave Wait a moment. I can’t see where you check that Catalog.searchBooksBy-
Title returns a value that conforms to the return value schema.
Theo If you look closer at the code, you’ll see it.
Dave takes a closer look at the code for Catalog.searchBooksByTitle. Now he sees it.
Listing12.22 The implementation of Catalog.searchBooksByTitle
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

=== 페이지 294 ===
266 CHAPTER 12 Advanced data validation
if(dev()) {
if(!ajv.validate(searchBooksResponseSchema, bookInfos)) {
var errors = ajv.errorsText(ajv.errors);
throw ("searchBooksByTitle returned an invalid value: " +
errors);
}
}
return bookInfos;
};
Dave Of course! It’s in the code of Catalog.searchBooksByTitle. If the return
value doesn’t conform to the schema, it throws an exception, and the test fails.
Joe Correct. Now, let’s improve the code of our unit test and return false when
an exception occurs inside Catalog.searchBooksByTitle.
Joe edits the test code. He shows his changes to Theo and Dave.
Listing12.23 A complete data schema-based unit test for search books
function searchBooksTest () {
var catalogRandom = JSONSchemaFaker.generate(catalogSchema);
var queryRandom = JSONSchemaFaker.generate({ "type": "string" });
try {
Catalog.searchBooksByTitle(catalogRandom, queryRandom);
return true;
} catch (error) {
return false;
}
}
Dave Let me see what happens when I run the test.
Joe Before we run it, we need to fix something in your unit test.
Dave What?
Joe The catalog data and the query are random. There’s a good chance that no
books will match the query. We need to create a query that matches at least
one book.
Dave How are we going to find a query that’s guaranteed to match at least one book?
Joe Our query will be the first letter of the first book from the catalog data that is
generated.
Joe types for a bit and shows Theo and Dave his refined test. They are delighted that Joe is
taking the time to fix their unit test.
Listing12.24 A refined data schema-based unit test for search books
function searchBooksTest () {
var catalogRandom = JSONSchemaFaker.generate(catalogSchema);
var queryRandom = JSONSchemaFaker.generate({ "type": "string" });
try {
var firstBook = _.values(_.get(catalogRandom, "booksByIsbn"))[0];

=== 페이지 295 ===
12.5 Automatic generation of schema-based unit tests 267
var query = _.get(firstBook, "title").substring(0,1);
Catalog.searchBooksByTitle(catalogRandom, query);
return true;
} catch (error) {
return false;
}
}
Dave I see. It’s less complicated than what I thought. Does it happen often that you
need to tweak the random data?
Joe No, usually the random data is just fine.
Dave OK, now I’m curious to see what happens when I execute the unit test.
When Dave executes the unit test, it fails. His expression is one of bewilderment. Theo is
just astonished.
Listing12.25 Running the schema-based unit test
searchBooksTest();
// → false
Dave I think something’s wrong in the code of the unit test.
Theo Maybe the unit test caught a bug in the implementation of Catalog.search-
BooksByTitle.
Dave Let’s check it out. Is there a way to have the unit test display the return value of
the function?
Joe Yes, here it is.
Joe once again turns to his laptop to update the code. He shows the others his new unit
test that includes the return value for Catalog.searchBooksByTitle.
Listing12.26 Including the return value in the unit test output
function searchBooksTest () {
var catalogRandom = JSONSchemaFaker.generate(catalogSchema);
var queryRandom = JSONSchemaFaker.generate({ "type": "string" });
try {
var firstBook = _.values(_.get(catalogRandom, "booksByIsbn"))[0];
var query = _.get(firstBook, "title").substring(0,1);
Catalog.searchBooksByTitle(catalogRandom, query);
return true;
} catch (error) {
console.log(error);
return false;
}
}
Dave Now, let’s see what’s displayed when I again run the unit test.

=== 페이지 296 ===
268 CHAPTER 12 Advanced data validation
Listing12.27 Running the schema-based unit test again
searchBooksTest();
// → searchBooksByTitle returned a value that doesn\'t conform to schema:
// data[0].authorNames[0] should be string,
// data[0].authorNames[1] should be string,
// data[1].authorNames[0] should be string
Dave I think I understand what happened. In our random catalog data, the authors
of the books are not present in the authorByIds index. That’s why we have all
those undefineds in the values returned by Catalog.searchBooksByTitle,
whereas in the schema, we expect a string.
Theo How do we fix that?
Dave Simple. Have Catalog.authorNames return the string Not available when
an author doesn’t exist in the catalog. Maybe something like this.
Listing12.28 Fixing a bug in the search books implementation
Catalog.authorNames = function(catalogData, book) {
var authorIds = _.get(book, "authorIds");
var names = _.map(authorIds, function(authorId) {
return _.get(catalogData,
["authorsById", authorId, "name"],
"Not available");
When no value is associated with
});
the key ["authorsById", authorId,
return names;
"name"], we return "Not available".
};
Dave executes the unit test again. Thankfully, this time it passes.
Listing12.29 Running the schema-based unit test again
searchBooksTest();
// → true
Joe Well done, Dave!
Dave You were right. The automatically generated unit tests were able to catch a bug
in the implementation of Catalog.searchBooksByTitle.
Joe Don’t worry. The same thing has happened to me so many times.
Dave Data validation à la DOP is really cool!
Joe That’s just the beginning, my friend. The more you use it, the more you love it!
Dave I must admit, I still miss one cool IDE feature from OOP.
Joe Which one?
Dave The autocompletion of field names in a class.
Joe For the moment, field name autocompletion for data is only available in
Clojure via clj-kondo and the integration it provides with Malli.

=== 페이지 297 ===
12.6 A new gift 269
 NOTE See https://github.com/clj-kondo/clj-kondo and https://github.com/metosin/
malli for the autocompletion feature provided by clj-kondo and its integration with Malli.
Dave Do you think that someday this functionality will be available in other program-
ming languages?
Joe Absolutely. IDEs like IntelliJ and Visual Studio Code already support JSON
Schema validation for JSON files. It’s only a matter of time before they support
JSON Schema validation for function arguments and provide autocompletion
of the field names in a map.
Dave I hope it won’t take them too much time.
12.6 A new gift
When Joe leaves the office, Dave gets an interesting idea. He shares it with Theo.
Dave Do you think we could make our own JSON Schema cheat sheet with the
advanced JSON schema features that we discovered today?
Theo Excellent idea! But you’ll have to do it on your own. I have to run to a meeting!
After his meeting, Theo comes back to Dave’s desk. When he sees Theo, Dave takes a
small package like the one Joe gave Theo a few weeks ago from the top of his desk. This
one, however, is wrapped in a light blue ribbon. With a solemn demeanor, Dave hands
Theo the gift.
When Theo undoes the ribbon, he discovers an stylish piece of paper decorated with lit-
tle computers in different colors. In the center of the paper, he reads the inscription,
“Advanced JSON Schema cheat sheet.” Theo smiles while browsing the JSON schema (see
listing 12.30). Then, he turns the paper over to find that the back is also filled with draw-
ings, this time keyboards and mice. In the center of the paper, Theo reads the inscription,
“Example of valid data” (see listing 12.31).
Listing12.30 Advanced JSON Schema cheat sheet
The { At the root level,
properties "type": "array", data is an array.
of each "items": {
field in the "type": "object", Each element of the
map "properties": { array is a map. myEnum is an
"myNumber": {"type": "number"}, enumeration value
myNumber "myString": {"type": "string"}, with two possibilities,
is a number. "myEnum": {"enum": ["myVal", "yourVal"]}, "myVal" and "yourVal".
"myBool": {"type": "boolean"}
myBool is
myString is "myAge": {
myAge is a boolean.
a string. "type": "integer",
an integer
"minimum": 0, between 0
"maximum": 120 and 120.
},
"myBirthday": {
myBirthday is a string
"type": "string",
conforming to the date
"format": "date"
format.
},

=== 페이지 298 ===
270 CHAPTER 12 Advanced data validation
"myLetters": {
myLetters is a string with
"type": "string",
letters only (lowercase or
"pattern": "[a-zA-Z]*"
uppercase).
}
"myNumberMap": {
myNumberMap is an homogeneous
"type": "object",
string map where all the values are
"additionalProperties": {"type": "number"}
numbers.
},
"myTuple": {
myTuple is a tuple where the first
"type": "array",
element is a string and the second
"prefixItems": [
element is a number.
{ "type": "string" },
{ "type": "number" }
]
} The mandatory fields in the map
are myNumber and myString.
},
Other fields are optional.
"required": ["myNumber", "myString"],
"additionalProperties": false
We don’t allow fields that
}
are not explicitly mentioned
}
in the schema.
Listing12.31 An example of valid data
[
{
"myNumber": 42,
"myString": "I-love-you",
"myEnum": "myVal",
"myBool": true,
"myTuple": ["Hello", 42]
},
{
"myNumber": 54,
"myString": "Happy",
"myAge": 42,
"myBirthday": "1978-11-23",
"myLetters": "Hello",
"myNumberMap": {
"banana": 23,
"apple": 34
}
}
]
Summary
 We define data schemas using a language like JSON Schema for function argu-
ments and return values.
 Function argument schemas allow developers to figure out the expected shape of
the function arguments they want to call.
 When invalid data is passed, data validation third-party libraries give meaning-
ful errors with detailed information about the data parts that are not valid.

=== 페이지 299 ===
Summary 271
 Unlike data validation at system boundaries, data validation inside the system is
supposed to run only at development time and should be disabled in production.
 We visualize a data schema by generating a data model diagram out of a JSON
Schema.
 For functions that have data schemas for their arguments and return values, we
can automatically generate schema-based unit tests.
 Data validation is executed at run time.
 We can define advanced data validation conditions that go beyond static types,
like checking whether a number is within a range or if a string matches a regu-
lar expression.
 Data validation inside the system should be disabled in production.
 Records are represented as heterogeneous maps, and indexes are represented as
homogeneous maps.
 When you define a complex data schema, it is advised to store nested schemas
in variables to make the schemas easier to read.
 We treat data validation like unit tests.
