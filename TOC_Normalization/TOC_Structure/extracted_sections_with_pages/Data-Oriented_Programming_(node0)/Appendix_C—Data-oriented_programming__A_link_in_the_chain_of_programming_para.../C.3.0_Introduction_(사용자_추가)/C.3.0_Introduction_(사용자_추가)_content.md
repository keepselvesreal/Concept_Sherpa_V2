# C.3.0 Introduction (사용자 추가)

**페이지**: 385-386
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:45

---


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
