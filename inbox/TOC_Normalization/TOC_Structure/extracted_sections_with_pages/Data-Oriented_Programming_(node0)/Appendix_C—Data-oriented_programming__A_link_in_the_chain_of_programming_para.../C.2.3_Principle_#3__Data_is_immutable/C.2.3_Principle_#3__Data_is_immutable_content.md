# C.2.3 Principle #3: Data is immutable

**페이지**: 383-384
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:45

---


--- 페이지 383 ---

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

--- 페이지 383 끝 ---


--- 페이지 384 ---

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

--- 페이지 384 끝 ---
