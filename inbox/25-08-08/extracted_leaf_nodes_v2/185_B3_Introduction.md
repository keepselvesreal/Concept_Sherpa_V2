# B.3 Introduction

**메타데이터:**
- ID: 185
- 레벨: 2
- 페이지: 398-399
- 페이지 수: 2
- 부모 ID: 184
- 텍스트 길이: 6234 문자

---

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

=== Page 398 ===
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

=== Page 399 ===
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

=== Page 400 ===
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