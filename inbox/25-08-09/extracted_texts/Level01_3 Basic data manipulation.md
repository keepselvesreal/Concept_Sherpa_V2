# 3 Basic data manipulation

**Level:** 1
**페이지 범위:** 71 - 98
**총 페이지 수:** 28
**ID:** 25

---

=== 페이지 71 ===
Basic data manipulation
Meditation and programming
This chapter covers
 Representing records with string maps to improve
flexibility
 Manipulating data with generic functions
 Accessing each piece of information via its
information path
 Gaining JSON serialization for free
After learning why and how to separate code from data in the previous chapter,
let’s talk about data on its own. In contrast to traditional OOP, where system design
tends to involve a rigid class hierarchy, DOP prescribes that we represent our data
model as a flexible combination of maps and arrays (or lists), where we can access
each piece of information via an information path. This chapter is a deep dive into
the second principle of DOP.
PRINCIPLE #2 Represent data entities with generic data structures.
43

=== 페이지 72 ===
44 CHAPTER 3 Basic data manipulation
We increase system flexibility when we represent records as string maps and not as
objects instantiated from classes. This liberates data from the rigidity of a class-based sys-
tem. Data becomes a first-class citizen powered by generic functions to add, remove, or
rename fields.
 NOTE We refer to maps that have strings as keys as string maps.
The dependency between the code that manipulates data and the data is a weak
dependency. The code only needs to know the keys of specific fields in the record it
wants to manipulate. The code doesn’t even need to know about all the keys in the
record, only the ones relevant to it. In this chapter, we’ll deal only with data query.
We’ll discuss managing changes in system state in the next chapter.
3.1 Designing a data model
During lunch at Simple, Theo and Joe don’t talk about programming. Instead, they start
getting to know each other on a personal level. Theo discovers that Joe is married to Kay,
who has just opened her creative therapy practice after many years of studying various
fields related to well-being. Neriah, their 14-year-old son, is passionate about drones, whereas
Aurelia, their 12-year-old daughter, plays the transverse flute.
Joe tells Theo that he’s been practicing meditation for 10 years. Meditation, he says, has
taught him how to break away from being continually lost in a “storm thought” (especially
negative thoughts, which can be the source of great suffering) to achieve a more direct
relationship with reality. The more he learns to experience reality as it is, the calmer his
mind. When he first started to practice meditation, it was sometimes difficult and even
weird, but by persevering, he has increased his feeling of well-being with each passing year.
When they’re back at the office, Joe tells Theo that his next step in their DOP journey
will be about data models. This includes data representation.
Joe When we design the data part of our system, we’re free to do it in isolation.
Theo What do you mean by isolation?
Joe I mean that you don’t have to bother with code, only data.
Theo Oh, right. I remember you telling me how that makes a DOP system simpler
than OOP. Separation of concerns is a design principle I’m used to in OOP.
Joe Indeed.
Theo And, when we think about data, the only relations we have to think about are
association and composition.
Joe Correct.
Theo Will the data model design be significantly different than the data model I’m
used to designing as an OOP developer?
Joe Not so much.
Theo OK. Let me see if I can draw a DOP-style data entity diagram.
Theo takes a look at the data mind map that he drew earlier in the morning. He then
draws the diagram in figure 3.1.
He refines the details of the fields of each data entity and the kind of relations between
entities. Figure 3.2 shows the result of this redefined data entity diagram.

=== 페이지 73 ===
3.1 Designing a data model 45
Books
Authors
Catalog
Book items
Library data Book lendings
Users
User management Members
Librarians Figure 3.1 A data mind map of
the Library Management System
CC Library
name: String
address: String
CC Catalog CC UserManagement
* * *
CC Book CC Librarian CC Member
email: String email: String
title : String
password: String password: String
publicationYear: Number
*
ISBN: String
publisher: String
* *
CC Author CC BookLending
name: String lendingDate: String
CC BookItem
* libld: String
purchaseDate: String
Figure 3.2 A data model of the Library Management System

=== 페이지 74 ===
46 CHAPTER 3 Basic data manipulation
Joe The next step is to be more explicit about the relations between entities.
Theo What do you mean?
Joe For example, in your entity diagram, Book and Author are connected by a
many-to-many association relation. How is this relation going to be repre-
sented in your program?
Theo In the Book entity, there will be a collection of author IDs, and in the Author
entity, there will be a collection of book IDs.
Joe Sounds good. And what will the book ID be?
Theo The book ISBN.
 NOTE The International Standard Book Number (ISBN) is a numeric commercial
