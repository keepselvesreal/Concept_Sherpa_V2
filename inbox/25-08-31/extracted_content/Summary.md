# Summary

--- 페이지 52 ---
24
CHAPTER 1
Complexity of object-oriented programming
Diamonds of Death” as OOP developers sometimes name the ambiguity that arises when a
class D inherits from two classes B and C, where both inherit from class A!
He tries to avoid the diamonds by transforming the User class into an interface and
using the composition over inheritance design pattern. But with the stress of the deadline
looming, he isn’t able to use all of his brain cells. In fact, the system has become so com-
plex, he’s unable to deliver the system by the deadline. Theo tells himself that he should
have used composition instead of class inheritance. But, it’s too late now.
TIP
In OOP, prefer composition over class inheritance.
At 10:00 PM, two hours before the deadline, Theo calls Nancy to explain the situation.
Theo
Look Nancy, we really did our best, but we won’t be able to add Super mem-
bers to the system before the deadline.
Nancy
No worries, my business partner and I decided to omit this feature for now.
We’ll add it later.
With mixed feelings of anger and relief, Theo stops pacing around his office. He realizes
he will be spending tonight in his own bed, rather than plowing away on his computer at
the office. That should make his wife happy.
Theo
I guess that means we’re ready for the launch tomorrow morning.
Nancy
Yes. We’ll offer this new product for a month or so, and if we get good market
traction, we’ll move forward with a bigger project.
Theo
Cool. Let’s be in touch in a month then. Good luck on the launch!
Summary
Complexity in the context of this book means hard to understand.
We use the terms code and behavior interchangeably.
DOP stands for data-oriented programming.
OOP stands for object-oriented programming.
FP stands for functional programming.
In a composition relation, when one object dies, the other one also dies.
A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
In an association relation, each object has an independent life cycle.
A many-to-many association relation is represented by an empty diamond and a
star at both edges.
Dashed arrows indicate a usage relation; for instance, when a class uses a method
of another class.
Plain arrows with empty triangles represent class inheritance, where the arrow
points towards the superclass.
The design presented in this chapter doesn’t pretend to be the smartest OOP
design. Experienced OOP developers would probably use a couple of design
patterns and suggest a much better diagram.


--- 페이지 53 ---
25
Summary
Traditional OOP systems tend to increase system complexity, in the sense that
OOP systems are hard to understand.
In traditional OOP, code and data are mixed together in classes: data as mem-
bers and code as methods.
In traditional OOP, data is mutable.
The root cause of the increase in complexity is related to the mixing of code
and data together into objects.
When code and data are mixed, classes tend to be involved in many relations.
When objects are mutable, extra thinking is required in order to understand
how the code behaves.
When objects are mutable, explicit synchronization mechanisms are required
on multi-threaded environments.
When data is locked in objects, data serialization is not trivial.
When code is locked in classes, class hierarchies tend to be complex.
A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part.
When data is mutable, code is unpredictable.
A strategic use of design patterns can help mitigate complexity in traditional
OOP to some degree.
Data immutability brings serenity to DOP developers’ minds.
Most OOP programming languages alleviate slightly the difficulty involved the
conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity.
In traditional OOP, data serialization is difficult.
In traditional OOP, data is locked in classes as members.
In traditional OOP, code is locked into classes.
DOP reduces complexity by rethinking data.
DOP is compatible both with OOP and FP.


