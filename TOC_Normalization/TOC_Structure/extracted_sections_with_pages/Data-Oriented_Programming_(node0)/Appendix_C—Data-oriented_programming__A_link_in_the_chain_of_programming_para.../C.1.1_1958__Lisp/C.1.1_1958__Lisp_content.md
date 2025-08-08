# C.1.1 1958: Lisp

**페이지**: 375-376
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:41

---


--- 페이지 375 ---

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

--- 페이지 375 끝 ---


--- 페이지 376 ---

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

--- 페이지 376 끝 ---
