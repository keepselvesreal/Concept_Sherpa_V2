# 8.2 Thread-safe counter with atoms

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

## 페이지 194

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

## 페이지 195

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

## 페이지 196

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

## 페이지 197

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

## 페이지 198

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