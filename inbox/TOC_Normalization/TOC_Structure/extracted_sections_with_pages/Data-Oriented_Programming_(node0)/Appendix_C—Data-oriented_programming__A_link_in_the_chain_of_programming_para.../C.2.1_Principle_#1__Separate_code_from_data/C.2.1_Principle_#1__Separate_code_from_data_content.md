# C.2.1 Principle #1: Separate code from data

**페이지**: 381-382
**계층**: Data-Oriented Programming (node0) > Appendix C—Data-oriented programming: A link in the chain of programming paradigms (node1)
**추출 시간**: 2025-08-06 19:47:44

---


--- 페이지 381 ---

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

--- 페이지 381 끝 ---


--- 페이지 382 ---

354 APPENDIX A Principles of data-oriented programming
TIP Adherence to data immutability eliminates the need for a concurrency mecha-
nism. The data you have in hand never changes!
A.3.3 Cost for Principle #3
As with the previous principles, applying Principle #3 comes at a price. The following
sections look at these costs:
 Performance hit
 Required library for persistent data structures
COST #1: PERFORMANCE HIT
As mentioned earlier, implementations of persistent data structures exist in most pro-
gramming languages. But even the most efficient implementation is a bit slower than
the in-place mutation of the data. In most applications, the performance hit and the
additional memory consumption involved in using immutable data structures is not
significant. But this is something to keep in mind.
COST #2: REQUIRED LIBRARY FOR PERSISTENT DATA STRUCTURES
In a language like Clojure, the native data structures of the language are immutable. How-
ever, in most programming languages, adhering to data immutability requires the inclu-
sion a third-party library that provides an implementation of persistent data structures.
The fact that the data structures are not native to the language means that it is dif-
ficult (if not impossible) to enforce the usage of immutable data across the board.
Also, when integrating with third-party libraries (e.g., a chart library), persistent data
structures must be converted into equivalent native data structures.
A.3.4 Summary of Principle #3
DOP considers data as a value that never changes. Adherence to this principle results
in code that is predictable even in a multi-threaded environment, and equality checks
are fast. However, a non-negligible mind shift is required, and in most programming
languages, a third-party library is needed to provide an efficient implementation of
persistent data structures.
DOP Principle #3: Data is immutable
To adhere to this principle, data is represented with immutable structures. The fol-
lowing diagram provides a visual representation of this.
DOPPrinciple #3: Data is immutable
Mutable
Data
Immutable

--- 페이지 382 끝 ---
