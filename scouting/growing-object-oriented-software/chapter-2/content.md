# Chapter 2: Test-Driven Development with Objects (pp.13-20)

---
**Page 13**

Chapter 2
Test-Driven Development with
Objects
Music is the space between the notes.
—Claude Debussy
A Web of Objects
Object-oriented design focuses more on the communication between objects than
on the objects themselves. As Alan Kay [Kay98] wrote:
The big idea is “messaging” […] The key in making great and growable systems is
much more to design how its modules communicate rather than what their internal
properties and behaviors should be.
An object communicates by messages: It receives messages from other objects
and reacts by sending messages to other objects as well as, perhaps, returning a
value or exception to the original sender. An object has a method of handling
every type of message that it understands and, in most cases, encapsulates some
internal state that it uses to coordinate its communication with other objects.
An object-oriented system is a web of collaborating objects. A system is built
by creating objects and plugging them together so that they can send messages
to one another. The behavior of the system is an emergent property of the
composition of the objects—the choice of objects and how they are connected
(Figure 2.1).
This lets us change the behavior of the system by changing the composition of
its objects—adding and removing instances, plugging different combinations
together—rather than writing procedural code. The code we write to manage
this composition is a declarative deﬁnition of the how the web of objects will
behave. It’s easier to change the system’s behavior because we can focus on what
we want it to do, not how.
Values and Objects
When designing a system, it’s important to distinguish between values that
model unchanging quantities or measurements, and objects that have an identity,
might change state over time, and model computational processes. In the
13


---
**Page 14**

Figure 2.1
A web of objects
object-oriented languages that most of us use, the confusion is that both concepts
are implemented by the same language construct: classes.
Values are immutable instances that model ﬁxed quantities. They have no in-
dividual identity, so two value instances are effectively the same if they have the
same state. This means that it makes no sense to compare the identity of two
values; doing so can cause some subtle bugs—think of the different ways of
comparing two copies of new Integer(999). That’s why we’re taught to use
string1.equals(string2) in Java rather than string1 == string2.
Objects, on the other hand, use mutable state to model their behavior over
time. Two objects of the same type have separate identities even if they have ex-
actly the same state now, because their states can diverge if they receive different
messages in the future.
In practice, this means that we split our system into two “worlds”: values,
which are treated functionally, and objects, which implement the stateful behavior
of the system. In Part III, you’ll see how our coding style varies depending on
which world we’re working in.
In this book, we will use the term object to refer only to instances with identity,
state, and processing—not values. There doesn’t appear to be another accepted
term that isn’t overloaded with other meanings (such as entity and process).
Follow the Messages
We can beneﬁt from this high-level, declarative approach only if our objects are
designed to be easily pluggable. In practice, this means that they follow common
communication patterns and that the dependencies between them are made ex-
plicit. A communication pattern is a set of rules that govern how a group of ob-
jects talk to each other: the roles they play, what messages they can send and
when, and so on. In languages like Java, we identify object roles with (abstract)
interfaces, rather than (concrete) classes—although interfaces don’t deﬁne
everything we need to say.
Chapter 2
Test-Driven Development with Objects
14


---
**Page 15**

In our view, the domain model is in these communication patterns, because
they are what gives meaning to the universe of possible relationships between
the objects. Thinking of a system in terms of its dynamic, communication structure
is a signiﬁcant mental shift from the static classiﬁcation that most of us learn
when being introduced to objects. The domain model isn’t even obviously visible
because the communication patterns are not explicitly represented in the program-
ming languages we get to work with. We hope to show, in this book, how tests
and mock objects help us see the communication between our objects more
clearly.
Here’s a small example of how focusing on the communication between objects
guides design.
In a video game, the objects in play might include: actors, such as the player
and the enemies; scenery, which the player ﬂies over; obstacles, which the
player can crash into; and effects, such as explosions and smoke. There are also
scripts spawning objects behind the scenes as the game progresses.
This is a good classiﬁcation of the game objects from the players’ point of view
because it supports the decisions they need to make when playing the game—when
interacting with the game from outside. This is not, however, a useful classiﬁcation
for the implementers of the game. The game engine has to display objects that
are visible, tell objects that are animated about the passing of time, detect colli-
sions between objects that are physical, and delegate decisions about what to do
when physical objects collide to collision resolvers.
Figure 2.2
Roles and objects in a video game
As you can see in Figure 2.2, the two views, one from the game engine and
one from the implementation of the in-play objects, are not the same. An Obstacle,
for example, is Visible and Physical, while a Script is a Collision Resolver and
Animated but not Visible. The objects in the game play different roles depending
15
Follow the Messages


