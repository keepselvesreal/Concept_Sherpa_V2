# Chapter 7: Basic data validation

**부제목:** A solemn gift
**계획된 페이지:** 169-190
**실제 페이지:** 169-190

=== PAGE 169 ===
Basic data validation
A solemn gift
This chapter covers
 The importance of validating data at system
boundaries
 Validating data using the JSON Schema language
 Integrating data validation into an existing code
base
 Getting detailed information about data validation
failures
At first glance, it may seem that embracing DOP means accessing data without validat-
ing it and engaging in wishful thinking, where data is always valid. In fact, data valida-
tion is not only possible but recommended when we follow data-oriented principles.
This chapter illustrates how to validate data when data is represented with
generic data structures. It focuses on data validation occurring at the boundaries of
the system, while in part 3, we will deal with validating data as it flows through the
system. This chapter is a deep dive into the fourth principle of DOP.
PRINCIPLE #4 Separate data schema from data representation.
141

=== PAGE 170 ===
142 CHAPTER 7 Basic data validation
7.1 Data validation in DOP
Theo has rescheduled his meetings. With such an imposing deadline, he’s still not sure if
he’s made a big mistake giving DOP a second chance.
 NOTE The reason why Theo rescheduled his meetings is explained in the opener
for part 2. Take a moment to read the opener if you missed it.
Joe What aspect of OOP do you think you will miss the most in your big project?
Theo Data validation.
Joe Can you elaborate a bit?
Theo In OOP, I have this strong guarantee that when a class is instantiated, its mem-
ber fields have the proper names and proper types. But with DOP, it’s so easy
to have small mistakes in field names and field types.
Joe Well, I have good news for you! There is a way to validate data in DOP.
Theo How does it work? I thought DOP and data validation were two contradictory
concepts!
Joe Not at all. It’s true that DOP doesn’t force you to validate data, but it doesn’t
prevent you from doing so. In DOP, the data schema is separate from the data
representation.
Theo I don’t get how that would eliminate data consistency issues.
Joe According to DOP, the most important data to validate is data that crosses the
boundaries of the system.
Theo Which boundaries are you referring to?
Joe In the case of a web server, it would be the areas where the web server commu-
nicates with its clients and with its data sources.
Theo A diagram might help me see it better.
Joe goes to the whiteboard and picks up the pen. He then draws a diagram like the one in
figure 7.1.
Client (e.g., web browser)
Data
Web server
Data Data
Web service Database Figure 7.1 High-level architecture of
a modern web server

=== PAGE 171 ===
7.2 JSON Schema in a nutshell 143
Joe This architectural diagram defines what we call the boundaries of the system in
terms of data exchange. Can you tell me what the three boundaries of the sys-
tem are?
 NOTE The boundaries of a system are defined as the areas where the system exchanges
data.
Theo Let me see. The first one is the client boundary, then we have the database
boundary, and finally, the web service boundary.
Joe Exactly! It’s important to identify the boundaries of a system because, in
DOP, we differentiate between two kinds of data validation: validation that
occurs at the boundaries of the system and validation that occurs inside the
system. Today, we’re going to focus on validation that occurs at the boundar-
ies of the system.
Theo Does that mean data validation at the boundaries of the system is more
important?
Joe Absolutely! Once you’ve ensured that data going into and out of the system is
valid, the odds for an unexpected piece of data inside the system are pretty low.
TIP When data at system boundaries is validated, it’s not critical to validate data
again inside the system.
Theo Why do we need data validation inside the system then?
Joe It has to do with making it easier to code your system as your code base grows.
Theo And, what’s the main purpose of data validation at the boundaries?
Joe To prevent invalid data from going in and out of the system, and to display
informative errors when we encounter invalid data. Let me draw a table on the
whiteboard so you can see the distinction (table 7.1).
Table 7.1 Two kinds of data validation
Kind of data validation Purpose Environment
Boundaries Guardian Production
Inside Ease of development Dev
Theo When will you teach me about data validation inside the system?
Joe Later, when the code base is bigger.
7.2 JSON Schema in a nutshell
Theo For now, the Library Management System is an application that runs in mem-
ory, with no database and no HTTP clients connected to it. But Nancy will
probably want me to make the system into a real web server with clients, data-
base, and external services.
Joe OK. Let’s imagine how a client request for searching books would look.

