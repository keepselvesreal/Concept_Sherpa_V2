# Chapter 9: Persistent data structures

**부제목:** Standing on the shoulders of giants
**계획된 페이지:** 203-224
**실제 페이지:** 203-224

=== PAGE 203 ===
Persistent data structures
Standing on the shoulders of giants
This chapter covers
 The internal details of persistent data
structures
 The time and memory efficiency of persistent
data structures
 Using persistent data structures in an
application
In part 1, we illustrated how to manage the state of a system without mutating data,
where immutability is maintained by constraining ourselves to manipulate the state
only with immutable functions using structural sharing. In this chapter, we present
a safer and more scalable way to preserve data immutability—representing data
with so-called persistent data structures. Efficient implementations of persistent
data structures exist for most programming languages via third-party libraries.
9.1 The need for persistent data structures
It’s at the university where Theo meets Joe this time. When Theo asks Joe if today’s topic
is academic in nature, Joe tells him that the use of persistent data structures only
became possible in programming languages following a discovery in 2001 by a computer
175

=== PAGE 204 ===
176 CHAPTER 9 Persistent data structures
researcher named Phil Bagwell.1 In 2007, Rich Hickey, the creator of Clojure, used this dis-
covery as the foundation of persistent data structures in Clojure. Unveiling the secrets of
these data structures to Theo in a university classroom is a way for Joe to honor the mem-
ory of Phil Bagwell, who unfortunately passed away in 2012. When they get to the univer-
sity classroom, Joe starts the conversation with a question.
Joe Are you getting used to DOP’s prohibition against mutating data in place and
creating new versions instead?
Theo I think so, but two things bother me about the idea of structural sharing that
you showed me.
Joe What bothers you, my friend?
Theo Safety and performance.
Joe What do you mean by safety?
Theo I mean that using immutable functions to manipulate data doesn’t prevent it
from being modified accidentally.
Joe Right! Would you like me to show you the naive way to handle immutability or
the real way?
Theo What are the pros and cons of each way?
Joe The naive way is easy but not efficient, although the real way is efficient but
not easy.
Theo Let’s start with the naive way then.
Joe Each programming language provides its own way to protect data from being
mutated.
Theo How would I do that in Java, for instance?
Joe Java provides immutable collections, and there is a way to convert a list or a
map to an immutable list or an immutable map.
 NOTE Immutable collections are not the same as persistent data structures.
Joe opens his laptop and fires it up. He brings up two code examples, one for immutable
lists and one for immutable maps.
Listing9.1 Converting a mutable list to an immutable list in Java
var myList = new ArrayList<Integer>();
myList.add(1);
myList.add(2);
myList.add(3);
var myImmutableList = List.of(myList.toArray());
1 P. Bagwell, “Ideal hash trees” (No. REP_WORK), 2001. [Online]. Available: https://lampwww.epfl.ch/papers/
idealhashtrees.pdf.

=== PAGE 205 ===
9.1 The need for persistent data structures 177
Listing9.2 Converting a mutable map to an immutable map in Java
var myMap = new HashMap<String, Object>();
myMap.put("name", "Isaac");
myMap.put("age", 42);
var myImmutableMap = Collections.unmodifiableMap(myMap);
Theo What happens when you try to modify an immutable collection?
Joe Java throws an UnsupportedOperationException.
Theo And in JavaScript?
Joe JavaScript provides an Object.freeze() function that prevents data from
being mutated. It works both with JavaScript arrays and objects.
Joe takes a minute to scroll through his laptop. When he finds what he’s looking for, he
shows Theo the code.
Listing9.3 Making an object immutable in JavaScript
var a = [1, 2, 3];
Object.freeze(a);
var b = {foo: 1};
Object.freeze(b);
Theo What happens when you try to modify a frozen object?
Joe It depends. In JavaScript strict mode, a TypeError exception is thrown, and in
nonstrict mode, it fails silently.
 NOTE JavaScript’s strict mode is a way to opt in to a restricted variant of JavaScript
