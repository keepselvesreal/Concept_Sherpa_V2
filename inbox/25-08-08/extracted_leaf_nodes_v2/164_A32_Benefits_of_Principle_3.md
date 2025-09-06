# A.3.2 Benefits of Principle #3

**메타데이터:**
- ID: 164
- 레벨: 2
- 페이지: 380-381
- 페이지 수: 2
- 부모 ID: 161
- 텍스트 길이: 3356 문자

---

f Principle #3
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

354 APPENDIX A Principles of data-oriented programming
TIP Adherence to data immutability eliminates the need for a concurrency mecha-
nism. The data you have in hand never changes!