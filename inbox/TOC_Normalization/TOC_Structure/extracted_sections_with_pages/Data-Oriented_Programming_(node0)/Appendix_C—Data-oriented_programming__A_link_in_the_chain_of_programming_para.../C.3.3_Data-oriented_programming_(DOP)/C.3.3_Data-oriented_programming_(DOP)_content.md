# C.3.3 Data-oriented programming (DOP)

**페이지**: 387-388
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:47

---


--- 페이지 387 ---

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

--- 페이지 387 끝 ---


--- 페이지 388 ---

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

--- 페이지 388 끝 ---
