Line1 # Develop from the Inputs to the Outputs (pp.43-43)
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
