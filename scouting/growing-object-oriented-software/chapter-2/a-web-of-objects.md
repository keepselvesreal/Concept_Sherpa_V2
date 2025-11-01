Line1 # A Web of Objects (pp.13-13)
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
