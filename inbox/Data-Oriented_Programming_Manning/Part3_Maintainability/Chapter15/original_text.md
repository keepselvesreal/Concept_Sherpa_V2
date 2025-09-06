# Chapter 15: Debugging

**부제목:** Innovation at the museum
**계획된 페이지:** 339-380
**실제 페이지:** 339-380

=== PAGE 339 ===
Debugging
Innovation at the museum
This chapter covers
 Reproducing a bug in code that involves
primitive data types
 Reproducing a bug in code that involves
aggregated data
 Replaying a scenario in the REPL
 Creating unit tests from bugs
When our programs don’t behave as expected, we need to investigate the source
code. The traditional tool for code investigation is the debugger. The debugger
allows us to run the code, step by step, until we find the line that causes the bug.
However, a debugger doesn’t allow us to reproduce the scenario that causes the
problem.
In DOP, we can capture the context of a scenario that causes a bug and replay
it in a separate process like a REPL or a unit test. This allows us to benefit from a
short feedback loop between our attempt to fix the code and the results of our
attempt.
311

=== PAGE 340 ===
312 CHAPTER 15 Debugging
15.1 Determinism in programming
After a few months, Theo calls Dave to tell him that he’s leaving Albatross. After Dave
recovers from this first surprise, he’s given another, more pleasant one. Theo informs Dave
that after consulting with the management team, they have decided that Dave will be in
charge of DOP at Albatross. In addition to the farewell at the office next week, Theo invites
Dave for a last one-on-one work session at the Exploratorium Museum of Science.
During their visit, Dave particularly enjoys the Cells to Self exhibit in the Living Systems
gallery; meanwhile, Theo is having fun with the Colored Shadows exhibit in the Reflec-
tions gallery. After the visit, Theo and Dave settle in the back row of the museum’s audito-
rium and open their laptops.
Dave Why did you want our last meeting to happen here at the Museum of Science?
Theo Remember when Joe told us that someday we’d be able to innovate in DOP?
Dave Yes.
Theo Well, that day may have come. I think I have discovered an interesting connec-
tion between DOP and science, and it has implications in the way we debug a
program.
Dave I’m curious.
Theo Do you believe in determinism?
Dave You mean that everything that happens in the universe is predestined and that
free will is an illusion?
Theo No, I don’t want to get into a philosophy. This is more of a scientific question.
Do you think that the same causes always produce the same effects?
Dave I think so. Otherwise, each time I use an elevator, I’d be scared to death that
the laws of physics have changed, and the elevator might go down instead of
up, or even crash!
Theo What about determinism in programming?
Dave How would you define causes and effects in programming?
Theo Let’s say, for the sake of simplicity, that in the context of programming, causes
are function arguments and effects are return values.
Dave What about side effects?
Theo Let’s leave them aside for now.
Dave What about the program state? I mean, a function could return a different
value for the same arguments if the program state changes.
Theo That’s why we should avoid state as much as possible.
Dave But you can’t avoid state in real-life applications!
Theo Right, but we can minimize the number of modules that deal with state. In fact,
that’s exactly what DOP has encouraged us to do: only the SystemState mod-
ule deals with state, and all other modules deal with immutable data.
Dave Then, I think that in modules that deal with immutable data, determinism as
you defined it holds. For the same arguments, a function will always return the
same value.
TIP In modules that deal with immutable data, function behavior is deterministic—the
same arguments always lead to the same return values.

=== PAGE 341 ===
15.1 Determinism in programming 313
Theo Perfect. Let’s give a name to the values of the function arguments that a function
is called with: the function run-time context or, in short, the function context.
Dave I think I see what you mean. In general, the function context should involve
both the function arguments and the program state. But in DOP, because we
deal with immutable data, a function context is made only of the values of the
function arguments.
TIP In DOP, the function context is made of the values of the function arguments.
Theo Exactly! Now, let’s talk about reproducibility. Let’s say that you want to capture
a function context and reproduce it in another environment.
Dave Could you be a bit more concrete about reproducing a function context in
another environment?
Theo Take, for example, a web service endpoint. You trigger the endpoint with some
parameters. Inside the program, down the stack, a function foo is called. Now,
you want to capture the context in which foo is called in order to reproduce
later the same behavior of foo.
Dave We deal with immutable data. So, if we call foo again with the same arguments,
it will behave the same.
Theo The problem is how do you know the values of the function arguments?
Remember that we didn’t trigger foo directly. We triggered the endpoint.
Dave That’s not a problem. You use a debugger and set a breakpoint inside the code of
foo, and you inspect the arguments when the program stops at the breakpoint.
Theo Let’s say foo receives three arguments: a number, a string, and a huge nested map.
How do you capture the arguments and replay foo with the same arguments?
Dave I am not sure what you mean exactly by replaying foo?
Theo I mean executing foo in the REPL.
 NOTE The REPL (Read Eval Print Loop), sometimes called language shell, is a pro-
gramming environment that takes pieces of code, executes them, and displays the
result. See table 15.1 for a list of REPLs for different programming languages.
Table 15.1 REPLs per programming language
JavaScript (Browser) Browser console
Node.js Node CLI
Java JShell
C# C# REPL
Python Python interpreter
Ruby Interactive Ruby
Dave Does the REPL have to be part of the process that I’m debugging?
Theo It doesn’t have to be. Think of the REPL as a scientific lab, where developers
perform experiments. Let’s say you’re using a separate process for the REPL.

=== PAGE 342 ===
314 CHAPTER 15 Debugging
Dave OK. For the number and the string, I can simply copy their values to the clip-
board, paste them to the REPL, and execute foo in the REPL with the same
arguments.
Theo That’s the easy part. What about the nested map?
Dave I don’t know. I don’t think I can copy a nested map from a debugger to the
clipboard!
Theo In fact, JavaScript debuggers can. For instance, in Chrome, there is a Copy
option that appears when you right-click on data that is displayed in the browser
console.
Dave I never noticed it.
Theo Even without that, you could serialize the nested map to a JSON string, copy
the string to the clipboard, and then paste the JSON string to the REPL.
Finally, you could deserialize the string into a hash map and call foo with it.
Dave Nice trick!
Theo I don’t think of it as a trick, but rather as a fundamental aspect of DOP: data is
represented with generic data structures.
Dave I see. It’s easy to serialize a generic data structure.
TIP In order to copy and paste a generic data structure, we serialize and deserialize it.
Theo You just discovered the two conditions for reproducibility in programming.
Dave The first one is that data should be immutable.
Theo Right, and the second one?
Dave It should be easy to serialize and deserialize any data.
TIP The two conditions for reproducibility in programming are immutability and
ease of (de)serialization.
15.2 Reproducibility with numbers and strings
Theo In fact, we don’t even need a debugger in order to capture a function context.
Dave But the function context is basically made of its arguments. How can you
inspect the arguments of a function without a debugger?
Theo By modifying the code of the function under investigation and printing the
serialization of the arguments to the console.
Dave I don’t get that.
Theo Let me show you what I mean with a function that deals with numbers.
Dave OK.
Theo Take for instance a function that returns the nth digit of a number.
Dave Oh no, I hate digit arithmetic!
Theo Don’t worry, we’ll find some code for it on the web.
Theo googles “nth digit of a number in JavaScript” and takes a piece of code from Stack-
Overflow that seems to work.

