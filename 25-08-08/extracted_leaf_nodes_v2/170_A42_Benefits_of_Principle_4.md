# A.4.2 Benefits of Principle #4

**메타데이터:**
- ID: 170
- 레벨: 2
- 페이지: 385-388
- 페이지 수: 4
- 부모 ID: 167
- 텍스트 길이: 8251 문자

---

f Principle #4
Separation of data schema from data representation provides numerous benefits. The
following sections describe these benefits in detail:
 Freedom to choose what data should be validated
 Optional fields
 Advanced data validation conditions
 Automatic generation of data model visualization
BENEFIT #1: FREEDOM TO CHOOSE WHAT DATA SHOULD BE VALIDATED
When data schema is separated from data representation, we can instantiate data with-
out specifying its expected shape. Such freedom is useful in various situations. For
example,
 Rapid prototyping or experimentation
 Code refactoring and data validation
Consider rapid prototyping. In classic OOP, we need to instantiate every piece of data
through a class. During the exploration phase of coding, when the final shape of our
data is not yet known, being forced to update the class definition each time the data
model changes slows us down. DOP enables a faster pace during the exploration
phase by delaying the data schema definition to a later phase.
One common refactoring pattern is split phase refactoring (https://refactoring
.com/catalog/splitPhase.html), where a single large function is split into multiple
smaller functions with private scope. We call these functions with data that has already
been validated by the larger function. In DOP, it is not necessary to specify the shape
of the arguments of the inner functions, relying on the data validation that has
already occurred.
Consider how to display some information about an author, such as their full name
and whether they are considered prolific. Using the code shown earlier to illustrate
Principle #2 to calculate the full name and the prolificity level of the author, one
might come up with a displayAuthorInfo function as the following listing shows.
ListingA.31 Displaying author information
class NameCalculation {
static fullName(data) {
return data.firstName + " " + data.lastName;
}
}
class AuthorRating {
static isProlific (data) {
return data.books > 100;
}
}
var authorSchema = {
"type": "object",

358 APPENDIX A Principles of data-oriented programming
"required": ["firstName", "lastName"],
"properties": {
"firstName": {"type": "string"},
"lastName": {"type": "string"},
"books": {"type": "integer"}
}
};
function displayAuthorInfo(authorData) {
if(!ajv.validate(authorSchema, authorData)) {
throw "displayAuthorInfo called with invalid data";
};
console.log("Author full name is: ",
NameCalculation.fullName(authorData));
if(authorData.books == null) {
console.log("Author has not written any book");
} else {
if (AuthorRating.isProlific(authorData)) {
console.log("Author is prolific");
} else {
console.log("Author is not prolific");
}
}
}
Notice that the first thing done inside the body of displayAuthorInfo is to validate
that the argument passed to the function. Now, apply the split phase refactoring pat-
tern to this simple example and split the body of displayAuthorInfo into two inner
functions:
 displayFullName displays the author’s full name.
 displayProlificity displays whether the author is prolific or not.
The next listing shows the resulting code.
ListingA.32 Application of split phase refactoring pattern
function displayFullName(authorData) {
console.log("Author full name is: ",
NameCalculation.fullName(authorData));
}
function displayProlificity(authorData) {
if(authorData.books == null) {
console.log("Author has not written any book");
} else {
if (AuthorRating.isProlific(authorData)) {
console.log("Author is prolific");
} else {
console.log("Author is not prolific");
}
}
}

