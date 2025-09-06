# B.4 Generic access to class members

**Level:** 1
**페이지 범위:** 401 - 407
**총 페이지 수:** 7
**ID:** 188

---

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
