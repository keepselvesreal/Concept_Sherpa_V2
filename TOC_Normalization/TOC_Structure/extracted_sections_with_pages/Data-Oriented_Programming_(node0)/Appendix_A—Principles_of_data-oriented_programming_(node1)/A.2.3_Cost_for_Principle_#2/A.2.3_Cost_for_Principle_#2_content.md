# A.2.3 Cost for Principle #2

**페이지**: 352-353
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:31

---


--- 페이지 352 ---

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

--- 페이지 352 끝 ---


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
