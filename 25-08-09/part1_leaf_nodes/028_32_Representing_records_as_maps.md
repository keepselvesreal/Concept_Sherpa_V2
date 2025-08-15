# 3.2 Representing records as maps

**ID**: 28  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

3.2 Representing records as maps
So far, we’ve illustrated the benefits we gain from the separation between code and
data at a high-system level. There’s a separation of concerns between code and data,
and each part has clear constraints:
 Code consists of static functions that receive data as an explicit argument.
 Data entities are modeled as records, and the relations between records are
represented by positional collections and indexes.
Now comes the question of the representation of the data. DOP has nothing special
tosay about collections and indexes. However, it’s strongly opinionated about the
representation of records: records should be represented by generic data structures
such as maps.
This applies to both OOP and FP languages. In dynamically-typed languages like
JavaScript, Python, and Ruby, data representation feels natural. While in statically-
typed languages like Java and C#, it is a bit more cumbersome.
Theo I’m really curious to know how we represent positional collections, indexes,
and records in DOP.
Joe Let’s start with positional collections. DOP has nothing special to say about the
representation of collections. They can be linked lists, arrays, vectors, sets, or
other collections best suited for the use case.
Theo It’s like in OOP.
Joe Right! For now, to keep things simple, we’ll use arrays to represent positional
collections.
Theo What about indexes?
Joe Indexes are represented as homogeneous string maps.
Theo What do you mean by a homogeneous map?

## 페이지 77

3.2 Representing records as maps 49
Joe I mean that all the values of the map are of the same kind. For example, in a
Book index, all the values are Book, and in an author index, all the values are
Author, and so forth.
Theo Again, it’s like in OOP.
 NOTE A homogeneous map is a map where all the values are of the same type. A hetero-
geneous map is a map where the values are of different types.
Joe Now, here’s the big surprise. In DOP, records are represented as maps, more
precisely, heterogeneous string maps.
Joe goes to the whiteboard and begins to draw. When he’s finished, he shows Theo the dia-
gram in figure 3.4.
Record Heterogeneous map
Linked list
Array
Data representation Collection
Set
Vector
Figure 3.4 The building blocks
Index Homogeneous map
of data representation
Theo stays silent for a while. He is shocked to hear that the data entities of a system can be
represented as a generic data structure, where the field names and value types are not
specified in a class. Then, Theo asks Joe:
Theo What are the benefits of this folly?
Joe Flexibility and genericity.
Theo Could you explain, please?
Joe I’ll explain in a moment, but before that, I’d like to show you what an instance
of a record in a DOP system looks like.
Theo OK.
Joe Let’s take as an example, Watchmen, by Alan Moore and Dave Gibbons, which is
my favorite graphic novel. This masterpiece was published in 1987. I’m going
to assume that, in a physical library, there are two copies of this book, whose ID
is nyc-central-lib, and that one of the two copies is currently out. Here’s
how I’d represent the Book record for Watchmen in DOP.
Joe comes closer to Theo’s laptop. He opens a text editor (not an IDE!) and types the Book
record for Theo.

## 페이지 78

50 CHAPTER 3 Basic data manipulation
Listing3.1 An instance of a Book record represented as a map
{
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authors": ["alan-moore", "dave-gibbons"],
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
},
{
"id": "book-item-2",
"libId": "nyc-central-lib",
"isLent": false
}
]
}
Theo looks at the laptop screen. He has a question.
Theo How am I supposed to instantiate the Book record for Watchmen programmat-
ically?
Joe It depends on the facilities that your programming language offers to instantiate
maps. With dynamic languages like JavaScript, Ruby, or Python, it’s straight-
forward, because we can use literals for maps and arrays. Here, let me show
you how.
Joe jots down the JavaScript code that creates an instance of a Book record, which rep-
resents as a map in JavaScript. He shows the code to Theo.
Listing3.2 A Book record represented as a map in JavaScript
var watchmenBook = {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authors": ["alan-moore", "dave-gibbons"],
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
},
{
"id": "book-item-2",
"libId": "nyc-central-lib",
"isLent": false
}
]
}

## 페이지 79

3.2 Representing records as maps 51
Theo And, if I’m in Java?
Joe It’s a bit more tedious, but still doable with the immutable Map and List static
factory methods.
 NOTE See “Creating Immutable Lists, Sets, and Maps” at http://mng.bz/voGm for
