# Chapter 5: Basic concurrency control

**부제목:** Conflicts at home
**계획된 페이지:** 119-137
**실제 페이지:** 119-137

=== PAGE 119 ===
Basic concurrency control
Conflicts at home
This chapter covers
 Managing concurrent mutations with a lock-free
optimistic concurrency control strategy
 Supporting high throughput of reads and writes
 Reconciliation between concurrent mutations
The changes required for system manage concurrency are only in the commit
phase. They involve a reconciliation algorithm that is universal, in the sense that it
can be used in any system where data is represented as an immutable hash map.
The implementation of the reconciliation algorithm is efficient because subse-
quent versions of the system state are created via structural sharing.
In the previous chapter, we illustrated the multiversion approach to state man-
agement, where a mutation is split into two distinct phases: the calculation phase
that deals only with computation, and the commit phase that moves the state ref-
erence forward. Usually, in a production system, mutations occur concurrently.
Moving the state forward naively like we did in the previous chapter is not appro-
priate. In the present chapter, we are going to learn how to handle concurrent
mutations.
91

=== PAGE 120 ===
92 CHAPTER 5 Basic concurrency control
In DOP, because only the code of the commit phase is stateful, that allows us to use
an optimistic concurrency control strategy that doesn’t involve any locking mechanism. As
a consequence, the throughput of reads and writes is high. The modifications to the
code are not trivial, as we have to implement an algorithm that reconciles concurrent
mutations. But the modifications impact only the commit phase. The code for the cal-
culation phase stays the same as in the previous chapter.
 NOTE This chapter requires more of an effort to grasp. The flow of the reconcilia-
tion algorithm is definitely not trivial, and the implementation involves a nontrivial
recursion.
5.1 Optimistic concurrency control
This morning, before getting to work, Theo takes Joe to the fitness room in the office and,
while running on the step machine, the two men talk about their personal lives again. Joe
talks about a fight he had last night with Kay, who thinks that he pays more attention to his
work than to his family. Theo recounts the painful conflict he had with Jane, his wife,
about house budget management. They went to see a therapist, an expert in Imago Rela-
tionship Therapy. Imago allowed them to transform their conflict into an opportunity to
grow and heal.
Joe’s ears perk up when he hears the word conflict because today’s lesson is going to be
about resolving conflicts and concurrent mutations. A different kind of conflict, though....
After a shower and a healthy breakfast, Theo and Joe get down to work.
Joe Yesterday, I showed you how to manage state with immutable data, assuming
that no mutations occur concurrently. Today, I am going to show you how to
deal with concurrency control in DOP.
Theo I’m curious to discover what kind of lock mechanisms you use in DOP to syn-
chronize concurrent mutations.
Joe In fact, we don’t use any lock mechanism!
Theo Why not?
Joe Locks hit performance, and if you’re not careful, your system could get into a
deadlock.
Theo So, how do you handle possible conflicts between concurrent mutations in
DOP?
Joe In DOP, we use a lock-free strategy called optimistic concurrency control. It’s a
strategy that allows databases like Elasticsearch to be highly scalable.
 NOTE See https://www.elastic.co/elasticsearch/ to find out more about Elastic-
search.
Theo You sound like my couples therapist and her anger-free, optimistic conflict
resolution strategy.
Joe Optimistic concurrency control and DOP fit together well. As you will see in a
moment, optimistic concurrency control is super efficient when the system
data is immutable.

