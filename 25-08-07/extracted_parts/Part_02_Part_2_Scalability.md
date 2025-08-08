# Part 2—Scalability

## 메타데이터
- **Part 번호**: 2
- **페이지 범위**: 165-272
- **총 페이지 수**: 108
- **추출 시간**: 2025-08-07 11:25:42 KST

## 내용

## 페이지 165

Part 2
Scalability
T
heo feels a bit uncomfortable about the meeting with Joe. He was so enthusias-
tic about DOP, and he was very good at teaching it. Every meeting with him was an
opportunity to learn new things. Theo feels lot of gratitude for the time Joe spent
with him. He doesn’t want to hurt him in any fashion. Surprisingly, Joe enters the
office with the same relaxed attitude as usual, and he is even smiling.
Joe I’m really glad that you got the deal with Nancy.
Theo Yeah. There’s lot of excitement about it here in the office, and a bit of
stress too.
Joe What kind of stress?
Theo You know.... We need to hire a team of developers, and the deadlines
are quite tight.
Joe But you told me that you won’t use DOP. I assume that you gave regular
deadlines?
Theo No, my boss Monica really wanted to close the deal. She feels that success
with this project is strategically important for Albatross, so it’s worthwhile
to accept some risk by giving what she calls an “optimistic” time estima-
tion. I told her that it was really an unrealistic time estimation, but Mon-
ica insists that if we make smart decisions and bring in more developers,
we can do it.
Joe I see. Now I understand why you told me over the phone that you were
very busy. Anyway, would you please share the reasons that made you
think DOP wouldn’t be a good fit at scale?

## 페이지 166

138 PART 2 Scalability
Theo First of all, let me tell you that I feel lot of gratitude for all the teaching you
shared with me. Reimplementing the Klafim prototype with DOP was really
fun and productive due to the flexibility this paradigm offers.
Joe I’m happy that you found it valuable.
Theo But, as I told you over the phone, now we’re scaling up into a long-term project
with several developers working on a large code base. We came to the conclu-
sion that DOP will not be a good fit at scale.
Joe Could you share the reasons behind your conclusion?
Theo There are many of them. First of all, as DOP deals only with generic data struc-
tures, it’s hard to know what kind of data we have in hand, while in OOP, we
know the type of every piece of data. For the prototype, it was kind of OK. But
as the code base grows and more developers are involved in the project, it
would be too painful.
Joe I hear you. What else, my friend?
Theo Our system is going to run on a multi-threaded environment. I reviewed the
concurrency control strategy that you presented, and it’s not thread-safe.
Joe I hear you. What else, my friend?
Theo I have been doing a bit of research about implementing immutable data struc-
tures with structural sharing. I discovered that when the size of the data
structures grows, there is a significant performance hit.
Joe I hear you. What else?
Theo As our system grows, we will use a database to store the application data and
external services to enrich book information, and in what you have showed me
so far, data lives in memory.
Joe I hear you. What else, my friend?
Theo Don’t you think I have shared enough reasons to abandon DOP?
Joe I think that your concerns about DOP at scale totally make sense. However, it
doesn’t mean that you should abandon DOP.
Theo What do you mean?
Joe With the help of meditation, I learned not be attached to the objections that
flow in my mind while I’m practicing. Sometimes all that is needed to quiet our
minds is to keep breathing; sometimes, a deeper level of practice is needed.
Theo I don’t see how breathing would convince me to give DOP a second chance.
Joe Breathing might not be enough in this case, but a deeper knowledge of DOP
could be helpful. Until now, I have shared with you only the material that was
needed in order to refactor your prototype. In order to use DOP in a big proj-
ect, a few more lessons are necessary.
Theo But I don’t have time for more lessons. I need to work.
Joe Have you heard the story about the young woodcutter and the old man?
Theo No.
Joe It goes like this.

## 페이지 167

PART 2 Scalability 139
The young woodcutter and the old man
A young woodcutter strained to saw down a tree. An old man who was watching near-
by asked, “What are you doing?”
“Are you blind?” the woodcutter replied. “I’m cutting down this tree.”
The old man replied, “You look exhausted! Take a break. Sharpen your saw.”
The young woodcutter explained to the old man that he had been sawing for hours
and did not have time to take a break.
The old man pushed back, “If you sharpen the saw, you would cut down the tree much
faster.”
The woodcutter said, “I don’t have time to sharpen the saw. Don’t you see, I’m too
busy!”
Theo takes a moment to meditate on the story. He wonders if he needs to take the time to
sharpen his saw and commit to a deeper level of practice.
Theo Do you really think that with DOP, it will take much less time to deliver the
project?
Joe I know so!
Theo But if we miss the deadline, I will probably get fired. I’m the one that needs to
take the risk, not you.
Joe Let’s make a deal. If you miss the deadline and get fired, I will hire you at my
company for double the salary you make at Albatross.
Theo And what if we meet the deadline?
Joe If you meet the deadline, you will probably get promoted. In that case, I will
ask you to buy a gift for my son Neriah and my daughter Aurelia.
Theo Deal! When will I get my first lesson about going deeper into DOP?
Joe Why not start right now?
Theo Let me reschedule my meetings.

## 페이지 169

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

## 페이지 170

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

## 페이지 171

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

## 페이지 172

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

## 페이지 173

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

## 페이지 174

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

## 페이지 175

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

## 페이지 176

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

## 페이지 177

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

## 페이지 178

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

## 페이지 179

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

## 페이지 180

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

## 페이지 181

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

## 페이지 182

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

## 페이지 187

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

## 페이지 188

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

## 페이지 189

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

## 페이지 190

162 CHAPTER 7 Basic data validation
 It’s good practice to be strict regarding data that you send and to be flexible
regarding data that you receive.
 Ajv is a JSON Schema library in JavaScript.
 By default, Ajv catches only the first validation failure.
 Advanced validation is covered in chapter 12.

## 페이지 191

Advanced
concurrency control
No more deadlocks!
This chapter covers
 Atoms as an alternative to locks
 Managing a thread-safe counter and a thread-safe
in-memory cache with atoms
 Managing the whole system state in a thread-safe
way with atoms
The traditional way to manage concurrency in a multi-threaded environment
involves lock mechanisms like mutexes. Lock mechanisms tend to increase the com-
plexity of the system because it’s not trivial to make sure the system is free of dead-
locks. In DOP, we leverage the fact that data is immutable, and we use a lock-free
mechanism, called an atom, to manage concurrency. Atoms are simpler to manage
than locks because they are lock-free. As a consequence, the usual complexity of
locks that are required to avoid deadlocks don’t apply to atoms.
 NOTE This chapter is mostly relevant to multi-threaded environments like Java,
C#, Python, and Ruby. It is less relevant to single-threaded environments like Java-
Script. The JavaScript code snippets in this chapter are written as though JavaScript
were multi-threaded.
163

## 페이지 192

164 CHAPTER 8 Advanced concurrency control
8.1 The complexity of locks
This Sunday afternoon, while riding his bike across the Golden Gate Bridge, Theo thinks
about the Klafim project with concern, not yet sure that betting on DOP was a good
choice. Suddenly, Theo realizes that he hasn’t yet scheduled the next session with Joe. He
gets off his bike to call Joe. Bad luck, the line is busy.
When Theo gets home, he tries to call Joe again, but once again the phone is busy. After
dinner, Theo tries to call Joe one more time, with the same result—a busy signal. “Obvi-
ously, Joe is very busy today,” Theo tells himself. Exhausted by his 50-mile bike ride at an
average of 17 miles per hour, he falls asleep on the sofa. When Theo wakes up, he’s elated
to see a text message from Joe, “See you Monday morning at 11 AM?” Theo answers with a
thumbs up and prepares for another week of work.
When Joe arrives at the office, Theo asks him why his phone was constantly busy the day
before. Joe answers that he was about to ask Theo the same question. They look at each
other, puzzled, and then simultaneously break into laughter as they realize what hap-
pened: in an amazing coincidence, they’d tried to phone each other at exactly the same
times. They both say at once:
“A deadlock!”
They both head for Theo’s office. When they get to Theo’s desk, Joe tells him that today’s
session is going to be about concurrency management in multi-threaded environments.
Joe How do you usually manage concurrency in a multi-threaded environment?
Theo I protect access to critical sections with a lock mechanism, a mutex, for instance.
Joe When you say access, do you mean write access or also read access?
Theo Both!
Joe Why do you need to protect read access with a lock?
Theo Because, without a lock protection, in the middle of a read, a write could hap-
pen in another thread. It would make my read logically inconsistent.
Joe Another option would be to clone the data before processing it in a read.
Theo Sometimes I would clone the data; but in many cases, when it’s large, it’s too
expensive to clone.
TIP Cloning data to avoid read locks doesn’t scale.
Joe In DOP, we don’t need to clone or to protect read access.
Theo Because data is immutable?
Joe Right. When data is immutable, even if a write happens in another thread
during a read, it won’t make the read inconsistent because the write never
mutates the data that is read.
Theo In a sense, a read always works on a data snapshot.
Joe Exactly!
TIP When data is immutable, a read is always safe.
Theo But what about write access? Don’t you need to protect that with locks?
Joe Nope.

## 페이지 193

8.2 Thread-safe counter with atoms 165
Theo Why not?
Joe We have a simpler mechanism—it’s called an atom.
Theo I am glad to hear there is a something simpler than locks. I really struggle each
time I have to integrate locks into a multi-threaded system.
Joe Me too! I remember a bug we had in production 10 years ago. We forgot to
release a lock when an exception was thrown in a critical section. It caused a
terrible deadlock.
Theo Deadlocks are really hard to avoid. Last year, we had a deadlock issue when two
locks were not released in the proper order.
Joe I have great news for you. With atoms, deadlocks never happen!
TIP With atoms, deadlocks never happen.
Theo That sounds great. Tell me more!
TIP Atoms provide a way to manage concurrency without locks.
8.2 Thread-safe counter with atoms
Joe Let’s start with a simple case: a counter shared between threads.
Theo What do you mean by a counter?
Joe Imagine that we’d like to count the number of database accesses and write the
total number of accesses to a log every minute.
Theo OK.
Joe Could you write JavaScript code for this multi-threaded counter using locks?
Theo But JavaScript is single-threaded!
Joe I know, but it’s just for the sake of illustration. Imagine that JavaScript were
multi-threaded and that it provided a Mutex object that you could lock and
unlock.
Theo It’s a bit awkward. I guess it would look like this.
Theo goes to the whiteboard. He writes what he imagines to be JavaScript code for a multi-
threaded counter with locks.
Listing8.1 A thread-safe counter protected by a mutex
var mutex = new Mutex();
var counter = 0;
function dbAccess() {
mutex.lock();
counter = counter + 1;
mutex.unlock();
// access the database
}
function logCounter() {
mutex.lock();

## 페이지 194

166 CHAPTER 8 Advanced concurrency control
console.log('Number of database accesses: ' + counter);
mutex.unlock();
}
Joe Excellent. Now, I am going to show you how to write the same code with atoms.
An atom provides three methods:
 get returns the current value of the atom.
 set overwrites the current value of the atom.
 swap receives a function and updates the value of the atom with the result
of the function called on the current value of the atom.
Joe unzips a pocket in his laptop case and takes out a piece of paper. He hands it to
Theo. Theo is pleasantly surprised as the sheet of paper succinctly describes the methods
(table 8.1).
Table 8.1 The three methods of an atom
Method Description
get Returns the current value
set Overwrites the current value
swap Updates the current value with a function
Theo How would it look like to implement a thread-safe counter with an atom?
Joe It’s quite simple, actually.
Joe pulls out his laptop, fires it up, and begins to type. When he’s done, he turns the laptop
around so that Theo can see the code to implement a thread-safe counter in an atom.
Listing8.2 A thread-safe counter stored in an atom
var counter = new Atom();
counter.set(0);
function dbAccess() {
counter.swap(function(x) {
The argument x is the
return x + 1;
current value of the atom,
});
same as counter.get().
// access the database
}
function logCounter() {
console.log('Number of database accesses: ' + counter.get());
}
Theo Could you tell me what’s going on here?
Joe Sure! First, we create an empty atom. Then, we initialize the value of the atom
with counter.set(0). In the logger thread, we read the current value of the
atom with counter.get().
Theo And how do you increment the counter in the threads that access the database?

## 페이지 195

8.2 Thread-safe counter with atoms 167
Joe We call swap with a function that receives x and returns x + 1.
Theo I don’t understand how swap could be thread-safe without using any locks.
Joe quickly goes to the whiteboard. He sketches the diagram in figure 8.1.
Take snapshot
Compute next state
Yes
State changed?
No
Update state
Figure 8.1 High-level flow of swap
Joe You see, swap computes the next value of the atom, and before modifying the
current value of the atom, it checks whether the value of the atom has changed
during the computation. If so, swap tries again, until no changes occur during
the computation.
Theo Is swap easy to implement?
Joe Let me show you the implementation of the Atom class and you’ll see.
Listing8.3 Implementation of the Atom class
class Atom {
state;
constructor() {}
get() {
return this.state;
}
set(state) {
this.state = state;
}
swap(f) {
while(true) {
var stateSnapshot = this.state;
var nextState = f(stateSnapshot);
if (!atomicCompareAndSet(this.state,

## 페이지 196

168 CHAPTER 8 Advanced concurrency control
stateSnapshot,
nextState)) {
Uses a special thread-safe comparison operation
continue;
as this.state might have changed in another
}
thread during execution of the function f.
return nextState;
}
}
}
Theo comes closer to the whiteboard. He modifies Joe’s diagram a bit to make the flow of
the swap operation more detailed. The resulting diagram is in figure 8.2. Theo still has a
few questions, though.
Take snapshot
snapshot = state
Compute next state
nextState = f(snapshot)
Check if state has changed
state == snapshot
Yes
State changed?
No
Update state
state = nextState
Figure 8.2 Detailed flow of swap
Theo What is atomicCompareAndSet?
Joe It’s the core operation of an atom. atomicCompareAndSet atomically sets the
state to a new value if, and only if, the state equals the provided old value. It
returns true upon success and false upon failure.
Theo How could it be atomic without using locks?
Joe That’s a great question! In fact, atomicCompareAndSet is a compare-and-swap
operation, provided by the language that relies on a functionality of the CPU
itself. For example, in Java the java.util.concurrent.atomic package has
an AtomicReference generic class that provides a compareAndSet() method.
 NOTE See http://tutorials.jenkov.com/java-concurrency/compare-and-swap.html
for general information about compare-and-swap operations. Implementations for
multi-threaded languages appear in table 8.2.

## 페이지 197

8.2 Thread-safe counter with atoms 169
Table 8.2 Implementation of an atomic compare and set in various languages
Language Link
Java http://mng.bz/mx0W
JavaScript Not relevant (single-threaded language)
Ruby http://mng.bz/5KG8
Python https://github.com/maxcountryman/atomos
C# http://mng.bz/6Zzp
Theo Apropos Java, how would the implementation of an atom look?
Joe It’s quite the same, besides the fact that Atom has to use generics, and the inner
state has to be stored in an AtomicReference.
Joe brings up a Java implementation of Atom on his laptop. Theo looks over the code.
Listing8.4 Implementation of the Atom class in Java
class Atom<ValueType> {
private AtomicReference<ValueType> state;
public Atom() {}
ValueType get() {
return this.state.get();
}
this.state might have
changed in another thread
void set(ValueType state) {
during the execution of f.
this.state.set(state);
}
ValueType swap(UnaryOPerator<ValueType> f) {
while(true) {
ValueType stateSnapshot = this.state.get();
ValueType nextState = f(stateSnapshot);
if (!this.state.compareAndSet(stateSnapshot,
nextState)) {
continue;
}
}
return nextState;
}
}
Theo What about using an atom in Java?
Joe Here, take a look. It’s quite simple.