that changes some silent errors to throw errors.
Theo In case of a nested collection, are the nested collections also frozen?
Joe No, but in JavaScript, one can write a deepFreeze() function that freezes an
object recursively. Here’s another example.
Listing9.4 Freezing an object recursively in JavaScript
function deepFreeze(object) {
// Retrieve the property names defined on object
const propNames = Object.getOwnPropertyNames(object);
// Freeze properties before freezing self
for (const name of propNames) {
const value = object[name];
if (value && typeof value === "object") {
deepFreeze(value);
}
}

=== PAGE 206 ===
178 CHAPTER 9 Persistent data structures
return Object.freeze(object);
}
Theo I see that it’s possible to ensure that data is never mutated, which answers my
concerns about safety. Now, let me share my concerns about performance.
TIP It’s possible to manually ensure that our data isn’t mutated, but it’s cumbersome.
Joe Sure.
Theo If I understand correctly, the main idea behind structural sharing is that most
data is usually shared between two versions.
Joe Correct.
Theo This insight allows us to create new versions of our collections using a shallow
copy instead of a deep copy, and you claimed that it was efficient.
Joe Exactly!
Theo Now, here is my concern. In the case of a collection with many entries, a shal-
low copy might be expensive.
Joe Could you give me an example of a collection with many entries?
Theo A catalog with 100,000 books, for instance.
Joe On my machine, making a shallow copy of a collection with 100,000 entries
doesn’t take more than 50 milliseconds.
Theo Sometimes, even 50 milliseconds per update isn’t acceptable.
Joe I totally agree with you. When one needs data immutability at scale, naive struc-
tural sharing is not appropriate.
Theo Also, shallow copying an array of 100,000 elements on each update would
increase the program memory by 100 KB.
Joe Indeed, at scale, we have a problem both with memory and computation.
TIP At scale, naive structural sharing causes a performance hit, both in terms of
memory and computation.
Theo Is there a better solution?
Joe Yes! For that, you’ll need to learn the real way to handle immutability. It’s
called persistent data structures.
9.2 The efficiency of persistent data structures
Theo In what sense are those data structures persistent?
Joe Persistent data structures are so named because they always preserve their pre-
vious versions.
TIP Persistent data structures always preserve the previous version of themselves
when they are modified.
Joe Persistent data structures address the two main limitations of naive structural
sharing: safety and performance.

=== PAGE 207 ===
9.2 The efficiency of persistent data structures 179
Theo Let’s start with safety. How do persistent data structures prevent data from
being mutated accidentally?
Joe In a language like Java, they implement the mutation methods of the collec-
tion interfaces by throwing the run-time exception UnsupportedOperation-
Exception.
Theo And, in a language like JavaScript?
Joe In JavaScript, persistent data structures provide their own methods to access
data, and none of those methods mutate data.
Theo Does that mean that we can’t use the dot notation to access fields?
Joe Correct. Fields of persistent data structures are accessed via a specific API.
Theo What about efficiency? How do persistent data structures make it possible to
create a new version of a huge collection in an efficient way?
Joe Persistent data structures organize data in such a way that we can use structural
sharing at the level of the data structure.
Theo Could you explain?
Joe Certainly. Let’s start with the simplest data structure: a linked list. Imagine that
you have a linked list with 100,000 elements.
Theo OK.
Joe What would it take to prepend an element to the head of the list?
Theo You mean to create a new version of the list with an additional element?
Joe Exactly!
Theo Well, we could copy the list and then prepend an element to the list, but it
would be quite expensive.
Joe What if I tell you that the original linked list is guaranteed to be immutable?
Theo In that case, I could create a new list with a new head that points to the head of
the original list.
Theo goes to the classroom blackboard. He picks up a piece of chalk and draws the dia-
gram shown in figure 9.1.
New list Original list
Figure 9.1 Structural sharing
0 1 2 3 4 5 with linked lists
Joe Would the efficiency of this operation depend on the size of the list?
Theo No, it would be efficient, no matter the size of the list.
Joe That’s what I mean by structural sharing at the level of the data structure itself.
It relies on a simple but powerful insight—when data is immutable, it is safe to
share it.
TIP When data is immutable, it is safe to share it.

