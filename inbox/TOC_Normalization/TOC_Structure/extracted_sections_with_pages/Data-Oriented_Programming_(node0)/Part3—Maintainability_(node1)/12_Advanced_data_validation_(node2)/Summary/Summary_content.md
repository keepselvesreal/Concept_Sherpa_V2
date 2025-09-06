# Summary

**페이지**: 388-389
**계층**: Data-Oriented Programming (node0) > Part3—Maintainability (node1) > 12 Advanced data validation (node2)
**추출 시간**: 2025-08-06 19:47:19

---


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


--- 페이지 389 ---

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

--- 페이지 389 끝 ---
