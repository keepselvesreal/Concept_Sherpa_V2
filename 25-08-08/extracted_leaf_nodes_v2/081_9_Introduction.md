# 9 Introduction

**메타데이터:**
- ID: 81
- 레벨: 2
- 페이지: 203-204
- 페이지 수: 2
- 부모 ID: 80
- 텍스트 길이: 6325 문자

---

=== Page 202 ===
174 CHAPTER 8 Advanced concurrency control
Joe Perfect.
Theo This atom stuff makes me think about what happened to us yesterday, when we
tried to call each other at the exact same time.
Joe What do you mean?
Theo I don’t know, but I am under the impression that mutexes are like phone calls,
and atoms are like text messages.
Joe smiles at Theo but doesn’t reveal the meaning of his smile. After the phone deadlock
yesterday, Theo’s pretty sure that he and Joe are on the same page.
Summary
 Managing concurrency with atoms is much simpler than managing concur-
rency with locks because we don’t have to deal with the risk of deadlocks.
 Cloning data to avoid read locks doesn’t scale.
 When data is immutable, reads are always safe.
 Atoms provide a way to manage concurrency without locks.
 With atoms, deadlocks never happen.
 Using atoms for a thread-safe counter is trivial because the state of the counter
is represented with a primitive type (an integer).
 We can manage composite data in a thread-safe way with atoms.
 We make the highly scalable state management approach from part 1 thread-
safe by keeping the whole system state inside an atom.
 It’s quite common to represent an in-memory cache as a string map.
 When data is immutable, it is safe (and fast) to compare by reference.
 In theory, atoms could create starvation in a system with thousands of threads
that do nothing besides swapping an atom.
 In practice, once an atom is swapped, the threads do some real work (e.g.,
database access) to provide an opportunity for other threads to swap the atom
successfully.

=== Page 203 ===
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

=== Page 204 ===
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

=== Page 205 ===
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