book identifier that is intended to be unique.
Joe And where will you hold the index that enables you to retrieve a Book from its
ISBN?
Theo In the Catalog because the catalog holds a bookByISBN index.
Joe What about author ID?
Theo Author ID is the author name in lowercase and with dashes instead of white
spaces (assuming that we don’t have two authors with the same name).
Joe And I guess that you also hold the author index in the Catalog?
Theo Exactly!
Joe Excellent. You’ve been 100% explicit about the relation between Book and
Author. I’ll ask you to do the same with the other relations of the system.
It’s quite easy for Theo to do, as he has done that so many times as an OOP developer. Fig-
ure 3.3 provides the detailed entity diagram of Theo’s system.
 NOTE By positional collection, we mean a collection where the elements are in order
(like a list or an array). By index, we mean a collection where the elements are accessi-
ble via a key (like a hash map or a dictionary).
The Catalog entity contains two indexes:
 booksByIsbn—The keys are book ISBNs, and the values are Book entities. Its type is
noted as {Book}.
 authorsById—The keys are author IDs, and the values are Author entities. Its type
is noted as {Author}.
Inside a Book entity, we have authors, which is a positional collection of author IDs of type
[String]. Inside an Author entity, we have books, which is a collection of book IDs of
type [String].
 NOTE For the notation for collections and index types, a positional collection of
Strings is noted as [String]. An index of Books is noted as {Book}. In the context of
a data model, the index keys are always strings.

=== 페이지 75 ===
3.1 Designing a data model 47
CC Library
name: String
address: String
catalog: Catalog
userManagement: UserManagement
CC Catalog CC UserManagement
booksByIsbn: {Book} librariansByEmail: {Librarian}
authorsById: {Author} membersByEmail: {Member}
*
*
* CC Author CC Librarian
CC Book i n d a : m S e tr : i n S g tring email: String CC Me * mber
title : String encryptedPassword: String
bookIsbns: [String] email: String
publicationYear: Number
encryptedPassword: String
isbn: String *
isBlocked: Boolean
authorIds: [String]
bookLendings: [BookLending]
bookItems: [BookItem] *
CC BookLending
lendingDate: String
bookItemId: String *
CC BookItem
bookIsbn: String
id: String
libId: String
*
purchaseDate: String
isLent: Boolean
Figure 3.3 Library management relation model. Dashed lines (e.g., between Book and Author) denote
indirect relations, [String] denotes a positional collection of strings, and {Book} denotes an index of
Books.
There is a dashed line between Book and Author, which means that the relation between
Book and Author is indirect. To access the collection of Author entities from a Book entity,
we’ll use the authorById index defined in the Catalog entity.
Joe I like your data entity diagram.
Theo Thank you.
Joe Can you tell me what the three kinds of data aggregations are in your diagram
(and, in fact, in any data entity diagram)?
Theo Let’s see...we have positional collections like authors in Book. We have
indexes like booksByIsbn in Catalog. I can’t find the third one.
Joe The third kind of data aggregation is what we’ve called, until now, an “entity”
(like Library, Catalog, Book, etc.), and the common term for entity in com-
puter science is record.

=== 페이지 76 ===
48 CHAPTER 3 Basic data manipulation
 NOTE A record is a data structure that groups together related data items. It’s a col-
lection of fields, possibly of different data types.
Theo Is it correct to say that a data entity diagram consists only of records, positional
collections, and indexes?
Joe That’s correct. Can you make a similar statement about the relations between
entities?
Theo The relations in a data entity diagram are either composition (solid line with a
full diamond) or association (dashed line with an empty diamond). Both types
of relations can be either one-to-one, one-to-many, or many-to-many.
Joe Excellent!
TIP A data entity diagram consists of records whose values are either primitives, posi-
tional collections, or indexes. The relation between records is either composition or
association.
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

=== 페이지 77 ===
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

=== 페이지 78 ===
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

=== 페이지 79 ===
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

=== 페이지 80 ===
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

=== 페이지 81 ===
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

