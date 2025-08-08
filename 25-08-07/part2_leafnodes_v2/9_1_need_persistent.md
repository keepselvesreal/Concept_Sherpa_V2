# 9.1 The need for persistent data structures

9.1 The need for persistent data structures
It’s at the university where Theo meets Joe this time. When Theo asks Joe if today’s topic
is academic in nature, Joe tells him that the use of persistent data structures only
became possible in programming languages following a discovery in 2001 by a computer
175

## 페이지 204

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

## 페이지 205

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

## 페이지 206

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