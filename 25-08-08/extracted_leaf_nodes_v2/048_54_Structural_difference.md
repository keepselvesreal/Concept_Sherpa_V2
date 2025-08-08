# 5.4 Structural difference

**메타데이터:**
- ID: 48
- 레벨: 2
- 페이지: 127-133
- 페이지 수: 7
- 부모 ID: 43
- 텍스트 길이: 11697 문자

---

ifference 99
5.4 Structural difference
 NOTE This section deals with the implementation of a structural diff algorithm. Feel
free to skip this section if you don’t want to challenge your mind right now with the
details of a sophisticated use of recursion. It won’t prevent you from enjoying the rest
of the book. You can come back to this section later.
Theo How do you calculate the diff between various versions of the system state?
Joe That’s the most challenging part of the reconciliation algorithm. We need to
implement a structural diff algorithm for hash maps.
Theo In what sense is the diff structural?
Joe The structural diff algorithm looks at the structure of the hash maps and
ignores the order of the fields.
Theo Could you give me an example?
Joe Let’s start with maps without nested fields. Basically, there are three kinds of
diffs: field replacement, field addition, and field deletion. In order to make
things not too complicated, for now, we’ll deal only with replacement and
addition.
Joe once again goes to the whiteboard and draws table 5.3, representing the three kinds of
diffs. Theo is thinking the whiteboard is really starting to fill up today.
Table 5.3 Kinds of structural differences between maps without nested fields
Kind First map Second map Diff
Replacement {"a": 1} {"a": 2} {"a": 2}
Addition {"a": 1} {"a": 1, "b": 2} {"b": 2}
Deletion {"a": 1, "b": 2} {"a": 1} Not supported
Theo I notice that the order of the maps matters a lot. What about nested fields?
Joe It’s the same idea, but the nesting makes it a bit more difficult to grasp.
Joe changes several of the columns in table 5.3. When he’s through, he shows Theo the
nested fields in table 5.4.
Table 5.4 Kinds of structural differences between maps with nested fields
Kind First map Second map Diff
Replacement { { {
"a": { "a": { "a": {
"x": 1 "x": 2 "x": 2
} } }
} } }

100 CHAPTER 5 Basic concurrency control
Table 5.4 Kinds of structural differences between maps with nested fields (continued)
Kind First map Second map Diff
Addition { { {
"a": { "a": { "a": {
"x": 1 "x": 1, "y": 2
} "y": 2, }
} } }
}
Deletion { { Not supported
"a": { "a": {
"x": 1, "y": 2
"y": 2, }
} }
}
 NOTE The version of the structural diff algorithm illustrated in this chapter does
