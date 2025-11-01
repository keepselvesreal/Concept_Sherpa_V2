Line1 # Values and Objects (pp.13-14)
Line2 
Line3 ---
Line4 **Page 13**
Line5 
Line6 Chapter 2
Line7 Test-Driven Development with
Line8 Objects
Line9 Music is the space between the notes.
Line10 —Claude Debussy
Line11 A Web of Objects
Line12 Object-oriented design focuses more on the communication between objects than
Line13 on the objects themselves. As Alan Kay [Kay98] wrote:
Line14 The big idea is “messaging” […] The key in making great and growable systems is
Line15 much more to design how its modules communicate rather than what their internal
Line16 properties and behaviors should be.
Line17 An object communicates by messages: It receives messages from other objects
Line18 and reacts by sending messages to other objects as well as, perhaps, returning a
Line19 value or exception to the original sender. An object has a method of handling
Line20 every type of message that it understands and, in most cases, encapsulates some
Line21 internal state that it uses to coordinate its communication with other objects.
Line22 An object-oriented system is a web of collaborating objects. A system is built
Line23 by creating objects and plugging them together so that they can send messages
Line24 to one another. The behavior of the system is an emergent property of the
Line25 composition of the objects—the choice of objects and how they are connected
Line26 (Figure 2.1).
Line27 This lets us change the behavior of the system by changing the composition of
Line28 its objects—adding and removing instances, plugging different combinations
Line29 together—rather than writing procedural code. The code we write to manage
Line30 this composition is a declarative deﬁnition of the how the web of objects will
Line31 behave. It’s easier to change the system’s behavior because we can focus on what
Line32 we want it to do, not how.
Line33 Values and Objects
Line34 When designing a system, it’s important to distinguish between values that
Line35 model unchanging quantities or measurements, and objects that have an identity,
Line36 might change state over time, and model computational processes. In the
Line37 13
Line38 
Line39 
Line40 ---
Line41 
Line42 ---
Line43 **Page 14**
Line44 
Line45 Figure 2.1
Line46 A web of objects
Line47 object-oriented languages that most of us use, the confusion is that both concepts
Line48 are implemented by the same language construct: classes.
Line49 Values are immutable instances that model ﬁxed quantities. They have no in-
Line50 dividual identity, so two value instances are effectively the same if they have the
Line51 same state. This means that it makes no sense to compare the identity of two
Line52 values; doing so can cause some subtle bugs—think of the different ways of
Line53 comparing two copies of new Integer(999). That’s why we’re taught to use
Line54 string1.equals(string2) in Java rather than string1 == string2.
Line55 Objects, on the other hand, use mutable state to model their behavior over
Line56 time. Two objects of the same type have separate identities even if they have ex-
Line57 actly the same state now, because their states can diverge if they receive different
Line58 messages in the future.
Line59 In practice, this means that we split our system into two “worlds”: values,
Line60 which are treated functionally, and objects, which implement the stateful behavior
Line61 of the system. In Part III, you’ll see how our coding style varies depending on
Line62 which world we’re working in.
Line63 In this book, we will use the term object to refer only to instances with identity,
Line64 state, and processing—not values. There doesn’t appear to be another accepted
Line65 term that isn’t overloaded with other meanings (such as entity and process).
Line66 Follow the Messages
Line67 We can beneﬁt from this high-level, declarative approach only if our objects are
Line68 designed to be easily pluggable. In practice, this means that they follow common
Line69 communication patterns and that the dependencies between them are made ex-
Line70 plicit. A communication pattern is a set of rules that govern how a group of ob-
Line71 jects talk to each other: the roles they play, what messages they can send and
Line72 when, and so on. In languages like Java, we identify object roles with (abstract)
Line73 interfaces, rather than (concrete) classes—although interfaces don’t deﬁne
Line74 everything we need to say.
Line75 Chapter 2
Line76 Test-Driven Development with Objects
Line77 14
Line78 
Line79 
Line80 ---