=== PAGE 172 ===
144 CHAPTER 7 Basic data validation
Theo Basically, a search request is made of a string and the fields you’d like to
retrieve for the books whose title contains the string. So the request has two
fields: title, which is a string, and fields, which is an array of strings.
Theo quickly writes on the whiteboard. When he finishes, he steps aside to let Joe view his
code for a search request.
Listing7.1 An example of a search request
{
"title": "habit",
"fields": ["title", "weight", "number_of_pages"]
}
Joe I see. Let me show you how to express the schema of a search request sepa-
rately from the representation of the search request data.
Theo What do you mean exactly by “separately?”
Joe Data representation stands on its own, and the data schema stands on its own.
You are free to validate that a piece of data conforms with a data schema as you
will and when you will.
TIP In DOP, the data schema is separate from the data representation.
Theo It’s a bit abstract for me.
Joe I know. It will become much clearer in a moment. For now, I am going to show
you how to build the data schema for the search request in a schema language
called JSON Schema.
Theo I love JSON!
 NOTE Information on the JSON Schema language can be found at https://json
-schema.org. The schemas in this book use JSON Schema version 2020-12.
Joe First, we have to express the data type of the request. What’s the data type in
the case of a book search request?
Theo It’s a map.
Joe In JSON Schema, the data type for maps is called object. Look at this basic
skeleton of a map. It’s a map with two fields: type and properties.
Joe goes to the whiteboard. He quickly writes the code for the map with its two fields.
Listing7.2 Basic schema skeleton of a map
{
"type": "object",
"properties": {...}
}

=== PAGE 173 ===
7.2 JSON Schema in a nutshell 145
Joe The value of type is "object", and the value of properties is a map with the
schema for the map fields.
Theo I assume that, inside properties, we are going to express the schema of the map
fields as JSON Schema.
Joe Correct.
Theo I am starting to feel the dizziness of recursion.
Joe In JSON Schema, a schema is usually a JSON object with a field called type,
which specifies the data type. For example, the type for the title field is
string and...
Theo ...the type for the fields field is array.
Joe Yes!
Now it’s Theo’s turn to go to the whiteboard. He fills the holes in the search request
schema with the information about the fields.
Listing7.3 Schema skeleton for search request
{
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {"type": "array"}
}
}
On Theo’s way back from the whiteboard to his desk, Joe makes a sign with his right hand
that says, “Stay near the whiteboard, please.” Theo turns and goes back to the whiteboard.
Joe We can be a little more precise about the fields property by providing infor-
mation about the type of the elements in the array. In JSON Schema, an array
schema has a property called items, whose value is the schema for the array
elements.
Without any hesitation, Theo adds this information on the whiteboard. Stepping aside, he
shows Joe the result.
Listing7.4 Schema for search request with information about array elements
{
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {"type": "string"}
}
}
}

