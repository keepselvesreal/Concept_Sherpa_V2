Line1 # Test Names Describe Features (pp.248-251)
Line2 
Line3 ---
Line4 **Page 248**
Line5 
Line6 Could Do Better1
Line7 We’ve seen many unit test suites that could be much more effective given a
Line8 little extra attention. They have too many “test smells” of the kind cataloged in
Line9 [Meszaros07], as well as in our own Chapters 20 and 24.When cleaning up tests,
Line10 or just trying to write new ones, the readability problems we watch out for are:
Line11 •
Line12 Test names that do not clearly describe the point of each test case and its
Line13 differences from the other test cases;
Line14 •
Line15 Single test cases that seem to be exercising multiple features;
Line16 •
Line17 Tests with different structure, so the reader cannot skim-read them to
Line18 understand their intention;
Line19 •
Line20 Tests with lots of code for setting up and handling exceptions, which buries
Line21 their essential logic; and,
Line22 •
Line23 Tests that use literal values (“magic numbers”) but are not clear about what,
Line24 if anything, is signiﬁcant about those values.
Line25 Test Names Describe Features
Line26 The name of the test should be the ﬁrst clue for a developer to understand what
Line27 is being tested and how the target object is supposed to behave.
Line28 Not every team we’ve worked with follows this principle. Some naive developers
Line29 use names that don’t mean anything at all:
Line30 public class TargetObjectTest {
Line31   @Test public void test1() { […]
Line32   @Test public void test2() { […]
Line33   @Test public void test3() { […]
Line34 We don’t see many of these nowadays; the world has moved on. A common
Line35 approach is to name a test after the method it’s exercising:
Line36 public class TargetObjectTest {
Line37   @Test public void isReady() { […]
Line38   @Test public void choose() { […]
Line39   @Test public void choose1() { […]
Line40 public class TargetObject  {
Line41   public void isReady() { […]
Line42   public void choose(Picker picker) { […]
Line43 perhaps with multiple tests for different paths through the same method.
Line44 1. This is (or was) a common phrase in UK school reports for children whose schoolwork
Line45 isn’t as good as it could be.
Line46 Chapter 21
Line47 Test Readability
Line48 248
Line49 
Line50 
Line51 ---
Line52 
Line53 ---
Line54 **Page 249**
Line55 
Line56 At best, such names duplicate the information a developer could get just by
Line57 looking at the target class; they break the “Don’t Repeat Yourself” principle
Line58 [Hunt99]. We don’t need to know that TargetObject has a choose() method—we
Line59 need to know what the object does in different situations, what the method is for.
Line60 A better alternative is to name tests in terms of the features that the target
Line61 object provides. We use a TestDox convention (invented by Chris Stevenson)
Line62 where each test name reads like a sentence, with the target class as the implicit
Line63 subject. For example,
Line64 •
Line65 A List holds items in the order they were added.
Line66 •
Line67 A List can hold multiple references to the same item.
Line68 •
Line69 A List throws an exception when removing an item it doesn’t hold.
Line70 We can translate these directly to method names:
Line71 public class ListTests {
Line72   @Test public void holdsItemsInTheOrderTheyWereAdded() { […]
Line73   @Test public void canHoldMultipleReferencesToTheSameItem() { […]
Line74   @Test public void throwsAnExceptionWhenRemovingAnItemItDoesntHold() { […]
Line75 These names can be as long as we like because they’re only called through
Line76 reﬂection—we never have to type them in to call them.
Line77 The point of the convention is to encourage the developer to think in terms of
Line78 what the target object does, not what it is. It’s also very compatible with our in-
Line79 cremental approach of adding a feature at a time to an existing codebase. It gives
Line80 us a consistent style of naming all the way from user stories, through tasks and
Line81 acceptance tests, to unit tests—as you saw in Part III.
Line82 As a matter of style, the test name should say something about the expected
Line83 result, the action on the object, and the motivation for the scenario. For example,
Line84 if we were testing a ConnectionMonitor class, then
Line85 pollsTheServersMonitoringPort()
Line86 doesn’t tell us enough: why does it poll, what happens when it gets a result? On
Line87 the other hand,
Line88 notifiesListenersThatServerIsUnavailableWhenCannotConnectToItsMonitoringPort()
Line89 explains both the scenario and the expected behavior. We’ll show later how this
Line90 style of naming maps onto our standard test structures.
Line91 249
Line92 Test Names Describe Features
Line93 
Line94 
Line95 ---
Line96 
Line97 ---
Line98 **Page 250**
Line99 
Line100 Test Name First or Last?
Line101 We’ve noticed that some developers start with a placeholder name, ﬁll out the body
Line102 of the test, and then decide what to call it. Others (such as Steve) like to decide
Line103 the test name ﬁrst, to clarify their intentions, before writing any test code. Both ap-
Line104 proaches work as long as the developer follows through and makes sure that the
Line105 test is, in the end, consistent and expressive.
Line106 The TestDox format fulﬁlls the early promise of TDD—that the tests should
Line107 act as documentation for the code. There are tools and IDE plug-ins that unpack
Line108 the “camel case” method names and link them to the class under test, such
Line109 as the TestDox plug-in for the IntelliJ IDE; Figure 21.1 shows the automatic
Line110 documentation for a KeyboardLayout class.
Line111 Figure 21.1
Line112 The TestDox IntelliJ plug-in
Line113 Regularly Read Documentation Generated from Tests
Line114 We ﬁnd that such generated documentation gives us a fresh perspective on the
Line115 test names, highlighting the problems we’re too close to the code to see. For
Line116 example, when generating the screenshot for Figure 21.1, Nat noticed that the
Line117 name of the ﬁrst test is unclear—it should be “translates numbers to key strokes
Line118 in all known layouts.”
Line119 We make an effort to at least skim-read the documentation regularly during
Line120 development.
Line121 Chapter 21
Line122 Test Readability
Line123 250
Line124 
Line125 
Line126 ---
Line127 
Line128 ---
Line129 **Page 251**
Line130 
Line131 Canonical Test Structure
Line132 We ﬁnd that if we write our tests in a standard form, they’re easier to
Line133 understand. We can skim-read to ﬁnd expectations and assertions quickly and
Line134 see how they relate to the code under test. If we’re ﬁnding it difﬁcult to write a
Line135 test in a standard form, that’s often a hint that the code is too complicated or
Line136 that we haven’t quite clariﬁed our ideas.
Line137 The most common form for a test is:
Line138 1.
Line139 Setup: prepare the context of the test, the environment in which the target
Line140 code will run;
Line141 2.
Line142 Execute: call the target code, triggering the tested behavior;
Line143 3.
Line144 Verify: check for a visible effect that we expect from the behavior; and,
Line145 4.
Line146 Teardown: clean up any leftover state that might corrupt other tests.
Line147 There are other versions of this form, such as “Arrange, Act, Assert,” which
Line148 collapse some of the stages.
Line149 For example:
Line150 public class StringTemplateTest {
Line151   @Test public void expandsMacrosSurroundedWithBraces() {
Line152     StringTemplate template = new StringTemplate("{a}{b}"); // Setup
Line153     HashMap<String,Object> macros = new HashMap<String,Object>();
Line154     macros.put("a", "A");
Line155     macros.put("b", "B");
Line156     String expanded = template.expand(macros);              // Execute
Line157     assertThat(expanded, equalTo("AB"));                    // Assert
Line158   }                                                         // No Teardown
Line159 }
Line160 Tests that set expectations on mock objects use a variant of this structure where
Line161 some of the assertions are declared before the execute stage and are implicitly
Line162 checked afterwards—for example, in LoggingXMPPFailureReporterTest from
Line163 Chapter 19:
Line164 @RunWith(JMock.class)
Line165 public class LoggingXMPPFailureReporterTest {
Line166   private final Mockery context = new Mockery() {{  // Setup
Line167    setImposteriser(ClassImposteriser.INSTANCE); 
Line168   }};
Line169   final Logger logger = context.mock(Logger.class);
Line170   final LoggingXMPPFailureReporter reporter = new LoggingXMPPFailureReporter(logger);
Line171 251
Line172 Canonical Test Structure
Line173 
Line174 
Line175 ---
