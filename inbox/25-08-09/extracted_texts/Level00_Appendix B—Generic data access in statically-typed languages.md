# Appendix B—Generic data access in statically-typed languages

**Level:** 0
**페이지 범위:** 392 - 408
**총 페이지 수:** 17
**ID:** 174

---

=== 페이지 392 ===
appendix B
Generic data access in
statically-typed languages
Representing data with generic data structures fits naturally in dynamically-typed
programming languages like JavaScript, Ruby, or Python. However, in statically-
typed programming languages like Java or C#, representing data as string maps
with values of an unspecified type is not natural for several reasons:
 Accessing map fields requires a type cast.
 Map field names are not validated at compile time.
 Autocompletion and other convenient IDE features are not available.
This appendix explores various ways to improve access to generic data in statically-
typed languages. We’ll look at:
 Value getters for maps to avoid type casting when accessing map fields
 Typed getters for maps to benefit from compile-time checks for map field
names
 Generic access for classes using reflection to benefit from autocompletion
and other convenient IDE features
B.1 Dynamic getters for string maps
Let’s start with a refresher about the approach we presented in part 1. Namely, we
represented records as string maps and accessed map fields with dynamic getters
and type casting.
 NOTE Most of the code snippets in this appendix use Java, but the approaches
illustrated can be applied to other object-oriented statically-typed languages like C#
or Go.
364

=== 페이지 393 ===
B.1 Dynamic getters for string maps 365
B.1.1 Accessing non-nested map fields with dynamic getters
Throughout this appendix, we will illustrate various ways to provide generic data access
using a book record. Our record is made of these parts:
 title (a string)
 isbn (a string)
 publicationYear (an integer)
Listing B.1 shows the representation of two books, Watchmen and Seven Habits of Highly
Effective People, in Java. These string maps contain values that are of type Object.
ListingB.1 Two books represented as maps
Map watchmenMap = Map.of(
"isbn", "978-1779501127",
"title", "Watchmen",
"publicationYear", 1987
);
Map sevenHabitsMap = Map.of(
"isbn", "978-1982137274",
"title", "7 Habits of Highly Effective People",
"publicationYear", 2020
);
The map fields can be accessed generically using a dynamic getter. The following list-
ing shows the implementation.
ListingB.2 The implementation of dynamic getter for map fields
class DynamicAccess {
static Object get(Map m, String k) {
return (m).get(k);
}
}
The drawback of dynamic getters is that a type cast is required to manipulate the value
of a map field. For instance, as shown in listing B.3, a cast to String is needed to call
the toUpperCase string method on the title field value.
ListingB.3 Accessing map fields with a dynamic getter and type casting
((String)DynamicAccess.get(watchmenMap, "title")).toUpperCase();
// → "WATCHMEN"
Dynamic getters provide generic data access in the sense that they do not require spe-
cific knowledge of the type of data the string map represents. As a consequence, the
name of the field can be received dynamically (e.g., from the user) as listing B.4
shows. This works because, in order to access a book data field in a string map, it is not
necessary to import the class that defines the book.

=== 페이지 394 ===
366 APPENDIX B Generic data access in statically-typed languages
ListingB.4 Mapping a map field with a dynamic getter and type casting
var books = List.of(watchmenMap, sevenHabitsMap);
var fieldName = "title";
books.stream()
.map(x -> DynamicAccess.get(x, fieldName))
.map(x -> ((String)x).toUpperCase())
.collect(Collectors.toList())
// → ["WATCHMEN", "7 HABITS OF HIGHLY EFFECTIVE PEOPLE"]
Another aspect of the genericity of dynamic getters is that they work on any type of
data. For instance, the dynamic getter for title works not only on books, but on any
piece of data that has a title field.
B.1.2 Accessing nested map fields with dynamic getters
Listing B.5 presents an example of search results. Suppose that the search results rep-
resent as a string map, where
 Keys are book ISBNs.
 Values are book data represented as string maps as in the previous section.
