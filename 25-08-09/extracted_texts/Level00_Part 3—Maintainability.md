# Part 3—Maintainability

**Level:** 0
**페이지 범위:** 273 - 360
**총 페이지 수:** 88
**ID:** 112

---

=== 페이지 273 ===
Part 3
Maintainability
A
fter a month, the Klafim project enters what Alabatross calls the mainte-
nance phase. Small new features need to be added on a weekly basis. Bugs need to be
fixed; nothing dramatic....
Monica, Theo’s boss, decides to allocate Dave to the maintenance of the Klafim
project. It makes sense. Over the last few months, Dave has demonstrated a great atti-
tude of curiosity and interest, and he has solid programming skills. Theo sets up a
meeting with Joe and Dave, hoping that Joe will be willing to teach DOP to Dave so
that he can continue to advance the good work he’s already done on Klafim. Theo
and Dave place a conference call to Joe.
Theo Hi, Joe. Will you have time over the next few weeks to teach Dave the
principles of DOP?
Joe Yes, but I prefer not to.
Dave Why? Is it because I don’t have enough experience in software develop-
ment? I can guarantee you that I’m a fast learner.
Joe It has nothing to do with your experience, Dave.
Theo Why not then?
Joe Theo, I think that you could be a great mentor for Dave.
Theo But, I don’t even know all the parts of DOP!
Dave Come on! No false modesty between us, my friend.
Joe Knowledge is never complete. As the great Socrates used to say, “The more
I know, the more I realize I know nothing.” I’m confident you will be able
to learn the missing parts by yourself and maybe even invent some.
Theo How will I be able to invent missing parts?

=== 페이지 274 ===
246 PART 3 Maintainability
Joe You see, DOP is such a simple paradigm that it’s fertile material for innovation.
Part of the material I taught you I learned from others, and part of it was an
invention of mine. If you keep practicing DOP, I’m quite sure you, too, will
come up with some inventions of your own.
Theo What do you say Dave? Are you willing to learn DOP from me?
Dave Definitely!
Theo Joe, will you be continue to be available if we need your help from time to time?
Joe Of course!

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

=== 페이지 300 ===
Polymorphism
Playing with the animals
in the countryside
This chapter covers
 Mimicking objects with multimethods (single
dispatch)
 Implementing multimethod on several argument
types (multiple dispatch)
 Implementing multimethods dynamically on
several arguments (dynamic dispatch)
OOP is well-known for allowing different classes to be called with the same inter-
face via a mechanism called polymorphism. It may seem that the only way to have
polymorphism in a program is with objects. In fact, in this chapter, we are going to
see that it is possible to have polymorphism without objects, thanks to multimeth-
ods. Moreover, multimethods provide a more advanced polymorphism than OOP
polymorphism because they support cases where the chosen implementation
depends on several argument types (multiple dispatch) and even on the dynamic
value of the arguments (dynamic dispatch).
272

=== 페이지 301 ===
13.1 The essence of polymorphism 273
13.1 The essence of polymorphism
For today’s session, Dave has invited Theo to come and visit him at his parents’ house in
the countryside. As Theo’s drive across the Golden Gate Bridge takes him from the freeway
to increasingly rural country roads, he lets himself be carried away by the beauty of the
landscape, the smell of fresh earth, and the sounds of animals in nature. This “nature
bath” puts him in an excellent mood. What a way to start the week!
Dave receives Theo in jeans and a T-shirt, a marked contrast with the elegant clothes he
wears at the office. A straw hat completes his country look. Theo says hello to Dave’s par-
ents, now retired. Dave suggests that they go pick a few oranges in the field to squeeze for
juice. After drinking a much more flavorful orange juice than they are used to in San Fran-
cisco, Theo and Dave get to work.
Dave When I was waiting for you this morning, I thought of another thing I miss
from OOP.
Theo What’s that?
Dave Polymorphism.
Theo What kind of polymorphism?
Dave You know, you define an interface, and different classes implement the same
interface in different ways.
Theo I see. And why do you think polymorphism is valuable?
Dave Because it allows us to decouple an interface from its implementations.
Theo Would you mind illustrating that with a concrete example?
Dave Sure. Because we’re in the country, I’ll use the classic OOP polymorphism
example with animals.
Theo Good idea!
Dave Let’s say that each animal has its own greeting by making a sound and saying
its name.
Theo Oh cool, like in anthropomorphic comics books.
Dave Anthro what?
Theo You know, comics books where animals can walk, speak, and so forth—like
Mickey Mouse.
Dave Of course, but I don’t know that term. Where does it come from?
Theo Anthropomorphism comes from the Greek ánthro–pos, which means human, and
morphe–, which means form.
Dave I see. So an anthropomorphic book is a book where animals have human traits.
The word sounds related to polymorphism.
Theo Absolutely. Polymorphism comes from the Greek polús, which means many, and
morphe–, which, again, means form.
Dave That makes sense. Polymorphism is the ability of different objects to imple-
ment the same method in different ways. That brings me back to my animal
example. In OOP, I’d define an IAnimal interface with a greet method, and
each animal class would implement greet in its own way. Here, I happen to
have an example.

=== 페이지 302 ===
274 CHAPTER 13 Polymorphism
Listing13.1 OOP polymorphism illustrated with animals
interface IAnimal {
public void greet();
}
class Dog implements IAnimal {
private String name;
public void greet() {
System.out.println("Woof woof! My name is " + animal.name);
}
}
class Cat implements IAnimal {
private String name;
public void greet() {
System.out.println("Meow! I am " + animal.name);
}
}
class Cow implements IAnimal {
private String name;
public void greet() {
System.out.println("Moo! Call me " + animal.name);
}
}
Theo Let me challenge you a bit. What is the fundamental difference between OOP
polymorphism and a switch statement?
Dave What do you mean?
Theo I could, for instance, represent an animal with a map having two fields, name
and type, and call a different piece of code, depending on the value of type.
Theo pulls his laptop from its bag and fires it up. While the laptop is booting up, he enjoys
another taste of that wonderful orange juice. When the laptop is ready, he quickly types in
the example switch case. Meanwhile, Dave has finished his glass of orange juice.
Listing13.2 A switch case where behavior depends on type
function greet(animal) {
switch (animal.type) {
case "dog":
console.log("Woof Woof! My name is: " + animal.name);
break;
case "cat":
console.log("Meow! I am: " + animal.name);
break;
case "cow":
console.log("Moo! Call me " + animal.name);
break;
};
}

=== 페이지 303 ===
13.1 The essence of polymorphism 275
Dave How would animal look, exactly?
Theo Like I just said, a map with two fields: name and type. Let me input that for you.
Listing13.3 Representing animals with maps
var myDog = {
"type": "dog",
"name": "Fido"
};
var myCat = {
"type": "cat",
"name": "Milo"
};
var myCow = {
"type": "cow",
"name": "Clarabelle"
};
Dave Could you have given another name to the field that holds the animal type?
Theo Absolutely. It could be anything.
Dave I see. You’re asking me the fundamental difference between your code with a
switch statement and my code with an interface and three classes?
Theo Exactly.
Dave First of all, if you pass an invalid map to your greet function, bad things will
happen.
Theo You’re right. Let me fix that and validate input data.
Listing13.4 Data validation
var animalSchema = {
"type": "object",
"properties": {
"name": {"type": "string"},
"type": {"type": "string"}
},
"required": ["name", "type"],
};
See chapter 12 about
data validation for
function greet(animal) {
details.
if(dev()) {
if(!ajv.validate(animalSchema, animal)) {
var errors = ajv.errorsText(ajv.errors);
throw ("greet called with invalid arguments: " + errors);
}
}
switch (animal.type) {
case "dog":

=== 페이지 304 ===
276 CHAPTER 13 Polymorphism
console.log("Woof Woof! My name is: " + animal.name);
break;
case "cat":
console.log("Meow! I am: " + animal.name);
break;
case "cow":
console.log("Moo! Call me " + animal.name);
break;
};
}
 NOTE You should not use switch statements like this in your production code.
We use them here for didactic purposes only as a step towards distilling the essence of
polymorphism.
Dave Another drawback of your approach is that when you want to modify the
implementation of greet for a specific animal, you have to change the code
that deals with all the animals, while in my approach, you would change only a
specific animal class.
Theo I agree, and I could also fix that by having a separate function for each animal,
something like this.
Listing13.5 Different implementations in different functions
function greetDog(animal) {
console.log("Woof Woof! My name is: " + animal.name);
}
function greetCat(animal) {
console.log("Meow! I am: " + animal.name);
}
function greetCow(animal) {
console.log("Moo! Call me " + animal.name);
}
function greet(animal) {
if(dev()) {
if(!ajv.validate(animalSchema, animal)) {
var errors = ajv.errorsText(ajv.errors);
throw ("greet called with invalid arguments: " + errors);
}
}
switch (animal.type) {
case "dog":
greetDog(animal);
break;
case "cat":
greetCat(animal);
break;
case "cow":
greetCow(animal);

=== 페이지 305 ===
13.2 Multimethods with single dispatch 277
break;
};
}
Dave But what if you want to extend the functionality of greet and add a new animal?
Theo Now you got me. I admit that with a switch statement, I can’t add a new animal
without modifying the original code, whereas in OOP, I can add a new class
without having to modify the original code.
Dave Yeah, but you helped me to realize that the main benefit of polymorphism is
that it makes the code easily extensible.
TIP The main benefit of polymorphism is extensibility.
Theo I’m going to ask Joe if there’s a way to benefit from polymorphism without
objects.
Theo sends a message to Joe and asks him about polymorphism in DOP. Joe answers that
he doesn’t have time to get into a deep response because he is in a tech conference where
he is about to give a talk about DOP. The only thing he has time to tell Theo is that he
should take a look at multimethods.
Theo and Dave read some online material about multimethods. It doesn’t look too
complicated. They decide that after lunch they will give multimethods a try.
13.2 Multimethods with single dispatch
During lunch, Theo asks Dave how it feels to have grown up in the country. Dave starts
with an enthusiastic description about being in direct contact with nature and living a sim-
pler life than in the city. He’s grateful for the experience, but he admits that country life
can sometimes be hard without the conveniences of the city. But who said simple was easy?
After lunch, they decide to have coffee. Dave asks Theo if he’d like to grind the coffee
beans himself. Theo accepts with joy. Next, Dave explains how to use a French press coffee
maker to get the ideal tradeoff between bitterness and rich taste. While savoring their
French press coffee in the garden, Theo and Dave continue their exploration of polymor-
phism à la DOP.
Theo From what I read before lunch, it seems that multimethods are a software con-
struct that provide polymorphism without the need for objects.
Dave I don’t get how that’s possible.
Theo Multimethods have two parts: a dispatch function and a set of methods that
provide an implementation for each dispatched value.
Dave I’m not sure I’m clear on that. Is a dispatch function like an interface?
Theo It’s like an interface in the sense that it defines the way the function needs to
be called, but it goes beyond that. It also dispatches a value that differentiates
between the different implementations.
Dave That’s a bit abstract for me.
Theo I think I understand how to implement the animal greeting capabilities. If we
use a multimethod called greet, we need a dispatch function and three
methods. Let’s call the dispatch function greetDispatch. It dispatches the
animal type, either "dog", "cat", or "cow". Then, each dispatch value is

=== 페이지 306 ===
278 CHAPTER 13 Polymorphism
handled by a specific method: "dog" by greetDog, "cat" by greetCat, and
"cow" by greetCow.
Theo takes out his notebook and opens it to a blank piece of paper. He draws a diagram
like the one in figure 13.1.
"dog" greetDog
Greet as a dog
greetDispatch "cat" greetCat
Emit the animal type Greet as a cat
animal
type, name "cow" greetCow
Greet as a cow
Figure 13.1 The logic flow
of the greet multimethod
Dave Why is there an arrow between animal and the methods, in addition to the
arrows between animal and the dispatch functions?
Theo Because the arguments of a multimethod are passed to the dispatch function
and to the methods.
TIP The arguments of a multimethod are passed to the dispatch function and to the
methods.
Dave Arguments plural?... I see only a single argument.
Theo You’re right. Right now our multimethod only receives a single argument, but
soon it will receive several arguments.
Dave I see. Could you show me how to write the code for the greet multimethod?
Theo For that, we need a library. For instance, in JavaScript, the arrows/multi-
method library provides an implementation of multimethods. Basically, we call
multi to create a multimethod called method to add a method.
 NOTE See http://mng.bz/nY9v for examples and documentation about this library.
