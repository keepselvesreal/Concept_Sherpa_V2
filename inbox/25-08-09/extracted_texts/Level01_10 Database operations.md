# 10 Database operations

**Level:** 1
**페이지 범위:** 225 - 247
**총 페이지 수:** 23
**ID:** 95

---

=== 페이지 225 ===
Database operations
A cloud is a cloud
This chapter covers
 Fetching data from the database
 Storing data in the database
 Manipulating data fetched from the database
Traditionally in OOP, we use design patterns and complex layers of objects to struc-
ture access to the database. In DOP, we prefer to represent data fetched from the
database with generic data collections, namely, lists of maps, where fields in the
maps correspond to database column values. As we’ll see throughout the chapter,
the fact that fields inside a map are accessible dynamically via their names allows us
to use the same generic code for different data entities.
TIP The best way to manipulate data is to represent data as data.
In this chapter, we’ll illustrate the application of data-oriented principles when
accessing data from a relational database. Basic knowledge of relational database
and SQL query syntax (like SELECT, AS, WHERE, and INNER JOIN) is assumed. This
approach can be easily adapted to NoSQL databases.
197

=== 페이지 226 ===
198 CHAPTER 10 Database operations
Applications that run on the server usually store data in a database. In DOP, we
represent data retrieved from the database the same way we represent any other data
in our application—with generic data collections. This leads to
 Reduced system complexity.
 Increased genericity.
10.1 Fetching data from the database
Theo and Joe go for a walk in a park near the office. They sit on a bench close to a beau-
tiful lake and gaze at the clouds in the sky. After a couple of minutes of meditative
silence, Joe asks Theo, “What do you see?” Theo tells him that this cloud looks to him
like a horse, and that one looks like a car. On their way back to the office, Theo asks Joe
for an explanation about the clouds. Joe answers with a mysterious smile on his lips, “A
cloud is a cloud.”
Theo So far you’ve shown me how DOP represents data that lives in the memory of
the application. What about data that comes from the outside?
Joe What do you mean by outside?
Theo Data that comes from the database.
Joe I’ll return the question to you. How do you think that we should represent data
that comes from the database in DOP?
Theo As generic data collections, I guess.
Joe Exactly! In DOP, we always represent data with generic data collections.
Theo Does that mean that we can manipulate data from the database with the same
flexibility as we manipulate in-memory data?
Joe Definitely.
TIP In DOP, we represent data from the database with generic data collections, and
we manipulate it with generic functions.
Theo Would you show me how to retrieve book search results when the catalog data
is stored in an SQL database?
Joe I’ll show you in a moment. First, tell me how you would design the tables that
store catalog data.
Theo Do you mean the exact table schemas with the information about primary keys
and nullability of each and every column?
Joe No, I only need a rough overview of the tables, their columns, and the relation-
ships between the tables.
Theo goes to the whiteboard. Figure 10.1 shows the diagram he draws as he explains his
thinking to Joe.

=== 페이지 227 ===
10.1 Fetching data from the database 199
T books
T authors
isbn VARCHAR[32]
id VARCHAR[64]
title VARCHAR[64]
name VARCHAR[64]
publication_year INTEGER
1
A book 1 An author
may have may author
many authors. many books.
* *
book_authors
T (relationships of books and authors)
book_isbn VARCHAR[32] Figure 10.1 The database model
author_id VARCHAR[64]
for books and authors
Theo I have a books table with three columns: title, isbn, and publication_
year. I also have an authors table with two columns: for id and name. Here,
let me draw these tables on the whiteboard to give you a visual (see tables 10.1
and 10.2).
Table 10.1 The books table filled with two books
title isbn publication_year
The Power of Habit 978-0812981605 2012
7 Habits of Highly Effective People 978-1982137274 1989
Table 10.2 The authors table filled with three authors
id name
sean-covey Sean Covey
stephen-covey Stephen Covey
charles-duhigg Charles Duhigg
Joe What about the connection between books and authors?
Theo Let’s see, a book could be written by multiple authors, and an author could write
multiple books. Therefore, I need a many-to-many book_authors table that con-
nects authors and books with two columns, book_isbn and author_id.
Theo once again turns to the whiteboard. He pens the book_authors table 10.3 to show Joe.
Table 10.3 The book_authors table with rows connecting books with their authors
book_isbn author_id
978-1982137274 sean-covey
978-1982137274 stephen-covey
978-0812981605 charles-duhigg

