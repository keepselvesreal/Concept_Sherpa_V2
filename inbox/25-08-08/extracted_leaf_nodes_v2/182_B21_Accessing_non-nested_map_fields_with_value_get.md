# B.2.1 Accessing non-nested map fields with value getters

**메타데이터:**
- ID: 182
- 레벨: 2
- 페이지: 395-395
- 페이지 수: 1
- 부모 ID: 180
- 텍스트 길이: 1954 문자

---

non-nested map fields with value getters
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