Dave Where should we start?
Theo We’ll start with multimethod initialization by creating a dispatch function
greetDispatch that defines the signature of the multimethod, validates the
arguments, and emits the type of the animal. Then we’ll pass greetDispatch
to multi in order to create the greet multimethod. Our dispatch function
would then look like this.
Listing13.6 The dispatch function for greet multimethod
function greetDispatch(animal) {
Signature definition
if(dev()) {

=== 페이지 307 ===
13.2 Multimethods with single dispatch 279
if(!ajv.validate(animalSchema, animal)) {
Argument validation
var errors = ajv.errorsText(ajv.errors);
throw ("greet called with invalid arguments: " + errors);
}
}
Dispatch value
return animal.type;
}
Multimethod
initialization
var greet = multi(greetDispatch);
TIP A multimethod dispatch function is responsible for three things: it defines the sig-
nature of the multimethod, it validates the arguments, and it emits a dispatch value.
Dave What’s next?
Theo Now we need to implement a method for each dispatched value. Let’s start
with the method that deals with dogs. We create a greetDog function that
receives an animal and then add a dog method to the greet multimethod
using the method function from the arrows/multimethod library. The method
function receives two arguments: the dispatched value and a function that cor-
responds to the dispatch value.
Listing13.7 Implementation of greet method for dogs
function greetDog(animal) {
Method
console.log("Woof woof! My name is " + animal.name);
implementation
}
greet = method("dog", greetDog)(greet);
Method declaration
Dave Does the method implementation have to be in the same module as the multi-
method initialization?
Theo No, not at all! Method declarations are decoupled from multimethod initializa-
tion exactly like class definitions are decoupled from the interface definition.
That’s what make multimethods extensible.
TIP Multimethods provides extensibility by decoupling between multimethod initial-
ization and method implementations.
Dave What about cats and cows?
Theo We add their method implementations like we did for dogs.
Theo takes a moment to envision the implementation. Then he codes up two more greet
methods for cats and cows.
Listing13.8 Implementation of greet method for cats
function greetCat(animal) {
console.log("Meow! I am " + animal.name);
}
greet = method("cat", greetCat)(greet);

=== 페이지 308 ===
280 CHAPTER 13 Polymorphism
Listing13.9 Implementation of greet method for cows
function greetCow(animal) {
console.log("Moo! Call me " + animal.name);
}
greet = method("cow", greetCow)(greet);
TIP In the context of multimethods, a method is a function that provides an imple-
mentation for a dispatch value.
Dave Are the names of dispatch functions and methods important?
Theo According to what I read, not really, but I like to follow a simple naming con-
vention: use the name of the multimethod (for example, greet) as a prefix for
the dispatch function (for example, greetDispatch) and the methods. Then
I’d have the Dispatch suffix for the dispatch function and a specific suffix for
each method (for example, greetDog, greetCat, and greetCow).
Dave How does the multimethod mechanism work under the hood?
Theo Internally, a multimethod maintains a hash map where the keys are the dis-
patched values, and the values are the methods. When we add a method, an
entry is added to the hash map, and when we call the multimethod, we query the
hash map to find the implementation that corresponds to the dispatched value.
Dave I don’t think you’ve told me yet how to call a multimethod.
Theo We call it as a regular function. Give me a minute, and I’ll show you an exam-
ple that calls a multimethod.
Listing13.10 Calling a multimethod like a regular function
greet(myDog);
// → "Woof woof! My name is Fido"
greet(myCat);
// → "Meow! I am Milo"
greet(myCow);
// → "Moo! Call me Clarabelle"
TIP Multimethods are called like regular functions.
Dave You told me earlier that in the dispatch function, we should validate the argu-
ments. Is that mandatory or is it a best practice?
Theo It’s a best practice.
Dave What happens if the dispatch function doesn’t validate the arguments, and we
pass an invalid argument?
Theo Like when an animal has no corresponding method?
Dave Exactly!
Theo In that case, you’ll get an error. For instance, the arrows/multimethods library
throws a NoMethodError exception.
Dave That’s annoying. Is there a way to provide a default implementation?

=== 페이지 309 ===
13.3 Multimethods with multiple dispatch 281
Theo Absolutely! In order to define a default implementation, you pass to method—
as a single argument—the function that provides the default implementation.
Theo writes the code and shows it to Dave. Dave then tests Theo’s code and seems satisfied
with the result.
Listing13.11 Defining a default implementation
function greetDefault(animal) {
console.log("My name is " + animal.name);
}
greet = method(greetDefault)(greet);
Listing13.12 Calling a multimethod when no method fits the dispatch value
var myHorse = {
"type": "horse",
"name": "Horace"
};
greet(myHorse);
// → "My name is Horace"
TIP Multimethods support default implementations that are called when no method
corresponds to the dispatch value.
Dave Cool!
13.3 Multimethods with multiple dispatch
Theo So far, we’ve mimicked OOP by having the type of the multimethod argument
as a dispatch value. But if you think again about the flow of a multimethod,
you’ll discover something interesting. Would you like to try and draw a dia-
gram that describes the flow of a multimethod in general?
Dave Let me get a fresh napkin. The one under my glass is a bit wet.
Theo Uh, Dave, you can use my notebook.
It takes Dave a few minutes to draw a diagram like the one in figure 13.2. He pushes the
notebook back to Theo.
Value1 Method1
Handle case 1
Dispatch function Value3 Method3
Emit a dispatch value Handle case 3
args
Value2 Method2
Handle case 2
Figure 13.2 The logic flow
of multimethods

=== 페이지 310 ===
282 CHAPTER 13 Polymorphism
Theo Excellent! I hope you see that the dispatch function can emit any value.
Dave Like what?
Theo Like emitting the type of two arguments!
Dave What do you mean?
Theo Imagine that our animals are polyglot.
Dave Poly what?
Theo Polyglot comes from the Greek polús, meaning much, and from glôssa, meaning
language. A polyglot is a person who can speak many languages.
Dave What languages would our animals speak?
Theo I don’t know. Let’s say English and French.
Dave OK, and how would we represent a language in our program?
Theo With a map, of course!
Dave What fields would we have in a language map?
Theo Let’s keep things simple and have two fields: type and name.
Dave Like an animal map?
Theo Not exactly. In a language map, the type field must be either fr for French or en
for English, whereas in the animal map, the type field is either dog, cat, or cow.
Dave Let me try to write the language map schema and the two language maps.
Theo gladly consents; his French press coffee is getting cold! Dave writes his implementa-
tion of the code and shows Theo.
Listing13.13 The schema of a language map
var languageSchema = {
"type": "object",
"properties": {
"name": {"type": "string"},
"type": {"type": "string"}
},
"required": ["name", "type"],
};
Listing13.14 Two language maps
var french = {
"type": "fr",
"name": "Français"
};
var english = {
"type": "en",
"name": "English"
};
Theo Excellent! Now, let’s write the code for the dispatch function and the methods
for our polyglot animals. Let’s call our multimethod, greetLang. We have one
dispatch function and six methods.

=== 페이지 311 ===
13.3 Multimethods with multiple dispatch 283
Dave Right, three animals (dog, cat, and cow) times two languages (en and fr).
Before the implementation, I’d like to draw a flow diagram. It will help me to
make things crystal clear.
Theo You need my notebook again?
Not waiting for Dave to respond, Theo pushes his notebook across the table to Dave. Dave
draws a diagram like the one in figure 13.3 and slides the notebook back to Theo.
["dog", "en"] greetLangDogEn
Greet as a dog in English
["cat", "en"] greetLangCatEn
Greet as a cat in English
["cow", "en"] greetLangCowEn
Greet as a cow in English
args greetLangDispatch
animal, language Emit the animal and the language types
["dog", "fr"] greetLangDogFr
Greet as a dog in French
["cat", "fr"] greetLangCatFr
Greet as a cat in French
["cow", "fr"] greetLangCowFr
Greet as a cow in French
Figure 13.3 The logic flow of the greetLang multimethod
Theo Why did you omit the arrow between the arguments and the methods?
Dave In order to keep the diagram readable. Otherwise, there would be too many
arrows.
Theo OK, I see. Are you ready for coding?
Dave Yes!
Theo The dispatch function needs to validate its arguments and return an array with
two elements: the type of animal and the type of language.
Dave types for a bit on his laptop. He initializes the multimethod with a dispatch function
that returns the type of its arguments and then shows the code to Theo.
Listing13.15 Initializing a multimethod with a dispatch function
var greetLangArgsSchema = {
"type": "array",
"prefixItems": [animalSchema, languageSchema]
};
function greetLangDispatch(animal, language) {
if(dev()) {

=== 페이지 312 ===
284 CHAPTER 13 Polymorphism
if(!ajv.validate(greetLangArgsSchema, [animal, language])) {
throw ("greetLang called with invalid arguments: " +
ajv.errorsText(ajv.errors));
}
}
return [animal.type, language.type];
};
var greetLang = multi(greetLangDispatch);
Dave Does the order of the elements in the array matter?
Theo It doesn’t matter, but it needs to be consistent with the wiring of the methods.
The implementation of greetLang would therefore look like this.
Listing13.16 The implementation of greetLang methods
function greetLangDogEn(animal, language) {
console.log("Woof woof! My name is " +
animal.name +
" and I speak " +
language.name);
}
greetLang = method(["dog", "en"], greetLangDogEn)(greetLang);
function greetLangDogFr(animal, language) {
console.log("Ouaf Ouaf! Je m'appelle " +
animal.name +
" et je parle " +
language.name);
}
greetLang = method(["dog", "fr"], greetLangDogFr)(greetLang);
function greetLangCatEn(animal, language) {
console.log("Meow! I am " +
animal.name +
" and I speak " +
language.name);
}
greetLang = method(["cat", "en"], greetLangCatEn)(greetLang);
function greetLangCatFr(animal, language) {
console.log("Miaou! Je m'appelle " +
animal.name +
" et je parle " +
language.name);
}
greetLang = method(["cat", "fr"], greetLangCatFr)(greetLang);
function greetLangCowEn(animal, language) {
console.log("Moo! Call me " +
animal.name +
" and I speak " +

=== 페이지 313 ===
13.3 Multimethods with multiple dispatch 285
language.name);
}
greetLang = method(["cow", "en"], greetLangCowEn)(greetLang);
function greetLangCowFr(animal, language) {
console.log("Meuh! Appelle moi " +
animal.name +
" et je parle " +
language.name);
}
greetLang = method(["cow", "fr"], greetLangCowFr)(greetLang);
Dave looks at the code for the methods that deal with French. He is surprised to see Ouaf
Ouaf instead of Woof Woof for dogs, Miaou instead of Meow for cats, and Meuh instead of
Moo for cows.
Dave I didn’t know that animal onomatopoeia were different in French than in
English!
Theo Ono what?
Dave Onomatopoeia, from the Greek ónoma that means name and poiéo– that means to
produce. It is the property of words that sound like what they represent; for
instance, Woof, Meow, and Moo.
Theo Yeah, for some reason in French, dogs Ouaf, cats Miaou, and cows Meuh.
Dave I see that in the array the animal type is always before the language type.
Theo Right! As I told you before, in a multimethod that features multiple dispatch,
the order doesn’t really matter, but it has to be consistent.
TIP Multiple dispatch is when a dispatch function emits a value that depends on more
than one argument. In a multimethod that features multiple dispatch, the order of
the elements in the array emitted by the dispatch function has to be consistent with
the order of the elements in the wiring of the methods.
Dave Now let me see if I can figure out how to use a multimethod that features mul-
tiple dispatch.
Dave remembers that Theo told him earlier that multimethods are used like regular func-
tions. With that in mind, he comes up with the code for a multimethod that features multi-
ple dispatch.
Listing13.17 Calling a multimethod that features multiple dispatch
greetLang(myDog, french);
// → "Ouaf Ouaf! Je m\'appelle Fido et je parle Français"
greetLang(myDog, english);
// → "Woof woof! My name is Fido and I speak English"
greetLang(myCat, french);
// → "Miaou! Je m\'appelle Milo et je parle Français"