=== 페이지 228 ===
200 CHAPTER 10 Database operations
Joe Great! Let’s start with the simplest case. We’re going to write code that searches
for books matching a title and that returns basic information about the books.
By basic information, I mean title, ISBN, and publication year.
Theo What about the book authors?
Joe We’ll deal with that later, as it’s a bit more complicated. Can you write an SQL
query for retrieving books that contain he word habit in their title?
Theo Sure.
This assignment is quite easy for Theo. First, he jots down the SQL query, then he displays
the results in table 10.4.
Listing10.1 SQL query to retrieve books whose title contains habit
SELECT
title,
isbn,
publication_year
FROM
books
WHERE title LIKE '%habit%';
Table 10.4 Results of the SQL query for books whose title contains the word habit
title isbn publication_year
The Power of Habit 978-0812981605 2012
7 Habits of Highly Effective People 978-1982137274 1989
Joe How would you describe these results as a data collection?
Theo I would say it’s a list of maps.
TIP In DOP, accessing data from a NoSQL database is similar to the way we access
data from a relational database.
Joe Right! Now, can you write the search results as a list of maps?
Theo It doesn’t sound too complicated. How about this?
Listing10.2 Search results as a list of maps
[
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
]

=== 페이지 229 ===
10.1 Fetching data from the database 201
Joe What about the JSON schema for the search results?
Theo It shouldn’t be too difficult if you allow me to take a look at the JSON schema
cheat sheet you kindly offered me the other day.
Joe Of course. The purpose of a gift is to be used by the one who receives it.
Theo takes a look at the JSON Schema cheat sheet to refresh his memory about the JSON
Schema syntax. After a few minutes, Theo comes up with a schema for the search results.
He certainly is putting Joe’s gift to good use.
Listing10.3 JSON schema cheat sheet
{
"type": "array",
"items": {
"type": "object",
"properties": {
"myNumber": {"type": "number"},
"myString": {"type": "string"},
"myEnum": {"enum": ["myVal", "yourVal"]},
"myBool": {"type": "boolean"}
},
"required": ["myNumber", "myString"],
"additionalProperties": false
}
}
Listing10.4 The JSON schema for search results from the database
var dbSearchResultSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["title", "isbn", "publication_year"],
"properties": {
"title": {"type": "string"},
"isbn": {"type": "string"},
"publication_year": {"type": "integer"}
}
}
};
Joe Excellent. Now I’m going to show you how to implement searchBooks in a
way that fetches data from the database and returns a JSON string with the
results. The cool thing is that we’re only going to use generic data collections
from the database layer down to the JSON serialization.
Theo Will it be similar to the implementation of searchBooks that we wrote when
you taught me the basis of DOP?
Joe Absolutely. The only difference is that then the state of the system was stored
locally, and we queried it with a function like _.filter. Now, we use SQL

=== 페이지 230 ===
202 CHAPTER 10 Database operations
queries to fetch the state from the database. In terms of data representation
and manipulation, it’s exactly the same.
Joe goes to the whiteboard and sketches out the data flow in figure 10.2. Theo studies the
diagram.
Database
Database driver
Data (list of maps)
Data manipulation
Data Figure 10.2 Data flow for serving
a request that fetches data from
JSON serialize
the database
Joe The data manipulation step in the diagram is implemented via generic func-
tions that manipulate data collections. As our examples get more elaborate, I
think you’ll see the benefits of being able to manipulate data collections with
generic functions.
Theo Sounds intriguing...
Joe For the communication with the database, we use a driver that returns a list of
maps. In JavaScript, you could use an SQL driver like node-postgres.
 NOTE See https://node-postgres.com for more information about this collection of