=== PAGE 343 ===
15.2 Reproducibility with numbers and strings 315
Listing15.1 Calculate the nth digit of a number
function nthDigit(a, n) {
return Math.floor((a / (Math.pow(10, n - 1)))) % 10;
}
Dave Do you understand how it works?
Theo Let’s see, dividing a by 10n–1 is like right-shifting it n–1 places. Then we need to
get the rightmost digit.
Dave And the last digit of a number is obtained by the modulo 10 operation?
Theo Right! Now, imagine that this function is called down the stack when some
endpoint is triggered. I’m going to modify it by adding context-capturing code.
Dave What’s that?
Theo Context-capturing code is code that we insert at the beginning of a function
body to print the values of the arguments. Let me edit the nthDigit code to
give you an example.
Listing15.2 Capturing a context made of numbers
function nthDigit(a, n) {
console.log(a);
console.log(n);
return Math.floor((a / (Math.pow(10, n - 1)))) % 10;
}
Dave It looks trivial.
Theo It is trivial for now, but it will get less trivial in a moment. Now, tell me what
happens when I trigger the endpoint.
Dave When the endpoint is triggered, the program will display the two numbers, a
and n, in the console.
Theo Exactly, and what would you have to do in order to replay the function in the
same context as when the endpoint was triggered?
Dave I would need to copy the values of a and n from the console, paste them into
the REPL, and call nthDigit with those two values.
Theo What makes you confident that when we run nthDigit in the REPL, it will
reproduce exactly what happened when the endpoint was triggered? Remem-
ber, the REPL might run in a separate process.
Dave I know that nthDigit depends only on its arguments.
Theo Good. Now, how can you be sure that the arguments you pass are the same as
the arguments that were passed?
Dave A number is a number!
Theo I agree with you. Let’s move on and see what happens with strings.
Dave I expect it to be exactly the same.
Theo It’s going to be almost the same. Let’s write a function that receives a sentence
and a prefix and returns true when the sentence contains a word that starts
with the prefix.

=== PAGE 344 ===
316 CHAPTER 15 Debugging
Dave Why would anyone ever need such a weird function?
Theo It could be useful for the Library Management System when a user wants to
find books whose title contains a prefix.
Dave Interesting. I’ll talk about that with Nancy. Anyway, coding such a function
seems quite obvious. I need to split the sentence string into an array of words
and then check whether a word in the array starts with the prefix.
Theo How are you going to check whether any element of the array satisfies the
condition?
Dave I think I’ll use Lodash filter and check the length of the returned array.
Theo That would work but it might have a performance issue.
Dave Why?
Theo Think about it for a minute.
Dave I got it! filter processes all the elements in the array rather than stopping
after the first match. Is there a function in Lodash that stops after the first
match?
Theo Yes, it’s called find.
Dave Cool. I’ll use that. Hang on.
Dave reaches over for his laptop and write the code to check whether a sentence contains a
word that starts with a prefix. After a brief period, he shows Theo his implementation of
hasWordStartingWith using _.find.
Listing15.3 Checking if a sentence contains a word starting with a prefix
function hasWordStartingWith(sentence, prefix) {
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo OK, now, please add the context-capturing code at the beginning of the function.
Dave Sure, let me edit this code a bit. Voilà!
Listing15.4 Capturing a context made of strings
function hasWordStartingWith(sentence, prefix) {
console.log(sentence);
console.log(prefix);
var words = sentence.split(" ");
return _.find(words, function(word) {
return word.startsWith(prefix);
}) != null;
}
Theo Let me inspect your code for a minute. I want to see what happens when I
check whether the sentence “I like the word reproducibility” contains a word that
starts with li.

=== PAGE 345 ===
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

=== PAGE 346 ===
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

=== PAGE 347 ===
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

=== PAGE 348 ===
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

=== PAGE 349 ===
15.4 Unit tests 321
Listing15.13 Testing searchBooksByTitle again
Catalog.searchBooksByTitle(catalogData, 'Habit');
// → [ { "title": "7 Habits of Highly Effective People", …}]
Dave It works!
Theo Let’s try more queries: abit and bit should not return any book, but habit
and 7 Habits should return only one book.
In the REPL, Dave tries the four queries that Theo suggested. For abit and bit, the code
works as expected, but for habit and 7 Habits it fails.
Dave Let me try to fix that code.
Theo I suggest that you instead write a couple of unit tests that check the various inputs.
Dave Good idea. Is there a way to use reproducibility in the context of unit tests?
Theo Absolutely!
15.4 Unit tests
Dave How do we use reproducibility in a unit test?
Theo As Joe told showed me so many times, in DOP, unit tests are really simple. They
call a function with some data, and they check that the data returned by the
function is the same as we expect.
Dave I remember that! I have written many unit tests for the Library Management
System following this approach. But sometimes, I struggled to provide input
data for the functions under test. For instance, building catalog data with all its
nested fields was not a pleasure.
Theo Here’s where reproducibility can help. Instead of building data manually, you
put the system under the conditions you’d like to test, and then capture data
inside the function under test. Once data is captured, you use it in your unit test.
Dave Nice! Let me write a unit test for Catalog.searchBooksByTitle following
this approach.
Dave triggers the search endpoint once again. Then, he opens the console and copies the
line with the captured catalog data to the clipboard. Finally, he pastes it inside the code of
the unit test.
Listing15.14 A unit test with captured data
var catalogData =
{"booksByIsbn":{"978-1982137274":{"isbn":"978-1982137274",
"title":"7 Habits of Highly Effective People","authorIds":["sean-covey",
"stephen-covey"]},"978-1779501127":{"isbn":"978-1779501127","title":
"Watchmen","publicationYear":1987,"authorIds":["alan-moore",
"dave-gibbons"]}},"authorsById":{"stephen-covey":{"name":
"Stephen Covey","bookIsbns":["978-1982137274"]},"sean-covey":
{"name":"Sean Covey","bookIsbns":["978-1982137274"]},"dave-gibbons":
{"name":"Dave Gibbons","bookIsbns":["978-1779501127"]},"alan-moore":
{"name":"Alan Moore","bookIsbns":["978-1779501127"]}}};
var query = "Habit";

=== PAGE 350 ===
322 CHAPTER 15 Debugging
var result = Catalog.searchBooksByTitle(catalogData, query);
var expectedResult = [
{
"authorNames": [
"Sean Covey",
"Stephen Covey",
],
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
}
];
_.isEqual(result, expectedResult);
// → true
Theo Well done! Now, would you like me to show you how to do the same without
copying and pasting?
Dave Definitely.
Theo Instead of displaying the captured data to the console, we’re going to write it to
a file and read data from that file inside the unit test.
Dave Where are you going to save the files that store captured data?
Theo Those files are part of the unit tests. They need to be under the same file tree
as the unit tests.
Dave There are so many files! How do we make sure a file doesn’t override an exist-
ing file?
Theo By following a simple file-naming convention. A name for a file that stores cap-
tured data is made of two parts: a context (for example, the name of the func-
tion where data was captured) and a universal unique identifier (a UUID).
Dave How do you generate a UUID?
Theo In some languages it’s part of the language, but in other languages like Java-
Script, you need a third-party library like uuid. Let me bookmark its site for you.
I also happen to have a list of libraries for UUIDs. I’ll send that table to you too.
Theo bookmarks the site for the third-party library uuid (https://github.com/uuidjs/
uuid) on Dave’s computer. Then, using his laptop, he finds his list and sends that to Dave.
Dave receives the email, and he takes a moment to quickly glance through the table 15.2
before turning his attention back to Theo.
Table 15.2 Libraries for UUID generation
Language UUID library
JavaScript https://github.com/uuidjs/uuid
Java java.util.UUID
C# Guid.NewGuid
Python uuid
Ruby SecureRandom

=== PAGE 351 ===
15.4 Unit tests 323
Theo The code for the dataFilePath function that receives a context and returns a
file path is fairly simple. Check this out.
Listing15.15 Computing the file path for storing captured data
var capturedDataFolder = "test-data";
The root folder
function dataFilePath(context) {
for captured data
var uuid = generateUUID();
return capturedDataFolder
UUID generation is language-
+ "/" + context
dependent (see table 15.2).
+ "-" + ".json";
}
Uses json as a file extension
because we serialize data to JSON
Dave How do we store a piece of data in a JSON file?
Theo We serialize it and write it to disk.
Dave Synchronously or asynchronously?
Theo I prefer to write to the disk asynchronously or in a separate thread in run times
that support multithreading to avoid slowing down the real work. Here’s my
implementation of dumpData.
Listing15.16 Dumping data in JSON format
function dumpData(data, context) {
var path = dataFilePath(context); Writes asynchronously
to prevent blocking
var content = JSON.stringify(data);
the real work
fs.writeFile(path, content, function () {
The third argument is a
console.log("Data for " +
callback function, called
context +
when write completes.
"stored in: " +
path);
Displays a message once
});
data is written to the file
}
Dave Let me see if I can use dumpData inside Catalog.searchBooksByTitle and
capture the context to a file. I think that something like this should work.
Listing15.17 Capturing the context into a file
Catalog.searchBooksByTitle = function(catalogData, query) {
dumpData([catalogData, query], 'searchBooksByTitle');
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

=== PAGE 352 ===
324 CHAPTER 15 Debugging
return bookInfos;
};
Theo Trigger the endpoint to see if it works.
Dave triggers the search endpoint once again and views the output in the console. When he
opens the file mentioned in the log message, he sees a single line that is hard to decipher.
Listing15.18 Console output when triggering the search endpoint
Data for searchBooksByTitle stored in
test-data/searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json
Listing15.19 The content of the JSON file that captured the context
[{"booksByIsbn":{"978-1982137274":{"isbn":"978-1982137274",
"title":"7 Habits of Highly Effective People","authorIds":
["sean-covey","stephen-covey"]},"978-1779501127":{"isbn":
"978-1779501127","title":"Watchmen","publicationYear":1987,
"authorIds":["alan-moore","dave-gibbons"]}},"authorsById":
{"stephen-covey":{"name":"Stephen Covey","bookIsbns":
["978-1982137274"]},"sean-covey":{"name":"Sean Covey",
"bookIsbns":["978-1982137274"]},"dave-gibbons":
{"name":"Dave Gibbons","bookIsbns":["978-1779501127"]},
"alan-moore":{"name":"Alan Moore","bookIsbns":
["978-1779501127"]}}},"Habit"]
Dave Reading this JSON file is very difficult!
Theo We can beautify the JSON string if you want.
Dave How?
Theo By passing to JSON.stringify the number of space characters to use for
indentation. How many characters would you like to use for indentation?
Dave Two.
After adding the number of indentation characters to the code of dumpData, Dave then
opens the JSON file mentioned in the log message (it’s a different file name!). He now
sees a beautiful JSON array with two elements.
Listing15.20 Dumping data in JSON format with indentation
The second argument to
function dumpData(data, context) {
JSON.stringify is ignored.
var path = dataFilePath(context);
The third argument to
var content = JSON.stringify(data, null, 2);
JSON.stringify specifies the
number of characters to
use for indentation.
fs.writeFile(path, content, function () {
console.log("Data for " + context + "stored in: " + path);
});
}

=== PAGE 353 ===
15.4 Unit tests 325
Listing15.21 The captured context with indentation in the JSON file
[
{
"booksByIsbn": {
"978-1982137274": {
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"authorIds": [
"sean-covey",
"stephen-covey"
]
},
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": [
"alan-moore",
"dave-gibbons"
]
}
},
"authorsById": {
"stephen-covey": {
"name": "Stephen Covey",
"bookIsbns": [
"978-1982137274"
]
},
"sean-covey": {
"name": "Sean Covey",
"bookIsbns": [
"978-1982137274"
]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": [
"978-1779501127"
]
},
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": [
"978-1779501127"
]
}
}
},
"Habit"
]