=== 페이지 314 ===
286 CHAPTER 13 Polymorphism
greetLang(myCat, english);
// → "Meow! I am Milo and I speak English"
greetLang(myCow, french);
// → "Meuh! Appelle moi Clarabelle et je parle Français"
greetLang(myCow, english);
// → "Moo! Call me Clarabelle and I speak English"
Theo Now do you agree that multimethods with multiple dispatch offer a more pow-
erful polymorphism that OOP polymorphism?
Dave Indeed, I do.
Theo Let me show you an even more powerful polymorphism called dynamic dis-
patch. But first, let’s get some more of that wonderful French press coffee.
Dave Great idea! While we’re in the kitchen, I think my mom made an orange Bundt
cake using the oranges from the grove.
13.4 Multimethods with dynamic dispatch
Dave refills their coffee cups as Theo takes two slices from the cake and dishes them up.
They take their coffee and cake outside to enjoy more of the fresh country air before
resuming their conversation.
Dave What is dynamic dispatch?
Theo It’s when the dispatch function of a multimethod returns a value that goes
beyond the static type of its arguments.
Dave Like what, for example?
Theo Like a number or a Boolean, for instance.
Dave Why would such a thing be useful?
Theo Imagine that instead of being polyglot, our animals would suffer from
dysmakrylexia.
Dave Suffering from what?
Theo Dysmakrylexia. It comes from the Greek dus, expressing the idea of difficulty,
makrýs meaning long, and léxis meaning diction. Therefore, dysmakrylexia is dif-
ficulty pronouncing long words.
Dave I’ve never heard of that.
Theo That’s because I just invented it.
Dave Funny. What’s considered a long word for our animals?
Theo Let’s say that when their name has more than five letters, they’re not able to
say it.
Dave A bit weird, but OK.
Theo Let’s call our multimethod dysGreet. Its dispatch function returns an array
with two elements: the animal type and a Boolean about whether the name is
long or not. Take a look at this multimethod initialization.

=== 페이지 315 ===
13.4 Multimethods with dynamic dispatch 287
Listing13.18 A multimethod using a dispatch function with dynamic dispatch
function dysGreetDispatch(animal) {
if(dev()) {
if(!ajv.validate(animalSchema, animal)) {
var errors = ajv.errorsText(ajv.errors);
throw ("dysGreet called with invalid arguments: " + errors);
}
}
var hasLongName = animal.name.length > 5;
return [animal.type, hasLongName];
};
var dysGreet = multi(dysGreetDispatch);
Dave Writing the dysGreet methods doesn’t seem too complicated.
As Theo reaches over to pass Dave his notebook, he accidently hits his coffee cup. Now Theo’s
notebook is completely wet, and all the diagrams are soggy! Fortunately, Dave brought an
extra napkin from the kitchen, and it’s still clean. He draws a flow diagram as in figure 13.4
and then grabs his laptop and writes the implementation of the dysGreet methods.
["dog", true] dysGreetDogLong
Greet as a dog mentioning name
["cat", true] dysGreetCatLong
Greet as a cat mentioning name
["cow", true] dysGreetCowLong
Greet as a cow mentioning name
args dysGreetLangDispatch
animal, language Emit the animal and the language types
["dog", false] dysGreetDogShort
Greet as a dog omitting name
["cat", false] dysGreetCatShort
Greet as a cat omitting name
["cow", false] dysGreetCowShort
Greet as a cow omitting name
Figure 13.4 The logic flow of the dysGreet multimethod
Listing13.19 The dysGreet methods
function dysGreetDogLong(animal) {
console.log("Woof woof! My name is " + animal.name);
}
dysGreet = method(["dog", true], dysGreetDogLong)(dysGreet);

=== 페이지 316 ===
288 CHAPTER 13 Polymorphism
function dysGreetDogShort(animal) {
console.log("Woof woof!");
}
dysGreet = method(["dog", false], dysGreetDogShort)(dysGreet);
function dysGreetCatLong(animal) {
console.log("Meow! I am " + animal.name);
}
dysGreet = method(["cat", true], dysGreetCatLong)(dysGreet);
function dysGreetCatShort(animal) {
console.log("Meow!");
}
dysGreet = method(["cat", false], dysGreetCatShort)(dysGreet);
function dysGreetCowLong(animal) {
console.log("Moo! Call me " + animal.name);
}
dysGreet = method(["cow", true], dysGreetCowLong)(dysGreet);
function dysGreetCowShort(animal) {
console.log("Moo!");
}
dysGreet = method(["cow", false], dysGreetCowShort)(dysGreet);
Theo checks that the code works as expected. He compliments Dave, not only on the
method implementation but also for having the foresight to grab an extra napkin.
Listing13.20 Testing dysGreet
dysGreet(myDog);
dysGreet(myCow);
dysGreet(myCat);
//"Woof woof!"
//"Moo! Call me Clarabelle"
//"Meow!"
Theo Well done, my friend! Our exploration of multimethods has come to an end. I
think it’s time for me to drive back if I want to get home before dark and beat
the rush hour traffic.
Dave Before you leave, let’s check if multimethods are available in programming
languages other than JavaScript.
Theo That’s a question for Joe.
Dave Do you think it’s OK if I call him now?
Theo I think it’s probably better if you send him an email. He’s in a tech conference,
and I’m not sure if it’s all day. Thank you for this beautiful day in the country
and the wonderful refreshments.
Dave I enjoyed it, also, especially our discussions about etymology. I think there are
some oranges for you to take home and enjoy later.
Theo Great! I can’t wait until my wife tries one.

=== 페이지 317 ===
13.5 Integrating multimethods in a production system 289
After Theo leaves, Dave sends Joe an email. A few minutes later, Dave receives an email
from Joe with the subject, “Support for multimethods in different languages.”
Support for multimethods in different languages
Python has a library called multimethods (https://github.com/weissjeffm/multimeth-
ods), and Ruby has one called Ruby multimethods (https://github.com/psantacl/
ruby-multimethods). Both seem to work quite like the JavaScript arrows/multi-
method library.
In Java, there is the Java Multimethod Framework (http://igm.univ-mlv.fr/~forax/
works/jmmf/), and C# supports multimethods natively via the dynamic keyword.
However, in both Java and C#, multimethods work only with static data types and not
with generic data structures.
Generic data structure
Language URL
support
JavaScript https://github.com/caderek/arrows/tree/master/ Yes
packages/multimethod
Java http://igm.univ-mlv.fr/~forax/works/jmmf/ No
C# Native support No
Python https://github.com/weissjeffm/multimethods Yes
Ruby https://github.com/psantacl/ruby-multimethods Yes
13.5 Integrating multimethods in a production system
While Theo is driving back home, his thoughts take him back to the fresh air of the coun-
try. This pleasant moment is interrupted by a phone call from Nancy at Klafim.
Nancy How are you doing?
Theo Fine. I’m driving back from the countryside.
Nancy Cool. Are you available to talk about work?
Theo Sure.
Nancy I’d like to add a tiny feature to the catalog.
In the past, when Nancy qualified a feature as tiny, it scared Theo because tiny turned into
huge. What seemed easy to her always took him a surprising amount of time to develop.
But after refactoring the system according to DOP principles, now what seems tiny to
Nancy is usually quite easy to implement.
Theo What feature?
Nancy I’d like to allow librarians to view the list of authors, ordered by last name, in
two formats: HTML and Markdown.

=== 페이지 318 ===
290 CHAPTER 13 Polymorphism
Theo It doesn’t sound too complicated.
Nancy Also, I need a bit of text formatting.
Theo What kind of text formatting?
Nancy Depending on the number of books an author has written, their name should
be in bold and italic fonts.
Theo Could you send me an email with all the details. I’ll take a look at it tomorrow
morning.
Nancy Perfect. Have a safe drive!
Before going to bed, Theo reflects about today’s etymology lessons. He realizes that he
never looked for the etymology of the word etymology itself! He searches for the term etymol-
ogy online and learns that the word etymology derives from the Greek étumon, meaning true
sense, and the suffix logia, denoting the study of. During the night, Theo dreams of dogs,
cats, and cows programming on their laptops in a field of grass.
When Theo arrives at the office the next day, he opens Nancy’s email with the details
about the text formatting feature. The details are summarized in table 13.1.
Table 13.1 Text formatting for author names according to the number of books
they have written
Number of books Italic Bold
10 or fewer Yes No
Between 11 and 50 No Yes
51 or more Yes Yes
Theo forwards Nancy’s email to Dave and asks him to take care of this task. Delegating
responsibility, after all, is the trait of a great manager.
Dave thinks the most difficult part of the feature lies in implementing an Author
.myName(author, format) function that receives two arguments: the author data and the
text format. He asks himself whether he can implement this function as a multimethod
and use what he learned yesterday with Theo at his parents’ home in the country. It seems
that this feature is quite similar to the one that dealt with dysmakrylexia. Instead of check-
ing the length of a string, he needs to check the length of an array.
First, Dave needs a data schema for the text format. He could represent a format as a
map with a type field like Theo did yesterday for languages, but at the moment, it seems
simpler to represent a format as a string that could be either markdown or html. He comes
up with the text format schema in listing 13.21. He already wrote the author schema with
Theo last week. It’s in listing 13.22.
Listing13.21 The text format schema
var textFormatSchema = {
"name": {"type": "string"},
"type": {"enum": ["markdown", "html"]}
};

=== 페이지 319 ===
13.5 Integrating multimethods in a production system 291
Listing13.22 The author schema
var authorSchema = {
"type": "object",
"required": ["name", "bookIsbns"],
"properties": {
"name": {"type": "string"},
"bookIsbns": {
"type": "array",
"items": {"type": "string"}
}
}
};
Now, Dave needs to write a dispatch function and initialize the multimethod. Remember-
ing that Theo had no qualms about creating the word dysmakrylexia, he decides that he
prefers his own neologism, prolificity, over the existing nominal form prolificness. He finds it
useful to have an Author.prolificityLevel helper function that returns the level of
prolificity of the author: either low, medium, or high. Now he’s ready to code the author-
NameDispatch function.
Listing13.23 Author.myName multimethod initialization
Author.prolificityLevel = function(author) {
var books = _.size(_.get(author, "bookIsbns"));
if (books <= 10) {
return "low";
};
if (books >= 51) {
return "high";
}
return "medium";
};
var authorNameArgsSchema = {
"type": "array",
"prefixItems": [
authorSchema,
{"enum": ["markdown", "html"]}
]
};
function authorNameDispatch(author, format) {
if(dev()) {
if(!ajv.validate(authorNameArgsSchema, [author, format])) {
throw ("Author.myName called with invalid arguments: " +
ajv.errorsText(ajv.errors));
}
}
return [Author.prolificityLevel(author), format];
};
Author.myName = multi(authorNameDispatch);

=== 페이지 320 ===
292 CHAPTER 13 Polymorphism
Then Dave works on the methods: first, the HTML format methods. In HTML, bold text is
wrapped inside a <b> tag, and italic text is wrapped in a <i> tag. For instance, in HTML,
three authors with different levels of prolificity would be written like this.
Listing13.24 Examples of bold and italic in HTML
Italic formatting for Bold formatting for
minimally prolific authors moderately prolific authors
<i>Yehonathan Sharvit<i>
Bold and italic formatting
<b>Stephen Covey</b>
for highly prolific authors
<b><i>Isaac Asimov</i></b>
With this information in hand, Dave writes the three methods that deal with HTML for-
matting. Easy!
Listing13.25 The methods that deal with HTML formatting
function authorNameLowHtml(author, format) {
return "<i>" + _.get(author, "name") + "</i>";
}
Author.myName = method(["low", "html"], authorNameLowHtml)(Author.myName);
function authorNameMediumHtml(author, format) {
return "<b>" + _.get(author, "name") + "</b>";
}
Author.myName =
method(["medium", "html"], authorNameMediumHtml)(Author.myName);
function authorNameHighHtml(author, format) {
return "<b><i>" + _.get(author, "name") + "</i></b>";
}
Author.myName =
method(["high", "html"], authorNameHighHtml)(Author.myName);
Then, Dave moves on to the three methods that deal with Markdown formatting. In
Markdown, bold text is wrapped in two asterisks, and italic text is wrapped in a single
asterisk. For instance, in Markdown, three authors with different levels of prolificity
would be written like the code in listing 13.26. The code for the Markdown methods is in
listing 13.27.
Listing13.26 Examples of bold and italic in Markdown
Italic formatting for Bold formatting for
minimally prolific authors moderately prolific authors
*Yehonathan Sharvit*
Bold and italic formatting
**Stephen Covey**
for highly prolific authors
***Isaac Asimov***

