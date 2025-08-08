# C.3.2 Data-driven programming

**페이지**: 386-387
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:47

---


--- 페이지 386 ---

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

--- 페이지 386 끝 ---


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