---
**Page 16**

on what the engine needs from them at the time. This mismatch between static
classiﬁcation and dynamic communication means that we’re unlikely to come
up with a tidy class hierarchy for the game objects that will also suit the needs
of the engine.
At best, a class hierarchy represents one dimension of an application, providing
a mechanism for sharing implementation details between objects; for example,
we might have a base class to implement the common features of frame-based
animation. At worst, we’ve seen too many codebases (including our own) that
suffer complexity and duplication from using one mechanism to represent multiple
concepts.
Roles, Responsibilities, Collaborators
We try to think about objects in terms of roles, responsibilities, and collaborators,
as best described by Wirfs-Brock and McKean in [Wirfs-Brock03]. An object is an
implementation of one or more roles; a role is a set of related responsibilities;
and a responsibility is an obligation to perform a task or know information. A
collaboration is an interaction of objects or roles (or both).
Sometimes we step away from the keyboard and use an informal design technique
that Wirfs-Brock and McKean describe, called CRC cards (Candidates, Responsi-
bilities, Collaborators). The idea is to use low-tech index cards to explore the po-
tential object structure of an application, or a part of it. These index cards allow
us to experiment with structure without getting stuck in detail or becoming too
attached to an early solution.
Figure 2.3
CRC card for a video game
Chapter 2
Test-Driven Development with Objects
16


---
**Page 17**

Tell, Don’t Ask
We have objects sending each other messages, so what do they say? Our experi-
ence is that the calling object should describe what it wants in terms of the role
that its neighbor plays, and let the called object decide how to make that happen.
This is commonly known as the “Tell, Don’t Ask” style or, more formally, the
Law of Demeter. Objects make their decisions based only on the information
they hold internally or that which came with the triggering message; they avoid
navigating to other objects to make things happen. Followed consistently, this
style produces more ﬂexible code because it’s easy to swap objects that play the
same role. The caller sees nothing of their internal structure or the structure of
the rest of the system behind the role interface.
When we don’t follow the style, we can end up with what’s known as “train
wreck” code, where a series of getters is chained together like the carriages in a
train. Here’s one case we found on the Internet:
((EditSaveCustomizer) master.getModelisable()
  .getDockablePanel()
    .getCustomizer())
      .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
After some head scratching, we realized what this fragment was meant to say:
master.allowSavingOfCustomisations();
This wraps all that implementation detail up behind a single call. The client of
master no longer needs to know anything about the types in the chain. We’ve
reduced the risk that a design change might cause ripples in remote parts of the
codebase.
As well as hiding information, there’s a more subtle beneﬁt from “Tell, Don’t
Ask.” It forces us to make explicit and so name the interactions between objects,
rather than leaving them implicit in the chain of getters. The shorter version
above is much clearer about what it’s for, not just how it happens to be
implemented.
But Sometimes Ask
Of course we don’t “tell” everything;1 we “ask” when getting information from
values and collections, or when using a factory to create new objects. Occasion-
ally, we also ask objects about their state when searching or ﬁltering, but we still
want to maintain expressiveness and avoid “train wrecks.”
For example (to continue with the metaphor), if we naively wanted to spread
reserved seats out across the whole of a train, we might start with something like:
1. Although that’s an interesting exercise to try, to stretch your technique.
17
But Sometimes Ask


---
**Page 18**

