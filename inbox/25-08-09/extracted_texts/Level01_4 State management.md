# 4 State management

**Level:** 1
**페이지 범위:** 99 - 118
**총 페이지 수:** 20
**ID:** 33

---

=== 페이지 99 ===
State management
Time travel
This chapter covers
 A multi-version approach to state management
 The calculation phase of a mutation
 The commit phase of a mutation
 Keeping a history of previous state versions
So far, we have seen how DOP handles queries via generic functions that access sys-
tem data, which is represented as a hash map. In this chapter, we illustrate how
DOP deals with mutations (requests that change the system state). Instead of updat-
ing the state in place, we maintain multiple versions of the system data. At a specific
point in time, the system state refers to a specific version of the system data. This
chapter is a deep dive in the third principle of DOP.
PRINCIPLE #3 Data is immutable.
The maintenance of multiple versions of the system data requires the data to be
immutable. This is made efficient both in terms of computation and memory via a
71

=== 페이지 100 ===
72 CHAPTER 4 State management
technique called structural sharing, where parts of the data that are common between
two versions are shared instead of being copied. In DOP, a mutation is split into two
distinct phases:
 In the calculation phase, we compute the next version of the system data.
 In the commit phase, we move the system state forward so that it refers to the
version of the system data computed by the calculation phase.
This distinction between calculation and commit phases allows us to reduce the part
of our system that is stateful to its bare minimum. Only the code of the commit phase
is stateful, while the code in the calculation phase of a mutation is stateless and is
made of generic functions similar to the code of a query. The implementation of the
commit phase is common to all mutations. As a consequence, inside the commit
phase, we have the ability to ensure that the state always refers to a valid version of the
system data.
Another benefit of this state management approach is that we can keep track of
the history of previous versions of the system data. Restoring the system to a previous
state (if needed) becomes straightforward. Table 4.1 shows the two phases.
Table 4.1 The two phases of a mutation
Phase Responsibility State Implementation
Calculation Computes the next version of system data Stateless Specific
Commit Moves the system state forward Stateful Common
In this chapter, we assume that no mutations occur concurrently in our system. In the
next chapter, we will deal with concurrency control.
4.1 Multiple versions of the system data
When Joe comes in to the office on Monday, he tells Theo that he needs to exercise before
starting to work with his mind. Theo and Joe go for a walk around the block, and the dis-
cussion turns toward version control systems. They discuss how Git keeps track of the
whole commit history and how easy and fast it is to restore the code to a previous state.
When Theo tells Joe that Git’s ability to “time travel” reminds him one of his favorite mov-
ies, Back to the Future, Joe shares that a month ago he watched the Back to the Future trilogy
with Neriah, his 14-year-old son.
Their walk complete, they arrive back at Theo’s office. Theo and Joe partake of the
espresso machine in the kitchen before they begin today’s lesson.
Joe So far, we’ve seen how we manage queries that retrieve information from the
system in DOP. Now I’m going to show you how we manage mutations. By a
mutation, I mean an operation that changes the state of the system.
 NOTE A mutation is an operation that changes the state of the system.

=== 페이지 101 ===
4.1 Multiple versions of the system data 73
Theo Is there a fundamental difference between queries and mutations in DOP?
After all, the whole state of the system is represented as a hash map. I could
easily write code that modifies part of the hash map, and it would be similar to
the code that retrieves information from the hash map.
Joe You could mutate the data in place, but then it would be challenging to ensure
that the code of a mutation doesn’t put the system into an invalid date. You
would also lose the ability to track previous versions of the system state.
Theo I see. So, how do you handle mutations in DOP?
Joe We adopt a multi-version state approach, similar to what a version control sys-
tem like Git does; we manage different versions of the system data. At a specific
point in time, the state of the system refers to a version of the system data. After
a mutation is executed, we move the reference forward.
Theo I’m confused. Is the system state mutable or immutable?
Joe The data is immutable, but the state reference is mutable.
TIP The data is immutable, but the state reference is mutable.
Noticing the look of confusion on Theo’s face, Joe draws a quick diagram on the white-
board. He then shows Theo figure 4.1, hoping that it will clear up Theo’s perplexity.
After mutation B After mutation C
Data V10 Data V10
MutationA MutationA
Data V11 Data V11
Mutation B Mutation B
System State Data V12 Data V12
Mutation C
System State Data V13
Figure 4.1 After mutation B is executed, the system state refers to Data V12. After
mutation C is executed, the system state refers to Data V13.
Theo Does that mean that before the code of a mutation runs, we make a copy of the
system data?
Joe No, that would be inefficient, as we would have to do a deep copy of the data.

