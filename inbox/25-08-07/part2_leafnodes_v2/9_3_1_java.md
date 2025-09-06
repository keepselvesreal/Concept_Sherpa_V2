# 9.3.1 Persistent data structures in Java

9.3.1 Persistent data structures in Java
Joe In an object-oriented language like Java, it’s quite straightforward to integrate
persistent data structures in a program because persistent data structures
implement collection interfaces, besides the parts of the interface that mutate
in place.
Theo What do you mean?

## 페이지 213

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

## 페이지 214

186 CHAPTER 9 Persistent data structures
Listing9.8 Creating a modified version of a Paguro map
var myMap = PersistentHashMap.of(Map.of("aa", 1, "bb", 2)
.entrySet());
Creates a Paguro map
from a Java map entry set
var myNextMap = myMap.assoc("aa", 42);
Theo Yes! Now I see how to use persistent data structures in Java, but what about
JavaScript?