A.4 Principle #4: Separate data schema from data representation 359
function displayAuthorInfo(authorData) {
if(!ajv.validate(authorSchema, authorData)) {
throw "displayAuthorInfo called with invalid data";
};
displayFullName(authorData);
displayProlificity(authorData);
}
Having the data schema separated from data representation eliminates the need to
specify a data schema for the arguments of the inner functions displayFullName and
displayProlificity. It makes the refactoring process a bit smoother. In some cases,
the inner functions are more complicated, and it makes sense to specify a data schema
for their arguments. DOP gives us the freedom to choose!
BENEFIT #2: OPTIONAL FIELDS
In OOP, allowing a class member to be optional is not easy. For instance, in Java one
needs a special construct like the Optional class introduced in Java 8 (http://mng.bz/
4jWa). In DOP, it is natural to declare a field as optional in a map. In fact, in JSON
Schema, by default, every field is optional.
In order to make a field not optional, its name must be included in the required
array as, for instance, in the author schema in listing A.33, where only firstName and
lastName are required, and books is optional. Notice that when an optional field is
defined in a map, its value is validated against the schema.
ListingA.33 A schema with an optional field
var authorSchema = { books is not included
in required, as it is an
"type": "object",
optional field.
"required": ["firstName", "lastName"],
"properties": {
"firstName": {"type": "string"},
"lastName": {"type": "string"}, When present, books
must be a number.
"books": {"type": "number"}
}
};
Let’s illustrate how the validation function deals with optional fields. A map without a
books field is considered to be valid as listing A.34 shows. Alternatively, a map with a
books field, where the value is not a number, is considered to be invalid as listing A.35
shows.
ListingA.34 A valid map without an optional field
var authorDataNoBooks = {
"firstName": "Yehonathan",
"lastName": "Sharvit"
}; The validation
passes, as books is
an optional field.
ajv.validate(authorSchema, authorDataNoBooks);
// → true

360 APPENDIX A Principles of data-oriented programming
ListingA.35 An invalid map with an invalid optional field
var authorDataInvalidBooks = {
"firstName": "Albert",
"lastName": "Einstein",
"books": "Five"
}; The validation fails,
as books is not a
number.
validate(authorSchema, authorDataInvalidBooks);
// → false
BENEFIT #3: ADVANCED DATA VALIDATION CONDITIONS
In DOP, data validation occurs at run time. It allows the definition of data validation
conditions that go beyond the type of a field. For example, validating that a field is not
only a string, but a string with a maximal number of characters or a number com-
prised in a range of numbers as well.
JSON Schema supports many other advanced data validation conditions such as
regular expression validation for string fields or number fields that should be a multi-
ple of a given number. The author schema in listing A.36 expects firstName and
lastName to be strings of less than 100 characters, and books to be a number between
0 and 10,000.
ListingA.36 A schema with advanced data validation conditions
var authorComplexSchema = {
"type": "object",
"required": ["firstName", "lastName"],
"properties": {
"firstName": {
"type": "string",
"maxLength": 100
},
"lastName": {
"type": "string",
"maxLength": 100
},
"books": {
"type": "integer",
"minimum": 0,
"maximum": 10000
}
}
};
BENEFIT #4: AUTOMATIC GENERATION OF DATA MODEL VISUALIZATION
With the data schema defined as data, we can use several tools to generate data model
visualizations. With tools like JSON Schema Viewer (https://navneethg.github.io/
jsonschemaviewer/) and Malli (https://github.com/metosin/malli), a UML diagram
can be generated from a JSON schema.

A.4 Principle #4: Separate data schema from data representation 361
For instance, the JSON schema in listing A.37 defines the shape of a bookList
field, which is an array of books where each book is a map, and in figure A.4, it is visu-
alized as a UML diagram. These tools generate the UML diagram from the JSON
schema.
ListingA.37 A JSON schema with an array of objects
{
"type": "object",
"required": ["firstName", "lastName"],
"properties": {
"firstName": {"type": "string"},
"lastName": {"type": "string"},
"bookList": {
"type": "array",
"items": {
"type": "object",
"properties": {
"title": {"type": "string"},
"publicationYear": {"type": "integer"}
}
}
}
}
}
C Author
firstName: String
lastName: String
bookList: <Book>
C Book
title : String
Figure A.4 A UML visualization of the
publicationYear: Int
JSON schema in listing A.37