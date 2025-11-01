Line1 # A Minimal Introduction to JUnit 4 (pp.21-24)
Line2 
Line3 ---
Line4 **Page 21**
Line5 
Line6 Chapter 3
Line7 An Introduction to the Tools
Line8 Man is a tool-using animal. Without tools he is nothing, with tools he
Line9 is all.
Line10 —Thomas Carlyle
Line11 Stop Me If You’ve Heard This One Before
Line12 This book is about the techniques of using tests to guide the development of
Line13 object-oriented software, not about speciﬁc technologies. To demonstrate the
Line14 techniques in action, however, we’ve had to pick some technologies for our ex-
Line15 ample code. For the rest of the book we’re going to use Java, with the JUnit 4,
Line16 Hamcrest, and jMock2 frameworks. If you’re using something else, we hope
Line17 we’ve been clear enough so that you can apply these ideas in your environment.
Line18 In this chapter we brieﬂy describe the programming interfaces for these three
Line19 frameworks, just enough to help you make sense of the code examples in the rest
Line20 of the book. If you already know how to use them, you can skip this chapter.
Line21 A Minimal Introduction to JUnit 4
Line22 We use JUnit 4 (version 4.6 at the time of writing) as our Java test framework.1
Line23 In essence, JUnit uses reﬂection to walk the structure of a class and run whatever
Line24 it can ﬁnd in that class that represents a test. For example, here’s a test that
Line25 exercises a Catalog class which manages a collection of Entry objects:
Line26 public class CatalogTest {
Line27   private final Catalog catalog = new Catalog();
Line28   @Test public void containsAnAddedEntry() { 
Line29     Entry entry = new Entry("fish", "chips");
Line30     catalog.add(entry);
Line31     assertTrue(catalog.contains(entry));
Line32   }
Line33   @Test public void indexesEntriesByName() {
Line34     Entry entry = new Entry("fish", "chips");
Line35     catalog.add(entry);
Line36     assertEquals(entry, catalog.entryFor("fish"));  
Line37     assertNull(catalog.entryFor("missing name"));  
Line38   }
Line39 }
Line40 1. JUnit is bundled with many Java IDEs and is available at www.junit.org.
Line41 21
Line42 
Line43 
Line44 ---
Line45 
Line46 ---
Line47 **Page 22**
Line48 
Line49 Test Cases
Line50 JUnit treats any method annotated with @Test as a test case; test methods must
Line51 have neither a return value nor parameters. In this case, CatalogTest deﬁnes two
Line52 tests, called containsAnAddedEntry() and indexesEntriesByName().
Line53 To run a test, JUnit creates a new instance of the test class and calls the relevant
Line54 test method. Creating a new test object each time ensures that the tests are isolated
Line55 from each other, because the test object’s ﬁelds are replaced before each test.
Line56 This means that a test is free to change the contents of any of the test object ﬁelds.
Line57 NUnit Behaves Differently from JUnit
Line58 Those working in .Net should note that NUnit reuses the same instance of the test
Line59 object for all the test methods, so any values that might change must either be
Line60 reset in [Setup] and [TearDown] methods (if they’re ﬁelds) or made local to the
Line61 test method.
Line62 Assertions
Line63 A JUnit test invokes the object under test and then makes assertions about the
Line64 results, usually using assertion methods deﬁned by JUnit which generate useful
Line65 error messages when they fail.
Line66 CatalogTest, for example, uses three of JUnit’s assertions: assertTrue()
Line67 asserts that an expression is true; assertNull() asserts that an object reference
Line68 is null; and assertEquals() asserts that two values are equal. When it fails,
Line69 assertEquals() reports the expected and actual values that were compared.
Line70 Expecting Exceptions
Line71 The @Test annotation supports an optional parameter expected that declares
Line72 that the test case should throw an exception. The test fails if it does not throw
Line73 an exception or if it throws an exception of a different type.
Line74 For example, the following test checks that a Catalog throws an
Line75 IllegalArgumentException when two entries are added with the same name:
Line76 @Test(expected=IllegalArgumentException.class)
Line77 public void cannotAddTwoEntriesWithTheSameName() {
Line78   catalog.add(new Entry("fish", "chips");
Line79   catalog.add(new Entry("fish", "peas");
Line80 }
Line81 Chapter 3
Line82 An Introduction to the Tools
Line83 22
Line84 
Line85 
Line86 ---
Line87 
Line88 ---
Line89 **Page 23**
Line90 
Line91 Test Fixtures
Line92 A test ﬁxture is the ﬁxed state that exists at the start of a test. A test ﬁxture ensures
Line93 that a test is repeatable—every time a test is run it starts in the same state so it
Line94 should produce the same results. A ﬁxture may be set up before the test runs and
Line95 torn down after it has ﬁnished.
Line96 The ﬁxture for a JUnit test is managed by the class that deﬁnes the test and is
Line97 stored in the object’s ﬁelds. All tests deﬁned in the same class start with an iden-
Line98 tical ﬁxture and may modify that ﬁxture as they run. For CatalogTest, the ﬁxture
Line99 is the empty Catalog object held in its catalog ﬁeld.
Line100 The ﬁxture is usually set up by ﬁeld initializers. It can also be set up by the
Line101 constructor of the test class or instance initializer blocks. JUnit also lets you
Line102 identify methods that set up and tear down the ﬁxture with annotations. JUnit
Line103 will run all methods annotated with @Before before running the tests, to set up
Line104 the ﬁxture, and those annotated by @After after it has run the test, to tear
Line105 down the ﬁxture. Many JUnit tests do not need to explicitly tear down the ﬁxture
Line106 because it is enough to let the JVM garbage collect any objects created when it
Line107 was set up.
Line108 For example, all the tests in CatalogTest initialize the catalog with the same
Line109 entry. This common initialization can be moved into a ﬁeld initializer and @Before
Line110 method:
Line111 public class CatalogTest {
Line112   final Catalog catalog = new Catalog();
Line113 final Entry entry = new Entry("fish", "chips");
Line114 @Before public void fillTheCatalog() {
Line115     catalog.add(entry);
Line116   }
Line117   @Test public void containsAnAddedEntry() {
Line118     assertTrue(catalog.contains(entry));
Line119   }
Line120   @Test public void indexesEntriesByName() {
Line121     assertEquals(equalTo(entry), catalog.entryFor("fish"));  
Line122     assertNull(catalog.entryFor("missing name"));  
Line123   }
Line124   @Test(expected=IllegalArgumentException.class)
Line125   public void cannotAddTwoEntriesWithTheSameName() {
Line126     catalog.add(new Entry("fish", "peas");
Line127   }
Line128 }
Line129 Test Runners
Line130 The way JUnit reﬂects on a class to ﬁnd tests and then runs those tests is controlled
Line131 by a test runner. The runner used for a class can be conﬁgured with the @RunWith
Line132 23
Line133 A Minimal Introduction to JUnit 4
Line134 
Line135 
Line136 ---
Line137 
Line138 ---
Line139 **Page 24**
Line140 
Line141 annotation.2 JUnit provides a small library of test runners. For example, the
Line142 Parameterized test runner lets you write data-driven tests in which the same test
Line143 methods are run for many different data values returned from a static method.
Line144 As we’ll see below, the jMock library uses a custom test runner to automatically
Line145 verify mock objects at the end of the test, before the test ﬁxture is torn down.
Line146 Hamcrest Matchers and assertThat()
Line147 Hamcrest is a framework for writing declarative match criteria. While not a
Line148 testing framework itself, Hamcrest is used by several testing frameworks, including
Line149 JUnit, jMock, and WindowLicker, which we use in the example in Part III.
Line150 A Hamcrest matcher reports whether a given object matches some criteria, can
Line151 describe its criteria, and can describe why an object does not meet its criteria.
Line152 For example, this code creates matchers for strings that contain a given substring
Line153 and uses them to make some assertions:
Line154 String s = "yes we have no bananas today";
Line155 Matcher<String> containsBananas = new StringContains("bananas");
Line156 Matcher<String> containsMangoes = new StringContains("mangoes");
Line157 assertTrue(containsBananas.matches(s));
Line158 assertFalse(containsMangoes.matches(s));
Line159 Matchers are not usually instantiated directly. Instead, Hamcrest provides
Line160 static factory methods for all of its matchers to make the code that creates
Line161 matchers more readable. For example:
Line162 assertTrue(containsString("bananas").matches(s));
Line163 assertFalse(containsString("mangoes").matches(s));
Line164 In practice, however, we use matchers in combination with JUnit’s
Line165 assertThat(), which uses matcher’s self-describing features to make clear exactly
Line166 what went wrong when an assertion fails.3 We can rewrite the assertions as:
Line167 assertThat(s, containsString("bananas"));
Line168 assertThat(s, not(containsString("mangoes"));
Line169 The second assertion demonstrates one of Hamcrest’s most useful features:
Line170 deﬁning new criteria by combining existing matchers. The not() method is a
Line171 factory function that creates a matcher that reverses the sense of any matcher
Line172 passed to it. Matchers are designed so that when they’re combined, both the code
Line173 and the failure messages are self-explanatory. For example, if we change the
Line174 second assertion to fail:
Line175 2. By the time of publication, JUnit will also have a Rule annotation for ﬁelds to support
Line176 objects that can “intercept” the lifecycle of a test run.
Line177 3. The assertThat() method was introduced in JUnit 4.5.
Line178 Chapter 3
Line179 An Introduction to the Tools
Line180 24
Line181 
Line182 
Line183 ---