## 페이지 198

170 CHAPTER 8 Advanced concurrency control
Listing8.5 Using an Atom in Java
Atom<Integer> counter = new Atom<Integer>();
counter.set(0);
counter.swap(x -> x + 1);
counter.get();
Theo takes a couple of minutes to meditate about this atom stuff and to digest what he’s
just learned. Then, he asks Joe:
Theo What if swap never succeeds? I mean, could the while loop inside the code of
swap turn out to be an infinite loop?
Joe No! By definition, when atomicCompareAndSet fails on a thread, it means that
the same atom was changed on another thread during the execution of swap.
In this race between threads, there is always a winner.
Theo But isn’t it possible that some thread never succeeds because it always loses the
race against other threads?
Joe In theory, yes, but I’ve never encountered such a situation. If you have thou-
sands of threads that do nothing besides swapping an atom, it could happen I
suppose. But, in practice, once the atom is swapped, the threads do some real
work, for example, database access or I/O. This gives other threads the oppor-
tunity to swap the atom successfully.
 NOTE In theory, atoms could create starvation in a system with thousands of threads
that do nothing beside swapping an atom. In practice, once an atom is swapped, the
threads do some real work (e.g., database access), which creates an opportunity for
other threads to swap the atom successfully.
Theo Interesting.... Indeed, atoms look much easier to manage than locks.
Joe Now let me show you how to use atoms with composite data.
Theo Why would that be different?
Joe Usually, dealing with composite data is more difficult than dealing with primi-
tive types.
Theo When you sold me on DOP, you told me that we are able to manage data with
the same simplicity as we manage numbers.
TIP In DOP, data is managed with the same simplicity as numbers.
Joe That’s exactly what I am about to show you.
8.3 Thread-safe cache with atoms
Joe Are you familiar with the notion of in-memory cache?
Theo You mean memoization?

## 페이지 199

8.3 Thread-safe cache with atoms 171
Joe Kind of. Imagine that database queries don’t vary too much in your applica-
tion. It makes sense in that case to store the results of previous queries in mem-
ory in order to improve the response time.
Theo Yes, of course!
Joe What data structure would you use to store the in-memory cache?
Theo Probably a string map, where the keys are the queries, and the values are the
results from the database.
TIP It’s quite common to represent an in-memory cache as a string map.
Joe Excellent! Now can you write the code to cache database queries in a thread-
safe way using a lock?
Theo Let me see: I’m going to use an immutable string map. Therefore, I don’t
need to protect read access with a lock. Only the cache update needs to be
protected.
Joe You’re getting the hang of this!
Theo The code should be something like this.
Listing8.6 Thread-safe cache with locks
var mutex = new Mutex();
var cache = {};
function dbAccessCached(query) {
var resultFromCache = _.get(cache, query);
if (resultFromCache != nil) {
return resultFromCache;
}
var result = dbAccess(query);
mutex.lock();
cache = _.set(cache, query, result);
mutex.unlock();
return result;
}
Joe Nice! Now, let me show you how to write the same code using an atom instead
of a lock. Take a look at this code and let me know if it’s clear to you.
Listing8.7 Thread-safe cache with atoms
var cache = new Atom();
cache.set({});
function dbAccessCached(query) {
var resultFromCache = _.get(cache.get(), query);
if (resultFromCache != nil) {
return resultFromCache;
}
var result = dbAccess(query);
cache.swap(function(oldCache) {

## 페이지 200

172 CHAPTER 8 Advanced concurrency control
return _.set(oldCache, query, result);
});
return result;
}
Theo I don’t understand the function you’re passing to the swap method.
Joe The function passed to swap receives the current value of the cache, which is a
string map, and returns a new version of the string map with an additional key-
value pair.
Theo I see. But something bothers me with the performance of the swap method in
the case of a string map. How does the comparison work? I mean, comparing
two string maps might take some time.
Joe Not if you compare them by reference. As we discussed in the past, when data
is immutable, it is safe to compare by reference, and it’s super fast.
TIP When data is immutable, it is safe (and fast) to compare it by reference.
Theo Cool. So atoms play well with immutable data.
Joe Exactly!
8.4 State management with atoms
Joe Do you remember a couple of weeks ago when I showed you how we resolve
potential conflicts between mutations? You told me that the code was not
thread-safe.
Theo Let me look again at the code.
Theo takes a look at the code for the SystemData class that he wrote some time ago
(repeated in listing 8.8). Without the validation logic, it makes the code easier to grasp.
Listing8.8 SystemData class from part 1
class SystemState {
systemData;
get() {
return this.systemData;
}
set(_systemData) {
this.systemData = _systemData;
}
commit(previous, next) {
this.systemData = SystemConsistency.reconcile(this.systemData,
previous,
next);
}
}

## 페이지 201

8.4 State management with atoms 173
It takes him a few minutes to remember how the commit method works. Suddenly, he has
an Aha! moment.
Theo This code is not thread-safe because the SystemConsistency.reconcile
code inside the commit method is not protected. Nothing prevents the two
threads from executing this code concurrently.
Joe Right! Now, can you tell me how to make it thread-safe?
Theo With locks?
Joe Come on...
Theo I was kidding, of course. We make the code thread-safe not with a lock but with
an atom.
Joe Nice joke!
Theo Let me see. I’d need to store the system data inside an atom. The get and set
method of SystemData would simply call the get and set methods of the
atom. How does this look?
Listing8.9 SystemData class with atom (without the commit method)
class SystemState {
systemData;
constructor() {
this.systemData = new Atom();
}
get() {
return this.systemData.get();
}
commit(prev, next) {
this.systemData.set(next);
}
}
Joe Excellent. Now for the fun part. Implement the commit method by calling the
swap method of the atom.
Theo Instead of calling SystemConsistency.reconcile() directly, I need to wrap
it into a call to swap. So, something like this?
Listing8.10 Implementation of SystemData.commit with atom
SystemData.commit = function(previous, next) {
this.systemData.swap(function(current) {
return SystemConsistency.reconcile(current,
previous,
next);
});
};

## 페이지 202

174 CHAPTER 8 Advanced concurrency control
Joe Perfect.
Theo This atom stuff makes me think about what happened to us yesterday, when we
tried to call each other at the exact same time.
Joe What do you mean?
Theo I don’t know, but I am under the impression that mutexes are like phone calls,
and atoms are like text messages.
Joe smiles at Theo but doesn’t reveal the meaning of his smile. After the phone deadlock
yesterday, Theo’s pretty sure that he and Joe are on the same page.
Summary
 Managing concurrency with atoms is much simpler than managing concur-
rency with locks because we don’t have to deal with the risk of deadlocks.
 Cloning data to avoid read locks doesn’t scale.
 When data is immutable, reads are always safe.
 Atoms provide a way to manage concurrency without locks.
 With atoms, deadlocks never happen.
 Using atoms for a thread-safe counter is trivial because the state of the counter
is represented with a primitive type (an integer).
 We can manage composite data in a thread-safe way with atoms.
 We make the highly scalable state management approach from part 1 thread-
safe by keeping the whole system state inside an atom.
 It’s quite common to represent an in-memory cache as a string map.
 When data is immutable, it is safe (and fast) to compare by reference.
 In theory, atoms could create starvation in a system with thousands of threads
that do nothing besides swapping an atom.
 In practice, once an atom is swapped, the threads do some real work (e.g.,
database access) to provide an opportunity for other threads to swap the atom
successfully.

## 페이지 203

Persistent data structures
Standing on the shoulders of giants
This chapter covers
 The internal details of persistent data
structures
 The time and memory efficiency of persistent
data structures
 Using persistent data structures in an
application
In part 1, we illustrated how to manage the state of a system without mutating data,
where immutability is maintained by constraining ourselves to manipulate the state
only with immutable functions using structural sharing. In this chapter, we present
a safer and more scalable way to preserve data immutability—representing data
with so-called persistent data structures. Efficient implementations of persistent
data structures exist for most programming languages via third-party libraries.
9.1 The need for persistent data structures
It’s at the university where Theo meets Joe this time. When Theo asks Joe if today’s topic
is academic in nature, Joe tells him that the use of persistent data structures only
became possible in programming languages following a discovery in 2001 by a computer
175

## 페이지 204

176 CHAPTER 9 Persistent data structures
researcher named Phil Bagwell.1 In 2007, Rich Hickey, the creator of Clojure, used this dis-
covery as the foundation of persistent data structures in Clojure. Unveiling the secrets of
these data structures to Theo in a university classroom is a way for Joe to honor the mem-
ory of Phil Bagwell, who unfortunately passed away in 2012. When they get to the univer-
sity classroom, Joe starts the conversation with a question.
Joe Are you getting used to DOP’s prohibition against mutating data in place and
creating new versions instead?
Theo I think so, but two things bother me about the idea of structural sharing that
you showed me.
Joe What bothers you, my friend?
Theo Safety and performance.
Joe What do you mean by safety?
Theo I mean that using immutable functions to manipulate data doesn’t prevent it
from being modified accidentally.
Joe Right! Would you like me to show you the naive way to handle immutability or
the real way?
Theo What are the pros and cons of each way?
Joe The naive way is easy but not efficient, although the real way is efficient but
not easy.
Theo Let’s start with the naive way then.
Joe Each programming language provides its own way to protect data from being
mutated.
Theo How would I do that in Java, for instance?
Joe Java provides immutable collections, and there is a way to convert a list or a
map to an immutable list or an immutable map.
 NOTE Immutable collections are not the same as persistent data structures.
Joe opens his laptop and fires it up. He brings up two code examples, one for immutable
lists and one for immutable maps.
Listing9.1 Converting a mutable list to an immutable list in Java
var myList = new ArrayList<Integer>();
myList.add(1);
myList.add(2);
myList.add(3);
var myImmutableList = List.of(myList.toArray());
1 P. Bagwell, “Ideal hash trees” (No. REP_WORK), 2001. [Online]. Available: https://lampwww.epfl.ch/papers/
idealhashtrees.pdf.

## 페이지 205

9.1 The need for persistent data structures 177
Listing9.2 Converting a mutable map to an immutable map in Java
var myMap = new HashMap<String, Object>();
myMap.put("name", "Isaac");
myMap.put("age", 42);
var myImmutableMap = Collections.unmodifiableMap(myMap);
Theo What happens when you try to modify an immutable collection?
Joe Java throws an UnsupportedOperationException.
Theo And in JavaScript?
Joe JavaScript provides an Object.freeze() function that prevents data from
being mutated. It works both with JavaScript arrays and objects.
Joe takes a minute to scroll through his laptop. When he finds what he’s looking for, he
shows Theo the code.
Listing9.3 Making an object immutable in JavaScript
var a = [1, 2, 3];
Object.freeze(a);
var b = {foo: 1};
Object.freeze(b);
Theo What happens when you try to modify a frozen object?
Joe It depends. In JavaScript strict mode, a TypeError exception is thrown, and in
nonstrict mode, it fails silently.
 NOTE JavaScript’s strict mode is a way to opt in to a restricted variant of JavaScript
that changes some silent errors to throw errors.
Theo In case of a nested collection, are the nested collections also frozen?
Joe No, but in JavaScript, one can write a deepFreeze() function that freezes an
object recursively. Here’s another example.
Listing9.4 Freezing an object recursively in JavaScript
function deepFreeze(object) {
// Retrieve the property names defined on object
const propNames = Object.getOwnPropertyNames(object);
// Freeze properties before freezing self
for (const name of propNames) {
const value = object[name];
if (value && typeof value === "object") {
deepFreeze(value);
}
}

## 페이지 206

178 CHAPTER 9 Persistent data structures
return Object.freeze(object);
}
Theo I see that it’s possible to ensure that data is never mutated, which answers my
concerns about safety. Now, let me share my concerns about performance.
TIP It’s possible to manually ensure that our data isn’t mutated, but it’s cumbersome.
Joe Sure.
Theo If I understand correctly, the main idea behind structural sharing is that most
data is usually shared between two versions.
Joe Correct.
Theo This insight allows us to create new versions of our collections using a shallow
copy instead of a deep copy, and you claimed that it was efficient.
Joe Exactly!
Theo Now, here is my concern. In the case of a collection with many entries, a shal-
low copy might be expensive.
Joe Could you give me an example of a collection with many entries?
Theo A catalog with 100,000 books, for instance.
Joe On my machine, making a shallow copy of a collection with 100,000 entries
doesn’t take more than 50 milliseconds.
Theo Sometimes, even 50 milliseconds per update isn’t acceptable.
Joe I totally agree with you. When one needs data immutability at scale, naive struc-
tural sharing is not appropriate.
Theo Also, shallow copying an array of 100,000 elements on each update would
increase the program memory by 100 KB.
Joe Indeed, at scale, we have a problem both with memory and computation.
TIP At scale, naive structural sharing causes a performance hit, both in terms of
memory and computation.
Theo Is there a better solution?
Joe Yes! For that, you’ll need to learn the real way to handle immutability. It’s
called persistent data structures.
9.2 The efficiency of persistent data structures
Theo In what sense are those data structures persistent?
Joe Persistent data structures are so named because they always preserve their pre-
vious versions.
TIP Persistent data structures always preserve the previous version of themselves
when they are modified.
Joe Persistent data structures address the two main limitations of naive structural
sharing: safety and performance.

## 페이지 207

9.2 The efficiency of persistent data structures 179
Theo Let’s start with safety. How do persistent data structures prevent data from
being mutated accidentally?
Joe In a language like Java, they implement the mutation methods of the collec-
tion interfaces by throwing the run-time exception UnsupportedOperation-
Exception.
Theo And, in a language like JavaScript?
Joe In JavaScript, persistent data structures provide their own methods to access
data, and none of those methods mutate data.
Theo Does that mean that we can’t use the dot notation to access fields?
Joe Correct. Fields of persistent data structures are accessed via a specific API.
Theo What about efficiency? How do persistent data structures make it possible to
create a new version of a huge collection in an efficient way?
Joe Persistent data structures organize data in such a way that we can use structural
sharing at the level of the data structure.
Theo Could you explain?
Joe Certainly. Let’s start with the simplest data structure: a linked list. Imagine that
you have a linked list with 100,000 elements.
Theo OK.
Joe What would it take to prepend an element to the head of the list?
Theo You mean to create a new version of the list with an additional element?
Joe Exactly!
Theo Well, we could copy the list and then prepend an element to the list, but it
would be quite expensive.
Joe What if I tell you that the original linked list is guaranteed to be immutable?
Theo In that case, I could create a new list with a new head that points to the head of
the original list.
Theo goes to the classroom blackboard. He picks up a piece of chalk and draws the dia-
gram shown in figure 9.1.
New list Original list
Figure 9.1 Structural sharing
0 1 2 3 4 5 with linked lists
Joe Would the efficiency of this operation depend on the size of the list?
Theo No, it would be efficient, no matter the size of the list.
Joe That’s what I mean by structural sharing at the level of the data structure itself.
It relies on a simple but powerful insight—when data is immutable, it is safe to
share it.
TIP When data is immutable, it is safe to share it.

## 페이지 208