=== PAGE 121 ===
5.1 Optimistic concurrency control 93
TIP Optimistic concurrency control with immutable data is super efficient.
Theo How does it work?
Joe Optimistic concurrency control occurs when we let mutations ask forgiveness
instead of permission.
TIP Optimistic concurrency control occurs when we let mutations ask forgiveness
instead of permission.
Theo What do you mean?
Joe The calculation phase does its calculation as if it were the only mutation run-
ning. The commit phase is responsible for reconciling concurrent mutations
when they don’t conflict or for aborting the mutation.
TIP The calculation phase does its calculation as if it were the only mutation running.
The commit phase is responsible for trying to reconcile concurrent mutations.
Theo That sounds quite challenging to implement.
Joe Dealing with state is never trivial. But the good news is that the code for the
reconciliation logic in the commit phase is universal.
Theo Does that mean that the same code for the commit phase can be used in any
DOP system?
Joe Definitely. The code that implements the commit phase assumes nothing
about the details of the system except that the system data is represented as an
immutable map.
TIP The implementation of the commit phase in optimistic concurrency control is
universal. It can be used in any system where the data is represented by an immutable
hash map.
Theo That’s awesome!
Joe Another cool thing is that handling concurrency doesn’t require any changes
to the code in the calculation phase. From the calculation phase perspective,
the next version of the system data is computed in isolation as if no other muta-
tions were running concurrently.
Joe stands up to illustrate what he means on the whiteboard. While Theo looks at the draw-
ing in figure 5.1, Joe summarizes the information in table 5.1.
Table 5.1 The two phases of a mutation with optimistic concurrency control
Phase Responsibility State Implementation
Calculation Compute next state in isolation Stateless Specific
Commit Reconcile and update system state Stateful Common

=== PAGE 122 ===
94 CHAPTER 5 Basic concurrency control
Calculation phase
Capturesystem state
Computenext version
Commit phase
Yes No
Concurrent mutations?
Yes No
Conflict?
Updatesystem state
Abortmutation Reconcilemutations
Updatesystem state
Figure 5.1 The logic flow
of optimistic concurrency
control
5.2 Reconciliation between concurrent mutations
Theo Could you give me some examples of conflicting concurrent mutations?
Joe Sure. One example would be two members trying to borrow the same book
copy. Another example might be when two librarians update the publication
year of the same book.
Theo You mentioned that the code for the reconciliation logic in the commit phase
is universal. What do you mean exactly by reconciliation logic?
Joe It’s quite similar to what could happen in Git when you merge a branch back
into the main branch.
Theo I love it when the main branch stays the same.
Joe Yes, it’s nice when the merge has no conflicts and can be done automatically.
Do you remember how Git handles the merge in that case?
Theo Git does a fast-forward; it updates the main branch to be the same as the merge
branch.
Joe Right! And what happens when you discover that, meanwhile, another devel-
oper has committed their code to the main branch?
Theo Then Git does a three-way merge, trying to combine all the changes from the
two merge branches with the main branch.
Joe Does it always go smoothly?
Theo Usually, yes, but it’s possible that two developers have modified the same line
in the same file. I then have to manually resolve the conflict. I hate when that
happens!
TIP In a production system, multiple mutations run concurrently. Before updating
the state, we need to reconcile the conflicts between possible concurrent mutations.

=== PAGE 123 ===
5.2 Reconciliation between concurrent mutations 95
Joe In DOP, the reconciliation algorithm in the commit phase is quite similar to a
merge in Git, except instead of a manual conflict resolution, we abort the
mutation. There are three possibilities to reconcile between possible concur-
rent mutations: fast-forward, three-way merge, or abort.
Joe goes to the whiteboard again. He draws the two diagrams shown in figures 5.2 and 5.3.
Yes No
State has stayed the same
Yes No
Concurrent mutations compatible?
Fast forward
3-way Merge Abort
Figure 5.2 The
reconciliation flow
The version during
the Commit phase
current
previous
next
The base version
for the Calculation
The version Figure 5.3 When the commit phase
phase
returned by the starts, there are three versions of the
Calculation phase system state.
Theo Could you explain in more detail?
Joe When the commit phase of a mutation starts, we have three versions of the sys-
tem state: previous, which is the version on which the calculation phase based
its computation; current, which is the current version during the commit
phase; and next, which is the version returned by the calculation phase.
Theo Why would current be different than previous?
Joe It happens when other mutations have run concurrently with our mutation.
Theo I see.
Joe If we are in a situation where the current state is the same as the previous state,
it means that no mutations run concurrently. Therefore, as in Git, we can
safely fast-forward and update the state of the system with the next version.
Theo What if the state has not stayed the same?
Joe Then it means that mutations have run concurrently. We have to check for
conflicts in a way similar to the three-way merge used by Git. The difference is
that instead of comparing lines, we compare fields of the system hash map.
Theo Could you explain that?

