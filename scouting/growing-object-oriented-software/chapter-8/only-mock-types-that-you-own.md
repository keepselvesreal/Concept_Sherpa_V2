Line1 # Only Mock Types That You Own (pp.69-71)
Line2 
Line3 ---
Line4 **Page 69**
Line5 
Line6 Chapter 8
Line7 Building on Third-Party Code
Line8 Programming today is all about doing science on the parts you have
Line9 to work with.
Line10 —Gerald Jay Sussman
Line11 Introduction
Line12 We’ve shown how we pull a system’s design into existence: discovering what our
Line13 objects need and writing interfaces and further objects to meet those needs. This
Line14 process works well for new functionality. At some point, however, our design
Line15 will come up against a need that is best met by third-party code: standard APIs,
Line16 open source libraries, or vendor products. The critical point about third-party
Line17 code is that we don’t control it, so we cannot use our process to guide its design.
Line18 Instead, we must focus on the integration between our design and the
Line19 external code.
Line20 In integration, we have an abstraction to implement, discovered while we de-
Line21 veloped the rest of the feature. With the third-party API pushing back at our
Line22 design, we must ﬁnd the best balance between elegance and practical use of
Line23 someone else’s ideas. We must check that we are using the third-party API cor-
Line24 rectly, and adjust our abstraction to ﬁt if we ﬁnd that our assumptions are
Line25 incorrect.
Line26 Only Mock Types That You Own
Line27 Don’t Mock Types You Can’t Change
Line28 When we use third-party code we often do not have a deep understanding of
Line29 how it works. Even if we have the source available, we rarely have time to read
Line30 it thoroughly enough to explore all its quirks. We can read its documentation,
Line31 which is often incomplete or incorrect. The software may also have bugs that we
Line32 will need to work around. So, although we know how we want our abstraction
Line33 to behave, we don’t know if it really does so until we test it in combination with
Line34 the third-party code.
Line35 We also prefer not to change third-party code, even when we have the sources.
Line36 It’s usually too much trouble to apply private patches every time there’s a new
Line37 version. If we can’t change an API, then we can’t respond to any design feedback
Line38 we get from writing unit tests that touch it. Whatever alarm bells the unit tests
Line39 69
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 70**
Line46 
Line47 might be ringing about the awkwardness of an external API, we have to live with
Line48 it as it stands.
Line49 This means that providing mock implementations of third-party types is of
Line50 limited use when unit-testing the objects that call them. We ﬁnd that tests that
Line51 mock external libraries often need to be complex to get the code into the right
Line52 state for the functionality we need to exercise. The mess in such tests is telling
Line53 us that the design isn’t right but, instead of ﬁxing the problem by improving the
Line54 code, we have to carry the extra complexity in both code and test.
Line55 A second risk is that we have to be sure that the behavior we stub or mock
Line56 matches what the external library will actually do. How difﬁcult this is depends
Line57 on the quality of the library—whether it’s speciﬁed (and implemented) well
Line58 enough for us to be certain that our unit tests are valid. Even if we get it right
Line59 once, we have to make sure that the tests remain valid when we upgrade the
Line60 libraries.
Line61 Write an Adapter Layer
Line62 If we don’t want to mock an external API, how can we test the code that drives
Line63 it? We will have used TDD to design interfaces for the services our objects
Line64 need—which will be deﬁned in terms of our objects’ domain, not the external
Line65 library.
Line66 We write a layer of adapter objects (as described in [Gamma94]) that uses the
Line67 third-party API to implement these interfaces, as in Figure 8.1. We keep this
Line68 layer as thin as possible, to minimize the amount of potentially brittle and hard-
Line69 to-test code. We test these adapters with focused integration tests to conﬁrm our
Line70 understanding of how the third-party API works. There will be relatively few
Line71 integration tests compared to the number of unit tests, so they should not get in
Line72 the way of the build even if they’re not as fast as the in-memory unit tests.
Line73 Figure 8.1
Line74 Mockable adapters to third-party objects
Line75 Following this approach consistently produces a set of interfaces that deﬁne
Line76 the relationship between our application and the rest of the world in our
Line77 application’s terms and discourages low-level technical concepts from leaking
Line78 Chapter 8
Line79 Building on Third-Party Code
Line80 70
Line81 
Line82 
Line83 ---
Line84 
Line85 ---
Line86 **Page 71**
Line87 
Line88 into the application domain model. In Chapter 25, we discuss a common example
Line89 where abstractions in the application’s domain model are implemented using a
Line90 persistence API.
Line91 There are some exceptions where mocking third-party libraries can be helpful.
Line92 We might use mocks to simulate behavior that is hard to trigger with the real
Line93 library, such as throwing exceptions. Similarly, we might use mocks to test a se-
Line94 quence of calls, for example making sure that a transaction is rolled back if there’s
Line95 a failure. There should not be many tests like this in a test suite.
Line96 This pattern does not apply to value types because, of course, we don’t need
Line97 to mock them. We still, however, have to make design decisions about how
Line98 much to use third-party value types in our code. They might be so fundamental
Line99 that we just use them directly. Often, however, we want to follow the same
Line100 principles of isolation as for third-party services, and translate between value
Line101 types appropriate to the application domain and to the external domain.
Line102 Mock Application Objects in Integration Tests
Line103 As described above, adapter objects are passive, reacting to calls from our code.
Line104 Sometimes, adapter objects must call back to objects from the application. Event-
Line105 based libraries, for example, usually expect the client to provide a callback object
Line106 to be notiﬁed when an event happens. In this case, the application code will give
Line107 the adapter its own event callback (deﬁned in terms of the application domain).
Line108 The adapter will then pass an adapter callback to the external library to receive
Line109 external events and translate them for the application callback.
Line110 In these cases, we do use mock objects when testing objects that integrate with
Line111 third-party code—but only to mock the callback interfaces deﬁned in the appli-
Line112 cation, to verify that the adapter translates events between domains correctly
Line113 (Figure 8.2).
Line114 Multithreading adds more complication to integration tests. For example,
Line115 third-party libraries may start background threads to deliver events to the appli-
Line116 cation code, so synchronization is a vital aspect of the design effort of adapter
Line117 layers; we discuss this further in Chapter 26.
Line118 Figure 8.2
Line119 Using mock objects in integration tests
Line120 71
Line121 Mock Application Objects in Integration Tests
Line122 
Line123 
Line124 ---