node.js modules for interfacing with PostgreSQL databases.
Theo And in Java?
Joe In Java, you could use JDBC (Java database connectivity) in addition to a small
utility function that converts a JDBC result set into a list of maps. If I can use
your laptop, I’ll show you what I mean.
Joe pulls a piece of code from one of his personal GitHub repositories. He then shows the
code for the JDBC conversion to Theo, who seems a bit surprised.
Listing10.5 Converting a JDBC result set into a list of hash maps
List<Map<String, Object>> convertJDBCResultSetToListOfMaps(ResultSet rs) {
List<Map<String, Object>> listOfMaps =
new ArrayList<Map<String, Object>>();
ResultSetMetaData meta = rs.getMetaData();
while (rs.next()) {
Map map = new HashMap();
for (int i = 1; i <= meta.getColumnCount(); i++) {
String key = meta.getColumnLabel(i);
Object value = rs.getObject(i);

=== 페이지 231 ===
10.1 Fetching data from the database 203
map.put(key, value);
}
listOfMaps.add(map);
}
return listOfMaps;
}
TIP Converting a JDBC result set into a list of hash maps is quite straightforward.
Theo I expected it to be much more complicated to convert a JDBC result set into a
list of hash maps.
Joe It’s straightforward because, in a sense, JDBC is data-oriented.
Theo What about the field types?
Joe When we convert a JDBC result set into a list of maps, each value is considered
an Object.
Theo That’s annoying because it means that in order to access the value, we need to
cast it to its type.
Joe Yes and no. Look at our book search use case. We pass all the values along with-
out really looking at their type. The concrete value type only matters when we
serialize the result into JSON and that’s handled by the JSON serialization
library. It’s called late binding.
 NOTE With late binding, we defer dealing with data types as long as possible.
Theo Does that mean in my application that I’m allowed to manipulate data without
dealing with concrete types?
TIP In DOP, flexibility is increased as many parts of the system are free to manipulate
data without dealing with concrete types.
Joe Exactly. You’ll see late binding in action in a moment. That’s one of the great-
est benefits of DOP.
Theo Interesting, I can’t wait to see that!
Joe One last thing before I show you the code for retrieving search results from the
database. In order to make it easier to read, I’m going to write JavaScript code
as if JavaScript were dealing with I/O is a synchronous way.
Theo What do you mean?
Joe In JavaScript, an I/O operation like sending a query to the database is done
asynchronously. In real life, it means using either callback functions or using
async and await keywords.
Theo Oh yeah, that’s because JavaScript is single-threaded.
 NOTE For sake of simplicity, the JavaScript snippets in this chapter are written as if
JavaScript were dealing with I/O in a synchronous way. In real-life JavaScript, we need
to use async and await around I/O calls.
Joe Indeed, so I’ll be writing the code that communicates with the database as
though JavaScript were dealing with I/O synchronously. Here’s an example.

=== 페이지 232 ===
204 CHAPTER 10 Database operations
Listing10.6 Searching books in the database, returning the results in JSON
dbClient holds the Initializes Ajv (a JSON schema validation
var dbClient; DB connection. library) with allErrors: true to catch all
the data validation errors
var ajv = new Ajv({allErrors: true});
var title = "habit";
var matchingBooksQuery = `SELECT title, isbn Uses a parameterized
SQL query as a security
FROM books
best practice
WHERE title LIKE '%$1%'`;
var books = dbClient.query(matchingBooksQuery,
Passes the parameters to the SQL
[title]);
query as a list of values (in our
if(!ajv.validate(dbSearchResultSchema, books)) {
case, a list with a single value)
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from the database: " + errors;
}
JSON.stringify(books);
Theo In a dynamically-typed language like JavaScript, I understand that the types of
the values in the list of maps returned by dbClient.query are determined at
run time. How does it work in a statically-typed language like Java, and what are
the types of the data fields in books?
Joe The function convertJDBCResultSetToListOfMaps we created earlier (see
listing 10.5) returns a list of Map<String, Object>. But JSON serialization
libraries like Gson know how to detect at run time the concrete type of the val-
ues in a map and serialize the values according to their type.
 NOTE See https://github.com/google/gson for information about Gson’s Java