180 CHAPTER 9 Persistent data structures
Theo I understand how to use structural sharing at the level of the data structure for
linked lists and prepend operations, but how would it work with operations
like appending or modifying an element in a list?
Joe For that purpose, we need to be smarter and represent our list as a tree.
Theo How does that help?
Joe It helps because when a list is represented as a tree, most of the nodes in the
tree can be shared between two versions of the list.
Theo I am totally confused.
Joe Imagine that you take a list with 100,000 elements and split it into two lists of
50,000 elements each: elements 0 to 49,999 in list 1, and elements 50,000 to
99,999 in list 2. How many operations would you need to create a new version
of the list where a single element—let’s say, element at index 75,100—is
modified?
It’s hard for Theo to visualize this kind of stuff mentally. He goes back to the blackboard
and draws a diagram (see figure 9.2). Once Theo looks at the diagram, it’s easy for him to
answer Joe’s question.
List «Next»
List
List 1 List 2
«Next»
0...49,999 50,000...99,999
List 2
Figure 9.2 Structural sharing when
50,000...99,999
a list of 100,000 elements is split
Theo List 1 could be shared with one operation. I’d need to create a new version of
list 2, where element 75,100 is modified. It would take 50,000 operations, so it’s
one operation of sharing and one operation of copying 50,000 elements. Over-
all, it’s 50,001 operations.
Joe Correct. You see that by splitting our original list into two lists, we can create a
new version of the list with a number of operations in the order of the size of
the list divided by 2.
Theo I agree, but 50,000 is still a big number.
Joe Indeed, but nobody prevents us from applying the same trick again, splitting
list 1 and list 2 in two lists each.
Theo How exactly?
Joe We can make list 1.1 with elements 0 to 24,999, then list 1.2 with elements
25,000 to 49,999, list 2.1 with elements 50,000 to 74,999, and list 2.2 with ele-
ments 75,000 to 99,999.
Theo Can you draw that on the blackboard?
Joe Sure.

## 페이지 209

9.2 The efficiency of persistent data structures 181
Now, it’s Joe that goes to the blackboard. He draws the diagram in figure 9.3.
«Next»
List
List
«Next»
List 1 List 2 List 2
List 1.1 List 1.2 List 2.1 List 2.2 «Next»
0...24,499 25,000...49,999 50,000...74,999 75,000...99,999 List 2.2
75,000...99,999
Figure 9.3 Structural sharing when a list of 100,000 elements is split twice
Theo Let me count the number of operations for updating a single element. It takes
2 operations of sharing and 1 operation of copying 25,000 elements. Overall, it
takes 25,002 operations to create a new version of the list.
Joe Correct!
Theo Let’s split the list again then!
Joe Absolutely. In fact, we can split the list again and again until the size of the
lists is at most 2. Can you guess what is the complexity of creating a new ver-
sion then?
Theo I’d say around log2 N operations.
Joe I see that you remember well your material from school. Do you have a gut
feeling about what is log2 N when N is 100,000?
Theo Let me see...2 to the power of 10 is around 1,000, and 2 to the power of 7 is
128. So, it should be a bit less than 17.
Joe It’s 16.6 to be precise. It means that in order to update an element in a per-
sistent list of 100,000 elements, we need around 17 operations. The same goes
for accessing elements.
Theo Nice, but 17 is still not negligible.
Joe I agree. We can easily improve the performance of accessing elements by using
a higher branching factor in our tree.
Theo What do you mean?
Joe Instead of splitting by 2 at each level, we could split by 32.
Theo But the running time of our algorithm would still grow with log N.
Joe You’re right. From a theoretical perspective, it’s the same. From a practical
perspective, however, it makes a big difference.
Theo Why?
Joe Because log32 N is 5 times lower than log2 N.

## 페이지 210

182 CHAPTER 9 Persistent data structures
Theo That’s true: 2 to the power of 5 is 32.
Joe Back to our list of 100,000 elements, can you tell me how many operations are
required to access an element if the branching factor is 32?
Theo With a branching factor of 2, it was 16.6. If I divide 16.6 by 5, I get 3.3.
Joe Correct!
TIP By using a branching factor of 32, we make elements accessed in persistent lists
more efficient.
Theo Does this trick also improve the performance of updating an element in a list?
Joe Yes, indeed, it does.
Theo How? We’d have to copy 32 elements at each level instead of 2 elements. It’s a
16× performance hit that’s not compensated for by the fact that the tree depth
is reduced by 5×!
Joe I see that you are quite sharp with numbers. There is another thing to take
into consideration in our practical analysis of the performance: modern CPU
architecture.
Theo Interesting. The more you tell me about persistent data structures, the more I
understand why you wanted to have this session at a university: it’s because
we’re dealing with all this academic stuff.
Joe Yep. So, to continue, modern CPUs read and write data from and to the main
memory in units of cache lines, often 32 or 64 bytes long.
Theo What difference does that make?
Joe A nice consequence of this data access pattern is that copying an array of size
32 is much faster than copying 16 arrays of size 2 that belong to different levels
of the tree.
Theo Why is that?
Joe The reason is that copying an array of size 32 can be done in a single pair of
cache accesses: one for read and one for write. Although for arrays that belong
to different tree levels, each array requires its own pair of cache accesses, even
if there are only 2 elements in the array.
Theo In other words, the performance of updating a persistent list is dominated by
the depth of the tree.
TIP In modern CPU architectures, the performance of updating a persistent list is
dominated much more by the depth of the tree than by the number of nodes at each
level of the tree.
Joe That’s correct, up to a certain point. With today’s CPUs, using a branching fac-
tor of 64 would, in fact, decrease the performance of update operations.
Theo I see.
Joe Now, I am going to make another interesting claim that is not accurate from a
theoretical perspective but accurate in practice.
Theo What is it?

## 페이지 211

9.2 The efficiency of persistent data structures 183
Joe The number of operations it takes to get or update an element in a persistent
list with branching factor 32 is constant.
Theo How can that be? You just made the point that the number of operations is
log32 N.
Joe Be patient, my friend. What is the highest number of elements that you can
have in a list, in practice?
Theo I don’t know. I never thought about that.
Joe Let’s assume that it takes 4 bytes to store an element in a list.
Theo OK.
Joe Now, can you tell me how much memory it would take to hold a list with 10 bil-
lion elements?
Theo You mean 1 with 10 zeros?
Joe Yes.
Theo Each element take 4 bytes, so it would be around 40 GB!
Joe Correct. Do you agree that it doesn’t make sense to hold a list that takes 40 GB
of memory?
Theo I agree.
Joe So let’s take 10 billion as an upper bound to the number of elements in a list.
What is log32 of 10 billion?
Once again, Theo uses the blackboard to clarify his thoughts. With that, he quickly finds
the answer.
Theo 1 billion is approximately 2^30. Therefore, 10 billion is around 2^33. That
means that log2 of 10 billion is 33, so log32 of 10 billion should be around
33/5, which is a bit less than 7.
Joe I am impressed again by your sharpness with numbers. To be precise, log32 of
10 billion is 6.64.
Theo (smiling) I didn’t get that far.
Joe Did I convince you that, in practice, accessing or updating an element in a per-
sistent list is essentially constant?
Theo Yes, and I find it quite amazing!
TIP Persistent lists can be manipulated in near constant time.
Joe Me too.
Theo What about persistent maps?
Joe It’s quite similar, but I don’t think we have time to discuss it now.
Startled, Theo looks at his watch. This morning’s session has gone by so quickly. He notices
that it’s time to get back to the office and have lunch.

## 페이지 212

184 CHAPTER 9 Persistent data structures
9.3 Persistent data structures libraries
On their way back to the office, Theo and Joe don’t talk too much. Theo’s thoughts take
him back to what he learned in the university classroom. He feels a lot of respect for Phil
Bagwell, who discovered how to manipulate persistent data structures efficiently, and for
Rich Hickey, who created a programming language incorporating that discovery as a core
feature and making it available to the world. Immediately after lunch, Theo asks Joe to
show him what it looks like to manipulate persistent data structures for real in a program-
ming language.
Theo Are persistent data structures available in all programming languages?
Joe A few programming languages like Clojure, Scala, and C# provide them as part
of the language. In most programming languages, though, you need a third-
party library.
Theo Could you give me a few references?
Joe Sure.
Using Theo’s laptop, Joe bookmarks some sites. He knows exactly which URLs to look for.
Then, while Theo is looking over the bookmarked sites, Joe goes to the whiteboard and
jots down the specific libraries in table 9.1.
 Immutable.js for JavaScript at https://immutable-js.com/
 Paguro for Java at https://github.com/GlenKPeterson/Paguro
 Immutable Collections for C# at http://mng.bz/QW51
 Pyrsistent for Python at https://github.com/tobgu/pyrsistent
 Hamster for Ruby at https://github.com/hamstergem/hamster
Table 9.1 Persistent data structure libraries
Language Library
JavaScript Immutable.js
Java Paguro
C# Provided by the language
Python Pyrsistent
Ruby Hamster
Theo What does it take to integrate persistent data structures provided by a third-
party library into your code?
9.3.1 Persistent data structures in Java
Joe In an object-oriented language like Java, it’s quite straightforward to integrate
persistent data structures in a program because persistent data structures
implement collection interfaces, besides the parts of the interface that mutate
in place.
Theo What do you mean?

## 페이지 213

9.3 Persistent data structures libraries 185
Joe Take for instance, Paguro for Java. Paguro persistent maps implement the
read-only methods of java.util.Map like get() and containsKey(), but not
methods like put() and remove(). On the other hand, Paguro vectors imple-
ment the read-only methods of java.util.List like get() and size(), but not
methods like set().
Theo What happens when we call put() or remove() on a Paguro map?
Joe It throws an UnSupportedOperationException exception.
Theo What about iterating over the elements of a Paguro collection with a forEach()?
Joe That works like it would in any Java collection. Here, let me show you an example.
Listing9.5 Iterating over a Paguro vector
var myVec = PersistentVector.ofIter(
List.of(10, 2, 3));
Creates a Paguro
vector from a
for (Integer i : myVec) {
Java list
System.out.println(i);
}
Theo What about Java streams?
Joe Paguro collections are Java collections, so they support the Java stream inter-
face. Take a look at this code.
Listing9.6 Streaming a Paguro vector
var myVec = PersistentVector.ofIter(List.of(10, 2, 3));
vec1.stream().sorted().map(x -> x + 1);
TIP Paguro collections implement the read-only parts of Java collection interfaces.
Therefore, they can be passed to any methods that expect to receive a Java collection
without mutating it.
Theo So far, you told me how do use Paguro collections as Java read-only collections.
How do I make modifications to Paguro persistent data structures?
Joe In a way similar to the _.set() function of Lodash FP that we talked about
earlier. Instead of mutating in place, you create a new version.
Theo What methods does Paguro expose for creating new versions of a data structure?
Joe For vectors, you use replace(), and for maps, you use assoc().
Listing9.7 Creating a modified version of a Paguro vector
var myVec = PersistentVector.ofIter(List.of(10, 2, 3));
var myNextVec = myVec.replace(0, 42);

## 페이지 214

186 CHAPTER 9 Persistent data structures
Listing9.8 Creating a modified version of a Paguro map
var myMap = PersistentHashMap.of(Map.of("aa", 1, "bb", 2)
.entrySet());
Creates a Paguro map
from a Java map entry set
var myNextMap = myMap.assoc("aa", 42);
Theo Yes! Now I see how to use persistent data structures in Java, but what about
JavaScript?
9.3.2 Persistent data structures in JavaScript
Joe In a language like JavaScript, it’s a bit more cumbersome to integrate per-
sistent data structures.
Theo How so?
Joe Because JavaScript objects and arrays don’t expose any interface.
Theo Bummer.
Joe It’s not as terrible as it sounds because Immutable.js exposes its own set of
functions to manipulate its data structures.
Theo What do you mean?
Joe I’ll show you in a moment. But first, let me show you how to initiate Immutable.js
persistent data structures.
Theo OK!
Joe Immutable.js provides a handy function that recursively converts a native data
object to an immutable one. It’s called Immutable.fromJS().
Theo What do you mean by recursively?
Joe Consider the map that holds library data from our Library Management Sys-
tem: it has values that are themselves maps. Immutable.fromJS() converts the
nested maps into immutable maps.
Theo Could you show me some code?
Joe Absolutely. Take a look at this JavaScript code for library data.
Listing9.9 Conversion to immutable data
var libraryData = Immutable.fromJS({
"catalog": {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore",
"dave-gibbons"]
}
},
"authorsById": {
"alan-moore": {
"name": "Alan Moore",

## 페이지 215

9.3 Persistent data structures libraries 187
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
}
});
Theo Do you mean that the catalog value in libraryData map is itself an immutable
map?
Joe Yes, and the same for booksByIsbn, authorIds, and so forth.
Theo Cool! So how do I access a field inside an immutable map?
Joe As I told you, Immutable.js provides its own API for data access. For instance,
in order to access a field inside an immutable map, you use Immutable.get()
or Immutable.getIn() like the following.
Listing9.10 Accessing a field and a nested field in an immutable map
Immutable.get(libraryData, "catalog");
Immutable.getIn(libraryData,
["catalog", "booksByIsbn", "978-1779501127", "title"]);
// → "Watchmen"
Theo How do I make a modification to a map?
Joe Similar to what we did with Lodash FP, you use an Immutable.set() or
Immutable.setIn() map to create a new version of the map where a field is
modified. Here’s how.
Listing9.11 Creating a new version of a map where a field is modified
Immutable.setIn(libraryData,
["catalog", "booksByIsbn",
"978-1779501127", "publicationYear"],
1988);
Theo What happens when I try to access a field in the map using JavaScript’s dot or
bracket notation?
Joe You access the internal representation of the map instead of accessing a map
field.
Theo Does that mean that we can’t pass data from Immutable.js to Lodash for data
manipulation?
Joe Yes, but it’s quite easy to convert any immutable collection into a native Java-
Script object back and forth.
Theo How?
Joe Immutable.js provides a toJS() method to convert an arbitrary deeply nested
immutable collection into a JavaScript object.

## 페이지 216

188 CHAPTER 9 Persistent data structures
Theo But if I have a huge collection, it could take lots of time to convert it, right?
Joe True. We need a better solution. Hopefully, Immutable.js provides its own set
of data manipulation functions like map(), filter(), and reduce().
Theo What if I need more data manipulation like Lodash’s _.groupBy()?
Joe You could write your own data manipulation functions that work with the
Immutable.js collections or use a library like mudash, which provides a port of
Lodash to Immutable.js.
 NOTE You can access the mudash library at https://github.com/brianneisler/mudash.
Theo What would you advise?
Joe A cup of coffee, then I’ll show you how to port functions from Lodash to
Immutable.js and how to adapt the code from your Library Management System.
You can decide on whichever approach works best for your current project.
9.4 Persistent data structures in action
Joe Let’s start with our search query. Can you look at the current code and tell me
the Lodash functions that we used to implement the search query?
Theo Including the code for the unit tests?
Joe Of course!
 NOTE See chapter 6 for the unit test of the search query.
9.4.1 Writing queries with persistent data structures
Theo The Lodash functions we used were get, map, filter, and isEqual.
Joe Here’s the port of those four functions from Lodash to Immutable.js.
Listing9.12 Porting some functions from Lodash to Immutable.js
Immutable.map = function(coll, f) {
return coll.map(f);
};
Immutable.filter = function(coll, f) {
if(Immutable.isMap(coll)) {
return coll.valueSeq().filter(f);
}
return coll.filter(f);
};
Immutable.isEqual = Immutable.is;
Theo The code seems quite simple. But can you explain it to me, function by function?
Joe Sure. Let’s start with get. For accessing a field in a map, Immutable.js provides
two functions: get for direct fields and getIn for nested fields. It’s different
from Lodash, where _.get works both on direct and nested fields.