=== 페이지 102 ===
74 CHAPTER 4 State management
Theo How does it work then?
Joe It works by using a technique called structural sharing, where most of the data
between subsequent versions of the state is shared instead of being copied.
This technique efficiently creates new versions of the system data, both in
terms of memory and computation.
Theo I’m intrigued.
TIP With structural sharing, it’s efficient (in terms of memory and computation) to
create new versions of data.
Joe I’ll explain in detail how structural sharing works in a moment.
Theo takes another look at the diagram in figure 4.1, which illustrates how the system state
refers to a version of the system data. Suddenly, a question emerges.
Theo Are the previous versions of the system data kept?
Joe In a simple application, previous versions are automatically removed by the
garbage collector. But, in some cases, we maintain historical references to pre-
vious versions of the data.
Theo What kind of cases?
Joe For example, if we want to support time travel in our system, as in Git, we can
move the system back to a previous version of the state easily.
Theo Now I understand what you mean by data is immutable, but the state reference
is mutable!
4.2 Structural sharing
As mentioned in the previous section, structural sharing enables the efficient cre-
ation of new versions of immutable data. In DOP, we use structural sharing in the
calculation phase of a mutation to compute the next state of the system based on
the current state of the system. Inside the calculation phase, we don’t have to deal
with state management; that is delayed to the commit phase. As a consequence, the
code involved in the calculation phase of a mutation is stateless and is as simple as
the code of a query.
Theo I’m really intrigued by this more efficient way to create new versions of data.
How does it work?
Joe Let’s take a simple example from our library system. Imagine that you want to
modify the value of a field in a book in the catalog; for instance, the publica-
tion year of Watchmen. Can you tell me the information path for Watchmen’s
publication year?
Theo takes a quick look at the catalog data in figure 4.2. Then he answers Joe’s question.

