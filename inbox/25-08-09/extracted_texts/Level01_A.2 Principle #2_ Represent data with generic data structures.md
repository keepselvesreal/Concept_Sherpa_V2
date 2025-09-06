# A.2 Principle #2: Represent data with generic data structures

**Level:** 1
**페이지 범위:** 373 - 378
**총 페이지 수:** 6
**ID:** 155

---

=== 페이지 373 ===
A.2 Principle #2: Represent data with generic data structures 345
A.2 Principle #2: Represent data with generic data
structures
When adhering to Principle #1, code is separated from data. DOP is not opinionated
about the programming constructs to use for organizing the code, but it has a lot to
say about how the data should be represented. This is the theme of Principle #2.
The most common generic data structures are maps (aka dictionaries) and arrays
(or lists). But other generic data structures (e.g., sets, trees, and queues) can be used
as well. Principle #2 does not deal with the mutability or the immutability of the data.
That is the theme of Principle #3.
PRINCIPLE #2 Represent application data with generic data structures.
A.2.1 Illustration of Principle #2
In DOP, data is represented with generic data structures (like maps and arrays)
instead of instantiating data via specific classes. In fact, most of the data entities that
appear in a typical application can be represented with maps and arrays (or lists). But
there exist other generic data structures (e.g., sets, lists, queues, etc.) that might be
required in some use cases. Let’s look at the same simple example we used to illustrate
Principle #1 (data that represents an author).
An author is a data entity with a firstName, a lastName, and the number of books
they have written. Principle #2 is broken when we use a specific class to represent an
author as this listing reveals.
ListingA.12 Breaking Principle #2 in OOP
class AuthorData {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
}
Principle #2 is followed when using a map (a dictionary or an associative array) as a
generic data structure that represents an author. The following listing illustrates how
we can follow this principle in OOP.
ListingA.13 Following Principle #2 in OOP
function createAuthorData(firstName, lastName, books) {
var data = new Map;
data.firstName = firstName;
data.lastName = lastName;

=== 페이지 374 ===
346 APPENDIX A Principles of data-oriented programming
data.books = books;
return data;
}
In a language like JavaScript, we can also instantiate a map via a data literal, which is a
bit more convenient. The following listing shows an example.
ListingA.14 Following Principle #2 with map literals
function createAuthorData(firstName, lastName, books) {
return {
firstName: firstName,
lastName: lastName,
books: books
};
}
A.2.2 Benefits of Principle #2
Using generic data structures to represent data has multiple benefits. We cover these
benefits in greater detail in the following sections:
 The ability to use generic functions that are not limited to our specific use case
 A flexible data model
