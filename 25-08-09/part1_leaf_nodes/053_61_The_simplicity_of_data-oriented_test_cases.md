# 6.1 The simplicity of data-oriented test cases

**ID**: 53  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

6.1 The simplicity of data-oriented test cases
Theo and Joe are seated around a large wooden table in a corner of “La vie est belle,” a
nice little French coffee shop, located near the Golden Gate Bridge. Theo orders a café
au lait with a croissant, and Joe orders a tight espresso with a pain au chocolat. Instead
of the usual general discussions about programming and life when they’re out of the
110

## 페이지 139

6.1 The simplicity of data-oriented test cases 111
office, Joe leads the discussion towards a very concrete topic—unit tests. Theo asks Joe for
an explanation.
Theo Are unit tests such a simple topic that we can tackle it here in a coffee shop?
Joe Unit tests in general, no. But unit tests for data-oriented code, yes!
Theo Why does that make a difference?
Joe The vast majority of the code base of a data-oriented system deals with data
manipulation.
Theo Yeah. I noticed that almost all the functions we wrote so far receive data and
return data.
TIP Most of the code in a data-oriented system deals with data manipulation.
Joe Writing a test case for functions that deal with data is only about generating
data input and expected output, and comparing the output of the function
with the expected output.
The steps of a test case
1 Generate data input: dataIn
2 Generate expected output: dataOut
3 Compare the output of the function with the expected output: f(dataIn) and
dataOut
Theo That’s it?
Joe Yes. As you’ll see in a moment, in DOP, there’s usually no need for mock
functions.
Theo I understand how to compare primitive values like strings or numbers, but I’m
not sure how I would compare data collections like maps.
Joe You compare field by field.
Theo Recursively?
Joe Yes!
Theo Oh no! I’m not able to write any recursive code in a coffee shop. I need the
calm of my office for that kind of stuff.
Joe Don’t worry. In DOP, data is represented in a generic way. There is a generic
function in Lodash called _.isEqual for recursive comparison of data collec-
tions. It works with both maps and arrays.
Joe opens his laptop. He is able to convince Theo by executing a few code snippets with
_.isEqual to compare an equal data collection with a non-equal one.
Listing6.1 Comparing an equal data collection recursively
_.isEqual({
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]

## 페이지 140

112 CHAPTER 6 Unit tests
}, {
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
});
// → true
Listing6.2 Comparing a non-equal data collection recursively
_.isEqual({
"name": "Alan Moore",
"bookIsbns": ["978-1779501127"]
}, {
"name": "Alan Moore",
"bookIsbns": ["bad-isbn"]
});
// → false
Theo Nice!
Joe Most of the test cases in DOP follow this pattern.
Theo decides he wants to try this out. He fires up his laptop and types a few lines of
pseudocode.
Listing6.3 The general pattern of a data-oriented test case
var dataIn = {
// input
};
var dataOut = {
// expected output
};
_.isEqual(f(dataIn), dataOut);
TIP It’s straightforward to write unit tests for code that deals with data manipulation.
Theo Indeed, this looks like something we can tackle in a coffee shop!