=== 페이지 321 ===
13.5 Integrating multimethods in a production system 293
Listing13.27 The methods that deal with Markdown formatting
function authorNameLowMarkdown(author, format) {
return "*" + _.get(author, "name") + "*";
}
Author.myName =
method(["low", "markdown"], authorNameLowMarkdown)(Author.myName);
function authorNameMediumMarkdown(author, format) {
return "**" + _.get(author, "name") + "**";
}
Author.myName =
method(["medium", "markdown"], authorNameMediumMarkdown)(Author.myName);
function authorNameHighMarkdown(author, format) {
return "***" + _.get(author, "name") + "***";
}
Author.myName =
method(["high", "markdown"], authorNameHighMarkdown)(Author.myName);
Dave decides to test his code by involving a mysterious author. Listing 13.28 and listing 13.29
show the tests.
Listing13.28 Testing HTML formatting
var yehonathan = {
"name": "Yehonathan Sharvit",
"bookIsbns": ["9781617298578"]
};
Author.myName(yehonathan, "html");
// → "<i>Yehonathan Sharvit</i>"
Listing13.29 Testing Markdown formatting
Author.myName(yehonathan, "markdown");
// → "*Yehonathan Sharvit*"
Theo shows up at Dave’s desk and asks to review Dave’s implementation of the list of
authors feature. Curious, Theo asks Dave about the author that appears in the test of
Author.myName.
Theo Who is Yehonathan Sharvit?
Dave I don’t really know. The name appeared when I googled “data-oriented pro-
gramming” yesterday. He wrote a book on the topic. I thought it would be cool
to use its ISBN in my test.

=== 페이지 322 ===
294 CHAPTER 13 Polymorphism
Summary
 The main benefit of polymorphism is extensibility.
 Multimethods make it possible to benefit from polymorphism when data is repre-
sented with generic maps.
 A multimethod is made of a dispatch function and multiple methods.
 The dispatch function of a multimethod emits a dispatch value.
 Each of the methods used in a multimethod provides an implementation for a
specific dispatch value.
 Multimethods can mimic OOP class inheritance via single dispatch.
 In single dispatch, a multimethod receives a single map that contains a type field,
and the dispatch function of the multimethod emits the value of the type field.
 In addition to single dispatch, multimethods provide two kinds of advanced
polymorphisms: multiple dispatch and dynamic dispatch.
 Multiple dispatch is used when the behavior of the multimethod depends on
multiple arguments.
 Dynamic dispatch is used when the behavior of the multimethod depends on run-
time arguments.
 The arguments of a multimethod are passed to the dispatch function and to the
methods.
 A multimethod dispatch function is responsible for
– Defining the signature.
– Validating the arguments.
– Emitting a dispatch value.
 Multimethods provides extensibility by decoupling between multimethod ini-
tialization and method implementations.
 Multimethods are called like regular functions.
 Multimethods support default implementations that are called when no method
corresponds to the dispatch value.
 In a multimethod that features multiple dispatch, the order of the elements in
the array emitted by the dispatch function has to be consistent with the order of
the elements in the wiring of the methods.
Lodash functions introduced in this chapter
Function Description
size(coll) Gets the size of coll

=== 페이지 323 ===
Advanced data
manipulation
Whatever is well-conceived
is clearly said
This chapter covers
 Manipulating nested data
 Writing clear and concise code for business
logic
 Separating business logic and generic data
manipulation
 Building custom data manipulation tools
 Using the best tool for the job
When our business logic involves advanced data processing, the generic data manip-
ulation functions provided by the language run time and by third-party libraries
might not be sufficient. Instead of mixing the details of data manipulation with
business logic, we can write our own generic data manipulation functions and imple-
ment our custom business logic using them. Separating business logic from the inter-
nal details of data manipulation makes the business logic code concise and easy to
read for other developers.
295

=== 페이지 324 ===
296 CHAPTER 14 Advanced data manipulation
14.1 Updating a value in a map with eloquence
Dave is more and more autonomous on the Klafim project. He can implement most fea-
tures on his own, typically turning to Theo only for code reviews. Dave’s code quality stan-
dards are quite high. Even when his code is functionally solid, he tends to be unsatisfied
with its readability. Today, he asks for Theo’s help in improving the readability of the code
that fixes a bug Theo introduced a long time ago.
Dave I think I have a found a bug in the code that returns book information from
the Open Library API.
Theo What bug?
Dave Sometimes, the API returns duplicate author names, and we pass the dupli-
cates through to the client.
Theo It doesn’t sound like a complicated bug to fix.
Dave Right, I fixed it, but I’m not satisfied with the readability of the code I wrote.
Theo Being critical of our own code is an important quality for a developer to prog-
ress. What is it exactly that you don’t like?
Dave Take a look at this code.
Listing14.1 Removing duplicates in a straightforward but tedious way
function removeAuthorDuplicates(book) {
var authors = _.get(book, "authors");
var uniqAuthors = _.uniq(authors);
return _.set(book,"authors", uniqAuthors);
}
Dave I’m using _.get to retrieve the array with the author names, then _.uniq to
create a duplicate-free version of the array, and finally, _.set to create a new
version of the book with no duplicate author names.
Theo The code is tedious because the next value of authorNames needs to be based
on its current value.
Dave But it’s a common use case! Isn’t there a simpler way to write this kind of code?
Theo Your astonishment definitely honors you as a developer, Dave. I agree with you
that there must be a simpler way. Let me phone Joe and see if he’s available for
a conference call.
Joe How’s it going, Theo?
Theo Great! Are you back from your tech conference?
Joe I just landed. I’m on my way home now in a taxi.
Theo How was your talk about DOP?
Joe Pretty good. At the beginning people were a bit suspicious, but when I told
them the story of Albatross and Klafim, it was quite convincing.
Theo Yeah, adults are like children in that way; they love stories.
Joe What about you? Did you manage to achieve polymorphism with multimethods?
Theo Yes! Dave even managed to implement a feature in Klafim with multimethods.
Joe Cool!

=== 페이지 325 ===
14.1 Updating a value in a map with eloquence 297
Theo Do you have time to help Dave with a question about programming?
Joe Sure.
Dave Hi Joe. How are you doing?
Joe Hello Dave. Not bad. What kind of help do you need?
Dave I’m wondering if there’s a simpler way to remove duplicates inside an array
value in a map. Using _.get, _.uniq, and _.set looks quite tedious.
Joe You should build your own data manipulation tools.
Dave What do you mean?
Joe You should write a generic update function that updates a value in a map,
applying a calculation based on its current value.1
Dave What would the arguments of update be in your opinion?
Joe Put the cart before the horse.
Dave What?!
Joe Rewrite your business logic as if update were already implemented, and you’ll
discover what the arguments of update should be.
Dave I see what you mean: the horse is the implementation of update, and the cart is
the usage of update.
Joe Exactly. But remember, it’s better if you keep your update function generic.
Dave How?
Joe By not limiting it to your specific use case.
Dave I see. The implementation of update should not deal with removing duplicate
elements. Instead, it should receive the updating function—in my case,
_.uniq—as an argument.
Joe Exactly! Uh, sorry Dave, I gotta go, I just got home. Good luck!
Dave Take care, Joe, and thanks!
Dave ends the conference call. Looking at Theo, he reiterates the conversation with Joe.
Dave Joe advised me to write my own update function. For that purpose, he told me
to start by rewriting removeAuthorDuplicates as if update were already
implemented. That will allow us to make sure we get the signature of update
right.
Theo Sounds like a plan.
Dave Joe called it “putting the cart before the horse.”
Theo Joe and his funny analogies...
TIP The best way to find the signature of a custom data manipulation function is to
think about the most convenient way to use it.
Dave Anyway, the way I’d like to use update inside removeAuthorDuplicates is
like this.
1 Lodash provides an implementation of update, but for the sake of teaching, we are writing our own imple-
mentation.

=== 페이지 326 ===
298 CHAPTER 14 Advanced data manipulation
Listing14.2 The code that removes duplicates in an elegant way
function removeAuthorDuplicates(book) {
return update(book, "authors", _.uniq);
}
Theo Looks good to me!
Dave Wow! Now the code with update is much more elegant than the code with
_.get and _.set!
Theo Before you implement update, I suggest that you write down in plain English
exactly what the function does.
Dave It’s quite easy: update receives a map called map, a path called path, and a
function called fun. It returns a new version of map, where path is associated
with fun(currentValue), and currentValue is the value associated with
path in map.
Thinking out loud, Dave simultaneously draws a diagram like that in figure 14.1. Theo is
becoming more and more impressed with his young protegé as he studies the figure.
{
"position" : "manager", "income"
"income" : 100000
} map fun path
update
{
"position" : "manager",
"income" : fun(100000)
res Figure 14.1 The
}
behavior of update
TIP Before implementing a custom data manipulation function, formulate in plain
English exactly what the function does.
Theo With such a clear definition, it’s going to be a piece of cake to implement
update!
After a few minutes, Dave comes up with the code. It doesn’t take long because the plain-
English diagram helps him to organize the code.
Listing14.3 A generic update function
function update(map, path, fun) {
var currentValue = _.get(map, path);
var nextValue = fun(currentValue);
return _.set(map, path, nextValue);
}

=== 페이지 327 ===
14.2 Manipulating nested data 299
Theo Why don’t you see if it works with a simple case such as incrementing a number
in a map?
Dave Good idea! I’ll try multiplying a value in a map by 2 with update. How’s this
look?
Listing14.4 Multiplying a value in a map by 2
var m = {
"position": "manager",
"income": 100000
};
update(m, "income", function(x) {
return x * 2;
});
// → {"position": "manager", "income": 200000}
Theo Great! It seems to work.
14.2 Manipulating nested data
The next Monday, during Theo and Dave’s weekly sync meeting, they discuss the upcom-
ing features for Klafim. Theo fondly remembers another Monday where they met at Dave’s
family home in the country. Coming back to the present moment, Theo begins.
Theo Recently, Nancy has been asking for more and more administrative features.
Dave Like what?
Theo I’ll give you a few examples.... Let me find the email I got from Nancy yesterday.
Dave OK.
Theo Here it is. There are three feature requests for now: listing all the book author
IDs, calculating the book lending ratio, and grouping books by a physical library.
Dave What feature should I tackle first?
Theo It doesn’t matter, but you should deliver the three of these before the end of
the week. Good luck, and don’t hesitate to call me if you need help.
On Tuesday, Dave asks for Theo’s help. Dave is not pleased with how his code looks.
Dave I started to work on the three admin features, but I don’t like the code I wrote.
Let me show you the code for retrieving the list of author IDs from the list of
books returned from the database.
Theo Can you remind me what an element in a book list returned from the database
looks like?
Dave Each book is a map with an authorIds array field.
Theo OK, so it sounds like a map over the books should do it.
Dave This is what I did, but it doesn’t work as expected. Here’s my code for listing
the book author IDs.

=== 페이지 328 ===
300 CHAPTER 14 Advanced data manipulation
Listing14.5 Retrieving the author IDs in books as an array of arrays
function authorIdsInBooks(books) {
return _.map(books, "authorIds");
}
Theo What’s the problem?
Dave The problem is that it returns an array of arrays of author IDs instead of an
array of author IDs. For instance, when I run authorIdsInBooks on a catalog
with two books, I get this result.
Listing14.6 The author IDs in an array of arrays
[
["sean-covey", "stephen-covey"],
["alan-moore", "dave-gibbons"]
]
Theo That’s not a big problem. You can flatten an array of arrays with _.flatten,
and you should get the result you expect.
Dave Nice! This is exactly what I need! Give me a moment to fix the code of
authorIdsInBooks. . . here you go.
Listing14.7 Retrieving the author IDs in books as an array of strings
function authorIdsInBooks(books) {
return _.flatten(_.map(books, "authorIds"));
}
Theo Don’t you think that mapping and then flattening deserves a function of its own?
Dave Maybe. It’s quite easy to implement a flatMap function.2 How about this?
Listing14.8 The implementation of flatMap
function flatMap(coll, f) {
return _.flatten(_.map(coll,f));
}
Theo Nice!
Dave I don’t know.... It’s kind of weird to have such a small function.
Theo I don’t think that code size is what matters here.
Dave What do you mean?
Theo See what happens when you rewrite authorIdsInBooks using flatMap.
Dave OK, here’s how I’d use flatMap to list the author IDs.
2 Lodash provides an implementation of flatMap, but for the sake of teaching, we are writing our own
implementation.