## 페이지 217

9.4 Persistent data structures in action 189
Theo What about map?
Joe Immutable.js provides its own map function. The only difference is that it is a
method of the collection, but it is something that we can easily adapt.
Theo What about filter? How would you make it work both for arrays and maps
like Lodash’s filter?
Joe Immutable.js provides a valueSeq method that returns the values of a map.
Theo Cool. And what about isEqual to compare two collections?
Joe That’s easy. Immutable.js provides a function named is that works exactly as
isEqual.
Theo So far, so good. What do I need to do now to make the code of the search
query work with Immutable.js?
Joe You simply replace each occurrence of an _ with Immutable; _.map becomes
Immutable.map, _.filter becomes Immutable.filter, and _.isEqual
becomes Immutable.isEqual.
Theo I can’t believe it’s so easy!
Joe Try it yourself; you’ll see. Sometimes, it’s a bit more cumbersome because
you need to convert the JavaScript objects to Immutable.js objects using
Immutable.fromJS.
Theo copies and pastes the snippets for the code and the unit tests of the search query.
Then, he uses his IDE to replace the _ with Immutable. When Theo executes the tests and
they pass, he is surprised but satisfied. Joe smiles.
Listing9.13 Implementing book search with persistent data structures
class Catalog {
static authorNames(catalogData, authorIds) {
return Immutable.map(authorIds, function(authorId) {
return Immutable.getIn(
catalogData,
["authorsById", authorId, "name"]);
});
}
static bookInfo(catalogData, book) {
var bookInfo = Immutable.Map({
"title": Immutable.get(book, "title"),
"isbn": Immutable.get(book, "isbn"),
"authorNames": Catalog.authorNames(
catalogData,
Immutable.get(book, "authorIds"))
});
return bookInfo;
}
static searchBooksByTitle(catalogData, query) {
var allBooks = Immutable.get(catalogData, "booksByIsbn");
var queryLowerCased = query.toLowerCase();
var matchingBooks = Immutable.filter(allBooks, function(book) {

## 페이지 218

190 CHAPTER 9 Persistent data structures
return Immutable.get(book, "title").
toLowerCase().
includes(queryLowerCased);
});
var bookInfos = Immutable.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
}
}
Listing9.14 Testing book search with persistent data structures
var catalogData = Immutable.fromJS({
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore",
"dave-gibbons"]
}
},
"authorsById": {
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
});
var bookInfo = Immutable.fromJS({
"isbn": "978-1779501127",
"title": "Watchmen",
"authorNames": ["Alan Moore",
"Dave Gibbons"]
});
Immutable.isEqual(
Catalog.searchBooksByTitle(catalogData, "Watchmen"),
Immutable.fromJS([bookInfo]));
// → true
Immutable.isEqual(
Catalog.searchBooksByTitle(catalogData, "Batman"),
Immutable.fromJS([]));
// → true

## 페이지 219

9.4 Persistent data structures in action 191
9.4.2 Writing mutations with persistent data structures
Theo Shall we move forward and port the add member mutation?
Joe Sure. Porting the add member mutation from Lodash to Immutable.js only
requires you to again replace the underscore (_) with Immutable. Let’s look at
some code.
Listing9.15 Implementing member addition with persistent data structures
UserManagement.addMember = function(userManagement, member) {
var email = Immutable.get(member, "email");
var infoPath = ["membersByEmail", email];
if(Immutable.hasIn(userManagement, infoPath)) {
throw "Member already exists.";
}
var nextUserManagement = Immutable.setIn(userManagement,
infoPath,
member);
return nextUserManagement;
};
Theo So, for the tests, I’d convert the JavaScript objects to Immutable.js objects with
Immutable.fromJS(). How does this look?
Listing9.16 Testing member addition with persistent data structures
var jessie = Immutable.fromJS({
"email": "jessie@gmail.com",
"password": "my-secret"
});
var franck = Immutable.fromJS({
"email": "franck@gmail.com",
"password": "my-top-secret"
});
var userManagementStateBefore = Immutable.fromJS({
"membersByEmail": {
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
});
var expectedUserManagementStateAfter = Immutable.fromJS({
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"

## 페이지 220

192 CHAPTER 9 Persistent data structures
}
}
});
var result = UserManagement.addMember(userManagementStateBefore, jessie);
Immutable.isEqual(result, expectedUserManagementStateAfter);
// → true
Joe Great!
9.4.3 Serialization and deserialization
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

## 페이지 221

9.4 Persistent data structures in action 193
9.4.4 Structural diff
Theo So far, we have ported pieces of code that dealt with simple data manipula-
tions. I’m curious to see how it goes with complex data manipulations such as
the code that computes the structural diff between two maps.
 NOTE Chapter 5 introduces structural diff.
Joe That also works smoothly, but we need to port another eight functions.
Listing9.19 Porting Lodash functions involved in structural diff computation
Immutable.reduce = function(coll, reducer, initialReduction) {
return coll.reduce(reducer, initialReduction);
};
Immutable.isEmpty = function(coll) {
return coll.isEmpty();
};
Immutable.keys = function(coll) {
return coll.keySeq();
};
Immutable.isObject = function(coll) {
return Immutable.Map.isMap(coll);
};
Immutable.isArray = Immutable.isIndexed;
Immutable.union = function() {
return Immutable.Set.union(arguments);
};
Theo Everything looks trivial with one exception: the use of arguments in Immutable
.union.
Joe In JavaScript, arguments is an implicit array-like object that contains the values
of the function arguments.
Theo I see. It’s one of those pieces of JavaScript magic!
Joe Yep. We need to use arguments because Lodash and Immutable.js differ slightly
in the signature of the union function. Immutable.Set.union receives an array
of lists, whereas a Lodash _.union receives several arrays.
Theo Makes sense. Let me give it a try.
Blowing on his fingers like a seasoned safecracker, first one hand and then the next, Theo
begins typing. Once again, Theo is surprised to discover that after replacing the _ with
Immutable in listing 9.20, the tests pass with the code in listing 9.21.
Listing9.20 Implementing structural diff with persistent data structures
function diffObjects(data1, data2) {
var emptyObject = Immutable.isArray(data1) ?
Immutable.fromJS([]) :

## 페이지 222

194 CHAPTER 9 Persistent data structures
Immutable.fromJS({});
if(data1 == data2) {
return emptyObject;
}
var keys = Immutable.union(Immutable.keys(data1), Immutable.keys(data2));
return Immutable.reduce(keys,
function (acc, k) {
var res = diff(Immutable.get(data1, k),
Immutable.get(data2, k));
if((Immutable.isObject(res) && Immutable.isEmpty(res)) ||
(res == "data-diff:no-diff")) {
return acc;
}
return Immutable.set(acc, k, res);
},
emptyObject);
}
function diff(data1, data2) {
if(Immutable.isObject(data1) && Immutable.isObject(data2)) {
return diffObjects(data1, data2);
}
if(data1 !== data2) {
return data2;
}
return "data-diff:no-diff";
}
Listing9.21 Testing structural diff with persistent data structures
var data1 = Immutable.fromJS({
g: {
c: 3
},
x: 2,
y: {
z: 1
},
w: [5]
});
var data2 = Immutable.fromJS({
g: {
c:3
},
x: 2,
y: {
z: 2
},
w: [4]
});
Immutable.isEqual(diff(data1, data2),
Immutable.fromJS({

## 페이지 223

Summary 195
"w": [
4
],
"y": {
"z": 2
}
}));
Joe What do you think of all this, my friend?
Theo I think that using persistent data collections with a library like Immutable.js is
much easier than understanding the internals of persistent data structures. But
I’m also glad that I know how it works under the hood.
After accompanying Joe to the office door, Theo meets Dave. Dave had been peering
through the window in Theo’s office, looking at the whiteboard, anxious to catch a glimpse
of today’s topic on DOP.
Dave What did Joe teach you today?
Theo He took me to the university and taught me the foundations of persistent data
structures for dealing with immutability at scale.
Dave What’s wrong with the structural sharing that I implemented a couple of
months ago?
Theo When the number of elements in the collection is big enough, naive structural
sharing has performance issues.
Dave I see. Could you tell me more about that?
Theo I’d love to, but my brain isn’t functioning properly after this interesting but
exhausting day. We’ll do it soon, promise.
Dave No worries. Have a nice evening, Theo.
Theo You too, Dave.
Summary
 It’s possible to manually ensure that our data isn’t mutated, but it’s cumbersome.
 At scale, naive structural sharing causes a performance hit, both in terms of
memory and computation.
 Naive structural sharing doesn’t prevent data structures from being accidentally
mutated.
 Immutable collections are not the same as persistent data structures.
 Immutable collections don’t provide an efficient way to create new versions of
the collections.
 Persistent data structures protect data from mutation.
 Persistent data structures provide an efficient way to create new versions of the
collections.
 Persistent data structures always preserve the previous version of themselves when
they are modified.

## 페이지 224

196 CHAPTER 9 Persistent data structures
 Persistent data structures represent data internally in such a way that structural
sharing scales well, both in terms of memory and computation.
 When data is immutable, it is safe to share it.
 Internally, persistence uses a branching factor of 32.
 In practice, manipulation of persistent data structures is efficient even for col-
lections with 10 billion entries!
 Due to modern architecture considerations, the performance of updating a
persistent list is dominated much more by the depth of the tree than by the
number of nodes at each level of the tree.
 Persistent lists can be manipulated in near constant time.
 In most languages, third-party libraries provide an implementation of persistent
data structures.
 Paguro collections implement the read-only parts of Java collection interfaces.
 Paguro collections can be passed to any methods that expect to receive a Java
collection without mutating them.

## 페이지 225

Database operations
A cloud is a cloud
This chapter covers
 Fetching data from the database
 Storing data in the database
 Manipulating data fetched from the database
Traditionally in OOP, we use design patterns and complex layers of objects to struc-
ture access to the database. In DOP, we prefer to represent data fetched from the
database with generic data collections, namely, lists of maps, where fields in the
maps correspond to database column values. As we’ll see throughout the chapter,
the fact that fields inside a map are accessible dynamically via their names allows us
to use the same generic code for different data entities.
TIP The best way to manipulate data is to represent data as data.
In this chapter, we’ll illustrate the application of data-oriented principles when
accessing data from a relational database. Basic knowledge of relational database
and SQL query syntax (like SELECT, AS, WHERE, and INNER JOIN) is assumed. This
approach can be easily adapted to NoSQL databases.
197

## 페이지 226

198 CHAPTER 10 Database operations
Applications that run on the server usually store data in a database. In DOP, we
represent data retrieved from the database the same way we represent any other data
in our application—with generic data collections. This leads to
 Reduced system complexity.
 Increased genericity.
10.1 Fetching data from the database
Theo and Joe go for a walk in a park near the office. They sit on a bench close to a beau-
tiful lake and gaze at the clouds in the sky. After a couple of minutes of meditative
silence, Joe asks Theo, “What do you see?” Theo tells him that this cloud looks to him
like a horse, and that one looks like a car. On their way back to the office, Theo asks Joe
for an explanation about the clouds. Joe answers with a mysterious smile on his lips, “A
cloud is a cloud.”
Theo So far you’ve shown me how DOP represents data that lives in the memory of
the application. What about data that comes from the outside?
Joe What do you mean by outside?
Theo Data that comes from the database.
Joe I’ll return the question to you. How do you think that we should represent data
that comes from the database in DOP?
Theo As generic data collections, I guess.
Joe Exactly! In DOP, we always represent data with generic data collections.
Theo Does that mean that we can manipulate data from the database with the same
flexibility as we manipulate in-memory data?
Joe Definitely.
TIP In DOP, we represent data from the database with generic data collections, and
we manipulate it with generic functions.
Theo Would you show me how to retrieve book search results when the catalog data
is stored in an SQL database?
Joe I’ll show you in a moment. First, tell me how you would design the tables that
store catalog data.
Theo Do you mean the exact table schemas with the information about primary keys
and nullability of each and every column?
Joe No, I only need a rough overview of the tables, their columns, and the relation-
ships between the tables.
Theo goes to the whiteboard. Figure 10.1 shows the diagram he draws as he explains his
thinking to Joe.

## 페이지 227

10.1 Fetching data from the database 199
T books
T authors
isbn VARCHAR[32]
id VARCHAR[64]
title VARCHAR[64]
name VARCHAR[64]
publication_year INTEGER
1
A book 1 An author
may have may author
many authors. many books.
* *
book_authors
T (relationships of books and authors)
book_isbn VARCHAR[32] Figure 10.1 The database model
author_id VARCHAR[64]
for books and authors
Theo I have a books table with three columns: title, isbn, and publication_
year. I also have an authors table with two columns: for id and name. Here,
let me draw these tables on the whiteboard to give you a visual (see tables 10.1
and 10.2).
Table 10.1 The books table filled with two books
title isbn publication_year
The Power of Habit 978-0812981605 2012
7 Habits of Highly Effective People 978-1982137274 1989
Table 10.2 The authors table filled with three authors
id name
sean-covey Sean Covey
stephen-covey Stephen Covey
charles-duhigg Charles Duhigg
Joe What about the connection between books and authors?
Theo Let’s see, a book could be written by multiple authors, and an author could write
multiple books. Therefore, I need a many-to-many book_authors table that con-
nects authors and books with two columns, book_isbn and author_id.
Theo once again turns to the whiteboard. He pens the book_authors table 10.3 to show Joe.
Table 10.3 The book_authors table with rows connecting books with their authors
book_isbn author_id
978-1982137274 sean-covey
978-1982137274 stephen-covey
978-0812981605 charles-duhigg

## 페이지 228

200 CHAPTER 10 Database operations
Joe Great! Let’s start with the simplest case. We’re going to write code that searches
for books matching a title and that returns basic information about the books.
By basic information, I mean title, ISBN, and publication year.
Theo What about the book authors?
Joe We’ll deal with that later, as it’s a bit more complicated. Can you write an SQL
query for retrieving books that contain he word habit in their title?
Theo Sure.
This assignment is quite easy for Theo. First, he jots down the SQL query, then he displays
the results in table 10.4.
Listing10.1 SQL query to retrieve books whose title contains habit
SELECT
title,
isbn,
publication_year
FROM
books
WHERE title LIKE '%habit%';
Table 10.4 Results of the SQL query for books whose title contains the word habit
title isbn publication_year
The Power of Habit 978-0812981605 2012
7 Habits of Highly Effective People 978-1982137274 1989
Joe How would you describe these results as a data collection?
Theo I would say it’s a list of maps.
TIP In DOP, accessing data from a NoSQL database is similar to the way we access
data from a relational database.
Joe Right! Now, can you write the search results as a list of maps?
Theo It doesn’t sound too complicated. How about this?
Listing10.2 Search results as a list of maps
[
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"publication_year": 1989
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"publication_year": 2012
}
]

## 페이지 229