=== 페이지 103 ===
4.2 Structural sharing 75
catalog
booksByIsbn authorsById
978-1779501127 alan-moore
title isbn name
Watchmen 978-1779501127 Alan Moore
authorIds publicationYear bookIsbns
1987
1 0 0
bookItems
dave-gibbons alan-moore 978-1779501127
1 0 dave-gibbons
id id name
book-item-2 book-item-1 Dave Gibbons
libId libId bookIsbns
la-central-lib nyc-cental-lib
0
isLent isLent
978-1779501127
false true
Figure 4.2 Visualization of the catalog data. The nodes in the information path to Watchmen’s publication
year are marked with a dotted border.
Theo The information path for Watchmen’s publication year is ["catalog", "books-
ByIsbn", "978-1779501127", "publicationYear"].
Joe Now, let me show how you to use the immutable function _.set that Lodash
also provides.
Theo Wait! What do you mean by an immutable function? When I looked at the
Lodash documentation for _.set on their website, it said that it mutates the
object.
Joe You’re right, but the default Lodash functions are not immutable. In order to
use an immutable version of the functions, we need to use the Lodash FP mod-
ule as explained in the Lodash FP guide.
 NOTE See https://lodash.com/docs/4.17.15#set to view Lodash’s documentation
for _.set, and see https://github.com/lodash/lodash/wiki/FP-Guide to view the
Lodash FP guide.
Theo Do the immutable functions have the same signature as the mutable functions?
Joe By default, the order of the arguments in immutable functions is shuffled.
The Lodash FP guide explains how to resolve this. With this piece of code,

=== 페이지 104 ===
76 CHAPTER 4 State management
the signature of the immutable functions is exactly the same as the mutable
functions.
Listing4.1 Configuring Lodash so immutable and mutable functions have same signature
_ = fp.convert({
"cap": false,
"curry": false,
"fixed": false,
"immutable": true,
"rearg": false
});
TIP In order to use Lodash immutable functions, we use Lodash’s FP module, and
we configure it so that the signature of the immutable functions is the same as in the
Lodash documentation web site.
Theo So basically, I can still rely on Lodash documentation when using immutable
versions of the functions.
Joe Except for the piece in the documentation that says the function mutates the
object.
Theo Of course!
Joe Now I’ll show you how to write code that creates a version of the library data
with the immutable function _.set.
Joe’s fingers fly across Theo’s keyboard. Theo then looks at Joe’s code, which creates a ver-
sion of the library data where the Watchmen publication year is set to 1986.
Listing4.2 Using _.set as an immutable function
var nextLibraryData = _.set(libraryData,
["catalog", "booksByIsbn",
"978-1779501127", "publicationYear"],
1986);
 NOTE A function is said to be immutable when, instead of mutating the data, it cre-
ates a new version of the data without changing the data it receives.
Theo You told me earlier that structural sharing allowed immutable functions to be
efficient in terms of memory and computation. Can you tell me what makes
them efficient?
Joe With pleasure, but before that, you have to answer a series of questions. Are
you ready?
Theo Yes, sure...
Joe What part of the library data is impacted by updating the Watchmen publication
year: the UserManagement or the Catalog?

=== 페이지 105 ===
4.2 Structural sharing 77
Theo Only the Catalog.
Joe What part of the Catalog?
Theo Only the booksByIsbn index.
Joe What part of the booksByIsbn index?
Theo Only the Book record that holds the information about Watchmen.
Joe What part of the Book record?
Theo Only the publicationYear field.
Joe Perfect! Now, suppose that the current version of the library data looks like
this.
Joe goes to the whiteboard and draws a diagram. Figure 4.3 shows the result.
Library
Catalog UserManagement
authorsByld booksBylsbn ...
... watchmen
title:Watchmen publicationYear:1987 authorlds
...
Figure 4.3 High-level visualization of the current version of Library
Theo So far, so good...
Joe Next, let me show you what an immutable function does when you use it to cre-
ate a new version of Library, where the publication year of Watchmen is set to
1986 instead of 1987.
Joe updates his diagram on the whiteboard. It now looks like figure 4.4.

=== 페이지 106 ===
78 CHAPTER 4 State management
«Next»
Library
Library
«Next»
Catalog UserManagement
Catalog
«Next»
booksByIsbn ... authorsById
booksByIsbn
«Next»
watchmen ...
watchmen
«Next»
publicationYear:1987 title:Watchmen authorlds
publicationYear:1986
...
Figure 4.4 Structural sharing provides an efficient way to create a new version of the data.
Next Library is recursively made of nodes that use the parts of Library that are
common between the two.
Theo Could you explain?
Joe The immutable function creates a fresh Library hash map, which recursively
uses the parts of the current Library that are common between the two ver-
sions instead of deeply copying them.
Theo It’s a bit abstract for me.
Joe The next version of Library uses the same UserManagement hash map as the
old one. The Catalog inside the next Library uses the same authorsById as
the current Catalog. The Watchmen Book record inside the next Catalog uses
all the fields of the current Book except for the publicationYear field.
Theo So, in fact, most parts of the data are shared between the two versions. Right?
Joe Exactly! That’s why this technique is called structural sharing.
TIP Structural sharing provides an efficient way (both in terms of memory and com-
putation) to create a new version of the data by recursively sharing the parts that don’t
need to change.
Theo That’s very cool!
Joe Indeed. Now let’s look at how to write a mutation for adding a member using
immutable functions.

=== 페이지 107 ===
4.2 Structural sharing 79
Once again, Joe goes to the whiteboard. Figure 4.5 shows the diagram that Joe draws to
illustrate how structural sharing looks when we add a member.
«Next»
Library
Library
«Next»
UserManagement Catalog
userManagement
«Next»
members librarians ...
members
Figure 4.5 Adding a member
with structural sharing. Most of
the data is shared between the
... member0 member1
two versions.
Theo Awesome! The Catalog and the librarians hash maps don’t have to be copied!
Joe Now, in terms of code, we have to write a Library.addMember function that
delegates to UserManagement.addMember.
Theo I guess it’s going to be similar to the code we wrote earlier to implement the
search books query, where Library.searchBooksByTitleJSON delegates to
Catalog.searchBooksByTitle.
Joe Similar in the sense that all the functions are static, and they receive the data
they manipulate as an argument. But there are two differences. First, a muta-
tion could fail, for instance, if the member to be added already exists. Second,
the code for Library.addMember is a bit more elaborate than the code for
Library.searchBooksByTitleJSON because we have to create a new version
of Library that refers to the new version of UserManagement. Here, let me
show you an example.
Listing4.3 The code for the mutation that adds a member
UserManagement.addMember = function(userManagement, member) {
var email = _.get(member, "email");
var infoPath = ["membersByEmail", email];
if(_.has(userManagement, infoPath)) {
Checks if a member with
throw "Member already exists.";
the same email address
}
already exists
var nextUserManagement = _.set(
userManagement,
Creates a new version of
infoPath,
userManagement that
member);
includes the member
return nextUserManagement;
};

=== 페이지 108 ===
80 CHAPTER 4 State management
Library.addMember = function(library, member) {
var currentUserManagement = _.get(library, "userManagement");
var nextUserManagement = UserManagement.addMember(
currentUserManagement,
member);
var nextLibrary = _.set(library,
"userManagement",
nextUserManagement);
Creates a new version of
return nextLibrary;
library that contains the new
};
version of userManagement
Theo To me, it’s a bit weird that immutable functions return an updated version of
the data instead of changing it in place.
Joe It was also weird for me when I first encountered immutable data in Clojure
seven years ago.
Theo How long did it take you to get used to it?
Joe A couple of weeks.
4.3 Implementing structural sharing
When Joe leaves the office, Theo meets Dave near the coffee machine. Dave looks perplexed.
Dave Who’s the guy that just left the office?
Theo It’s Joe. My DOP mentor.
Dave What’s DOP?
Theo DOP refers to data-oriented programming.
Dave I never heard that term before.
Theo It’s not well-known by programmers yet, but it’s quite a powerful programming
paradigm. From what I’ve seen so far, it makes programming much simpler.
Dave Can you give me an example?
Theo I just learned about structural sharing and how it makes it possible to create
new versions of data, effectively without copying.
Dave How does that work?
Theo takes Dave to his office and shows him Joe’s diagram on the whiteboard (see figure 4.6).
It takes Theo a few minutes to explain to Dave what it does exactly, but in the end, Dave
gets it.
Dave What does the implementation of structural sharing look like?
Theo I don’t know. I used the _.set function from Lodash.
Dave It sounds like an interesting challenge.
Theo Take the challenge if you want. Right now, I’m too tired for this recursive algo-
rithmic stuff.

=== 페이지 109 ===
4.3 Implementing structural sharing 81
«Next»
Library
Library
«Next»
Catalog UserManagement
Catalog
«Next»
booksByIsbn ... authorsById
booksByIsbn
«Next»
watchmen ...
watchmen
«Next»
publicationYear:1987 title:Watchmen authorlds
publicationYear:1986
...
Figure 4.6 Structural sharing in action
The next day, Theo stops by Dave’s cubicle before heading to his office. Dave, with a touch
of pride, shows Theo his implementation of structural sharing. Theo is amazed by the fact
that it’s only 11 lines of JavaScript code!
Listing4.4 The implementation of structural sharing
function setImmutable(map, path, v) {
var modifiedNode = v;
var k = path[0];
var restOfPath = path.slice(1);
if (restOfPath.length > 0) {
modifiedNode = setImmutable(map[k], restOfPath, v);
}
var res = Object.assign({}, map);
Shallow
res[k] = modifiedNode;
clones a map
return res;
in JavaScript.
}
Theo Dave, you’re brilliant!
Dave (smiling) Aw, shucks.
Theo Oops, I have to go. I’m already late for my session with Joe! Joe is probably wait-
ing in my office, biting his nails.

=== 페이지 110 ===
82 CHAPTER 4 State management
4.4 Data safety
Joe is about to start the day’s lesson. Theo asks him a question about yesterday’s material
instead.
Theo Something isn’t clear to me regarding this structural sharing stuff. What hap-
pens if we write code that modifies the data part that’s shared between the two
versions of the data? Does the change affect both versions?
Joe Could you please write a code snippet that illustrates your question?
Theo starts typing on his laptop. He comes up with this code to illustrate modifying a piece
of data shared between two versions.
Listing4.5 Modifying data that’s shared between two versions
var books = {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore",
"dave-gibbons"]
}
};
var nextBooks = _.set(books, ["978-1779501127", "publicationYear"], 1986)
console.log("Before:", nextBooks["978-1779501127"]["authorIds"][1]);
books["978-1779501127"]["authorIds"][1] = "dave-chester-gibbons";
console.log("After:", nextBooks["978-1779501127"]["authorIds"][1]);
// → Before: dave-gibbons
// → After: dave-chester-gibbons
Theo My question is, what is the value of isBlocked in updatedMember?
Joe The answer is that mutating data via the native hash map setter is forbidden.
All the data manipulation must be done via immutable functions.
 NOTE All data manipulation must be done with immutable functions. It is forbid-
