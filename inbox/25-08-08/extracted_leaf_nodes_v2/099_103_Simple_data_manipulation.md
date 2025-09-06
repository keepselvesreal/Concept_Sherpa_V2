# 10.3 Simple data manipulation

**메타데이터:**
- ID: 99
- 레벨: 2
- 페이지: 235-238
- 페이지 수: 4
- 부모 ID: 95
- 텍스트 길이: 6421 문자

---

manipulation 207
10.3 Simple data manipulation
Quite often, in a production application, we need to reshape data fetched from the
database. The simplest case is when we need to rename the columns from the data-
base to those that are more appropriate for our application.
Joe Did you notice that the column names in our database follow the snake case
convention?
Theo I’m so used to the convention, no. I didn’t even think about that.
Joe Well, for instance, the column for the publication year of a book is called
publication_year.
Theo Go on...
Joe Inside JSON, I like to use Pascal case, like publicationYear.
Theo And I’d prefer to have bookTitle instead of title.
Joe So we’re both unhappy with the JSON string that searchBooks returns if we
pass the data retrieved from the database as is.
Theo Indeed!
Joe How would you fix it?
Theo I would modify the SQL query so that it renames the columns in the results.
Here, let me show you the query.
Listing10.11 Renaming columns inside the SQL query
SELECT
title AS bookTitle,
isbn,
publication_year AS publicationYear
FROM
books
WHERE title LIKE '%habit%';
Joe That would work, but it seems a bit weird to modify an SQL query so that it fits
the naming convention of the application.
Theo Yeah, I agree. I imagine a database like MongoDB doesn’t make it easy to
rename the fields inside a query.
Joe Yep. Sometimes it makes more sense to deal with field names in application
code. How would you handle that?
Theo Well, in that case, for every map returned by the database query, I’d use a func-
tion to modify the field names.
Joe Could you show me what the code would look like?
Theo Sure. How about this?
Listing10.12 Renaming specific keys in a list of maps
function renameBookInfoKeys(bookInfo) {
return {

208 CHAPTER 10 Database operations
"bookTitle": _.get(bookInfo, "title"),
"isbn": _.get(bookInfo, "isbn"),
"publicationYear": _.get(bookInfo, "publication_year")
};
}
var bookResults = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"publication_year": 1989
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"publication_year": 2012
}
];
_.map(bookResults, renameBookInfoKeys);
Joe Would you write a similar piece of code for every query that you fetched from
the database?
Theo What do you mean?
Joe Suppose you want to rename the fields returned by a query that retrieves the
books a user has borrowed.
Theo I see. I’d write a similar piece of code for each case.
Joe In DOP, we can use the fact that a field name is just a string and write a generic
function called renameResultKeys that works on every list of maps.
Theo Wow! How does renameResultKeys know what fields to rename?
Joe You pass the mapping between the old and the new names as a map.
TIP In DOP, field names are just strings. It allows us to write generic functions to
manipulate a list of maps that represent data fetched from the database.
Theo Could you show me an example?
Joe Sure. A map like this can be passed to renameResultKeys to rename the fields
in the book search results. So, for example, you could write renameResult-
Keys like this.
Listing10.13 Renaming fields in SQL results
renameResultKeys(bookResults, {
"title": "bookTitle",
"publication_year": "publicationYear"
});
Theo What happened to the field that stores the isbn?
Joe When a field is not mentioned, renameResultKeys leaves it as-is.

10.3 Simple data manipulation 209
Theo Awesome! Can you show me the implementation of renameResultKeys?
Joe Sure, it’s only about map and reduce, so I’d do something like the following.
Listing10.14 Renaming the keys in SQL results
function renameKeys(map, keyMap) {
return _.reduce(keyMap,
function(res, newKey, oldKey) {
var value = _.get(map, oldKey);
var resWithNewKey = _.set(res, newKey, value);
var resWithoutOldKey = _.omit(resWithNewKey, oldKey);
return resWithoutOldKey;
},
map);
}
function renameResultKeys(results, keyMap) {
return _.map(results, function(result) {
return renameKeys(result, keyMap);
});
}
Theo That code isn’t exactly easy to understand!
Joe Don’t worry. The more you write data manipulation functions with map, filter,
and reduce, the more you get used to it.
Theo I hope so!
Joe What’s really important for now is that you understand what makes it possible
in DOP to write a function like renameResultKeys.
Theo I would say it’s because fields are accessible dynamically with strings.
Joe Exactly. You could say that fields are first-class citizens.
TIP In DOP, fields are first-class citizens.
Theo How would you write unit tests for a data manipulation function like rename-
ResultKeys?
Joe It’s similar to the unit tests we wrote earlier. You generate input and expected
results, and you make sure that the actual results equal the expected results.
Hang on; this may take a while.
While Joe is busy coding, Theo takes this opportunity to run to the kitchen and prepare
two espressos. What luck! There’s a box of Swiss chocolates on the counter. He grabs a cou-
ple of pieces and returns to his office just as Joe is finishing up the unit test.
Listing10.15 Unit test for renameResultKeys
var listOfMaps = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",

210 CHAPTER 10 Database operations
"publication_year": 1989
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"publication_year": 2012
}
];
var expectedResults = [
{
"bookTitle": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"publicationYear": 1989
},
{
"bookTitle": "The Power of Habit",
"isbn": "978-0812981605",
"publicationYear": 2012
}
];
var results = renameResultKeys(listOfMaps,
{"title": "bookTitle",
"publication_year": "publicationYear"});
_.isEqual(expectedResults, results);
Theo Nice!
Joe Do you see why you’re free to use renameResultKeys with the results of any
SQL query?
Theo Yes, because the code of renameResultKeys is decoupled from the internal
details of the representation of data it operates on.
Joe Exactly! Now, suppose an SQL query returns user info in a table. How would
you use renameResultKeys to rename email to userEmail? Assume the table
looks like this (table 10.5).
Once again, the whiteboard comes in to play. When he’s finished, Joe shows Theo the
table.
Table 10.5 Results of an SQL query that returns email and
encrypted_password of some users
email encrypted_password
jennie@gmail.com secret-pass
franck@hotmail.com my-secret
Theo That’s easy!