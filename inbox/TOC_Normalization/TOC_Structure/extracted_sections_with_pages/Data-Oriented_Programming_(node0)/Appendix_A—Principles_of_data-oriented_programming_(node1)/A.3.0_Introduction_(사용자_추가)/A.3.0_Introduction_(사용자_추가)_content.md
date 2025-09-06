# A.3.0 Introduction (사용자 추가)

**페이지**: 354-355
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:31

---


--- 페이지 354 ---

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

--- 페이지 354 끝 ---


--- 페이지 355 ---

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

--- 페이지 355 끝 ---
