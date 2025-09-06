# 11 Introduction

**메타데이터:**
- ID: 103
- 레벨: 2
- 페이지: 248-249
- 페이지 수: 2
- 부모 ID: 102
- 텍스트 길이: 5140 문자

---

=== Page 247 ===
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

=== Page 248 ===
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

=== Page 249 ===
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

=== Page 250 ===
222 CHAPTER 11 Web services
11.2 Building the insides like the outsides
While Theo drinks his macchiato, Joe draws a diagram on a whiteboard. Figure 11.1 shows
Joe’s diagram.
Web browser
Data
Web server
Data Data
Web service Database Figure 11.1 The high-level architecture
of a modern information system
Joe Before we dive into the details of the implementation of the book search result
enrichment, let me give you a brief intro.
Theo Sure.
Joe takes a sip of his espresso. He then points to the diagram (figure 11.1) on the whiteboard.
Joe Does this look familiar to you?
Theo Of course!
Joe Can you show me, roughly, the steps in the data flow of a web service?
Theo Sure.
Theo moves closer to the whiteboard. He writes a list of steps (see the sidebar) near the
architecture diagram.
The steps of the data flow inside a web service
1 Receive a request from a client.
2 Apply business logic to the request.
3 Fetch data from external sources (e.g., database and other web services).
4 Apply business logic to the responses from external sources.
5 Send the response to the client.
Joe Excellent! Now comes an important insight about DOP.
Theo I’m all ears.