not deal with deletions. Dealing with deletions is definitely possible, but it requires a
more complicated algorithm.
Theo As you said, it’s harder to grasp. What about arrays?
Joe We compare the elements of the arrays in order: if they are equal, the diff is
null; if they differ, the diff has the value of the second array.
Joe summarizes the various kinds of diffs in another table on the whiteboard. Theo looks
at the result in table 5.5.
Table 5.5 Kinds of structural differences between arrays without nested elements
Kind First array Second array Diff
Replacement [1] [2] [2]
Addition [1] [1, 2] [null, 2]
Deletion [1, 2] [1] Not supported
Theo This usage of null is a bit weird but OK. Is it complicated to implement the
structural diff algorithm?
Joe Definitely! It took a good dose of mental gymnastics to come up with these 30
lines of code.
Joe downloads the code from one his personal repositories. Theo, with thumb and forefin-
gers touching his chin and his forehead slightly tilted, studies the code.
Listing5.4 The implementation of a structural diff
function diffObjects(data1, data2) {
_.isArray checks whether
var emptyObject = _.isArray(data1) ? [] : {};
its argument is an array.
if(data1 == data2) {

5.4 Structural difference 101
return emptyObject;
_.union creates an
} array of unique
var keys = _.union(_.keys(data1), _.keys(data2)); values from two
return _.reduce(keys, arrays (like union of
function (acc, k) { two sets in Maths).
var res = diff(
_.get(data1, k),
_.isObject checks
_.get(data2, k));
whether its argument
if((_.isObject(res) && _.isEmpty(res)) ||
is a collection (either
a map or an array).
(res == "no-diff")) {
return acc;
_.isEmpty }
checks return _.set(acc, [k], res);
whether its },
argument
emptyObject);
is an empty
} "no-diff" is how
collection.
we mark that
function diff(data1, data2) { two values are
if(_.isObject(data1) && _.isObject(data2)) { the same.
return diffObjects(data1, data2);
}
if(data1 !== data2) {
return data2;
}
return "no-diff";
}
Theo Wow! It involves a recursion inside a reduce! I’m sure Dave will love this, but
I’m too tired to understand this code right now. Let’s focus on what it does
instead of how it does it.
In order familiarize himself with the structural diff algorithm, Theo runs the algorithm
with examples from the table that Joe drew on the whiteboard. While Theo occupies his
fingers with more and more complicated examples, his mind wanders in the realm of
performance.
Listing5.5 An example of usage of a structural diff
var data1 = {
"a": {
"x": 1,
"y": [2, 3],
"z": 4
}
};
var data2 = {
"a": {
"x": 2,
"y": [2, 4],
"z": 4
}
}

102 CHAPTER 5 Basic concurrency control
diff(data1, data2);
//{
// "a": {
// "x": 2,
// "y": [
// undefined,
// 4
// ]
// }
//}
Theo What about the performance of the structural diff algorithm? It seems that the
algorithm goes over the leaves of both pieces of data?
Joe In the general case, that’s true. But, in the case of system data that’s manipu-
lated with structural sharing, the code is much more efficient.
Theo What do you mean?
Joe With structural sharing, most of the nested objects are shared between two ver-
sions of the system state. Therefore, most of the time, when the code enters
diffObjects, it will immediately return because data1 and data2 are the same.
TIP Calculating the diff between two versions of the state is efficient because two
hash maps created via structural sharing from the same hash map have most of their
nodes in common.
Theo Another benefit of immutable data... Let me see how the diff algorithm
behaves with concurrent mutations. I think I’ll start with a tiny library with no
users and a catalog with a single book, Watchmen.
Listing5.6 The data for a tiny library
var library = {
"catalog": {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore", "dave-gibbons"]
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
}
};

5.4 Structural difference 103
Joe I suggest that we start with nonconflicting mutations. What do you suggest?
Theo A mutation that updates the publication year of Watchmen and a mutation that
updates both the title of Watchmen and the name of the author of Watchmen.
On his laptop, Theo creates three versions of the library. He shows Joe his code, where one
mutation updates the publication year of Watchmen, and the other one updates the title of
Watchmen and the author’s name.
Listing5.7 Two nonconflicting mutations
var previous = library;
var next = _.set(
library,
["catalog", "booksByIsbn", "978-1779501127", "publicationYear"],
1986);
var libraryWithUpdatedTitle = _.set(
library,
["catalog", "booksByIsbn", "978-1779501127", "title"],
"The Watchmen");
var current = _.set(
libraryWithUpdatedTitle,
["catalog", "authorsById", "dave-gibbons", "name"],
"David Chester Gibbons");
Theo I’m curious to see what the diff between previous and current looks like.
Joe Run the code and you’ll see.
Theo runs the code snippets for the structural diff between previous and next and for
the structural diff between previous and current. His curiosity satisfied, Theo finds it’s
all beginning to make sense.
Listing5.8 Structural diff between maps with a single difference
diff(previous, next);
//{
// "catalog": {
// "booksByIsbn": {
// "978-1779501127": {
// "publicationYear": 1986
// }
// }
// }
//}
Listing5.9 Structural diff between maps with two differences
diff(previous, current);
//{
// "authorsById": {
// "dave-gibbons": {
// "name": "David Chester Gibbons",

