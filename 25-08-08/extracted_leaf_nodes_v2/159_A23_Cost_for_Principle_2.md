# A.2.3 Cost for Principle #2

**메타데이터:**
- ID: 159
- 레벨: 2
- 페이지: 375-377
- 페이지 수: 3
- 부모 ID: 155
- 텍스트 길이: 5521 문자

---

rinciple #2
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

350 APPENDIX A Principles of data-oriented programming
author is prolific, the books field can be accessed as though it were declared as an
integer as in this listing.
ListingA.23 Type casting is not needed when accessing dynamic fields in C#
class AuthorRating {
public static bool isProlific (Dictionary<String, dynamic> data) {
return data["books"] > 100;
}
}