ListingB.5 Search results represented as a map
Map searchResultsMap = Map.of(
"978-1779501127", Map.of(
"isbn", "978-1779501127",
"title", "Watchmen",
"publicationYear", 1987
),
"978-1982137274", Map.of(
"isbn", "978-1982137274",
"title", "7 Habits of Highly Effective People",
"publicationYear", 2020
)
);
Book fields are nested in the search result map. In order to access nested map fields, a
get method is added to the DynamicAccess class in listing B.6. This get method
receives a list of strings that represents the information path of the nested map field.
ListingB.6 The implementation of dynamic getter for nested map fields
class DynamicAccess {
static Object get(Map m, String k) {
return (m).get(k);
}
static Object get(Map m, List<String> path) {
Object v = m;
for (String k : path) {

=== 페이지 395 ===
B.2 Value getters for maps 367
v = get((Map)v, k);
if (v == null) {
return null;
}
}
return v;
}
}
As with non-nested map fields in the previous section, type casting is required to manip-
ulate a nested map field. Listing B.7 shows how to access these nested map fields. In
the next section, we will look at how to avoid type casting when manipulating values in
string maps.
ListingB.7 Nested map fields with a dynamic getter and type casting
((String)DynamicAccess.get(searchResultsMap,
List.of("978-1779501127", "title"))).toUpperCase();
// → "WATCHMEN"
B.2 Value getters for maps
The simplest way to avoid type casting when manipulating the value of a string map
field is to use a dynamic data type (see appendix A). Dynamic data types are sup-
ported in languages like C#, but not in languages like Java. Next, we’ll illustrate how
value getters make it possible to avoid type casting.
B.2.1 Accessing non-nested map fields with value getters
In this section, books are still represented as string maps with values of type Object.
The following listing shows this representation.
ListingB.8 Two books represented as maps
Map watchmenMap = Map.of(
"isbn", "978-1779501127",
"title", "Watchmen",
"publicationYear", 1987
);
Map sevenHabitsMap = Map.of(
"isbn", "978-1982137274",
"title", "7 Habits of Highly Effective People",
"publicationYear", 2020
);
The idea of value getters is quite simple. Instead of doing the type casting outside the
getter, it is done inside the getter. A value getter is required for every type: getAs-
String for strings, getAsInt for integers, getAsFloat for float numbers, getAsBoolean
for Boolean values, and so forth.