public class Train {
  private final List<Carriage> carriages […]
  private int percentReservedBarrier = 70;
  public void reserveSeats(ReservationRequest request) {
    for (Carriage carriage : carriages) {
      if (carriage.getSeats().getPercentReserved() < percentReservedBarrier) {
        request.reserveSeatsIn(carriage);
        return;
      }
    }
    request.cannotFindSeats();
  }
}
We shouldn’t expose the internal structure of Carriage to implement this, not
least because there may be different types of carriages within a train. Instead, we
should ask the question we really want answered, instead of asking for the
information to help us ﬁgure out the answer ourselves:
public void reserveSeats(ReservationRequest request) {
  for (Carriage carriage : carriages) {
    if (carriage.hasSeatsAvailableWithin(percentReservedBarrier)) {
      request.reserveSeatsIn(carriage);
      return;
    }
  }
  request.cannotFindSeats();
} 
Adding a query method moves the behavior to the most appropriate object,
gives it an explanatory name, and makes it easier to test.
We try to be sparing with queries on objects (as opposed to values) because
they can allow information to “leak” out of the object, making the system a little
bit more rigid. At a minimum, we make a point of writing queries that describe
the intention of the calling object, not just the implementation.
Unit-Testing the Collaborating Objects
We appear to have painted ourselves into a corner. We’re insisting on focused
objects that send commands to each other and don’t expose any way to query
their state, so it looks like we have nothing available to assert in a unit test. For
example, in Figure 2.4, the circled object will send messages to one or more of
its three neighbors when invoked. How can we test that it does so correctly
without exposing any of its internal state?
One option is to replace the target object’s neighbors in a test with substitutes,
or mock objects, as in Figure 2.5. We can specify how we expect the target object
to communicate with its mock neighbors for a triggering event; we call these
speciﬁcations expectations. During the test, the mock objects assert that they
Chapter 2
Test-Driven Development with Objects
18


---
**Page 19**

Figure 2.4
Unit-testing an object in isolation
Figure 2.5
Testing an object with mock objects
have been called as expected; they also implement any stubbed behavior needed
to make the rest of the test work.
With this infrastructure in place, we can change the way we approach TDD.
Figure 2.5 implies that we’re just trying to test the target object and that we al-
ready know what its neighbors look like. In practice, however, those collaborators
don’t need to exist when we’re writing a unit test. We can use the test to help us
tease out the supporting roles our object needs, deﬁned as Java interfaces, and
ﬁll in real implementations as we develop the rest of the system. We call this in-
terface discovery; you’ll see an example when we extract an AuctionEventListener
in Chapter 12.
Support for TDD with Mock Objects
To support this style of test-driven programming, we need to create mock in-
stances of the neighboring objects, deﬁne expectations on how they’re called and
then check them, and implement any stub behavior we need to get through the
test. In practice, the runtime structure of a test with mock objects usually looks
like Figure 2.6.
19
Support for TDD with Mock Objects


---
**Page 20**

Figure 2.6
Testing an object with mock objects
We use the term mockery2 for the object that holds the context of a test, creates
mock objects, and manages expectations and stubbing for the test. We’ll show
the practice throughout Part III, so we’ll just touch on the basics here. The
essential structure of a test is:
•
Create any required mock objects.
•
Create any real objects, including the target object.
•
Specify how you expect the mock objects to be called by the target object.
•
Call the triggering method(s) on the target object.
•
Assert that any resulting values are valid and that all the expected calls have
been made.
The unit test makes explicit the relationship between the target object and its
environment. It creates all the objects in the cluster and makes assertions about
the interactions between the target object and its collaborators. We can code this
infrastructure by hand or, these days, use one of the multiple mock object
frameworks that are available in many languages. The important point, as we
stress repeatedly throughout this book, is to make clear the intention of every
test, distinguishing between the tested functionality, the supporting infrastructure,
and the object structure.
2. This is a pun by Ivan Moore that we adopted in a ﬁt of whimsy.
Chapter 2
Test-Driven Development with Objects
20