=== PAGE 354 ===
326 CHAPTER 15 Debugging
Dave While looking at the contents of the JSON file, I thought about the fact that we
write data to the file in an asynchronous way. It means that data is written con-
currently to the execution of the function code, right?
Theo Right! As I told you, we don’t want to slow down the real work.
Dave I get that. What happens if the code of the function modifies the data that we
are writing? Will we write the original data to the file or the modified data?
Theo I’ll let you think about that while I get a cup of tea at the museum coffee shop.
Would you like some coffee?
Dave What, you’re not having coffee?
Theo I finally found the time to read the book The Power of Habit by Charles Duhigg.
Joe read the book and quit biting his fingernails, so I decided to read it to cut
down on my habit of going for yet another cup of coffee.
Dave That’s impressive, but I’d like an espresso, please.
While Theo goes to the coffee shop, Dave explores the Wind Arrows exhibit outside the
auditorium. He’s hoping that his mind will be inspired by the beauty of science. He takes a
few breaths to relax, and after a couple of minutes, Dave has an Aha! moment. He knows
the answer to his question about the function changing data.
Theo comes back, gingerly carrying the hot beverages, and finds Dave in the audito-
rium. Dave smiles at Theo and says:
Dave In DOP, we never mutate data. Therefore, my question is no longer a ques-
tion: the code of the function cannot modify the data while we are writing it
to the file.
Theo You’ve got it! Now, let me show you how to use data from the JSON file in a
unit test. First, we need a function that reads data from a JSON file and deseri-
alizes it, probably something like readData.
Listing15.22 Reading data from a JSON file
function readData(path) {
return JSON.parse(fs.readFileSync(path));
}
Dave Why are you reading synchronously and not asynchronously like you did when
we captured the data?
Theo Because readData is meant to be used inside a unit test, and we cannot run
the test before the data is read from the file.
Dave That makes sense. Using readData inside a unit test seems straightforward. Let
me use it to read our captured data.
Listing15.23 A unit test that reads captured data from a file
var data = readData("test-data/" +
"searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json");
var catalogData = data[0];
var query = data[1];

=== PAGE 355 ===
15.4 Unit tests 327
var result = Catalog.searchBooksByTitle(catalogData, query);
var expectedResult = [
{
"authorNames": [
"Sean Covey",
"Stephen Covey",
],
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
}
];
_.isEqual(result, expectedResult);
// → false
Theo Do you prefer the version of the unit test with the inline data or with the data
read from the file?
Dave It depends. When data is minimal, I prefer to have the data inline because it
allows me to see the data. But when data is substantial, like the catalog data,
having the data inline makes the code hard to read.
Theo OK. Let’s fix the code of the improved search so that it works with the two que-
ries that return an empty result.
Dave I completely forgot about that. Do you remember those two queries?
Theo Yes, it was habit and 7 Habits.
Dave The first query doesn’t work because the code leaves the strings in their origi-
nal case. I can easily fix that by converting both the book title and the query to
lowercase.
Theo And what about the second query?
Dave It’s much harder to deal with because it’s made of two words. I somehow need
to check whether the title subsequently contains those two prefixes.
Theo Are you familiar with the \b regular expression metacharacter?
Dave No.
Theo \b matches a position that is called a word boundary. It allows us to perform pre-
fix matching.
Dave Cool. Can you give me an example?
Theo Sure. For instance, \bHabits and \b7 Habits match 7 Habits of Highly
Effective People, but abits won’t match.
Dave What about \bHabits of?
Theo It also matches.
Dave Excellent. This is exactly what I need! Let me fix the code of hasWordStart-
ingWith so that it does a case-insensitive prefix match.
Listing15.24 A revised version of hasWordStartingWith
function hasWordStartingWith(sentence, prefix) {
var sentenceLowerCase = sentence.toLowerCase();
var prefixLowerCase = prefix.toLowerCase();

=== PAGE 356 ===
328 CHAPTER 15 Debugging
var prefixRegExp = new RegExp("\\b" +
When passing \b to the
prefixLowerCase);
RegExp constructor, we
return sentenceLowerCase.match(prefixRegExp) != null; need an extra backslash.
}
Theo Now, let me write unit tests for all the cases.
Dave One test per query?
Theo You could, but it’s more efficient to have a unit test for all the queries that
should return a book and another one for all the queries that should return no
books. Give me a minute.
Theo codes for a while and produces two unit tests. He then shows the tests to Dave and
enjoys another sip of his tea.
Listing15.25 A unit test for several queries that should return a book
var data =
readData("test-data/" +
"searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json");
var catalogData = data[0];
var queries = ["Habit", "habit", "7 Habit", "habits of"];
var expectedResult = [
{
"authorNames": [
"Sean Covey",
"Stephen Covey",
],
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
}
];
_.every(queries, function(query) {
var result = Catalog.searchBooksByTitle(catalogData, query);
return _.isEqual(result, expectedResult);
});
// → [true, true, true, true]
Listing15.26 A unit test for several queries that should return no book
var data =
readData("test-data/" +
"searchBooksByTitle-68e57c85-2213-471a-8442-c4516e83d786.json");
var catalogData = data[0];
var queries = ["abit", "bit", "7 abit", "habit of"];
var expectedResult = [ ];
_.every(queries, function(query) {
var result = Catalog.searchBooksByTitle(catalogData, query);
return _.isEqual(result, expectedResult);
});
// → [true, true, true, true]