10.1 Fetching data from the database 201
Joe What about the JSON schema for the search results?
Theo It shouldn’t be too difficult if you allow me to take a look at the JSON schema
cheat sheet you kindly offered me the other day.
Joe Of course. The purpose of a gift is to be used by the one who receives it.
Theo takes a look at the JSON Schema cheat sheet to refresh his memory about the JSON
Schema syntax. After a few minutes, Theo comes up with a schema for the search results.
He certainly is putting Joe’s gift to good use.
Listing10.3 JSON schema cheat sheet
{
"type": "array",
"items": {
"type": "object",
"properties": {
"myNumber": {"type": "number"},
"myString": {"type": "string"},
"myEnum": {"enum": ["myVal", "yourVal"]},
"myBool": {"type": "boolean"}
},
"required": ["myNumber", "myString"],
"additionalProperties": false
}
}
Listing10.4 The JSON schema for search results from the database
var dbSearchResultSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["title", "isbn", "publication_year"],
"properties": {
"title": {"type": "string"},
"isbn": {"type": "string"},
"publication_year": {"type": "integer"}
}
}
};
Joe Excellent. Now I’m going to show you how to implement searchBooks in a
way that fetches data from the database and returns a JSON string with the
results. The cool thing is that we’re only going to use generic data collections
from the database layer down to the JSON serialization.
Theo Will it be similar to the implementation of searchBooks that we wrote when
you taught me the basis of DOP?
Joe Absolutely. The only difference is that then the state of the system was stored
locally, and we queried it with a function like _.filter. Now, we use SQL

## 페이지 230

202 CHAPTER 10 Database operations
queries to fetch the state from the database. In terms of data representation
and manipulation, it’s exactly the same.
Joe goes to the whiteboard and sketches out the data flow in figure 10.2. Theo studies the
diagram.
Database
Database driver
Data (list of maps)
Data manipulation
Data Figure 10.2 Data flow for serving
a request that fetches data from
JSON serialize
the database
Joe The data manipulation step in the diagram is implemented via generic func-
tions that manipulate data collections. As our examples get more elaborate, I
think you’ll see the benefits of being able to manipulate data collections with
generic functions.
Theo Sounds intriguing...
Joe For the communication with the database, we use a driver that returns a list of
maps. In JavaScript, you could use an SQL driver like node-postgres.
 NOTE See https://node-postgres.com for more information about this collection of
node.js modules for interfacing with PostgreSQL databases.
Theo And in Java?
Joe In Java, you could use JDBC (Java database connectivity) in addition to a small
utility function that converts a JDBC result set into a list of maps. If I can use
your laptop, I’ll show you what I mean.
Joe pulls a piece of code from one of his personal GitHub repositories. He then shows the
code for the JDBC conversion to Theo, who seems a bit surprised.
Listing10.5 Converting a JDBC result set into a list of hash maps
List<Map<String, Object>> convertJDBCResultSetToListOfMaps(ResultSet rs) {
List<Map<String, Object>> listOfMaps =
new ArrayList<Map<String, Object>>();
ResultSetMetaData meta = rs.getMetaData();
while (rs.next()) {
Map map = new HashMap();
for (int i = 1; i <= meta.getColumnCount(); i++) {
String key = meta.getColumnLabel(i);
Object value = rs.getObject(i);

## 페이지 231

10.1 Fetching data from the database 203
map.put(key, value);
}
listOfMaps.add(map);
}
return listOfMaps;
}
TIP Converting a JDBC result set into a list of hash maps is quite straightforward.
Theo I expected it to be much more complicated to convert a JDBC result set into a
list of hash maps.
Joe It’s straightforward because, in a sense, JDBC is data-oriented.
Theo What about the field types?
Joe When we convert a JDBC result set into a list of maps, each value is considered
an Object.
Theo That’s annoying because it means that in order to access the value, we need to
cast it to its type.
Joe Yes and no. Look at our book search use case. We pass all the values along with-
out really looking at their type. The concrete value type only matters when we
serialize the result into JSON and that’s handled by the JSON serialization
library. It’s called late binding.
 NOTE With late binding, we defer dealing with data types as long as possible.
Theo Does that mean in my application that I’m allowed to manipulate data without
dealing with concrete types?
TIP In DOP, flexibility is increased as many parts of the system are free to manipulate
data without dealing with concrete types.
Joe Exactly. You’ll see late binding in action in a moment. That’s one of the great-
est benefits of DOP.
Theo Interesting, I can’t wait to see that!
Joe One last thing before I show you the code for retrieving search results from the
database. In order to make it easier to read, I’m going to write JavaScript code
as if JavaScript were dealing with I/O is a synchronous way.
Theo What do you mean?
Joe In JavaScript, an I/O operation like sending a query to the database is done
asynchronously. In real life, it means using either callback functions or using
async and await keywords.
Theo Oh yeah, that’s because JavaScript is single-threaded.
 NOTE For sake of simplicity, the JavaScript snippets in this chapter are written as if
JavaScript were dealing with I/O in a synchronous way. In real-life JavaScript, we need
to use async and await around I/O calls.
Joe Indeed, so I’ll be writing the code that communicates with the database as
though JavaScript were dealing with I/O synchronously. Here’s an example.

## 페이지 232

204 CHAPTER 10 Database operations
Listing10.6 Searching books in the database, returning the results in JSON
dbClient holds the Initializes Ajv (a JSON schema validation
var dbClient; DB connection. library) with allErrors: true to catch all
the data validation errors
var ajv = new Ajv({allErrors: true});
var title = "habit";
var matchingBooksQuery = `SELECT title, isbn Uses a parameterized
SQL query as a security
FROM books
best practice
WHERE title LIKE '%$1%'`;
var books = dbClient.query(matchingBooksQuery,
Passes the parameters to the SQL
[title]);
query as a list of values (in our
if(!ajv.validate(dbSearchResultSchema, books)) {
case, a list with a single value)
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from the database: " + errors;
}
JSON.stringify(books);
Theo In a dynamically-typed language like JavaScript, I understand that the types of
the values in the list of maps returned by dbClient.query are determined at
run time. How does it work in a statically-typed language like Java, and what are
the types of the data fields in books?
Joe The function convertJDBCResultSetToListOfMaps we created earlier (see
listing 10.5) returns a list of Map<String, Object>. But JSON serialization
libraries like Gson know how to detect at run time the concrete type of the val-
ues in a map and serialize the values according to their type.
 NOTE See https://github.com/google/gson for information about Gson’s Java
serialization/deserialization library.
Theo What do you mean by serializing a value according to its type?
Joe For instance, the value of the field publication_year is a number; therefore,
it is not wrapped with quotes. However, the value of the field title is a string;
therefore, it is wrapped with quotes.
Theo Nice! Now, I understand what you mean by late binding.
Joe Cool! Now, let me show you how we store data in the database.
10.2 Storing data in the database
In the previous section, we saw how to retrieve data from the database as a list of maps.
Next, we’ll see how to store data in the database when data is represented with a map.
Theo I guess that storing data in the database is quite similar to fetching data from
the database.
Joe It’s similar in the sense that we deal only with generic data collections. Can you
write a parameterized SQL query that inserts a row with user info using only
email and encrypted_password, please?
Theo OK.

## 페이지 233

10.2 Storing data in the database 205
Theo takes a moment to think about the code and writes a few lines of SQL as Joe
requested. He shows it to Joe.
Listing10.7 SQL statement to add a member
INSERT
INTO members
(email, encrypted_password)
VALUES ($1, $2)
Joe Great! And here’s how to integrate your SQL query in our application code.
Listing10.8 Adding a member from inside the application
var addMemberQuery =
"INSERT INTO members (email, password) VALUES ($1, $2)";
dbClient.query(addMemberQuery,
Passes the two parameters to
[_.get(member, "email"),
the SQL query as an array
_.get(member, "encryptedPassword")]);
Theo Your code is very clear, but something still bothers me.
Joe What is that?
Theo I find it cumbersome that you use _.get(user, "email") instead of user
.email, like I would if the data were represented with a class.
Joe In JavaScript, you are allowed to use the dot notation user.email instead of
_.get(user, "email").
Theo Then why don’t you use the dot notation?
Joe Because I wanted to show you how you can apply DOP principles even in lan-
guages like Java, where the dot notation is not available for hash maps.
 NOTE In this book, we avoid using the JavaScript dot notation to access a field in a
hash map in order to illustrate how to apply DOP in languages that don’t support dot
notation on hash maps.
Theo That’s exactly my point. I find it cumbersome in a language like Java to use
_.get(user, "email") instead of user.email like I would if the data were
represented with a class.
Joe On one hand, it’s cumbersome. On the other hand, representing data with a
hash map instead of a static class allows you to access fields in a flexible way.
Theo I know—you’ve told me so many times! But I can’t get used to it.
Joe Let me give you another example of the benefits of the flexible access to data
fields in the context of adding a member to the database. You said that writing
[_.get(member, "email"), _.get(member, "encryptedPassword")] was
less convenient than writing [member.email, member.encryptedPassword].
Right?
Theo Absolutely!
Joe Let me show you how to write the same code in a more succinct way, using a
function from Lodash called _.at.

## 페이지 234

206 CHAPTER 10 Database operations
Theo What does this _.at function do?
Joe It receives a map m, a list keyList, and returns a list made of the values in m
associated with the keys in keyList.
Theo How about an example?
Joe Sure. We create a list made of the fields email and encryptedPassword of a
member.
Joe types for a bit. He shows this code to Theo.
Listing10.9 Creating a list made of some values in a map with _.at
var member = {
"email": "samantha@gmail.com",
"encryptedPassword": "c2VjcmV0",
"isBlocked": false
};
_.at(member,
["email", "encryptedPassword"]);
// ? ["samantha@gmail.com", "c2VjcmV0"]
Theo Do the values in the results appear in the same order as the keys in keyList?
Joe Yes!
Theo That’s cool.
TIP Accessing a field in a hash map is more flexible than accessing a member in an
object instantiated from a class.
Joe And here’s the code for adding a member using _.at.
Listing10.10 Using _.at to return multiple values from a map
class CatalogDB {
static addMember(member) {
var addMemberQuery = `INSERT
INTO members
(email, encrypted_password)
VALUES ($1, $2)`;
dbClient.query(addMemberQuery,
_.at(member, ["email",
"encryptedPassword"]));
}
}
Theo I can see how the _.at function becomes really beneficial when we need to
pass a bigger number of field values.
Joe I’ll be showing you more examples that use the flexible data access that we
have in DOP.

## 페이지 235

10.3 Simple data manipulation 207
10.3 Simple data manipulation
Quite often, in a production application, we need to reshape data fetched from the
database. The simplest case is when we need to rename the columns from the data-
base to those that are more appropriate for our application.
Joe Did you notice that the column names in our database follow the snake case
convention?
Theo I’m so used to the convention, no. I didn’t even think about that.
Joe Well, for instance, the column for the publication year of a book is called
publication_year.
Theo Go on...
Joe Inside JSON, I like to use Pascal case, like publicationYear.
Theo And I’d prefer to have bookTitle instead of title.
Joe So we’re both unhappy with the JSON string that searchBooks returns if we
pass the data retrieved from the database as is.
Theo Indeed!
Joe How would you fix it?
Theo I would modify the SQL query so that it renames the columns in the results.
Here, let me show you the query.
Listing10.11 Renaming columns inside the SQL query
SELECT
title AS bookTitle,
isbn,
publication_year AS publicationYear
FROM
books
WHERE title LIKE '%habit%';
Joe That would work, but it seems a bit weird to modify an SQL query so that it fits
the naming convention of the application.
Theo Yeah, I agree. I imagine a database like MongoDB doesn’t make it easy to
rename the fields inside a query.
Joe Yep. Sometimes it makes more sense to deal with field names in application
code. How would you handle that?
Theo Well, in that case, for every map returned by the database query, I’d use a func-
tion to modify the field names.
Joe Could you show me what the code would look like?
Theo Sure. How about this?
Listing10.12 Renaming specific keys in a list of maps
function renameBookInfoKeys(bookInfo) {
return {

## 페이지 236

208 CHAPTER 10 Database operations
"bookTitle": _.get(bookInfo, "title"),
"isbn": _.get(bookInfo, "isbn"),
"publicationYear": _.get(bookInfo, "publication_year")
};
}
var bookResults = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"publication_year": 1989
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"publication_year": 2012
}
];
_.map(bookResults, renameBookInfoKeys);
Joe Would you write a similar piece of code for every query that you fetched from
the database?
Theo What do you mean?
Joe Suppose you want to rename the fields returned by a query that retrieves the
books a user has borrowed.
Theo I see. I’d write a similar piece of code for each case.
Joe In DOP, we can use the fact that a field name is just a string and write a generic
function called renameResultKeys that works on every list of maps.
Theo Wow! How does renameResultKeys know what fields to rename?
Joe You pass the mapping between the old and the new names as a map.
TIP In DOP, field names are just strings. It allows us to write generic functions to
manipulate a list of maps that represent data fetched from the database.
Theo Could you show me an example?
Joe Sure. A map like this can be passed to renameResultKeys to rename the fields
in the book search results. So, for example, you could write renameResult-
Keys like this.
Listing10.13 Renaming fields in SQL results
renameResultKeys(bookResults, {
"title": "bookTitle",
"publication_year": "publicationYear"
});
Theo What happened to the field that stores the isbn?
Joe When a field is not mentioned, renameResultKeys leaves it as-is.

## 페이지 237

10.3 Simple data manipulation 209
Theo Awesome! Can you show me the implementation of renameResultKeys?
Joe Sure, it’s only about map and reduce, so I’d do something like the following.
Listing10.14 Renaming the keys in SQL results
function renameKeys(map, keyMap) {
return _.reduce(keyMap,
function(res, newKey, oldKey) {
var value = _.get(map, oldKey);
var resWithNewKey = _.set(res, newKey, value);
var resWithoutOldKey = _.omit(resWithNewKey, oldKey);
return resWithoutOldKey;
},
map);
}
function renameResultKeys(results, keyMap) {
return _.map(results, function(result) {
return renameKeys(result, keyMap);
});
}
Theo That code isn’t exactly easy to understand!
Joe Don’t worry. The more you write data manipulation functions with map, filter,
and reduce, the more you get used to it.
Theo I hope so!
Joe What’s really important for now is that you understand what makes it possible
in DOP to write a function like renameResultKeys.
Theo I would say it’s because fields are accessible dynamically with strings.
Joe Exactly. You could say that fields are first-class citizens.
TIP In DOP, fields are first-class citizens.
Theo How would you write unit tests for a data manipulation function like rename-
ResultKeys?
Joe It’s similar to the unit tests we wrote earlier. You generate input and expected
results, and you make sure that the actual results equal the expected results.
Hang on; this may take a while.
While Joe is busy coding, Theo takes this opportunity to run to the kitchen and prepare
two espressos. What luck! There’s a box of Swiss chocolates on the counter. He grabs a cou-
ple of pieces and returns to his office just as Joe is finishing up the unit test.
Listing10.15 Unit test for renameResultKeys
var listOfMaps = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",

## 페이지 238

210 CHAPTER 10 Database operations
"publication_year": 1989
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"publication_year": 2012
}
];
var expectedResults = [
{
"bookTitle": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"publicationYear": 1989
},
{
"bookTitle": "The Power of Habit",
"isbn": "978-0812981605",
"publicationYear": 2012
}
];
var results = renameResultKeys(listOfMaps,
{"title": "bookTitle",
"publication_year": "publicationYear"});
_.isEqual(expectedResults, results);
Theo Nice!
Joe Do you see why you’re free to use renameResultKeys with the results of any
SQL query?
Theo Yes, because the code of renameResultKeys is decoupled from the internal
details of the representation of data it operates on.
Joe Exactly! Now, suppose an SQL query returns user info in a table. How would
you use renameResultKeys to rename email to userEmail? Assume the table
looks like this (table 10.5).
Once again, the whiteboard comes in to play. When he’s finished, Joe shows Theo the
table.
Table 10.5 Results of an SQL query that returns email and
encrypted_password of some users
email encrypted_password
jennie@gmail.com secret-pass
franck@hotmail.com my-secret
Theo That’s easy!

