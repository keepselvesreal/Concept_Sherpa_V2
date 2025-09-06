# 5.5 Implementing the reconciliation algorithm

**메타데이터:**
- ID: 49
- 레벨: 2
- 페이지: 134-135
- 페이지 수: 2
- 부모 ID: 43
- 텍스트 길이: 3897 문자

---

the reconciliation algorithm
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