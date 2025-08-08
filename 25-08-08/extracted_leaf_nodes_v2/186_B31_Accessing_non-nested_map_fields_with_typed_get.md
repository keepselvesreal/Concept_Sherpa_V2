# B.3.1 Accessing non-nested map fields with typed getters

**메타데이터:**
- ID: 186
- 레벨: 2
- 페이지: 398-398
- 페이지 수: 1
- 부모 ID: 184
- 텍스트 길이: 2294 문자

---

non-nested map fields with typed getters
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