=== PAGE 174 ===
146 CHAPTER 7 Basic data validation
Before going back to his desk, Theo asks Joe:
Theo Are we done now?
Joe Not yet. We can be more precise about the fields field in the search request.
I assume that the fields in the request should be part of a closed list of fields.
Therefore, instead of allowing any string, we could have a list of allowed values.
Theo Like an enumeration value?
Joe Exactly! In fact, JSON Schema supports enumeration values with the enum key-
word. Instead of {"type": "string"}, you need to have {"enum": […]} and
replace the dots with the supported fields.
Once again, Theo turns to the whiteboard. He replaces the dots with the information Joe
requests.
Listing7.5 Schema for the search request with enumeration values
{
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {
"enum": [
"publishers",
"number_of_pages",
"weight",
"physical_format",
"subjects",
"publish_date",
"physical_dimensions"
]
}
}
}
}
Theo Are we done, now?
Joe Almost. We need to decide whether the fields of our search request are optional
or required. In our case, both title and fields are required.
Theo How do we express this information in JSON Schema?
Joe There is a field called required whose value is an array made of the names of
the required fields in the map.
After adding the required field, Theo looks at Joe. This time he makes a move with his
right hand that says, “Now you can go back to your desk.”
Listing7.6 Schema of a search request
var searchBooksRequestSchema = {
"type": "object",

=== PAGE 175 ===
7.2 JSON Schema in a nutshell 147
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {
"enum": [
"publishers",
"number_of_pages",
"weight",
"physical_format",
"subjects",
"publish_date",
"physical_dimensions"
]
}
}
},
"required": ["title", "fields"]
};
Joe Now I’ll show you how to validate a piece of data according to a schema.
Theo What do you mean, validate?
Joe Validating data according to a schema means checking whether data conforms
to the schema. In our case, it means checking whether a piece of data is a valid
search books request.
TIP Data validation in DOP means checking whether a piece of data conforms to a
schema.
Theo I see.
Joe There are a couple of libraries that provide JSON Schema validation. They
have a validate function that receives a schema and a piece of data and
returns true when the data is valid and false when the data is not valid. I just
happen to have a file in my laptop that provides a table with a list of schema
validation libraries (table 7.2). We can print it out if you like.
Theo turns on the printer as Joe scans through his laptop for the table. When he has it up,
he checks with Theo and presses Print.
Table 7.2 Libraries for JSON Schema validation
Language Library URL
JavaScript Ajv https://github.com/ajv-validator/ajv
Java Snow https://github.com/ssilverman/snowy-json
C# JSON.net Schema https://www.newtonsoft.com/jsonschema
Python jschon https://github.com/marksparkza/jschon
Ruby JSONSchemer https://github.com/davishmcclurg/json_schemer

=== PAGE 176 ===
148 CHAPTER 7 Basic data validation
Theo So, if I call validate with this search request and that schema, it will return
true?
Theo indicates the search request example from listing 7.7 and the schema from listing 7.6.
Listing7.7 An example of a search request
{
"title": "habit",
"fields": ["title", "weight", "number_of_pages"]
}
Joe Give it a try, and you’ll see.
Indeed! When Theo executes the code to validate the search request, it returns true.
Listing7.8 Validating the search request
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {"type": "string"}
}
},
"required": ["title", "fields"]
};
var searchBooksRequest = {
"title": "habit",
"fields": ["title", "weight", "number_of_pages"]
};
validate(searchBooksRequestSchema, searchBooksRequest);
// → true
Joe Now, please try an invalid request.
Theo Let me think about what kind of invalidity to try. I know, I’ll make a typo in the
title field and call it tilte with the l before the t.
As expected, the code with the type returns false. Theo is not surprised, and Joe is smil-
ing from ear to ear.
Listing7.9 Validating an invalid search request
var invalidSearchBooksRequest = {
"tilte": "habit",
"fields": ["title", "weight", "number_of_pages"]
};

=== PAGE 177 ===
7.3 Schema flexibility and strictness 149
validate(searchBooksRequestSchema, invalidSearchBooksRequest);
// → false
Theo The syntax of JSON Schema is much more verbose than the syntax for declar-
ing the members in a class. Why is that so?
Joe For two reasons. First, because JSON Schema is language independent, it can
be used in any programming language. As I told you, there are JSON Schema
validators available in most programming languages.
Theo I see.
Joe Second, JSON Schema allows you to express validation conditions that are much
harder, if not impossible, to express when data is represented with classes.
TIP The expressive power of JSON Schema is high!
Theo Now you have triggered my curiosity. Can you give me some examples?
Joe In a moment, we’ll talk about schema composition. Someday I’ll show you
some examples of advanced validation.
 NOTE Advanced validation is covered in chapter 12.