=== 페이지 396 ===
368 APPENDIX B Generic data access in statically-typed languages
The value getter approach is used by Java libraries like Apache Wicket (http://
mng.bz/wnqQ) and Gson (https://github.com/google/gson). Listing B.9 shows an
implementation for getAsString that retrieves a map field value as a string.
ListingB.9 The implementation of value getter for map fields
class DynamicAccess {
static Object get(Map m, String k) {
return (m).get(k);
}
static String getAsString(Map m, String k) {
return (String)get(m, k);
}
}
A map field can be accessed without type casting. For instance, we can use getAsString
to manipulate a book title as in the next listing.
ListingB.10 Accessing non-nested fields with value getter
DynamicAccess.getAsString(watchmenMap, "title").toUpperCase();
// → "WATCHMEN"
Mapping over books with a value getter is a bit more convenient without type casting.
Look at the following listing, for example.
ListingB.11 Mapping over a list of maps with a value getter
var books = List.of(watchmenMap, sevenHabitsMap);
books.stream()
.map(x -> DynamicAccess.getAsString(x, "title"))
.map(x -> x.toUpperCase())
.collect(Collectors.toList())
// → ["WATCHMEN", "7 HABITS OF HIGHLY EFFECTIVE PEOPLE"]
B.2.2 Accessing nested map fields with value getters
The value getter approach applies naturally to nested map fields. As in the dynamic
getter section, suppose that search results are represented as a string map as in list-
ing B.12. Book fields are nested in the search results map, where
 Keys are book ISBNs.
 Values are book data represented as string maps as in the previous section.
ListingB.12 Search results represented as a map
Map searchResultsMap = Map.of(
"978-1779501127", Map.of(

=== 페이지 397 ===
B.2 Value getters for maps 369
"isbn", "978-1779501127",
"title", "Watchmen",
"publicationYear", 1987
),
"978-1982137274", Map.of(
"isbn", "978-1982137274",
"title", "7 Habits of Highly Effective People",
"publicationYear", 2020
)
);
In order to access nested map fields without type casting, we added a getAsString
method to the DynamicAccess class. This class receives a list of strings that represents
the information path of the nested map field as in the following listing.
ListingB.13 The implementation of value getter for nested map fields
class DynamicAccess {
static Object get(Map m, String k) {
return (m).get(k);
}
static Object get(Map m, List<String> p) {
Object v = m;
for (String k : p) {
v = get((Map)v, k);
if (v == null) {
return null;
}
}
return v;
}
static String getAsString(Map m, String k) {
return (String)get(m, k);
}
static String getAsString(Map m, List<String> p) {
return (String)get(m, p);
}
}
With the nested value getter, book titles can be manipulated inside search results with-
out type casting. The following listing demonstrates this.
ListingB.14 Accessing nested map fields with value getter
var informationPath = List.of("978-1779501127", "title");
DynamicAccess.getAsString(searchResultsMap, informationPath)
.toUpperCase();
// → "WATCHMEN"

=== 페이지 398 ===
370 APPENDIX B Generic data access in statically-typed languages
Value getters make data access a bit more convenient when avoiding type casting. The
next section shows how typed getters make it possible to benefit from compile-time
checks, even when data is represented as string maps.
B.3 Typed getters for maps
The typed getter approach is applicable in statically-typed languages that support generic
types like Java and C#. In this section, we will illustrate the typed getter approach in Java.
B.3.1 Accessing non-nested map fields with typed getters
As in the previous sections, we’ll use the representation of two books, Watchmen and
Seven Habits of Highly Effective People, in Java as string maps. The following listing shows
the maps, whose values are of type Object.
ListingB.15 Two books represented as maps
Map watchmenMap = Map.of(
"isbn", "978-1779501127",
"title", "Watchmen",
"publicationYear", 1987
);
Map sevenHabitsMap = Map.of(
"isbn", "978-1982137274",
"title", "7 Habits of Highly Effective People",
"publicationYear", 2020
);
The idea of typed getters is to create a generic object. This object would then contain
information about:
 The field name
 The type of the field value
Now, we can use this object on a string map to retrieve the typed value of the field in
the map. For example, in listing B.16, there is a typed getter named TITLE that
retrieves the value of a field named title as a string. The implementation of typed
getter is in listing B.17.
ListingB.16 Accessing map fields with a typed getter
Getter<String> TITLE = new Getter("title");
TITLE.get(watchmenMap).toUpperCase();
// → "WATCHMEN"
ListingB.17 The implementation of a typed getter
class Getter <T> {
private String key;

=== 페이지 399 ===
B.3 Typed getters for maps 371
public <T> Getter (String k) {
this.key = k;
}
public T get (Map m) {
return (T)(DynamicAccess.get(m, key));
}
}
TIP Typed getters are generic objects. Unlike value getters from the previous section,
it is not necessary to provide an implementation for every type.
In a sense, typed getters support compile-time validation and autocompletion. If the
name of the typed getter TITLE is misspelled, the compiler throws an error. Typing the
first few letters of TITLE into an IDE provides autocompletion of the symbol ofthe typed
getter. However, when you instantiate a typed getter, the field name must be passed as a
string, and neither compile-time checks nor autocompletion are available. Mapping over
a list of maps with a typed getter is quite simple as you can see in the following listing.
ListingB.18 Mapping over a list of maps with a typed getter
var books = List.of(watchmenMap, sevenHabitsMap);
books.stream()
.map(x -> TITLE.get(x))
.map(x -> x.toUpperCase())
.collect(Collectors.toList())
// → ["WATCHMEN", "7 HABITS OF HIGHLY EFFECTIVE PEOPLE"]
B.3.2 Accessing nested map fields with typed getters
The typed getter approach extends well to nested map fields. As in the value getter
section, suppose that search results, presented in listing B.19, are represented as a
string map, where
 Keys are book ISBNs.
 Values are book data represented as string maps as in the previous section.
ListingB.19 Search results represented as a map
Map searchResultsMap = Map.of(
"978-1779501127", Map.of(
"isbn", "978-1779501127",
"title", "Watchmen",
"publicationYear", 1987
),
"978-1982137274", Map.of(
"isbn", "978-1982137274",
"title", "7 Habits of Highly Effective People",
"publicationYear", 2020
)
);

=== 페이지 400 ===
372 APPENDIX B Generic data access in statically-typed languages
In order to support nested map fields, a constructor is added to the Getter class,
which receives a list of strings that represents the information path. The following list-
ing shows this implementation.
ListingB.20 A nested typed getter
class Getter <T> {
private List<String> path;
private String key;
private boolean nested;
public <T> Getter (List<String> path) {
this.path = path;
nested = true;
}
public <T> Getter (String k) {
this.key = k;
nested = false;
}
public T get (Map m) {
if(nested) {
return (T)(DynamicAccess.get(m, path));
}
return (T)(DynamicAccess.get(m, key));
}
}
Nested map fields are manipulated with typed getters without any type casting. The
following listing provides an example.
ListingB.21 Accessing nested map fields with typed getter
var informationPath = List.of("978-1779501127",
"title");
Getter<String> NESTED_TITLE = new Getter(informationPath);
NESTED_TITLE.get(searchResultsMap).toUpperCase();
// → "WATCHMEN"
Why use typed getters? Typed getters provide several benefits:
 No required type casting
 No need for implementing a getter for each and every type
 Compile-time validation at usage time
 Autocompletion at usage time
However, at creation time, map fields are accessed as strings. The next section illus-
trates how to provide generic access when data is represented not as string maps but
as classes.

=== 페이지 401 ===
B.4 Generic access to class members 373
B.4 Generic access to class members
Providing generic access to class members is a totally different approach. With this
technique, we represent data with classes as in traditional OOP and use reflection in
order to provide generic data access.
 NOTE The generic access to class members approach is applicable in statically-
typed languages that support reflection like Java and C#. This section illustrates the
approach in Java.
B.4.1 Generic access to non-nested class members
Instead of representing data as string maps, data can be represented as classes with
data members only, providing generic access to the class members via reflection. This
approach is interesting as only read data access is needed. However, when creating
new versions of data or adding new data fields, it is better to represent data with maps
as in part 1 of the book.
 NOTE The approach presented in this section is applicable only for read data access.
Here are a few guidelines in order to represent a book as a class. Make sure that
 The class has only data members (no methods).
 The members are public.
 The members are immutable.
 The hashCode(), equals() and toString() methods are properly implemented.
For instance, in Java, mark the members with public and final as in listing B.22. In
the listing, the implementation of the hashCode(), equals(), and toString() meth-
ods are omitted for the sake of simplicity.
ListingB.22 Representing books with a class
public class BookData {
public final String isbn;
public final String title;
public final Integer publicationYear;
public BookData (
String isbn,
String title,
Integer publicationYear) {
this.isbn = isbn;
this.title = title;
this.publicationYear = publicationYear;
}
public boolean equals(Object o) {
// Omitted for sake of simplicity
}

=== 페이지 402 ===
374 APPENDIX B Generic data access in statically-typed languages
public int hashCode() {
// Omitted for sake of simplicity
}
public String toString() {
// Omitted for sake of simplicity
}
}
Since Java 14, there is a simpler way to represent data using data records (http://
mng.bz/q2q2) as listing B.23 displays. Data records provide
 Private final fields
 Public read accessors
 A public constructor, whose signature is derived from the record component list
 Implementations of equals() and hashCode() methods, which specify that two
records are equal if they are of the same type and their record components
are equal
 Implementation of toString(), which includes the string representation of the
record components with their names
ListingB.23 Representing books with a record
public record BookData (String isbn,
String title,
Integer publicationYear
) {}
Let’s create two objects (or records) for Watchmen and Seven Habits of Highly Effective
People. The following listing provides the code for the two objects.
ListingB.24 Two book records
BookData watchmenRecord = new BookData(
"978-1779501127",
"Watchmen",
1987
);
BookData sevenHabitsRecord = new BookData(
"978-1982137274",
"7 Habits of Highly Effective People",
2020
);
The traditional way to access a data member is via its accessor (e.g., watchmen
.title() to retrieve the title of Watchmen). In order to access a data member whose
name comes from a dynamic source like a variable (or as part of a request payload),
we need to use reflection. In Java, accessing the title field in a book looks like the code
snippet in the following listing.

=== 페이지 403 ===
B.4 Generic access to class members 375
ListingB.25 Accessing a data member via reflection
watchmenRecord
.getClass()
.getDeclaredField("title")
.get(watchmenRecord)
// → "watchmen"
Listing B.26 shows how reflection can be used to provide access to any data member. The
listing provides the implementation of dynamic access to non-nested class members.
ListingB.26 Accessing non-nested class members dynamically
class DynamicAccess {
static Object get(Object o, String k) {
if(o instanceof Map) {
return ((Map)o).get(k);
}
try {
return (o.getClass().getDeclaredField(k).get(o));
} catch (IllegalAccessException | NoSuchFieldException e) {
return null;
}
}
static String getAsString(Object o, String k) {
return (String)get(o, k);
}
}
Now, data members are accessible with the same genericity and dynamism as fields in
a string map. The code in the next listing shows how this is done.
ListingB.27 Accessing a class member dynamically
((String)DynamicAccess.get(watchmenRecord, "title")).toUpperCase();
// → "WATCHMEN"
Without any code modification, value getters (presented earlier in this appendix in
the context of string maps) can now work with classes and records. The following list-
ing uses value getters in this way.
ListingB.28 Accessing a class member with a value getter
DynamicAccess.getAsString(watchmenRecord, "title").toUpperCase();
// → "WATCHMEN"
It is possible to map over a list of objects without having to import the class definition
of the objects we map over. This is shown in the following listing.

=== 페이지 404 ===
376 APPENDIX B Generic data access in statically-typed languages
ListingB.29 Mapping over a list of objects with a value getter
var books = List.of(watchmenRecord, sevenHabitsRecord);
books.stream()
.map(x -> DynamicAccess.getAsString(x, "title"))
.map(x -> x.toUpperCase())
.collect(Collectors.toList())
// → ["WATCHMEN", "7 HABITS OF HIGHLY EFFECTIVE PEOPLE"]
The typed getters we introduced earlier in the appendix can be used on objects. Take
a look at the following listing to see how this is carried out.
ListingB.30 Mapping over a list of objects with a typed getter
var books = List.of(watchmenRecord, sevenHabitsRecord);
books.stream()
.map(x -> TITLE.get(x))
.map(x -> x.toUpperCase())
.collect(Collectors.toList())
// → ["WATCHMEN", "7 HABITS OF HIGHLY EFFECTIVE PEOPLE"]
B.4.2 Generic access to nested class members
The previous section showed how to provide the same data access to classes as we used
for string maps. This becomes powerful when we combine classes and maps. For
example, listing B.31 represents search results as a map, where
 Keys are book ISBNs (strings).
 Values are book data represented as data classes (or records) as in the previous
section.
ListingB.31 Search results represented as a map of records
Map searchResultsRecords = Map.of(
"978-1779501127", new BookData(
"978-1779501127",
"Watchmen",
1987
),
"978-1982137274", new BookData(
"978-1982137274",
"7 Habits of Highly Effective People",
2020
)
);
For this implementation, it is necessary to add two additional methods. We need to
declare the static get and getAsString() methods that receive a list of strings as the
next listing shows.

=== 페이지 405 ===
B.4 Generic access to class members 377
ListingB.32 The implementation of value getter for nested class members
class DynamicAccess {
static Object get(Object o, String k) {
if(o instanceof Map) {
return ((Map)o).get(k);
}
try {
return (o.getClass().getDeclaredField(k).get(o));
} catch (IllegalAccessException | NoSuchFieldException e) {
return null;
}
}
static Object get(Object o, List<String> p) {
Object v = o;
for (String k : p) {
v = get(v, k);
}
return v;
}
static String getAsString(Object o, String k) {
return (String)get(o, k);
}
static String getAsString(Object o, List<String> p) {
return (String)get(o, p);
}
}
Now, a data member that is nested inside a string map can be accessed through its
information path as, for instance, in listing B.6. The following listing provides the
code to access the data member with a value getter.
ListingB.33 Accessing a member of a class nested in a map
var informationPath = List.of("978-1779501127", "title");
DynamicClassAccess
.getAsString(searchResultsRecords, informationPath)
.toUpperCase();
// → "WATCHMEN"
There is a second kind of nested data member when a data member is itself an object.
For instance, listing B.34 shows how a bookAttributes field can be made from a
BookAttributes class, and listing B.35 shows an example of the nested class.
ListingB.34 Representing book attributes with a nested class
public class BookAttributes {
public Integer numberOfPages;
public String language;
public BookAttributes(Integer numberOfPages, String language) {

=== 페이지 406 ===
378 APPENDIX B Generic data access in statically-typed languages
this.numberOfPages = numberOfPages;
this.language = language;
}
}
public class BookWithAttributes {
public String isbn;
public String title;
public Integer publicationYear;
public BookAttributes attributes;
public Book (
String isbn,
String title,
Integer publicationYear,
Integer numberOfPages,
String language) {
this.isbn = isbn;
this.title = title;
this.publicationYear = publicationYear;
this.attributes = new BookAttributes(numberOfPages, language);
}
}
ListingB.35 An instance of a nested class
BookData sevenHabitsNestedRecord = new BookWithAttributes(
"978-1982137274",
"7 Habits of Highly Effective People",
2020,
432,
"en"
);
Value getters work without any modification on nested data members. We can do this
with the code in the following listing.
ListingB.36 Accessing a nested class member with a value getter
var informationPath = List.of("attributes",
"language");
DynamicClassAccess.getAsString(sevenHabitsNestedRecord, informationPath)
.toUpperCase();
// → "EN"
B.4.3 Automatic JSON serialization of objects
An approach similar to the one illustrated in the previous section is used by JSON seri-
alization libraries like Gson (https://github.com/google/gson) in order to serialize
objects to JSON automatically. Gson uses reflection to go over the class members, gen-
erating a JSON representation of each member value. Listing B.37 displays an exam-
ple of Gson in action.

=== 페이지 407 ===
B.4 Generic access to class members 379
ListingB.37 JSON serialization of an object with Gson
import com.google.gson.*;
var gson = new Gson();
BookData sevenHabitsRecord = new BookData(
"978-1982137274",
"7 Habits of Highly Effective People",
2020
);
System.out.println(gson.toJson(sevenHabitsRecord));
// → {"title":"7 Habits of Highly Effective People", …}
Listing B.38 shows how it also works with objects nested in maps. Listing B.39 then
provides an example with objects nested in objects.
ListingB.38 JSON serialization of objects nested in a map with Gson
Map searchResultsRecords = Map.of(
"978-1779501127", new BookData(
"978-1779501127",
"Watchmen",
1987
),
"978-1982137274", new BookData(
"978-1982137274",
"7 Habits of Highly Effective People",
2020
)
);
System.out.println(gson.toJson(searchResultsRecords));
// → {"978-1779501127":{"isbn":"978-1779501127","title":"Watchmen", …}}
ListingB.39 JSON serialization of an object nested in an object with Gson
BookData sevenHabitsNestedRecord = new BookWithAttributes(
"978-1982137274",
"7 Habits of Highly Effective People",
2020,
432,
"en"
);
System.out.println(gson.toJson(sevenHabitsNestedRecord));
// → {"isbn":"978-1982137274",
// → "title":"7 Habits of Highly Effective People", …}

=== 페이지 408 ===
380 APPENDIX B Generic data access in statically-typed languages
Summary
This appendix has presented various ways to provide generic data access in statically-
typed programming languages. Table B.1 summarizes the benefits and drawbacks of
each approach. As you incorporate DOP practices in your programs, remember that
data can be represented either as string maps or as classes (or records) and benefits
from generic data access via:
 Dynamic getters
 Value getters
 Typed getters
 Reflection
Table B.1 Various ways to provide generic data access in statically-typed programming languages
Approach Representation Benefits Drawbacks
Dynamic getters Map Generic access Requires type casting
Value getters Map No type casting Implementation per type
Typed getters Map Compile-time validation on No compile-time validation
usage on creation
Reflection Class Full compile-time validation Not modifiable