=== PAGE 357 ===
15.5 Dealing with external data sources 329
Dave What is _.every?
Theo It’s a Lodash function that receives a collection and a predicate and returns
true if the predicate returns true for every element of the collection.
Dave Nice!
Dave runs the unit tests and they pass. He then enjoys a sip of his espresso.
Dave Now, am I allowed to trigger the search endpoint with 7 Habit in order to con-
firm that the improved search works as expected?
Theo Of course. It’s only during the multiple iterations of code improvements that I
advise you not to trigger the system from the outside in order to benefit from a
shorter feedback loop. Once you’re done with the debugging and fixing, you
must then test the system from end to end.
Dave triggers the search endpoint with 7 Habit. It returns the details about 7 Habits of
Highly Effective People as expected.
15.5 Dealing with external data sources
Dave Can we also use reproducibility when the code involves fetching data from an
external data source like a database or an external service?
Theo Why not?
Dave The function context might be exactly the same, but the behavior might be dif-
ferent if the function fetches data from a data source that returns a different
response for the same query.
Theo Well, it depends on the data source. Some databases are immutable in the
sense that the same query always returns the same response.
Dave I have never heard about immutable databases.
Theo Sometimes, they are called functional databases or append-only databases.
Dave Never heard about them either. Did you mean read-only databases?
Theo Read-only databases are immutable for sure, but they are not useful for storing
the state of an application.
Dave How could a database be both writable and immutable?
Theo By embracing time.
Dave What does time have to do with immutability?
Theo In an immutable database, a record has an automatically generated timestamp,
and instead of updating a record, we create a new version of it with a new time-
stamp. Moreover, a query always has a time range in addition to the query
parameters.
Dave Why does that guarantee that the same query will always return the same
response?
Theo In an immutable database, queries don’t operate on the database itself. Instead,
they operate on a database snapshot, which never changes. Therefore, queries
with the same parameters are guaranteed to return the same response.

=== PAGE 358 ===
330 CHAPTER 15 Debugging
Dave Are there databases like that for real?
Theo Yes. For instance, the Datomic immutable database is used by some digital
banks.
 NOTE See https://www.datomic.com for more information on the Datomic transac-
tional database.
Dave But most databases don’t provide such a guarantee!
Theo Right, but in practice, when we’re debugging an issue in our local environ-
ment, data usually doesn’t change.
Dave What do you mean?
Theo Take, for instance, Klafim’s database. In theory, between the time you trigger
the search endpoint and the time you replay the search code from the REPL
with the same context, a book might have been borrowed, and its availability
state in the database has changed. This leads to a difference response to the
search query.
Dave Exactly.
Theo But in practice, you are the only one that interacts with the system in your local
environment. Therefore, it should not happen.
Dave I see. Because we are at the Museum of Science, would you allow me an anal-
ogy with science?
Theo Of course!
Dave In a sense, external data sources are like hidden variables in quantum physics.
In theory, they can alter the result of an experiment for no obvious reason. But
in practice, our physical world looks stable at the macro level.
With today’s discussion at an end, Theo searches his bag to find a parcel wrapped with gift
wrap from the museum’s souvenir shop, which he hands to Dave with a smile. Dave opens
the gift to find a T-shirt. On one side there is an Albert Einstein avatar and his famous
quote: “God does not play dice with the universe”; on the other side, an avatar of Alan Kay
and his quote: “The last thing you want to do is to mess with internal state.”
Dave thanks Theo for his gift. Theo can feel a touch of emotion at the back of his
throat. He’s really enjoyed playing the role of mentor with Dave, a rather skilled student.
Farewell
A week after the meeting with Dave at the museum, Theo invites Joe and Nancy for his
farewell party at Albatross. This is the first time that Joe meets Nancy, and Theo takes the
opportunity to tell Nancy that if the Klafim project met its deadlines, it was thanks to Joe.
Everyone is curious about the name of the company Theo is going to work for, but no one
dares to ask him. Finally, it’s Dave who gets up the courage to ask.
Dave May I ask you what company are you going to work for?
Theo I’m going to take a break.

=== PAGE 359 ===
Summary 331
Dave Really?
Theo Yes. I’ll be traveling around the world for a couple of months.
Dave And after that, will you go back to work in programming?
Theo I’m not sure.
Dave Do you have other projects in mind?
Theo I’m thinking of writing a book.
Dave A book?
Theo Yes. DOP has been a meaningful journey for me. I have learned some interest-
ing lessons about reducing complexity in programming, and I would like to
share my story with the community of developers.
Dave Well, if you are as good of a storyteller as you are as a teacher, I am sure your
book will be a success.
Theo Thank you, Dave!
Monica, Dave, Nancy, Joe, and all the other Albatross employees raise their glasses to
Theo’s health and exclaim together, “Cheers! Here’s to a successful book.”
Summary
 We reproduce a scenario by capturing the context in which a function is called
and replaying it either in the REPL or in a unit test. In this chapter, we call it
context capturing.
 In DOP, a function context is made only of data.
 There are various locations to capture a function context—the clipboard, the
console, a file.
 We are able to capture a function’s context because data is represented with a
generic data structure and, therefore, it is easily serializable.
 Replaying a scenario in the REPL provides a short feedback loop that allows us
to be effective when we want to fix our code.
 When we execute a function with a captured context, the behavior of the func-
tion is guaranteed to be the same as long as it only manipulates immutable data
as specified by DOP.
 In modules that deal with immutable data, function behavior is deterministic—
the same arguments always lead to the same return values.
 The function context is made of the values of the function arguments.
 The REPL (Read Eval Print Loop), sometimes called language shell, is a pro-
gramming environment that takes pieces of code, executes them, and displays
the result.
 In order to copy and paste a generic data structure, we serialize and deserialize it.

=== PAGE 360 ===
332 CHAPTER 15 Debugging
 Reproducibility allows us to reproduce a scenario in a pristine environment.
 The two conditions for reproducibility in programming are immutability and
ease of (de)serialization.
Lodash functions introduced in this chapter
Function Description
find(coll, pred) Iterates over elements of coll, returning the first element for which pred
returns true

=== PAGE 361 ===
appendix A
Principles of data-oriented
programming
Data-oriented programming (DOP) is a programming paradigm aimed at simplify-
ing the design and implementation of software systems, where information is at the
center in systems such as frontend or backend web applications and web services,
for example. Instead of designing information systems around software constructs
that combine code and data (e.g., objects instantiated from classes), DOP encour-
ages the separation of code from data. Moreover, DOP provides guidelines about
how to represent and manipulate data.
TIP In DOP, data is treated as a first-class citizen.
The essence of DOP is that it treats data as a first-class citizen. It gives developers
the ability to manipulate data inside a program with the same simplicity as they
manipulate numbers or strings. Treating data as a first-class citizen is made possible
by adhering to four core principles:
 Separating code (behavior) from data.
 Representing data with generic data structures.
 Treating data as immutable.
 Separating data schema from data representation.