=== 페이지 82 ===
54 CHAPTER 3 Basic data manipulation
TIP DOP compromises on data safety to gain flexibility and genericity.
At the whiteboard, Joe quickly sketches the tradeoffs (see table 3.1).
Table 3.1 The tradeoff among safety, flexibility, and genericity
OOP DOP
Safety High Low
Flexibility Low High
Genericity Low High
3.3 Manipulating data with generic functions
Joe Now let me show you how to manipulate data in DOP with generic functions.
Theo Yes, I’m quite curious to see how you’ll implement the search functionality of
the Library Management System.
Joe OK. First, let’s instantiate a Catalog record for the catalog data of a library,
where we have a single book, Watchmen.
Joe instantiates a Catalog record according to Theo’s data model in figure 3.3. Here’s
what Joe shows to Theo.
Listing3.5 A Catalog record
var catalogData = {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore", "dave-gibbons"],
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
},
"authorsById": {
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
},

=== 페이지 83 ===
3.3 Manipulating data with generic functions 55
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
}
Theo I see the two indexes we talked about, booksByIsbn and authorsById. How
do you differentiate a record from an index in DOP?
Joe In an entity diagram, there’s a clear distinction between records and indexes.
But in our code, both are plain data.
Theo I guess that’s why this approach is called data-oriented programming.
Joe See how straightforward it is to visualize any part of the system data inside a
program? The reason is that data is represented as data!
TIP In DOP, data is represented as data.
Theo That sounds like a lapalissade.1
Joe Oh, does it? I’m not so sure! In OOP, data is usually represented by objects,
which makes it more challenging to visualize data inside a program.
TIP In DOP, we can visualize any part of the system data.
Theo How would you retrieve the title of a specific book from the catalog data?
Joe Great question! In fact, in a DOP system, every piece of information has an
information path from which we can retrieve the information.
Theo Information path?
Joe For example, the information path to the title of the Watchmen book in the
catalog is ["booksByIsbn", "978-1779501127", "title"].
Theo Ah, I see. So, is an information path sort of like a file path, but that names in
an information path correspond to nested entities?
Joe You’re exactly right. And once we have the path of a piece of information, we
can retrieve the information with Lodash’s _.get function.
Joe types a few characters on Theo’s laptop. Theo is amazed at how little code is needed to
get the book title.
Listing3.6 Retrieving the title of a book from its information path
_.get(catalogData, ["booksByIsbn", "978-1779501127", "title"])
// → "Watchmen"
Theo Neat. I wonder how hard it would be to implement a function like _.get
myself.
1 A lapalissade is an obvious truth—a truism or tautology—that produces a comical effect.

=== 페이지 84 ===
56 CHAPTER 3 Basic data manipulation
After a few minutes of trial and error, Theo is able to produce his implementation. He
shows Joe the code.
Listing3.7 Custom implementation of get
function get(m, path) {
var res = m;
for(var i = 0; i < path.length; i++) {
We could use
var key = path[i];
forEach instead
res = res[key];
of a for loop.
}
return res;
}
After testing Theo’s implementation of get, Joe compliments Theo. He’s grateful that
Theo is catching on so quickly.
Listing3.8 Testing the custom implementation of get
get(catalogData, ["booksByIsbn", "978-1779501127", "title"]);
// → "Watchmen"
Joe Well done!
Theo I wonder if a function like _.get works smoothly in a statically-typed language
like Java?
Joe It depends on whether you only need to pass the value around or to access the
value concretely.
Theo I don’t follow.
Joe Imagine that once you get the title of a book, you want to convert the string
into an uppercase string. You need to do a static cast to String, right? Here,
let me show you an example that casts a field value to a string, then we can
manipulate it as a string.
Listing3.9 Casting a field value to a string
((String)watchmen.get("title")).toUpperCase()
Theo That makes sense. The values of the map are of different types, so the compiler
declares it as a Map<String,Object>. The information of the type of the field
is lost.
Joe It’s a bit annoying, but quite often our code just passes the data around. In that
case, we don’t have to deal with static casting. Moreover, in a language like C#,
when using the dynamic data type, type casting can be avoided.2,3
2 See http://mng.bz/4jo5 for the C# documentation on the built-in reference to dynamic types.
3 See appendix A for details about dynamic fields and type casting in C#.