=== PAGE 208 ===
180 CHAPTER 9 Persistent data structures
Theo I understand how to use structural sharing at the level of the data structure for
linked lists and prepend operations, but how would it work with operations
like appending or modifying an element in a list?
Joe For that purpose, we need to be smarter and represent our list as a tree.
Theo How does that help?
Joe It helps because when a list is represented as a tree, most of the nodes in the
tree can be shared between two versions of the list.
Theo I am totally confused.
Joe Imagine that you take a list with 100,000 elements and split it into two lists of
50,000 elements each: elements 0 to 49,999 in list 1, and elements 50,000 to
99,999 in list 2. How many operations would you need to create a new version
of the list where a single element—let’s say, element at index 75,100—is
modified?
It’s hard for Theo to visualize this kind of stuff mentally. He goes back to the blackboard
and draws a diagram (see figure 9.2). Once Theo looks at the diagram, it’s easy for him to
answer Joe’s question.
List «Next»
List
List 1 List 2
«Next»
0...49,999 50,000...99,999
List 2
Figure 9.2 Structural sharing when
50,000...99,999
a list of 100,000 elements is split
Theo List 1 could be shared with one operation. I’d need to create a new version of
list 2, where element 75,100 is modified. It would take 50,000 operations, so it’s
one operation of sharing and one operation of copying 50,000 elements. Over-
all, it’s 50,001 operations.
Joe Correct. You see that by splitting our original list into two lists, we can create a
new version of the list with a number of operations in the order of the size of
the list divided by 2.
Theo I agree, but 50,000 is still a big number.
Joe Indeed, but nobody prevents us from applying the same trick again, splitting
list 1 and list 2 in two lists each.
Theo How exactly?
Joe We can make list 1.1 with elements 0 to 24,999, then list 1.2 with elements
25,000 to 49,999, list 2.1 with elements 50,000 to 74,999, and list 2.2 with ele-
ments 75,000 to 99,999.
Theo Can you draw that on the blackboard?
Joe Sure.

=== PAGE 209 ===
9.2 The efficiency of persistent data structures 181
Now, it’s Joe that goes to the blackboard. He draws the diagram in figure 9.3.
«Next»
List
List
«Next»
List 1 List 2 List 2
List 1.1 List 1.2 List 2.1 List 2.2 «Next»
0...24,499 25,000...49,999 50,000...74,999 75,000...99,999 List 2.2
75,000...99,999
Figure 9.3 Structural sharing when a list of 100,000 elements is split twice
Theo Let me count the number of operations for updating a single element. It takes
2 operations of sharing and 1 operation of copying 25,000 elements. Overall, it
takes 25,002 operations to create a new version of the list.
Joe Correct!
Theo Let’s split the list again then!
Joe Absolutely. In fact, we can split the list again and again until the size of the
lists is at most 2. Can you guess what is the complexity of creating a new ver-
sion then?
Theo I’d say around log2 N operations.
Joe I see that you remember well your material from school. Do you have a gut
feeling about what is log2 N when N is 100,000?
Theo Let me see...2 to the power of 10 is around 1,000, and 2 to the power of 7 is
128. So, it should be a bit less than 17.
Joe It’s 16.6 to be precise. It means that in order to update an element in a per-
sistent list of 100,000 elements, we need around 17 operations. The same goes
for accessing elements.
Theo Nice, but 17 is still not negligible.
Joe I agree. We can easily improve the performance of accessing elements by using
a higher branching factor in our tree.
Theo What do you mean?
Joe Instead of splitting by 2 at each level, we could split by 32.
Theo But the running time of our algorithm would still grow with log N.
Joe You’re right. From a theoretical perspective, it’s the same. From a practical
perspective, however, it makes a big difference.
Theo Why?
Joe Because log32 N is 5 times lower than log2 N.

