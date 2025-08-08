# 11.5 Passing information forward

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