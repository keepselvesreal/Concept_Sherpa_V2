# 6 Introduction

**메타데이터:**
- ID: 52
- 레벨: 2
- 페이지: 138-139
- 페이지 수: 2
- 부모 ID: 51
- 텍스트 길이: 5746 문자

---

=== Page 137 ===
Summary 109
 Calculating the structural diff between two versions of the state is efficient because
two hash maps created via structural sharing from the same hash map have most
of their nodes in common.
 When data is immutable, it is safe to compare by reference, which is fast. When
the references are the same, it means that the data is the same.
 There are three kinds of structural differences between two nested hash maps:
replacement, addition, and deletion.
 Our structural diff algorithm supports replacements and additions but not
deletions.
Lodash functions introduced in this chapter
Function Description
concat(arrA, arrB) Creates an new array, concatenating arrA and arrB
intersection(arrA, arrB) Creates an array of unique values both in arrA and arrB
union(arrA, arrB) Creates an array of unique values from arrA and arrB
find(coll, pred) Iterates over elements of coll, returning the first element for
which pred returns true
isEmpty(coll) Checks if coll is empty
reduce(coll, f, initVal) Reduces coll to a value that is the accumulated result of running
each element in coll through f, where each successive invoca-
tion is supplied the return value of the previous
isArray(coll) Checks if coll is an array
isObject(coll) Checks if coll is a collection

=== Page 138 ===
Unit tests
Programming at a coffee shop
This chapter covers
 Generation of the minimal data input for a
test case
 Comparison of the output of a function with
the expected output
 Guidance about the quality and the quantity
of the test cases
In a data-oriented system, our code deals mainly with data manipulation: most of
our functions receive data and return data. As a consequence, it’s quite easy to
write unit tests to check whether our code behaves as expected. A unit test is made
of test cases that generate data input and compare the data output of the function
with the expected data output. In this chapter, we write unit tests for the queries
and mutations that we wrote in the previous chapters.
6.1 The simplicity of data-oriented test cases
Theo and Joe are seated around a large wooden table in a corner of “La vie est belle,” a
nice little French coffee shop, located near the Golden Gate Bridge. Theo orders a café
au lait with a croissant, and Joe orders a tight espresso with a pain au chocolat. Instead
of the usual general discussions about programming and life when they’re out of the
110

=== Page 139 ===
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

=== Page 140 ===
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
6.2 Unit tests for data manipulation code
A waiter in an elegant bow tie brings Theo his croissant and Joe his pain au chocolat. The
two friends momentarily interrupt their discussion to savor their French pastries. When
they’re done, they ask the waiter to bring them their drinks. Meanwhile, they resume the
discussion.
Joe Do you remember the code flow of the implementation of the search query?
Theo Let me look again at the code that implements the search query.
Theo brings up the implementation of the search query on his laptop. Noticing that Joe is
chewing on his nails again, he quickly checks out the code.