USING FUNCTIONS THAT ARE NOT LIMITED TO A SPECIFIC USE CASE
Using generic data structures to represent data makes it possible to manipulate data
with a rich set of functions that are available on those data structures natively in our
programming language. Additionally, third-party libraries also provide more of these
functions. For instance, JavaScript natively provides some basic functions on maps and
arrays, and third-party libraries like Lodash (https://lodash.com/) extend the func-
tionality with even more functions. There is a famous quote by Alan Perlis that sum-
marizes this benefit:
It is better to have 100 functions operate on one data structure than to have 10 functions
operate on 10 data structures.
—Alan Perlis (“Epigrams on Programming,” 1982)
When an author is represented as a map, the author can be serialized into JSON
using JSON.stringify(), which is part of JavaScript. The following listing provides
an example.
ListingA.15 [#serialize-klipse-js],reftext="A.1"
var data = createAuthorData("Isaac", "Asimov", 500);
JSON.stringify(data);
// → "{\"firstName\":\"Isaac\",\"lastName\":\"Asimov\",\"books\":500}"
Serializing author data without the number of books can be accomplished via Lodash’s
_.pick() function. The following listing uses _.pick() to create an object with a sub-
set of keys.

=== 페이지 375 ===
A.2 Principle #2: Represent data with generic data structures 347
ListingA.16 Manipulating data with generic functions
var data = createAuthorData("Isaac", "Asimov", 500);
var dataWithoutBooks = _.pick(data, ["firstName", "lastName"]);
JSON.stringify(dataWithoutBooks);
// → "{\"firstName\":\"Isaac\",\"lastName\":\"Asimov\"}"
TIP When adhering to Principle #2, a rich set of functionality is available for data
manipulation.
FLEXIBLE DATA MODEL
When using generic data structures, the data model is flexible, and data is not forced
into a specific shape. Data can be created with no predefined shape, and its shape can
be modified at will.
In classic OOP, when not adhering to Principle #2, each piece of data is instanti-
ated via a class and must follow a rigid shape. When a slightly different data shape is
needed, a new class must be defined. Take, for example, AuthorData, a class that rep-
resents an author entity made of three fields: firstName, lastName, and books. Sup-
pose that you want to add a field called fullName with the full name of the author. If
we fail to adhere to Principle #2, a new class, AuthorDataWithFullName, must be
defined. However, when using generic data structures, fields can be added to (or
removed from) a map on the fly as the following listing shows.
ListingA.17 Adding a field on the fly
var data = createAuthorData("Isaac", "Asimov", 500);
data.fullName = "Isaac Asimov";
TIP Working with a flexible data model is particularly useful in applications where
the shape of the data tends to be dynamic (e.g., web apps and web services).
Part 1 of the book explores in detail the benefits of a flexible data model in real-world
applications. Next, let’s explore the cost for adhering to Principle #2.
A.2.3 Cost for Principle #2
As with any programming principle, using this principle comes with its own set of trade-
offs. The price paid for representing data with generic data structures is as follows:
 There is a slight performance hit.
 No data schema is required.
 No compile-time check that the data is valid is necessary.
 In some statically-typed languages, type casting is needed.
COST #1: PERFORMANCE HIT
When specific classes are used to instantiate data, retrieving the value of a class mem-
ber is fast because the compiler knows how the data will look and can do many optimi-
zations. With generic data structures, it is harder to optimize, so retrieving the value

=== 페이지 376 ===
348 APPENDIX A Principles of data-oriented programming
associated to a key in a map, for example, is a bit slower than retrieving the value of a
class member. Similarly, setting the value of an arbitrary key in a map is a bit slower
than setting the value of a class member. In most programming languages, this perfor-
mance hit is not significant, but it is something to keep in mind.
TIP Retrieving and storing the value associated to an arbitrary key from a map is a bit
slower than with a class member.
COST #2: NO DATA SCHEMA
When data is instantiated from a class, the information about the data shape is in the
class definition. Every piece of data has an associated data shape. The existence of
data schema at a class level is useful for developers and for IDEs because
 Developers can easily discover the expected data shape.
 IDEs provide features like field name autocompletion.
When data is represented with generic data structures, the data schema is not part of
the data representation. As a consequence, some pieces of data might have an associ-
ated data schema and other pieces of data do not (see Principle #4).
TIP When generic data structures are used to store data, the data shape is not part of
the data representation.
COST #3: NO COMPILE-TIME CHECK THAT THE DATA IS VALID
Look again at the fullName function in the following listing, which was created to
explore Principle #1. This function receives the data it manipulates as an argument.
ListingA.18 Declaring the fullName function
function fullName(data) {
return data.firstName + " " + data.lastName;
}
When data is passed to fullName that does not conform to the shape fullName
expects, an error occurs at run time. With generic data structures, mistyping the field
storing the first name (e.g., fistName instead of firstName) does not result in a
compile-time error or an exception. Rather, firstName is mysteriously omitted from
the result. The following listing shows this unexpected behavior.
ListingA.19 Unexpected behavior with invalid data
fullName({fistName: "Issac", lastName: "Asimov"});
// → "undefined Asimov"
When we instantiate data via classes with a rigid data shape, this type of error is caught
at compile time. This drawback is mitigated by the application of Principle #4 that
deals with data validation.

=== 페이지 377 ===
A.2 Principle #2: Represent data with generic data structures 349
TIP When data is represented with generic data structures, data shape errors are
caught only at run time.
COST #4: THE NEED FOR EXPLICIT TYPE CASTING
In some statically-typed languages, explicit type casting is needed. This section takes a
look at explicit type casting in Java and at dynamic fields in C#.
In a statically-typed language like Java, author data can be represented as a map
whose keys are of type string and whose values are of types Object. For example, in
Java, author data is represented by a Map<String, Object> as the following listing
illustrates.
ListingA.20 Author data as a string map in Java
var asimov = new HashMap<String, Object>();
asimov.put("firstName", "Isaac");
asimov.put("lastName", "Asimov");
asimov.put("books", 500);
Because the information about the exact type of the field values is not available at
compile time, when accessing a field, an explicit type cast is required. For instance, in
order to check whether an author is prolific, the value of the books field must be type
cast to an integer as the next listing shows.
ListingA.21 Type casting is required when accessing a field in Java
class AuthorRating {
static boolean isProlific (Map<String, Object> data) {
return (int)data.get("books") > 100;
}
}
Some Java JSON serialization libraries like Gson (https://github.com/google/gson)
support serialization of maps of type Map<String, Object>, without requiring the user
to do any type casting. All the magic happens behind the scenes!
C# supports a dynamic data type called dynamic (see http://mng.bz/voqJ), which
allows type checking to occur at run time. Using this feature, author data is repre-
sented as a dictionary, where the keys are of type string, and the values are of type
dynamic. The next listing provides this representation.
ListingA.22 Author data as a dynamic string map in C#
var asimov = new Dictionary<string, dynamic>();
asimov["name"] = "Isaac Asimov";
asimov["books"] = 500;
The information about the exact type of the field values is resolved at run time. When
accessing a field, no type cast is required. For instance, when checking whether an

=== 페이지 378 ===
350 APPENDIX A Principles of data-oriented programming
author is prolific, the books field can be accessed as though it were declared as an
integer as in this listing.
ListingA.23 Type casting is not needed when accessing dynamic fields in C#
class AuthorRating {
public static bool isProlific (Dictionary<String, dynamic> data) {
return data["books"] > 100;
}
}
A.2.4 Summary of Principle #2
DOP uses generic data structures to represent data. This might cause a (small) perfor-
mance hit and impose the need to manually document the shape of data because the
compiler cannot validate it statically. Adherence to this principle enables the manipu-
lation of data with a rich set of generic functions (provided by the language and by
third-party libraries). Additionally, our data model is flexible. At this point, the data
can be either mutable or immutable. The next principle (Principle #3) illustrates the
value of immutability.
DOP Principle #2: Represent data with generic data structures
To comply with this principle, we represent application data with generic data struc-
tures, mostly maps and arrays (or lists). The following diagram shows a visual repre-
sentation of this principle.
DOPPrinciple #2: Represent data with generic data structures
Specific
Data
Generic
 Benefits include
– Using generic functions that are not limited to our specific use case
– A flexible data model
 The cost for implementing this principle includes
– There is a slight performance hit.
– No data schema is required.
– No compile time check that the data is valid is necessary.
– In some statically-typed languages, explicit type casting is needed.