When these four principles are combined, they form a cohesive whole as figure A.1
shows. Systems built using DOP are simpler and easier to understand, so the devel-
oper experience is significantly improved.
TIP In a data-oriented system, code is separated from data. Data is represented
with generic data structures that are immutable and have a separate schema.
333

=== PAGE 362 ===
334 APPENDIX A Principles of data-oriented programming
Principle #2: Represent Immutable
data with generic data
structures.
Generic
Mutable
Representation
Principle #3:
Specific
Data is
Data immutable.
Schema
Principle #4: Separate
data schema from data
Data-oriented
representation.
programming
Functional
Code
Principle #1: programming
Separate code
from data.
Object-oriented
programming
Figure A.1 The principles of DOP
Notice that DOP principles are language-agnostic. They can be adhered to (or bro-
ken) in
 Object-oriented programming (OOP) languages such as Java, C#, C++, etc.
 Functional programming (FP) languages such as Clojure, OCaml, Haskell, etc.
 Languages that support both OOP and FP such as JavaScript, Python, Ruby,
Scala, etc.
TIP DOP principles are language-agnostic.
 NOTE For OOP developers, the transition to DOP might require more of a mind
shift than for FP developers because DOP prohibits the encapsulation of data in state-
ful classes.
This appendix succinctly illustrates how these principles can be applied or broken in
JavaScript. Mentioned briefly are the benefits of adherence to each principle, and the
costs paid to enjoy those benefits. This appendix also illustrates the principles of DOP
via simple code snippets. Throughout the book, the application of DOP principles to
production information systems is explored in depth.

=== PAGE 363 ===
A.1 Principle #1: Separate code from data 335
A.1 Principle #1: Separate code from data
Principle #1 is a design principle that recommends a clear separation between code
(behavior) and data. This may appear to be a FP principle, but in fact, one can adhere
to it or break it either in FP or in OOP:
 Adherence to this principle in OOP means aggregating the code as methods of
a static class.
 Breaking this principle in FP means hiding state in the lexical scope of a function.
Also, this principle does not relate to the way data is represented. Data representation
is addressed by Principle #2.
PRINCIPLE #1 Separate code from data in a way that the code resides in functions
whose behavior does not depend on data that is encapsulated in the function’s
context.
A.1.1 Illustration of Principle #1
Our exploration of Principle #1 begins by illustrating how it can be applied to OOP
and FP. The following sections illustrate how this principle can be adhered to or bro-
ken in a simple program that deals with:
 An author entity with a firstName, a lastName, and the number of books they
wrote.
 A piece of code that calculates the full name of the author.
 A piece of code that determines if an author is prolific, based on the number of
books they wrote.
BREAKING PRINCIPLE #1 IN OOP
Breaking Principle #1 in OOP happens when we write code that combines data and
code together in an object. The following listing demonstrates what this looks like.
ListingA.1 Breaking Principle #1 in OOP
class Author {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
fullName() {
return this.firstName + " " + this.lastName;
}
isProlific() {
return this.books > 100;
}
}

=== PAGE 364 ===
336 APPENDIX A Principles of data-oriented programming
var obj = new Author("Isaac", "Asimov", 500);
Isaac Asimov really
obj.fullName();
wrote around 500
// → "Isaac Asimov" books!
BREAKING PRINCIPLE #1 IN FP
Breaking this principle without classes in FP means hiding data in the lexical scope of
a function. The next listing provides an example of this.
ListingA.2 Breaking Principle #1 in FP
function createAuthorObject(firstName, lastName, books) {
return {
fullName: function() {
return firstName + " " + lastName;
},
isProlific: function () {
return books > 100;
}
};
}
var obj = createAuthorObject("Isaac", "Asimov", 500);
obj.fullName();
// → "Isaac Asimov"
ADHERING TO PRINCIPLE #1 IN OOP
Listing A.3 shows an example that adheres to Principle #1 in OOP. Compliance with
this principle may be achieved even with classes by writing programs such that:
 The code consists of static methods.
 The data is encapsulated in data classes (classes that are merely containers of
data).
ListingA.3 Following Principle #1 in OOP
class AuthorData {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
}
class NameCalculation {
static fullName(data) {
return data.firstName + " " + data.lastName;
}
}
class AuthorRating {
static isProlific (data) {
return data.books > 100;
}
}

=== PAGE 365 ===
A.1 Principle #1: Separate code from data 337
var data = new AuthorData("Isaac", "Asimov", 500);
NameCalculation.fullName(data);
// → "Isaac Asimov"
ADHERING TO PRINCIPLE #1 IN FP
Listing A.4 shows an example that adheres to Principle #1 in FP. Compliance with this
principle means separating code from data.
ListingA.4 Following Principle #1 in FP
function createAuthorData(firstName, lastName, books) {
return {
firstName: firstName,
lastName: lastName,
books: books
};
}
function fullName(data) {
return data.firstName + " " + data.lastName;
}
function isProlific (data) {
return data.books > 100;
}
var data = createAuthorData("Isaac", "Asimov", 500);
fullName(data);
// → "Isaac Asimov"
A.1.2 Benefits of Principle #1
Having illustrated how to follow or break Principle #1 both in OOP and FP, let’s look
at the benefits that Principle #1 brings to our programs. Careful separation of code
from data benefits our programs in the following ways:
 Code can be reused in different contexts.
 Code can be tested in isolation.
 Systems tend to be less complex.