=== 페이지 329 ===
14.3 Using the best tool for the job 301
Listing14.9 Retrieving the author IDs as an array of strings using flatMap
function authorIdsInBooks(books) {
return flatMap(books, "authorIds");
}
Theo What implementation do you prefer, the one with flatten and map (in listing
14.7) or the one with flatMap (in listing 14.9)?
Dave I don’t know. To me, they look quite similar.
Theo Right, but which implementation is more readable?
Dave Well, assuming I know what flatMap does, I would say the implementation
with flatMap. Because it’s more concise, it is a bit more readable.
Theo Again, it’s not about the size of the code. It’s about the clarity of intent and the
power of naming things.
Dave I don’t get that.
Theo Let me give you an example from our day-to-day language.
Dave OK.
Theo Could you pass me that thing on your desk that’s used for writing?
It takes Dave a few seconds to get that Theo has asked him to pass the pen on the desk.
After he passes Theo the pen, he asks:
Dave Why didn’t you simply ask for the pen?
Theo I wanted you to experience how it feels when we use descriptions instead of
names to convey our intent.
Dave Oh, I see. You mean that once we use a name for the operation that maps and
flattens, the code becomes clearer.
Theo Exactly.
Dave Let’s move on to the second admin feature: calculating the book lending ratio.
Theo Before that, I think we deserve a short period for rest and refreshments, where
we drink a beverage made by percolation from roasted and ground seeds.
Dave A coffee break!
14.3 Using the best tool for the job
After the coffee break, Dave shows Theo his implementation of the book lending ratio cal-
culation. This time, he seems to like the code he wrote.
Dave I’m quite proud of the code I wrote to calculate the book lending ratio.
Theo Show me the money!
Dave My function receives a list of books from the database like this.
Listing14.10 A list of two books with bookItems
[
{
"isbn": "978-1779501127",

=== 페이지 330 ===
302 CHAPTER 14 Advanced data manipulation
"title": "Watchmen",
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
}
]
},
{
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"bookItems": [
{
"id": "book-item-123",
"libId": "hudson-park-lib",
"isLent": true
},
{
"id": "book-item-17",
"libId": "nyc-central-lib",
"isLent": false
}
]
}
]
Theo Quite a nested piece of data!
Dave Yeah, but now that I’m using flatMap, calculating the lending ratio is quite
easy. I’m going over all the book items with forEach and incrementing either
the lent or the notLent counter. At the end, I return the ratio between lent
and (lent + notLent). Here’s how I do that.
Listing14.11 Calculating the book lending ratio using forEach
function lendingRatio(books) {
var bookItems = flatMap(books, "bookItems");
var lent = 0;
var notLent = 0;
_.forEach(bookItems, function(item) {
if(_.get(item, "isLent")) {
lent = lent + 1;
} else {
notLent = notLent + 1;
}
});
return lent/(lent + notLent);
}
Theo Would you allow me to tell you frankly what I think of your code?
Dave If you are asking this question, it means that you don’t like it. Right?
Theo It’s nothing against you; I don’t like any piece of code with forEach.

=== 페이지 331 ===
14.3 Using the best tool for the job 303
Dave What’s wrong with forEach?
Theo It’s too generic!
Dave I thought that genericity was a positive thing in programming.
Theo It is when we build a utility function, but when we use a utility function, we
should use the least generic function that solves our problem.
Dave Why?
Theo Because we ought to choose the right tool for the job, like in the real life.
Dave What do you mean?
Theo Let me give you an example. Yesterday, I had to clean my drone from the
inside. Do you think that I used a screwdriver or a Swiss army knife to unscrew
the drone cover?
Dave A screwdriver, of course! It’s much more convenient to manipulate.
Theo Right. Also, imagine that someone looks at me using a screwdriver. It’s quite
clear to them that I am turning a screw. It conveys my intent clearly.
Dave Are you saying that forEach is like the Swiss army knife of data manipulation?
Theo That’s a good way to put it.
TIP Pick the least generic utility function that solves your problem.
Dave What function should I use then, to iterate over the book item collection?
Theo You could use _.reduce.
Dave I thought reduce was about returning data from a collection. Here, I don’t
need to return data; I need to update two variables, lent and notLent.
Theo You could represent those two values in a map with two keys.
Dave Can you show me how to rewrite my lendingRatio function using reduce?
Theo Sure. The initial value passed to reduce is the map, {"lent": 0, "notLent": 0},
and inside each iteration, we update one of the two keys, like this.
Listing14.12 Calculating the book lending ratio using reduce
function lendingRatio(books) {
var bookItems = flatMap(books, "bookItems");
var stats = _.reduce(bookItems, function(res, item) {
if(_.get(item, "isLent")) {
res.lent = res.lent + 1;
} else {
res.notLent = res.notLent + 1;
}
return res;
}, {notLent: 0, lent:0});
return stats.lent/(stats.lent + stats.notLent);
}
Dave Instead of updating the variables lent and notLent, now we are updating lent
and notLent map fields. What’s the difference?

=== 페이지 332 ===
304 CHAPTER 14 Advanced data manipulation
Theo Dealing with map fields instead of variables allows us to get rid of reduce in
our business logic code.
Dave How could you iterate over a collection without forEach and without reduce?
Theo I can’t avoid the iteration over a collection, but I can hide reduce behind a
utility function. Take a look at the way reduce is used inside the code of
lendingRatio. What is the meaning of the reduce call?
Dave looks at the code in listing 14.12. He thinks for a long moment before he answers.
Dave I think it’s counting the number of times isLent is true and false.
Theo Right. Now, let’s use Joe’s advice about building our own data manipulation
tool.
Dave How exactly?
Theo I suggest that you write a countByBoolField utility function that counts the
number of times a field is true and false.
Dave OK, but before implementing this function, let me first rewrite the code of
lendingRatio, assuming this function already exists.
Theo You are definitely a fast learner, Dave!
Dave Thanks! I think that by using countByBoolField, the code for calculating the
lending ratio using a custom utility function would be something like this.
Listing14.13 Calculating the book lending ratio
function lendingRatio(books) {
var bookItems = flatMap(books, "bookItems");
var stats = countByBoolField(bookItems, "isLent", "lent", "notLent");
return stats.lent/(stats.lent + stats.notLent);
}
TIP Don’t use _.reduce or any other low-level data manipulation function inside
code that deals with business logic. Instead, write a utility function—with a proper
name—that hides _.reduce.
Theo Perfect. Don’t you think that this code is clearer than the code using _.reduce?
Dave I do! The code is both more concise and the intent is clearer. Let me see if I
can implement countByBoolField now.
Theo I suggest that you write a unit test first.
Dave Good idea.
Dave types for a bit. When he’s satisfied, he shows Theo the result.
Listing14.14 A unit test for countByBoolField
var input = [
{"a": true},
{"a": false},
{"a": true},

=== 페이지 333 ===
14.4 Unwinding at ease 305
{"a": true}
];
var expectedRes = {
"aTrue": 3,
"aFalse": 1
};
_.isEqual(countByBoolField(input, "a", "aTrue", "aFalse"), expectedRes);
Theo Looks good to me. Now, for the implementation of countByBoolField, I
think you are going to need our update function.
Dave I think you’re right. On each iteration, I need to increment the value of either
aTrue or aFalse using update and a function that increments a number by 1.
After a few minutes of trial and error, Dave comes up with the piece of code that uses
reduce, update, and inc. He shows Theo the code for countByBoolField.
Listing14.15 The implementation of countByBoolField
function inc (n) {
return n + 1;
}
function countByBoolField(coll, field, keyTrue, keyFalse) {
return _.reduce(coll, function(res, item) {
if (_.get(item, field)) {
return update(res, keyTrue, inc);
}
return update(res, keyFalse, inc);
}, {[keyTrue]: 0,
Creates a map with
[keyFalse]: 0});
keyTrue and keyFalse
}
associated to 0
Theo Well done! Shall we move on and review the third admin feature?
Dave The third feature is more complicated. I would like to use the teachings from
the first two features for the implementation of the third feature.
Theo OK. Call me when you’re ready for the code review.
14.4 Unwinding at ease
Dave really struggled with the implementation of the last admin feature, grouping books
by a physical library. After a couple of hours of frustration, Dave calls Theo for a rescue.
Dave I really had a hard time implementing the grouping by library feature.
Theo I only have a couple of minutes before my next meeting, but I can try to help
you. What’s the exact definition of grouping by library?
Dave Let me show you the unit test I wrote.

=== 페이지 334 ===
306 CHAPTER 14 Advanced data manipulation
Listing14.16 Unit test for grouping books by a library
var books = [
{
"isbn": "978-1779501127",
"title": "Watchmen",
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
}
]
},
{
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"bookItems": [
{
"id": "book-item-123",
"libId": "hudson-park-lib",
"isLent": true
},
{
"id": "book-item-17",
"libId": "nyc-central-lib",
"isLent": false
}
]
}
];
var expectedRes =
{
"hudson-park-lib": [
{
"bookItems": {
"id": "book-item-123",
"isLent": true,
"libId": "hudson-park-lib",
},
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
},
],
"nyc-central-lib": [
{
"bookItems": {
"id": "book-item-1",
"isLent": true,
"libId": "nyc-central-lib",
},
"isbn": "978-1779501127",
"title": "Watchmen",
},

=== 페이지 335 ===
14.4 Unwinding at ease 307
{
"bookItems": {
"id": "book-item-17",
"isLent": false,
"libId": "nyc-central-lib",
},
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
},
],
};
_.isEqual(booksByRack(books) , expectedRes);
Theo Cool.... Writing unit tests before implementing complicated functions was
also helpful for me when I refactored Klafim from OOP to DOP.
Dave Writing unit tests for functions that receive and return data is much more fun
than writing unit tests for the methods of stateful objects.
TIP Before implementing a complicated function, write a unit test for it.
Theo What was difficult about the implementation of booksByLib?
Dave I started with a complicated implementation involving merge and reduce
before I remembered that you advised me to hide reduce behind a generic
function. But I couldn’t figure out what kind of generic function I needed.
Theo Indeed, it’s not easy to implement.
Dave I’m glad to hear that. I thought I was doing something wrong.
Theo The challenge here is that you need to work with book items, but the book title
and ISBN are not present in the book item map.
Dave Exactly!
Theo It reminds me a query I had to write a year ago on MongoDB, where data was
laid out in a similar way.
Dave And what did your query look like?
Theo I used MongoDB’s $unwind operator. Given a map m with a field <arr,
myArray>, it returns an array where each element is a map corresponding to m
without arr and with item associated to an element of myArray.
Dave That’s a bit abstract for me. Could you give me an example?
Theo moves to the whiteboard. He draws a diagram like the one in figure 14.2.
Theo In my case, I was dealing with an online store, where a customer cart was repre-
sented as a map with a customer-id field and an items array field. Each ele-
ment in the array represented an item in the cart. I wrote a query with unwind
that retrieved the cart items with the customer-id field.
Dave Amazing! That’s exactly what we need. Let’s write our own unwind function!

=== 페이지 336 ===
308 CHAPTER 14 Advanced data manipulation
{
"customer-id" : "joe",
// Other fields
"items" : [
{
"item" : "phone",
"quantity" : 1
},
{
"item" : "pencil",
"quantity" : 10 "items"
}
] map path
}
unwind
{ {
"customer-id" : "joe", "customer-id" : "joe",
// Other fields // Other fields
"items" : { res "items" : {
"item" : "phone", "item" : "pencil",
"quantity" : 1 "quantity" : 10
} }
} }
Figure 14.2 The behavior of unwind
Theo I’d be happy to pair program with you on this cool stuff, but I’m already run-
ning late for another meeting.
Dave I’m glad I’m not a manager!
When Theo leaves for his meeting, Dave goes to the kitchen and prepares himself a long
espresso as a reward for all that he’s accomplished today. He thoroughly enjoys it as he
works on the implementation of unwind.
As Joe advised, Dave starts by writing the code for booksByLib as if unwind were already
implemented. He needs to go over each book and unwind its book items using flatMap
and unwind. He then groups the book items by their libId using _.groupBy. Satisfied
with the resulting code, he finishes his espresso.
Listing14.17 Grouping books by a library using unwind
function booksByRack(books) {
var bookItems = flatMap(books, function(book) {
return unwind(book, "bookItems");
});
return _.groupBy(bookItems, "bookItems.libId")
}
Dave cannot believe that such a complicated function could be implemented so clearly
and compactly. Dave says to himself that the complexity must reside in the implementation
of unwind—but he soon finds out that he’s wrong; it is not going to be as complicated as
he thought! He starts by writing a unit test for unwind, similar to Theo’s MongoDB cus-
tomer cart scenario.