=== PAGE 210 ===
182 CHAPTER 9 Persistent data structures
Theo That’s true: 2 to the power of 5 is 32.
Joe Back to our list of 100,000 elements, can you tell me how many operations are
required to access an element if the branching factor is 32?
Theo With a branching factor of 2, it was 16.6. If I divide 16.6 by 5, I get 3.3.
Joe Correct!
TIP By using a branching factor of 32, we make elements accessed in persistent lists
more efficient.
Theo Does this trick also improve the performance of updating an element in a list?
Joe Yes, indeed, it does.
Theo How? We’d have to copy 32 elements at each level instead of 2 elements. It’s a
16× performance hit that’s not compensated for by the fact that the tree depth
is reduced by 5×!
Joe I see that you are quite sharp with numbers. There is another thing to take
into consideration in our practical analysis of the performance: modern CPU
architecture.
Theo Interesting. The more you tell me about persistent data structures, the more I
understand why you wanted to have this session at a university: it’s because
we’re dealing with all this academic stuff.
Joe Yep. So, to continue, modern CPUs read and write data from and to the main
memory in units of cache lines, often 32 or 64 bytes long.
Theo What difference does that make?
Joe A nice consequence of this data access pattern is that copying an array of size
32 is much faster than copying 16 arrays of size 2 that belong to different levels
of the tree.
Theo Why is that?
Joe The reason is that copying an array of size 32 can be done in a single pair of
cache accesses: one for read and one for write. Although for arrays that belong
to different tree levels, each array requires its own pair of cache accesses, even
if there are only 2 elements in the array.
Theo In other words, the performance of updating a persistent list is dominated by
the depth of the tree.
TIP In modern CPU architectures, the performance of updating a persistent list is
dominated much more by the depth of the tree than by the number of nodes at each
level of the tree.
Joe That’s correct, up to a certain point. With today’s CPUs, using a branching fac-
tor of 64 would, in fact, decrease the performance of update operations.
Theo I see.
Joe Now, I am going to make another interesting claim that is not accurate from a
theoretical perspective but accurate in practice.
Theo What is it?

=== PAGE 211 ===
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

=== PAGE 212 ===
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

=== PAGE 213 ===
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

=== PAGE 214 ===
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

=== PAGE 215 ===
9.3 Persistent data structures libraries 187
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
}
});
Theo Do you mean that the catalog value in libraryData map is itself an immutable
map?
Joe Yes, and the same for booksByIsbn, authorIds, and so forth.
Theo Cool! So how do I access a field inside an immutable map?
Joe As I told you, Immutable.js provides its own API for data access. For instance,
in order to access a field inside an immutable map, you use Immutable.get()
or Immutable.getIn() like the following.
Listing9.10 Accessing a field and a nested field in an immutable map
Immutable.get(libraryData, "catalog");
Immutable.getIn(libraryData,
["catalog", "booksByIsbn", "978-1779501127", "title"]);
// → "Watchmen"
Theo How do I make a modification to a map?
Joe Similar to what we did with Lodash FP, you use an Immutable.set() or
Immutable.setIn() map to create a new version of the map where a field is
modified. Here’s how.
Listing9.11 Creating a new version of a map where a field is modified
Immutable.setIn(libraryData,
["catalog", "booksByIsbn",
"978-1779501127", "publicationYear"],
1988);
Theo What happens when I try to access a field in the map using JavaScript’s dot or
bracket notation?
Joe You access the internal representation of the map instead of accessing a map
field.
Theo Does that mean that we can’t pass data from Immutable.js to Lodash for data
manipulation?
Joe Yes, but it’s quite easy to convert any immutable collection into a native Java-
Script object back and forth.
Theo How?
Joe Immutable.js provides a toJS() method to convert an arbitrary deeply nested
immutable collection into a JavaScript object.

=== PAGE 216 ===
188 CHAPTER 9 Persistent data structures
Theo But if I have a huge collection, it could take lots of time to convert it, right?
Joe True. We need a better solution. Hopefully, Immutable.js provides its own set
of data manipulation functions like map(), filter(), and reduce().
Theo What if I need more data manipulation like Lodash’s _.groupBy()?
Joe You could write your own data manipulation functions that work with the
Immutable.js collections or use a library like mudash, which provides a port of
Lodash to Immutable.js.
 NOTE You can access the mudash library at https://github.com/brianneisler/mudash.
Theo What would you advise?
Joe A cup of coffee, then I’ll show you how to port functions from Lodash to
Immutable.js and how to adapt the code from your Library Management System.
You can decide on whichever approach works best for your current project.
9.4 Persistent data structures in action
Joe Let’s start with our search query. Can you look at the current code and tell me
the Lodash functions that we used to implement the search query?
Theo Including the code for the unit tests?
Joe Of course!
 NOTE See chapter 6 for the unit test of the search query.
