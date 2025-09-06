# B.4.3 Automatic JSON serialization of objects

**메타데이터:**
- ID: 192
- 레벨: 2
- 페이지: 406-407
- 페이지 수: 2
- 부모 ID: 188
- 텍스트 길이: 1710 문자

---

JSON serialization of objects
An approach similar to the one illustrated in the previous section is used by JSON seri-
alization libraries like Gson (https://github.com/google/gson) in order to serialize
objects to JSON automatically. Gson uses reflection to go over the class members, gen-
erating a JSON representation of each member value. Listing B.37 displays an exam-
ple of Gson in action.

B.4 Generic access to class members 379
ListingB.37 JSON serialization of an object with Gson
import com.google.gson.*;
var gson = new Gson();
BookData sevenHabitsRecord = new BookData(
"978-1982137274",
"7 Habits of Highly Effective People",
2020
);
System.out.println(gson.toJson(sevenHabitsRecord));
// → {"title":"7 Habits of Highly Effective People", …}
Listing B.38 shows how it also works with objects nested in maps. Listing B.39 then
provides an example with objects nested in objects.
ListingB.38 JSON serialization of objects nested in a map with Gson
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
System.out.println(gson.toJson(searchResultsRecords));
// → {"978-1779501127":{"isbn":"978-1779501127","title":"Watchmen", …}}
ListingB.39 JSON serialization of an object nested in an object with Gson
BookData sevenHabitsNestedRecord = new BookWithAttributes(
"978-1982137274",
"7 Habits of Highly Effective People",
2020,
432,
"en"
);
System.out.println(gson.toJson(sevenHabitsNestedRecord));
// → {"isbn":"978-1982137274",
// → "title":"7 Habits of Highly Effective People", …}

380 APPENDIX B Generic data access in statically-typed languages