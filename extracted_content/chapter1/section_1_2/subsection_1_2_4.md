# 1.2.4 Complex class hierarchies

1.2.4 Complex class hierarchies
One way to avoid writing the same code twice in OOP involves class inheritance. Indeed,
when every requirement of the system is known up front, you design your class hier-
archy is such a way that classes with common behavior derive from a base class.
Figure 1.15 shows an example of this pattern that focuses on the part of our class
diagram that deals with members and librarians. Both Librarians and Members need
the ability to log in, and they inherit this ability from the User class.
So far, so good, but when new requirements are introduced after the system is imple-
mented, it’s a completely different story. Fast forward to Monday, March 29th, at 11:00 AM,
where two days are left before the deadline (Wednesday at midnight).

=== PAGE 49 ===
1.2 Sources of complexity 21
C Librarian
blockMember(member: Member) : Bool
unblockMember(member: Member) : Bool
addBookItem(bookItem: BookItem) : BookItem
getBookLendingsOfMember(member: Member) : List<BookLending>
CC Member
isBlocked() : Bool
returnBook(bookLending : BookLending) : Bool
checkout(bookItem: BookItem) : BookLending
C User
id : String
email : String Figure 1.15 The part of the
password : String class diagram that deals with
login() : Bool members and librarians
Nancy calls Theo with an urgent request. Theo is not sure if it’s a dream or reality. He
pinches himself and he can feel the jolt. It’s definitely reality!
Nancy How is the project doing?
Theo Fine, Nancy. We’re on schedule to meet the deadline. We’re running our last
round of regression tests now.
Nancy Fantastic! It means we have time for adding a tiny feature to the system, right?
Theo Depends what you mean by “tiny.”
Nancy We need to add VIP members to the system.
Theo What do you mean by VIP members?
Nancy VIP members are allowed to add book items to the library by themselves.
Theo Hmm...
Nancy What?
Theo That’s not a tiny change!
Nancy Why?
I’ll ask you the same question Nancy asked Theo: why is adding VIP members to our
system not a tiny task? After all, Theo has already written the code that allows librari-
ans to add book items to the library (it’s in Librarian::addBookItem). What prevents
him from reusing this code for VIP members? The reason is that, in OOP, the code is
locked into classes as methods.
TIP In OOP, code is locked into classes.
VIP members are members that are allowed to add book items to the library by them-
selves. Theo decomposes the customer requirements into two pieces:

=== PAGE 50 ===
22 CHAPTER 1 Complexity of object-orientedprogramming
 VIP members are library members.
 VIP members are allowed to add book items to the library by themselves.
Theo then decides that he needs a new class, VIPMember. For the first requirement
(VIP members are library members), it seems reasonable to make VIPMember derive
from Member. However, handling the second requirement (VIP members are allowed
to add book items) is more complex. He cannot make a VIPMember derive from
Librarian because the relation between VIPMember and Librarian is not linear:
 On one hand, VIP members are like librarians in that they are allowed to add
book items.
 On the other hand, VIP members are not like librarians in that they are not
allowed to block members or list the books lent to a member.
The problem is that the code that adds book items is locked in the Librarian class.
There is no way for the VIPMember class to use this code.
Figure 1.16 shows one possible solution that makes the code of Librarian::add-
BookItem available to both Librarian and VIPMember classes. Here are the changes to
the previous class diagram:
 A base class UserWithBookItemRight extends User.
 addBookItem moves from Librarian to UserWithBookItemRight.
 Both VIPMember and Librarian extend UserWithBookItemRight.
C Librarian
blockMember(member: Member) : Bool C VIPMember
unblockMember(member: Member) : Bool
getBookLendingsOfMember(member: Member) : List<BookLending>
CC Member
CC UserWithBookItemRight
isBlocked() : Bool
returnBook(bookLending : BookLending) : Bool addBookItem(bookItem: BookItem) : BookItem
checkout(bookItem: BookItem) : BookLending
C User
id : String
email : String
password : String
login() : Bool
Figure 1.16 A class diagram for a system with VIP members
It wasn’t easy, but Theo manages to handle the change on time, thanks to an all nighter
coding on his laptop. He was even able to add new tests to the system and run the regres-
sion tests again. However, he was so excited that he didn’t pay attention to the diamond