9.4.1 Writing queries with persistent data structures
Theo The Lodash functions we used were get, map, filter, and isEqual.
Joe Here’s the port of those four functions from Lodash to Immutable.js.
Listing9.12 Porting some functions from Lodash to Immutable.js
Immutable.map = function(coll, f) {
return coll.map(f);
};
Immutable.filter = function(coll, f) {
if(Immutable.isMap(coll)) {
return coll.valueSeq().filter(f);
}
return coll.filter(f);
};
Immutable.isEqual = Immutable.is;
Theo The code seems quite simple. But can you explain it to me, function by function?
Joe Sure. Let’s start with get. For accessing a field in a map, Immutable.js provides
two functions: get for direct fields and getIn for nested fields. It’s different
from Lodash, where _.get works both on direct and nested fields.

=== PAGE 217 ===
9.4 Persistent data structures in action 189
Theo What about map?
Joe Immutable.js provides its own map function. The only difference is that it is a
method of the collection, but it is something that we can easily adapt.
Theo What about filter? How would you make it work both for arrays and maps
like Lodash’s filter?
Joe Immutable.js provides a valueSeq method that returns the values of a map.
Theo Cool. And what about isEqual to compare two collections?
Joe That’s easy. Immutable.js provides a function named is that works exactly as
isEqual.
Theo So far, so good. What do I need to do now to make the code of the search
query work with Immutable.js?
Joe You simply replace each occurrence of an _ with Immutable; _.map becomes
Immutable.map, _.filter becomes Immutable.filter, and _.isEqual
becomes Immutable.isEqual.
Theo I can’t believe it’s so easy!
Joe Try it yourself; you’ll see. Sometimes, it’s a bit more cumbersome because
you need to convert the JavaScript objects to Immutable.js objects using
Immutable.fromJS.
Theo copies and pastes the snippets for the code and the unit tests of the search query.
Then, he uses his IDE to replace the _ with Immutable. When Theo executes the tests and
they pass, he is surprised but satisfied. Joe smiles.
Listing9.13 Implementing book search with persistent data structures
class Catalog {
static authorNames(catalogData, authorIds) {
return Immutable.map(authorIds, function(authorId) {
return Immutable.getIn(
catalogData,
["authorsById", authorId, "name"]);
});
}
static bookInfo(catalogData, book) {
var bookInfo = Immutable.Map({
"title": Immutable.get(book, "title"),
"isbn": Immutable.get(book, "isbn"),
"authorNames": Catalog.authorNames(
catalogData,
Immutable.get(book, "authorIds"))
});
return bookInfo;
}
static searchBooksByTitle(catalogData, query) {
var allBooks = Immutable.get(catalogData, "booksByIsbn");
var queryLowerCased = query.toLowerCase();
var matchingBooks = Immutable.filter(allBooks, function(book) {

=== PAGE 218 ===
190 CHAPTER 9 Persistent data structures
return Immutable.get(book, "title").
toLowerCase().
includes(queryLowerCased);
});
var bookInfos = Immutable.map(matchingBooks, function(book) {
return Catalog.bookInfo(catalogData, book);
});
return bookInfos;
}
}
Listing9.14 Testing book search with persistent data structures
var catalogData = Immutable.fromJS({
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
"bookIsbns": ["978-1779501127"]
},
"dave-gibbons": {
"name": "Dave Gibbons",
"bookIsbns": ["978-1779501127"]
}
}
});
var bookInfo = Immutable.fromJS({
"isbn": "978-1779501127",
"title": "Watchmen",
"authorNames": ["Alan Moore",
"Dave Gibbons"]
});
Immutable.isEqual(
Catalog.searchBooksByTitle(catalogData, "Watchmen"),
Immutable.fromJS([bookInfo]));
// → true
Immutable.isEqual(
Catalog.searchBooksByTitle(catalogData, "Batman"),
Immutable.fromJS([]));
// → true

