Line1 # Mock Application Objects in Integration Tests (pp.71-74)
Line2 
Line3 ---
Line4 **Page 71**
Line5 
Line6 into the application domain model. In Chapter 25, we discuss a common example
Line7 where abstractions in the application’s domain model are implemented using a
Line8 persistence API.
Line9 There are some exceptions where mocking third-party libraries can be helpful.
Line10 We might use mocks to simulate behavior that is hard to trigger with the real
Line11 library, such as throwing exceptions. Similarly, we might use mocks to test a se-
Line12 quence of calls, for example making sure that a transaction is rolled back if there’s
Line13 a failure. There should not be many tests like this in a test suite.
Line14 This pattern does not apply to value types because, of course, we don’t need
Line15 to mock them. We still, however, have to make design decisions about how
Line16 much to use third-party value types in our code. They might be so fundamental
Line17 that we just use them directly. Often, however, we want to follow the same
Line18 principles of isolation as for third-party services, and translate between value
Line19 types appropriate to the application domain and to the external domain.
Line20 Mock Application Objects in Integration Tests
Line21 As described above, adapter objects are passive, reacting to calls from our code.
Line22 Sometimes, adapter objects must call back to objects from the application. Event-
Line23 based libraries, for example, usually expect the client to provide a callback object
Line24 to be notiﬁed when an event happens. In this case, the application code will give
Line25 the adapter its own event callback (deﬁned in terms of the application domain).
Line26 The adapter will then pass an adapter callback to the external library to receive
Line27 external events and translate them for the application callback.
Line28 In these cases, we do use mock objects when testing objects that integrate with
Line29 third-party code—but only to mock the callback interfaces deﬁned in the appli-
Line30 cation, to verify that the adapter translates events between domains correctly
Line31 (Figure 8.2).
Line32 Multithreading adds more complication to integration tests. For example,
Line33 third-party libraries may start background threads to deliver events to the appli-
Line34 cation code, so synchronization is a vital aspect of the design effort of adapter
Line35 layers; we discuss this further in Chapter 26.
Line36 Figure 8.2
Line37 Using mock objects in integration tests
Line38 71
Line39 Mock Application Objects in Integration Tests
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 72**
Line46 
Line47 This page intentionally left blank
