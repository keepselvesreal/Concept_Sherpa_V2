# B.2.2 Accessing nested map fields with value getters

**메타데이터:**
- ID: 183
- 레벨: 2
- 페이지: 396-397
- 페이지 수: 2
- 부모 ID: 180
- 텍스트 길이: 2052 문자

---

nested map fields with value getters
The value getter approach applies naturally to nested map fields. As in the dynamic
getter section, suppose that search results are represented as a string map as in list-
ing B.12. Book fields are nested in the search results map, where
 Keys are book ISBNs.
 Values are book data represented as string maps as in the previous section.
ListingB.12 Search results represented as a map
Map searchResultsMap = Map.of(
"978-1779501127", Map.of(

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

370 APPENDIX B Generic data access in statically-typed languages
Value getters make data access a bit more convenient when avoiding type casting. The
next section shows how typed getters make it possible to benefit from compile-time
checks, even when data is represented as string maps.