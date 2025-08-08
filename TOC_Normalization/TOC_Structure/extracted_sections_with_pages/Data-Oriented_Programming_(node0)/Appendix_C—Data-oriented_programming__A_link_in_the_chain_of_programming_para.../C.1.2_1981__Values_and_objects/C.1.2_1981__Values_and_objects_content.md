# C.1.2 1981: Values and objects

**페이지**: 377-378
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:42

---


--- 페이지 377 ---

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

--- 페이지 377 끝 ---


--- 페이지 378 ---

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

--- 페이지 378 끝 ---
