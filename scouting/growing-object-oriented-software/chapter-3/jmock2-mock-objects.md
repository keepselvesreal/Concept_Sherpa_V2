Line1 # jMock2: Mock Objects (pp.25-30)
Line2 
Line3 ---
Line4 **Page 25**
Line5 
Line6 assertThat(s, not(containsString("bananas"));
Line7 the failure report is:
Line8 java.lang.AssertionError: 
Line9 Expected: not a string containing "bananas"
Line10      got: "Yes, we have no bananas"
Line11 Instead of writing code to explicitly check a condition and to generate an in-
Line12 formative error message, we can pass a matcher expression to assertThat() and
Line13 let it do the work.
Line14 Hamcrest is also user-extensible. If we need to check a speciﬁc condition,
Line15 we can write a new matcher by implementing the Matcher interface and an
Line16 appropriately-named factory method, and the result will combine seamlessly with
Line17 the existing matcher expressions. We describe how to write custom Hamcrest
Line18 matchers in Appendix B.
Line19 jMock2: Mock Objects
Line20 jMock2 plugs into JUnit (and other test frameworks) providing support for the
Line21 mock objects testing style introduced in Chapter 2. jMock creates mock objects
Line22 dynamically, so you don’t have to write your own implementations of the types
Line23 you want to mock. It also provides a high-level API for specifying how the object
Line24 under test should invoke the mock objects it interacts with, and how the mock
Line25 objects will behave in response.
Line26 Understanding jMock
Line27 jMock is designed to make the expectation descriptions as clear as possible. We
Line28 used some unusual Java coding practices to do so, which can appear surprising
Line29 at ﬁrst. jMock’s design was motivated by the ideas presented in this book, backed
Line30 by many years of experience in real projects. If the examples don’t make sense to
Line31 you, there’s more description in Appendix A and at www.jmock.org.We (of course)
Line32 believe that it’s worth suspending your judgment until you’ve had a chance to work
Line33 through some of the examples.
Line34 The core concepts of the jMock API are the mockery, mock objects, and expec-
Line35 tations. A mockery represents the context of the object under test, its neighboring
Line36 objects; mock objects stand in for the real neighbors of the object under test while
Line37 the test runs; and expectations describe how the object under test should invoke
Line38 its neighbors during the test.
Line39 An example will show how these ﬁt together. This test asserts that an
Line40 AuctionMessageTranslator will parse a given message text to generate
Line41 an auctionClosed() event. For now, just concentrate on the structure; the test
Line42 will turn up again in context in Chapter 12.
Line43 25
Line44 jMock2: Mock Objects
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 26**
Line51 
Line52 @RunWith(JMock.class) 1
Line53 public class AuctionMessageTranslatorTest {
Line54   private final Mockery context = new JUnit4Mockery(); 2
Line55   private final AuctionEventListener listener =  
Line56                               context.mock(AuctionEventListener.class); 3
Line57   private final AuctionMessageTranslator translator = 
Line58                                 new AuctionMessageTranslator(listener); 4
Line59   @Test public void
Line60 notifiesAuctionClosedWhenCloseMessageReceived() {
Line61     Message message = new Message();
Line62     message.setBody("SOLVersion: 1.1; Event: CLOSE;"); 5
Line63     context.checking(new Expectations() {{ 6
Line64       oneOf(listener).auctionClosed(); 7
Line65     }});
Line66     translator.processMessage(UNUSED_CHAT, message); 8
Line67   } 9
Line68 }
Line69 1
Line70 The @RunWith(JMock.class) annotation tells JUnit to use the jMock test
Line71 runner, which automatically calls the mockery at the end of the test to check
Line72 that all mock objects have been invoked as expected.
Line73 2
Line74 The test creates the Mockery. Since this is a JUnit 4 test, it creates a
Line75 JUnit4Mockery which throws the right type of exception to report test failures
Line76 to JUnit 4. By convention, jMock tests hold the mockery in a ﬁeld named
Line77 context, because it represents the context of the object under test.
Line78 3
Line79 The test uses the mockery to create a mock AuctionEventListener that will
Line80 stand in for a real listener implementation during this test.
Line81 4
Line82 The test instantiates the object under test, an AuctionMessageTranslator,
Line83 passing the mock listener to its constructor. The AuctionMessageTranslator
Line84 does not distinguish between a real and a mock listener: It communicates
Line85 through the AuctionEventListener interface and does not care how that
Line86 interface is implemented.
Line87 5
Line88 The test sets up further objects that will be used in the test.
Line89 6
Line90 The test then tells the mockery how the translator should invoke its neighbors
Line91 during the test by deﬁning a block of expectations. The Java syntax we use
Line92 to do this is obscure, so if you can bear with us for now we explain it in
Line93 more detail in Appendix A.
Line94 7
Line95 This is the signiﬁcant line in the test, its one expectation. It says that, during
Line96 the action, we expect the listener’s auctionClosed() method to be called
Line97 exactly once. Our deﬁnition of success is that the translator will notify its
Line98 Chapter 3
Line99 An Introduction to the Tools
Line100 26
Line101 
Line102 
Line103 ---
Line104 
Line105 ---
Line106 **Page 27**
Line107 
Line108 listener that an auctionClosed() event has happened whenever it receives a
Line109 raw Close message.
Line110 8
Line111 This is the call to the object under test, the outside event that triggers the
Line112 behavior we want to test. It passes a raw Close message to the translator
Line113 which, the test says, should make the translator call auctionClosed() once
Line114 on the listener. The mockery will check that the mock objects are invoked
Line115 as expected while the test runs and fail the test immediately if they are
Line116 invoked unexpectedly.
Line117 9
Line118 Note that the test does not require any assertions. This is quite common in
Line119 mock object tests.
Line120 Expectations
Line121 The example above speciﬁes one very simple expectation. jMock’s expectation
Line122 API is very expressive. It lets you precisely specify:
Line123 •
Line124 The minimum and maximum number of times an invocation is expected;
Line125 •
Line126 Whether an invocation is expected (the test should fail if it is not received)
Line127 or merely allowed to happen (the test should pass if it is not received);
Line128 •
Line129 The parameter values, either given literally or constrained by Hamcrest
Line130 matchers;
Line131 •
Line132 The ordering constraints with respect to other expectations; and,
Line133 •
Line134 What should happen when the method is invoked—a value to return, an
Line135 exception to throw, or any other behavior.
Line136 An expectation block is designed to stand out from the test code that surrounds
Line137 it, making an obvious separation between the code that describes how neighboring
Line138 objects should be invoked and the code that actually invokes objects and tests
Line139 the results. The code within an expectation block acts as a little declarative
Line140 language that describes the expectations; we’ll return to this idea in “Building
Line141 Up to Higher-Level Programming” (page 65).
Line142 There’s more to the jMock API which we don’t have space for in this chapter;
Line143 we’ll describe more of its features in examples in the rest of the book, and there’s
Line144 a summary in Appendix A. What really matters, however, is not the implementa-
Line145 tion we happened to come up with, but its underlying concepts and motivations.
Line146 We will do our best to make them clear.
Line147 27
Line148 jMock2: Mock Objects
Line149 
Line150 
Line151 ---
Line152 
Line153 ---
Line154 **Page 28**
Line155 
Line156 This page intentionally left blank
