Line1 # Communication over Classification (pp.58-59)
Line2 
Line3 ---
Line4 **Page 58**
Line5 
Line6 Communication over Classiﬁcation
Line7 As we wrote in Chapter 2, we view a running system as a web of communicating
Line8 objects, so we focus our design effort on how the objects collaborate to deliver
Line9 the functionality we need. Obviously, we want to achieve a well-designed class
Line10 structure, but we think the communication patterns between objects are more
Line11 important.
Line12 In languages such as Java, we can use interfaces to deﬁne the available messages
Line13 between objects, but we also need to deﬁne their patterns of communication—their
Line14 communication protocols. We do what we can with naming and convention, but
Line15 there’s nothing in the language to describe relationships between interfaces or
Line16 methods within an interface, which leaves a signiﬁcant part of the design implicit.
Line17 Interface and Protocol
Line18 Steve heard this useful distinction in a conference talk: an interface describes
Line19 whether two components will ﬁt together, while a protocol describes whether they
Line20 will work together.
Line21 We use TDD with mock objects as a technique to make these communication
Line22 protocols visible, both as a tool for discovering them during development and
Line23 as a description when revisiting the code. For example, the unit test towards the
Line24 end of Chapter 3 tells us that, given a certain input message, the translator
Line25 should call listener.auctionClosed() exactly once—and nothing else. Although
Line26 the listener interface has other methods, this test says that its protocol requires
Line27 that auctionClosed() should be called on its own.
Line28 @Test public void
Line29 notifiesAuctionClosedWhenCloseMessageReceived() {
Line30   Message message = new Message();
Line31   message.setBody("SOLVersion: 1.1; Event: CLOSE;");
Line32   context.checking(new Expectations() {{ 
Line33     oneOf(listener).auctionClosed(); 
Line34   }});
Line35   translator.processMessage(UNUSED_CHAT, message); 
Line36 }
Line37 TDD with mock objects also encourages information hiding. We should mock
Line38 an object’s peers—its dependencies, notiﬁcations, and adjustments we categorized
Line39 on page 52—but not its internals. Tests that highlight an object’s neighbors help
Line40 us to see whether they are peers, or should instead be internal to the target object.
Line41 A test that is clumsy or unclear might be a hint that we’ve exposed too much
Line42 implementation, and that we should rebalance the responsibilities between the
Line43 object and its neighbors.
Line44 Chapter 7
Line45 Achieving Object-Oriented Design
Line46 58
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 59**
Line53 
Line54 Value Types
Line55 Before we go further, we want to revisit the distinction we described in “Values
Line56 and Objects” (page 13): values are immutable, so they’re simpler and have no
Line57 meaningful identity; objects have state, so they have identity and relationships
Line58 with each other.
Line59 The more code we write, the more we’re convinced that we should deﬁne
Line60 types to represent value concepts in the domain, even if they don’t do much. It
Line61 helps to create a consistent domain model that is more self-explanatory. If we
Line62 create, for example, an Item type in a system, instead of just using String, we can
Line63 ﬁnd all the code that’s relevant for a change without having to chase through the
Line64 method calls. Speciﬁc types also reduce the risk of confusion—as the Mars Climate
Line65 Orbiter disaster showed, feet and metres may both be represented as numbers
Line66 but they’re different things.1 Finally, once we have a type to represent a concept,
Line67 it usually turns out to be a good place to hang behavior, guiding us towards using
Line68 a more object-oriented approach instead of scattering related behavior across
Line69 the code.
Line70 We use three basic techniques for introducing value types, which we’ve called
Line71 (in a ﬁt of alliteration): breaking out, budding off, and bundling up.
Line72 Breaking out
Line73 When we ﬁnd that the code in an object is becoming complex, that’s often
Line74 a sign that it’s implementing multiple concerns and that we can break out
Line75 coherent units of behavior into helper types. There’s an example in “Tidying
Line76 Up the Translator” (page 135) where we break a class that handles incoming
Line77 messages into two parts: one to parse the message string, and one to interpret
Line78 the result of the parsing.
Line79 Budding off
Line80 When we want to mark a new domain concept in the code, we often introduce
Line81 a placeholder type that wraps a single ﬁeld, or maybe has no ﬁelds at all. As
Line82 the code grows, we ﬁll in more detail in the new type by adding ﬁelds and
Line83 methods. With each type that we add, we’re raising the level of abstraction
Line84 of the code.
Line85 Bundling up
Line86 When we notice that a group of values are always used together, we take
Line87 that as a suggestion that there’s a missing construct. A ﬁrst step might be to
Line88 create a new type with ﬁxed public ﬁelds—just giving the group a name
Line89 highlights the missing concept. Later we can migrate behavior to the new
Line90 1. In 1999, NASA’s Mars Climate Orbiter burned up in the planet’s atmosphere because,
Line91 amongst other problems, the navigation software confused metric with imperial units.
Line92 There’s a brief description at http://news.bbc.co.uk/1/hi/sci/tech/514763.stm.
Line93 59
Line94 Value Types
Line95 
Line96 
Line97 ---
