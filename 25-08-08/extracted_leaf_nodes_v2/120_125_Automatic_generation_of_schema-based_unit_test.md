# 12.5 Automatic generation of schema-based unit tests

**메타데이터:**
- ID: 120
- 레벨: 2
- 페이지: 290-296
- 페이지 수: 7
- 부모 ID: 114
- 텍스트 길이: 10430 문자

---

eneration of schema-based unit tests
Joe Once you’ve defined a data schema for function arguments and for its return
value, it’s quite simple to generate a unit test for this function.
Dave How?
Joe Well, think about it. What’s the essence of a unit test for a function?
Dave A unit test calls a function with some arguments and checks whether the func-
tion returns the expected value.
Joe Exactly! Now, let’s adapt it to the context of data schema and DOP. Let’s say you
have a function with a schema for their arguments and for their return value.

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