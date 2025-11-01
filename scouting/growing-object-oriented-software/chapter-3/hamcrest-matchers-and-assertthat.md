Line1 # Hamcrest Matchers and assertThat() (pp.24-25)
Line2 
Line3 ---
Line4 **Page 24**
Line5 
Line6 annotation.2 JUnit provides a small library of test runners. For example, the
Line7 Parameterized test runner lets you write data-driven tests in which the same test
Line8 methods are run for many different data values returned from a static method.
Line9 As we’ll see below, the jMock library uses a custom test runner to automatically
Line10 verify mock objects at the end of the test, before the test ﬁxture is torn down.
Line11 Hamcrest Matchers and assertThat()
Line12 Hamcrest is a framework for writing declarative match criteria. While not a
Line13 testing framework itself, Hamcrest is used by several testing frameworks, including
Line14 JUnit, jMock, and WindowLicker, which we use in the example in Part III.
Line15 A Hamcrest matcher reports whether a given object matches some criteria, can
Line16 describe its criteria, and can describe why an object does not meet its criteria.
Line17 For example, this code creates matchers for strings that contain a given substring
Line18 and uses them to make some assertions:
Line19 String s = "yes we have no bananas today";
Line20 Matcher<String> containsBananas = new StringContains("bananas");
Line21 Matcher<String> containsMangoes = new StringContains("mangoes");
Line22 assertTrue(containsBananas.matches(s));
Line23 assertFalse(containsMangoes.matches(s));
Line24 Matchers are not usually instantiated directly. Instead, Hamcrest provides
Line25 static factory methods for all of its matchers to make the code that creates
Line26 matchers more readable. For example:
Line27 assertTrue(containsString("bananas").matches(s));
Line28 assertFalse(containsString("mangoes").matches(s));
Line29 In practice, however, we use matchers in combination with JUnit’s
Line30 assertThat(), which uses matcher’s self-describing features to make clear exactly
Line31 what went wrong when an assertion fails.3 We can rewrite the assertions as:
Line32 assertThat(s, containsString("bananas"));
Line33 assertThat(s, not(containsString("mangoes"));
Line34 The second assertion demonstrates one of Hamcrest’s most useful features:
Line35 deﬁning new criteria by combining existing matchers. The not() method is a
Line36 factory function that creates a matcher that reverses the sense of any matcher
Line37 passed to it. Matchers are designed so that when they’re combined, both the code
Line38 and the failure messages are self-explanatory. For example, if we change the
Line39 second assertion to fail:
Line40 2. By the time of publication, JUnit will also have a Rule annotation for ﬁelds to support
Line41 objects that can “intercept” the lifecycle of a test run.
Line42 3. The assertThat() method was introduced in JUnit 4.5.
Line43 Chapter 3
Line44 An Introduction to the Tools
Line45 24
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 25**
Line52 
Line53 assertThat(s, not(containsString("bananas"));
Line54 the failure report is:
Line55 java.lang.AssertionError: 
Line56 Expected: not a string containing "bananas"
Line57      got: "Yes, we have no bananas"
Line58 Instead of writing code to explicitly check a condition and to generate an in-
Line59 formative error message, we can pass a matcher expression to assertThat() and
Line60 let it do the work.
Line61 Hamcrest is also user-extensible. If we need to check a speciﬁc condition,
Line62 we can write a new matcher by implementing the Matcher interface and an
Line63 appropriately-named factory method, and the result will combine seamlessly with
Line64 the existing matcher expressions. We describe how to write custom Hamcrest
Line65 matchers in Appendix B.
Line66 jMock2: Mock Objects
Line67 jMock2 plugs into JUnit (and other test frameworks) providing support for the
Line68 mock objects testing style introduced in Chapter 2. jMock creates mock objects
Line69 dynamically, so you don’t have to write your own implementations of the types
Line70 you want to mock. It also provides a high-level API for specifying how the object
Line71 under test should invoke the mock objects it interacts with, and how the mock
Line72 objects will behave in response.
Line73 Understanding jMock
Line74 jMock is designed to make the expectation descriptions as clear as possible. We
Line75 used some unusual Java coding practices to do so, which can appear surprising
Line76 at ﬁrst. jMock’s design was motivated by the ideas presented in this book, backed
Line77 by many years of experience in real projects. If the examples don’t make sense to
Line78 you, there’s more description in Appendix A and at www.jmock.org.We (of course)
Line79 believe that it’s worth suspending your judgment until you’ve had a chance to work
Line80 through some of the examples.
Line81 The core concepts of the jMock API are the mockery, mock objects, and expec-
Line82 tations. A mockery represents the context of the object under test, its neighboring
Line83 objects; mock objects stand in for the real neighbors of the object under test while
Line84 the test runs; and expectations describe how the object under test should invoke
Line85 its neighbors during the test.
Line86 An example will show how these ﬁt together. This test asserts that an
Line87 AuctionMessageTranslator will parse a given message text to generate
Line88 an auctionClosed() event. For now, just concentrate on the structure; the test
Line89 will turn up again in context in Chapter 12.
Line90 25
Line91 jMock2: Mock Objects
Line92 
Line93 
Line94 ---
