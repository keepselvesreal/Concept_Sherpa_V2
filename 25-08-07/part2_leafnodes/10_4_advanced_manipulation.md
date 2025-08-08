# 10.4 Advanced data manipulation

211
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

## 페이지 240

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

## 페이지 241

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

## 페이지 242

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

## 페이지 243

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

## 페이지 244

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

## 페이지 245

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

## 페이지 246

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

## 페이지 247

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

## 페이지 248

Web services
A faithful messenger
This chapter covers
 Representing a client request as a map
 Representing a server response as a map
 Passing data forward
 Combining data from different sources
The architecture of modern information systems is made of software components
written in various programming languages like JSON, which communicate over the
wire by sending and receiving data represented in a language-independent data
exchange format. DOP applies the same principle to the communication between
inner parts of a program.
 NOTE When a web browser sends a request to a web service, it’s quite common
that the web service itself sends requests to other web services in order to fulfill the
web browser request. One popular data exchange format is JSON.
Inside a program, components communicate by sending and receiving data repre-
sented in a component independent format—namely, immutable data collections.
In the context of a web service that fulfills a client request by fetching data from a
220

## 페이지 249

11.1 Another feature request 221
database and other web services, representing data, as with immutable data collec-
tions, leads to these benefits:
 Using generic data manipulation functions to manipulate data from multiple
data sources
 Passing data forward freely with no additional complexity
11.1 Another feature request
After having delivered the database milestone on time, Theo calls Nancy to share the good
news. Instead of celebrating Theo’s success, Nancy asks him about the ETA for the next
milestone, Book Information Enrichment with the Open Library Books API. Theo tells her
that he’ll get back to her with an ETA by the end of the day. When Joe arrives at the office,
Theo tells him about the discussion with Nancy.
Theo I just got a phone call from Nancy, and she is stressed about the next milestone.
Joe What’s in the next milestone?
Theo Do you remember the Open Library Books API that I told you about a few
weeks ago?
 NOTE You can find the Open Library Books API at https://openlibrary.org/dev/
docs/api/books.
Joe No.
Theo It’s a web service that provides detailed information about books.
Joe Cool!
Theo Nancy wants to enrich the book search results. Instead of fetching book infor-
mation from the database, we need to retrieve extended book information
from the Open Library Books API.
Joe What kind of book information?
Theo Everything! Number of pages, weight, physical format, topics, etc....
Joe What about the information from the database?
Theo Besides the information about the availability of the books, we don’t need it
anymore.
Joe Have you already looked at the Open Library Books API?
Theo It’s a nightmare! For some books, the information contains dozen of fields,
and for other books, it has only two or three fields.
Joe What’s the problem then?
Theo I have no idea how to represent data that is so sparse and unpredictable.
Joe When we represent data as data, that’s not an issue. Let’s have a coffee and I’ll
show you.

## 페이지 250

222 CHAPTER