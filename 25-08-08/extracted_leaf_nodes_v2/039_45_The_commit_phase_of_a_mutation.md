# 4.5 The commit phase of a mutation

**메타데이터:**
- ID: 39
- 레벨: 2
- 페이지: 111-112
- 페이지 수: 2
- 부모 ID: 33
- 텍스트 길이: 4140 문자

---

hase of a mutation 83
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