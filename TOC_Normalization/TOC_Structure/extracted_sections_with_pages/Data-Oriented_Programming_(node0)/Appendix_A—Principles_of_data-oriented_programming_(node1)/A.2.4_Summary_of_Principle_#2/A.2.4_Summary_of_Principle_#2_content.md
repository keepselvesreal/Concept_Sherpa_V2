# A.2.4 Summary of Principle #2

**페이지**: 353-354
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:31

---


--- 페이지 353 ---

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

--- 페이지 353 끝 ---


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