Theo What kind of advanced validation?
Joe What I mean by advanced validation is, for instance, validating that a number
falls within a given range or validating that a string matches a regular expression.
Theo Is there a way to get details about why the request is invalid?
Joe Absolutely! I’ll show you later. For now, let me show you how to make sure the
response the server sends back to the client is valid.
Theo It sounds much more complicated than a search book request!
Joe Why?
Theo Because a search response is made of multiple book results, and in each book
result, some of the fields are optional!
7.3 Schema flexibility and strictness
Joe Can you give me an example of what a book search response would look like?
Theo Take a look at this example. It’s a search response with information about two
books: 7 Habits of Highly Effective People and The Power of Habit.
Listing7.10 An example of a search response
[
{
"title": "7 Habits of Highly Effective People",
"available": true,
"isbn": "978-0812981605",
"subtitle": "Powerful Lessons in Personal Change",
"number_of_pages": 432
},

=== PAGE 178 ===
150 CHAPTER 7 Basic data validation
{
"title": "The Power of Habit",
"available": false,
"isbn_13": "978-1982137274",
"subtitle": "Why We Do What We Do in Life and Business",
"subjects": [
"Social aspects",
"Habit",
"Change (Psychology)"
]
}
]
Joe It’s funny that you mention The Power of Habit. I’m reading this book in order
to get rid of my habit of biting my nails. Anyway, what fields are required and
what fields are optional in a book search response?
Theo In book information, the title and available fields are required. The other
fields are optional.
Joe As I told you when we built the schema for the book search request, fields in a
map are optional by default. In order to make a field mandatory, we have to
include it in the required array. I’d probably implement it with something
like this.
Listing7.11 Schema of a search response
var searchBooksResponseSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["title", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"subtitle": {"type": "string"},
"number_of_pages": {"type": "integer"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn": {"type": "string"},
"isbn_13": {"type": "string"}
}
}
};
TIP In JSON Schema, map fields are optional by default.
Theo I must admit that specifying a list of required fields is much simpler than hav-
ing to specify that a member in a class in nullable!
Joe Agreed!
Theo On the other hand, I find the nesting of the book information schema in the
search response schema a bit hard to read.

=== PAGE 179 ===
7.3 Schema flexibility and strictness 151
Joe Nothing prevents you from separating the book information schema from the
search response schema.
Theo How?
Joe It’s just JSON, my friend. It means, you are free to manipulate the schema as
any other map in your program. For instance, you could have the book infor-
mation schema in a variable named bookInfoSchema and use it in the search
books response schema. Let me refactor the schema to show you what I mean.
Listing7.12 Schema of a search response refactored
var bookInfoSchema = {
"type": "object",
"required": ["title", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"subtitle": {"type": "string"},
"number_of_pages": {"type": "integer"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn": {"type": "string"},
"isbn_13": {"type": "string"}
}
};
var searchBooksResponseSchema = {
"type": "array",
"items": bookInfoSchema
};
Theo Once again, I have to admit that JSON Schemas are more composable than
class definitions.
TIP JSON Schemas are just maps. We are free to compose and manipulate them like
any other map.
Joe Let’s move on to validating data received from external data sources.
Theo Is that different?
Joe Not really, but I’ll take it as an opportunity to show you some other features of
JSON Schema.
Theo I’m curious to learn how data validation is used when we access data from the
database.
Joe Each time we access data from the outside, it’s a good practice to validate it.
Can you show me an example of how a database response for a search query
would look?
TIP It’s a good practice to validate data that comes from an external data source.

=== PAGE 180 ===
152 CHAPTER 7 Basic data validation
Theo When we query books from the database, we expect to receive an array of
books with three fields: title, isbn, and available. The first two values should
be strings, and the third one should be a Boolean.
Joe Are those fields optional or required?
Theo What do you mean?
Joe Could there be books for which some of the fields are not defined?
Theo No.
Joe In that case, the schema is quite simple. Would you like to try writing the
schema for the database response?
Theo Let me see. It’s an array of objects where each object has three properties, so
something like this?
Listing7.13 Schema of a database response
{
"type": "array",
"items": {
"type": "object",
"required": ["title", "isbn", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"isbn": {"type": "string"}
}
}
}
Joe Well done, my friend! Now, I want to tell you about the additionalProperties
field in JSON Schema.
Theo What’s that?
Joe Take a look at this array.
Listing7.14 A book array with an additional property
[
{
"title": "7 Habits of Highly Effective People",
"available": true,
"isbn": "978-0812981605",
"dummy_property": 42
},
{
"title": "The Power of Habit",
"available": false,
"isbn": "978-1982137274",
"dummy_property": 45
}
]

=== PAGE 181 ===
7.3 Schema flexibility and strictness 153
Joe Is it a valid database response?
Theo No. A database response should not have a dummy_property field. It should
have only the three required fields specified in the schema.
Joe It might be surprising but, by default, fields not specified in the schema of an
object are allowed in JSON Schema. In order to disallow them, one has to set
additionalProperties to false like this.
Listing7.15 Disallowing properties not mentioned in the schema
var booksFromDBSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["title", "isbn", "available"],
"additionalProperties": false,
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"isbn": {"type": "string"}
}
}
};
TIP In JSON Schema, by default, fields not specified in the schema of a map are
allowed.
Theo Why is that?
Joe The reason is that usually having additional fields in a map doesn’t cause
trouble. If your code doesn’t care about a field, it simply ignores it. But some-
times we want to be as strict as possible, and we set additionalProperties
to false.
Theo What about the search request and response schema from the previous discus-
sions? Should we set additionalProperties to false?
Joe That’s an excellent question. I’d say it’s a matter of taste. Personally, I like to
allow additional fields in requests and disallow them in responses.
Theo What’s the advantage?
Joe Well, the web server is responsible for the responses it sends to its clients. It
makes sense then to be as strict as possible. However, the requests are created
by the clients, and I prefer to do my best to serve my clients even when they are
not as strict as they should be.
Theo Naturally. “The client is always right.”
Joe Actually, I prefer the way Jon Postel formulated his robustness principle: “Be
conservative in what you send, be liberal in what you accept.”
TIP It’s a good practice to be strict with the data that you send and to be flexible with
the data that you receive.