=== 페이지 85 ===
3.3 Manipulating data with generic functions 57
TIP In statically-typed languages, we sometimes need to statically cast the field values.
Theo What about performance?
Joe In most programming languages, maps are quite efficient. Accessing a field
in a map is slightly slower than accessing a class member. Usually, it’s not
significant.
TIP There’s no significant performance hit for accessing a field in a map instead of as
a class member.
Theo Let’s get back to this idea of information path. It works in OOP too. I could
access the title of the Watchmen book with catalogData.booksByIsbn["978-
1779501127"].title. I’d use class members for record fields and strings for
index keys.
Joe There’s a fundamental difference, though. When records are represented as
maps, the information can be retrieved via its information path using a generic
function like _.get. But when records are represented as objects, you need to
write specific code for each type of information path.
Theo What do you mean by specific code? What’s specific in catalogData.books-
ByIsbn["978-1779501127"].title?
Joe In a statically-typed language like Java, you’d need to import the class defini-
tions for Catalog and Book.
Theo And, in a dynamically-typed language like JavaScript...?
Joe Even in JavaScript, when you represent records with objects instantiated from
classes, you can’t easily write a function that receives a path as an argument
and display the information that corresponds to this path. You would have to
write specific code for each kind of path. You’d access class members with dot
notation and map fields with bracket notation.
Theo Would you say that in DOP, the information path is a first-class citizen?
Joe Absolutely! The information path can be stored in a variable and passed as an
argument to a function.
TIP In DOP, you can retrieve every piece of information via a path and a generic
function.
Joe goes to the whiteboard. He draws a diagram like that in figure 3.5, which shows the
catalog data as a tree.
Joe You see, Theo, each piece of information is accessible via a path made of
strings and integers. For example, the path of Alan Moore’s first book is
["catalog", "authorsById", "alan-moore", "bookIsbns", 0].

=== 페이지 86 ===
58 CHAPTER 3 Basic data manipulation
catalog
booksByIsbn authorsById
978-1779501127 alan-moore
title isbn name
Watchmen 978-1779501127 Alan Moore
authorIds publicationYear bookIsbns
1987
1 0 0
bookItems
dave-gibbons alan-moore 978-1779501127
1 0 dave-gibbons
id id name
book-item-2 book-item-1 Dave Gibbons
libId libId bookIsbns
la-central-lib nyc-cental-lib
0
isLent isLent
978-1779501127
false true
Figure 3.5 The catalog data as a tree
3.4 Calculating search results
Theo Interesting. I’m starting to feel the power of expression of DOP!
Joe Wait, that’s just the beginning. Let me show you how simple it is to write code
that retrieves book information and displays it in search results. Can you tell
me exactly what information has to appear in the search results?
Theo Searching for book information should return isbn, title, and author-
Names.
Joe And what would a BookInfo record look like for Watchmen?
Theo quickly enters the code on his laptop. He then shows it to Joe.
Listing3.10 A BookInfo record for Watchmen in the context of search result
{
"title": "Watchmen",
"isbn": "978-1779501127",
"authorNames": [
"Alan Moore",
"Dave Gibbons",
]
}

=== 페이지 87 ===
3.4 Calculating search results 59
Joe Now I’ll show you step by step how to write a function that returns search
results matching a title in JSON format. I’ll use generic data manipulation
functions from Lodash.
Theo I’m ready!
Joe Let’s start with an authorNames function that calculates the author names of a
Book record by looking at the authorsById index. Could you tell me what’s
the information path for the name of an author whose ID is authorId?
Theo It’s ["authorsById", authorId, "name"].
Joe Now, let me show you how to retrieve the name of several authors using _.map.
Joe types the code to map the author IDs to the author names. Theo nonchalantly peeks
over Joe’s shoulder.
Listing3.11 Mapping author IDs to author names
_.map(["alan-moore", "dave-gibbons"],
function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
// → [ "Alan Moore", "Dave Gibbons"]
Theo What’s this _.map function? It smells like functional programming! You said I
wouldn’t have to learn FP to implement DOP!
Joe No need to learn functional programming in order to use _.map, which is a
function that transforms the values of a collection. You can implement it with
a simple for loop.
Theo spends a couple of minutes in front of his computer figuring out how to implement
_.map. Now he’s got it!
Listing3.12 Custom implementation of map
function map(coll, f) {
var res = [];
for(var i = 0; i < coll.length; i++) {
We could use
res[i] = f(coll[i]);
forEach instead
}
of a for loop.
return res;
}
After testing Theo’s implementation of map, Joe shows Theo the test. Joe again compli-
ments Theo.
Listing3.13 Testing the custom implementation of map
map(["alan-moore", "dave-gibbons"],
function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
// → [ "Alan Moore", "Dave Gibbons"]

=== 페이지 88 ===
60 CHAPTER 3 Basic data manipulation
Joe Well done!
Theo You were right! It wasn’t hard.
Joe Now, let’s implement authorNames using _.map.
It takes a few minutes for Theo to come up with the implementation of authorNames.
When he’s finished, he turns his laptop to Joe.
Listing3.14 Calculating the author names of a book
function authorNames(catalogData, book) {
var authorIds = _.get(book, "authorIds");
var names = _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
return names;
}
Joe We also need a bookInfo function that converts a Book record into a Book-
Info record. Let me show you the code for that.
Listing3.15 Converting a Book record into a BookInfo record
function bookInfo(catalogData, book) {
var bookInfo = {
"title": _.get(book, "title"),
"isbn": _.get(book, "isbn"),
"authorNames": authorNames(catalogData, book)
};
There’s no need to create
return bookInfo;
a class for bookInfo.
}
Theo Looking at the code, I see that a BookInfo record has three fields: title,
isbn, and authorNames. Is there a way to get this information without looking
at the code?
Joe You can either add it to the data entity diagram or write it in the documenta-
tion of the bookInfo function, or both.
Theo I have to get used to the idea that in DOP, the record field information is not
part of the program.
Joe Indeed, it’s not part of the program, but it gives us a lot of flexibility.
Theo Is there any way for me to have my cake and eat it too?
Joe Yes, and someday I’ll show you how to make record field information part of a
DOP program (see chapters 7 and 12).
Theo Sounds intriguing!
Joe Now that we have all the pieces in place, we can write our searchBooksBy-
Title function, which returns the book information about the books that
match the query. First, we find the Book records that match the query with
_.filter and then we transform each Book record into a BookInfo record
with _.map and bookInfo.

=== 페이지 89 ===
3.4 Calculating search results 61
Listing3.16 Searching books that match a query
function searchBooksByTitle(catalogData, query) {
var allBooks = _.values(_.get(catalogData, "booksByIsbn"));
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title").includes(query);
The includes JavaScript
});
function checks whether
a string includes a string
var bookInfos = _.map(matchingBooks, function(book) { as a substring.
return bookInfo(catalogData, book);
});
return bookInfos;
}
Theo You’re using Lodash functions without any explanation again!
Joe Sorry about that. I am so used to basic data manipulation functions that I con-
sider them as part of the language. What functions are new to you?
Theo _.values and _.filter
Joe Well, _.values returns a collection made of the values of a map, and _.filter
returns a collection made of the values that satisfy a predicate.
Theo _.values seems trivial. Let me try to implement _.filter.
The implementation of _.filter takes a bit more time. Eventually, Theo manages to get
it right, then he is able to test it.
Listing3.17 Custom implementation of filter
function filter(coll, f) {
var res = [];
for(var i = 0; i < coll.length; i++) {
We could use
if(f(coll[i])) {
forEach instead
res.push(coll[i]);
of a for loop.
}
}
return res;
}
Listing3.18 Testing the custom implementation of filter
filter(["Watchmen", "Batman"], function (title) {
return title.includes("Watch");
});
// → ["Watchmen"]
Theo To me, it’s a bit weird that to access the title of a book record, I need to write
_.get(book, "title"). I’d expect it to be book.title in dot notation or
book["title"] in bracket notation.
Joe Remember that book is a record that’s not represented as an object. It’s a map.
Indeed, in JavaScript, you can write _.get(book, "title"), book.title, or
book["title"]. But I prefer to use Lodash’s _.get function. In some lan-
guages, the dot and the bracket notations might not work on maps.

=== 페이지 90 ===
62 CHAPTER 3 Basic data manipulation
Theo Being language-agnostic has a price!
Joe Right, would you like to test searchBooksByTitle?
Theo Absolutely! Let me call searchBooksByTitle to search the books whose title
contain the string Watch.
Listing3.19 Testing searchBooksByTitle
searchBooksByTitle(catalogData, "Wat");
//[
// {
// "authorNames": [
// "Alan Moore",
// "Dave Gibbons"
// ],
// "isbn": "978-1779501127",
// "title": "Watchmen"
// }
//]
Theo It seems to work! Are we done with the search implementation?
Joe Almost. The searchBooksByTitle function we wrote is going to be part of the
Catalog module, and it returns a collection of records. We have to write a
function that’s part of the Library module, and that returns a JSON string.
Theo You told me earlier that JSON serialization was straightforward in DOP.
Joe Correct. The code for searchBooksByTitleJSON retrieves the Catalog record,
passes it to searchBooksByTitle, and converts the results to JSON with
JSON.stringify. That’s part of JavaScript. Here, let me show you.
Listing3.20 Implementation of searching books in a library as JSON
function searchBooksByTitleJSON(libraryData, query) {
var results = searchBooksByTitle(_.get(libraryData, "catalog"), query);
var resultsJSON = JSON.stringify(results);
return resultsJSON;
}
Joe In order to test our code, we need to create a Library record that contains our
Catalog record. Could you do that for me, please?
Theo Should the Library record contain all the Library fields (name, address,
and UserManagement)?
Joe That’s not necessary. For now, we only need the catalog field, then the test
for searching books.
Listing3.21 A Library record
var libraryData = {
"catalog": {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",

=== 페이지 91 ===
3.4 Calculating search results 63
"publicationYear": 1987,
"authorIds": ["alan-moore",
"dave-gibbons"],
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
},
"authorsById": {
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
}
};
Listing3.22 Test for searching books in a library as JSON
searchBooksByTitleJSON(libraryData, "Wat");
Theo How are we going to combine the four functions that we’ve written so far?
Joe The functions authorNames, bookInfo, and searchBooksByTitle go into
the Catalog module, and searchBooksByTitleJSON goes into the Library
module.
Theo looks at the resulting code of the two modules, Library and Catalog. He’s quite
amazed by its conciseness.
Listing3.23 Calculating search results for Library and Catalog
class Catalog {
static authorNames(catalogData, book) {
var authorIds = _.get(book, "authorIds");
var names = _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
return names;
}

=== 페이지 92 ===
64 CHAPTER 3 Basic data manipulation
static bookInfo(catalogData, book) {
var bookInfo = {
"title": _.get(book, "title"),
"isbn": _.get(book, "isbn"),
"authorNames": Catalog.authorNames(catalogData, book)
};
There’s no need
return bookInfo;
to create a class
}
for bookInfo.
static searchBooksByTitle(catalogData, query) {
var allBooks = _.get(catalogData, "booksByIsbn");
When _.filter is
var matchingBooks = _.filter(allBooks,
passed a map, it
function(book) {
goes over the values
return _.get(book, "title").includes(query);
of the map.
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
}
}
class Library {
static searchBooksByTitleJSON(libraryData, query) {
var catalogData = _.get(libraryData, "catalog");
var results = Catalog.searchBooksByTitle(catalogData, query);
var resultsJSON = JSON.stringify(results);
Converts data
return resultsJSON;
to JSON (part
}
of JavaScript)
}
After testing the final code in listing 3.24, Theo looks again at the source code from list-
ing 3.23. After a few seconds, he feels like he’s having another Aha! moment.
Listing3.24 Search results in JSON
Library.searchBooksByTitleJSON(libraryData, "Watchmen");
// → "[{\"title\":\"Watchmen\",\"isbn\":\"978-1779501127\",
// → \"authorNames\":[\"Alan Moore\",\"Dave Gibbons\"]}]"
Theo The important thing is not that the code is concise, but that the code contains
no abstractions. It’s just data manipulation!
Joe responds with a smile that says, “You got it, my friend!”
Joe It reminds me of what my first meditation teacher told me 10 years ago:
meditation guides the mind to grasp the reality as it is without the abstractions
created by our thoughts.
TIP In DOP, many parts of our code base tend to be just about data manipulation
with no abstractions.

=== 페이지 93 ===
3.5 Handling records of different types 65
3.5 Handling records of different types
We’ve seen how DOP enables us to treat records as first-class citizens that can be
manipulated in a flexible way using generic functions. But if a record is nothing more
than an aggregation of fields, how do we know what the type of the record is? DOP has
a surprising answer to this question.
Theo I have a question. If a record is nothing more than a map, how do you know
the type of the record?
Joe That’s a great question with a surprising answer.
Theo I’m curious.
Joe Most of the time, there’s no need to know the record type.
Theo What! What do you mean?
Joe I mean that what matters most are the values of the fields. For example, take a
look at the Catalog.authorNames source code. It operates on a Book record,
but the only thing that matters is the value of the authorIds field.
Doubtful, Theo looks at the source code for Catalog.authorNames. This is what Theo sees.
Listing3.25 Calculating the author names of a book
function authorNames(catalogData, book) {
var authorIds = _.get(book, "authorIds");
var names = _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
return names;
}
Theo What about differentiating between various user types like Member versus
Librarian? I mean, they both have email and encryptedPassword. How do
you know if a record represents a Member or a Librarian?
Joe Simple. You check to see if the record is found in the librariansByEmail
index or in the membersByEmail index of the Catalog.
Theo Could you be more specific?
Joe Sure! Let me write what the user management data of our tiny library might
look like, assuming we have one librarian and one member. To keep things
simple, I’m encrypting passwords through naive base-64 encoding for the User-
Management record.
Listing3.26 A UserManagement record
var userManagementData = {
"librariansByEmail": {
"franck@gmail.com" : { The base-64
encoding of
"email": "franck@gmail.com",
"mypassword"
"encryptedPassword": "bXlwYXNzd29yZA=="
}
},

=== 페이지 94 ===
66 CHAPTER 3 Basic data manipulation
"membersByEmail": {
"samantha@gmail.com": {
"email": "samantha@gmail.com",
"encryptedPassword": "c2VjcmV0",
The base-64
"isBlocked": false,
encoding of
"bookLendings": [
"secret"
{
"bookItemId": "book-item-1",
"bookIsbn": "978-1779501127",
"lendingDate": "2020-04-23"
}
]
}
}
}
TIP Most of the time, there’s no need to know the record type.
Theo This morning, you told me you’d show me the code for UserManagement
.isLibrarian function this afternoon.
Joe So, here we are. It’s afternoon, and I’m going to fulfill my promise.
Joe implements isLibrarian. With a slight pause, he then issues the test for isLibrarian.
Listing3.27 Checking if a user is a librarian
function isLibrarian(userManagement, email) {
return _.has(_.get(userManagement, "librariansByEmail"), email);
}
Listing3.28 Testing isLibrarian
isLibrarian(userManagementData, "franck@gmail.com");
// → true
Theo I’m assuming that _.has is a function that checks whether a key exists in a
map. Right?
Joe Correct.
Theo OK. You simply check whether the librariansByEmail map contains the
email field.
Joe Yep.
Theo Would you use the same pattern to check whether a member is a Super mem-
ber or a VIP member?
Joe Sure. We could have SuperMembersByEmail and VIPMembersByEmail indexes.
But there’s a better way.
Theo How?
Joe When a member is a VIP member, we add a field, isVIP, with the value true to
its record. To check if a member is a VIP member, we check whether the
isVIP field is set to true in the member record. Here’s how I would code
isVIPMember.

=== 페이지 95 ===
3.5 Handling records of different types 67
Listing3.29 Checking whether a member is a VIP member
function isVIPMember(userManagement, email) {
return _.get(userManagement, ["membersByEmail", email, "isVIP"]) == true;
}
Theo I see that you access the isVIP field via its information path, ["membersBy-
Email", email, "isVIP"].
Joe Yes, I think it makes the code crystal clear.
Theo I agree. I guess we can do the same for isSuperMember and set an isSuper
field to true when a member is a Super member?
Joe Yes, just like this.
Joe assembles all the pieces in a UserManagement class. He then shows the code to Theo.
Listing3.30 The code of UserManagement module
class UserManagement {
isLibrarian(userManagement, email) {
return _.has(_.get(userManagement, "librariansByEmail"), email);
}
isVIPMember(userManagement, email) {
return _.get(userManagement,
["membersByEmail", email, "isVIP"]) == true;
}
isSuperMember(userManagement, email) {
return _.get(userManagement,
["membersByEmail", email, "isSuper"]) == true;
}
}
Theo looks at the UserManagement module code for a couple of seconds. Suddenly, an
idea comes to his mind.
Theo Why not have a type field in member record whose value would be either VIP
or Super?
Joe I assume that, according to the product requirements, a member can be both a
VIP and a Super member.
Theo Hmm...then the types field could be a collection containing VIP or Super
or both.
Joe In some situations, having a types field is helpful, but I find it simpler to have
a Boolean field for each feature that the record supports.
Theo Is there a name for fields like isVIP and isSuper?
Joe I call them feature fields.
TIP Instead of maintaining type information about a record, use a feature field (e.g.,
isVIP).

=== 페이지 96 ===
68 CHAPTER 3 Basic data manipulation
Theo Can we use feature fields to differentiate between librarians and members?
Joe You mean having an isLibrarian and an isMember field?
Theo Yes, and having a common User record type for both librarians and members.
Joe We can, but I think it’s simpler to have different record types for librarians and
members: Librarian for librarians and Member for members.
Theo Why?
Joe Because there’s a clear distinction between librarians and members in terms of
data. For example, members can have book lendings but librarians don’t.
Theo I agree. Now, we need to mention the two Member feature fields in our entity
diagram.
With that, Theo adds these fields to his diagram on the whiteboard. When he’s finished, he
shows Joe his additions (figure 3.6).
CC Library
name: String
address: String
catalog: Catalog
userManagement: Catalog
CC Catalog CC UserManagement
booksByIsbn: {Book} librariansByEmail: {Librarian}
authorsById: {Author} membersByEmail: {Member}
*
*
* CC Author CC Librarian *
CC Book id: String email: String CC Member
name: String
title : String encryptedPassword: String email: String
bookIsbns: [String]
publicationYear: Number encryptedPassword: String
isbn: String * isBlocked: Boolean
authorIds: [String] bookLendings: [BookLending]
bookItems: [BookItem] * isVIP: Boolean
isSuper: Boolean
CC BookLending
lendingDate: String
bookItemId: String *
CC BookItem
bookIsbn: String
id: String
libId: String
*
purchaseDate: String
isLent: Boolean
Figure 3.6 A library management data model with the Member feature fields isVIP and isSuper
Joe Do you like the data model that we have designed together?
Theo I find it quite simple and clear.

=== 페이지 97 ===
Summary 69
Joe That’s the main goal of DOP.
Theo Also, I’m pleasantly surprised how easy it is to adapt to changing requirements,
both in terms of code and the data model.
Joe I suppose you’re also happy to get rid of complex class hierarchy diagrams.
Theo Absolutely! Also, I think I’ve found an interesting connection between DOP
and meditation.
Joe Really?
Theo When we were eating at Simple, you told me that meditation helped you expe-
rience reality as it is without the filter of your thoughts.
Joe Right.
Theo From what you taught me today, I understand that in DOP, we are encouraged
to treat data as data without the filter of our classes.
Joe Clever! I never noticed that connection between those two disciplines that are
so important for me. I guess you’d like to continue your journey in the realm
of DOP.
Theo Definitely. Let’s meet again tomorrow.
Joe Unfortunately, tomorrow I’m taking my family to the beach to celebrate the
twelfth birthday of my eldest daughter, Aurelia.
Theo Happy birthday, Aurelia!
Joe We could meet again next Monday, if that’s OK with you.
Theo With pleasure!
Summary
 DOP principle #2 is to represent data entities with generic data structures.
 We refer to maps that have strings as keys as string maps.
 Representing data as data means representing records with string maps.
 By positional collection, we mean a collection where the elements are in order
(like a list or an array).
 A positional collection of Strings is noted as [String].
 By index, we mean a collection where the elements are accessible via a key (like
a hash map or a dictionary).
 An index of Books is noted as {Book}.
 In the context of a data model, the index keys are always strings.
 A record is a data structure that groups together related data items. It’s a collec-
tion of fields, possibly of different data types.
 A homogeneous map is a map where all the values are of the same type.
 A heterogeneous map is a map where the values are of different types.
 In DOP, we represent a record as a heterogeneous string map.
 A data entity diagram consists of records whose values are either primitives, posi-
tional collections, or indexes.
 The relation between records in a data entity diagram is either composition or
association.

=== 페이지 98 ===
70 CHAPTER 3 Basic data manipulation
 The data part of a DOP system is flexible, and each piece of information is
accessible via its information path.
 There is a tradeoff between flexibility and safety in a data model.
 DOP compromises on data safety to gain flexibility and genericity.
 In DOP, the data model is flexible. We’re free to add, remove, and rename
record fields dynamically at run time.
 We manipulate data with generic functions.
 Generic functions are provided either by the language itself or by third-party
libraries like Lodash.
 JSON serialization is implemented in terms of a generic function.
 On the one hand, we’ve lost the safety of accessing record fields via members
defined at compile time. On the other hand, we’ve liberated data from the lim-
itation of classes and objects. Data is represented as data!
 The weak dependency between code and data makes it is easier to adapt to
changing requirements.
 When data is represented as data, it is straightforward to visualize system data.
 Usually, we do not need to maintain type information about a record.
 We can visualize any part of the system data.
 In statically-typed languages, we sometimes need to statically cast the field values.
 Instead of maintaining type information about a record, we use a feature field.
 There is no significant performance hit for accessing a field in a map instead of
a class member.
 In DOP, you can retrieve every piece of information via an information path and
a generic function.
 In DOP, many parts of our code base tend to be just about data manipulation
with no abstractions.
Lodash functions introduced in this chapter
Function Description
get(map, path) Gets the value of map at path
has(map, path) Checks if map has a field at path
merge(mapA, mapB) Creates a map resulting from the recursive merges between mapA and mapB
values(map) Creates an array of values of map
filter(coll, pred) Iterates over elements of coll, returning an array of all elements for which
pred returns true
map(coll, f) Creates an array of values by running each element in coll through f