=== 페이지 337 ===
14.4 Unwinding at ease 309
Listing14.18 A unit test for unwind
var customer = {
"customer-id": "joe",
"items": [
{
"item": "phone",
"quantity": 1
},
{
"item": "pencil",
"quantity": 10
}
]
};
var expectedRes = [
{
"customer-id": "joe",
"items": {
"item": "phone",
"quantity": 1
}
},
{
"customer-id": "joe",
"items": {
"item": "pencil",
"quantity": 10
}
}
]
_.isEqual(unwind(customer, "items"), expectedRes)
The implementation of unwind is definitely not as complicated as Dave thought. It retrieves
the array arr associated with f in m and creates, for each element of arr, a version of m,
where f is associated with elem. Dave is happy to remember that data being immutable,
there is no need to clone m.
Listing14.19 The implementation of unwind
function unwind(map, field) {
var arr = _.get(map, field);
return _.map(arr, function(elem) {
return _.set(map, field, elem);
});
}
After a few moments of contemplating his beautiful code, Dave sends Theo a message with
a link to the pull request that implements grouping books by a library with unwind. After
that he leaves the office to go home, by bike, tired but satisfied.

=== 페이지 338 ===
310 CHAPTER 14 Advanced data manipulation
Summary
 Maintain a clear separation between the code that deals with business logic and
the implementation of the data manipulation.
 Separating business logic from data manipulation makes our code not only con-
cise, but also easy to read because it conveys the intent in a clear manner.
 We design and implement custom data manipulation functions in a four-step
process:
a Discover the function signature by using it before it is implemented.
b Write a unit test for the function.
c Formulate the behavior of the function in plain English.
d Implement the function.
 The best way to find the signature of a custom data manipulation function is to
think about the most convenient way to use it.
 Before implementing a custom data manipulation function, formulate in plain
English exactly what the function does.
 Pick the least generic utility function that solves your problem.
 Don’t use _.reduce or any other low-level data manipulation function inside
code that deals with business logic. Instead, write a utility function—with a proper
name—that hides _.reduce.
 Before implementing a complicated function, write a unit test for it.
Lodash functions introduced in this chapter
Function Description
flatten(arr) Flattens arr a single level deep
sum(arr) Computes the sum of the values in arr
uniq(arr) Creates an array of unique values from arr
every(coll, pred) Checks if pred returns true for all elements of coll
forEach(coll, f) Iterates over elements of coll and invokes f for each element
sortBy(coll, f) Creates an array of elements, sorted in ascending order, by the results of
running each element in coll through f

=== 페이지 339 ===
Debugging
Innovation at the museum
This chapter covers
 Reproducing a bug in code that involves
primitive data types
 Reproducing a bug in code that involves
aggregated data
 Replaying a scenario in the REPL
 Creating unit tests from bugs
When our programs don’t behave as expected, we need to investigate the source
code. The traditional tool for code investigation is the debugger. The debugger
allows us to run the code, step by step, until we find the line that causes the bug.
However, a debugger doesn’t allow us to reproduce the scenario that causes the
problem.
In DOP, we can capture the context of a scenario that causes a bug and replay
it in a separate process like a REPL or a unit test. This allows us to benefit from a
short feedback loop between our attempt to fix the code and the results of our
attempt.
311

=== 페이지 340 ===
312 CHAPTER 15 Debugging
15.1 Determinism in programming
After a few months, Theo calls Dave to tell him that he’s leaving Albatross. After Dave
recovers from this first surprise, he’s given another, more pleasant one. Theo informs Dave
that after consulting with the management team, they have decided that Dave will be in
charge of DOP at Albatross. In addition to the farewell at the office next week, Theo invites
Dave for a last one-on-one work session at the Exploratorium Museum of Science.
During their visit, Dave particularly enjoys the Cells to Self exhibit in the Living Systems
gallery; meanwhile, Theo is having fun with the Colored Shadows exhibit in the Reflec-
tions gallery. After the visit, Theo and Dave settle in the back row of the museum’s audito-
rium and open their laptops.
Dave Why did you want our last meeting to happen here at the Museum of Science?
Theo Remember when Joe told us that someday we’d be able to innovate in DOP?
Dave Yes.
Theo Well, that day may have come. I think I have discovered an interesting connec-
tion between DOP and science, and it has implications in the way we debug a
program.
Dave I’m curious.
Theo Do you believe in determinism?
Dave You mean that everything that happens in the universe is predestined and that
free will is an illusion?
Theo No, I don’t want to get into a philosophy. This is more of a scientific question.
Do you think that the same causes always produce the same effects?
Dave I think so. Otherwise, each time I use an elevator, I’d be scared to death that
the laws of physics have changed, and the elevator might go down instead of
up, or even crash!
Theo What about determinism in programming?
Dave How would you define causes and effects in programming?
Theo Let’s say, for the sake of simplicity, that in the context of programming, causes
are function arguments and effects are return values.
Dave What about side effects?
Theo Let’s leave them aside for now.
Dave What about the program state? I mean, a function could return a different
value for the same arguments if the program state changes.
Theo That’s why we should avoid state as much as possible.
Dave But you can’t avoid state in real-life applications!
Theo Right, but we can minimize the number of modules that deal with state. In fact,
that’s exactly what DOP has encouraged us to do: only the SystemState mod-
ule deals with state, and all other modules deal with immutable data.
Dave Then, I think that in modules that deal with immutable data, determinism as
you defined it holds. For the same arguments, a function will always return the
same value.
TIP In modules that deal with immutable data, function behavior is deterministic—the
same arguments always lead to the same return values.

=== 페이지 341 ===
15.1 Determinism in programming 313
Theo Perfect. Let’s give a name to the values of the function arguments that a function
is called with: the function run-time context or, in short, the function context.
Dave I think I see what you mean. In general, the function context should involve
both the function arguments and the program state. But in DOP, because we
deal with immutable data, a function context is made only of the values of the
function arguments.
TIP In DOP, the function context is made of the values of the function arguments.
Theo Exactly! Now, let’s talk about reproducibility. Let’s say that you want to capture
a function context and reproduce it in another environment.
Dave Could you be a bit more concrete about reproducing a function context in
another environment?
Theo Take, for example, a web service endpoint. You trigger the endpoint with some
parameters. Inside the program, down the stack, a function foo is called. Now,
you want to capture the context in which foo is called in order to reproduce
later the same behavior of foo.
Dave We deal with immutable data. So, if we call foo again with the same arguments,
it will behave the same.
Theo The problem is how do you know the values of the function arguments?
Remember that we didn’t trigger foo directly. We triggered the endpoint.
Dave That’s not a problem. You use a debugger and set a breakpoint inside the code of
foo, and you inspect the arguments when the program stops at the breakpoint.
Theo Let’s say foo receives three arguments: a number, a string, and a huge nested map.
How do you capture the arguments and replay foo with the same arguments?
Dave I am not sure what you mean exactly by replaying foo?
Theo I mean executing foo in the REPL.
 NOTE The REPL (Read Eval Print Loop), sometimes called language shell, is a pro-
gramming environment that takes pieces of code, executes them, and displays the
result. See table 15.1 for a list of REPLs for different programming languages.
Table 15.1 REPLs per programming language
JavaScript (Browser) Browser console
Node.js Node CLI
Java JShell
C# C# REPL
Python Python interpreter
Ruby Interactive Ruby
Dave Does the REPL have to be part of the process that I’m debugging?
Theo It doesn’t have to be. Think of the REPL as a scientific lab, where developers
perform experiments. Let’s say you’re using a separate process for the REPL.

=== 페이지 342 ===
314 CHAPTER 15 Debugging
Dave OK. For the number and the string, I can simply copy their values to the clip-
board, paste them to the REPL, and execute foo in the REPL with the same
arguments.
Theo That’s the easy part. What about the nested map?
Dave I don’t know. I don’t think I can copy a nested map from a debugger to the
clipboard!
Theo In fact, JavaScript debuggers can. For instance, in Chrome, there is a Copy
option that appears when you right-click on data that is displayed in the browser
console.
Dave I never noticed it.
Theo Even without that, you could serialize the nested map to a JSON string, copy
the string to the clipboard, and then paste the JSON string to the REPL.
Finally, you could deserialize the string into a hash map and call foo with it.
Dave Nice trick!
Theo I don’t think of it as a trick, but rather as a fundamental aspect of DOP: data is
represented with generic data structures.
Dave I see. It’s easy to serialize a generic data structure.
TIP In order to copy and paste a generic data structure, we serialize and deserialize it.
Theo You just discovered the two conditions for reproducibility in programming.
Dave The first one is that data should be immutable.
Theo Right, and the second one?
Dave It should be easy to serialize and deserialize any data.
TIP The two conditions for reproducibility in programming are immutability and
ease of (de)serialization.
15.2 Reproducibility with numbers and strings
Theo In fact, we don’t even need a debugger in order to capture a function context.
Dave But the function context is basically made of its arguments. How can you
inspect the arguments of a function without a debugger?
Theo By modifying the code of the function under investigation and printing the
serialization of the arguments to the console.
Dave I don’t get that.
Theo Let me show you what I mean with a function that deals with numbers.
Dave OK.
Theo Take for instance a function that returns the nth digit of a number.
Dave Oh no, I hate digit arithmetic!
Theo Don’t worry, we’ll find some code for it on the web.
Theo googles “nth digit of a number in JavaScript” and takes a piece of code from Stack-
Overflow that seems to work.

=== 페이지 343 ===
15.2 Reproducibility with numbers and strings 315
Listing15.1 Calculate the nth digit of a number
function nthDigit(a, n) {
return Math.floor((a / (Math.pow(10, n - 1)))) % 10;
}
Dave Do you understand how it works?
Theo Let’s see, dividing a by 10n–1 is like right-shifting it n–1 places. Then we need to
get the rightmost digit.
Dave And the last digit of a number is obtained by the modulo 10 operation?
Theo Right! Now, imagine that this function is called down the stack when some
endpoint is triggered. I’m going to modify it by adding context-capturing code.
Dave What’s that?
Theo Context-capturing code is code that we insert at the beginning of a function
body to print the values of the arguments. Let me edit the nthDigit code to
give you an example.
Listing15.2 Capturing a context made of numbers
function nthDigit(a, n) {
console.log(a);
console.log(n);
return Math.floor((a / (Math.pow(10, n - 1)))) % 10;
}
Dave It looks trivial.
Theo It is trivial for now, but it will get less trivial in a moment. Now, tell me what
happens when I trigger the endpoint.
Dave When the endpoint is triggered, the program will display the two numbers, a
and n, in the console.
Theo Exactly, and what would you have to do in order to replay the function in the
same context as when the endpoint was triggered?
Dave I would need to copy the values of a and n from the console, paste them into
the REPL, and call nthDigit with those two values.
Theo What makes you confident that when we run nthDigit in the REPL, it will
reproduce exactly what happened when the endpoint was triggered? Remem-
ber, the REPL might run in a separate process.
Dave I know that nthDigit depends only on its arguments.
Theo Good. Now, how can you be sure that the arguments you pass are the same as
the arguments that were passed?
Dave A number is a number!
Theo I agree with you. Let’s move on and see what happens with strings.
Dave I expect it to be exactly the same.
Theo It’s going to be almost the same. Let’s write a function that receives a sentence
and a prefix and returns true when the sentence contains a word that starts
with the prefix.

