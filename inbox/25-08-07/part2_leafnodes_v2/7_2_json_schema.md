# 7.2 JSON Schema in a nutshell

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