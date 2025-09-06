# 8.4 State management with atoms

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