=== 페이지 344 ===
316 CHAPTER 15 Debugging
Dave Why would anyone ever need such a weird function?
Theo It could be useful for the Library Management System when a user wants to
find books whose title contains a prefix.
Dave Interesting. I’ll talk about that with Nancy. Anyway, coding such a function
seems quite obvious. I need to split the sentence string into an array of words
and then check whether a word in the array starts with the prefix.
Theo How are you going to check whether any element of the array satisfies the
condition?
Dave I think I’ll use Lodash filter and check the length of the returned array.
Theo That would work but it might have a performance issue.
Dave Why?
Theo Think about it for a minute.
Dave I got it! filter processes all the elements in the array rather than stopping
after the first match. Is there a function in Lodash that stops after the first
match?
Theo Yes, it’s called find.
Dave Cool. I’ll use that. Hang on.
Dave reaches over for his laptop and write the code to check whether a sentence contains a
word that starts with a prefix. After a brief period, he shows Theo his implementation of
hasWordStartingWith using _.find.
Listing15.3 Checking if a sentence contains a word starting with a prefix
function hasWordStartingWith(sentence, prefix) {
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo OK, now, please add the context-capturing code at the beginning of the function.
Dave Sure, let me edit this code a bit. Voilà!
Listing15.4 Capturing a context made of strings
function hasWordStartingWith(sentence, prefix) {
console.log(sentence);
console.log(prefix);
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo Let me inspect your code for a minute. I want to see what happens when I
check whether the sentence “I like the word reproducibility” contains a word that
starts with li.

=== 페이지 345 ===
15.2 Reproducibility with numbers and strings 317
Theo uses Dave’s laptop to examine Dave’s code. It returns true as expected, but it doesn’t
display to the console the text that Dave expected. He shares his surprise with Theo.
Listing15.5 Testing hasWordStartingWith
hasWordStartingWith("I like the word \"reproducibility\"", "li");
// It returns true
// It displays the following two lines:
// I like the word "reproducibility"
// li
Dave Where are the quotes around the strings? And where are the backslashes
before the quotes surrounding the word reproducibility?
Theo They disappeared!
Dave Why?
Theo When you print a string to the console, the content of the string is displayed
without quotes. It’s more human-readable.
Dave Bummer! That’s not good for reproducibility. So, after I copy and paste a
string I have to manually wrap it with quotes and backslashes.
Theo Fortunately, there is a simpler solution. If you serialize your string to JSON,
then it has the quotes and the backslashes. For instance, this code displays the
string you expected.
Listing15.6 Displaying to the console the serialization of a string
console.log(JSON.stringify(
"I like the word \"reproducibility\""));
// → "I like the word \"reproducibility\""
Dave I didn’t know that strings were considered valid JSON data. I thought only
objects and arrays were valid.
Theo Both compound data types and primitive data types are valid JSON data.
Dave Cool! I’ll fix the code in hasWordStartingWith that captures the string argu-
ments. Here you go.
Listing15.7 Capturing a context made of strings using JSON serialization
function hasWordStartingWith(sentence, prefix) {
console.log(JSON.stringify(sentence));
console.log(JSON.stringify(prefix));
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo Great! Capturing strings takes a bit more work than with numbers, but with
JSON they’re not too bad.
Dave Right. Now, I’m curious to see if using JSON serialization for context capturing
works well with numbers.

=== 페이지 346 ===
318 CHAPTER 15 Debugging
Theo It works. In fact, it works well with any data, whether it’s a primitive data type or
a collection.
Dave Nice!
Theo Next, I’ll show you how to use this approach to reproduce a real scenario that
happens in the context of the Library Management System.
Dave No more digit arithmetic?
Theo No more!
15.3 Reproducibility with any data
The essence of DOP is that it treats data as a first-class citizen. As a consequence, we
can reproduce any scenario that deals with data with the same simplicity as we repro-
duce a scenario that deals with numbers and strings.
Dave I just called Nancy to tell her about the improved version of the book search,
where a prefix could match any word in the book title.
Theo And?
Dave She likes the idea.
Theo Great! Let’s use this feature as an opportunity to exercise reproducibility with
any data.
Dave Where should we start?
Theo First, we need to add context-capturing code inside the function that does the
book matching.
Dave The function is Catalog.searchBooksByTitle.
Theo What are the arguments of Catalog.searchBooksByTitle?
Dave It has two arguments: catalogData is a big nested hash map, and query is a
string.
Theo Can you edit the code and add the context-capturing piece?
Dave Sure. What about this code?
Listing15.8 Capturing the arguments of Catalog.searchBooksByTitle
Catalog.searchBooksByTitle = function(catalogData, query) {
console.log(JSON.stringify(catalogData));
console.log(JSON.stringify(query));
var allBooks = _.get(catalogData, "booksByIsbn");
var queryLowerCased = query.toLowerCase();
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title")
.toLowerCase()
.startsWith(queryLowerCased);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
};

=== 페이지 347 ===
15.3 Reproducibility with any data 319
Theo Perfect. Now let’s trigger the search endpoint.
Theo triggers the search endpoint with the query “Watch,” hoping to get details about
Watchmen. When the endpoint returns, Theo opens the console and Dave can see two lines
of output.
Listing15.9 Console output when triggering the search endpoint
{"booksByIsbn":{"978-1982137274":{"isbn":"978-1982137274"\
,"title":"7 Habits of Highly Effective People","authorIds":\
["sean-covey","stephen-covey"]},"978-1779501127":{"isbn":\
"978-1779501127","title":"Watchmen","publicationYear":\
1987,"authorIds":["alan-moore", "dave-gibbons"]}},\
"authorsById":{"stephen-covey":{"name":"Stephen Covey",\
"bookIsbns":["978-1982137274"]},"sean-covey":{"name":"Sean Covey",\
"bookIsbns":["978-1982137274"]},"dave-gibbons":{"name":"Dave Gibbons",\
"bookIsbns":["978-1779501127"]},"alan-moore":{"name":"Alan Moore",\
"bookIsbns":["978-1779501127"]}}}
"Watch"
Dave I know that the first line contains the catalog data, but it’s really hard to read.
Theo That doesn’t matter too much. You only need to copy and paste it in order to
reproduce the Catalog.searchBooksByTitle call.
Dave Let me do that. Here.
Listing15.10 Reproducing a function call
var catalogData = {"booksByIsbn":{"978-1982137274":
{"isbn":"978-1982137274","title":"7 Habits of Highly Effective People",
"authorIds":["sean-covey","stephen-covey"]},"978-1779501127":
{"isbn":"978-1779501127","title":"Watchmen","publicationYear":1987,
"authorIds":["alan-moore","dave-gibbons"]}},"authorsById":
{"stephen-covey":{"name":"Stephen Covey","bookIsbns":
["978-1982137274"]},"sean-covey":{"name":"Sean Covey","bookIsbns":
["978-1982137274"]},"dave-gibbons":{"name":"Dave Gibbons","bookIsbns":
["978-1779501127"]},"alan-moore":{"name":"Alan Moore","bookIsbns":
["978-1779501127"]}}};
var query = "Watch";
Catalog.searchBooksByTitle(catalogData, query);
Theo Now that we have real catalog data in hand, we can do some interesting things
in the REPL.
Dave Like what?
Theo Like implementing the improved search feature without having to leave the
REPL.
TIP Reproducibility allows us to reproduce a scenario in a pristine environment.
Dave Without triggering the search endpoint?
Theo Exactly! We are going to improve our code until it works as desired, using the
short feedback loop that the console provides.

=== 페이지 348 ===
320 CHAPTER 15 Debugging
Dave Cool! In the catalog, we have the book, 7 Habits of Highly Effective People. Let’s
see what happens when we search books that match the word Habit.
Theo replaces the value of the query in listing 15.10 with "Habit". The code now
returns an empty array as in listing 15.11. This is expected because the current imple-
mentation only searches for books whose title starts with the query, whereas the title
starts with 7 Habits.
Listing15.11 Testing searchBooksByTitle
Catalog.searchBooksByTitle(catalogData, 'Habit');
// → []
Theo Would you like to implement the improved search?
Dave It’s not too hard; we have already implemented hasWordStartingWith. Here’s
the improved search.
Listing15.12 An improved version of book search
Catalog.searchBooksByTitle = function(catalogData, query) {
console.log(JSON.stringify(catalogData));
console.log(JSON.stringify(query));
var allBooks = _.get(catalogData, "booksByIsbn");
var matchingBooks = _.filter(allBooks, function(book) {
return hasWordStartingWith(_.get(book, "title"), query);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
};
Theo I like it. Let’s see if it works as expected.
Dave is about to trigger the search endpoint when suddenly Theo stops him. He says with
an authoritative tone:
Theo Dave, don’t do that!
Dave Don’t do what?
Theo Don’t trigger an endpoint to test your code.
Dave Why?
Theo Because the REPL environment gives you a much quicker feedback than trig-
gering the endpoint. The main benefit of reproducibility is to be able to repro-
duce the real-life conditions in a more effective environment.
Dave executes the code from his improved search with the word Habit. This time, however,
it returns the details about the book, 7 Habits of Highly Effective People.

=== 페이지 349 ===
15.4 Unit tests 321
Listing15.13 Testing searchBooksByTitle again
Catalog.searchBooksByTitle(catalogData, 'Habit');
// → [ { "title": "7 Habits of Highly Effective People", …}]
Dave It works!
Theo Let’s try more queries: abit and bit should not return any book, but habit
and 7 Habits should return only one book.
In the REPL, Dave tries the four queries that Theo suggested. For abit and bit, the code
works as expected, but for habit and 7 Habits it fails.
Dave Let me try to fix that code.
Theo I suggest that you instead write a couple of unit tests that check the various inputs.
Dave Good idea. Is there a way to use reproducibility in the context of unit tests?
Theo Absolutely!
15.4 Unit tests
Dave How do we use reproducibility in a unit test?
Theo As Joe told showed me so many times, in DOP, unit tests are really simple. They
call a function with some data, and they check that the data returned by the
function is the same as we expect.
Dave I remember that! I have written many unit tests for the Library Management
System following this approach. But sometimes, I struggled to provide input
data for the functions under test. For instance, building catalog data with all its
nested fields was not a pleasure.
Theo Here’s where reproducibility can help. Instead of building data manually, you
put the system under the conditions you’d like to test, and then capture data
inside the function under test. Once data is captured, you use it in your unit test.
Dave Nice! Let me write a unit test for Catalog.searchBooksByTitle following
this approach.
Dave triggers the search endpoint once again. Then, he opens the console and copies the
line with the captured catalog data to the clipboard. Finally, he pastes it inside the code of
the unit test.
Listing15.14 A unit test with captured data
var catalogData =
{"booksByIsbn":{"978-1982137274":{"isbn":"978-1982137274",
"title":"7 Habits of Highly Effective People","authorIds":["sean-covey",
"stephen-covey"]},"978-1779501127":{"isbn":"978-1779501127","title":
"Watchmen","publicationYear":1987,"authorIds":["alan-moore",
"dave-gibbons"]}},"authorsById":{"stephen-covey":{"name":
"Stephen Covey","bookIsbns":["978-1982137274"]},"sean-covey":
{"name":"Sean Covey","bookIsbns":["978-1982137274"]},"dave-gibbons":
{"name":"Dave Gibbons","bookIsbns":["978-1779501127"]},"alan-moore":
{"name":"Alan Moore","bookIsbns":["978-1779501127"]}}};
var query = "Habit";

=== 페이지 350 ===
322 CHAPTER 15 Debugging
var result = Catalog.searchBooksByTitle(catalogData, query);
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
_.isEqual(result, expectedResult);
// → true
Theo Well done! Now, would you like me to show you how to do the same without
copying and pasting?
Dave Definitely.
Theo Instead of displaying the captured data to the console, we’re going to write it to
a file and read data from that file inside the unit test.
Dave Where are you going to save the files that store captured data?
Theo Those files are part of the unit tests. They need to be under the same file tree
as the unit tests.
Dave There are so many files! How do we make sure a file doesn’t override an exist-
ing file?
Theo By following a simple file-naming convention. A name for a file that stores cap-
tured data is made of two parts: a context (for example, the name of the func-
tion where data was captured) and a universal unique identifier (a UUID).
Dave How do you generate a UUID?
Theo In some languages it’s part of the language, but in other languages like Java-
Script, you need a third-party library like uuid. Let me bookmark its site for you.
I also happen to have a list of libraries for UUIDs. I’ll send that table to you too.
Theo bookmarks the site for the third-party library uuid (https://github.com/uuidjs/
uuid) on Dave’s computer. Then, using his laptop, he finds his list and sends that to Dave.
Dave receives the email, and he takes a moment to quickly glance through the table 15.2
before turning his attention back to Theo.
Table 15.2 Libraries for UUID generation
Language UUID library
JavaScript https://github.com/uuidjs/uuid
Java java.util.UUID
C# Guid.NewGuid
Python uuid
Ruby SecureRandom

=== 페이지 351 ===
15.4 Unit tests 323
Theo The code for the dataFilePath function that receives a context and returns a
file path is fairly simple. Check this out.
Listing15.15 Computing the file path for storing captured data
var capturedDataFolder = "test-data";
The root folder
function dataFilePath(context) {
for captured data
var uuid = generateUUID();
return capturedDataFolder
UUID generation is language-
+ "/" + context
dependent (see table 15.2).
+ "-" + ".json";
}
Uses json as a file extension
because we serialize data to JSON
Dave How do we store a piece of data in a JSON file?
Theo We serialize it and write it to disk.
Dave Synchronously or asynchronously?
Theo I prefer to write to the disk asynchronously or in a separate thread in run times
that support multithreading to avoid slowing down the real work. Here’s my
implementation of dumpData.
Listing15.16 Dumping data in JSON format
function dumpData(data, context) {
var path = dataFilePath(context); Writes asynchronously
to prevent blocking
var content = JSON.stringify(data);
the real work
fs.writeFile(path, content, function () {
The third argument is a
console.log("Data for " +
callback function, called
context +
when write completes.
"stored in: " +
path);
Displays a message once
});
data is written to the file
}
Dave Let me see if I can use dumpData inside Catalog.searchBooksByTitle and
capture the context to a file. I think that something like this should work.
Listing15.17 Capturing the context into a file
Catalog.searchBooksByTitle = function(catalogData, query) {
dumpData([catalogData, query], 'searchBooksByTitle');
var allBooks = _.get(catalogData, "booksByIsbn");
var queryLowerCased = query.toLowerCase();
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title")
.toLowerCase()
.startsWith(queryLowerCased);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});

=== 페이지 352 ===
324 CHAPTER 15 Debugging
return bookInfos;
};
Theo Trigger the endpoint to see if it works.
Dave triggers the search endpoint once again and views the output in the console. When he
opens the file mentioned in the log message, he sees a single line that is hard to decipher.
Listing15.18 Console output when triggering the search endpoint
Data for searchBooksByTitle stored in
test-data/searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json
Listing15.19 The content of the JSON file that captured the context
[{"booksByIsbn":{"978-1982137274":{"isbn":"978-1982137274",
"title":"7 Habits of Highly Effective People","authorIds":
["sean-covey","stephen-covey"]},"978-1779501127":{"isbn":
"978-1779501127","title":"Watchmen","publicationYear":1987,
"authorIds":["alan-moore","dave-gibbons"]}},"authorsById":
{"stephen-covey":{"name":"Stephen Covey","bookIsbns":
["978-1982137274"]},"sean-covey":{"name":"Sean Covey",
"bookIsbns":["978-1982137274"]},"dave-gibbons":
{"name":"Dave Gibbons","bookIsbns":["978-1779501127"]},
"alan-moore":{"name":"Alan Moore","bookIsbns":
["978-1779501127"]}}},"Habit"]
Dave Reading this JSON file is very difficult!
Theo We can beautify the JSON string if you want.
Dave How?
Theo By passing to JSON.stringify the number of space characters to use for
indentation. How many characters would you like to use for indentation?
Dave Two.
After adding the number of indentation characters to the code of dumpData, Dave then
opens the JSON file mentioned in the log message (it’s a different file name!). He now
sees a beautiful JSON array with two elements.
Listing15.20 Dumping data in JSON format with indentation
The second argument to
function dumpData(data, context) {
JSON.stringify is ignored.
var path = dataFilePath(context);
The third argument to
var content = JSON.stringify(data, null, 2);
JSON.stringify specifies the
number of characters to
use for indentation.
fs.writeFile(path, content, function () {
console.log("Data for " + context + "stored in: " + path);
});
}

=== 페이지 353 ===
15.4 Unit tests 325
Listing15.21 The captured context with indentation in the JSON file
[
{
"booksByIsbn": {
"978-1982137274": {
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"authorIds": [
"sean-covey",
"stephen-covey"
]
},
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": [
"alan-moore",
"dave-gibbons"
]
}
},
"authorsById": {
"stephen-covey": {
"name": "Stephen Covey",
"bookIsbns": [
"978-1982137274"
]
},
"sean-covey": {
"name": "Sean Covey",
"bookIsbns": [
"978-1982137274"
]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": [
"978-1779501127"
]
},
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": [
"978-1779501127"
]
}
}
},
"Habit"
]

