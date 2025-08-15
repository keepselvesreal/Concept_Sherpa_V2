# A.4 Principle #4: Separate data schema from data representation

**Level:** 1
**페이지 범위:** 383 - 390
**총 페이지 수:** 8
**ID:** 167

---

=== 페이지 383 ===
A.4 Principle #4: Separate data schema from data representation 355
 Benefits include
– Data access to all with confidence
– Predictable code behavior
– Fast equality checks
– Concurrency safety for free
 The cost for implementing Principle #3 includes
– A performance hit
– Required library for persistent data structures
A.4 Principle #4: Separate data schema from data
representation
With data separated from code and represented with generic and immutable data
structures, now comes the question of how do we express the shape of the data? In
DOP, the expected shape is expressed as a data schema that is kept separated from the
data itself. The main benefit of Principle #4 is that it allows developers to decide
which pieces of data should have a schema and which pieces of data should not.
PRINCIPLE #4 Separate data schema from data representation.
A.4.1 Illustration of Principle #4
Think about handling a request for the addition of an author to the system. To keep things
simple, imagine that such a request contains only basic information about the author:
their first name and last name and, optionally, the number of books they have written. As
seen in Principle #2 (represent data with generic data structures), in DOP, request data
is represented as a string map, where the map is expected to have three fields:
 firstName—a string
 lastName—a string
 books—a number (optional)
In DOP, the expected shape of data is represented as data that is kept separate from the
request data. For instance, JSON schema (https://json-schema.org/) can represent the
data schema of the request with a map. The following listing provides an example.
ListingA.28 The JSON schema for an addAuthor request data
Data is expected to be a map (in JSON,
a map is called an object).
Only firstName and
var addAuthorRequestSchema = {
lastName fields are
"type": "object",
required.
"required": ["firstName", "lastName"],

=== 페이지 384 ===
356 APPENDIX A Principles of data-oriented programming
"properties": {
"firstName": {"type": "string"},
firstName must
"lastName": {"type": "string"},
be a string.
"books": {"type": "integer"}
}
books must be a number lastName must
};
(when it is provided). be a string.
A data validation library is used to check whether a piece of data conforms to a data
schema. For instance, we could use Ajv JSON schema validator (https://ajv.js.org/) to
validate data with the validate function that returns true when data is valid and
false when data is invalid. The following listing shows this approach.
ListingA.29 Data validation with Ajv
var validAuthorData = {
firstName: "Isaac",
lastName: "Asimov",
books: 500
};
ajv.validate(addAuthorRequestSchema,
validAuthorData); //
Data is
// → true
valid.
var invalidAuthorData = {
firstName: "Isaac",
lastNam: "Asimov",
books: "five hundred"
};
Data has lastNam instead
of lastName, and books is a
ajv.validate(addAuthorRequestSchema,
string instead of a number.
invalidAuthorData);
// → false
When data is invalid, the details about data validation failures are available in a human
readable format. The next listing shows this approach.
ListingA.30 Getting details about data validation failure
var invalidAuthorData = {
firstName: "Isaac", By default, Ajv stores only
the first data validation
lastNam: "Asimov",
error. Set allErrors: true
books: "five hundred"
to store all errors.
};
var ajv = new Ajv({allErrors: true}); Data validation errors are
stored internally as an
ajv.validate(addAuthorRequestSchema, invalidAuthorData);
array. In order to get a
ajv.errorsText(ajv.errors);
human readable string, use
// → "data should have required property 'lastName',
the errorsText function.
// → data.books should be number"

=== 페이지 385 ===
A.4 Principle #4: Separate data schema from data representation 357
A.4.2 Benefits of Principle #4
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

=== 페이지 386 ===
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

=== 페이지 387 ===
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

=== 페이지 388 ===
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

=== 페이지 389 ===
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
A.4.3 Cost for Principle #4
Applying Principle #4 comes with a price. The following sections look at these costs:
 Weak connection between data and its schema
 Small performance hit
COST #1: WEAK CONNECTION BETWEEN DATA AND ITS SCHEMA
By definition, when data schema and data representation are separated, the connec-
tion between data and its schema is weaker than when data is represented with classes.
Moreover, the schema definition language (e.g., JSON Schema) is not part of the

=== 페이지 390 ===
362 APPENDIX A Principles of data-oriented programming
programming language. It is up to the developer to decide where data validation is
necessary and where it is superfluous. As the idiom says, with great power comes great
responsibility.
COST #2: LIGHT PERFORMANCE HIT
As mentioned earlier, implementations of JSON schema validation exist in most
programming languages. In DOP, data validation occurs at run time, and it takes
some time to run the data validation. In OOP, data validation usually occurs at com-
pile time.
This drawback is mitigated by the fact that, even in OOP, some parts of data valida-
tion occur at run time. For instance, the conversion of a request JSON payload into an
object occurs at run time. Moreover, in DOP, it is quite common to have some data val-
idation parts enabled only during development and to disable them when the system
runs in production. As a consequence, this performance hit is not significant.
A.4.4 Summary of Principle #4
In DOP, data is represented with immutable generic data structures. When additional
information about the shape of the data is required, a data schema can be defined
(e.g., using JSON Schema). Keeping the data schema separate from the data repre-
sentation gives us the freedom to decide where data should be validated.
Moreover, data validation occurs at run time. As a consequence, data validation
conditions that go beyond the static data types (e.g., the string length) can be expressed.
However, with great power comes great responsibility, and it is up to the developer to
remember to validate data.
DOP Principle #4: Separate between data schema and data representation
To adhere to this principle, separate between data schema and data representation.
The following diagram illustrates this.
DOPPrinciple #4: Separate between data
schema and data representation
Representation
Data
Schema
 Benefits include
– Freedom to choose what data should be validated
– Optional fields
– Advanced data validation conditions
– Automatic generation of data model visualization
