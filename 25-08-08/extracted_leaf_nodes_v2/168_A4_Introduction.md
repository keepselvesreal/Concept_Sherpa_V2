# A.4 Introduction

**메타데이터:**
- ID: 168
- 레벨: 2
- 페이지: 383-384
- 페이지 수: 2
- 부모 ID: 167
- 텍스트 길이: 7989 문자

---

=== Page 382 ===
354 APPENDIX A Principles of data-oriented programming
TIP Adherence to data immutability eliminates the need for a concurrency mecha-
nism. The data you have in hand never changes!
A.3.3 Cost for Principle #3
As with the previous principles, applying Principle #3 comes at a price. The following
sections look at these costs:
 Performance hit
 Required library for persistent data structures
COST #1: PERFORMANCE HIT
As mentioned earlier, implementations of persistent data structures exist in most pro-
gramming languages. But even the most efficient implementation is a bit slower than
the in-place mutation of the data. In most applications, the performance hit and the
additional memory consumption involved in using immutable data structures is not
significant. But this is something to keep in mind.
COST #2: REQUIRED LIBRARY FOR PERSISTENT DATA STRUCTURES
In a language like Clojure, the native data structures of the language are immutable. How-
ever, in most programming languages, adhering to data immutability requires the inclu-
sion a third-party library that provides an implementation of persistent data structures.
The fact that the data structures are not native to the language means that it is dif-
ficult (if not impossible) to enforce the usage of immutable data across the board.
Also, when integrating with third-party libraries (e.g., a chart library), persistent data
structures must be converted into equivalent native data structures.
A.3.4 Summary of Principle #3
DOP considers data as a value that never changes. Adherence to this principle results
in code that is predictable even in a multi-threaded environment, and equality checks
are fast. However, a non-negligible mind shift is required, and in most programming
languages, a third-party library is needed to provide an efficient implementation of
persistent data structures.
DOP Principle #3: Data is immutable
To adhere to this principle, data is represented with immutable structures. The fol-
lowing diagram provides a visual representation of this.
DOPPrinciple #3: Data is immutable
Mutable
Data
Immutable

=== Page 383 ===
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

=== Page 384 ===
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

=== Page 385 ===
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