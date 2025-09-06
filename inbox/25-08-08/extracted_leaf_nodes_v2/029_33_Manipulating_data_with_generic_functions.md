# 3.3 Manipulating data with generic functions

**메타데이터:**
- ID: 29
- 레벨: 2
- 페이지: 82-85
- 페이지 수: 4
- 부모 ID: 25
- 텍스트 길이: 7310 문자

---

g data with generic functions
Joe Now let me show you how to manipulate data in DOP with generic functions.
Theo Yes, I’m quite curious to see how you’ll implement the search functionality of
the Library Management System.
Joe OK. First, let’s instantiate a Catalog record for the catalog data of a library,
where we have a single book, Watchmen.
Joe instantiates a Catalog record according to Theo’s data model in figure 3.3. Here’s
what Joe shows to Theo.
Listing3.5 A Catalog record
var catalogData = {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore", "dave-gibbons"],
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
},
{
"id": "book-item-2",
"libId": "nyc-central-lib",
"isLent": false
}
]
}
},
"authorsById": {
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
},

3.3 Manipulating data with generic functions 55
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
}
Theo I see the two indexes we talked about, booksByIsbn and authorsById. How
do you differentiate a record from an index in DOP?
Joe In an entity diagram, there’s a clear distinction between records and indexes.
But in our code, both are plain data.
Theo I guess that’s why this approach is called data-oriented programming.
Joe See how straightforward it is to visualize any part of the system data inside a
program? The reason is that data is represented as data!
TIP In DOP, data is represented as data.
Theo That sounds like a lapalissade.1
Joe Oh, does it? I’m not so sure! In OOP, data is usually represented by objects,
which makes it more challenging to visualize data inside a program.
TIP In DOP, we can visualize any part of the system data.
Theo How would you retrieve the title of a specific book from the catalog data?
Joe Great question! In fact, in a DOP system, every piece of information has an
information path from which we can retrieve the information.
Theo Information path?
Joe For example, the information path to the title of the Watchmen book in the
catalog is ["booksByIsbn", "978-1779501127", "title"].
Theo Ah, I see. So, is an information path sort of like a file path, but that names in
an information path correspond to nested entities?
Joe You’re exactly right. And once we have the path of a piece of information, we
can retrieve the information with Lodash’s _.get function.
Joe types a few characters on Theo’s laptop. Theo is amazed at how little code is needed to
get the book title.
Listing3.6 Retrieving the title of a book from its information path
_.get(catalogData, ["booksByIsbn", "978-1779501127", "title"])
// → "Watchmen"
Theo Neat. I wonder how hard it would be to implement a function like _.get
myself.
1 A lapalissade is an obvious truth—a truism or tautology—that produces a comical effect.

56 CHAPTER 3 Basic data manipulation
After a few minutes of trial and error, Theo is able to produce his implementation. He
shows Joe the code.
Listing3.7 Custom implementation of get
function get(m, path) {
var res = m;
for(var i = 0; i < path.length; i++) {
We could use
var key = path[i];
forEach instead
res = res[key];
of a for loop.
}
return res;
}
After testing Theo’s implementation of get, Joe compliments Theo. He’s grateful that
Theo is catching on so quickly.
Listing3.8 Testing the custom implementation of get
get(catalogData, ["booksByIsbn", "978-1779501127", "title"]);
// → "Watchmen"
Joe Well done!
Theo I wonder if a function like _.get works smoothly in a statically-typed language
like Java?
Joe It depends on whether you only need to pass the value around or to access the
value concretely.
Theo I don’t follow.
Joe Imagine that once you get the title of a book, you want to convert the string
into an uppercase string. You need to do a static cast to String, right? Here,
let me show you an example that casts a field value to a string, then we can
manipulate it as a string.
Listing3.9 Casting a field value to a string
((String)watchmen.get("title")).toUpperCase()
Theo That makes sense. The values of the map are of different types, so the compiler
declares it as a Map<String,Object>. The information of the type of the field
is lost.
Joe It’s a bit annoying, but quite often our code just passes the data around. In that
case, we don’t have to deal with static casting. Moreover, in a language like C#,
when using the dynamic data type, type casting can be avoided.2,3
2 See http://mng.bz/4jo5 for the C# documentation on the built-in reference to dynamic types.
3 See appendix A for details about dynamic fields and type casting in C#.

3.3 Manipulating data with generic functions 57
TIP In statically-typed languages, we sometimes need to statically cast the field values.
Theo What about performance?
Joe In most programming languages, maps are quite efficient. Accessing a field
in a map is slightly slower than accessing a class member. Usually, it’s not
significant.
TIP There’s no significant performance hit for accessing a field in a map instead of as
a class member.
Theo Let’s get back to this idea of information path. It works in OOP too. I could
access the title of the Watchmen book with catalogData.booksByIsbn["978-
1779501127"].title. I’d use class members for record fields and strings for
index keys.
Joe There’s a fundamental difference, though. When records are represented as
maps, the information can be retrieved via its information path using a generic
function like _.get. But when records are represented as objects, you need to
write specific code for each type of information path.
Theo What do you mean by specific code? What’s specific in catalogData.books-
ByIsbn["978-1779501127"].title?
Joe In a statically-typed language like Java, you’d need to import the class defini-
tions for Catalog and Book.
Theo And, in a dynamically-typed language like JavaScript...?
Joe Even in JavaScript, when you represent records with objects instantiated from
classes, you can’t easily write a function that receives a path as an argument
and display the information that corresponds to this path. You would have to
write specific code for each kind of path. You’d access class members with dot
notation and map fields with bracket notation.
Theo Would you say that in DOP, the information path is a first-class citizen?
Joe Absolutely! The information path can be stored in a variable and passed as an
argument to a function.
TIP In DOP, you can retrieve every piece of information via a path and a generic
function.
Joe goes to the whiteboard. He draws a diagram like that in figure 3.5, which shows the
catalog data as a tree.
Joe You see, Theo, each piece of information is accessible via a path made of
strings and integers. For example, the path of Alan Moore’s first book is
["catalog", "authorsById", "alan-moore", "bookIsbns", 0].

58 CHAPTER 3 Basic data manipulation
catalog
booksByIsbn authorsById
978-1779501127 alan-moore
title isbn name
Watchmen 978-1779501127 Alan Moore
authorIds publicationYear bookIsbns
1987
1 0 0
bookItems
dave-gibbons alan-moore 978-1779501127
1 0 dave-gibbons
id id name
book-item-2 book-item-1 Dave Gibbons
libId libId bookIsbns
la-central-lib nyc-cental-lib
0
isLent isLent
978-1779501127
false true
Figure 3.5 The catalog data as a tree