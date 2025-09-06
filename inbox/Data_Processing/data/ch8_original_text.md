# Chapter 8: Advanced concurrency control

**부제목:** No more deadlocks!
**계획된 페이지:** 191-202
**실제 페이지:** 191-202

=== PAGE 191 ===
Advanced
concurrency control
No more deadlocks!
This chapter covers
 Atoms as an alternative to locks
 Managing a thread-safe counter and a thread-safe
in-memory cache with atoms
 Managing the whole system state in a thread-safe
way with atoms
The traditional way to manage concurrency in a multi-threaded environment
involves lock mechanisms like mutexes. Lock mechanisms tend to increase the com-
plexity of the system because it’s not trivial to make sure the system is free of dead-
locks. In DOP, we leverage the fact that data is immutable, and we use a lock-free
mechanism, called an atom, to manage concurrency. Atoms are simpler to manage
than locks because they are lock-free. As a consequence, the usual complexity of
locks that are required to avoid deadlocks don’t apply to atoms.
 NOTE This chapter is mostly relevant to multi-threaded environments like Java,
C#, Python, and Ruby. It is less relevant to single-threaded environments like Java-
Script. The JavaScript code snippets in this chapter are written as though JavaScript
were multi-threaded.
163

=== PAGE 192 ===
164 CHAPTER 8 Advanced concurrency control
8.1 The complexity of locks
This Sunday afternoon, while riding his bike across the Golden Gate Bridge, Theo thinks
about the Klafim project with concern, not yet sure that betting on DOP was a good
choice. Suddenly, Theo realizes that he hasn’t yet scheduled the next session with Joe. He
gets off his bike to call Joe. Bad luck, the line is busy.
When Theo gets home, he tries to call Joe again, but once again the phone is busy. After
dinner, Theo tries to call Joe one more time, with the same result—a busy signal. “Obvi-
ously, Joe is very busy today,” Theo tells himself. Exhausted by his 50-mile bike ride at an
average of 17 miles per hour, he falls asleep on the sofa. When Theo wakes up, he’s elated
to see a text message from Joe, “See you Monday morning at 11 AM?” Theo answers with a
thumbs up and prepares for another week of work.
When Joe arrives at the office, Theo asks him why his phone was constantly busy the day
before. Joe answers that he was about to ask Theo the same question. They look at each
other, puzzled, and then simultaneously break into laughter as they realize what hap-
pened: in an amazing coincidence, they’d tried to phone each other at exactly the same
times. They both say at once:
“A deadlock!”
They both head for Theo’s office. When they get to Theo’s desk, Joe tells him that today’s
session is going to be about concurrency management in multi-threaded environments.
Joe How do you usually manage concurrency in a multi-threaded environment?
Theo I protect access to critical sections with a lock mechanism, a mutex, for instance.
Joe When you say access, do you mean write access or also read access?
Theo Both!
Joe Why do you need to protect read access with a lock?
Theo Because, without a lock protection, in the middle of a read, a write could hap-
pen in another thread. It would make my read logically inconsistent.
Joe Another option would be to clone the data before processing it in a read.
Theo Sometimes I would clone the data; but in many cases, when it’s large, it’s too
expensive to clone.
TIP Cloning data to avoid read locks doesn’t scale.
Joe In DOP, we don’t need to clone or to protect read access.
Theo Because data is immutable?
Joe Right. When data is immutable, even if a write happens in another thread
during a read, it won’t make the read inconsistent because the write never
mutates the data that is read.
Theo In a sense, a read always works on a data snapshot.
Joe Exactly!
TIP When data is immutable, a read is always safe.
Theo But what about write access? Don’t you need to protect that with locks?
Joe Nope.