BENEFIT #1: CODE CAN BE REUSED IN DIFFERENT CONTEXTS
Imagine that besides the author entity, there is a user entity that has nothing to do
with authors but has two of the same data fields as the author entity: firstName and
lastName. The logic of calculating the full name is the same for authors and users—
retrieving the values of two fields with the same names. However, in traditional OOP
as in the version with createAuthorObject in listing A.5, the code of fullName cannot
be reused on a user in a straightforward way because it is locked inside the Author class.
ListingA.5 The code of fullName is locked in the Author class
class Author {
constructor(firstName, lastName, books) {

=== PAGE 366 ===
338 APPENDIX A Principles of data-oriented programming
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
fullName() {
return this.firstName + " " + this.lastName;
}
isProlific() {
return this.books > 100;
}
}
One way to achieve code reusability when code and data are mixed is to use OOP
mechanisms like inheritance or composition to let the User and Author classes use
the same fullName method. These techniques are adequate for simple use cases, but
in real-world systems, the abundance of classes (either base classes or composite
classes) tends to increase complexity.
Listing A.6 shows a simple way to avoid inheritance. In this listing, we duplicate the
code of fullName inside a createUserObject function.
ListingA.6 Duplicating code in OOP to avoid inheritance
function createAuthorObject(firstName, lastName, books) {
var data = {firstName: firstName, lastName: lastName, books: books};
return {
fullName: function fullName() {
return data.firstName + " " + data.lastName;
}
};
}
function createUserObject(firstName, lastName, email) {
var data = {firstName: firstName, lastName: lastName, email: email};
return {
fullName: function fullName() {
return data.firstName + " " + data.lastName;
}
};
}
var obj = createUserObject("John", "Doe", "john@doe.com");
obj.fullName();
// → "John Doe"
In DOP, no modification to the code that deals with author entities is necessary in
order to make it available to user entities, because:
 The code that deals with full name calculation is separate from the code that
deals with the creation of author data.
 The function that calculates the full name works with any hash map that has a
firstName and a lastName field.

=== PAGE 367 ===
A.1 Principle #1: Separate code from data 339
It is possible to leverage the fact that data relevant to the full name calculation for a
user and an author has the same shape. With no modifications, the fullName function
works properly both on author data and on user data as the following listing shows.
ListingA.7 The same code on data entities of different types (FP style)
function createAuthorData(firstName, lastName, books) {
return {firstName: firstName, lastName: lastName, books: books};
}
function fullName(data) {
return data.firstName + " " + data.lastName;
}
function createUserData(firstName, lastName, email) {
return {firstName: firstName, lastName: lastName, email: email};
}
var authorData = createAuthorData("Isaac", "Asimov", 500);
fullName(authorData);
var userData = createUserData("John", "Doe", "john@doe.com");
fullName(userData);
// → "John Doe"
When Principle #1 is applied in OOP, code reuse is straightforward even when classes
are used. In statically-typed OOP languages like Java or C, we would have to create a
common interface for AuthorData and UserData. In a dynamically-typed language
like JavaScript, however, that is not required. The code of NameCalculation.full-
Name() works both with author data and user data as the next listing demonstrates.
ListingA.8 The same code on data entities of different types (OOP style)
class AuthorData {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
}
class NameCalculation {
static fullName(data) {
return data.firstName + " " + data.lastName;
}
}
class UserData {
constructor(firstName, lastName, email) {
this.firstName = firstName;
this.lastName = lastName;
this.email = email;

=== PAGE 368 ===
340 APPENDIX A Principles of data-oriented programming
}
}
var userData = new UserData("John", "Doe", "john@doe.com");
NameCalculation.fullName(userData);
var authorData = new AuthorData("Isaac", "Asimov", 500);
NameCalculation.fullName(authorData);
// → "John Doe"
TIP When code is separate from data, it is straightforward to reuse code in different
contexts. This benefit is achievable both in FP and in OOP.
BENEFIT #2: CODE CAN BE TESTED IN ISOLATION
A similar benefit is the ability to test code in an isolated context. When code is not sep-
arate from data, it is necessary to instantiate an object to test its methods. For instance,
in order to test the fullName code that lives inside the createAuthorObject function,
we need to instantiate an author object as the following listing shows.
ListingA.9 Testing code when code and data are mixed
var author = createAuthorObject("Isaac", "Asimov", 500);
author.fullName() === "Isaac Asimov"
// → true
In this simple scenario, it is not overly burdensome. We only load (unnecessarily) the
code for isProlific. Although in a real-world situation, instantiating an object might
involve complex and tedious setup.
In the DOP version, where createAuthorData and fullName are separate, we can
create the data to be passed to fullName in isolation, testing fullName in isolation as
well. The following listing provides an example.
ListingA.10 Testing code in isolation (FP style)
var author = {
firstName: "Isaac",
lastName: "Asimov"
};
fullName(author) === "Isaac Asimov"
// → true
If classes are used, it is only necessary to instantiate a data object. We do not need to
load the code for isProlific, which lives in a separate class than fullName, in order
to test fullName. The next listing lays out an example of this approach.
ListingA.11 Testing code in isolation (OOP style)
var data = new AuthorData("Isaac", "Asimov");
NameCalculation.fullName(data) === "Isaac Asimov"
// → true

=== PAGE 369 ===
A.1 Principle #1: Separate code from data 341
TIP Writing tests is easier when code is separated from data.
BENEFIT #3: SYSTEMS TEND TO BE LESS COMPLEX
The third benefit of applying Principle #1 to our programs is that systems tend to be less
complex. This benefit is the deepest one but also the one that is most subtle to explain.
The type of complexity I refer to is the one that makes systems hard to understand
as defined in the paper, “Out of the Tar Pit,” by Ben Moseley and Peter Marks (http://
mng.bz/enzq). It has nothing to do with the complexity of the resources consumed by
a program. Similarly, references to simplicity mean not complex (in other words, easy to
understand).
 NOTE Complex in the context of this book means hard to understand.
Keep in mind that complexity and simplicity (like hard and easy) are not absolute but
relative concepts. The complexity of two systems can be compared to determine
whether system A is more complex (or simpler) than system B. When code and data
are kept separate, the system tends to be easier to understand for two reasons:
 The scope of a data entity or a code entity is smaller than the scope of an entity that com-
bines code and data. Each entity is therefore easier to understand.
 Entities of the system are split into disjoint groups: code and data. Entities therefore
have fewer relations to other entities.
This insight is illustrated in a class diagram of our fictitious Library Management Sys-
tem, where code and data are mixed. It is not necessary to know the details of the
classes of this system to see that the diagram in figure A.2 represents a complex system;
C Library
C Catalog
* *
C Book C Librarian
*
*
C Member
*
C Author
C BookItem C User
Figure A.2 A class
diagram overview for the
C BookLending * Library Management
System

=== PAGE 370 ===
342 APPENDIX A Principles of data-oriented programming
this in the sense that it is hard to understand. The system is hard to understand because
there are many dependencies between the entities that compose the system.
The most complex entity of the system in figure A.2 is the Librarian entity, which
is connected via six relations to other entities. Some relations are data relations (asso-
ciation and composition), and some relations are code relations (inheritance and
dependency). But in this design, the Librarian entity mixes code and data, and there-
fore, it has to be involved in both data and code relations. If each entity of the system
is split into a code entity and a data entity without making any further modification to the
system, the result (see figure A.3) is made of two disconnected parts:
 The left part is made only of data entities and data relations: association and
composition.
 The right part is made only of code entities and code relations: dependency
and inheritance.
C LibraryData * C LibrarianData C CatalogCode
*
C MemberData C CatalogData C LibrarianCode
*
C BookData C MemberCode C BookLendingCode C BookItemCode
*
* *
C BookItemData C AuthorData C UserCode C BookItem
*
C BookLendingData
Figure A.3 A class diagram where every class is split into code and data entities
The new system, where code and data are separate, is easier to understand than the
original system, where code and data are mixed. Thus, the data part of the system and
the code part of the system can each be understood on its own.
TIP A system made of disconnected parts is less complex than a system made of a sin-
gle part.
One could argue that the complexity of the original system, where code and data are
mixed, is due to a bad design and that an experienced OOP developer would have
designed a simpler system using smart design patterns. That is true, but in a sense, it is

=== PAGE 371 ===
A.1 Principle #1: Separate code from data 343
irrelevant. The point of Principle #1 is that a system made of entities that do not com-
bine code and data tends to be simpler than a system made of entities that do combine
code and data.
It has been said many times that simplicity is hard. According to the first principle of
DOP, simplicity is easier to achieve when separating code and data.
TIP Simplicity is easier to achieve when code is separated from data.
A.1.3 Cost for Principle #1
This section looks at the cost involved when we implement Principle #1. The price we
pay in order to benefit from the separation between code and data is threefold:
 There is no control on what code can access what data.
 There is no packaging.
 Our systems are made from more entities.
COST #1: THERE IS NO CONTROL ON WHAT CODE CAN ACCESS WHAT DATA
When code and data are mixed, it is easy to understand what pieces of code can access
what kinds of data. For example, in OOP, the data is encapsulated in an object, which
guarantees that the data is accessible only by the object’s methods. In DOP, data
stands on its own. It is transparent if you like, and as a consequence, it can be accessed
by any piece of code.
When refactoring the shape of some data, every place in our code that accesses this
kind of data must be known. Moreover, without the application of Principle #3 (enforc-
ing data immutability), which we discuss later, accessing data by any piece of code is
inherently unsafe. In that case, it would be hard to guarantee the validity of our data.
TIP Data safety is ensured by another principle (Principle #3) that enforces data
immutability.
COST #2: THERE IS NO PACKAGING
One of the benefits of mixing code and data is that when you have an object in hand,
it is a package that contains both the code (via methods) and the data (via members).
As a consequence, it is easy to discover how to manipulate the data: you look at the
methods of the class.
In DOP, the code that manipulates the data could be anywhere. For example,
createAuthorData might be in one file and fullName in another file. This makes it
difficult for developers to discover that the fullName function is available. In some sit-
uations, it could lead to wasted time and unnecessary code duplication.
COST #3: OUR SYSTEMS ARE MADE FROM MORE ENTITIES
Let’s do simple arithmetic. Imagine a system made of N classes that combine code and
data. When you split the system into code entities and data entities, you get a system
made of 2N entities. This calculation is not accurate, however, because usually when
you separate code and data, the class hierarchy tends to get simpler as we need less

=== PAGE 372 ===
344 APPENDIX A Principles of data-oriented programming
class inheritance and composition. Therefore, the number of classes in the resulting
system will probably be somewhere between N and 2N.
On one hand, when adhering to Principle #1, the entities of the system are sim-
pler. On the other hand, there are more entities. This cost is mitigated by Principle
#2, which guides us to represent our data with generic data structures.
TIP When adhering to Principle #1, systems are made of simpler entities, but there
are more of them.
A.1.4 Summary of Principle #1
DOP requires the separation of code from data. In OOP languages, aggregate code in
static methods and data in classes with no methods. In FP languages, avoid hiding data
in the lexical scope of functions.
Separating code from data comes at a price. It reduces control over what pieces of
code access our data and can cause our systems to be made of more entities. But it’s
worth paying the price because, when adhering to this principle, our code can be
reused in different contexts in a straightforward way and tested in isolation. Moreover,
a system made of separate entities for code and data tends to be easier to understand.
DOP Principle #1: Separate code from data
To follow this principle, we separate code from data in such a way that the code
resides in functions whose behavior does not depend on data that is encapsulated
in the function’s context. The following diagram provides a visual representation
of this.
DOPPrinciple #1: Separate code from data
FP
Code
System OOP
Data
 Benefits include
– Code can be reused in different contexts.
– Code can be tested in isolation.
– Systems tend to be less complex.
 The cost for implementing Principle #1 includes
– No control on what code accesses which data.
– No packaging.
– More entities.

=== PAGE 373 ===
A.2 Principle #2: Represent data with generic data structures 345
A.2 Principle #2: Represent data with generic data
structures
When adhering to Principle #1, code is separated from data. DOP is not opinionated
about the programming constructs to use for organizing the code, but it has a lot to
say about how the data should be represented. This is the theme of Principle #2.
The most common generic data structures are maps (aka dictionaries) and arrays
(or lists). But other generic data structures (e.g., sets, trees, and queues) can be used
as well. Principle #2 does not deal with the mutability or the immutability of the data.
That is the theme of Principle #3.
PRINCIPLE #2 Represent application data with generic data structures.
A.2.1 Illustration of Principle #2
In DOP, data is represented with generic data structures (like maps and arrays)
instead of instantiating data via specific classes. In fact, most of the data entities that
appear in a typical application can be represented with maps and arrays (or lists). But
there exist other generic data structures (e.g., sets, lists, queues, etc.) that might be
required in some use cases. Let’s look at the same simple example we used to illustrate
Principle #1 (data that represents an author).
An author is a data entity with a firstName, a lastName, and the number of books
they have written. Principle #2 is broken when we use a specific class to represent an
author as this listing reveals.
ListingA.12 Breaking Principle #2 in OOP
class AuthorData {
constructor(firstName, lastName, books) {
this.firstName = firstName;
this.lastName = lastName;
this.books = books;
}
}
Principle #2 is followed when using a map (a dictionary or an associative array) as a
generic data structure that represents an author. The following listing illustrates how
we can follow this principle in OOP.
ListingA.13 Following Principle #2 in OOP
function createAuthorData(firstName, lastName, books) {
var data = new Map;
data.firstName = firstName;
data.lastName = lastName;

=== PAGE 374 ===
346 APPENDIX A Principles of data-oriented programming
data.books = books;
return data;
}
In a language like JavaScript, we can also instantiate a map via a data literal, which is a
bit more convenient. The following listing shows an example.
ListingA.14 Following Principle #2 with map literals
function createAuthorData(firstName, lastName, books) {
return {
firstName: firstName,
lastName: lastName,
books: books
};
}
A.2.2 Benefits of Principle #2
Using generic data structures to represent data has multiple benefits. We cover these
benefits in greater detail in the following sections:
 The ability to use generic functions that are not limited to our specific use case
 A flexible data model
USING FUNCTIONS THAT ARE NOT LIMITED TO A SPECIFIC USE CASE
Using generic data structures to represent data makes it possible to manipulate data
with a rich set of functions that are available on those data structures natively in our
programming language. Additionally, third-party libraries also provide more of these
functions. For instance, JavaScript natively provides some basic functions on maps and
arrays, and third-party libraries like Lodash (https://lodash.com/) extend the func-
tionality with even more functions. There is a famous quote by Alan Perlis that sum-
marizes this benefit:
It is better to have 100 functions operate on one data structure than to have 10 functions
operate on 10 data structures.
—Alan Perlis (“Epigrams on Programming,” 1982)
When an author is represented as a map, the author can be serialized into JSON
using JSON.stringify(), which is part of JavaScript. The following listing provides
an example.
ListingA.15 [#serialize-klipse-js],reftext="A.1"
var data = createAuthorData("Isaac", "Asimov", 500);
JSON.stringify(data);
// → "{\"firstName\":\"Isaac\",\"lastName\":\"Asimov\",\"books\":500}"
Serializing author data without the number of books can be accomplished via Lodash’s
_.pick() function. The following listing uses _.pick() to create an object with a sub-
set of keys.

=== PAGE 375 ===
A.2 Principle #2: Represent data with generic data structures 347
ListingA.16 Manipulating data with generic functions
var data = createAuthorData("Isaac", "Asimov", 500);
var dataWithoutBooks = _.pick(data, ["firstName", "lastName"]);
JSON.stringify(dataWithoutBooks);
// → "{\"firstName\":\"Isaac\",\"lastName\":\"Asimov\"}"
TIP When adhering to Principle #2, a rich set of functionality is available for data
manipulation.
FLEXIBLE DATA MODEL
When using generic data structures, the data model is flexible, and data is not forced
into a specific shape. Data can be created with no predefined shape, and its shape can
be modified at will.
In classic OOP, when not adhering to Principle #2, each piece of data is instanti-
ated via a class and must follow a rigid shape. When a slightly different data shape is
needed, a new class must be defined. Take, for example, AuthorData, a class that rep-
resents an author entity made of three fields: firstName, lastName, and books. Sup-
pose that you want to add a field called fullName with the full name of the author. If
we fail to adhere to Principle #2, a new class, AuthorDataWithFullName, must be
defined. However, when using generic data structures, fields can be added to (or
removed from) a map on the fly as the following listing shows.
ListingA.17 Adding a field on the fly
var data = createAuthorData("Isaac", "Asimov", 500);
data.fullName = "Isaac Asimov";
TIP Working with a flexible data model is particularly useful in applications where
the shape of the data tends to be dynamic (e.g., web apps and web services).
Part 1 of the book explores in detail the benefits of a flexible data model in real-world
applications. Next, let’s explore the cost for adhering to Principle #2.
A.2.3 Cost for Principle #2
As with any programming principle, using this principle comes with its own set of trade-
offs. The price paid for representing data with generic data structures is as follows:
 There is a slight performance hit.
 No data schema is required.
 No compile-time check that the data is valid is necessary.
 In some statically-typed languages, type casting is needed.
COST #1: PERFORMANCE HIT
When specific classes are used to instantiate data, retrieving the value of a class mem-
ber is fast because the compiler knows how the data will look and can do many optimi-
zations. With generic data structures, it is harder to optimize, so retrieving the value

=== PAGE 376 ===
348 APPENDIX A Principles of data-oriented programming
associated to a key in a map, for example, is a bit slower than retrieving the value of a
class member. Similarly, setting the value of an arbitrary key in a map is a bit slower
than setting the value of a class member. In most programming languages, this perfor-
mance hit is not significant, but it is something to keep in mind.
TIP Retrieving and storing the value associated to an arbitrary key from a map is a bit
slower than with a class member.
COST #2: NO DATA SCHEMA
When data is instantiated from a class, the information about the data shape is in the
class definition. Every piece of data has an associated data shape. The existence of
data schema at a class level is useful for developers and for IDEs because
 Developers can easily discover the expected data shape.
 IDEs provide features like field name autocompletion.
When data is represented with generic data structures, the data schema is not part of
the data representation. As a consequence, some pieces of data might have an associ-
ated data schema and other pieces of data do not (see Principle #4).
TIP When generic data structures are used to store data, the data shape is not part of
the data representation.
COST #3: NO COMPILE-TIME CHECK THAT THE DATA IS VALID
Look again at the fullName function in the following listing, which was created to
explore Principle #1. This function receives the data it manipulates as an argument.
ListingA.18 Declaring the fullName function
function fullName(data) {
return data.firstName + " " + data.lastName;
}
When data is passed to fullName that does not conform to the shape fullName
expects, an error occurs at run time. With generic data structures, mistyping the field
storing the first name (e.g., fistName instead of firstName) does not result in a
compile-time error or an exception. Rather, firstName is mysteriously omitted from
the result. The following listing shows this unexpected behavior.
ListingA.19 Unexpected behavior with invalid data
fullName({fistName: "Issac", lastName: "Asimov"});
// → "undefined Asimov"
When we instantiate data via classes with a rigid data shape, this type of error is caught
at compile time. This drawback is mitigated by the application of Principle #4 that
deals with data validation.

=== PAGE 377 ===
A.2 Principle #2: Represent data with generic data structures 349
TIP When data is represented with generic data structures, data shape errors are
caught only at run time.
COST #4: THE NEED FOR EXPLICIT TYPE CASTING
In some statically-typed languages, explicit type casting is needed. This section takes a
look at explicit type casting in Java and at dynamic fields in C#.
In a statically-typed language like Java, author data can be represented as a map
whose keys are of type string and whose values are of types Object. For example, in
Java, author data is represented by a Map<String, Object> as the following listing
illustrates.
ListingA.20 Author data as a string map in Java
var asimov = new HashMap<String, Object>();
asimov.put("firstName", "Isaac");
asimov.put("lastName", "Asimov");
asimov.put("books", 500);
Because the information about the exact type of the field values is not available at
compile time, when accessing a field, an explicit type cast is required. For instance, in
order to check whether an author is prolific, the value of the books field must be type
cast to an integer as the next listing shows.
ListingA.21 Type casting is required when accessing a field in Java
class AuthorRating {
static boolean isProlific (Map<String, Object> data) {
return (int)data.get("books") > 100;
}
}
Some Java JSON serialization libraries like Gson (https://github.com/google/gson)
support serialization of maps of type Map<String, Object>, without requiring the user
to do any type casting. All the magic happens behind the scenes!
C# supports a dynamic data type called dynamic (see http://mng.bz/voqJ), which
allows type checking to occur at run time. Using this feature, author data is repre-
sented as a dictionary, where the keys are of type string, and the values are of type
dynamic. The next listing provides this representation.
ListingA.22 Author data as a dynamic string map in C#
var asimov = new Dictionary<string, dynamic>();
asimov["name"] = "Isaac Asimov";
asimov["books"] = 500;
The information about the exact type of the field values is resolved at run time. When
accessing a field, no type cast is required. For instance, when checking whether an

=== PAGE 378 ===
350 APPENDIX A Principles of data-oriented programming
author is prolific, the books field can be accessed as though it were declared as an
integer as in this listing.
ListingA.23 Type casting is not needed when accessing dynamic fields in C#
class AuthorRating {
public static bool isProlific (Dictionary<String, dynamic> data) {
return data["books"] > 100;
}
}
A.2.4 Summary of Principle #2
DOP uses generic data structures to represent data. This might cause a (small) perfor-
mance hit and impose the need to manually document the shape of data because the
compiler cannot validate it statically. Adherence to this principle enables the manipu-
lation of data with a rich set of generic functions (provided by the language and by
third-party libraries). Additionally, our data model is flexible. At this point, the data
can be either mutable or immutable. The next principle (Principle #3) illustrates the
value of immutability.
DOP Principle #2: Represent data with generic data structures
To comply with this principle, we represent application data with generic data struc-
tures, mostly maps and arrays (or lists). The following diagram shows a visual repre-
sentation of this principle.
DOPPrinciple #2: Represent data with generic data structures
Specific
Data
Generic
 Benefits include
– Using generic functions that are not limited to our specific use case
– A flexible data model
 The cost for implementing this principle includes
– There is a slight performance hit.
– No data schema is required.
– No compile time check that the data is valid is necessary.
– In some statically-typed languages, explicit type casting is needed.

=== PAGE 379 ===
A.3 Principle #3: Data is immutable 351
A.3 Principle #3: Data is immutable
With data separated from code and represented with generic data structures, how are
changes to the data managed? DOP is very strict on this question. Mutation of data is
not allowed! In DOP, changes to data are accomplished by creating new versions of
the data. The reference to a variable may be changed so that it refers to a new version of
the data, but the value of the data itself must never change.
PRINCIPLE #3 Data is immutable.
A.3.1 Illustration of Principle #3
Think about the number 42. What happens to 42 when you add 1 to it? Does it
become 43? No, 42 stays 42 forever! Now, put 42 inside an object: {num: 42}. What
happens to the object when you add 1 to 42? Does it become 43? It depends on the
programming language.
 In Clojure, a programming language that embraces data immutability, the value
of the num field stays 42 forever, no matter what.
 In many programming languages, the value of the num field becomes 43.
For instance, in JavaScript, mutating the field of a map referred by two variables has
an impact on both variables. The following listing demonstrates this.
ListingA.24 Mutating data referred by two variables impact both variables
var myData = {num: 42};
var yourData = myData;
yourData.num = yourData.num + 1;
console.log(myData.num);
// → 43
Now, myData.num equals 43. According to DOP, however, data should never change!
Instead of mutating data, a new version of it is created. A naive (and inefficient) way
to create a new version of data is to clone it before modifying it. For instance, in list-
ing A.25, there is a function that changes the value of a field inside an object by clon-
ing the object via Object.assign, provided natively by JavaScript. When changeValue
is called on myData, myData is not affected; myData.num remains 42. This is the essence
of data immutability!
ListingA.25 Data immutability via cloning
function changeValue(obj, k, v) {
var res = Object.assign({}, obj);
res[k] = v;

=== PAGE 380 ===
352 APPENDIX A Principles of data-oriented programming
return res;
}
var myData = {num: 42};
var yourData = changeValue(myData, "num", myData.num + 1);
console.log(myData.num);
// → 43
Embracing immutability in an efficient way, both in terms of computation and mem-
ory, requires a third-party library like Immutable.js (https://immutable-js.com/), which
provides an efficient implementation of persistent data structures (aka immutable
data structures). In most programming languages, libraries exist that provide an effi-
cient implementation of persistent data structures.
With Immutable.js, JavaScript native maps and arrays are not used, but rather,
immutable maps and immutable lists are instantiated via Immutable.Map and Immutable
.List. An element of a map is accessed using the get method. A new version of the
map is created when a field is modified with the set method.
Listing A.26 shows how to create and manipulate immutable data efficiently with a
third-party library. In the output, yourData.get("num") is 43, but myData.get("num")
remains 42.
ListingA.26 Creating and manipulating immutable data
var myData = Immutable.Map({num: 42})
var yourData = myData.set("num", 43);
console.log(yourData.get("num"));
// → 43
console.log(myData.get("num"));
// → 42
TIP When data is immutable, instead of mutating data, a new version of it is created.
A.3.2 Benefits of Principle #3
When programs are constrained from mutating data, we derive benefit in numerous
ways. The following sections detail these benefits:
 Data access to all with confidence
 Predictable code behavior
 Fast equality checks
 Concurrency safety for free
BENEFIT #1: DATA ACCESS TO ALL WITH CONFIDENCE
According to Principle #1 (separate code from data), data access is transparent. Any
function is allowed to access any piece of data. Without data immutability, we must be
careful when passing data as an argument to a function. We can either make sure the
function does not mutate the data or clone the data before it is passed to the function.
When adhering to data immutability, none of this is required.