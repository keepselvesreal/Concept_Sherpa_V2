# A.1.2 Benefits of Principle #1

**페이지**: 347-348
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:28

---


--- 페이지 347 ---

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

--- 페이지 347 끝 ---


--- 페이지 348 ---

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

--- 페이지 348 끝 ---
