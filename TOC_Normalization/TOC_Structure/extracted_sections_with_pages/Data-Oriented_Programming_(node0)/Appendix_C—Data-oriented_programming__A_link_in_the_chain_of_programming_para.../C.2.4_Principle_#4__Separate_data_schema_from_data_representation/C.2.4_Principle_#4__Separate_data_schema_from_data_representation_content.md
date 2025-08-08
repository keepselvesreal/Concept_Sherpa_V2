# C.2.4 Principle #4: Separate data schema from data representation

**페이지**: 384-385
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:45

---


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


--- 페이지 385 ---

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

--- 페이지 385 끝 ---