more information on this Java core library.
Joe types the Java code to create an instance of a Book record represented as a map. He
shows Theo the Java code.
Listing3.3 A Book record represented as a map in Java
Map watchmen = Map.of(
"isbn", "978-1779501127",
"title", "Watchmen",
"publicationYear", 1987,
"authors", List.of("alan-moore", "dave-gibbons"),
"bookItems", List.of(
Map.of(
"id", "book-item-1",
"libId", "nyc-central-lib",
"isLent", true
),
Map.of (
"id", "book-item-2",
"libId", "nyc-central-lib",
"isLent", false
)
)
);
TIP In DOP, we represent a record as a heterogeneous string map.
Theo I’d definitely prefer to create a Book record using a Book class and a BookItem
class.
Theo opens his IDE. He types the JavaScript code to represent a Book record as an instance
of a Book class.
Listing3.4 A Book record as an instance of a Book class in JavaScript
class Book {
isbn;
title;
publicationYear;
authors;
bookItems;
constructor(isbn, title, publicationYear, authors, bookItems) {
this.isbn = isbn;
this.title = title;
this.publicationYear = publicationYear;
this.authors = authors;
this.bookItems = bookItems;

## 페이지 80

52 CHAPTER 3 Basic data manipulation
}
}
class BookItem {
id;
libId;
isLent;
constructor(id, libId, isLent) {
this.id = id;
this.libId = libId;
this.isLent = isLent;
}
}
var watchmenBook = new Book("978-1779501127",
"Watchmen",
1987,
["alan-moore", "dave-gibbons"],
[new BookItem("book-item-1", "nyc-central-lib", true),
new BookItem("book-item-2", "nyc-central-lib", false)]);
Joe Theo, why do you prefer classes over maps for representing records?
Theo It makes the data shape of the record part of my program. As a result, the IDE
can auto-complete field names, and errors are caught at compile time.
Joe Fair enough. Can I show you some drawbacks for this approach?
Theo Sure.
Joe Imagine that you want to display the information about a book in the context
of search results. In that case, instead of author IDs, you want to display
author names, and you don’t need the book item information. How would
you handle that?
Theo I’d create a class BookInSearchResults without a bookItems member and
with an authorNames member instead of the authorIds member of the Book
class. Also, I would need to write a copy constructor that receives a Book object.
Joe In classic OOP, the fact that data is instantiated only via classes brings safety.
But this safety comes at the cost of flexibility.
TIP There’s a tradeoff between flexibility and safety in a data model.
Theo So, how can it be different?
Joe In the DOP approach, where records are represented as maps, we don’t need
to create a class for each variation of the data. We’re free to add, remove, and
rename record fields dynamically. Our data model is flexible.
Theo Interesting!
TIP In DOP, the data model is flexible. We’re free to add, remove, and rename
record fields dynamically at run time.
Joe Now, let me talk about genericity. How would you serialize the content of a
Book object to JSON?

## 페이지 81

3.2 Representing records as maps 53
TIP In DOP, records are manipulated with generic functions.
Theo Oh no! I remember that while working on the Klafim prototype, I had a night-
mare about JSON serialization when I was developing the first version of the
Library Management System.
Joe Well, in DOP, serializing a record to JSON is super easy.
Theo Does it require the usage of reflection in order to go over the fields of the
record like the Gson Java library does?
 NOTE See https://github.com/google/gson for more information on Gson.
Joe Not at all! Remember that in DOP, a record is nothing more than data. We can
write a generic JSON serialization function that works with any record. It can
be a Book, an Author, a BookItem, or anything else.
Theo Amazing!
TIP In DOP, you get JSON serialization for free.
Joe Actually, as I’ll show you in a moment, lots of data manipulation stuff can be
done using generic functions.
Theo Are the generic functions part of the language?
Joe It depends on the functions and on the language. For example, JavaScript pro-
vides a JSON serialization function called JSON.stringify out of the box, but
none for omitting multiple keys or for renaming keys.
Theo That’s annoying.
Joe Not so much; there are third-party libraries that provide data-manipulation facil-
ities. A popular data manipulation library in the JavaScript ecosystem is Lodash.
 NOTE See https://lodash.com/ to find out more about Lodash.
Theo What about other languages?
Joe Lodash has been ported to Java, C#, Python, and Ruby. Let me bookmark some
sites for you.
Joe bookmarks these sites for Theo:
 https://javalibs.com/artifact/com.github.javadev/underscore-lodash for Java
 https://www.nuget.org/packages/lodash/ for C#
 https://github.com/dgilland/pydash for Python
 https://rudash-website.now.sh/ for Ruby
 NOTE Throughout the book, we use Lodash to show how to manipulate data with
generic functions, but there is nothing special about Lodash. The exact same approach
could be implemented via other data manipulation libraries or custom code.
Theo Cool!
Joe Actually, Lodash and its rich set of data manipulation functions can be ported
to any language. That’s why it’s so beneficial to represent records as maps.

## 페이지 82

54 CHAPTER 3 Basic data manipulation
TIP DOP compromises on data safety to gain flexibility and genericity.
At the whiteboard, Joe quickly sketches the tradeoffs (see table 3.1).
Table 3.1 The tradeoff among safety, flexibility, and genericity
OOP DOP
Safety High Low
Flexibility Low High
Genericity Low High