=== PAGE 193 ===
8.2 Thread-safe counter with atoms 165
Theo Why not?
Joe We have a simpler mechanism—it’s called an atom.
Theo I am glad to hear there is a something simpler than locks. I really struggle each
time I have to integrate locks into a multi-threaded system.
Joe Me too! I remember a bug we had in production 10 years ago. We forgot to
release a lock when an exception was thrown in a critical section. It caused a
terrible deadlock.
Theo Deadlocks are really hard to avoid. Last year, we had a deadlock issue when two
locks were not released in the proper order.
Joe I have great news for you. With atoms, deadlocks never happen!
TIP With atoms, deadlocks never happen.
Theo That sounds great. Tell me more!
TIP Atoms provide a way to manage concurrency without locks.
8.2 Thread-safe counter with atoms
Joe Let’s start with a simple case: a counter shared between threads.
Theo What do you mean by a counter?
Joe Imagine that we’d like to count the number of database accesses and write the
total number of accesses to a log every minute.
Theo OK.
Joe Could you write JavaScript code for this multi-threaded counter using locks?
Theo But JavaScript is single-threaded!
Joe I know, but it’s just for the sake of illustration. Imagine that JavaScript were
multi-threaded and that it provided a Mutex object that you could lock and
unlock.
Theo It’s a bit awkward. I guess it would look like this.
Theo goes to the whiteboard. He writes what he imagines to be JavaScript code for a multi-
threaded counter with locks.
Listing8.1 A thread-safe counter protected by a mutex
var mutex = new Mutex();
var counter = 0;
function dbAccess() {
mutex.lock();
counter = counter + 1;
mutex.unlock();
// access the database
}
function logCounter() {
mutex.lock();

=== PAGE 194 ===
166 CHAPTER 8 Advanced concurrency control
console.log('Number of database accesses: ' + counter);
mutex.unlock();
}
Joe Excellent. Now, I am going to show you how to write the same code with atoms.
An atom provides three methods:
 get returns the current value of the atom.
 set overwrites the current value of the atom.
 swap receives a function and updates the value of the atom with the result
of the function called on the current value of the atom.
Joe unzips a pocket in his laptop case and takes out a piece of paper. He hands it to
Theo. Theo is pleasantly surprised as the sheet of paper succinctly describes the methods
(table 8.1).
Table 8.1 The three methods of an atom
Method Description
get Returns the current value
set Overwrites the current value
swap Updates the current value with a function
Theo How would it look like to implement a thread-safe counter with an atom?
Joe It’s quite simple, actually.
Joe pulls out his laptop, fires it up, and begins to type. When he’s done, he turns the laptop
around so that Theo can see the code to implement a thread-safe counter in an atom.
Listing8.2 A thread-safe counter stored in an atom
var counter = new Atom();
counter.set(0);
function dbAccess() {
counter.swap(function(x) {
The argument x is the
return x + 1;
current value of the atom,
});
same as counter.get().
// access the database
}
function logCounter() {
console.log('Number of database accesses: ' + counter.get());
}
Theo Could you tell me what’s going on here?
Joe Sure! First, we create an empty atom. Then, we initialize the value of the atom
with counter.set(0). In the logger thread, we read the current value of the
atom with counter.get().
Theo And how do you increment the counter in the threads that access the database?

=== PAGE 195 ===
8.2 Thread-safe counter with atoms 167
Joe We call swap with a function that receives x and returns x + 1.
Theo I don’t understand how swap could be thread-safe without using any locks.
Joe quickly goes to the whiteboard. He sketches the diagram in figure 8.1.
Take snapshot
Compute next state
Yes
State changed?
No
Update state
Figure 8.1 High-level flow of swap
Joe You see, swap computes the next value of the atom, and before modifying the
current value of the atom, it checks whether the value of the atom has changed
during the computation. If so, swap tries again, until no changes occur during
the computation.
Theo Is swap easy to implement?
Joe Let me show you the implementation of the Atom class and you’ll see.
Listing8.3 Implementation of the Atom class
class Atom {
state;
constructor() {}
get() {
return this.state;
}
set(state) {
this.state = state;
}
swap(f) {
while(true) {
var stateSnapshot = this.state;
var nextState = f(stateSnapshot);
if (!atomicCompareAndSet(this.state,

=== PAGE 196 ===
168 CHAPTER 8 Advanced concurrency control
stateSnapshot,
nextState)) {
Uses a special thread-safe comparison operation
continue;
as this.state might have changed in another
}
thread during execution of the function f.
return nextState;
}
}
}
Theo comes closer to the whiteboard. He modifies Joe’s diagram a bit to make the flow of
the swap operation more detailed. The resulting diagram is in figure 8.2. Theo still has a
few questions, though.
Take snapshot
snapshot = state
Compute next state
nextState = f(snapshot)
Check if state has changed
state == snapshot
Yes
State changed?
No
Update state
state = nextState
Figure 8.2 Detailed flow of swap
Theo What is atomicCompareAndSet?
Joe It’s the core operation of an atom. atomicCompareAndSet atomically sets the
state to a new value if, and only if, the state equals the provided old value. It
returns true upon success and false upon failure.
Theo How could it be atomic without using locks?
Joe That’s a great question! In fact, atomicCompareAndSet is a compare-and-swap
operation, provided by the language that relies on a functionality of the CPU
itself. For example, in Java the java.util.concurrent.atomic package has
an AtomicReference generic class that provides a compareAndSet() method.
 NOTE See http://tutorials.jenkov.com/java-concurrency/compare-and-swap.html
