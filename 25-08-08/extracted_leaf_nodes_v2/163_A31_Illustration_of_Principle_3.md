# A.3.1 Illustration of Principle #3

**메타데이터:**
- ID: 163
- 레벨: 2
- 페이지: 379-379
- 페이지 수: 1
- 부모 ID: 161
- 텍스트 길이: 2851 문자

---

on of Principle #3
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