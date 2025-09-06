# B.1.1 Accessing non-nested map fields with dynamic getters

**메타데이터:**
- ID: 178
- 레벨: 2
- 페이지: 393-393
- 페이지 수: 1
- 부모 ID: 176
- 텍스트 길이: 2346 문자

---

non-nested map fields with dynamic getters
Throughout this appendix, we will illustrate various ways to provide generic data access
using a book record. Our record is made of these parts:
 title (a string)
 isbn (a string)
 publicationYear (an integer)
Listing B.1 shows the representation of two books, Watchmen and Seven Habits of Highly
Effective People, in Java. These string maps contain values that are of type Object.
ListingB.1 Two books represented as maps
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
The map fields can be accessed generically using a dynamic getter. The following list-
ing shows the implementation.
ListingB.2 The implementation of dynamic getter for map fields
class DynamicAccess {
static Object get(Map m, String k) {
return (m).get(k);
}
}
The drawback of dynamic getters is that a type cast is required to manipulate the value
of a map field. For instance, as shown in listing B.3, a cast to String is needed to call
the toUpperCase string method on the title field value.
ListingB.3 Accessing map fields with a dynamic getter and type casting
((String)DynamicAccess.get(watchmenMap, "title")).toUpperCase();
// → "WATCHMEN"
Dynamic getters provide generic data access in the sense that they do not require spe-
cific knowledge of the type of data the string map represents. As a consequence, the
name of the field can be received dynamically (e.g., from the user) as listing B.4
shows. This works because, in order to access a book data field in a string map, it is not
necessary to import the class that defines the book.

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