serialization/deserialization library.
Theo What do you mean by serializing a value according to its type?
Joe For instance, the value of the field publication_year is a number; therefore,
it is not wrapped with quotes. However, the value of the field title is a string;
therefore, it is wrapped with quotes.
Theo Nice! Now, I understand what you mean by late binding.
Joe Cool! Now, let me show you how we store data in the database.
10.2 Storing data in the database
In the previous section, we saw how to retrieve data from the database as a list of maps.
Next, we’ll see how to store data in the database when data is represented with a map.
Theo I guess that storing data in the database is quite similar to fetching data from
the database.
Joe It’s similar in the sense that we deal only with generic data collections. Can you
write a parameterized SQL query that inserts a row with user info using only
email and encrypted_password, please?
Theo OK.

=== 페이지 233 ===
10.2 Storing data in the database 205
Theo takes a moment to think about the code and writes a few lines of SQL as Joe
requested. He shows it to Joe.
Listing10.7 SQL statement to add a member
INSERT
INTO members
(email, encrypted_password)
VALUES ($1, $2)
Joe Great! And here’s how to integrate your SQL query in our application code.
Listing10.8 Adding a member from inside the application
var addMemberQuery =
"INSERT INTO members (email, password) VALUES ($1, $2)";
dbClient.query(addMemberQuery,
Passes the two parameters to
[_.get(member, "email"),
the SQL query as an array
_.get(member, "encryptedPassword")]);
Theo Your code is very clear, but something still bothers me.
Joe What is that?
Theo I find it cumbersome that you use _.get(user, "email") instead of user
.email, like I would if the data were represented with a class.
Joe In JavaScript, you are allowed to use the dot notation user.email instead of
_.get(user, "email").
Theo Then why don’t you use the dot notation?
Joe Because I wanted to show you how you can apply DOP principles even in lan-
guages like Java, where the dot notation is not available for hash maps.
 NOTE In this book, we avoid using the JavaScript dot notation to access a field in a
hash map in order to illustrate how to apply DOP in languages that don’t support dot
notation on hash maps.
Theo That’s exactly my point. I find it cumbersome in a language like Java to use
_.get(user, "email") instead of user.email like I would if the data were
represented with a class.
Joe On one hand, it’s cumbersome. On the other hand, representing data with a
hash map instead of a static class allows you to access fields in a flexible way.
Theo I know—you’ve told me so many times! But I can’t get used to it.
Joe Let me give you another example of the benefits of the flexible access to data
fields in the context of adding a member to the database. You said that writing
[_.get(member, "email"), _.get(member, "encryptedPassword")] was
less convenient than writing [member.email, member.encryptedPassword].
Right?
Theo Absolutely!
Joe Let me show you how to write the same code in a more succinct way, using a
function from Lodash called _.at.

=== 페이지 234 ===
206 CHAPTER 10 Database operations
Theo What does this _.at function do?
Joe It receives a map m, a list keyList, and returns a list made of the values in m
associated with the keys in keyList.
Theo How about an example?
Joe Sure. We create a list made of the fields email and encryptedPassword of a
member.
Joe types for a bit. He shows this code to Theo.
Listing10.9 Creating a list made of some values in a map with _.at
var member = {
"email": "samantha@gmail.com",
"encryptedPassword": "c2VjcmV0",
"isBlocked": false
};
_.at(member,
["email", "encryptedPassword"]);
// ? ["samantha@gmail.com", "c2VjcmV0"]
Theo Do the values in the results appear in the same order as the keys in keyList?
Joe Yes!
Theo That’s cool.
TIP Accessing a field in a hash map is more flexible than accessing a member in an
object instantiated from a class.
Joe And here’s the code for adding a member using _.at.
Listing10.10 Using _.at to return multiple values from a map
class CatalogDB {
static addMember(member) {
var addMemberQuery = `INSERT
INTO members
(email, encrypted_password)
VALUES ($1, $2)`;
dbClient.query(addMemberQuery,
_.at(member, ["email",
"encryptedPassword"]));
}
}
Theo I can see how the _.at function becomes really beneficial when we need to
pass a bigger number of field values.
Joe I’ll be showing you more examples that use the flexible data access that we
have in DOP.

