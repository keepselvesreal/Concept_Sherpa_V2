# 15.3 Reproducibility with any data

**메타데이터:**
- ID: 142
- 레벨: 2
- 페이지: 346-348
- 페이지 수: 3
- 부모 ID: 138
- 텍스트 길이: 5669 문자

---

lity with any data
The essence of DOP is that it treats data as a first-class citizen. As a consequence, we
can reproduce any scenario that deals with data with the same simplicity as we repro-
duce a scenario that deals with numbers and strings.
Dave I just called Nancy to tell her about the improved version of the book search,
where a prefix could match any word in the book title.
Theo And?
Dave She likes the idea.
Theo Great! Let’s use this feature as an opportunity to exercise reproducibility with
any data.
Dave Where should we start?
Theo First, we need to add context-capturing code inside the function that does the
book matching.
Dave The function is Catalog.searchBooksByTitle.
Theo What are the arguments of Catalog.searchBooksByTitle?
Dave It has two arguments: catalogData is a big nested hash map, and query is a
string.
Theo Can you edit the code and add the context-capturing piece?
Dave Sure. What about this code?
Listing15.8 Capturing the arguments of Catalog.searchBooksByTitle
Catalog.searchBooksByTitle = function(catalogData, query) {
console.log(JSON.stringify(catalogData));
console.log(JSON.stringify(query));
var allBooks = _.get(catalogData, "booksByIsbn");
var queryLowerCased = query.toLowerCase();
var matchingBooks = _.filter(allBooks, function(book) {
return _.get(book, "title")
.toLowerCase()
.startsWith(queryLowerCased);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
};

15.3 Reproducibility with any data 319
Theo Perfect. Now let’s trigger the search endpoint.
Theo triggers the search endpoint with the query “Watch,” hoping to get details about
Watchmen. When the endpoint returns, Theo opens the console and Dave can see two lines
of output.
Listing15.9 Console output when triggering the search endpoint
{"booksByIsbn":{"978-1982137274":{"isbn":"978-1982137274"\
,"title":"7 Habits of Highly Effective People","authorIds":\
["sean-covey","stephen-covey"]},"978-1779501127":{"isbn":\
"978-1779501127","title":"Watchmen","publicationYear":\
1987,"authorIds":["alan-moore", "dave-gibbons"]}},\
"authorsById":{"stephen-covey":{"name":"Stephen Covey",\
"bookIsbns":["978-1982137274"]},"sean-covey":{"name":"Sean Covey",\
"bookIsbns":["978-1982137274"]},"dave-gibbons":{"name":"Dave Gibbons",\
"bookIsbns":["978-1779501127"]},"alan-moore":{"name":"Alan Moore",\
"bookIsbns":["978-1779501127"]}}}
"Watch"
Dave I know that the first line contains the catalog data, but it’s really hard to read.
Theo That doesn’t matter too much. You only need to copy and paste it in order to
reproduce the Catalog.searchBooksByTitle call.
Dave Let me do that. Here.
Listing15.10 Reproducing a function call
var catalogData = {"booksByIsbn":{"978-1982137274":
{"isbn":"978-1982137274","title":"7 Habits of Highly Effective People",
"authorIds":["sean-covey","stephen-covey"]},"978-1779501127":
{"isbn":"978-1779501127","title":"Watchmen","publicationYear":1987,
"authorIds":["alan-moore","dave-gibbons"]}},"authorsById":
{"stephen-covey":{"name":"Stephen Covey","bookIsbns":
["978-1982137274"]},"sean-covey":{"name":"Sean Covey","bookIsbns":
["978-1982137274"]},"dave-gibbons":{"name":"Dave Gibbons","bookIsbns":
["978-1779501127"]},"alan-moore":{"name":"Alan Moore","bookIsbns":
["978-1779501127"]}}};
var query = "Watch";
Catalog.searchBooksByTitle(catalogData, query);
Theo Now that we have real catalog data in hand, we can do some interesting things
in the REPL.
Dave Like what?
Theo Like implementing the improved search feature without having to leave the
REPL.
TIP Reproducibility allows us to reproduce a scenario in a pristine environment.
Dave Without triggering the search endpoint?
Theo Exactly! We are going to improve our code until it works as desired, using the
short feedback loop that the console provides.

320 CHAPTER 15 Debugging
Dave Cool! In the catalog, we have the book, 7 Habits of Highly Effective People. Let’s
see what happens when we search books that match the word Habit.
Theo replaces the value of the query in listing 15.10 with "Habit". The code now
returns an empty array as in listing 15.11. This is expected because the current imple-
mentation only searches for books whose title starts with the query, whereas the title
starts with 7 Habits.
Listing15.11 Testing searchBooksByTitle
Catalog.searchBooksByTitle(catalogData, 'Habit');
// → []
Theo Would you like to implement the improved search?
Dave It’s not too hard; we have already implemented hasWordStartingWith. Here’s
the improved search.
Listing15.12 An improved version of book search
Catalog.searchBooksByTitle = function(catalogData, query) {
console.log(JSON.stringify(catalogData));
console.log(JSON.stringify(query));
var allBooks = _.get(catalogData, "booksByIsbn");
var matchingBooks = _.filter(allBooks, function(book) {
return hasWordStartingWith(_.get(book, "title"), query);
});
var bookInfos = _.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
};
Theo I like it. Let’s see if it works as expected.
Dave is about to trigger the search endpoint when suddenly Theo stops him. He says with
an authoritative tone:
Theo Dave, don’t do that!
Dave Don’t do what?
Theo Don’t trigger an endpoint to test your code.
Dave Why?
Theo Because the REPL environment gives you a much quicker feedback than trig-
gering the endpoint. The main benefit of reproducibility is to be able to repro-
duce the real-life conditions in a more effective environment.
Dave executes the code from his improved search with the word Habit. This time, however,
it returns the details about the book, 7 Habits of Highly Effective People.