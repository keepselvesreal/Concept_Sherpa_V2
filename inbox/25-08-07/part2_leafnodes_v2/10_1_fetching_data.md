# 10.1 Fetching data from the database

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

## 페이지 227

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

## 페이지 228

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

## 페이지 229

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

## 페이지 230

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

## 페이지 231

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

## 페이지 232

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