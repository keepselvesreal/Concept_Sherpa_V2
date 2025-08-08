# B.4.2 Generic access to nested class members

**메타데이터:**
- ID: 191
- 레벨: 2
- 페이지: 404-405
- 페이지 수: 2
- 부모 ID: 188
- 텍스트 길이: 3395 문자

---

cess to nested class members
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