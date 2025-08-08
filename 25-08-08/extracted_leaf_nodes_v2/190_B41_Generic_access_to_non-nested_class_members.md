# B.4.1 Generic access to non-nested class members

**메타데이터:**
- ID: 190
- 레벨: 2
- 페이지: 401-403
- 페이지 수: 3
- 부모 ID: 188
- 텍스트 길이: 5261 문자

---

cess to non-nested class members
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