## 페이지 239

10.4 Advanced data manipulation 211
On his laptop, Theo writes the code to rename email. Satisfied, he turns the laptop to Joe.
Listing10.16 Renaming email to userEmail
var listOfMaps = [
{
"email": "jennie@gmail.com",
"encryptedPassword": "secret-pass"
},
{
"email": "franck@hotmail.com",
"encryptedPassword": "my-secret"
}
];
renameResultKeys(listOfMaps,
{"email": "userEmail"});
Joe Excellent! I think you’re ready to move on to advanced data manipulation.
10.4 Advanced data manipulation
In some cases, we need to change the structure of the rows returned by an SQL query
(for instance, aggregating fields from different rows into a single map). This could be
done at the level of the SQL query, using advanced features like JSON aggregation in
PostgreSQL. However, sometimes it makes more sense to reshape the data inside the
application because it keeps the SQL queries simple. As with the simple data manipu-
lation scenario of the previous section, once we write code that implements some data
manipulation, we’re free to use the same code for similar use cases, even if they involve
data entities of different types.
Theo What kind of advanced data manipulation did you have in mind?
Joe You’ll see in a minute, but first, an SQL task for you. Write an SQL query that
returns books, including author names, that contain the word habit in their
title.
Theo Let me give it a try.
After some trial and error, Theo is able to nail it down. He jots down an SQL query that
joins the three tables: books, book_authors, and authors.
Listing10.17 SQL query to retrieve books containing the word habit
SELECT
title,
isbn,
authors.name AS author_name
FROM
books
INNER JOIN
book_authors

## 페이지 240

212 CHAPTER 10 Database operations
ON books.isbn = book_authors.book_isbn
INNER JOIN
authors
ON book_authors.author_id = authors.id
WHERE books.title LIKE '%habit%';
Joe How many rows are in the results?
Theo goes to the whiteboard. He quickly sketches a table showing the results, then he
answers Joe’s question. Because 7 Habits of Highly Effective People has two authors, Theo lists
the book twice in table 10.6.
Table 10.6 Results of the SQL query that retrieves books whose title contain the word habit, including
author names
title isbn author_name
7 Habits of Highly Effective People 978-1982137274 Sean Covey
7 Habits of Highly Effective People 978-1982137274 Stephen Covey
The Power of Habit 978-0812981605 Charles Duhigg
Theo Three rows.
Joe And how many books?
Theo Two books.
Joe Can you show me the results of the SQL query as a list of maps?
Theo Sure.
Listing10.18 A list of maps with the results for listing 10.17
[
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"publication_year": "Sean Covey"
},
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Stephen Covey"
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"author_name": "Charles Duhigg"
}
]
Joe And what does the list of maps that we need to return look like?
Theo It’s a list with two maps, where the author names are aggregated in a list. Let
me write the code for that.

## 페이지 241

10.4 Advanced data manipulation 213
Listing10.19 Aggregating author names in a list
[
{
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"authorNames": [
"Sean Covey",
"Stephen Covey"
]
},
{
"isbn": "978-0812981605",
"title": "The Power of Habit",
"authorNames": ["Charles Duhigg"]
}
]
Joe Perfect! Now, let’s take an example of an advanced data manipulation task,
where we convert the list of maps as returned from the database to a list of
maps where the author names are aggregated.
Theo Hmm... That sounds tough.
Joe Let me break the task in two steps. First, we group together rows that belong to
the same book (with the same ISBN). Then, in each group, we aggregate
author names in a list. Hold on, I’ll diagram it as a data processing pipeline.
Joe goes the whiteboard. He draws the diagram in figure 10.3.
Joe Does it makes sense to you now?
Theo Yes, the data pipeline makes sense, but I have no idea how to write code that
implements it!
Joe Let me guide you step by step. Let’s start by grouping together books with the
same ISBN using _.groupBy.
Listing10.20 Grouping rows by ISBN
var sqlRows = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Sean Covey"
},
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Stephen Covey"
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"author_name": "Charles Duhigg"
}
];
_.groupBy(sqlRows, "isbn");

## 페이지 242

214 CHAPTER 10 Database operations
title7 Habits of Highly Effective People title7 Habits of Highly Effective People
isbn978-1982137274 isbn978-1982137274
author_name Sean Covey author_name StephenCovey
titleThe Power of Habit
isbn978-0812981605
author_nameCharles Duhigg
group byisbn
978-1982137274 978-0812981605
title7 Habits of Highly Effective People titleThe Power of Habit
isbn978-1982137274 isbn978-0812981605
author_nameSean Covey author_nameCharles Duhigg
title7 Habits of Highly Effective People
isbn978-1982137274
author_nameStephenCovey
aggregateauthor_names
title7 Habits of Highly Effective People titleThe Power of Habit
isbn978-1982137274 isbn978-0812981605
authorNames[Sean Covey, Stephen Covey] authorNames[Charles Duhigg]
Figure 10.3 Data pipeline for aggregating author names
Theo What does rowsByIsbn look like?
Joe It’s a map where the keys are isbn, and the values are lists of rows. Here’s how
that would look.
Listing10.21 Rows grouped by ISBN
{
"978-0812981605": [
{
"author_name": "Charles Duhigg",
"isbn": "978-0812981605",

## 페이지 243

10.4 Advanced data manipulation 215
"title": "The Power of Habit"
}
],
"978-1982137274": [
{
"author_name": "Sean Covey",
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
},
{
"author_name": "Stephen Covey",
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
}
]
}
Theo What’s the next step?
Joe Now, we need to take each list of rows in rowsByIsbn and aggregate author
names.
Theo And how do we do that?
Joe Let’s do it on the list of two rows for 7 Habits of Highly Effective People. The code
looks like this.
Listing10.22 Aggregating author names
var rows7Habits = [
{
"author_name": "Sean Covey",
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
},
{
"author_name": "Stephen Covey",
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
}
]; Takes the
author names
from all rows
var authorNames = _.map(rows7Habits, "author_name");
var firstRow = _.nth(rows7Habits, 0);
var bookInfoWithAuthorNames = _.set(firstRow, "authorNames", authorNames);
_.omit(bookInfoWithAuthorNames, "author_name");
Removes the
author_name field
Joe First, we take the author names from all the rows. Then, we take the first row as
a basis for the book info, we add a field authorNames, and remove the field
author_name.
Theo Can we make a function of it?
Joe That’s exactly what I was going to suggest!

## 페이지 244

216 CHAPTER 10 Database operations
Theo I’ll call the function aggregateField. It will receive three arguments: the
rows, the name of the field to aggregate, and the name of the field that holds
the aggregation.
Theo turns to his laptop. After a couple of minutes, his screen displays the implementation
for aggregateField.
Listing10.23 Aggregating an arbitrary field
function aggregateField(rows, fieldName, aggregateFieldName) {
var aggregatedValues = _.map(rows, fieldName);
var firstRow = _.nth(rows, 0);
var firstRowWithAggregatedValues = _.set(firstRow,
aggregateFieldName,
aggregatedValues);
return _.omit(firstRowWithAggregatedValues, fieldName);
}
Joe Do you mind writing a test case to make sure your function works as expected?
Theo With pleasure! Take a look.
Listing10.24 Test case for aggregateField
var expectedResults = {
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"authorNames": [
"Sean Covey",
"Stephen Covey"
]
};
_.isEqual(expectedResults,
aggregateField(rows7Habits,
"author_name",
"authorNames"));
Joe Excellent! Now that we have a function that aggregates a field from a list of
rows, we only need to map the function over the values of our rowsByIsbn. Let
me code that up for you.
Listing10.25 Aggregating author names in rowsByIsbn
var rowsByIsbn = _.groupBy(sqlRows, "isbn");
var groupedRows = _.values(rowsByIsbn);
_.map(rowsByIsbn, function(groupedRows) {
return aggregateField(groupedRows, "author_name", "authorNames");
})

## 페이지 245

10.4 Advanced data manipulation 217
Theo Why did you take the values of rowsByIsbn?
Joe Because we don’t really care about the keys in rowsByIsbn. We only care about
the grouping of the rows in the values of the hash map.
Theo Let me try to combine everything we’ve done and write a function that receives
a list of rows and returns a list of book info with the author names aggregated
in a list.
Joe Good luck, my friend!
To Theo, it’s less complicated than it seems. After a couple of trials and errors, he arrives at
the code and the test case.
Listing10.26 Aggregating a field in a list of rows
function aggregateFields(rows, idFieldName,
fieldName, aggregateFieldName) {
var groupedRows = _.values(_.groupBy(rows, idFieldName));
return _.map(groupedRows, function(groupedRows) {
return aggregateField(groupedRows, fieldName, aggregateFieldName);
});
}
var sqlRows = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Sean Covey"
},
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"author_name": "Stephen Covey"
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"author_name": "Charles Duhigg"
}
];
var expectedResults =
[
{
"authorNames": [
"Sean Covey",
"Stephen Covey"
],
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
},
{
"authorNames": ["Charles Duhigg"],
"isbn": "978-0812981605",
"title": "The Power of Habit",

## 페이지 246

218 CHAPTER 10 Database operations
}
];
_.isEqual(aggregateFields(sqlRows,
"isbn",
"author_name",
"authorNames"),
expectedResults);
Theo I think I’ve got it.
Joe Congratulations! I’m proud of you, Theo.
Now Theo understands what Joe meant when he told him “a cloud is cloud” when they
were walking back from the park to the office. Instead of trapping data in the limits of our
objects, DOP guides us to represent data as data.
Summary
 Inside our applications, we represent data fetched from the database, no matter
if it is relational or nonrelational, as a generic data structure.
 In the case of a relational database, data is represented as a list of maps.
 Representing data from the database as data reduces system complexity because
we don’t need design patterns or complex class hierarchies to do it.
 We are free to manipulate data from the database with generic functions, such as
returning a list made of the values of some data fields, creating a version of a
map omitting a data field, or grouping maps in a list according to the value of a
data field.
 We use generic functions for data manipulation with great flexibility, using the
fact that inside a hash map, we access the value of a field via its name, repre-
sented as a string.
 When we package our data manipulation logic into custom functions that receive
field names as arguments, we are able to use those functions on different data
entities.
 The best way to manipulate data is to represent data as data.
 We represent data from the database with generic data collections, and we
manipulate it with generic functions.
 Accessing data from a NoSQL database is done in a similar way to the approach
presented in this chapter for accessing data from a relational database.
 With late binding, we care about data types as late as possible.
 Flexibility is increased as many parts of the system are free to manipulate data
without dealing with concrete types.
 Accessing a field in a hash map is more flexible than accessing a member in an
object instantiated from a class.

## 페이지 247

Summary 219
 In DOP, field names are just strings. It allows us to write generic functions to
manipulate list of maps representing data fetched from the database.
 In DOP, fields are first-class citizens.
 We can implement renaming keys in a list of maps or aggregating rows returned
by a database query via generic functions.
 JDBC stands for Java database connectivity.
 Converting a JDBC result set into a list of maps is quite straightforward.
Lodash functions introduced in this chapter
Function Description
at(map, [paths]) Creates an array of values corresponding to paths of map
omit(map, [paths]) Creates a map composed of the fields of map not in paths
nth(arr, n) Gets the element at index n in arr
groupBy(coll, f) Creates a map composed of keys generated from the results of running
each element of coll through f. The corresponding value for each key
is an array of elements responsible for generating the key.

## 페이지 248

Web services
A faithful messenger
This chapter covers
 Representing a client request as a map
 Representing a server response as a map
 Passing data forward
 Combining data from different sources
The architecture of modern information systems is made of software components
written in various programming languages like JSON, which communicate over the
wire by sending and receiving data represented in a language-independent data
exchange format. DOP applies the same principle to the communication between
inner parts of a program.
 NOTE When a web browser sends a request to a web service, it’s quite common
that the web service itself sends requests to other web services in order to fulfill the
web browser request. One popular data exchange format is JSON.
Inside a program, components communicate by sending and receiving data repre-
sented in a component independent format—namely, immutable data collections.
In the context of a web service that fulfills a client request by fetching data from a
220

## 페이지 249

11.1 Another feature request 221
database and other web services, representing data, as with immutable data collec-
tions, leads to these benefits:
 Using generic data manipulation functions to manipulate data from multiple
data sources
 Passing data forward freely with no additional complexity
11.1 Another feature request
After having delivered the database milestone on time, Theo calls Nancy to share the good
news. Instead of celebrating Theo’s success, Nancy asks him about the ETA for the next
milestone, Book Information Enrichment with the Open Library Books API. Theo tells her
that he’ll get back to her with an ETA by the end of the day. When Joe arrives at the office,
Theo tells him about the discussion with Nancy.
Theo I just got a phone call from Nancy, and she is stressed about the next milestone.
Joe What’s in the next milestone?
Theo Do you remember the Open Library Books API that I told you about a few
weeks ago?
 NOTE You can find the Open Library Books API at https://openlibrary.org/dev/
docs/api/books.
Joe No.
Theo It’s a web service that provides detailed information about books.
Joe Cool!
Theo Nancy wants to enrich the book search results. Instead of fetching book infor-
mation from the database, we need to retrieve extended book information
from the Open Library Books API.
Joe What kind of book information?
Theo Everything! Number of pages, weight, physical format, topics, etc....
Joe What about the information from the database?
Theo Besides the information about the availability of the books, we don’t need it
anymore.
Joe Have you already looked at the Open Library Books API?
Theo It’s a nightmare! For some books, the information contains dozen of fields,
and for other books, it has only two or three fields.
Joe What’s the problem then?
Theo I have no idea how to represent data that is so sparse and unpredictable.
Joe When we represent data as data, that’s not an issue. Let’s have a coffee and I’ll
show you.

## 페이지 250

222 CHAPTER 11 Web services
11.2 Building the insides like the outsides
While Theo drinks his macchiato, Joe draws a diagram on a whiteboard. Figure 11.1 shows
Joe’s diagram.
Web browser
Data
Web server
Data Data
Web service Database Figure 11.1 The high-level architecture
of a modern information system
Joe Before we dive into the details of the implementation of the book search result
enrichment, let me give you a brief intro.
Theo Sure.
Joe takes a sip of his espresso. He then points to the diagram (figure 11.1) on the whiteboard.
Joe Does this look familiar to you?
Theo Of course!
Joe Can you show me, roughly, the steps in the data flow of a web service?
Theo Sure.
Theo moves closer to the whiteboard. He writes a list of steps (see the sidebar) near the
architecture diagram.
The steps of the data flow inside a web service
1 Receive a request from a client.
2 Apply business logic to the request.
3 Fetch data from external sources (e.g., database and other web services).
4 Apply business logic to the responses from external sources.
5 Send the response to the client.
Joe Excellent! Now comes an important insight about DOP.
Theo I’m all ears.

## 페이지 251