104 CHAPTER 5 Basic concurrency control
// }
// },
// "catalog": {
// "booksByIsbn": {
// "978-1779501127": {
// "title": "The Watchmen"
// }
// }
// }
//}
//
Joe Can you give me the information path of the single field in the structural diff
between previous and next?
Theo It’s ["catalog", "booksByIsbn", "978-1779501127", "publicationYear"].
Joe Right. And what are the information paths of the fields in the structural diff
between previous and current?
Theo It’s ["catalog", "booksByIsbn", "978-1779501127", "title"] for the book
title and ["authorsById", "dave-gibbons", "name"] for the author’s name.
Joe Perfect! Now, can you figure out how to detect conflicting mutations by
inspecting the information paths of the structural diffs?
Theo We need to check if they have an information path in common or not.
Joe Exactly! If they have, it means the mutations are conflicting.
Theo But I have no idea how to write code that retrieves the information paths of a
nested map.
Joe Once again, it’s a nontrivial piece of code that involves a recursion inside a
reduce. Let me download another piece of code from my repository and show
it to you.
Listing5.10 Calculating the information paths of a (nested) map
function informationPaths (obj, path = []) {
return _.reduce(obj,
function(acc, v, k) {
if (_.isObject(v)) {
return _.concat(acc,
informationPaths(v,
_.concat(path, k)));
}
return _.concat(acc, [_.concat(path, k)]);
},
[]);
}
Theo Let me see if your code works as expected with the structural diffs of the
mutations.
Theo tests Joe’s code with two code snippets. The first shows the information paths of the
structural diff between previous and next, and the second shows the information paths
of the structural diff between previous and current.

5.4 Structural difference 105
Listing5.11 Fields that differ between previous and next
informationPaths(diff(previous, next));
// → ["catalog.booksByIsbn.978-1779501127.publicationYear"]
Listing5.12 Fields that differ between previous and current
informationPaths(diff(previous, current));
// [
// [
// "catalog",
// "booksByIsbn",
// "978-1779501127",
// "title"
// ],
// [
// "authorsById",
// "dave-gibbons",
// "name"
// ]
//]
Theo Nice! I assume that Lodash has a function that checks whether two arrays have
an element in common.
Joe Almost. There is _.intersection, which returns an array of the unique values
that are in two given arrays. For our purpose, though, we need to check
whether the intersection is empty. Here, look at this example.
Listing5.13 Checking whether two diff maps have a common information path
function havePathInCommon(diff1, diff2) {
return !_.isEmpty(_.intersection(informationPaths(diff1),
informationPaths(diff2)));
}
Theo You told me earlier that in the case of nonconflicting mutations, we can
safely patch the changes induced by the transition from previous to next
into current. How do you implement that?
Joe We do a recursive merge between current and the diff between previous and
next.
Theo Does Lodash provide an immutable version of recursive merge?
Joe Yes, here’s another example. Take a look at this code.
Listing5.14 Applying a patch
_.merge(current, (diff(previous, next)));
//{
// "authorsById": {
// "dave-gibbons": {
// "name": "David Chester Gibbons"
// }
// },

106 CHAPTER 5 Basic concurrency control
// "catalog": {
// "authorsById": {
// "alan-moore": {
// "bookIsbns": ["978-1779501127"]
// "name": "Alan Moore"
// },
// "dave-gibbons": {
// "bookIsbns": ["978-1779501127"],
// "name": "Dave Gibbons"
// },
// },
// "booksByIsbn": {
// "978-1779501127": {
// "authorIds": ["alan-moore", "dave-gibbons"],
// "isbn": "978-1779501127",
// "publicationYear": 1986,
// "title": "The Watchmen"
// }
// }
// }
//}
Theo Could it be as simple as this?
Joe Indeed.