=== PAGE 182 ===
154 CHAPTER 7 Basic data validation
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

=== PAGE 183 ===
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

=== PAGE 184 ===
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

=== PAGE 185 ===
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

=== PAGE 186 ===
158 CHAPTER 7 Basic data validation
7.5 Details about data validation failures
Joe So far, we’ve treated JSON Schema validation as though it were binary: either a
piece of data is valid or it isn’t.
Theo Right...
Joe But, in fact, when a piece of data is not valid, we can get details about the
reason of the invalidity.
Theo Like when a required field is missing, can we get the name of the missing field?
Joe Yes. When a piece of data is not of the expected type, we can get information
about that also.
Theo That sounds very useful!
Joe Indeed. Let me show you how it works. Until now, we used a generic validate
function, but when we deal with validation failures, we need to be more specific.
Theo Why?
Joe Because each data validator library has its own way of exposing the details of
adata validation failure. For instance, in JavaScript Ajv, the errors from the
last data validation are stored as an array inside the validator instance.
Theo Why an array?
Joe Because there could be several failures. But let’s start with the case of a single
failure. Imagine we encounter a search book request where the title field is
named myTitle instead of title. Take a look at this example. As you can see,
we first instantiate a validator instance.
Listing7.20 Accessing validation errors in Ajv
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {"type": "string"}
}
},
"required": ["title", "fields"]
};
var invalidSearchBooksRequest = {
"myTitle": "habit",
"fields": ["title", "weight", "number_of_pages"]
};
Instantiates a
var ajv = new Ajv(); validator instance
ajv.validate(searchBooksRequestSchema, invalidSearchBooksRequest);
ajv.errors
Displays the
validation errors

=== PAGE 187 ===
7.5 Details about data validation failures 159
Theo And what does the information inside the errors array look like?
Joe Execute the code snippet. You’ll see.
When Theo executes the code snippets from listing 7.20, he can hardly believe his eyes. He
looks at the details, finding the results hard to digest.
Listing7.21 Details for a single data validation failure in an array format
[
{
"instancePath": "",
"schemaPath": "#/required",
"keyword": "required",
"params": {
"missingProperty":"title"
},
"message": "must have required property 'title'"
}
]
Theo I find the contents of the errors array a bit hard to understand.
Joe Me too. Fortunately, Ajv provides a errorsText utility function to convert the
errors array in a human readable format. See, for instance, what is returned
when you call errorsText.
Listing7.22 Displaying the errors in human readable format
ajv.errorsText(ajv.errors);
// → "data must have required property 'title'"
Theo Let me see what happens when there are more than one validation failure in
the data.
Joe By default, Ajv catches only one validation error.
TIP By default, Ajv catches only the first validation failure.
Theo I guess that’s for performance reasons. Once the validator encounters an
error, it doesn’t continue the data parsing.
Joe Probably. Anyway, in order to catch more than one validation failure, you need
to pass the allErrors options to the Ajv constructor. Check out this code.
Listing7.23 Catching multiple validation failures
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {"type": "string"}

