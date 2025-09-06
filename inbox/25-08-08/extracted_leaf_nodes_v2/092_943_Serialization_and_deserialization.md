# 9.4.3 Serialization and deserialization

**메타데이터:**
- ID: 92
- 레벨: 3
- 페이지: 220-220
- 페이지 수: 1
- 부모 ID: 88
- 텍스트 길이: 1545 문자

---

ion and deserialization
Theo Does Immutable.js also support JSON serialization and deserialization?
Joe It supports serialization out of the box. As for deserialization, we need to write
our own function.
Theo Does Immutable.js provide an Immutable.stringify() function?
Joe That’s not necessary because the native JSON.stringify() function works
with Immutable.js objects. Here’s another example.
Listing9.17 JSON serialization of an Immutable.js collection
var bookInfo = Immutable.fromJS({
"isbn": "978-1779501127",
"title": "Watchmen",
"authorNames": ["Alan Moore",
"Dave Gibbons"]
});
JSON.stringify(bookInfo);
// → {\"isbn\":\"978-1779501127\",\"title\":\"Watchmen\",
// → \"authorNames\":[\"Alan Moore\",\"Dave Gibbons\"]}
Theo How does JSON.stringify() know how to handle an Immutable.js collection?
Joe As an OOP developer, you shouldn’t be surprised by that.
Theo Hmm...let me think a minute. OK, here’s my guess. Is that because JSON
.stringify() calls some method on its argument?
Joe Exactly! If the object passed to JSON.stringify() has a .toJSON() method,
it’s called by JSON.stringify().
Theo Nice. What about JSON deserialization?
Joe That needs to be done in two steps. You first convert the JSON string to a Java-
Script object and then to an immutable collection.
Theo Something like this piece of code?
Listing9.18 Converting a JSON string into an immutable collection
Immutable.parseJSON = function(jsonString) {
return Immutable.fromJS(JSON.parse(jsonString));
};
Joe Exactly.

9.4 Persistent data structures in action 193