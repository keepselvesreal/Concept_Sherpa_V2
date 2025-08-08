# 6.2.2 Unit tests for functions down the tree

**메타데이터:**
- ID: 57
- 레벨: 3
- 페이지: 143-146
- 페이지 수: 4
- 부모 ID: 54
- 텍스트 길이: 6174 문자

---

for functions down the tree
Joe Let’s start from the function that appears in the deepest node in our tree:
Catalog.authorNames. Take a look at the code for Catalog.authorNames
and tell me what are the input and the output of Catalog.authorNames.
Joe turns his laptop so Theo can a closer look at the code. Theo takes a sip of his café au
lait as he looks over what’s on Joe’s laptop.
Listing6.5 The code of Catalog.authorNames
Catalog.authorNames = function (catalogData, authorIds) {
return _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
};
Theo The input of Catalog.authorNames is catalogData and authorIds. The
output is authorNames.
Joe Would you do me a favor and express it visually?
Theo Sure.
It’s Theo’s turn to grab a napkin. He draws a small rectangle with two inward arrows and
one outward arrow as in figure 6.2.
catalogData authorIds
Catalog.authorNames()
Figure 6.2 Visualization of the input
authorNames and output of Catalog.authorNames
Joe Excellent! Now, how many combinations of input would you include in the
unit test for Catalog.authorNames?
Theo Let me see.
Theo reaches for another napkin. This time he creates a table to gather his thoughts
(table 6.1).

116 CHAPTER 6 Unit tests
Table 6.1 The table of test cases for Catalog.authorNames
catalogData authorIds authorNames
Catalog with two authors Empty array Empty array
Catalog with two authors Array with one author ID Array with one author name
Catalog with two authors Array with two author IDs Array with two author names
Theo To begin with, I would have a catalogData with two author IDs and call
Catalog.authorNames with three arguments: an empty array, an array with a
single author ID, and an array with two author IDs.
Joe How would you generate the catalogData?
Theo Exactly as we generated it before.
Turning to his laptop, Theo writes the code for catalogData. He shows it to Joe.
Listing6.6 A complete catalogData map
var catalogData = {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore", "dave-gibbons"],
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
},
{
"id": "book-item-2",
"libId": "nyc-central-lib",
"isLent": false
}
]
}
},
"authorsById": {
"alan-moore": {
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
};

6.2 Unit tests for data manipulation code 117
Joe You could use your big catalogData map for the unit test, but you could also
use a smaller map in the context of Catalog.authorNames. You can get rid of
the booksByIsbn field of the catalogData and the bookIsbns fields of the
authors.
Joe deletes a few lines from catalogData and gets a much smaller map. He shows the revi-
sion to Theo.
Listing6.7 A minimal version of catalogData
var catalogData = {
"authorsById": {
"alan-moore": {
"name": "Alan Moore"
},
"dave-gibbons": {
"name": "Dave Gibbons"
}
}
};
Theo Wait a minute! This catalogData is not valid.
Joe In DOP, data validity depends on the context. In the context of Library
.searchBooksByTitleJSON and Catalog.searchBooksByTitle, the mini-
mal version of catalogData is indeed not valid. However, in the context of
Catalog.bookInfo and Catalog.authorNames, it is perfectly valid. The reason
is that those two functions access only the authorsById field of catalogData.
TIP The validity of the data depends on the context.
Theo Why is it better to use a minimal version of the data in a test case?
Joe For a very simple reason—the smaller the data, the easier it is to manipulate.
TIP The smaller the data, the easier it is to manipulate.
Theo I’ll appreciate that when I write the unit tests!
Joe Definitely! One last thing before we start coding: how would you check that the
output of Catalog.authorNames is as expected?
Theo I would check that the value returned by Catalog.authorNames is an array
with the expected author names.
Joe How would you handle the array comparison?
Theo Let me think. I want to compare by value, not by reference. I guess I’ll have to
check that the array is of the expected size and then check member by mem-
ber, recursively.
Joe That’s too much of a mental burden when you’re in a coffee shop. As I showed
you earlier (see listing 6.1), we can recursively compare two data collections by
value with _.isEqual from Lodash.

118 CHAPTER 6 Unit tests
TIP We can compare the output and the expected output of our functions with
_.isEqual.
Theo Sounds good! Let me write the test cases.
Theo starts typing on his laptop. After a few minutes, he has some test cases for Catalog
.authorNames, each made from a function call to Catalog.authorNames wrapped in
_.isEqual.
Listing6.8 Unit test for Catalog.authorNames
var catalogData = {
"authorsById": {
"alan-moore": {
"name": "Alan Moore"
},
"dave-gibbons": {
"name": "Dave Gibbons"
}
}
};
_.isEqual(Catalog.authorNames(catalogData, []), []);
_.isEqual(Catalog.authorNames(
catalogData,
["alan-moore"]),
["Alan Moore"]);
_.isEqual(Catalog.authorNames(catalogData, ["alan-moore", "dave-gibbons"]),
["Alan Moore", "Dave Gibbons"]);
Joe Well done! Can you think of more test cases?
Theo Yes. There are test cases where the author ID doesn’t appear in the catalog
data, and test cases with empty catalog data. With minimal catalog data and
_.isEqual, it’s really easy to write lots of test cases!
Theo really enjoys this challenge. He creates a few more test cases to present to Joe.
Listing6.9 More test cases for Catalog.authorNames
_.isEqual(Catalog.authorNames({}, []), []);
_.isEqual(Catalog.authorNames({}, ["alan-moore"]), [undefined]);
_.isEqual(Catalog.authorNames(catalogData, ["alan-moore",
"albert-einstein"]), ["Alan Moore", undefined]);
_.isEqual(Catalog.authorNames(catalogData, []), []);
_.isEqual(Catalog.authorNames(catalogData, ["albert-einstein"]),
[undefined]);
Theo How do I run these unit tests?
Joe You use your preferred test framework.

6.2 Unit tests for data manipulation code 119
 NOTE We don’t deal here with test runners and test frameworks. We deal only with
the logic of the test cases.