den to use the native hash map setter.
Theo When you say “forbidden,” you mean that it’s up to the developer to make sure
it doesn’t happen. Right?
Joe Exactly.
Theo Is there a way to protect our system from a developer’s mistake?
Joe Yes, there is a way to ensure the immutability of the data at the level of the data
structure. It’s called persistent data structures.
Theo Are persistent data structures also efficient in terms of memory and computation?
Joe Actually, the way data is organized inside persistent data structures make them
even more efficient than immutable functions.

=== 페이지 111 ===
4.5 The commit phase of a mutation 83
TIP Persistent data structures are immutable at the level of the data. There is no way
to mutate them, even by mistake.
Theo Are there libraries providing persistent data structures?
Joe Definitely. I just happen to have a list of those libraries on my computer.
Joe, being well-organized for a programmer, quickly brings up his list. He shows it to Theo:
 Immutable.js in JavaScript at https://immutable-js.com/
 Paguro in Java at https://github.com/GlenKPeterson/Paguro
 Immutable Collections in C# at http://mng.bz/y4Ke
 Pyrsistent in Python at https://github.com/tobgu/pyrsistent
 Hamster in Ruby at https://github.com/hamstergem/hamster
Theo Why not use persistent data structures instead of immutable functions?
Joe The drawback of persistent data structures is that they are not native. This
means that working with them requires conversion from native to persistent
and from persistent to native.
Theo What approach would you recommend?
Joe If you want to play around a bit, then start with immutable functions. But for a
production application, I’d recommend using persistent data structures.
Theo Too bad the native data structures aren’t persistent!
Joe That’s one of the reasons why I love Clojure—the native data structures of the
language are immutable!
4.5 The commit phase of a mutation
So far, we saw how to implement the calculation phase of a mutation. The calculation
phase is stateless in the sense that it doesn’t make any change to the system. Now, let’s
see how to update the state of the system inside the commit phase.
Theo takes another look at the code for Library.addMember. Something bothers him:
this function returns a new state of the library that contains an additional member, but it
doesn’t affect the current state of the library.
Listing4.6 The commit phase moves the system state forward
Library.addMember = function(library, member) {
var currentUserManagement = _.get(library, "userManagement");
var nextUserManagement = UserManagement.addMember(
currentUserManagement,
member);
var nextLibrary = _.set(library, "userManagement", nextUserManagement);
return nextLibrary;
};
Theo I see that Library.addMember doesn’t change the state of the library. How
does the library state get updated?

