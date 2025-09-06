# A.3 Introduction

**메타데이터:**
- ID: 162
- 레벨: 2
- 페이지: 379-380
- 페이지 수: 2
- 부모 ID: 161
- 텍스트 길이: 8284 문자

---

=== Page 378 ===
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

=== Page 379 ===
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

=== Page 380 ===
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

=== Page 381 ===
A.3 Principle #3: Data is immutable 353
TIP When data is immutable, it can be passed to any function with confidence
because data never changes.
BENEFIT #2: PREDICTABLE CODE BEHAVIOR
As an illustration of what is meant by predictable, here is an example of an unpredictable
piece of code that does not adhere to data immutability. Take a look at the piece of
asynchronous JavaScript code in the following listing. When data is mutable, the behav-
ior of asynchronous code is not predictable.
ListingA.27 Unpredictable asynchronous code when data is mutable
var myData = {num: 42};
setTimeout(function (data){
console.log(data.num);
}, 1000, myData);
myData.num = 0;
The value of data.num inside the timeout callback is not predictable. It depends on
whether the data is modified by another piece of code during the 1,000 ms of the
timeout. However, with immutable data, it is guaranteed that data never changes and
that data.num is always 42 inside the callback.
TIP When data is immutable, the behavior of code that manipulates data is predictable.
BENEFIT #3: FAST EQUALITY CHECKS
With UI frameworks like React.js, there are frequent checks to see what portion of the
UI data has been modified since the previous rendering cycle. Portions that did not
change are not rendered again. In fact, in a typical frontend application, most of the
UI data is left unchanged between subsequent rendering cycles.
In a React application that does not adhere to data immutability, it is necessary to
check every (nested) part of the UI data. However, in a React application that follows
data immutability, it is possible to optimize the comparison of the data for the case
where data is not modified. Indeed, when the object address is the same, then it is cer-
tain that the data did not change.
Comparing object addresses is much faster than comparing all the fields. In part 1
of the book, fast equality checks are used to reconcile between concurrent mutations
in a highly scalable production system.
TIP Immutable data enables fast equality checks by comparing data by reference.
BENEFIT #4: FREE CONCURRENCY SAFETY
In a multi-threaded environment, concurrency safety mechanisms (e.g., mutexes)
are often used to prevent the data in thread A from being modified while it is accessed
in thread B. In addition to the slight performance hit they cause, concurrency safety
mechanisms impose a mental burden that makes code writing and reading much
more difficult.