=== PAGE 124 ===
96 CHAPTER 5 Basic concurrency control
Joe We calculate the diff between previous and next and between previous and
current. If the two diffs have no fields in common, then there is no conflict
between the mutations that have run concurrently. We can safely apply the
changes from previous to next into current.
Joe makes his explanation visual with another diagram on the whiteboard. He then shows
figure 5.4 to Theo.
diffPreviousCurrent diffPreviousNext
current
previous merged
diffPreviousNext
next
Figure 5.4 In a three-way merge, we calculate the diff between previous and
next, and we apply it to current.
Theo What if there is a conflict?
Joe Then we abort the mutation.
Theo Aborting a user request seems unacceptable.
Joe In fact, in a user-facing system, conflicting concurrent mutations are fairly rare.
That’s why it’s OK to abort and let the user run the mutation again. Here, let
me draft a table to show you the differences between Git and DOP (table 5.2).
Table 5.2 The analogy between Git and data-oriented programming
Data-oriented programming Git
Concurrent mutations Different branches
A version of the system data A commit
State A reference
Calculation phase Branching
Validation Precommit hook
Reconciliation Merge
Fast-forward Fast-forward
Three-way merge Three-way merge
Abort Manual conflict resolution
Hash map Tree (folder)
Leaf node Blob (file)
Data field Line of code

=== PAGE 125 ===
5.3 Reducing collections 97
Theo Great! That helps, but in cases where two mutations update the same field of
the same entity, I think it’s fair enough to let the user know that the request
can’t be processed.
TIP In a user-facing system, conflicting concurrent mutations are fairly rare.
5.3 Reducing collections
Joe Are you ready to challenge your mind with the implementation of the diff
algorithm?
Theo Let’s take a short coffee break before, if you don’t mind. Then, I’ll be ready to
tackle anything.
After enjoying large mug of hot coffee and a few butter cookies, Theo and Joe are back to
work. Their discussion on the diff algorithm continues.
Joe In the implementation of the diff algorithm, we’re going to reduce collections.
Theo I heard about reducing collections in a talk about FP, but I don’t remember
the details. Could you remind me how this works?
Joe Imagine you want to calculate the sum of the elements in a collection of num-
bers. With Lodash’s _.reduce, it would look like this.
Listing5.1 Summing numbers with _.reduce
_.reduce([1, 2, 3], function(res, elem) {
return res + elem;
}, 0);
// → 6
Theo I don’t understand.
Joe goes to the whiteboard and writes the description of _.reduce. Theo waits patiently
until Joe puts the pen down before looking at the description.
Description of _.reduce
_.reduce receives three arguments:
 coll—A collection of elements
 f—A function that receives two arguments
 initVal—A value
Logic flow:
1 Initialize currentRes with initVal.
2 For each element x of coll, update currentRes with f(currentRes, x).
3 Return currentRes.

=== PAGE 126 ===
98 CHAPTER 5 Basic concurrency control
Theo Would you mind if I manually expand the logic flow of that code you just wrote
for _.reduce?
Joe I think it’s a great idea!
Theo In our case, initVal is 0. It means that the first call to f will be f(0, 1). Then,
we’ll have f(f(0, 1), 2) and, finally, f(f(f(0, 1), 2), 3).
Joe I like your manual expansion, Theo! Let’s make it visual.
Now Theo goes to the whiteboard and draws a diagram. Figure 5.5 shows what that looks like.
f
f a
2
f a
1
a 0 initVal Figure 5.5 Visualization
of _.reduce
Theo It’s much clearer now. I think that by implementing my custom version of
_.reduce, it will make things 100% clear.
It takes Theo much less time than he expected to implement reduce(). In no time at all,
he shows Joe the code.
Listing5.2 Custom implementation of _.reduce
function reduce(coll, f, initVal) {
var currentRes = initVal;
for (var i = 0; i < coll.length; i++) {
We could use
currentRes = f(currentRes, coll[i])
forEach instead
}
of a for loop.
return currentRes;
}
After checking that Theo’s code works as expected (see listing 5.3), Joe is proud of Theo.
He seems to be catching on better than he anticipated.
Listing5.3 Testing the custom implementation of reduce()
reduce([1, 2, 3], function(res, elem) {
return res + elem;
}, 0);
// → 6
Joe Well done!

=== PAGE 127 ===
5.4 Structural difference 99
5.4 Structural difference
 NOTE This section deals with the implementation of a structural diff algorithm. Feel