=== 페이지 112 ===
84 CHAPTER 4 State management
Joe That’s an excellent question. Library.addMember deals only with data calcula-
tion and is stateless. The state is updated in the commit phase by moving for-
ward the version of the state that the system state refers to.
Theo What do you mean by that?
Joe Here’s what happens when we add a member to the system. The calculation
phase creates a version of the state that has two members. Before the commit
phase, the system state refers to the version of the state with one member. The
responsibility of the commit phase is to move the system state forward so that it
refers to the version of the state with two members.
TIP The responsibility of the commit phase is to move the system state forward to the
version of the state returned by the calculation phase.
Joe draws another illustration on the whiteboard (figure 4.7). He hopes it helps to clear up
any misunderstanding Theo may have.
Before Commit After Commit
State with one State with one
System State
member member
addMember addMember
State with two State with two
System State
members members
Figure 4.7 The commit phase moves the system state forward.
Theo How is this implemented?
Joe The code is made of two classes: System, a singleton stateful class that imple-
ments the mutations, and SystemState, a singleton stateful class that manages
the system state.
Theo It sounds to me like classic OOP.
Joe Right, and this part of the system being stateful is OOP-like.
Theo I’m happy to see that you still find some utility in OOP.
Joe Meditation taught me that every part of our universe has a role to play.
Theo Nice! Could you show me some code?
Joe Sure.
Joe thinks for a moment before starting to type. He wants to show the System class and its
implementation of the addMember mutation.
Listing4.7 The System class
class System {
addMember(member) {
var previous = SystemState.get();

=== 페이지 113 ===
4.6 Ensuring system state integrity 85
var next = Library.addMember(previous, member);
SystemState.commit(previous, next);
SystemState is covered
}
in listing 4.8.
}
Theo What does SystemState look like?
Joe I had a feeling you were going to ask that. Here’s the code for the System-
State class, which is a stateful class!
Listing4.8 The SystemState class
class SystemState {
systemState;
get() {
return this.systemState;
}
commit(previous, next) {
this.systemState = next;
}
}
Theo I don’t get the point of SystemState. It’s a simple class with a getter and a
commit function, right?
Joe In a moment, we are going to enrich the code of the SystemState.commit
method so that it provides data validation and history tracking. For now, the
important thing to notice is that the code of the calculation phase is stateless
and is decoupled from the code of the commit phase, which is stateful.
TIP The calculation phase is stateless. The commit phase is stateful.
4.6 Ensuring system state integrity
Theo Something still bothers me about the way functions manipulate immutable
data in the calculation phase. How do we preserve data integrity?
Joe What do you mean?
Theo In OOP, data is manipulated only by methods that belong to the same class as
the data. It prevents other classes from corrupting the inner state of the class.
Joe Could you give me an example of an invalid state of the library?
Theo For example, imagine that the code of a mutation adds a book item to the
book lendings of a member without marking the book item as lent in the cata-
log. Then the system data would be corrupted.
Joe In DOP, we have the privilege of ensuring data integrity at the level of the
whole system instead of scattering the validation among many classes.
Theo How does that work?
Joe The fact that the code for the commit phase is common to all the mutations
allows us to validate the system data in a central place. At the beginning of the
commit phase, there is a step that checks whether the version of the system