=== PAGE 219 ===
9.4 Persistent data structures in action 191
9.4.2 Writing mutations with persistent data structures
Theo Shall we move forward and port the add member mutation?
Joe Sure. Porting the add member mutation from Lodash to Immutable.js only
requires you to again replace the underscore (_) with Immutable. Let’s look at
some code.
Listing9.15 Implementing member addition with persistent data structures
UserManagement.addMember = function(userManagement, member) {
var email = Immutable.get(member, "email");
var infoPath = ["membersByEmail", email];
if(Immutable.hasIn(userManagement, infoPath)) {
throw "Member already exists.";
}
var nextUserManagement = Immutable.setIn(userManagement,
infoPath,
member);
return nextUserManagement;
};
Theo So, for the tests, I’d convert the JavaScript objects to Immutable.js objects with
Immutable.fromJS(). How does this look?
Listing9.16 Testing member addition with persistent data structures
var jessie = Immutable.fromJS({
"email": "jessie@gmail.com",
"password": "my-secret"
});
var franck = Immutable.fromJS({
"email": "franck@gmail.com",
"password": "my-top-secret"
});
var userManagementStateBefore = Immutable.fromJS({
"membersByEmail": {
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
});
var expectedUserManagementStateAfter = Immutable.fromJS({
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"

=== PAGE 220 ===
192 CHAPTER 9 Persistent data structures
}
}
});
var result = UserManagement.addMember(userManagementStateBefore, jessie);
Immutable.isEqual(result, expectedUserManagementStateAfter);
// → true
Joe Great!
9.4.3 Serialization and deserialization
Theo Does Immutable.js also support JSON serialization and deserialization?
Joe It supports serialization out of the box. As for deserialization, we need to write
our own function.
Theo Does Immutable.js provide an Immutable.stringify() function?
Joe That’s not necessary because the native JSON.stringify() function works
with Immutable.js objects. Here’s another example.
Listing9.17 JSON serialization of an Immutable.js collection
var bookInfo = Immutable.fromJS({
"isbn": "978-1779501127",
"title": "Watchmen",
"authorNames": ["Alan Moore",
"Dave Gibbons"]
});
JSON.stringify(bookInfo);
// → {\"isbn\":\"978-1779501127\",\"title\":\"Watchmen\",
// → \"authorNames\":[\"Alan Moore\",\"Dave Gibbons\"]}
Theo How does JSON.stringify() know how to handle an Immutable.js collection?
Joe As an OOP developer, you shouldn’t be surprised by that.
Theo Hmm...let me think a minute. OK, here’s my guess. Is that because JSON
.stringify() calls some method on its argument?
Joe Exactly! If the object passed to JSON.stringify() has a .toJSON() method,
it’s called by JSON.stringify().
Theo Nice. What about JSON deserialization?
Joe That needs to be done in two steps. You first convert the JSON string to a Java-
Script object and then to an immutable collection.
Theo Something like this piece of code?
Listing9.18 Converting a JSON string into an immutable collection
Immutable.parseJSON = function(jsonString) {
return Immutable.fromJS(JSON.parse(jsonString));
};
Joe Exactly.

=== PAGE 221 ===
9.4 Persistent data structures in action 193
9.4.4 Structural diff
Theo So far, we have ported pieces of code that dealt with simple data manipula-
tions. I’m curious to see how it goes with complex data manipulations such as
the code that computes the structural diff between two maps.
 NOTE Chapter 5 introduces structural diff.