=== 페이지 235 ===
10.3 Simple data manipulation 207
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

=== 페이지 236 ===
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

=== 페이지 237 ===
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

=== 페이지 238 ===
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

=== 페이지 239 ===
10.4 Advanced data manipulation 211
On his laptop, Theo writes the code to rename email. Satisfied, he turns the laptop to Joe.
Listing10.16 Renaming email to userEmail
var listOfMaps = [
{
"email": "jennie@gmail.com",
"encryptedPassword": "secret-pass"
},
{
"email": "franck@hotmail.com",
"encryptedPassword": "my-secret"
}
];
renameResultKeys(listOfMaps,
{"email": "userEmail"});
Joe Excellent! I think you’re ready to move on to advanced data manipulation.
10.4 Advanced data manipulation
In some cases, we need to change the structure of the rows returned by an SQL query
(for instance, aggregating fields from different rows into a single map). This could be
done at the level of the SQL query, using advanced features like JSON aggregation in
PostgreSQL. However, sometimes it makes more sense to reshape the data inside the
application because it keeps the SQL queries simple. As with the simple data manipu-
lation scenario of the previous section, once we write code that implements some data
manipulation, we’re free to use the same code for similar use cases, even if they involve
data entities of different types.
Theo What kind of advanced data manipulation did you have in mind?
Joe You’ll see in a minute, but first, an SQL task for you. Write an SQL query that
returns books, including author names, that contain the word habit in their
title.
Theo Let me give it a try.
After some trial and error, Theo is able to nail it down. He jots down an SQL query that
joins the three tables: books, book_authors, and authors.
Listing10.17 SQL query to retrieve books containing the word habit
SELECT
title,
isbn,
authors.name AS author_name
FROM
books
INNER JOIN
book_authors

=== 페이지 240 ===
212 CHAPTER 10 Database operations
ON books.isbn = book_authors.book_isbn
INNER JOIN
authors
ON book_authors.author_id = authors.id
WHERE books.title LIKE '%habit%';
Joe How many rows are in the results?
Theo goes to the whiteboard. He quickly sketches a table showing the results, then he
answers Joe’s question. Because 7 Habits of Highly Effective People has two authors, Theo lists
the book twice in table 10.6.
Table 10.6 Results of the SQL query that retrieves books whose title contain the word habit, including
author names
title isbn author_name
7 Habits of Highly Effective People 978-1982137274 Sean Covey
7 Habits of Highly Effective People 978-1982137274 Stephen Covey
The Power of Habit 978-0812981605 Charles Duhigg
Theo Three rows.
Joe And how many books?
Theo Two books.
Joe Can you show me the results of the SQL query as a list of maps?
Theo Sure.
Listing10.18 A list of maps with the results for listing 10.17
[
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"publication_year": "Sean Covey"
},
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Stephen Covey"
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"author_name": "Charles Duhigg"
}
]
Joe And what does the list of maps that we need to return look like?
Theo It’s a list with two maps, where the author names are aggregated in a list. Let
me write the code for that.

=== 페이지 241 ===
10.4 Advanced data manipulation 213
Listing10.19 Aggregating author names in a list
[
{
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"authorNames": [
"Sean Covey",
"Stephen Covey"
]
},
{
"isbn": "978-0812981605",
"title": "The Power of Habit",
"authorNames": ["Charles Duhigg"]
}
]
Joe Perfect! Now, let’s take an example of an advanced data manipulation task,
where we convert the list of maps as returned from the database to a list of
maps where the author names are aggregated.
Theo Hmm... That sounds tough.
Joe Let me break the task in two steps. First, we group together rows that belong to
the same book (with the same ISBN). Then, in each group, we aggregate
author names in a list. Hold on, I’ll diagram it as a data processing pipeline.
Joe goes the whiteboard. He draws the diagram in figure 10.3.
Joe Does it makes sense to you now?
Theo Yes, the data pipeline makes sense, but I have no idea how to write code that
implements it!
Joe Let me guide you step by step. Let’s start by grouping together books with the
same ISBN using _.groupBy.
Listing10.20 Grouping rows by ISBN
var sqlRows = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Sean Covey"
},
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Stephen Covey"
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"author_name": "Charles Duhigg"
}
];
_.groupBy(sqlRows, "isbn");