for general information about compare-and-swap operations. Implementations for
multi-threaded languages appear in table 8.2.

=== PAGE 197 ===
8.2 Thread-safe counter with atoms 169
Table 8.2 Implementation of an atomic compare and set in various languages
Language Link
Java http://mng.bz/mx0W
JavaScript Not relevant (single-threaded language)
Ruby http://mng.bz/5KG8
Python https://github.com/maxcountryman/atomos
C# http://mng.bz/6Zzp
Theo Apropos Java, how would the implementation of an atom look?
Joe It’s quite the same, besides the fact that Atom has to use generics, and the inner
state has to be stored in an AtomicReference.
Joe brings up a Java implementation of Atom on his laptop. Theo looks over the code.
Listing8.4 Implementation of the Atom class in Java
class Atom<ValueType> {
private AtomicReference<ValueType> state;
public Atom() {}
ValueType get() {
return this.state.get();
}
this.state might have
changed in another thread
void set(ValueType state) {
during the execution of f.
this.state.set(state);
}
ValueType swap(UnaryOPerator<ValueType> f) {
while(true) {
ValueType stateSnapshot = this.state.get();
ValueType nextState = f(stateSnapshot);
if (!this.state.compareAndSet(stateSnapshot,
nextState)) {
continue;
}
}
return nextState;
}
}
Theo What about using an atom in Java?
Joe Here, take a look. It’s quite simple.

=== PAGE 198 ===
170 CHAPTER 8 Advanced concurrency control
Listing8.5 Using an Atom in Java
Atom<Integer> counter = new Atom<Integer>();
counter.set(0);
counter.swap(x -> x + 1);
counter.get();
Theo takes a couple of minutes to meditate about this atom stuff and to digest what he’s
just learned. Then, he asks Joe:
Theo What if swap never succeeds? I mean, could the while loop inside the code of
swap turn out to be an infinite loop?
Joe No! By definition, when atomicCompareAndSet fails on a thread, it means that
the same atom was changed on another thread during the execution of swap.
In this race between threads, there is always a winner.
Theo But isn’t it possible that some thread never succeeds because it always loses the
race against other threads?
Joe In theory, yes, but I’ve never encountered such a situation. If you have thou-
sands of threads that do nothing besides swapping an atom, it could happen I
suppose. But, in practice, once the atom is swapped, the threads do some real
work, for example, database access or I/O. This gives other threads the oppor-
tunity to swap the atom successfully.
 NOTE In theory, atoms could create starvation in a system with thousands of threads
that do nothing beside swapping an atom. In practice, once an atom is swapped, the
threads do some real work (e.g., database access), which creates an opportunity for
other threads to swap the atom successfully.
Theo Interesting.... Indeed, atoms look much easier to manage than locks.
Joe Now let me show you how to use atoms with composite data.
Theo Why would that be different?
Joe Usually, dealing with composite data is more difficult than dealing with primi-
tive types.
Theo When you sold me on DOP, you told me that we are able to manage data with
the same simplicity as we manage numbers.
TIP In DOP, data is managed with the same simplicity as numbers.
Joe That’s exactly what I am about to show you.
8.3 Thread-safe cache with atoms
Joe Are you familiar with the notion of in-memory cache?
Theo You mean memoization?

