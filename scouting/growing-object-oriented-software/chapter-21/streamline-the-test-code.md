Line1 # Streamline the Test Code (pp.252-254)
Line2 
Line3 ---
Line4 **Page 252**
Line5 
Line6 @Test public void writesMessageTranslationFailureToLog() {
Line7     Exception exception = new Exception("an exception");
Line8     context.checking(new Expectations() {{          // Expect
Line9       oneOf(logger).severe( expected log message here);
Line10     }});
Line11     reporter.cannotTranslateMessage("auction id",   // Execute
Line12                                     "failed message", exception); 
Line13 // implicitly check expectations are satisfied
Line14 // Assert
Line15   }
Line16   @AfterClass public static void resetLogging() {   // Teardown
Line17     LogManager.getLogManager().reset();
Line18   }  
Line19 }
Line20 Write Tests Backwards
Line21 Although we stick to a canonical format for test code, we don’t necessarily write
Line22 tests from top to bottom. What we often do is: write the test name, which helps us
Line23 decide what we want to achieve; write the call to the target code, which is the entry
Line24 point for the feature; write the expectations and assertions, so we know what effects
Line25 the feature should have; and, write the setup and teardown to deﬁne the context
Line26 for the test. Of course, there may be some blurring of these steps to help the
Line27 compiler, but this sequence reﬂects how we tend to think through a new unit test.
Line28 Then we run it and watch it fail.
Line29 How Many Assertions in a Test Method?
Line30 Some TDD practitioners suggest that each test should only contain one expectation
Line31 or assertion.This is useful as a training rule when learning TDD, to avoid asserting
Line32 everything the developer can think of, but we don’t ﬁnd it practical. A better rule
Line33 is to think of one coherent feature per test, which might be represented by up to
Line34 a handful of assertions. If a single test seems to be making assertions about
Line35 different features of a target object, it might be worth splitting up. Once again,
Line36 expressiveness is the key: as a reader of this test, can I ﬁgure out what’s
Line37 signiﬁcant?
Line38 Streamline the Test Code
Line39 All code should emphasize “what” it does over “how,” including test code; the
Line40 more implementation detail is included in a test method, the harder it is for
Line41 the reader to understand what’s important. We try to move everything out
Line42 of the test method that doesn’t contribute to the description, in domain
Line43 terms, of the feature being exercised. Sometimes that involves restructuring the
Line44 code, sometimes just ignoring the syntax noise.
Line45 Chapter 21
Line46 Test Readability
Line47 252
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 253**
Line54 
Line55 Use Structure to Explain
Line56 As you’ll have seen throughout Part III, we make a point of following “Small
Line57 Methods to Express Intent” (page 226), even to the extent of writing a tiny
Line58 method like translatorFor() just to reduce the Java syntax noise. This ﬁts
Line59 nicely into the Hamcrest approach, where the assertThat() and jMock expecta-
Line60 tion syntaxes are designed to allow developers to compose small features into a
Line61 (more or less) readable description of an assertion. For example,
Line62 assertThat(instruments, hasItem(instrumentWithPrice(greaterThan(81))));
Line63 checks whether the collection instruments has at least one Instrument with a
Line64 strikePrice property greater than 81. The assertion line expresses our intent,
Line65 the helper method creates a matcher that checks the value:
Line66 private Matcher<? super Instrument> 
Line67 instrumentWithPrice(Matcher<? super Integer> priceMatcher) {
Line68   return new FeatureMatcher<Instrument, Integer>(
Line69                priceMatcher, "instrument at price", "price") {
Line70     @Override protected Integer featureValueOf(Instrument actual) {
Line71       return actual.getStrikePrice();
Line72     }
Line73   };
Line74 }
Line75 This may create more program text in the end, but we’re prioritizing expressive-
Line76 ness over minimizing the source lines.
Line77 Use Structure to Share
Line78 We also extract common features into methods that can be shared between tests
Line79 for setting up values, tearing down state, making assertions, and occasionally
Line80 triggering the event. For example, in Chapter 19, we exploited jMock’s facility
Line81 for setting multiple expectation blocks to write a expectSniperToFailWhenItIs()
Line82 method that wraps up repeated behavior behind a descriptive name.
Line83 The only caution with factoring out test structure is that, as we said in the in-
Line84 troduction to this chapter, we have to be careful not to make a test so abstract
Line85 that we cannot see what it does any more. Our highest concern is making the
Line86 test describe what the target code does, so we refactor enough to be able to see
Line87 its ﬂow, but we don’t always refactor as hard as we would for production code.
Line88 Accentuate the Positive
Line89 We only catch exceptions in a test if we want to assert something about them. We
Line90 sometimes see tests like this:
Line91 253
Line92 Streamline the Test Code
Line93 
Line94 
Line95 ---
Line96 
Line97 ---
Line98 **Page 254**
Line99 
Line100 @Test public void expandsMacrosSurroundedWithBraces() {
Line101   StringTemplate template = new StringTemplate("{a}{b}");
Line102   try {
Line103     String expanded = template.expand(macros);
Line104     assertThat(expanded, equalTo("AB"));
Line105   } catch (TemplateFormatException e) {
Line106     fail("Template failed: " + e);
Line107   }
Line108 }
Line109 If this test is intended to pass, then converting the exception actually drops infor-
Line110 mation from the stack trace. The simplest thing to do is to let the exception
Line111 propagate for the test runtime to catch. We can add arbitrary exceptions to the
Line112 test method signature because it’s only called by reﬂection. This removes at least
Line113 half the lines of the test, and we can compact it further to be:
Line114 @Test public void expandsMacrosSurroundedWithBraces() throws Exception {
Line115   assertThat(new StringTemplate("{a}{b}").expand(macros),
Line116              equalTo("AB"));
Line117 }
Line118 which tells us just what is supposed to happen and ignores everything else.
Line119 Delegate to Subordinate Objects
Line120 Sometimes helper methods aren’t enough and we need helper objects to support
Line121 the tests. We saw this in the test rig we built in Chapter 11. We developed the
Line122 ApplicationRunner, AuctionSniperDriver, and FakeAuctionServer classes so we
Line123 could write tests in terms of auctions and Snipers, not in terms of Swing and
Line124 messaging.
Line125 A more common technique is to write test data builders to build up complex
Line126 data structures with just the appropriate values for a test; see Chapter 22 for
Line127 more detail. Again, the point is to include in the test just the values that are rele-
Line128 vant, so that the reader can understand the intent; everything else can be defaulted.
Line129 There are two approaches to writing subordinate objects. In Chapter 11 we
Line130 started by writing the test we wanted to see and then ﬁlling in the supporting
Line131 objects: start from a statement of the problem and see where it goes. The alterna-
Line132 tive is to write the code directly in the tests, and then refactor out any clusters
Line133 of behavior. This is the origin of the WindowLicker framework, which started
Line134 out as helper code in JUnit tests for interacting with the Swing event dispatcher
Line135 and eventually grew into a separate project.
Line136 Assertions and Expectations
Line137 The assertions and expectations of a test should communicate precisely what
Line138 matters in the behavior of the target code. We regularly see code where tests assert
Line139 Chapter 21
Line140 Test Readability
Line141 254
Line142 
Line143 
Line144 ---
