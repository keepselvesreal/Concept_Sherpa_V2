Line1 # Design to Fail (pp.267-268)
Line2 
Line3 ---
Line4 **Page 267**
Line5 
Line6 Chapter 23
Line7 Test Diagnostics
Line8 Mistakes are the portals of discovery.
Line9 —James Joyce
Line10 Design to Fail
Line11 The point of a test is not to pass but to fail. We want the production code to
Line12 pass its tests, but we also want the tests to detect and report any errors that
Line13 do exist. A “failing” test has actually succeeded at the job it was designed to do.
Line14 Even unexpected test failures, in an area unrelated to where we are working, can
Line15 be valuable because they reveal implicit relationships in the code that we hadn’t
Line16 noticed.
Line17 One situation we want to avoid, however, is when we can’t diagnose a test
Line18 failure that has happened. The last thing we should have to do is crack open the
Line19 debugger and step through the tested code to ﬁnd the point of disagreement. At
Line20 a minimum, it suggests that our tests don’t yet express our requirements clearly
Line21 enough. In the worst case, we can ﬁnd ourselves in “debug hell,” with deadlines
Line22 to meet but no idea of how long a ﬁx will take. At this point, the temptation will
Line23 be high to just delete the test—and lose our safety net.
Line24 Stay Close to Home
Line25 Synchronize frequently with the source code repository—up to every few minutes—
Line26 so that if a test fails unexpectedly it won’t cost much to revert your recent changes
Line27 and try another approach.
Line28 The other implication of this tip is not to be too inhibited about dropping code and
Line29 trying again. Sometimes it’s quicker to roll back and restart with a clear head than
Line30 to keep digging.
Line31 We’ve learned the hard way to make tests fail informatively. If a failing test
Line32 clearly explains what has failed and why, we can quickly diagnose and correct
Line33 the code. Then, we can get on with the next task.
Line34 Chapter 21 addressed the static readability of tests. This chapter describes
Line35 some practices that we ﬁnd helpful to make sure the tests give us the information
Line36 we need at runtime.
Line37 267
Line38 
Line39 
Line40 ---
Line41 
Line42 ---
Line43 **Page 268**
Line44 
Line45 Small, Focused, Well-Named Tests
Line46 The easiest way to improve diagnostics is to keep each test small and focused
Line47 and give tests readable names, as described in Chapter 21. If a test is small, its
Line48 name should tell us most of what we need to know about what has gone wrong.
Line49 Explanatory Assertion Messages
Line50 JUnit’s assertion methods all have a version in which the ﬁrst parameter is a
Line51 message to display when the assertion fails. From what we’ve seen, this feature
Line52 is not used as often as it should be to make assertion failures more helpful.
Line53 For example, when this test fails:
Line54 Customer customer  = order.getCustomer();
Line55 assertEquals("573242", customer.getAccountId());
Line56 assertEquals(16301, customer.getOutstandingBalance());
Line57 the report does not make it obvious which of the assertions has failed:
Line58 ComparisonFailure: expected:<[16301]> but was:<[16103]>
Line59 The message is describing the symptom (the balance is 16103) rather than the
Line60 cause (the outstanding balance calculation is wrong).
Line61 If we add a message to identify the value being asserted:
Line62 assertEquals("account id", "573242", customer.getAccountId());
Line63 assertEquals("outstanding balance", 16301, customer.getOustandingBalance());
Line64 we can immediately see what the point is:
Line65 ComparisonFailure: outstanding balance expected:<[16301]> but was:<[16103]>
Line66 Highlight Detail with Matchers
Line67 Developers can provide another level of diagnostic detail by using assertThat()
Line68 with Hamcrest matchers. The Matcher API includes support for describing the
Line69 value that mismatched, to help with understanding exactly what is different. For
Line70 example, the instrument strike price assertion on page 252 generates this failure
Line71 report:
Line72 Expected: a collection containing instrument at price a value greater than <81>
Line73      but: price was <50>, price was <72>, price was <31>
Line74 which shows exactly which values are relevant.
Line75 Chapter 23
Line76 Test Diagnostics
Line77 268
Line78 
Line79 
Line80 ---