=== PAGE 199 ===
8.3 Thread-safe cache with atoms 171
Joe Kind of. Imagine that database queries don’t vary too much in your applica-
tion. It makes sense in that case to store the results of previous queries in mem-
ory in order to improve the response time.
Theo Yes, of course!
Joe What data structure would you use to store the in-memory cache?
Theo Probably a string map, where the keys are the queries, and the values are the
results from the database.
TIP It’s quite common to represent an in-memory cache as a string map.
Joe Excellent! Now can you write the code to cache database queries in a thread-
safe way using a lock?
Theo Let me see: I’m going to use an immutable string map. Therefore, I don’t
need to protect read access with a lock. Only the cache update needs to be
protected.
Joe You’re getting the hang of this!
Theo The code should be something like this.
Listing8.6 Thread-safe cache with locks
var mutex = new Mutex();
var cache = {};
function dbAccessCached(query) {
var resultFromCache = _.get(cache, query);
if (resultFromCache != nil) {
return resultFromCache;
}
var result = dbAccess(query);
mutex.lock();
cache = _.set(cache, query, result);
mutex.unlock();
return result;
}
Joe Nice! Now, let me show you how to write the same code using an atom instead
of a lock. Take a look at this code and let me know if it’s clear to you.
Listing8.7 Thread-safe cache with atoms
var cache = new Atom();
cache.set({});
function dbAccessCached(query) {
var resultFromCache = _.get(cache.get(), query);
if (resultFromCache != nil) {
return resultFromCache;
}
var result = dbAccess(query);
cache.swap(function(oldCache) {

=== PAGE 200 ===
172 CHAPTER 8 Advanced concurrency control
return _.set(oldCache, query, result);
});
return result;
}
Theo I don’t understand the function you’re passing to the swap method.
Joe The function passed to swap receives the current value of the cache, which is a
string map, and returns a new version of the string map with an additional key-
value pair.
Theo I see. But something bothers me with the performance of the swap method in
the case of a string map. How does the comparison work? I mean, comparing
two string maps might take some time.
Joe Not if you compare them by reference. As we discussed in the past, when data
is immutable, it is safe to compare by reference, and it’s super fast.
TIP When data is immutable, it is safe (and fast) to compare it by reference.
Theo Cool. So atoms play well with immutable data.
Joe Exactly!
8.4 State management with atoms
Joe Do you remember a couple of weeks ago when I showed you how we resolve
potential conflicts between mutations? You told me that the code was not
thread-safe.
Theo Let me look again at the code.
Theo takes a look at the code for the SystemData class that he wrote some time ago
(repeated in listing 8.8). Without the validation logic, it makes the code easier to grasp.
Listing8.8 SystemData class from part 1
class SystemState {
systemData;
get() {
return this.systemData;
}
set(_systemData) {
this.systemData = _systemData;
}
commit(previous, next) {
this.systemData = SystemConsistency.reconcile(this.systemData,
previous,
next);
}
}

=== PAGE 201 ===
8.4 State management with atoms 173
It takes him a few minutes to remember how the commit method works. Suddenly, he has
an Aha! moment.
Theo This code is not thread-safe because the SystemConsistency.reconcile
code inside the commit method is not protected. Nothing prevents the two
threads from executing this code concurrently.
Joe Right! Now, can you tell me how to make it thread-safe?
Theo With locks?
Joe Come on...
Theo I was kidding, of course. We make the code thread-safe not with a lock but with
an atom.
Joe Nice joke!
Theo Let me see. I’d need to store the system data inside an atom. The get and set
method of SystemData would simply call the get and set methods of the
atom. How does this look?
Listing8.9 SystemData class with atom (without the commit method)
class SystemState {
systemData;
constructor() {
this.systemData = new Atom();
}
get() {
return this.systemData.get();
}
commit(prev, next) {
this.systemData.set(next);
}
}
Joe Excellent. Now for the fun part. Implement the commit method by calling the
swap method of the atom.
Theo Instead of calling SystemConsistency.reconcile() directly, I need to wrap
it into a call to swap. So, something like this?
Listing8.10 Implementation of SystemData.commit with atom
SystemData.commit = function(previous, next) {
this.systemData.swap(function(current) {
return SystemConsistency.reconcile(current,
previous,
next);
});
};

=== PAGE 202 ===
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