Line1 # Assertions and Expectations (pp.254-255)
Line2 
Line3 ---
Line4 **Page 254**
Line5 
Line6 @Test public void expandsMacrosSurroundedWithBraces() {
Line7   StringTemplate template = new StringTemplate("{a}{b}");
Line8   try {
Line9     String expanded = template.expand(macros);
Line10     assertThat(expanded, equalTo("AB"));
Line11   } catch (TemplateFormatException e) {
Line12     fail("Template failed: " + e);
Line13   }
Line14 }
Line15 If this test is intended to pass, then converting the exception actually drops infor-
Line16 mation from the stack trace. The simplest thing to do is to let the exception
Line17 propagate for the test runtime to catch. We can add arbitrary exceptions to the
Line18 test method signature because it’s only called by reﬂection. This removes at least
Line19 half the lines of the test, and we can compact it further to be:
Line20 @Test public void expandsMacrosSurroundedWithBraces() throws Exception {
Line21   assertThat(new StringTemplate("{a}{b}").expand(macros),
Line22              equalTo("AB"));
Line23 }
Line24 which tells us just what is supposed to happen and ignores everything else.
Line25 Delegate to Subordinate Objects
Line26 Sometimes helper methods aren’t enough and we need helper objects to support
Line27 the tests. We saw this in the test rig we built in Chapter 11. We developed the
Line28 ApplicationRunner, AuctionSniperDriver, and FakeAuctionServer classes so we
Line29 could write tests in terms of auctions and Snipers, not in terms of Swing and
Line30 messaging.
Line31 A more common technique is to write test data builders to build up complex
Line32 data structures with just the appropriate values for a test; see Chapter 22 for
Line33 more detail. Again, the point is to include in the test just the values that are rele-
Line34 vant, so that the reader can understand the intent; everything else can be defaulted.
Line35 There are two approaches to writing subordinate objects. In Chapter 11 we
Line36 started by writing the test we wanted to see and then ﬁlling in the supporting
Line37 objects: start from a statement of the problem and see where it goes. The alterna-
Line38 tive is to write the code directly in the tests, and then refactor out any clusters
Line39 of behavior. This is the origin of the WindowLicker framework, which started
Line40 out as helper code in JUnit tests for interacting with the Swing event dispatcher
Line41 and eventually grew into a separate project.
Line42 Assertions and Expectations
Line43 The assertions and expectations of a test should communicate precisely what
Line44 matters in the behavior of the target code. We regularly see code where tests assert
Line45 Chapter 21
Line46 Test Readability
Line47 254
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 255**
Line54 
Line55 too much detail, which makes them difﬁcult to read and brittle when things
Line56 change; we discuss what this might mean in “Too Many Expectations” (page 242).
Line57 For the expectations and assertions we write, we try to keep them as narrowly
Line58 deﬁned as possible. For example, in the “instrument with price” assertion above,
Line59 we check only the strike price and ignore the rest of the values as irrelevant in
Line60 that test. In other cases, we’re not interested in all of the arguments to a method,
Line61 so we ignore them in the expectation. In Chapter 19, we deﬁne an expectation
Line62 that says that we care about the Sniper identiﬁer and message, but that any
Line63 RuntimeException object will do for the third argument:
Line64 oneOf(failureReporter).cannotTranslateMessage(
Line65                          with(SNIPER_ID), with(badMessage),
Line66                          with(any(RuntimeException.class)));
Line67 If you learned about pre- and postconditions in college, this is when that training
Line68 will come in useful.
Line69 Finally, a word of caution on assertFalse(). The combination of the failure
Line70 message and negation makes it easy to read this as meaning that the two dates
Line71 should not be different:
Line72 assertFalse("end date", first.endDate().equals(second.endDate()));
Line73 We could use assertTrue() and add a “!” to the result but, again, the single
Line74 character is easy to miss. That’s why we prefer to use matchers to make the code
Line75 more explicit:
Line76 assertThat("end date", first.endDate(), not(equalTo(second.endDate())));
Line77 which also has the advantage of showing the actual date received in the failure
Line78 report:
Line79 java.lang.AssertionError: end date
Line80 Expected: not <Thu Jan 01 02:34:38 GMT 1970>
Line81      but: was <Thu Jan 01 02:34:38 GMT 1970>
Line82 Literals and Variables
Line83 One last point. As we wrote in the introduction to this chapter, test code tends
Line84 to be more concrete than production code, which means it has more literal values.
Line85 Literal values without explanation can be difﬁcult to understand because the
Line86 programmer has to interpret whether a particular value is signiﬁcant (e.g. just
Line87 outside the allowed range) or just an arbitrary placeholder to trace behavior (e.g.
Line88 should be doubled and passed on to a peer). A literal value does not describe its
Line89 role, although there are some techniques for doing so that we will show in
Line90 Chapter 23
Line91 One solution is to allocate literal values to variables and constants with names
Line92 that describe their function. For example, in Chapter 12 we declared
Line93 255
Line94 Literals and Variables
Line95 
Line96 
Line97 ---