=== 페이지 354 ===
326 CHAPTER 15 Debugging
Dave While looking at the contents of the JSON file, I thought about the fact that we
write data to the file in an asynchronous way. It means that data is written con-
currently to the execution of the function code, right?
Theo Right! As I told you, we don’t want to slow down the real work.
Dave I get that. What happens if the code of the function modifies the data that we
are writing? Will we write the original data to the file or the modified data?
Theo I’ll let you think about that while I get a cup of tea at the museum coffee shop.
Would you like some coffee?
Dave What, you’re not having coffee?
Theo I finally found the time to read the book The Power of Habit by Charles Duhigg.
Joe read the book and quit biting his fingernails, so I decided to read it to cut
down on my habit of going for yet another cup of coffee.
Dave That’s impressive, but I’d like an espresso, please.
While Theo goes to the coffee shop, Dave explores the Wind Arrows exhibit outside the
auditorium. He’s hoping that his mind will be inspired by the beauty of science. He takes a
few breaths to relax, and after a couple of minutes, Dave has an Aha! moment. He knows
the answer to his question about the function changing data.
Theo comes back, gingerly carrying the hot beverages, and finds Dave in the audito-
rium. Dave smiles at Theo and says:
Dave In DOP, we never mutate data. Therefore, my question is no longer a ques-
tion: the code of the function cannot modify the data while we are writing it
to the file.
Theo You’ve got it! Now, let me show you how to use data from the JSON file in a
unit test. First, we need a function that reads data from a JSON file and deseri-
alizes it, probably something like readData.
Listing15.22 Reading data from a JSON file
function readData(path) {
return JSON.parse(fs.readFileSync(path));
}
Dave Why are you reading synchronously and not asynchronously like you did when
we captured the data?
Theo Because readData is meant to be used inside a unit test, and we cannot run
the test before the data is read from the file.
Dave That makes sense. Using readData inside a unit test seems straightforward. Let
me use it to read our captured data.
Listing15.23 A unit test that reads captured data from a file
var data = readData("test-data/" +
"searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json");
var catalogData = data[0];
var query = data[1];

=== 페이지 355 ===
15.4 Unit tests 327
var result = Catalog.searchBooksByTitle(catalogData, query);
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
_.isEqual(result, expectedResult);
// → false
Theo Do you prefer the version of the unit test with the inline data or with the data
read from the file?
Dave It depends. When data is minimal, I prefer to have the data inline because it
allows me to see the data. But when data is substantial, like the catalog data,
having the data inline makes the code hard to read.
Theo OK. Let’s fix the code of the improved search so that it works with the two que-
ries that return an empty result.
Dave I completely forgot about that. Do you remember those two queries?
Theo Yes, it was habit and 7 Habits.
Dave The first query doesn’t work because the code leaves the strings in their origi-
nal case. I can easily fix that by converting both the book title and the query to
lowercase.
Theo And what about the second query?
Dave It’s much harder to deal with because it’s made of two words. I somehow need
to check whether the title subsequently contains those two prefixes.
Theo Are you familiar with the \b regular expression metacharacter?
Dave No.
Theo \b matches a position that is called a word boundary. It allows us to perform pre-
fix matching.
Dave Cool. Can you give me an example?
Theo Sure. For instance, \bHabits and \b7 Habits match 7 Habits of Highly
Effective People, but abits won’t match.
Dave What about \bHabits of?
Theo It also matches.
Dave Excellent. This is exactly what I need! Let me fix the code of hasWordStart-
ingWith so that it does a case-insensitive prefix match.
Listing15.24 A revised version of hasWordStartingWith
function hasWordStartingWith(sentence, prefix) {
var sentenceLowerCase = sentence.toLowerCase();
var prefixLowerCase = prefix.toLowerCase();

=== 페이지 356 ===
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

=== 페이지 357 ===
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

=== 페이지 358 ===
330 CHAPTER 15 Debugging
Dave Are there databases like that for real?
Theo Yes. For instance, the Datomic immutable database is used by some digital
banks.
 NOTE See https://www.datomic.com for more information on the Datomic transac-
tional database.
Dave But most databases don’t provide such a guarantee!
Theo Right, but in practice, when we’re debugging an issue in our local environ-
ment, data usually doesn’t change.
Dave What do you mean?
Theo Take, for instance, Klafim’s database. In theory, between the time you trigger
the search endpoint and the time you replay the search code from the REPL
with the same context, a book might have been borrowed, and its availability
state in the database has changed. This leads to a difference response to the
search query.
Dave Exactly.
Theo But in practice, you are the only one that interacts with the system in your local
environment. Therefore, it should not happen.
Dave I see. Because we are at the Museum of Science, would you allow me an anal-
ogy with science?
Theo Of course!
Dave In a sense, external data sources are like hidden variables in quantum physics.
In theory, they can alter the result of an experiment for no obvious reason. But
in practice, our physical world looks stable at the macro level.
With today’s discussion at an end, Theo searches his bag to find a parcel wrapped with gift
wrap from the museum’s souvenir shop, which he hands to Dave with a smile. Dave opens
the gift to find a T-shirt. On one side there is an Albert Einstein avatar and his famous
quote: “God does not play dice with the universe”; on the other side, an avatar of Alan Kay
and his quote: “The last thing you want to do is to mess with internal state.”
Dave thanks Theo for his gift. Theo can feel a touch of emotion at the back of his
throat. He’s really enjoyed playing the role of mentor with Dave, a rather skilled student.
Farewell
A week after the meeting with Dave at the museum, Theo invites Joe and Nancy for his
farewell party at Albatross. This is the first time that Joe meets Nancy, and Theo takes the
opportunity to tell Nancy that if the Klafim project met its deadlines, it was thanks to Joe.
Everyone is curious about the name of the company Theo is going to work for, but no one
dares to ask him. Finally, it’s Dave who gets up the courage to ask.
Dave May I ask you what company are you going to work for?
Theo I’m going to take a break.

=== 페이지 359 ===
Summary 331
Dave Really?
Theo Yes. I’ll be traveling around the world for a couple of months.
Dave And after that, will you go back to work in programming?
Theo I’m not sure.
Dave Do you have other projects in mind?
Theo I’m thinking of writing a book.
Dave A book?
Theo Yes. DOP has been a meaningful journey for me. I have learned some interest-
ing lessons about reducing complexity in programming, and I would like to
share my story with the community of developers.
Dave Well, if you are as good of a storyteller as you are as a teacher, I am sure your
book will be a success.
Theo Thank you, Dave!
Monica, Dave, Nancy, Joe, and all the other Albatross employees raise their glasses to
Theo’s health and exclaim together, “Cheers! Here’s to a successful book.”
Summary
 We reproduce a scenario by capturing the context in which a function is called
and replaying it either in the REPL or in a unit test. In this chapter, we call it
context capturing.
 In DOP, a function context is made only of data.
 There are various locations to capture a function context—the clipboard, the
console, a file.
 We are able to capture a function’s context because data is represented with a
generic data structure and, therefore, it is easily serializable.
 Replaying a scenario in the REPL provides a short feedback loop that allows us
to be effective when we want to fix our code.
 When we execute a function with a captured context, the behavior of the func-
tion is guaranteed to be the same as long as it only manipulates immutable data
as specified by DOP.
 In modules that deal with immutable data, function behavior is deterministic—
the same arguments always lead to the same return values.
 The function context is made of the values of the function arguments.
 The REPL (Read Eval Print Loop), sometimes called language shell, is a pro-
gramming environment that takes pieces of code, executes them, and displays
the result.
 In order to copy and paste a generic data structure, we serialize and deserialize it.

=== 페이지 360 ===
332 CHAPTER 15 Debugging
 Reproducibility allows us to reproduce a scenario in a pristine environment.
 The two conditions for reproducibility in programming are immutability and
ease of (de)serialization.
Lodash functions introduced in this chapter
Function Description
find(coll, pred) Iterates over elements of coll, returning the first element for which pred
returns true