11.2 Building the insides like the outsides 223
Joe We should build the insides of our systems like we build the outsides.
Theo What do you mean?
Joe How do components of a system communicate over the wire?
Theo By sending data.
Joe Does the data format depend on the programming language of the components?
Theo No, quite often it’s JSON, for which we have parsers in all programming
languages.
Joe What the idiom says is that, inside our program, the inner components of a pro-
gram should communicate in a way that doesn’t depend on the components.
Theo I don’t get that.
Joe Let me explain why traditional OOP breaks this idiom. Perhaps it will be
clearer then. When data is represented with classes, the inner components of
a program need to know the internals of the class definitions in order to
communicate.
Theo What do you mean?
Joe In order to be able to access a member in a class, a component needs to import
the class definition.
Theo How could it be different?
Joe In DOP, as we have seen so far, the inner components of a program communi-
cate via generic data collections. It’s similar to how components of a system
communicate over the wire.
TIP We should build the insides of our systems like we build the outsides.
Theo Why is that so important?
Joe From a design perspective, it’s important because it means that the inner com-
ponents of a program are loosely coupled.
Theo What do you mean by loosely coupled?
Joe I mean that components need no knowledge about the internals of other com-
ponents. The only knowledge required is the names of the fields.
TIP In DOP, the inner components of a program are loosely coupled.
Theo And from an implementation perspective?
Joe As you’ll see in a moment, implementing the steps of the data flow that you
just wrote on the whiteboard is easy. It comes down to expressing the busi-
ness logic in terms of generic data manipulation functions. Here, let me
show you a diagram.
Joe steps up to the whiteboard and sketches the drawing in figure 11.2. As Joe finishes, his
cell phone rings. He excuses himself and steps outside to take the call.

## 페이지 252

224 CHAPTER 11 Web services
JSON parse/serialize
Data
Business logic
Data manipulation
Data
Figure 11.2 The internals of a
JSON parse/serialize
data-oriented web service
Theo stands alone for a few minutes in front of the whiteboard, meditating about “build-
ing the insides of our systems like we build the outsides.” Without really noticing it, he
takes a marker and starts drawing a new diagram (see figure 11.3), which summarizes the
insights that Joe just shared with him.
Web browser
Data
Web service
JSON Parser (1) JSON Serializer (6)
Data Data
Business Logic
Data Manipulation (2) Data Manipulation (5)
Figure 11.3 Building the insides of our
systems like building the outsides. The inner
Data Data components of a web service communicate
with data. As an example, here is a typical
JSON Serializer (3) JSON Parser (4) flow of a web service handling a client
request: (1) Parse the client JSON request
into data. (2) Manipulate data according
Data Data to business logic. (3) Serialize data into a
JSON request to a database and another
Web service. (4) Parse JSON responses into
data. (5) Manipulate data according to
Web service Database business logic. (6) Serialize data into a
JSON response to the client.

## 페이지 253

11.3 Representing a client request as a map 225
11.3 Representing a client request as a map
After a few minutes, Joe comes back. When he looks at Theo’s new drawing in figure 11.3,
he seems satisfied.
Joe Sorry for the interruption. Let’s start from the beginning—parsing a client
request. How do you usually receive the parameters of a client request?
Theo It depends. The parameters could be sent as URL query parameters in a GET
request or as a JSON payload in the body of a POST request.
Joe Let’s suppose we receive a JSON payload inside a web request. Can you give me
an example of a JSON payload for an advanced search request?
Theo It would contain the text that the book title should match.
Joe And what are the details about the fields to retrieve from the Open Library
Books API?
Theo They won’t be passed as part of the JSON payload because they’re the same for
all search requests.
Joe I can imagine a scenario where you want the client to decide what fields to
retrieve. For instance, a mobile client would prefer to retrieve only the most
important fields and save network bandwidth.
Theo Well, in that case, I would have two different search endpoints: one for mobile
and one for desktop.
Joe What about situations where the client wants to display different pieces of infor-
mation, depending on the application screen. For instance, in an extended
search result screen, we display all the fields. In a basic search result screen, we
display only the most important fields. Now you have four different use cases:
desktop extended, desktop basic, mobile extended, and mobile basic. Would
you create four different endpoints?
Theo OK, you’ve convinced me. Let’s have a single search endpoint and let the
client decide what fields to retrieve.
Joe Can you show me an example of a JSON payload for a search request?
Theo Sure.
Because there’s not much code, Theo writes the search request on the whiteboard. It takes
very little time to show how the clients would decide on what fields to retrieve for each
search result.
Listing11.1 Example of the search request payload
{
"title": "habit",
"fields": ["title", "weight", "number_of_pages"]
}
Joe Excellent! Now, the first step is to parse the JSON string into a data structure.
Theo Let me guess, it’s going to be a generic data structure.
Joe Of course! In that case, we’ll have a map. Usually, JSON parsing is handled by
the web server framework, but I’m going to show you how to do it manually.

## 페이지 254

226 CHAPTER 11 Web services
Theo Wait! What do you mean by the web server framework?
Joe Stuff like Express in Node.js, Spring in Java, Django in Python, Ruby on Rails,
ASP.net in C#, and so forth.
Theo Oh, I see. So, how do you manually parse a JSON string into a map?
Joe In JavaScript, we use JSON.parse. In Java, we use a third-party library like Gson
(https://github.com/google/gson), maintained by Google.
Joe opens his laptop and writes two code fragments, one in JavaScript and the other in Java
with Gson. When he’s done, he shows the code to Theo.
Listing11.2 Parsing a JSON string in JavaScript
var jsonString =
'{"title":"habit","fields":["title","weight","number_of_pages"]}';
JSON.parse(jsonString);
Listing11.3 Parsing a JSON string in Java with Gson
var jsonString =
'{"title":"habit","fields":["title","weight","number_of_pages"]}';
gson.fromJson(jsonString, Map.class);
Joe Can you write the JSON schema for the payload of a search request?
Theo Sure. It would look something like this.
Listing11.4 The JSON schema for a search request
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {
"enum": [
"title",
"full_title",
"subtitle",
"publisher",
"publish_date",
"weight",
"physical_dimensions",
"number_of_pages",
"subjects",
"publishers",
"genre"
]
}
}
},
"required": ["title", "fields"]
};

## 페이지 255

11.4 Representing a server response as a map 227
Joe Nice! You marked the elements in the fields array as enums and not as
strings. Where did you get the list of allowed values?
Theo Nancy gave me the list of the fields that she wants to expose to the users. Here,
let me show you her list.
Listing11.5 The important fields from the Open Library Books API
- title
- full_title
- subtitle
- publisher
- publish_date
- weight
- physical_dimensions
- number_of_pages
- subjects
- publishers
- genre
11.4 Representing a server response as a map
Joe What does the Open Library Books API look like?
Theo It’s quite straightforward. We create a GET request with the book ISBN, and it
gives us a JSON string with extended information about the book. Take a look
at this.
When Theo executes the code snippet, it displays a JSON string with the extended infor-
mation about 7 Habits of Highly Effective People.
Listing11.6 Fetching data from the Open Library Books API
fetchAndLog(
"https:/ /openlibrary.org/isbn/978-1982137274.json"
);
A utility function
//{
that fetches JSON
// "authors": [
and displays it to
// {
the console
// "key": "/authors/OL383159A",
// },
// {
// "key": "/authors/OL30179A",
// },
// {
// "key": "/authors/OL1802361A",
// },
// ],
// "created": {
// "type": "/type/datetime",
// "value": "2020-08-17T14:26:27.274890",
// },
// "full_title": "7 Habits of Highly Effective
// People : Revised and Updated Powerful
// Lessons in Personal Change",

## 페이지 256

228 CHAPTER 11 Web services
// "isbn_13": [
// "9781982137274",
// ],
// "key": "/books/OL28896586M",
// "languages": [
// {
// "key": "/languages/eng",
// },
// ],
// "last_modified": {
// "type": "/type/datetime",
// "value": "2021-09-08T19:07:57.049009",
// },
// "latest_revision": 3,
// "lc_classifications": [
// "",
// ],
// "number_of_pages": 432,
// "publish_date": "2020",
// "publishers": [
// "Simon & Schuster, Incorporated",
// ],
// "revision": 3,
// "source_records": [
// "bwb:9781982137274",
// ],
// "subtitle": "Powerful Lessons in Personal Change",
// "title": "7 Habits of Highly Effective
// People : Revised and Updated",
// "type": {
// "key": "/type/edition",
// },
// "works": [
// {
// "key": "/works/OL2629977W",
// },
// ],
//}
Joe Did Nancy ask for any special treatment of the fields returned by the API?
Theo Nothing special besides keeping only the fields I showed you.
Joe That’s it?
Theo Yes. For example, here’s the JSON string returned by the Open Library Books
API for 7 Habits of Highly Effective People after having kept only the necessary
fields.
Listing11.7 Open Library response for 7 Habits of Highly Effective People
{
"title":"7 Habits of Highly Effective People : Revised and Updated",
"subtitle":"Powerful Lessons in Personal Change",
"number_of_pages":432,
"full_title":"7 Habits of Highly Effective People : Revised and Updated

## 페이지 257

11.4 Representing a server response as a map 229
Powerful Lessons in Personal Change",
"publish_date":"2020",
"publishers":["Simon & Schuster, Incorporated"]
}
Theo Also, Nancy wants us to keep only the fields that appear in the client request.
Joe Do you know how to implement the double field filtering?
Theo Yeah, I’ll parse the JSON string from the API into a hash map, like we parsed a
client request, and then I’ll use _.pick twice to keep only the required fields.
Joe It sounds like a great plan to me. Can you code it, including validating the data
that is returned by the Open Library API?
Theo Sure! Let me first write the JSON schema for the Open Library API response.
Theo needs to refresh his memory with the materials about schema composition in order
to express the fact that either isbn_10 or isbn_13 are mandatory. After a few moments,
he shows the JSON schema to Joe.
Listing11.8 The JSON schema for the Open Library Books API response
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

## 페이지 258

230 CHAPTER 11 Web services
var mandatoryIsbn10 = {
"type": "object",
"required": ["isbn_10"]
};
var bookInfoSchema = {
"allOf": [
basicBookInfoSchema,
{
"anyOf": [mandatoryIsbn13, mandatoryIsbn10]
}
]
};
Theo Now, assuming that I have a fetchResponseBody function that sends a request
and retrieves the body of the response as a string, let me code up the how to do
the retrieval. Give me a sec.
Theo types away in his IDE for several minutes. He shows the result to Joe.
Listing11.9 Retrieving book information from the Open Library Books API
var ajv = new Ajv({allErrors: true});
class OpenLibraryDataSource {
static rawBookInfo(isbn) {
var url = `https:/ /openlibrary.org/isbn/${isbn}.json`;
var jsonString = fetchResponseBody(url);
Fetches JSON in
return JSON.parse(jsonString);
the body of a
}
response
static bookInfo(isbn, requestedFields) {
var relevantFields = ["title", "full_title",
"subtitle", "publisher",
"publish_date", "weight",
"physical_dimensions", "genre",
"subjects", "number_of_pages"];
var rawInfo = rawBookInfo(isbn);
if(!ajv.validate(bookInfoSchema, rawInfo)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from Open Books API: " +
errors;
}
var relevantInfo =
_.pick(_.pick(rawInfo, relevantFields), requestedFields);
return _.set(relevantInfo, "isbn", isbn);
}
}
 NOTE The JavaScript snippets of this chapter are written as if JavaScript were deal-
ing with I/O in a synchronous way. In real life, we need to use async and await around
I/O calls.

## 페이지 259

11.5 Passing information forward 231
Joe Looks good! But why did you add the isbn field to the map returned by
bookInfo?
Theo It will allow me to combine information from two sources about the same book.
Joe I like it!
11.5 Passing information forward
Joe If I understand it correctly, the program needs to combine two kinds of data:
basic book information from the database and extended book information
from the Open Library API. How are you going to combine them into a single
piece of data in the response to the client?
Theo In traditional OOP, I would create a specific class for each type of book
information.
Joe What to you mean?
Theo You know, I’d have classes like DBBook, OpenLibraryBook, and CombinedBook.
Joe Hmm...
Theo But that won’t work because we decided to go with a dynamic approach, where
the client decides what fields should appear in the response.
Joe True, and classes don’t bring any added value because we need to pass data for-
ward. Do you know the story of the guy who asked his friend to bring flowers to
his fiancée?
Theo No.
Joe takes a solemn position as if to speak before a gathering of peers. With a deep breath,
he tells Theo the following story. Entranced, Theo listens carefully.
The story of the guy who asked his friend to bring flowers to his fiancée
A few weeks before their wedding, Hugo wanted to send flowers to Iris, his fiancée,
who was on vacation with her family in a neighboring town. Unable to travel because
he’s needed at work to fix a critical error in a security app, Hugo asks his friend Willy
to make the trip and to take the bouquet of flowers to his beloved, accompanied by
an envelope containing a love letter that Hugo had written for his fiancée. Willy, hav-
ing to make the trip anyway, kindly accepts.
Before giving the flowers to Iris, Willy phoned his friend Hugo to let him know that he
was about to complete his mission. Hugo’s joy was beyond belief until Willy told Hugo
how much he admired the quality of his writing style.
Hugo was disappointed. “What! Did you read the letter I wrote to my fiancée?”
“Of course!” answered Willy. “It was necessary to do so in order to fulfill my duty
faithfully.”
Theo That doesn’t make any sense! Why would Willy have to read the letter in order
to fulfill his duty?

## 페이지 260

232 CHAPTER 11 Web services
Joe That’s exactly the point of the story! In a sense, traditional OOP is like Hugo’s
friend, Willy. In order to pass information forward, OOP developers think they
need to “open the letter” and represent information with specific classes.
Theo Oh, I see. And DOP developers emulate the spirit of what Hugo expected from
a delivery person; they just pass information forward as generic data structures.
Joe Exactly.
Theo That’s a subtle but funny analogy.
Joe Let’s get back to the question of combining data from the database with data
from the Books API. There are two ways to do this—nesting and merging.
Joe goes to the whiteboard. He finds an area to draw table 11.1 for Theo.
Table 11.1 Two ways to combine hash maps
Advantages Disadvantages
Nesting No need to handle conflicts. Result is not flat.
Merging Result is flat. Need to handle conflicts.
Theo How does nesting work?
Joe In nesting, we add a field named extendedInfo to the information fetched
from the Open Library API.
Theo I see. And what about merging?
Joe In merging, we combine the fields of both maps into a single map.
Theo If there are fields with the same name in both maps, what then?
Joe Then you have a merge conflict, and you need to decide how to handle the
conflict. That’s the drawback of merging.
 NOTE When merging maps, we need to think about the occurrences of conflicting
fields.
Theo Hopefully, in the context of extended search results, the maps don’t have any
fields in common.
Joe Then let’s merge them!
Theo Would I need to write custom code for merging two maps?
Joe No! As you might remember from one of our previous sessions, Lodash pro-
vides a handy _.merge function.
 NOTE _.merge was introduced in chapter 5.
Theo Could you refresh my memory?
Joe Sure. Show me an example of maps with data from the database and data from
the Open Library Books API, and I’ll show you how to merge them.
Theo From the database, we get only two fields: isbn and available. From the
Open Library API, we get six fields. Here’s what they look like.

## 페이지 261

