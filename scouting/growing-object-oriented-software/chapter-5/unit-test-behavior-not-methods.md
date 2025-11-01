Line1 # Unit-Test Behavior, Not Methods (pp.43-44)
Line2 
Line3 ---
Line4 **Page 43**
Line5 
Line6 we’re wrong. Second, more subtly, we ﬁnd that our emphasis on (or, perhaps,
Line7 mania for) expressing our intentions is fundamental for developing reliable,
Line8 maintainable systems—and for us that includes tests and failure messages. Taking
Line9 the trouble to generate a useful diagnostic helps us clarify what the test, and
Line10 therefore the code, is supposed to do. We look at error diagnostics and how to
Line11 improve them in Chapter 23.
Line12 Develop from the Inputs to the Outputs
Line13 We start developing a feature by considering the events coming into the system
Line14 that will trigger the new behavior. The end-to-end tests for the feature will simu-
Line15 late these events arriving. At the boundaries of our system, we will need to write
Line16 one or more objects to handle these events. As we do so, we discover that these
Line17 objects need supporting services from the rest of the system to perform their re-
Line18 sponsibilities. We write more objects to implement these services, and discover
Line19 what services these new objects need in turn.
Line20 In this way, we work our way through the system: from the objects that receive
Line21 external events, through the intermediate layers, to the central domain model,
Line22 and then on to other boundary objects that generate an externally visible response.
Line23 That might mean accepting some text and a mouse click and looking for a record
Line24 in a database, or receiving a message in a queue and looking for a ﬁle on a server.
Line25 It’s tempting to start by unit-testing new domain model objects and then trying
Line26 to hook them into the rest of the application. It seems easier at the start—we feel
Line27 we’re making rapid progress working on the domain model when we don’t have
Line28 to make it ﬁt into anything—but we’re more likely to get bitten by integration
Line29 problems later. We’ll have wasted time building unnecessary or incorrect func-
Line30 tionality, because we weren’t receiving the right kind of feedback when we were
Line31 working on it.
Line32 Unit-Test Behavior, Not Methods
Line33 We’ve learned the hard way that just writing lots of tests, even when it produces
Line34 high test coverage, does not guarantee a codebase that’s easy to work with. Many
Line35 developers who adopt TDD ﬁnd their early tests hard to understand when they
Line36 revisit them later, and one common mistake is thinking about testing methods.
Line37 A test called testBidAccepted() tells us what it does, but not what it’s for.
Line38 We do better when we focus on the features that the object under test should
Line39 provide, each of which may require collaboration with its neighbors and calling
Line40 more than one of its methods. We need to know how to use the class to achieve
Line41 a goal, not how to exercise all the paths through its code.
Line42 43
Line43 Unit-Test Behavior, Not Methods
Line44 
Line45 
Line46 ---
Line47 
Line48 ---
Line49 **Page 44**
Line50 
Line51 The Importance of Describing Behavior, Not API Features
Line52 Nat used to run a company that produced online advertising and branded content
Line53 for clients sponsoring sports teams. One of his clients sponsored a Formula One
Line54 racing team. Nat wrote a fun little game that simulated Formula One race strategies
Line55 for the client to put on the team’s website. It took him two weeks to write, from
Line56 initial idea to ﬁnal deliverable, and once he handed it over to the client he forgot
Line57 all about it.
Line58 It turned out, however, that the throw-away game was by far the most popular
Line59 content on the team’s website. For the next F1 season, the client wanted to capi-
Line60 talize on its success. They wanted the game to model the track of each Grand
Line61 Prix, to accommodate the latest F1 rules, to have a better model of car physics,
Line62 to simulate dynamic weather, overtaking, spin-outs, and more.
Line63 Nat had written the original version test-ﬁrst, so he expected it to be easy to
Line64 change. However, going back to the code, he found the tests very hard to under-
Line65 stand. He had written a test for each method of each object but couldn’t understand
Line66 from those tests how each object was meant to behave—what the responsibilities
Line67 of the object were and how the different methods of the object worked together.
Line68 It helps to choose test names that describe how the object behaves in the
Line69 scenario being tested. We look at this in more detail in “Test Names Describe
Line70 Features” (page 248).
Line71 Listen to the Tests
Line72 When writing unit and integration tests, we stay alert for areas of the code that
Line73 are difﬁcult to test. When we ﬁnd a feature that’s difﬁcult to test, we don’t just
Line74 ask ourselves how to test it, but also why is it difﬁcult to test.
Line75 Our experience is that, when code is difﬁcult to test, the most likely cause is
Line76 that our design needs improving. The same structure that makes the code difﬁcult
Line77 to test now will make it difﬁcult to change in the future. By the time that future
Line78 comes around, a change will be more difﬁcult still because we’ll have forgotten
Line79 what we were thinking when we wrote the code. For a successful system, it might
Line80 even be a completely different team that will have to live with the consequences
Line81 of our decisions.
Line82 Our response is to regard the process of writing tests as a valuable early
Line83 warning of potential maintenance problems and to use those hints to ﬁx a problem
Line84 while it’s still fresh. As Figure 5.3 shows, if we’re ﬁnding it hard to write the next
Line85 failing test, we look again at the design of the production code and often refactor
Line86 it before moving on.
Line87 Chapter 5
Line88 Maintaining the Test-Driven Cycle
Line89 44
Line90 
Line91 
Line92 ---
