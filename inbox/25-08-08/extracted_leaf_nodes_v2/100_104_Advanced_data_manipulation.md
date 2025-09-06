# 10.4 Advanced data manipulation

**메타데이터:**
- ID: 100
- 레벨: 2
- 페이지: 239-245
- 페이지 수: 7
- 부모 ID: 95
- 텍스트 길이: 10351 문자

---

ta manipulation 211
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