# 7.4 Schema composition

7.4 Schema composition
Theo What about validating data that comes from an external web service?
Joe Can you give me an example?
Theo In the near future, we’ll have to integrate with a service called Open Library
Books API that provides detailed information about books.
 NOTE For information on the Open Library Books API, see https://openlibrary
.org/dev/docs/api/books.
Joe Can you show me, for instance, the service response for Watchmen?
Theo Sure. Here you go.
Theo taps a few keys on his keyboard and brings up the response. Joe looks at the JSON for
a long time.
Listing7.16 An Open Library Books API response example
{
"publishers": [
"DC Comics"
],
"number_of_pages": 334,
"weight": "1.4 pounds",
"physical_format": "Paperback",
"subjects": [
"Graphic Novels",
"Comics & Graphic Novels",
"Fiction",
"Fantastic fiction"
],
"isbn_13": [
"9780930289232"
],
"title": "Watchmen",
"isbn_10": [
"0930289234"
],
"publish_date": "April 1, 1995",
"physical_dimensions": "10.1 x 6.6 x 0.8 inches"
}
Theo asks himself, “What could be so special in this JSON?” While Joe is meditating about
this piece of JSON, Theo writes the JSON Schema for the Books API response. It doesn’t
seem to be more complicated than any of the previous schemas. When Theo is done, he
asks Joe to take a look at the schema.
Listing7.17 Schema of the Open Library Books API response
{
"type": "object",
"required": ["title"],

## 페이지 183

7.4 Schema composition 155
"properties": {
"title": {"type": "string"},
"publishers": {
"type": "array",
"items": {"type": "string"}
},
"number_of_pages": {"type": "integer"},
"weight": {"type": "string"},
"physical_format": {"type": "string"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn_13": {
"type": "array",
"items": {"type": "string"}
},
"isbn_10": {
"type": "array",
"items": {"type": "string"}
},
"publish_date": {"type": "string"},
"physical_dimensions": {"type": "string"}
}
}
Joe Good job!
Theo That wasn’t so hard. I really don’t see why you looked at this JSON response for
such a long time.
Joe Well, it has to do with the isbn_10 and isbn_13 fields. I assume that they’re
not both mandatory.
Theo Right! That’s why I didn’t include them in the required field of my schema.
Joe But one of them should always be there. Right?
Theo Sometimes one of them and sometimes both of them, like for Watchmen. It
depends on the publication year of the book. Books published before 2007
have isbn_10, and books published after 2007 have isbn_13.
Joe Oh, I see. And Watchmen has both because it was originally published in 1986
but published again after 2007.
Theo Correct.
Joe Then, you need your schema to indicate that one of the isbn fields is man-
datory. That’s a good opportunity for me to tell you about JSON Schema
composition.
Theo What’s that?
Joe It’s a way to combine schemas, similarly to how we combine logical conditions
with AND, OR, and NOT.
Theo I’d like to see that.
Joe Sure. How would you express the schema for the Books API response as a
composition of three schemas: basicBookInfoSchema, the schema that you
wrote where only title is required; mandatoryIsbn13, a schema where only

## 페이지 184

156 CHAPTER 7 Basic data validation
isbn_13 is required; and mandatoryIsb10, a schema where only isbn_10 is
required?
Theo I think it should be basicBookInfoSchema AND (mandatoryIsbn13 OR
mandatoryIsbn10).
Joe Exactly! The only thing is that in JSON Schema, we use allOf instead of AND,
and anyOf instead of OR.
Joe shows Theo the result in listing 7.18 and an example of its usage in listing 7.19.
Listing7.18 Schema of an external API response
var basicBookInfoSchema = {
"type": "object",
"required": ["title"],
"properties": {
"title": {"type": "string"},
"publishers": {
"type": "array",
"items": {"type": "string"}
},
"number_of_pages": {"type": "integer"},
"weight": {"type": "string"},
"physical_format": {"type": "string"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn_13": {
"type": "array",
"items": {"type": "string"}
},
"isbn_10": {
"type": "array",
"items": {"type": "string"}
},
"publish_date": {"type": "string"},
"physical_dimensions": {"type": "string"}
}
};
var mandatoryIsbn13 = {
"type": "object",
"required": ["isbn_13"]
};
var mandatoryIsbn10 = {
"type": "object",
"required": ["isbn_10"]
};
var bookInfoSchema = {
"allOf": [
basicBookInfoSchema,
{

## 페이지 185

7.4 Schema composition 157
"anyOf": [mandatoryIsbn13, mandatoryIsbn10]
}
]
};
Listing7.19 Validating an external API response
var bookInfo = {
"publishers": [
"DC Comics"
],
"number_of_pages": 334,
"weight": "1.4 pounds",
"physical_format": "Paperback",
"subjects": [
"Graphic Novels",
"Comics & Graphic Novels",
"Fiction",
"Fantastic fiction"
],
"isbn_13": [
"9780930289232"
],
"title": "Watchmen",
"isbn_10": [
"0930289234"
],
"publish_date": "April 1, 1995",
"physical_dimensions": "10.1 x 6.6 x 0.8 inches"
};
validate(bookInfoSchema, bookInfo);
// → true
Theo I see why they call it allOf and anyOf. The first one means that data must con-
form to all the schemas, and the second one means that data must conform to
any of the schemas.
Joe Yup.
 NOTE JSON Schema also supports oneOf for cases where data must be valid against
exactly one schema.
Theo Nice. With schema composition, JSON Schema seems to have more expressive
power than what I was used to when representing data with classes.
Joe That’s only the beginning. I’ll show you more data validation conditions that
can’t be expressed when data is represented with classes some other time.
 NOTE Advanced data validation is covered in chapter 12.
Theo Something still bothers me, though. When data isn’t valid, you don’t know what
went wrong.

## 페이지 186

158 CHAPTER 7 Basic data validation