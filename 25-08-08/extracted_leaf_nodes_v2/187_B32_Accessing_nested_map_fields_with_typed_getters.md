# B.3.2 Accessing nested map fields with typed getters

**메타데이터:**
- ID: 187
- 레벨: 2
- 페이지: 399-400
- 페이지 수: 2
- 부모 ID: 184
- 텍스트 길이: 2055 문자

---

nested map fields with typed getters
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