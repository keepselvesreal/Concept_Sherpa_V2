Line1 # Internals vs. Peers (pp.50-51)
Line2 
Line3 ---
Line4 **Page 50**
Line5 
Line6 Many object-oriented languages support encapsulation by providing control over
Line7 the visibility of an object’s features to other objects, but that’s not enough. Objects
Line8 can break encapsulation by sharing references to mutable objects, an effect known
Line9 as aliasing. Aliasing is essential for conventional object- oriented systems (other-
Line10 wise no two objects would be able to communicate), but accidental aliasing can
Line11 couple unrelated parts of a system so it behaves mysteriously and is inﬂexible to
Line12 change.
Line13 We follow standard practices to maintain encapsulation when coding: deﬁne
Line14 immutable value types, avoid global variables and singletons, copy collections
Line15 and mutable values when passing them between objects, and so on. We have
Line16 more about information hiding later in this chapter.
Line17 Internals vs. Peers
Line18 As we organize our system, we must decide what is inside and outside each object,
Line19 so that the object provides a coherent abstraction with a clear API. Much of the
Line20 point of an object, as we discussed above, is to encapsulate access to its internals
Line21 through its API and to hide these details from the rest of the system. An object
Line22 communicates with other objects in the system by sending and receiving messages,
Line23 as in Figure 6.2; the objects it communicates with directly are its peers.
Line24 Figure 6.2
Line25 Objects communicate by sending and receiving messages
Line26 This decision matters because it affects how easy an object is to use, and so
Line27 contributes to the internal quality of the system. If we expose too much of an
Line28 object’s internals through its API, its clients will end up doing some of its work.
Line29 We’ll have distributed behavior across too many objects (they’ll be coupled to-
Line30 gether), increasing the cost of maintenance because any changes will now ripple
Line31 across the code. This is the effect of the “train wreck” example on page 17:
Line32 Chapter 6
Line33 Object-Oriented Style
Line34 50
Line35 
Line36 
Line37 ---
Line38 
Line39 ---
Line40 **Page 51**
Line41 
Line42 ((EditSaveCustomizer) master.getModelisable()
Line43   .getDockablePanel()
Line44     .getCustomizer())
Line45       .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
Line46 Every getter in this example exposes a structural detail. If we wanted to change,
Line47 say, the way customizations on the master are enabled, we’d have to change all
Line48 the intermediate relationships.
Line49 Different Levels of Language
Line50 As you’ll see in Part III, we often write helper methods to make code more readable.
Line51 We’re not afraid of adding very small methods if they clarify the meaning of the
Line52 feature they represent. We name these methods to make the calling code read
Line53 as naturally as possible; we don’t have to conform to external conventions since
Line54 these methods are only there to support other code. For example, in Chapter 15
Line55 we have a line in a test that reads:
Line56 allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING)));
Line57 We’ll explain what this means at the time. What’s relevant here is that
Line58 aSniperThatIs() is a local method that constructs a value to be passed to the
Line59 with() method, and that its name is intended to describe its intent in this context.
Line60 In effect, we’re constructing a very small embedded language that deﬁnes, in this
Line61 case, a part of a test.
Line62 As well as distinguishing between value and object types (page 13), we ﬁnd that
Line63 we tend towards different programming styles at different levels in the code.
Line64 Loosely speaking, we use the message-passing style we’ve just described between
Line65 objects, but we tend to use a more functional style within an object, building up
Line66 behavior from methods and values that have no side effects.
Line67 Features without side effects mean that we can assemble our code from smaller
Line68 components, minimizing the amount of risky shared state. Writing large-scale
Line69 functional programs is a topic for a different book, but we ﬁnd that a little
Line70 immutability within the implementation of a class leads to much safer code and
Line71 that, if we do a good job, the code reads well too.
Line72 So how do we choose the right features for an object?
Line73 No And’s, Or’s, or But’s
Line74 Every object should have a single, clearly deﬁned responsibility; this is the “single
Line75 responsibility” principle [Martin02]. When we’re adding behavior to a system,
Line76 this principle helps us decide whether to extend an existing object or create a
Line77 new service for an object to call.
Line78 51
Line79 No And’s, Or’s, or But’s
Line80 
Line81 
Line82 ---