free to skip this section if you don’t want to challenge your mind right now with the
details of a sophisticated use of recursion. It won’t prevent you from enjoying the rest
of the book. You can come back to this section later.
Theo How do you calculate the diff between various versions of the system state?
Joe That’s the most challenging part of the reconciliation algorithm. We need to
implement a structural diff algorithm for hash maps.
Theo In what sense is the diff structural?
Joe The structural diff algorithm looks at the structure of the hash maps and
ignores the order of the fields.
Theo Could you give me an example?
Joe Let’s start with maps without nested fields. Basically, there are three kinds of
diffs: field replacement, field addition, and field deletion. In order to make
things not too complicated, for now, we’ll deal only with replacement and
addition.
Joe once again goes to the whiteboard and draws table 5.3, representing the three kinds of
diffs. Theo is thinking the whiteboard is really starting to fill up today.
Table 5.3 Kinds of structural differences between maps without nested fields
Kind First map Second map Diff
Replacement {"a": 1} {"a": 2} {"a": 2}
Addition {"a": 1} {"a": 1, "b": 2} {"b": 2}
Deletion {"a": 1, "b": 2} {"a": 1} Not supported
Theo I notice that the order of the maps matters a lot. What about nested fields?
Joe It’s the same idea, but the nesting makes it a bit more difficult to grasp.
Joe changes several of the columns in table 5.3. When he’s through, he shows Theo the
nested fields in table 5.4.
Table 5.4 Kinds of structural differences between maps with nested fields
Kind First map Second map Diff
Replacement { { {
"a": { "a": { "a": {
"x": 1 "x": 2 "x": 2
} } }
} } }

=== PAGE 128 ===
100 CHAPTER 5 Basic concurrency control
Table 5.4 Kinds of structural differences between maps with nested fields (continued)
Kind First map Second map Diff
Addition { { {
"a": { "a": { "a": {
"x": 1 "x": 1, "y": 2
} "y": 2, }
} } }
}
Deletion { { Not supported
"a": { "a": {
"x": 1, "y": 2
"y": 2, }
} }
}
 NOTE The version of the structural diff algorithm illustrated in this chapter does
not deal with deletions. Dealing with deletions is definitely possible, but it requires a
more complicated algorithm.
Theo As you said, it’s harder to grasp. What about arrays?
Joe We compare the elements of the arrays in order: if they are equal, the diff is
null; if they differ, the diff has the value of the second array.
Joe summarizes the various kinds of diffs in another table on the whiteboard. Theo looks
at the result in table 5.5.
Table 5.5 Kinds of structural differences between arrays without nested elements
Kind First array Second array Diff
Replacement [1] [2] [2]
Addition [1] [1, 2] [null, 2]
Deletion [1, 2] [1] Not supported
Theo This usage of null is a bit weird but OK. Is it complicated to implement the
structural diff algorithm?
Joe Definitely! It took a good dose of mental gymnastics to come up with these 30
lines of code.
Joe downloads the code from one his personal repositories. Theo, with thumb and forefin-
gers touching his chin and his forehead slightly tilted, studies the code.
Listing5.4 The implementation of a structural diff
function diffObjects(data1, data2) {
_.isArray checks whether
var emptyObject = _.isArray(data1) ? [] : {};
its argument is an array.
if(data1 == data2) {

=== PAGE 129 ===
5.4 Structural difference 101
return emptyObject;
_.union creates an
} array of unique
var keys = _.union(_.keys(data1), _.keys(data2)); values from two
return _.reduce(keys, arrays (like union of
function (acc, k) { two sets in Maths).
var res = diff(
_.get(data1, k),
_.isObject checks
_.get(data2, k));
whether its argument
if((_.isObject(res) && _.isEmpty(res)) ||
is a collection (either
a map or an array).
(res == "no-diff")) {
return acc;
_.isEmpty }
checks return _.set(acc, [k], res);
whether its },
argument
emptyObject);
is an empty
} "no-diff" is how
collection.
we mark that
function diff(data1, data2) { two values are
if(_.isObject(data1) && _.isObject(data2)) { the same.
return diffObjects(data1, data2);
}
if(data1 !== data2) {
return data2;
}
return "no-diff";
}
Theo Wow! It involves a recursion inside a reduce! I’m sure Dave will love this, but
I’m too tired to understand this code right now. Let’s focus on what it does
instead of how it does it.
In order familiarize himself with the structural diff algorithm, Theo runs the algorithm
with examples from the table that Joe drew on the whiteboard. While Theo occupies his
fingers with more and more complicated examples, his mind wanders in the realm of
performance.
Listing5.5 An example of usage of a structural diff
var data1 = {
"a": {
"x": 1,
"y": [2, 3],
"z": 4
}
};
var data2 = {
"a": {
"x": 2,
"y": [2, 4],
"z": 4
}
}

