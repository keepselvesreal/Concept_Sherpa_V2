# 8.4 State management with atoms

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

## 페이지 201

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

## 페이지 202

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

## 페이지 203

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

## 페이지 204

176 CHAPTER