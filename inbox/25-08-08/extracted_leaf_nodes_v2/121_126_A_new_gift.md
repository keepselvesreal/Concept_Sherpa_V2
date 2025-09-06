# 12.6 A new gift

**메타데이터:**
- ID: 121
- 레벨: 2
- 페이지: 297-297
- 페이지 수: 1
- 부모 ID: 114
- 텍스트 길이: 3410 문자

---

269
 NOTE See https://github.com/clj-kondo/clj-kondo and https://github.com/metosin/
malli for the autocompletion feature provided by clj-kondo and its integration with Malli.
Dave Do you think that someday this functionality will be available in other program-
ming languages?
Joe Absolutely. IDEs like IntelliJ and Visual Studio Code already support JSON
Schema validation for JSON files. It’s only a matter of time before they support
JSON Schema validation for function arguments and provide autocompletion
of the field names in a map.
Dave I hope it won’t take them too much time.
12.6 A new gift
When Joe leaves the office, Dave gets an interesting idea. He shares it with Theo.
Dave Do you think we could make our own JSON Schema cheat sheet with the
advanced JSON schema features that we discovered today?
Theo Excellent idea! But you’ll have to do it on your own. I have to run to a meeting!
After his meeting, Theo comes back to Dave’s desk. When he sees Theo, Dave takes a
small package like the one Joe gave Theo a few weeks ago from the top of his desk. This
one, however, is wrapped in a light blue ribbon. With a solemn demeanor, Dave hands
Theo the gift.
When Theo undoes the ribbon, he discovers an stylish piece of paper decorated with lit-
tle computers in different colors. In the center of the paper, he reads the inscription,
“Advanced JSON Schema cheat sheet.” Theo smiles while browsing the JSON schema (see
listing 12.30). Then, he turns the paper over to find that the back is also filled with draw-
ings, this time keyboards and mice. In the center of the paper, Theo reads the inscription,
“Example of valid data” (see listing 12.31).
Listing12.30 Advanced JSON Schema cheat sheet
The { At the root level,
properties "type": "array", data is an array.
of each "items": {
field in the "type": "object", Each element of the
map "properties": { array is a map. myEnum is an
"myNumber": {"type": "number"}, enumeration value
myNumber "myString": {"type": "string"}, with two possibilities,
is a number. "myEnum": {"enum": ["myVal", "yourVal"]}, "myVal" and "yourVal".
"myBool": {"type": "boolean"}
myBool is
myString is "myAge": {
myAge is a boolean.
a string. "type": "integer",
an integer
"minimum": 0, between 0
"maximum": 120 and 120.
},
"myBirthday": {
myBirthday is a string
"type": "string",
conforming to the date
"format": "date"
format.
},

270 CHAPTER 12 Advanced data validation
"myLetters": {
myLetters is a string with
"type": "string",
letters only (lowercase or
"pattern": "[a-zA-Z]*"
uppercase).
}
"myNumberMap": {
myNumberMap is an homogeneous
"type": "object",
string map where all the values are
"additionalProperties": {"type": "number"}
numbers.
},
"myTuple": {
myTuple is a tuple where the first
"type": "array",
element is a string and the second
"prefixItems": [
element is a number.
{ "type": "string" },
{ "type": "number" }
]
} The mandatory fields in the map
are myNumber and myString.
},
Other fields are optional.
"required": ["myNumber", "myString"],
"additionalProperties": false
We don’t allow fields that
}
are not explicitly mentioned
}
in the schema.
Listing12.31 An example of valid data
[
{
"myNumber": 42,
"myString": "I-love-you",
"myEnum": "myVal",
"myBool": true,
"myTuple": ["Hello", 42]
},
{
"myNumber": 54,
"myString": "Happy",
"myAge": 42,
"myBirthday": "1978-11-23",
"myLetters": "Hello",
"myNumberMap": {
"banana": 23,
"apple": 34
}
}
]