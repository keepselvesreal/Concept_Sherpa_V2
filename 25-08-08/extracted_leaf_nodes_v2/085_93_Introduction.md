# 9.3 Introduction

**메타데이터:**
- ID: 85
- 레벨: 3
- 페이지: 212-213
- 페이지 수: 2
- 부모 ID: 84
- 텍스트 길이: 7521 문자

---

=== Page 211 ===
9.2 The efficiency of persistent data structures 183
Joe The number of operations it takes to get or update an element in a persistent
list with branching factor 32 is constant.
Theo How can that be? You just made the point that the number of operations is
log32 N.
Joe Be patient, my friend. What is the highest number of elements that you can
have in a list, in practice?
Theo I don’t know. I never thought about that.
Joe Let’s assume that it takes 4 bytes to store an element in a list.
Theo OK.
Joe Now, can you tell me how much memory it would take to hold a list with 10 bil-
lion elements?
Theo You mean 1 with 10 zeros?
Joe Yes.
Theo Each element take 4 bytes, so it would be around 40 GB!
Joe Correct. Do you agree that it doesn’t make sense to hold a list that takes 40 GB
of memory?
Theo I agree.
Joe So let’s take 10 billion as an upper bound to the number of elements in a list.
What is log32 of 10 billion?
Once again, Theo uses the blackboard to clarify his thoughts. With that, he quickly finds
the answer.
Theo 1 billion is approximately 2^30. Therefore, 10 billion is around 2^33. That
means that log2 of 10 billion is 33, so log32 of 10 billion should be around
33/5, which is a bit less than 7.
Joe I am impressed again by your sharpness with numbers. To be precise, log32 of
10 billion is 6.64.
Theo (smiling) I didn’t get that far.
Joe Did I convince you that, in practice, accessing or updating an element in a per-
sistent list is essentially constant?
Theo Yes, and I find it quite amazing!
TIP Persistent lists can be manipulated in near constant time.
Joe Me too.
Theo What about persistent maps?
Joe It’s quite similar, but I don’t think we have time to discuss it now.
Startled, Theo looks at his watch. This morning’s session has gone by so quickly. He notices
that it’s time to get back to the office and have lunch.

=== Page 212 ===
184 CHAPTER 9 Persistent data structures
9.3 Persistent data structures libraries
On their way back to the office, Theo and Joe don’t talk too much. Theo’s thoughts take
him back to what he learned in the university classroom. He feels a lot of respect for Phil
Bagwell, who discovered how to manipulate persistent data structures efficiently, and for
Rich Hickey, who created a programming language incorporating that discovery as a core
feature and making it available to the world. Immediately after lunch, Theo asks Joe to
show him what it looks like to manipulate persistent data structures for real in a program-
ming language.
Theo Are persistent data structures available in all programming languages?
Joe A few programming languages like Clojure, Scala, and C# provide them as part
of the language. In most programming languages, though, you need a third-
party library.
Theo Could you give me a few references?
Joe Sure.
Using Theo’s laptop, Joe bookmarks some sites. He knows exactly which URLs to look for.
Then, while Theo is looking over the bookmarked sites, Joe goes to the whiteboard and
jots down the specific libraries in table 9.1.
 Immutable.js for JavaScript at https://immutable-js.com/
 Paguro for Java at https://github.com/GlenKPeterson/Paguro
 Immutable Collections for C# at http://mng.bz/QW51
 Pyrsistent for Python at https://github.com/tobgu/pyrsistent
 Hamster for Ruby at https://github.com/hamstergem/hamster
Table 9.1 Persistent data structure libraries
Language Library
JavaScript Immutable.js
Java Paguro
C# Provided by the language
Python Pyrsistent
Ruby Hamster
Theo What does it take to integrate persistent data structures provided by a third-
party library into your code?
9.3.1 Persistent data structures in Java
Joe In an object-oriented language like Java, it’s quite straightforward to integrate
persistent data structures in a program because persistent data structures
implement collection interfaces, besides the parts of the interface that mutate
in place.
Theo What do you mean?

=== Page 213 ===
9.3 Persistent data structures libraries 185
Joe Take for instance, Paguro for Java. Paguro persistent maps implement the
read-only methods of java.util.Map like get() and containsKey(), but not
methods like put() and remove(). On the other hand, Paguro vectors imple-
ment the read-only methods of java.util.List like get() and size(), but not
methods like set().
Theo What happens when we call put() or remove() on a Paguro map?
Joe It throws an UnSupportedOperationException exception.
Theo What about iterating over the elements of a Paguro collection with a forEach()?
Joe That works like it would in any Java collection. Here, let me show you an example.
Listing9.5 Iterating over a Paguro vector
var myVec = PersistentVector.ofIter(
List.of(10, 2, 3));
Creates a Paguro
vector from a
for (Integer i : myVec) {
Java list
System.out.println(i);
}
Theo What about Java streams?
Joe Paguro collections are Java collections, so they support the Java stream inter-
face. Take a look at this code.
Listing9.6 Streaming a Paguro vector
var myVec = PersistentVector.ofIter(List.of(10, 2, 3));
vec1.stream().sorted().map(x -> x + 1);
TIP Paguro collections implement the read-only parts of Java collection interfaces.
Therefore, they can be passed to any methods that expect to receive a Java collection
without mutating it.
Theo So far, you told me how do use Paguro collections as Java read-only collections.
How do I make modifications to Paguro persistent data structures?
Joe In a way similar to the _.set() function of Lodash FP that we talked about
earlier. Instead of mutating in place, you create a new version.
Theo What methods does Paguro expose for creating new versions of a data structure?
Joe For vectors, you use replace(), and for maps, you use assoc().
Listing9.7 Creating a modified version of a Paguro vector
var myVec = PersistentVector.ofIter(List.of(10, 2, 3));
var myNextVec = myVec.replace(0, 42);

=== Page 214 ===
186 CHAPTER 9 Persistent data structures
Listing9.8 Creating a modified version of a Paguro map
var myMap = PersistentHashMap.of(Map.of("aa", 1, "bb", 2)
.entrySet());
Creates a Paguro map
from a Java map entry set
var myNextMap = myMap.assoc("aa", 42);
Theo Yes! Now I see how to use persistent data structures in Java, but what about
JavaScript?
9.3.2 Persistent data structures in JavaScript
Joe In a language like JavaScript, it’s a bit more cumbersome to integrate per-
sistent data structures.
Theo How so?
Joe Because JavaScript objects and arrays don’t expose any interface.
Theo Bummer.
Joe It’s not as terrible as it sounds because Immutable.js exposes its own set of
functions to manipulate its data structures.
Theo What do you mean?
Joe I’ll show you in a moment. But first, let me show you how to initiate Immutable.js
persistent data structures.
Theo OK!
Joe Immutable.js provides a handy function that recursively converts a native data
object to an immutable one. It’s called Immutable.fromJS().
Theo What do you mean by recursively?
Joe Consider the map that holds library data from our Library Management Sys-
tem: it has values that are themselves maps. Immutable.fromJS() converts the
nested maps into immutable maps.
Theo Could you show me some code?
Joe Absolutely. Take a look at this JavaScript code for library data.
Listing9.9 Conversion to immutable data
var libraryData = Immutable.fromJS({
"catalog": {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore",
"dave-gibbons"]
}
},
"authorsById": {
"alan-moore": {
"name": "Alan Moore",