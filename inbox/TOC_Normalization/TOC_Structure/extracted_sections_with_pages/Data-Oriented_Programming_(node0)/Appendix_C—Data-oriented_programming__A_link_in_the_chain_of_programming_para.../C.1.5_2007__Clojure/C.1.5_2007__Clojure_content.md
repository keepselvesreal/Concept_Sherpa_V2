# C.1.5 2007: Clojure

**페이지**: 379-380
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:43

---


--- 페이지 379 ---

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

--- 페이지 379 끝 ---


--- 페이지 380 ---

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

--- 페이지 380 끝 ---