Joe That also works smoothly, but we need to port another eight functions.
Listing9.19 Porting Lodash functions involved in structural diff computation
Immutable.reduce = function(coll, reducer, initialReduction) {
return coll.reduce(reducer, initialReduction);
};
Immutable.isEmpty = function(coll) {
return coll.isEmpty();
};
Immutable.keys = function(coll) {
return coll.keySeq();
};
Immutable.isObject = function(coll) {
return Immutable.Map.isMap(coll);
};
Immutable.isArray = Immutable.isIndexed;
Immutable.union = function() {
return Immutable.Set.union(arguments);
};
Theo Everything looks trivial with one exception: the use of arguments in Immutable
.union.
Joe In JavaScript, arguments is an implicit array-like object that contains the values
of the function arguments.
Theo I see. It’s one of those pieces of JavaScript magic!
Joe Yep. We need to use arguments because Lodash and Immutable.js differ slightly
in the signature of the union function. Immutable.Set.union receives an array
of lists, whereas a Lodash _.union receives several arrays.
Theo Makes sense. Let me give it a try.
Blowing on his fingers like a seasoned safecracker, first one hand and then the next, Theo
begins typing. Once again, Theo is surprised to discover that after replacing the _ with
Immutable in listing 9.20, the tests pass with the code in listing 9.21.
Listing9.20 Implementing structural diff with persistent data structures
function diffObjects(data1, data2) {
var emptyObject = Immutable.isArray(data1) ?
Immutable.fromJS([]) :

=== PAGE 222 ===
194 CHAPTER 9 Persistent data structures
Immutable.fromJS({});
if(data1 == data2) {
return emptyObject;
}
var keys = Immutable.union(Immutable.keys(data1), Immutable.keys(data2));
return Immutable.reduce(keys,
function (acc, k) {
var res = diff(Immutable.get(data1, k),
Immutable.get(data2, k));
if((Immutable.isObject(res) && Immutable.isEmpty(res)) ||
(res == "data-diff:no-diff")) {
return acc;
}
return Immutable.set(acc, k, res);
},
emptyObject);
}
function diff(data1, data2) {
if(Immutable.isObject(data1) && Immutable.isObject(data2)) {
return diffObjects(data1, data2);
}
if(data1 !== data2) {
return data2;
}
return "data-diff:no-diff";
}
Listing9.21 Testing structural diff with persistent data structures
var data1 = Immutable.fromJS({
g: {
c: 3
},
x: 2,
y: {
z: 1
},
w: [5]
});
var data2 = Immutable.fromJS({
g: {
c:3
},
x: 2,
y: {
z: 2
},
w: [4]
});
Immutable.isEqual(diff(data1, data2),
Immutable.fromJS({

=== PAGE 223 ===
Summary 195
"w": [
4
],
"y": {
"z": 2
}
}));
Joe What do you think of all this, my friend?
Theo I think that using persistent data collections with a library like Immutable.js is
much easier than understanding the internals of persistent data structures. But
I’m also glad that I know how it works under the hood.
After accompanying Joe to the office door, Theo meets Dave. Dave had been peering
through the window in Theo’s office, looking at the whiteboard, anxious to catch a glimpse
of today’s topic on DOP.
Dave What did Joe teach you today?
Theo He took me to the university and taught me the foundations of persistent data
structures for dealing with immutability at scale.
Dave What’s wrong with the structural sharing that I implemented a couple of
months ago?
Theo When the number of elements in the collection is big enough, naive structural
sharing has performance issues.
Dave I see. Could you tell me more about that?
Theo I’d love to, but my brain isn’t functioning properly after this interesting but
exhausting day. We’ll do it soon, promise.
Dave No worries. Have a nice evening, Theo.
Theo You too, Dave.
Summary
 It’s possible to manually ensure that our data isn’t mutated, but it’s cumbersome.
 At scale, naive structural sharing causes a performance hit, both in terms of
memory and computation.
 Naive structural sharing doesn’t prevent data structures from being accidentally
mutated.
 Immutable collections are not the same as persistent data structures.
 Immutable collections don’t provide an efficient way to create new versions of
the collections.
 Persistent data structures protect data from mutation.
 Persistent data structures provide an efficient way to create new versions of the
collections.
 Persistent data structures always preserve the previous version of themselves when
they are modified.

=== PAGE 224 ===
196 CHAPTER 9 Persistent data structures
 Persistent data structures represent data internally in such a way that structural
sharing scales well, both in terms of memory and computation.
 When data is immutable, it is safe to share it.
 Internally, persistence uses a branching factor of 32.
 In practice, manipulation of persistent data structures is efficient even for col-
lections with 10 billion entries!
 Due to modern architecture considerations, the performance of updating a
persistent list is dominated much more by the depth of the tree than by the
number of nodes at each level of the tree.
 Persistent lists can be manipulated in near constant time.
 In most languages, third-party libraries provide an implementation of persistent
data structures.
 Paguro collections implement the read-only parts of Java collection interfaces.
 Paguro collections can be passed to any methods that expect to receive a Java
collection without mutating them.