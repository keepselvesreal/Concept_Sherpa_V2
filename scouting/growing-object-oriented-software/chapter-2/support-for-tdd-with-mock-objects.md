Line1 # Support for TDD with Mock Objects (pp.19-20)
Line2 
Line3 ---
Line4 **Page 19**
Line5 
Line6 Figure 2.4
Line7 Unit-testing an object in isolation
Line8 Figure 2.5
Line9 Testing an object with mock objects
Line10 have been called as expected; they also implement any stubbed behavior needed
Line11 to make the rest of the test work.
Line12 With this infrastructure in place, we can change the way we approach TDD.
Line13 Figure 2.5 implies that we’re just trying to test the target object and that we al-
Line14 ready know what its neighbors look like. In practice, however, those collaborators
Line15 don’t need to exist when we’re writing a unit test. We can use the test to help us
Line16 tease out the supporting roles our object needs, deﬁned as Java interfaces, and
Line17 ﬁll in real implementations as we develop the rest of the system. We call this in-
Line18 terface discovery; you’ll see an example when we extract an AuctionEventListener
Line19 in Chapter 12.
Line20 Support for TDD with Mock Objects
Line21 To support this style of test-driven programming, we need to create mock in-
Line22 stances of the neighboring objects, deﬁne expectations on how they’re called and
Line23 then check them, and implement any stub behavior we need to get through the
Line24 test. In practice, the runtime structure of a test with mock objects usually looks
Line25 like Figure 2.6.
Line26 19
Line27 Support for TDD with Mock Objects
Line28 
Line29 
Line30 ---
Line31 
Line32 ---
Line33 **Page 20**
Line34 
Line35 Figure 2.6
Line36 Testing an object with mock objects
Line37 We use the term mockery2 for the object that holds the context of a test, creates
Line38 mock objects, and manages expectations and stubbing for the test. We’ll show
Line39 the practice throughout Part III, so we’ll just touch on the basics here. The
Line40 essential structure of a test is:
Line41 •
Line42 Create any required mock objects.
Line43 •
Line44 Create any real objects, including the target object.
Line45 •
Line46 Specify how you expect the mock objects to be called by the target object.
Line47 •
Line48 Call the triggering method(s) on the target object.
Line49 •
Line50 Assert that any resulting values are valid and that all the expected calls have
Line51 been made.
Line52 The unit test makes explicit the relationship between the target object and its
Line53 environment. It creates all the objects in the cluster and makes assertions about
Line54 the interactions between the target object and its collaborators. We can code this
Line55 infrastructure by hand or, these days, use one of the multiple mock object
Line56 frameworks that are available in many languages. The important point, as we
Line57 stress repeatedly throughout this book, is to make clear the intention of every
Line58 test, distinguishing between the tested functionality, the supporting infrastructure,
Line59 and the object structure.
Line60 2. This is a pun by Ivan Moore that we adopted in a ﬁt of whimsy.
Line61 Chapter 2
Line62 Test-Driven Development with Objects
Line63 20
