# 10 Introduction

**메타데이터:**
- ID: 96
- 레벨: 2
- 페이지: 225-226
- 페이지 수: 2
- 부모 ID: 95
- 텍스트 길이: 5630 문자

---

=== Page 224 ===
196 CHAPTER 9 Persistent data structures
 Persistent data structures represent data internally in such a way that structural
sharing scales well, both in terms of memory and computation.
 When data is immutable, it is safe to share it.
 Internally, persistence uses a branching factor of 32.
 In practice, manipulation of persistent data structures is efficient even for col-
lections with 10 billion entries!
 Due to modern architecture considerations, the performance of updating a
persistent list is dominated much more by the depth of the tree than by the
number of nodes at each level of the tree.
 Persistent lists can be manipulated in near constant time.
 In most languages, third-party libraries provide an implementation of persistent
data structures.
 Paguro collections implement the read-only parts of Java collection interfaces.
 Paguro collections can be passed to any methods that expect to receive a Java
collection without mutating them.

=== Page 225 ===
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

=== Page 226 ===
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

=== Page 227 ===
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