=== 페이지 114 ===
86 CHAPTER 4 State management
state to be committed is valid. If the data is invalid, the commit is rejected.
Here let me show you.
Listing4.9 Data validation inside the commit phase
SystemState.commit = function(previous, next) {
if(!SystemValidity.validate(previous, next)) { // not implemented for now
throw "The system data to be committed is not valid!";
};
this.systemData = next;
};
Theo It sounds similar to a commit hook in Git.
Joe I like your analogy!
Theo Why are you passing the previous state in previous and the next state in next
to SystemValidity.validate?
Joe Because it allows SystemValidity.validate to optimize the validation in
terms of computation. For example, we could validate just the data that has
changed.
TIP In DOP, we validate the system data as a whole. Data validation is decoupled
from data manipulation.
Theo What does the code of SystemValidity.validate look like?
Joe Someday, I will show you how to define a data schema and to validate that a
piece of data conforms to a schema.
 NOTE See chapters 7 and 12 to see how Joe defines this data schema.
4.7 Restoring previous states
Another advantage of the multi-version state approach with immutable data that is
manipulated via structural sharing is that we can keep track of the history of all the
versions of the data without exploding the memory of our program. It allows us, for
instance, to restore the system back to an earlier state easily.
Theo You told me earlier that it was easy to restore the system to a previous state.
Could you show me how?
Joe Happily, but before that, I’d like to make sure you understand why keeping
track of all the versions of the data is efficient in terms of memory.
Theo I think it’s related to the fact that immutable functions use structural sharing,
and most of the data between subsequent versions of the state is shared.
TIP Structural sharing allows us to keep many versions of the system state without
exploding memory use.
Joe Perfect! Now, I’ll show you how simple it is to undo a mutation. In order to
implement an undo mechanism, our SystemState class needs to have two

