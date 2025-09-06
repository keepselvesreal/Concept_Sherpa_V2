# B.1.2 Accessing nested map fields with dynamic getters

**메타데이터:**
- ID: 179
- 레벨: 2
- 페이지: 394-394
- 페이지 수: 1
- 부모 ID: 176
- 텍스트 길이: 1055 문자

---

nested map fields with dynamic getters
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