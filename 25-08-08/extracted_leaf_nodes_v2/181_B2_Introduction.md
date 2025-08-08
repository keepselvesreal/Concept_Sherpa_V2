# B.2 Introduction

**메타데이터:**
- ID: 181
- 레벨: 2
- 페이지: 395-396
- 페이지 수: 2
- 부모 ID: 180
- 텍스트 길이: 6383 문자

---

=== Page 394 ===
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

=== Page 395 ===
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

=== Page 396 ===
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

=== Page 397 ===
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