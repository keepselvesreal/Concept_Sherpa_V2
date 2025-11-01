Line1 # How Writing a Test First Helps the Design (pp.57-58)
Line2 
Line3 ---
Line4 **Page 57**
Line5 
Line6 Chapter 7
Line7 Achieving Object-Oriented
Line8 Design
Line9 In matters of style, swim with the current; in matters of principle, stand
Line10 like a rock.
Line11 —Thomas Jefferson
Line12 How Writing a Test First Helps the Design
Line13 The design principles we outlined in the previous chapter apply to ﬁnding the
Line14 right boundaries for an object so that it plays well with its neighbors—a caller
Line15 wants to know what an object does and what it depends on, but not how it
Line16 works. We also want an object to represent a coherent unit that makes sense in
Line17 its larger environment. A system built from such components will have the
Line18 ﬂexibility to reconﬁgure and adapt as requirements change.
Line19 There are three aspects of TDD that help us achieve this scoping. First, starting
Line20 with a test means that we have to describe what we want to achieve before we
Line21 consider how. This focus helps us maintain the right level of abstraction for the
Line22 target object. If the intention of the unit test is unclear then we’re probably
Line23 mixing up concepts and not ready to start coding. It also helps us with information
Line24 hiding as we have to decide what needs to be visible from outside the object.
Line25 Second, to keep unit tests understandable (and, so, maintainable), we have to
Line26 limit their scope. We’ve seen unit tests that are dozens of lines long, burying the
Line27 point of the test somewhere in its setup. Such tests tell us that the component
Line28 they’re testing is too large and needs breaking up into smaller components. The
Line29 resulting composite object should have a clearer separation of concerns as we
Line30 tease out its implicit structure, and we can write simpler tests for the extracted
Line31 objects.
Line32 Third, to construct an object for a unit test, we have to pass its dependencies
Line33 to it, which means that we have to know what they are. This encourages context
Line34 independence, since we have to be able to set up the target object’s environment
Line35 before we can unit-test it—a unit test is just another context. We’ll notice that
Line36 an object with implicit (or just too many) dependencies is painful to prepare for
Line37 testing—and make a point of cleaning it up.
Line38 In this chapter, we describe how we use an incremental, test-driven approach
Line39 to nudge our code towards the design principles we described in the previous
Line40 chapter.
Line41 57
Line42 
Line43 
Line44 ---
Line45 
Line46 ---
Line47 **Page 58**
Line48 
Line49 Communication over Classiﬁcation
Line50 As we wrote in Chapter 2, we view a running system as a web of communicating
Line51 objects, so we focus our design effort on how the objects collaborate to deliver
Line52 the functionality we need. Obviously, we want to achieve a well-designed class
Line53 structure, but we think the communication patterns between objects are more
Line54 important.
Line55 In languages such as Java, we can use interfaces to deﬁne the available messages
Line56 between objects, but we also need to deﬁne their patterns of communication—their
Line57 communication protocols. We do what we can with naming and convention, but
Line58 there’s nothing in the language to describe relationships between interfaces or
Line59 methods within an interface, which leaves a signiﬁcant part of the design implicit.
Line60 Interface and Protocol
Line61 Steve heard this useful distinction in a conference talk: an interface describes
Line62 whether two components will ﬁt together, while a protocol describes whether they
Line63 will work together.
Line64 We use TDD with mock objects as a technique to make these communication
Line65 protocols visible, both as a tool for discovering them during development and
Line66 as a description when revisiting the code. For example, the unit test towards the
Line67 end of Chapter 3 tells us that, given a certain input message, the translator
Line68 should call listener.auctionClosed() exactly once—and nothing else. Although
Line69 the listener interface has other methods, this test says that its protocol requires
Line70 that auctionClosed() should be called on its own.
Line71 @Test public void
Line72 notifiesAuctionClosedWhenCloseMessageReceived() {
Line73   Message message = new Message();
Line74   message.setBody("SOLVersion: 1.1; Event: CLOSE;");
Line75   context.checking(new Expectations() {{ 
Line76     oneOf(listener).auctionClosed(); 
Line77   }});
Line78   translator.processMessage(UNUSED_CHAT, message); 
Line79 }
Line80 TDD with mock objects also encourages information hiding. We should mock
Line81 an object’s peers—its dependencies, notiﬁcations, and adjustments we categorized
Line82 on page 52—but not its internals. Tests that highlight an object’s neighbors help
Line83 us to see whether they are peers, or should instead be internal to the target object.
Line84 A test that is clumsy or unclear might be a hint that we’ve exposed too much
Line85 implementation, and that we should rebalance the responsibilities between the
Line86 object and its neighbors.
Line87 Chapter 7
Line88 Achieving Object-Oriented Design
Line89 58
Line90 
Line91 
Line92 ---
