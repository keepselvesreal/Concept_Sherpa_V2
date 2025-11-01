Line1 # Diagnostics Are a First-Class Feature (pp.271-272)
Line2 
Line3 ---
Line4 **Page 271**
Line5 
Line6 Notice that jMock can accept a name when creating a mock object that will
Line7 be used in failure reporting. In fact, where there’s more than one mock object of
Line8 the same type, jMock insists that they are named to avoid confusion (the default
Line9 is to use the class name).
Line10 Tracer objects can be a useful design tool when TDD’ing a class. We sometimes
Line11 use an empty interface to mark (and name) a domain concept and show how
Line12 it’s used in a collaboration. Later, as we grow the code, we ﬁll in the interface
Line13 with methods to describe its behavior.
Line14 Explicitly Assert That Expectations Were Satisﬁed
Line15 A test that has both expectations and assertions can produce a confusing failure.
Line16 In jMock and other mock object frameworks, the expectations are checked after
Line17 the body of the test. If, for example, a collaboration doesn’t work properly and
Line18 returns a wrong value, an assertion might fail before any expectations are checked.
Line19 This would produce a failure report that shows, say, an incorrect calculation result
Line20 rather than the missing collaboration that actually caused it.
Line21 In a few cases, then, it’s worth calling the assertIsSatisfied() method on
Line22 the Mockery before any of the test assertions to get the right failure report:
Line23 context.assertIsSatisfied();
Line24 assertThat(result, equalTo(expectedResult));
Line25 This demonstrates why it is important to “Watch the Test Fail” (page 42). If
Line26 you expect the test to fail because an expectation is not satisﬁed but a postcondi-
Line27 tion assertion fails instead, you will see that you should add an explicit call to
Line28 assert that all expectations have been satisﬁed.
Line29 Diagnostics Are a First-Class Feature
Line30 Like everyone else, we ﬁnd it easy to get carried away with the simple three-step
Line31 TDD cycle: fail, pass, refactor. We’re making good progress and we know what
Line32 the failures mean because we’ve just written the test. But nowadays, we try to
Line33 follow the four-step TDD cycle (fail, report, pass, refactor) we described in
Line34 Chapter 5, because that’s how we know we’ve understood the feature—and
Line35 whoever has to change it in a month’s time will also understand it. Figure 23.1
Line36 shows again that we need to maintain the quality of the tests, as well as the
Line37 production code.
Line38 271
Line39 Diagnostics Are a First-Class Feature
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 272**
Line46 
Line47 Figure 23.1
Line48 Improve the diagnostics as part of the TDD cycle
Line49 Chapter 23
Line50 Test Diagnostics
Line51 272
