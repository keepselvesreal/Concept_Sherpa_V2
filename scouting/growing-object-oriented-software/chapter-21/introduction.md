Line1 # Introduction (pp.247-248)
Line2 
Line3 ---
Line4 **Page 247**
Line5 
Line6 Chapter 21
Line7 Test Readability
Line8 To design is to communicate clearly by whatever means you can control
Line9 or master.
Line10 —Milton Glaser
Line11 Introduction
Line12 Teams that adopt TDD usually see an early boost in productivity because the
Line13 tests let them add features with conﬁdence and catch errors immediately. For
Line14 some teams, the pace then slows down as the tests themselves become a mainte-
Line15 nance burden. For TDD to be sustainable, the tests must do more than verify the
Line16 behavior of the code; they must also express that behavior clearly—they must
Line17 be readable. This matters for the same reason that code readability matters: every
Line18 time the developers have to stop and puzzle through a test to ﬁgure out what it
Line19 means, they have less time left to spend on creating new features, and the team
Line20 velocity drops.
Line21 We take as much care about writing our test code as about production code,
Line22 but with differences in style since the two types of code serve different purposes.
Line23 Test code should describe what the production code does. That means that it
Line24 tends to be concrete about the values it uses as examples of what results to expect,
Line25 but abstract about how the code works. Production code, on the other hand,
Line26 tends to be abstract about the values it operates on but concrete about how it
Line27 gets the job done. Similarly, when writing production code, we have to consider
Line28 how we will compose our objects to make up a working system, and manage
Line29 their dependencies carefully. Test code, on the other hand, is at the end of the
Line30 dependency chain, so it’s more important for it to express the intention of its
Line31 target code than to plug into a web of other objects. We want our test code to
Line32 read like a declarative description of what is being tested.
Line33 In this chapter, we’ll describe some practices that we’ve found helpful to keep
Line34 our tests readable and expressive.
Line35 247
Line36 
Line37 
Line38 ---
Line39 
Line40 ---
Line41 **Page 248**
Line42 
Line43 Could Do Better1
Line44 We’ve seen many unit test suites that could be much more effective given a
Line45 little extra attention. They have too many “test smells” of the kind cataloged in
Line46 [Meszaros07], as well as in our own Chapters 20 and 24.When cleaning up tests,
Line47 or just trying to write new ones, the readability problems we watch out for are:
Line48 •
Line49 Test names that do not clearly describe the point of each test case and its
Line50 differences from the other test cases;
Line51 •
Line52 Single test cases that seem to be exercising multiple features;
Line53 •
Line54 Tests with different structure, so the reader cannot skim-read them to
Line55 understand their intention;
Line56 •
Line57 Tests with lots of code for setting up and handling exceptions, which buries
Line58 their essential logic; and,
Line59 •
Line60 Tests that use literal values (“magic numbers”) but are not clear about what,
Line61 if anything, is signiﬁcant about those values.
Line62 Test Names Describe Features
Line63 The name of the test should be the ﬁrst clue for a developer to understand what
Line64 is being tested and how the target object is supposed to behave.
Line65 Not every team we’ve worked with follows this principle. Some naive developers
Line66 use names that don’t mean anything at all:
Line67 public class TargetObjectTest {
Line68   @Test public void test1() { […]
Line69   @Test public void test2() { […]
Line70   @Test public void test3() { […]
Line71 We don’t see many of these nowadays; the world has moved on. A common
Line72 approach is to name a test after the method it’s exercising:
Line73 public class TargetObjectTest {
Line74   @Test public void isReady() { […]
Line75   @Test public void choose() { […]
Line76   @Test public void choose1() { […]
Line77 public class TargetObject  {
Line78   public void isReady() { […]
Line79   public void choose(Picker picker) { […]
Line80 perhaps with multiple tests for different paths through the same method.
Line81 1. This is (or was) a common phrase in UK school reports for children whose schoolwork
Line82 isn’t as good as it could be.
Line83 Chapter 21
Line84 Test Readability
Line85 248
Line86 
Line87 
Line88 ---
