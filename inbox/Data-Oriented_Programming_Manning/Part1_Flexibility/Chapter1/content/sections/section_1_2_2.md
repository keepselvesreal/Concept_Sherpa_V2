# 1.2.2 Unpredictable code behavior

**설명:** 1.2.2 Unpredictable behavior
**페이지 범위:** 45-46
**섹션 유형:** subsection

1.2.2 Unpredictable code behavior
You might be a bit tired after the system-level analysis that we presented in the previ-
ous section. Let’s get refreshed and look at some code.
Take a look at the code in listing 1.1, where we get the blocked status of a member
and display it twice. If I tell you that when I called displayBlockedStatusTwice, the
program displayed true on the first console.log call, can you tell me what the pro-
gram displayed on the second console.log call?

=== PAGE 45 ===
1.2 Sources of complexity 17
Listing1.1 Really simple code
class Member {
isBlocked;
displayBlockedStatusTwice() {
var isBlocked = this.isBlocked;
console.log(isBlocked);
console.log(isBlocked);
}
}
member.displayBlockedStatusTwice();
“Of course, it displayed true again,” you say. And you are right!
Now, take a look at a slightly different pseudocode as shown in listing 1.2. Here we
display, twice, the blocked status of a member without assigning a variable. Same ques-
tion as before: if I tell you that when I called displayBlockedStatusTwice, the pro-
gram displayed true on the first console.log call, can you tell me what the program
displayed on the second console.log call?
Listing1.2 Apparently simple code
class Member {
isBlocked;
displayBlockedStatusTwice() {
console.log(this.isBlocked);
console.log(this.isBlocked);
}
}
member.displayBlockedStatusTwice();
The correct answer is...in a single-threaded environment, it displays true, while in a
multi-threaded environment, it’s unpredictable. Indeed, in a multi-threaded environ-
ment between the two console.log calls, there could be a context switch that changes
the state of the object (e.g., a librarian unblocked the member). In fact, with a slight
modification, the same kind of code unpredictability could occur even in a single-
threaded environment like JavaScript, when data is modified via asynchronous code
(see the section about Principle #3 in appendix A). The difference between the two
code snippets is that
 In the first listing (listing 1.1), we access a Boolean value twice , which is a prim-
itive value.
 In the second listing (listing 1.2), we access a member of an object twice.
TIP When data is mutable, code is unpredictable.

=== PAGE 46 ===
18 CHAPTER 1 Complexity of object-orientedprogramming
This unpredictable behavior of the second listing is one of the annoying conse-
quences of OOP. Unlike primitive types, which are usually immutable, object mem-
bers are mutable. One way to solve this problem in OOP is to protect sensitive code
with concurrency safety mechanisms like mutexes, but that introduces issues like a
performance hit and a risk of deadlocks.
We will see later in the book that DOP treats every piece of data in the same way:
both primitive types and collection types are immutable values. This value treatment for
all citizens brings serenity to DOP developers’ minds, and more brain cells are avail-
able to handle the interesting pieces of the applications they build.
TIP Data immutability brings serenity to DOP developers’ minds.