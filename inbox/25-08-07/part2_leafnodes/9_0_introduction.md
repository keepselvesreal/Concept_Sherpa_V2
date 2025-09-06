# 9.0 Introduction (사용자 추가)

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