11.5 Passing information forward 233
Listing11.10 A map with book information from the database
var dataFromDb = {
"available": true,
"isbn": "978-1982137274"
};
Listing11.11 A map with book information from the Open Library Books API
var dataFromOpenLib = {
"title":"7 Habits of Highly Effective People : Revised and Updated",
"subtitle":"Powerful Lessons in Personal Change",
"number_of_pages":432,
"full_title":"7 Habits of Highly Effective People : \
Revised and Updated Powerful Lessons in Personal Change",
"publish_date":"2020",
"publishers":["Simon & Schuster, Incorporated"]
};
Joe After calling _.merge, the result is a map with fields from both maps.
Listing11.12 Merging two maps
_.merge(dataFromDb, dataFromOpenLib);
//{
// "available": true,
// "full_title": "7 Habits of Highly Effective People :\
// Revised and Updated Powerful Lessons in Personal Change",
// "isbn": "978-1982137274",
// "number_of_pages": 432,
// "publish_date": "2020",
// "publishers": [ "Simon & Schuster, Incorporated"],
// "subtitle": "Powerful Lessons in Personal Change",
// "title": "7 Habits of Highly Effective People : Revised and Updated"
//}
Theo Let me code the JSON schema for the search books response. Here’s how that
would look.
Listing11.13 JSON schema for search books response
var searchBooksResponseSchema = {
"type": "object",
"required": ["title", "isbn", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
"publishers": {
"type": "array",
"items": {"type": "string"}
},
"number_of_pages": {"type": "integer"},
"weight": {"type": "string"},

## 페이지 262

234 CHAPTER 11 Web services
"physical_format": {"type": "string"},
"subjects": {
"type": "array",
"items": {"type": "string"}
},
"isbn": {"type": "string"},
"publish_date": {"type": "string"},
"physical_dimensions": {"type": "string"}
}
};
Theo Yes! I think we now have all the pieces to enrich our search results.
11.6 Search result enrichment in action
Joe Can you write the steps of the enrichment data flow?
Theo Sure.
Theo goes to the whiteboard. He takes a moment to gather his thoughts, and then erases
enough space so there’s room to list the steps.
The steps for the search result enrichment data flow
1 Receive a request from a client.
2 Extract from the client’s request the query and the fields to fetch from Open
Library.
3 Retrieve from the database the books that match the query.
4 Fetch information from Open Library for each ISBN that match the query.
5 Extract from Open Library responses for the required fields.
6 Combine book information from the database with information from Open
Library.
7 Send the response to the client.
Joe Perfect! Would you like to try to implement it?
Theo I think I’ll start with the implementation of the book retrieval from the data-
base. It’s quite similar to what we did last month.
 NOTE See chapter 10 for last month’s lesson.
Joe Actually, it’s even simpler because you don’t need to join tables.
Theo That’s right, I need values only for the isbn and available columns.
Theo works for a bit in his IDE. He begins with the book retrieval from the database.
Listing11.14 Retrieving books whose title matches a query
var dbSearchResultSchema = {
"type": "array",
"items": {

## 페이지 263

11.6 Search result enrichment in action 235
"type": "object",
"required": ["isbn", "available"],
"properties": {
"isbn": {"type": "string"},
"available": {"type": "boolean"}
}
}
};
class CatalogDB {
static matchingBooks(title) {
var matchingBooksQuery = `
SELECT isbn, available
FROM books
WHERE title = like '%$1%';
`;
var books = dbClient.query(catalogDB, matchingBooksQuery, [title]);
if(!ajv.validate(dbSearchResultSchema, books)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from the database: " +
errors;
}
return books;
}
}
Joe So far, so good...
Theo Next, I’ll go with the implementation of the retrieval of book information from
Open Library for several books. Unfortunately, the Open Library Books API
doesn’t support querying several books at once. I’ll need to send one request
per book.
Joe That’s a bit annoying. Let’s make our life easier and pretend that _.map works
with asynchronous functions. In real life, you’d need something like Promise
.all in order to send the requests in parallel and combine the responses.
Theo OK, then it’s quite straightforward. I’ll take the book retrieval code and add a
multipleBookInfo function that maps over bookInfo.
Theo looks over the book retrieval code in listing 11.9 and then concentrates as he types
into his IDE. When he’s done, he shows the result in listing 11.15 to Joe.
Listing11.15 Retrieving book information from Open Library for several books
class OpenLibraryDataSource {
static rawBookInfo(isbn) {
var url = `https:/ /openlibrary.org/isbn/${isbn}.json`;
var jsonString = fetchResponseBody(url);
return JSON.parse(jsonString);
}
static bookInfo(isbn, requestedFields) {
var relevantFields = ["title", "full_title",
"subtitle", "publisher",
"publish_date", "weight",

## 페이지 264

236 CHAPTER 11 Web services
"physical_dimensions", "genre",
"subjects", "number_of_pages"];
var rawInfo = rawBookInfo(isbn);
if(!ajv.validate(dbSearchResultSchema, bookInfoSchema)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from Open Books API: " +
errors;
}
var relevantInfo =
_.pick(_.pick(rawInfo, relevantFields), requestedFields);
return _.set(relevantInfo, "isbn", isbn);
}
static multipleBookInfo(isbns, fields) {
return _.map(function(isbn) {
return bookInfo(isbn, fields);
}, isbns);
}
}
Joe Nice! Now comes the fun part: combining information from several data sources.
Theo Yeah. I have two arrays in my hands: one with book information from the data-
base and one with book information from Open Library. I somehow need to
join the arrays, but I’m not sure I can assume that the positions of the book
information are the same in both arrays.
Joe What would you like to have in your hands?
Theo I wish I had two hash maps.
Joe And what would the keys in the hash maps be?
Theo Book ISBNs.
Joe Well, I have good news for you: your wish is granted!
Theo How?
Joe Lodash provides a function named _.keyBy that transforms an array into a map.
Theo I can’t believe it. Can you show me an example?
Joe Sure. Let’s call _.keyBy on an array with two books.
Listing11.16 Transforming an array into a map with _.keyBy
var books = [
{
"title": "7 Habits of Highly Effective People",
"isbn": "978-1982137274",
"available": true
},
{
"title": "The Power of Habit",
"isbn": "978-0812981605",
"available": false
}
];
_.keyBy(books, "isbn");

## 페이지 265

11.6 Search result enrichment in action 237
Joe And here’s the result.
Listing11.17 The result of keyBy
{
"978-0812981605": {
"available": false,
"isbn": "978-0812981605",
"title": "The Power of Habit"
},
"978-1982137274": {
"available": true,
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People"
}
}
Theo keyBy is awesome!
Joe Don’t exaggerate, my friend; _.keyBy is quite similar to _.groupBy. The
only difference is that _.keyBy assumes that there’s only one element in
each group.
Theo I think that, with _.keyBy, I’ll be able to write a generic joinArrays function.
Joe I’m glad to see you thinking in terms of implementing business logic through
generic data manipulation functions.
TIP Many parts of the business logic can be implemented through generic data
manipulation functions.
Theo The joinArrays function needs to receive the arrays and the field name for
which we decide the two elements that need to be combined, for instance,
isbn.
Joe Remember, in general, it’s not necessarily the same field name for both arrays.
Theo Right, so joinArrays needs to receive four arguments: two arrays and two
field names.
Joe Go for it! And, please, write a unit test for joinArrays.
Theo Of course...
Theo works for a while and produces the code in listing 11.18. He then types the unit test
in listing 11.19.
Listing11.18 A generic function for joining arrays
function joinArrays(a, b, keyA, keyB) {
var mapA = _.keyBy(a, keyA);
var mapB = _.keyBy(b, keyB);
var mapsMerged = _.merge(mapA, mapB);
return _.values(mapsMerged);
}

## 페이지 266

238 CHAPTER 11 Web services
Listing11.19 A unit test for joinArrays
var dbBookInfos = [
{
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"available": true
},
{
"isbn": "978-0812981605",
"title": "The Power of Habit",
"available": false
}
];
var openLibBookInfos = [
{
"isbn": "978-0812981605",
"title": "7 Habits of Highly Effective People",
"subtitle": "Powerful Lessons in Personal Change",
"number_of_pages": 432,
},
{
"isbn": "978-1982137274",
"title": "The Power of Habit",
"subtitle": "Why We Do What We Do in Life and Business",
"subjects": [
"Social aspects",
"Habit",
"Change (Psychology)"
],
}
];
var joinedArrays = [
{
"available": true,
"isbn": "978-1982137274",
"subjects": [
"Social aspects",
"Habit",
"Change (Psychology)",
],
"subtitle": "Why We Do What We Do in Life and Business",
"title": "The Power of Habit",
},
{
"available": false,
"isbn": "978-0812981605",
"number_of_pages": 432,
"subtitle": "Powerful Lessons in Personal Change",
"title": "7 Habits of Highly Effective People",
},
]

## 페이지 267

11.6 Search result enrichment in action 239
_.isEqual(joinedArrays,
joinArrays(dbBookInfos, openLibBookInfos, "isbn", "isbn"));
Joe Excellent! Now, you are ready to adjust the last piece of the extended search
result endpoint.
Theo That’s quite easy. We fetch data from the database and from Open Library and
join them.
Theo works quite rapidly. He then shows Joe the code.
Listing11.20 Search books and enriched book information
class Catalog {
static enrichedSearchBooksByTitle(searchPayload) {
if(!ajv.validate(searchBooksRequestSchema, searchPayload)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid request:" + errors;
}
var title = _.get(searchPayload, "title");
var fields = _.get(searchPayload, "fields");
var dbBookInfos = CatalogDataSource.matchingBooks(title);
var isbns = _.map(dbBookInfos, "isbn");
var openLibBookInfos =
OpenLibraryDataSource.multipleBookInfo(isbns, fields);
var res = joinArrays(dbBookInfos, openLibBookInfos);
if(!ajv.validate(searchBooksResponseSchema, request)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid response:" + errors;
}
return res;
}
}
Now comes the tricky part. Theo takes a few moments to meditate about the simplicity of
the code that implements the extended search endpoint. He thinks about how classes are
much less complex when we use them only to aggregate stateless functions that operate on
similar domain entities and then goes to work plotting the code.
Listing11.21 Schema for the extended search endpoint (Open Books API part)
var basicBookInfoSchema = {
"type": "object",
"required": ["title"],
"properties": {
"title": {"type": "string"},
"publishers": {
"type": "array",
"items": {"type": "string"}
},

## 페이지 268

240 CHAPTER 11 Web services
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
"anyOf": [mandatoryIsbn13, mandatoryIsbn10]
}
]
};
Listing11.22 Extended search endpoint (Open Books API part)
var ajv = new Ajv({allErrors: true});
class OpenLibraryDataSource {
static rawBookInfo(isbn) {
var url = `https:/ /openlibrary.org/isbn/${isbn}.json`;
var jsonString = fetchResponseBody(url);
return JSON.parse(jsonString);
}
static bookInfo(isbn, requestedFields) {
var relevantFields = ["title", "full_title",
"subtitle", "publisher",
"publish_date", "weight",

## 페이지 269

11.6 Search result enrichment in action 241
"physical_dimensions", "genre",
"subjects", "number_of_pages"];
var rawInfo = rawBookInfo(isbn);
if(!ajv.validate(bookInfoSchema, rawInfo)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from Open Books API: " +
errors;
}
var relevantInfo = _.pick(
_.pick(rawInfo, relevantFields),
requestedFields);
return _.set(relevantInfo, "isbn", isbn);
}
static multipleBookInfo(isbns, fields) {
return _.map(function(isbn) {
return bookInfo(isbn, fields);
}, isbns);
}
}
Listing11.23 Extended search endpoint (database part)
var dbClient;
var dbSearchResultSchema = {
"type": "array",
"items": {
"type": "object",
"required": ["isbn", "available"],
"properties": {
"isbn": {"type": "string"},
"available": {"type": "boolean"}
}
}
};
class CatalogDB {
static matchingBooks(title) {
var matchingBooksQuery = `
SELECT isbn, available
FROM books
WHERE title = like '%$1%';
`;
var books = dbClient.query(catalogDB, matchingBooksQuery, [title]);
if(!ajv.validate(dbSearchResultSchema, books)) {
var errors = ajv.errorsText(ajv.errors);
throw "Internal error: Unexpected result from the database: "
+ errors;
}
return books;
}
}

## 페이지 270

242 CHAPTER 11 Web services
Listing11.24 Schema for the implementation of the extended search endpoint
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {
"type": [
"title",
"full_title",
"subtitle",
"publisher",
"publish_date",
"weight",
"physical_dimensions",
"number_of_pages",
"subjects",
"publishers",
"genre"
]
}
}
},
"required": ["title", "fields"]
};
var searchBooksResponseSchema = {
"type": "object",
"required": ["title", "isbn", "available"],
"properties": {
"title": {"type": "string"},
"available": {"type": "boolean"},
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
"isbn": {"type": "string"},
"publish_date": {"type": "string"},
"physical_dimensions": {"type": "string"}
}
};
Listing11.25 Schema for the extended search endpoint (combines the pieces)
class Catalog {
static enrichedSearchBooksByTitle(request) {

## 페이지 271

11.6 Search result enrichment in action 243
if(!ajv.validate(searchBooksRequestSchema, request)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid request:" + errors;
}
var title = _.get(request, "title");
var fields = _.get(request, "fields");
var dbBookInfos = CatalogDataSource.matchingBooks(title);
var isbns = _.map(dbBookInfos, "isbn");
var openLibBookInfos =
OpenLibraryDataSource.multipleBookInfo(isbns, fields);
var response = joinArrays(dbBookInfos, openLibBookInfos);
if(!ajv.validate(searchBooksResponseSchema, request)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid response:" + errors;
}
return response;
}
}
class Library {
static searchBooksByTitle(payloadBody) {
var payloadData = JSON.parse(payloadBody);
var results = Catalog.searchBooksByTitle(payloadData);
return JSON.stringify(results);
}
}
TIP Classes are much less complex when we use them as a means to aggregate state-
less functions that operate on similar domain entities.
Joe interrupts Theo’s meditation moment. After looking over the code in the previous list-
ings, he congratulates Theo.
Joe Excellent job, my friend! By the way, after reading The Power of Habit, I quit
chewing my nails.
Theo Wow! That’s terrific! Maybe I should read that book to overcome my habit of
drinking too much coffee.
Joe Thanks, and good luck with the coffee habit.
Theo I was supposed to call Nancy later today with an ETA for the Open Library
Book milestone. I wonder what her reaction will be when I tell her the feature
is ready.
Joe Maybe you should tell her it’ll be ready in a week, which would give you time to
begin work on the next milestone.

## 페이지 272

244 CHAPTER 11 Web services
Delivering on time
Joe was right! Theo recalls Joe’s story about the young woodcutter and the old man. Theo
was able to learn DOP and deliver the project on time! He’s pleased that he took the time
“to sharpen his saw and commit to a deeper level of practice.”
 NOTE If you are unable to recall the story or if you missed it, check out the opener
to part 2.
The Klafim project is a success. Nancy is pleased. Theo’s boss is satisfied. Theo got pro-
moted. What more can a person ask for?
Theo remembers his deal with Joe. As he strolls through the stores of the Westfield San
Francisco Center to look for a gift for each of Joe’s children, Neriah and Aurelia, he is
filled with a sense of purpose and great pleasure. He buys a DJI Mavic Air 2 drone for Ner-
iah, and the latest Apple Airpod Pros for Aurelia. He also takes this opportunity to buy a
necklace and a pair of earrings for his wife, Jane. It’s a way for him to thank her for having
endured his long days at work since the beginning of the Klafim project.
 NOTE The story continues in the opener of part 3.
Summary
 We build the insides of our systems like we build the outsides.
 Components inside a program communicate via data that is represented as
immutable data collections in the same way as components communicate via
data over the wire.
 In DOP, the inner components of a program are loosely coupled.
 Many parts of business logic can be implemented through generic data manipu-
lation functions. We use generic functions to
– Implement each step of the data flow inside a web service.
– Parse a request from a client.
– Apply business logic to the request.
– Fetch data from external sources (e.g., database and other web services).
– Apply business logic to the responses from external sources.
– Serialize response to the client.
 Classes are much less complex when we use them as a means to aggregate
together stateless functions that operate on similar domain entities.
Lodash functions introduced in this chapter
Function Description
keyBy(coll, f) Creates a map composed of keys generated from the results of running each ele-
ment of coll through f; the corresponding value for each key is the last element
responsible for generating the key.