=== 페이지 242 ===
214 CHAPTER 10 Database operations
title7 Habits of Highly Effective People title7 Habits of Highly Effective People
isbn978-1982137274 isbn978-1982137274
author_name Sean Covey author_name StephenCovey
titleThe Power of Habit
isbn978-0812981605
author_nameCharles Duhigg
group byisbn
978-1982137274 978-0812981605
title7 Habits of Highly Effective People titleThe Power of Habit
isbn978-1982137274 isbn978-0812981605
author_nameSean Covey author_nameCharles Duhigg
title7 Habits of Highly Effective People
isbn978-1982137274
author_nameStephenCovey
aggregateauthor_names
title7 Habits of Highly Effective People titleThe Power of Habit
isbn978-1982137274 isbn978-0812981605
authorNames[Sean Covey, Stephen Covey] authorNames[Charles Duhigg]
Figure 10.3 Data pipeline for aggregating author names
Theo What does rowsByIsbn look like?
Joe It’s a map where the keys are isbn, and the values are lists of rows. Here’s how
that would look.
Listing10.21 Rows grouped by ISBN
{
"978-0812981605": [
{
"author_name": "Charles Duhigg",
"isbn": "978-0812981605",

=== 페이지 243 ===
10.4 Advanced data manipulation 215
"title": "The Power of Habit"
}
],
"978-1982137274": [
{
"author_name": "Sean Covey",
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
},
{
"author_name": "Stephen Covey",
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
}
]
}
Theo What’s the next step?
Joe Now, we need to take each list of rows in rowsByIsbn and aggregate author
names.
Theo And how do we do that?
Joe Let’s do it on the list of two rows for 7 Habits of Highly Effective People. The code
looks like this.
Listing10.22 Aggregating author names
var rows7Habits = [
{
"author_name": "Sean Covey",
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
},
{
"author_name": "Stephen Covey",
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
}
]; Takes the
author names
from all rows
var authorNames = _.map(rows7Habits, "author_name");
var firstRow = _.nth(rows7Habits, 0);
var bookInfoWithAuthorNames = _.set(firstRow, "authorNames", authorNames);
_.omit(bookInfoWithAuthorNames, "author_name");
Removes the
author_name field
Joe First, we take the author names from all the rows. Then, we take the first row as
a basis for the book info, we add a field authorNames, and remove the field
author_name.
Theo Can we make a function of it?
Joe That’s exactly what I was going to suggest!

=== 페이지 244 ===
216 CHAPTER 10 Database operations
Theo I’ll call the function aggregateField. It will receive three arguments: the
rows, the name of the field to aggregate, and the name of the field that holds
the aggregation.
Theo turns to his laptop. After a couple of minutes, his screen displays the implementation
for aggregateField.
Listing10.23 Aggregating an arbitrary field
function aggregateField(rows, fieldName, aggregateFieldName) {
var aggregatedValues = _.map(rows, fieldName);
var firstRow = _.nth(rows, 0);
var firstRowWithAggregatedValues = _.set(firstRow,
aggregateFieldName,
aggregatedValues);
return _.omit(firstRowWithAggregatedValues, fieldName);
}
Joe Do you mind writing a test case to make sure your function works as expected?
Theo With pleasure! Take a look.
Listing10.24 Test case for aggregateField
var expectedResults = {
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"authorNames": [
"Sean Covey",
"Stephen Covey"
]
};
_.isEqual(expectedResults,
aggregateField(rows7Habits,
"author_name",
"authorNames"));
Joe Excellent! Now that we have a function that aggregates a field from a list of
rows, we only need to map the function over the values of our rowsByIsbn. Let
me code that up for you.
Listing10.25 Aggregating author names in rowsByIsbn
var rowsByIsbn = _.groupBy(sqlRows, "isbn");
var groupedRows = _.values(rowsByIsbn);
_.map(rowsByIsbn, function(groupedRows) {
return aggregateField(groupedRows, "author_name", "authorNames");
})

