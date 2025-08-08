# A.0 Introduction (사용자 추가)

**페이지**: 345-346
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:27

---


--- 페이지 345 ---

15.2 Reproducibility with numbers and strings 317
Theo uses Dave’s laptop to examine Dave’s code. It returns true as expected, but it doesn’t
display to the console the text that Dave expected. He shares his surprise with Theo.
Listing15.5 Testing hasWordStartingWith
hasWordStartingWith("I like the word \"reproducibility\"", "li");
// It returns true
// It displays the following two lines:
// I like the word "reproducibility"
// li
Dave Where are the quotes around the strings? And where are the backslashes
before the quotes surrounding the word reproducibility?
Theo They disappeared!
Dave Why?
Theo When you print a string to the console, the content of the string is displayed
without quotes. It’s more human-readable.
Dave Bummer! That’s not good for reproducibility. So, after I copy and paste a
string I have to manually wrap it with quotes and backslashes.
Theo Fortunately, there is a simpler solution. If you serialize your string to JSON,
then it has the quotes and the backslashes. For instance, this code displays the
string you expected.
Listing15.6 Displaying to the console the serialization of a string
console.log(JSON.stringify(
"I like the word \"reproducibility\""));
// → "I like the word \"reproducibility\""
Dave I didn’t know that strings were considered valid JSON data. I thought only
objects and arrays were valid.
Theo Both compound data types and primitive data types are valid JSON data.
Dave Cool! I’ll fix the code in hasWordStartingWith that captures the string argu-
ments. Here you go.
Listing15.7 Capturing a context made of strings using JSON serialization
function hasWordStartingWith(sentence, prefix) {
console.log(JSON.stringify(sentence));
console.log(JSON.stringify(prefix));
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo Great! Capturing strings takes a bit more work than with numbers, but with
JSON they’re not too bad.
Dave Right. Now, I’m curious to see if using JSON serialization for context capturing
works well with numbers.

--- 페이지 345 끝 ---


--- 페이지 346 ---

318 CHAPTER 15 Debugging
Theo It works. In fact, it works well with any data, whether it’s a primitive data type or
a collection.
Dave Nice!
Theo Next, I’ll show you how to use this approach to reproduce a real scenario that
happens in the context of the Library Management System.
Dave No more digit arithmetic?
Theo No more!
15.3 Reproducibility with any data
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

--- 페이지 346 끝 ---
