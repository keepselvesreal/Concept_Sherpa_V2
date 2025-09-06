# 11.3 Representing a client request as a map

225
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