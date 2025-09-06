# 12.3 Advanced data validation

**메타데이터:**
- ID: 118
- 레벨: 2
- 페이지: 285-287
- 페이지 수: 3
- 부모 ID: 114
- 텍스트 길이: 5264 문자

---

ta validation 257
return bookInfos;
};
Theo Excellent! Now we need to figure out how to deal with advanced data validation.
12.3 Advanced data validation
Dave What do you mean by advanced data validation?
Theo I mean going beyond static types.
Dave Could you give me an example?
Theo Sure. Take, for instance, the publication year of a book. It’s an integer, but
what else could you say about this number?
Dave It has to be positive. It would say it’s a positive integer.
Theo Come on, Dave! Be courageous, go beyond types.
Dave I don’t know. I would say it’s a number that should be higher than 1900. I
don’t think it makes sense to have a book that is published before 1900.
Theo Exactly. And what about the higher limit?
Dave I’d say that the publication year should be less than the current year.
Theo Very good! I see that JSON Schema supports number ranges. Here is how we
can write the schema for an integer that represents a year and should be
between 1900 and 2021.
Listing12.12 The schema for an integer between 1900 and 2021
var publicationYearSchema = {
"type": "integer",
"minimum": 1900,
"maximum": 2021
};
Dave Why isn’t this kind of data validation possible in OOP?
Theo I’ll let you think about that for a moment.
Dave I think have it! In DOP, data validation is executed at run time, while static
type validation in OOP is executed at compile time. At compile time, we only
have information about static types; at run time, we have the data itself. That’s
why in DOP data validation, it’s possible to go beyond types.
 NOTE Of course, it’s also possible in traditional OOP to write custom run-time data
validation. Here, though, we are comparing data schema with static types.
Theo You got it! Now, let me show you how to write the schema for a string that
should match a regular expression.
 NOTE See http://mng.bz/OGNP for the JavaScript Guide to regular expressions.
Theo Let’s take for example the book ID. I am assuming it must be a UUID.
Dave Right.
Theo Can you write the regular expression for a valid UUID?

258 CHAPTER 12 Advanced data validation
Dave googles “UUID regex” and finds something he thinks just might work. He shows the
regular expression to Theo.
Listing12.13 The regular expression for a valid UUID
[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}
Dave Now, how do we plug a regular expression into a JSON Schema?
Theo While you were looking for the UUID regular expression, I read about the
pattern field. Here’s how we can plug the UUID regular expression into a
JSON Schema.
Listing12.14 The schema for a UUID
var uuidSchema = {
"type": "string",
"pattern": "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}" +
"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
};
Dave Nice! Let me improve the catalog schema and refine the schema for purchase-
Date, isbn, libId, and authorId with regular expressions.
Theo Before you do that, though, let me tell you something I read about regular
expressions: some of them are predefined. For example, there is a predefined
regular expression for dates.
Dave How does it work?
Theo With the help of the format field.
 NOTE According to JSON Schema specification, format is just for annotation and
doesn’t affect validation. But in practice, JSON Schema validation libraries use format
also for validation.
Theo moves to his laptop. He inputs the schema for a date and shows it to Dave.
Listing12.15 The schema for a date
{
"type": "string",
"format": "date"
}
TIP In DOP, data validation goes beyond static types (e.g., number ranges, regular
expressions, and so on).
Dave Very cool! Do I have all the information I need in order to refine the catalog
schema?
Theo Yes, go for it!
It takes Dave a bit of time to write the regular expressions for isbn, authorId, and libId.
But with the help of Google (again) and a bit of simplification, Dave comes up with the
schema in listings 12.16 and 12.17.

12.3 Advanced data validation 259
Listing12.16 The refined schema of the catalog data (Part 1)
var isbnSchema = {
"type": "string",
"pattern": "^[0-9-]{10,20}$"
};
var libIdSchema = {
"type": "string",
"pattern": "^[a-z0-9-]{3,20}$"
};
var authorIdSchema ={
"type": "string",
"pattern": "[a-z-]{2,50}"
};
var bookItemSchema = {
"type": "object",
"additionalProperties": {
"id": uuidSchema,
"libId": libIdSchema,
"purchaseDate": {
"type": "string",
"format": "date"
},
"isLent": {"type": "boolean"}
}
};
Listing12.17 The refined schema of the catalog data (Part 2)
var bookSchema = {
"type": "object",
"required": ["title", "isbn", "authorIds", "bookItems"],
"properties": {
"title": {"type": "string"},
"publicationYear": publicationYearSchema,
"isbn": isbnSchema,
"publisher": {"type": "string"},
"authorIds": {
"type": "array",
"items": authorIdSchema
},
"bookItems": bookItemSchema
}
};
var authorSchema = {
"type": "object",
"required": ["id", "name", "bookIsbns"],
"properties": {
"id": {"type": "string"},
"name": {"type": "string"},

260 CHAPTER 12 Advanced data validation
"bookIsbns": {
"items": isbnSchema
}
}
};
var catalogSchema = {
"type": "object",
"properties": {
"booksByIsbn": {
"type": "object",
"additionalProperties": bookSchema
},
"authorsById": {
"type": "object",
"additionalProperties": authorSchema
}
},
"required": ["booksByIsbn", "authorsById"]
};