=== 페이지 245 ===
10.4 Advanced data manipulation 217
Theo Why did you take the values of rowsByIsbn?
Joe Because we don’t really care about the keys in rowsByIsbn. We only care about
the grouping of the rows in the values of the hash map.
Theo Let me try to combine everything we’ve done and write a function that receives
a list of rows and returns a list of book info with the author names aggregated
in a list.
Joe Good luck, my friend!
To Theo, it’s less complicated than it seems. After a couple of trials and errors, he arrives at
the code and the test case.
Listing10.26 Aggregating a field in a list of rows
function aggregateFields(rows, idFieldName,
fieldName, aggregateFieldName) {
var groupedRows = _.values(_.groupBy(rows, idFieldName));
return _.map(groupedRows, function(groupedRows) {
return aggregateField(groupedRows, fieldName, aggregateFieldName);
});
}
var sqlRows = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Sean Covey"
},
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Stephen Covey"
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"author_name": "Charles Duhigg"
}
];
var expectedResults =
[
{
"authorNames": [
"Sean Covey",
"Stephen Covey"
],
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
},
{
"authorNames": ["Charles Duhigg"],
"isbn": "978-0812981605",
"title": "The Power of Habit",

=== 페이지 246 ===
218 CHAPTER 10 Database operations
}
];
_.isEqual(aggregateFields(sqlRows,
"isbn",
"author_name",
"authorNames"),
expectedResults);
Theo I think I’ve got it.
Joe Congratulations! I’m proud of you, Theo.
Now Theo understands what Joe meant when he told him “a cloud is cloud” when they
were walking back from the park to the office. Instead of trapping data in the limits of our
objects, DOP guides us to represent data as data.
Summary
 Inside our applications, we represent data fetched from the database, no matter
if it is relational or nonrelational, as a generic data structure.
 In the case of a relational database, data is represented as a list of maps.
 Representing data from the database as data reduces system complexity because
we don’t need design patterns or complex class hierarchies to do it.
 We are free to manipulate data from the database with generic functions, such as
returning a list made of the values of some data fields, creating a version of a
map omitting a data field, or grouping maps in a list according to the value of a
data field.
 We use generic functions for data manipulation with great flexibility, using the
fact that inside a hash map, we access the value of a field via its name, repre-
sented as a string.
 When we package our data manipulation logic into custom functions that receive
field names as arguments, we are able to use those functions on different data
entities.
 The best way to manipulate data is to represent data as data.
 We represent data from the database with generic data collections, and we
manipulate it with generic functions.
 Accessing data from a NoSQL database is done in a similar way to the approach
presented in this chapter for accessing data from a relational database.
 With late binding, we care about data types as late as possible.
 Flexibility is increased as many parts of the system are free to manipulate data
without dealing with concrete types.
 Accessing a field in a hash map is more flexible than accessing a member in an
object instantiated from a class.

=== 페이지 247 ===
Summary 219
 In DOP, field names are just strings. It allows us to write generic functions to
manipulate list of maps representing data fetched from the database.
 In DOP, fields are first-class citizens.
 We can implement renaming keys in a list of maps or aggregating rows returned
by a database query via generic functions.
 JDBC stands for Java database connectivity.
 Converting a JDBC result set into a list of maps is quite straightforward.
Lodash functions introduced in this chapter
Function Description
at(map, [paths]) Creates an array of values corresponding to paths of map
omit(map, [paths]) Creates a map composed of the fields of map not in paths
nth(arr, n) Gets the element at index n in arr
groupBy(coll, f) Creates a map composed of keys generated from the results of running
each element of coll through f. The corresponding value for each key
is an array of elements responsible for generating the key.
