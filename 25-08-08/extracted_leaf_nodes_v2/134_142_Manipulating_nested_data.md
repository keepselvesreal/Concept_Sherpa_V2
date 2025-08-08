# 14.2 Manipulating nested data

**메타데이터:**
- ID: 134
- 레벨: 2
- 페이지: 327-328
- 페이지 수: 2
- 부모 ID: 131
- 텍스트 길이: 3449 문자

---

g nested data 299
Theo Why don’t you see if it works with a simple case such as incrementing a number
in a map?
Dave Good idea! I’ll try multiplying a value in a map by 2 with update. How’s this
look?
Listing14.4 Multiplying a value in a map by 2
var m = {
"position": "manager",
"income": 100000
};
update(m, "income", function(x) {
return x * 2;
});
// → {"position": "manager", "income": 200000}
Theo Great! It seems to work.
14.2 Manipulating nested data
The next Monday, during Theo and Dave’s weekly sync meeting, they discuss the upcom-
ing features for Klafim. Theo fondly remembers another Monday where they met at Dave’s
family home in the country. Coming back to the present moment, Theo begins.
Theo Recently, Nancy has been asking for more and more administrative features.
Dave Like what?
Theo I’ll give you a few examples.... Let me find the email I got from Nancy yesterday.
Dave OK.
Theo Here it is. There are three feature requests for now: listing all the book author
IDs, calculating the book lending ratio, and grouping books by a physical library.
Dave What feature should I tackle first?
Theo It doesn’t matter, but you should deliver the three of these before the end of
the week. Good luck, and don’t hesitate to call me if you need help.
On Tuesday, Dave asks for Theo’s help. Dave is not pleased with how his code looks.
Dave I started to work on the three admin features, but I don’t like the code I wrote.
Let me show you the code for retrieving the list of author IDs from the list of
books returned from the database.
Theo Can you remind me what an element in a book list returned from the database
looks like?
Dave Each book is a map with an authorIds array field.
Theo OK, so it sounds like a map over the books should do it.
Dave This is what I did, but it doesn’t work as expected. Here’s my code for listing
the book author IDs.

300 CHAPTER 14 Advanced data manipulation
Listing14.5 Retrieving the author IDs in books as an array of arrays
function authorIdsInBooks(books) {
return _.map(books, "authorIds");
}
Theo What’s the problem?
Dave The problem is that it returns an array of arrays of author IDs instead of an
array of author IDs. For instance, when I run authorIdsInBooks on a catalog
with two books, I get this result.
Listing14.6 The author IDs in an array of arrays
[
["sean-covey", "stephen-covey"],
["alan-moore", "dave-gibbons"]
]
Theo That’s not a big problem. You can flatten an array of arrays with _.flatten,
and you should get the result you expect.
Dave Nice! This is exactly what I need! Give me a moment to fix the code of
authorIdsInBooks. . . here you go.
Listing14.7 Retrieving the author IDs in books as an array of strings
function authorIdsInBooks(books) {
return _.flatten(_.map(books, "authorIds"));
}
Theo Don’t you think that mapping and then flattening deserves a function of its own?
Dave Maybe. It’s quite easy to implement a flatMap function.2 How about this?
Listing14.8 The implementation of flatMap
function flatMap(coll, f) {
return _.flatten(_.map(coll,f));
}
Theo Nice!
Dave I don’t know.... It’s kind of weird to have such a small function.
Theo I don’t think that code size is what matters here.
Dave What do you mean?
Theo See what happens when you rewrite authorIdsInBooks using flatMap.
Dave OK, here’s how I’d use flatMap to list the author IDs.
2 Lodash provides an implementation of flatMap, but for the sake of teaching, we are writing our own
implementation.