=== PAGE 188 ===
160 CHAPTER 7 Basic data validation
}
},
"required": ["title", "fields"]
};
A request with
three failures
var invalidSearchBooksRequest = {
"myTitle": "habit",
"fields": [1, 2]
}; Instantiates the Ajv constructor
with allErrors: true in order to
catch more than one failure
var ajv = new Ajv({allErrors: true});
ajv.validate(searchBooksRequestSchema,
invalidSearchBooksRequest); Converts the
errors to a human
readable format
ajv.errorsText(ajv.errors);
// → "data must have required property 'title',
// → data/fields/0 must be string,
// → data/fields/1 must be string"
Joe We validate a search request with myTitle instead of title and numbers
instead of strings in the fields array. As you can see in the output of the code
snippet, three errors are returned.
Theo Great! I think I have all that I need in order to add data validation to the
boundaries of my system when Nancy asks me to make the Library Manage-
ment System into a web server.
Joe Would you allow me to give you a small gift as a token of our friendship?
Theo I’d be honored.
Joe takes a small package out of his bag, wrapped in a light-green ribbon. He hands Theo
the package with a solemn gesture.
When Theo undoes the ribbon, he discovers an elegant piece of paper decorated with
pretty little designs. In the center of the paper, Theo manages to read the inscription
“JSON Schema cheat sheet.” He smiles while browsing the cheat sheet. It’s exactly what he
needs.
Listing7.24 JSON Schema cheat sheet
{ At the root level,
data is an array.
"type": "array",
"items": { Each element of the
array is a map.
"type": "object",
myNumber "properties": {
The properties of
is a number. "myNumber": {"type": "number"},
each field in the map
"myString": {"type": "string"},
myString is
"myEnum": {"enum": ["myVal", "yourVal"]},
a string. myEnum is a
"myBool": {"type": "boolean"}
enumeration
myBool is a }, value with two
boolean. "required": ["myNumber", "myString"], possibilities:
The mandatory fields in the map "myVal" and
are myNumber and myString; "yourVal".
other fields are optional.

=== PAGE 189 ===
Summary 161
"additionalProperties": false
We don’t allow fields that
}
are not explicitly mentioned
}
in the schema.
Then, Theo turns the paper over to find that the back is also filled with drawings. In the
center of the paper, he reads the inscription, “An example of valid data.”
Listing7.25 An example of valid data
[
{
This map is valid
"myNumber": 42,
because all its
"myString": "Hello",
fields are valid.
"myEnum": "myVal",
"myBool": true
},
{
This map is valid
"myNumber": 54,
because it contains all
"myString": "Happy"
the required fields.
}
]
Summary
 DOP Principle #4 is to separate data schema and data representation.
 The boundaries of a system are defined to be the areas where the system
exchanges data.
 Some examples of data validation at the boundaries of the system are validation
of client requests and responses, and validation of data that comes from exter-
nal sources.
 Data validation in DOP means checking whether a piece of data conforms to a
schema.
 When a piece of data is not valid, we get information about the validation fail-
ures and send this information back to the client in a human readable format.
 When data at system boundaries is valid, it’s not critical to validate data again
inside the system.
 JSON Schema is a language that allows us to separate data validation from data
representation.
 JSON Schema syntax is a bit verbose.
 The expressive power of JSON Schema is high.
 JSON Schemas are just maps and, as so, we are free to manipulate them like any
other maps in our programs.
 We can store a schema definition in a variable and use this variable in another
schema.
 In JSON Schema, map fields are optional by default.
 It’s good practice to validate data that comes from an external data source.

=== PAGE 190 ===
162 CHAPTER 7 Basic data validation
 It’s good practice to be strict regarding data that you send and to be flexible
regarding data that you receive.
 Ajv is a JSON Schema library in JavaScript.
 By default, Ajv catches only the first validation failure.
 Advanced validation is covered in chapter 12.