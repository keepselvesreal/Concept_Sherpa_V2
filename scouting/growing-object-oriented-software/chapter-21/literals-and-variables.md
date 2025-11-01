Line1 # Literals and Variables (pp.255-256)
Line2 
Line3 ---
Line4 **Page 255**
Line5 
Line6 too much detail, which makes them difﬁcult to read and brittle when things
Line7 change; we discuss what this might mean in “Too Many Expectations” (page 242).
Line8 For the expectations and assertions we write, we try to keep them as narrowly
Line9 deﬁned as possible. For example, in the “instrument with price” assertion above,
Line10 we check only the strike price and ignore the rest of the values as irrelevant in
Line11 that test. In other cases, we’re not interested in all of the arguments to a method,
Line12 so we ignore them in the expectation. In Chapter 19, we deﬁne an expectation
Line13 that says that we care about the Sniper identiﬁer and message, but that any
Line14 RuntimeException object will do for the third argument:
Line15 oneOf(failureReporter).cannotTranslateMessage(
Line16                          with(SNIPER_ID), with(badMessage),
Line17                          with(any(RuntimeException.class)));
Line18 If you learned about pre- and postconditions in college, this is when that training
Line19 will come in useful.
Line20 Finally, a word of caution on assertFalse(). The combination of the failure
Line21 message and negation makes it easy to read this as meaning that the two dates
Line22 should not be different:
Line23 assertFalse("end date", first.endDate().equals(second.endDate()));
Line24 We could use assertTrue() and add a “!” to the result but, again, the single
Line25 character is easy to miss. That’s why we prefer to use matchers to make the code
Line26 more explicit:
Line27 assertThat("end date", first.endDate(), not(equalTo(second.endDate())));
Line28 which also has the advantage of showing the actual date received in the failure
Line29 report:
Line30 java.lang.AssertionError: end date
Line31 Expected: not <Thu Jan 01 02:34:38 GMT 1970>
Line32      but: was <Thu Jan 01 02:34:38 GMT 1970>
Line33 Literals and Variables
Line34 One last point. As we wrote in the introduction to this chapter, test code tends
Line35 to be more concrete than production code, which means it has more literal values.
Line36 Literal values without explanation can be difﬁcult to understand because the
Line37 programmer has to interpret whether a particular value is signiﬁcant (e.g. just
Line38 outside the allowed range) or just an arbitrary placeholder to trace behavior (e.g.
Line39 should be doubled and passed on to a peer). A literal value does not describe its
Line40 role, although there are some techniques for doing so that we will show in
Line41 Chapter 23
Line42 One solution is to allocate literal values to variables and constants with names
Line43 that describe their function. For example, in Chapter 12 we declared
Line44 255
Line45 Literals and Variables
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 256**
Line52 
Line53 public static final Chat UNUSED_CHAT = null;
Line54 to show that we were using null to represent an argument that was unused in
Line55 the target code. We weren’t expecting the code to receive null in production,
Line56 but it turns out that we don’t care and it makes testing easier. Similarly, a team
Line57 might develop conventions for naming common values, such as:
Line58 public final static INVALID_ID = 666;
Line59 We name variables to show the roles these values or objects play in the test and
Line60 their relationships to the target object.
Line61 Chapter 21
Line62 Test Readability
Line63 256
