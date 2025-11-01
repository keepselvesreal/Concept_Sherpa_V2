Line1 # Watch the Test Fail (pp.42-43)
Line2 
Line3 ---
Line4 **Page 42**
Line5 
Line6 Write the Test That You’d Want to Read
Line7 We want each test to be as clear as possible an expression of the behavior to be
Line8 performed by the system or object. While writing the test, we ignore the fact that
Line9 the test won’t run, or even compile, and just concentrate on its text; we act as
Line10 if the supporting code to let us run the test already exists.
Line11 When the test reads well, we then build up the infrastructure to support the
Line12 test. We know we’ve implemented enough of the supporting code when the test
Line13 fails in the way we’d expect, with a clear error message describing what needs
Line14 to be done. Only then do we start writing the code to make the test pass. We
Line15 look further at making tests readable in Chapter 21.
Line16 Watch the Test Fail
Line17 We always watch the test fail before writing the code to make it pass, and check
Line18 the diagnostic message. If the test fails in a way we didn’t expect, we know we’ve
Line19 misunderstood something or the code is incomplete, so we ﬁx that. When we get
Line20 the “right” failure, we check that the diagnostics are helpful. If the failure descrip-
Line21 tion isn’t clear, someone (probably us) will have to struggle when the code breaks
Line22 in a few weeks’ time. We adjust the test code and rerun the tests until the error
Line23 messages guide us to the problem with the code (Figure 5.2).
Line24 Figure 5.2
Line25 Improving the diagnostics as part of the TDD cycle
Line26 As we write the production code, we keep running the test to see our progress
Line27 and to check the error diagnostics as the system is built up behind the test. Where
Line28 necessary, we extend or modify the support code to ensure the error messages
Line29 are always clear and relevant.
Line30 There’s more than one reason for insisting on checking the error messages.
Line31 First, it checks our assumptions about the code we’re working on—sometimes
Line32 Chapter 5
Line33 Maintaining the Test-Driven Cycle
Line34 42
Line35 
Line36 
Line37 ---
Line38 
Line39 ---
Line40 **Page 43**
Line41 
Line42 we’re wrong. Second, more subtly, we ﬁnd that our emphasis on (or, perhaps,
Line43 mania for) expressing our intentions is fundamental for developing reliable,
Line44 maintainable systems—and for us that includes tests and failure messages. Taking
Line45 the trouble to generate a useful diagnostic helps us clarify what the test, and
Line46 therefore the code, is supposed to do. We look at error diagnostics and how to
Line47 improve them in Chapter 23.
Line48 Develop from the Inputs to the Outputs
Line49 We start developing a feature by considering the events coming into the system
Line50 that will trigger the new behavior. The end-to-end tests for the feature will simu-
Line51 late these events arriving. At the boundaries of our system, we will need to write
Line52 one or more objects to handle these events. As we do so, we discover that these
Line53 objects need supporting services from the rest of the system to perform their re-
Line54 sponsibilities. We write more objects to implement these services, and discover
Line55 what services these new objects need in turn.
Line56 In this way, we work our way through the system: from the objects that receive
Line57 external events, through the intermediate layers, to the central domain model,
Line58 and then on to other boundary objects that generate an externally visible response.
Line59 That might mean accepting some text and a mouse click and looking for a record
Line60 in a database, or receiving a message in a queue and looking for a ﬁle on a server.
Line61 It’s tempting to start by unit-testing new domain model objects and then trying
Line62 to hook them into the rest of the application. It seems easier at the start—we feel
Line63 we’re making rapid progress working on the domain model when we don’t have
Line64 to make it ﬁt into anything—but we’re more likely to get bitten by integration
Line65 problems later. We’ll have wasted time building unnecessary or incorrect func-
Line66 tionality, because we weren’t receiving the right kind of feedback when we were
Line67 working on it.
Line68 Unit-Test Behavior, Not Methods
Line69 We’ve learned the hard way that just writing lots of tests, even when it produces
Line70 high test coverage, does not guarantee a codebase that’s easy to work with. Many
Line71 developers who adopt TDD ﬁnd their early tests hard to understand when they
Line72 revisit them later, and one common mistake is thinking about testing methods.
Line73 A test called testBidAccepted() tells us what it does, but not what it’s for.
Line74 We do better when we focus on the features that the object under test should
Line75 provide, each of which may require collaboration with its neighbors and calling
Line76 more than one of its methods. We need to know how to use the class to achieve
Line77 a goal, not how to exercise all the paths through its code.
Line78 43
Line79 Unit-Test Behavior, Not Methods
Line80 
Line81 
Line82 ---