=== PAGE 130 ===
102 CHAPTER 5 Basic concurrency control
diff(data1, data2);
//{
// "a": {
// "x": 2,
// "y": [
// undefined,
// 4
// ]
// }
//}
Theo What about the performance of the structural diff algorithm? It seems that the
algorithm goes over the leaves of both pieces of data?
Joe In the general case, that’s true. But, in the case of system data that’s manipu-
lated with structural sharing, the code is much more efficient.
Theo What do you mean?
Joe With structural sharing, most of the nested objects are shared between two ver-
sions of the system state. Therefore, most of the time, when the code enters
diffObjects, it will immediately return because data1 and data2 are the same.
TIP Calculating the diff between two versions of the state is efficient because two
hash maps created via structural sharing from the same hash map have most of their
nodes in common.
Theo Another benefit of immutable data... Let me see how the diff algorithm
behaves with concurrent mutations. I think I’ll start with a tiny library with no
users and a catalog with a single book, Watchmen.
Listing5.6 The data for a tiny library
var library = {
"catalog": {
"booksByIsbn": {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore", "dave-gibbons"]
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
}
};

=== PAGE 131 ===
5.4 Structural difference 103
Joe I suggest that we start with nonconflicting mutations. What do you suggest?
Theo A mutation that updates the publication year of Watchmen and a mutation that
updates both the title of Watchmen and the name of the author of Watchmen.
On his laptop, Theo creates three versions of the library. He shows Joe his code, where one
mutation updates the publication year of Watchmen, and the other one updates the title of
Watchmen and the author’s name.
Listing5.7 Two nonconflicting mutations
var previous = library;
var next = _.set(
library,
["catalog", "booksByIsbn", "978-1779501127", "publicationYear"],
1986);
var libraryWithUpdatedTitle = _.set(
library,
["catalog", "booksByIsbn", "978-1779501127", "title"],
"The Watchmen");
var current = _.set(
libraryWithUpdatedTitle,
["catalog", "authorsById", "dave-gibbons", "name"],
"David Chester Gibbons");
Theo I’m curious to see what the diff between previous and current looks like.
Joe Run the code and you’ll see.
Theo runs the code snippets for the structural diff between previous and next and for
the structural diff between previous and current. His curiosity satisfied, Theo finds it’s
all beginning to make sense.
Listing5.8 Structural diff between maps with a single difference
diff(previous, next);
//{
// "catalog": {
// "booksByIsbn": {
// "978-1779501127": {
// "publicationYear": 1986
// }
// }
// }
//}
Listing5.9 Structural diff between maps with two differences
diff(previous, current);
//{
// "authorsById": {
// "dave-gibbons": {
// "name": "David Chester Gibbons",

=== PAGE 132 ===
104 CHAPTER 5 Basic concurrency control
// }
// },
// "catalog": {
// "booksByIsbn": {
// "978-1779501127": {
// "title": "The Watchmen"
// }
// }
// }
//}
//
Joe Can you give me the information path of the single field in the structural diff
between previous and next?
Theo It’s ["catalog", "booksByIsbn", "978-1779501127", "publicationYear"].
Joe Right. And what are the information paths of the fields in the structural diff
between previous and current?
Theo It’s ["catalog", "booksByIsbn", "978-1779501127", "title"] for the book
title and ["authorsById", "dave-gibbons", "name"] for the author’s name.
Joe Perfect! Now, can you figure out how to detect conflicting mutations by
inspecting the information paths of the structural diffs?
Theo We need to check if they have an information path in common or not.
Joe Exactly! If they have, it means the mutations are conflicting.
Theo But I have no idea how to write code that retrieves the information paths of a
nested map.
Joe Once again, it’s a nontrivial piece of code that involves a recursion inside a
reduce. Let me download another piece of code from my repository and show
it to you.
Listing5.10 Calculating the information paths of a (nested) map
function informationPaths (obj, path = []) {
return _.reduce(obj,
function(acc, v, k) {
if (_.isObject(v)) {
return _.concat(acc,
informationPaths(v,
_.concat(path, k)));
}
return _.concat(acc, [_.concat(path, k)]);
},
[]);
}
Theo Let me see if your code works as expected with the structural diffs of the
mutations.
Theo tests Joe’s code with two code snippets. The first shows the information paths of the
structural diff between previous and next, and the second shows the information paths
of the structural diff between previous and current.

=== PAGE 133 ===
5.4 Structural difference 105
Listing5.11 Fields that differ between previous and next
informationPaths(diff(previous, next));
// → ["catalog.booksByIsbn.978-1779501127.publicationYear"]
Listing5.12 Fields that differ between previous and current
informationPaths(diff(previous, current));
// [
// [
// "catalog",
// "booksByIsbn",
// "978-1779501127",
// "title"
// ],
// [
// "authorsById",
// "dave-gibbons",
// "name"
// ]
//]
Theo Nice! I assume that Lodash has a function that checks whether two arrays have
an element in common.
Joe Almost. There is _.intersection, which returns an array of the unique values
that are in two given arrays. For our purpose, though, we need to check
whether the intersection is empty. Here, look at this example.
Listing5.13 Checking whether two diff maps have a common information path
function havePathInCommon(diff1, diff2) {
return !_.isEmpty(_.intersection(informationPaths(diff1),
informationPaths(diff2)));
}
Theo You told me earlier that in the case of nonconflicting mutations, we can
safely patch the changes induced by the transition from previous to next
into current. How do you implement that?
Joe We do a recursive merge between current and the diff between previous and
next.
Theo Does Lodash provide an immutable version of recursive merge?
Joe Yes, here’s another example. Take a look at this code.
Listing5.14 Applying a patch
_.merge(current, (diff(previous, next)));
//{
// "authorsById": {
// "dave-gibbons": {
// "name": "David Chester Gibbons"
// }
// },

=== PAGE 134 ===
106 CHAPTER 5 Basic concurrency control
// "catalog": {
// "authorsById": {
// "alan-moore": {
// "bookIsbns": ["978-1779501127"]
// "name": "Alan Moore"
// },
// "dave-gibbons": {
// "bookIsbns": ["978-1779501127"],
// "name": "Dave Gibbons"
// },
// },
// "booksByIsbn": {
// "978-1779501127": {
// "authorIds": ["alan-moore", "dave-gibbons"],
// "isbn": "978-1779501127",
// "publicationYear": 1986,
// "title": "The Watchmen"
// }
// }
// }
//}
Theo Could it be as simple as this?
Joe Indeed.
5.5 Implementing the reconciliation algorithm
Joe All the pieces are now in place to implement our reconciliation algorithm.
Theo What kind of changes are required?
Joe It only requires changes in the code of SystemState.commit. Here, look at
this example on my laptop.
Listing5.15 The SystemState class
class SystemState {
systemData;
get() {
return this.systemData;
}
set(_systemData) {
this.systemData = _systemData;
}
commit(previous, next) {
var nextSystemData = SystemConsistency.reconcile(
this.systemData,
SystemConsistency class is
previous,
implemented in listing 5.16.
next);
if(!SystemValidity.validate(previous, nextSystemData)) {
throw "The system data to be committed is not valid!";
};

=== PAGE 135 ===
5.5 Implementing the reconciliation algorithm 107
this.systemData = nextSystemData;
}
}
Theo How does SystemConsistency do the reconciliation?
Joe The SystemConsistency class starts the reconciliation process by comparing
previous and current. If they are the same, then we fast-forward and return
next. Look at this code for SystemConsistency.
Listing5.16 The reconciliation flow in action
class SystemConsistency {
static threeWayMerge(current, previous, next) {
var previousToCurrent = diff(previous, current);
var previousToNext = diff(previous, next);
if(havePathInCommon(previousToCurrent, previousToNext)) { When the system
return _.merge(current, previousToNext); state is the same
} as the state used
throw "Conflicting concurrent mutations."; by the calculation
} phase, we fast-
static reconcile(current, previous, next) { forward.
if(current == previous) {
return next;
}
return SystemConsistency.threeWayMerge(current,
previous,
next);
}
}
Theo Wait a minute! Why do you compare previous and current by reference?
You should be comparing them by value, right? And, it would be quite expen-
sive to compare all the leaves of the two nested hash maps!
Joe That’s another benefit of immutable data. When the data is not mutated, it is
safe to compare references. If they are the same, we know for sure that the data
is the same.
TIP When data is immutable, it is safe to compare by reference, which is super fast.
When the references are the same, it means that the data is the same.
Theo What about the implementation of the three-way merge algorithm?
Joe When previous differs from current, it means that concurrent mutations
have run. In order to determine whether there is a conflict, we calculate two
diffs: the diff between previous and current and the diff between previous
and next. If the intersection between the two diffs is empty, it means there is
no conflict. We can safely patch the changes between previous to next into
current.
Theo takes a closer look at the code for the SystemConsistency class in listing 5.16. He
tries to figure out if the code is thread-safe or not.

=== PAGE 136 ===
108 CHAPTER 5 Basic concurrency control
Theo I think the code for SystemConsistency class is not thread-safe! If there’s a
context switch between checking whether the system has changed in the
SystemConsistency class and the updating of the state in SystemData class, a
mutation might override the changes of a previous mutation.
Joe You are totally right! The code works fine in a single-threaded environment
like JavaScript, where concurrency is handled via an event loop. However, in a
multi-threaded environment, the code needs to be refined in order to be
thread-safe. I’ll show you some day.
 NOTE The SystemConsistency class is not thread-safe. We will make it thread-safe
in chapter 8.
Theo I think I understand why you called it optimistic concurrency control. It’s
because we assume that conflicts don’t occur too often. Right?
Joe Correct! It makes me wonder what your therapist would say about conflicts that
cannot be resolved. Are there some cases where it’s not possible to reconcile
the couple?
Theo I don’t think she ever mentioned such a possibility.
Joe She must be a very optimistic person.
Summary
 Optimistic concurrency control allows mutations to ask forgiveness instead of
permission.
 Optimistic concurrency control is lock-free.
 Managing concurrent mutations of our system state with optimistic concurrency
control allows our system to support a high throughput of reads and writes.
 Optimistic concurrency control with immutable data is super efficient.
 Before updating the state, we need to reconcile the conflicts between possible con-
current mutations.
 We reconcile between concurrent mutations in a way that is similar to how Git han-
dles a merge between two branches: either a fast-forward or a three-way merge.
 The changes required to let our system manage concurrency are only in the
commit phase.
 The calculation phase does its calculation as if it were the only mutation running.
 The commit phase is responsible for trying to reconcile concurrent mutations.
 The reconciliation algorithm is universal in the sense that it can be used in any sys-
tem where the system data is represented as an immutable hash map.
 The implementation of the reconciliation algorithm is efficient, as it leverages
the fact that subsequent versions of the system state are created via structural
sharing.
 In a user-facing system, conflicting concurrent mutations are fairly rare.
 When we cannot safely reconcile between concurrent mutations, we abort the
mutation and ask the user to try again.

=== PAGE 137 ===
Summary 109
 Calculating the structural diff between two versions of the state is efficient because
two hash maps created via structural sharing from the same hash map have most
of their nodes in common.
 When data is immutable, it is safe to compare by reference, which is fast. When
the references are the same, it means that the data is the same.
 There are three kinds of structural differences between two nested hash maps:
replacement, addition, and deletion.
 Our structural diff algorithm supports replacements and additions but not
deletions.
Lodash functions introduced in this chapter
Function Description
concat(arrA, arrB) Creates an new array, concatenating arrA and arrB
intersection(arrA, arrB) Creates an array of unique values both in arrA and arrB
union(arrA, arrB) Creates an array of unique values from arrA and arrB
find(coll, pred) Iterates over elements of coll, returning the first element for
which pred returns true
isEmpty(coll) Checks if coll is empty
reduce(coll, f, initVal) Reduces coll to a value that is the accumulated result of running
each element in coll through f, where each successive invoca-
tion is supplied the return value of the previous
isArray(coll) Checks if coll is an array
isObject(coll) Checks if coll is a collection