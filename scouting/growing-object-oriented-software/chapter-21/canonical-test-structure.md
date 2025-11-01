Line1 # Canonical Test Structure (pp.251-252)
Line2 
Line3 ---
Line4 **Page 251**
Line5 
Line6 Canonical Test Structure
Line7 We ﬁnd that if we write our tests in a standard form, they’re easier to
Line8 understand. We can skim-read to ﬁnd expectations and assertions quickly and
Line9 see how they relate to the code under test. If we’re ﬁnding it difﬁcult to write a
Line10 test in a standard form, that’s often a hint that the code is too complicated or
Line11 that we haven’t quite clariﬁed our ideas.
Line12 The most common form for a test is:
Line13 1.
Line14 Setup: prepare the context of the test, the environment in which the target
Line15 code will run;
Line16 2.
Line17 Execute: call the target code, triggering the tested behavior;
Line18 3.
Line19 Verify: check for a visible effect that we expect from the behavior; and,
Line20 4.
Line21 Teardown: clean up any leftover state that might corrupt other tests.
Line22 There are other versions of this form, such as “Arrange, Act, Assert,” which
Line23 collapse some of the stages.
Line24 For example:
Line25 public class StringTemplateTest {
Line26   @Test public void expandsMacrosSurroundedWithBraces() {
Line27     StringTemplate template = new StringTemplate("{a}{b}"); // Setup
Line28     HashMap<String,Object> macros = new HashMap<String,Object>();
Line29     macros.put("a", "A");
Line30     macros.put("b", "B");
Line31     String expanded = template.expand(macros);              // Execute
Line32     assertThat(expanded, equalTo("AB"));                    // Assert
Line33   }                                                         // No Teardown
Line34 }
Line35 Tests that set expectations on mock objects use a variant of this structure where
Line36 some of the assertions are declared before the execute stage and are implicitly
Line37 checked afterwards—for example, in LoggingXMPPFailureReporterTest from
Line38 Chapter 19:
Line39 @RunWith(JMock.class)
Line40 public class LoggingXMPPFailureReporterTest {
Line41   private final Mockery context = new Mockery() {{  // Setup
Line42    setImposteriser(ClassImposteriser.INSTANCE); 
Line43   }};
Line44   final Logger logger = context.mock(Logger.class);
Line45   final LoggingXMPPFailureReporter reporter = new LoggingXMPPFailureReporter(logger);
Line46 251
Line47 Canonical Test Structure
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 252**
Line54 
Line55 @Test public void writesMessageTranslationFailureToLog() {
Line56     Exception exception = new Exception("an exception");
Line57     context.checking(new Expectations() {{          // Expect
Line58       oneOf(logger).severe( expected log message here);
Line59     }});
Line60     reporter.cannotTranslateMessage("auction id",   // Execute
Line61                                     "failed message", exception); 
Line62 // implicitly check expectations are satisfied
Line63 // Assert
Line64   }
Line65   @AfterClass public static void resetLogging() {   // Teardown
Line66     LogManager.getLogManager().reset();
Line67   }  
Line68 }
Line69 Write Tests Backwards
Line70 Although we stick to a canonical format for test code, we don’t necessarily write
Line71 tests from top to bottom. What we often do is: write the test name, which helps us
Line72 decide what we want to achieve; write the call to the target code, which is the entry
Line73 point for the feature; write the expectations and assertions, so we know what effects
Line74 the feature should have; and, write the setup and teardown to deﬁne the context
Line75 for the test. Of course, there may be some blurring of these steps to help the
Line76 compiler, but this sequence reﬂects how we tend to think through a new unit test.
Line77 Then we run it and watch it fail.
Line78 How Many Assertions in a Test Method?
Line79 Some TDD practitioners suggest that each test should only contain one expectation
Line80 or assertion.This is useful as a training rule when learning TDD, to avoid asserting
Line81 everything the developer can think of, but we don’t ﬁnd it practical. A better rule
Line82 is to think of one coherent feature per test, which might be represented by up to
Line83 a handful of assertions. If a single test seems to be making assertions about
Line84 different features of a target object, it might be worth splitting up. Once again,
Line85 expressiveness is the key: as a reader of this test, can I ﬁgure out what’s
Line86 signiﬁcant?
Line87 Streamline the Test Code
Line88 All code should emphasize “what” it does over “how,” including test code; the
Line89 more implementation detail is included in a test method, the harder it is for
Line90 the reader to understand what’s important. We try to move everything out
Line91 of the test method that doesn’t contribute to the description, in domain
Line92 terms, of the feature being exercised. Sometimes that involves restructuring the
Line93 code, sometimes just ignoring the syntax noise.
Line94 Chapter 21
Line95 Test Readability
Line96 252
Line97 
Line98 
Line99 ---