=== 페이지 115 ===
4.7 Restoring previous states 87
references to the system data: systemData references the current state of the
system, and previousSystemData references the previous state of the system.
Theo That makes sense.
Joe In the commit phase, we update both previousSystemData and systemData.
Theo What does it take to implement an undo mechanism?
Joe The undo is achieved by having systemData reference the same version of the
system data as previousSystemData.
Theo Could you walk me through an example?
Joe To make things simple, I am going to give a number to each version of the sys-
tem state. It starts at V0, and each time a mutation is committed, the version is
incremented: V1, V2, V3, and so forth.
Theo OK.
Joe Let’s say that currently our system state is at V12 (see figure 4.8). In the
SystemState object, systemData refers to V12, and previousSystemData
refers to V11.
previousSystemData
MutationA Mutation B
Data V10 Data V11 Data V12
systemData
Figure 4.8 When the system state is at V12, systemData refers to V12, and
previousSystemData refers to V11.
Theo So far, so good...
Joe Now, when a mutation is committed (for instance, adding a member), both
references move forward: systemData refers to V13, and previousSystem-
Data refers to V12.
Joe erases the whiteboard to make room for another diagram (figure 4.9). When he’s
through with his drawing, he shows it to Theo.
previousSystemData
MutationA Mutation B Mutation C
Data V10 Data V11 Data V12 Data V13
systemData
Figure 4.9 When a mutation is committed, systemData refers to V13, and
previousSystemData refers to V12.

=== 페이지 116 ===
88 CHAPTER 4 State management
Theo I suppose that when we undo the mutation, both references move backward.
Joe In theory, yes, but in practice, it’s necessary to maintain a stack of all the state
references. For now, to simplify things, we’ll maintain only a reference to the
previous version. As a consequence, when we undo the mutation, both refer-
ences refer to V12. Let me draw another diagram on the whiteboard that shows
this state (see figure 4.10).
previousSystemData
MutationA Mutation B Mutation C
Data V10 Data V11 Data V12 Data V13
systemData
Figure 4.10 When a mutation is undone, both systemData and previousSystemData refer
to V12.
Theo Could you show me how to implement this undo mechanism?
Joe Actually, it takes only a couple of changes to the SystemState class. Pay atten-
tion to the changes in the commit function. Inside systemDataBeforeUpdate,
we keep a reference to the current state of the system. If the validation and
the conflict resolution succeed, we update both previousSystemData and
systemData.
Listing4.10 The SystemState class with undo capability
class SystemState {
systemData;
previousSystemData;
get() {
return this.systemData;
}
commit(previous, next) {
var systemDataBeforeUpdate = this.systemData;
if(!Consistency.validate(previous, next)) {
throw "The system data to be committed is not valid!";
}
this.systemData = next;
this.previousSystemData = systemDataBeforeUpdate;
}
undoLastMutation() {
this.systemData = this.previousSystemData;
}
}

=== 페이지 117 ===
Summary 89
Theo I see that implementing System.undoLastMutation is simply a matter of hav-
ing systemData refer the same value as previousSystemData.
Joe As I told you, if we need to allow multiple undos, the code would be a bit more
complicated, but you get the idea.
Theo I think so. Although Back to the Future belongs to the realm of science fiction, in
DOP, time travel is real.
Summary
 DOP principle #3 states that data is immutable.
 A mutation is an operation that changes the state of the system.
 In a multi-version approach to state management, mutations are split into cal-
culation and commit phases.
 All data manipulation must be done via immutable functions. It is forbidden to
use the native hash map setter.
 Structural sharing allows us to create new versions of data efficiently (in terms of
memory and computation), where data that is common between the two ver-
sions is shared instead of being copied.
 Structural sharing creates a new version of the data by recursively sharing the
parts that don’t need to change.
 A mutation is split in two phases: calculation and commit.
 A function is said to be immutable when, instead of mutating the data, it creates
a new version of the data without changing the data it receives.
 During the calculation phase, data is manipulated with immutable functions that
use structural sharing.
 The calculation phase is stateless.
 During the commit phase, we update the system state.
 The responsibility of the commit phase is to move the system state forward to
the version of the state returned by the calculation phase.
 The data is immutable, but the state reference is mutable.
 The commit phase is stateful.
 We validate the system data as a whole. Data validation is decoupled from data
manipulation.
 The fact that the code for the commit phase is common to all the mutations
allows us to validate the system state in a central place before we update the
state.
 Keeping the history of the versions of the system data is memory efficient due to
structural sharing.
 Restoring the system to one of its previous states is straightforward due to the
clear separation between the calculation phase and the commit phase.

=== 페이지 118 ===
90 CHAPTER 4 State management
 In order to use Lodash immutable functions, we use the Lodash FP module
(https://github.com/lodash/lodash/wiki/FP-Guide).
Lodash functions introduced in this chapter
Function Description
set(map, path, value) Creates a map with the same fields as map with the addition of a
<path, value> field