=== PAGE 51 ===
1.2 Sources of complexity 23
problem VIPMember introduced in his class diagram due to multiple inheritance: VIPMember
extends both Member and UserWithBookItemRight, which both extend User.
Wednesday, March 31, at 10:00 AM (14 hours before the deadline), Theo calls Nancy to
tell her the good news.
Theo We were able to add VIP members to the system on time, Nancy.
Nancy Fantastic! I told you it was a tiny feature.
Theo Yeah, well...
Nancy Look, I was going to call you anyway. I just finished a meeting with my business
partner, and we realized that we need another tiny feature before the launch.
Will you be able to handle it before the deadline?
Theo Again, it depends what you mean by “tiny.”
Nancy We need to add Super members to the system.
Theo What do you mean by Super members?
Nancy Super members are allowed to list the books lent to other members.
Theo Err...
Nancy What?
Theo That’s not a tiny change!
Nancy Why?
As with VIP members, adding Super members to the system requires changes to Theo’s
class hierarchy. Figure 1.17 shows the solution Theo has in mind.
C Librarian
C VIPMember C SuperMember
getBookLendingsOfMember(member: Member) : List<BookLending>
CC UserWithBlockMemberRight
CC UserWithBookItemRight
blockMember(member: Member) : Bool
addBookItem(bookItem: BookItem) : BookItem
unblockMember(member: Member) : Bool
CC Member
isBlocked() : Bool
returnBook(bookLending : BookLending) : Bool
checkout(bookItem: BookItem) : BookLending
C User
id : String
email : String
password : String
login() : Bool
Figure 1.17 A class diagram for a system with Super and VIP members
The addition of Super members has made the system really complex. Theo suddenly
notices that he has three diamonds in his class diagram—not gemstones but three “Deadly

=== PAGE 52 ===
24 CHAPTER 1 Complexity of object-orientedprogramming
Diamonds of Death” as OOP developers sometimes name the ambiguity that arises when a
class D inherits from two classes B and C, where both inherit from class A!
He tries to avoid the diamonds by transforming the User class into an interface and
using the composition over inheritance design pattern. But with the stress of the deadline
looming, he isn’t able to use all of his brain cells. In fact, the system has become so com-
plex, he’s unable to deliver the system by the deadline. Theo tells himself that he should
have used composition instead of class inheritance. But, it’s too late now.
TIP In OOP, prefer composition over class inheritance.
At 10:00 PM, two hours before the deadline, Theo calls Nancy to explain the situation.
Theo Look Nancy, we really did our best, but we won’t be able to add Super mem-
bers to the system before the deadline.
Nancy No worries, my business partner and I decided to omit this feature for now.
We’ll add it later.
With mixed feelings of anger and relief, Theo stops pacing around his office. He realizes
he will be spending tonight in his own bed, rather than plowing away on his computer at
the office. That should make his wife happy.
Theo I guess that means we’re ready for the launch tomorrow morning.
Nancy Yes. We’ll offer this new product for a month or so, and if we get good market
traction, we’ll move forward with a bigger project.
Theo Cool. Let’s be in touch in a month then. Good luck on the launch!
Summary
 Complexity in the context of this book means hard to understand.
 We use the terms code and behavior interchangeably.
 DOP stands for data-oriented programming.
 OOP stands for object-oriented programming.
 FP stands for functional programming.
 In a composition relation, when one object dies, the other one also dies.
 A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
 In an association relation, each object has an independent life cycle.
 A many-to-many association relation is represented by an empty diamond and a
star at both edges.
 Dashed arrows indicate a usage relation; for instance, when a class uses a method
of another class.
 Plain arrows with empty triangles represent class inheritance, where the arrow
points towards the superclass.
 The design presented in this chapter doesn’t pretend to be the smartest OOP
design. Experienced OOP developers would probably use a couple of design
patterns and suggest a much better diagram.

=== PAGE 53 ===
Summary 25
 Traditional OOP systems tend to increase system complexity, in the sense that
OOP systems are hard to understand.
 In traditional OOP, code and data are mixed together in classes: data as mem-
bers and code as methods.
 In traditional OOP, data is mutable.
 The root cause of the increase in complexity is related to the mixing of code
and data together into objects.
 When code and data are mixed, classes tend to be involved in many relations.
 When objects are mutable, extra thinking is required in order to understand
how the code behaves.
 When objects are mutable, explicit synchronization mechanisms are required
on multi-threaded environments.
 When data is locked in objects, data serialization is not trivial.
 When code is locked in classes, class hierarchies tend to be complex.
 A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
 A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part.
 When data is mutable, code is unpredictable.
 A strategic use of design patterns can help mitigate complexity in traditional
OOP to some degree.
 Data immutability brings serenity to DOP developers’ minds.
 Most OOP programming languages alleviate slightly the difficulty involved the
conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity.
 In traditional OOP, data serialization is difficult.
 In traditional OOP, data is locked in classes as members.
 In traditional OOP, code is locked into classes.
 DOP reduces complexity by rethinking data.
 DOP is compatible both with OOP and FP.

=== PAGE 54 ===
Separation between
code and data
A whole new world
This chapter covers
 The benefits of separating code from data
 Designing a system where code and data are
separate
 Implementing a system that respects the
separation between code and data
The first insight of DOP is that we can decrease the complexity of our systems by
separating code from data. Indeed, when code is separated from data, our systems
are made of two main pieces that can be thought about separately: data entities and
code modules. This chapter is a deep dive in the first principle of DOP (summa-
rized in figure 2.1).
PRINCIPLE #1 Separate code from data such that the code resides in functions,
whose behavior doesn’t depend on data that is somehow encapsulated in the func-
tion’s context.
26