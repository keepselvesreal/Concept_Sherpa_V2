Line1 # Highlight Detail with Matchers (pp.268-269)
Line2 
Line3 ---
Line4 **Page 268**
Line5 
Line6 Small, Focused, Well-Named Tests
Line7 The easiest way to improve diagnostics is to keep each test small and focused
Line8 and give tests readable names, as described in Chapter 21. If a test is small, its
Line9 name should tell us most of what we need to know about what has gone wrong.
Line10 Explanatory Assertion Messages
Line11 JUnit’s assertion methods all have a version in which the ﬁrst parameter is a
Line12 message to display when the assertion fails. From what we’ve seen, this feature
Line13 is not used as often as it should be to make assertion failures more helpful.
Line14 For example, when this test fails:
Line15 Customer customer  = order.getCustomer();
Line16 assertEquals("573242", customer.getAccountId());
Line17 assertEquals(16301, customer.getOutstandingBalance());
Line18 the report does not make it obvious which of the assertions has failed:
Line19 ComparisonFailure: expected:<[16301]> but was:<[16103]>
Line20 The message is describing the symptom (the balance is 16103) rather than the
Line21 cause (the outstanding balance calculation is wrong).
Line22 If we add a message to identify the value being asserted:
Line23 assertEquals("account id", "573242", customer.getAccountId());
Line24 assertEquals("outstanding balance", 16301, customer.getOustandingBalance());
Line25 we can immediately see what the point is:
Line26 ComparisonFailure: outstanding balance expected:<[16301]> but was:<[16103]>
Line27 Highlight Detail with Matchers
Line28 Developers can provide another level of diagnostic detail by using assertThat()
Line29 with Hamcrest matchers. The Matcher API includes support for describing the
Line30 value that mismatched, to help with understanding exactly what is different. For
Line31 example, the instrument strike price assertion on page 252 generates this failure
Line32 report:
Line33 Expected: a collection containing instrument at price a value greater than <81>
Line34      but: price was <50>, price was <72>, price was <31>
Line35 which shows exactly which values are relevant.
Line36 Chapter 23
Line37 Test Diagnostics
Line38 268
Line39 
Line40 
Line41 ---
Line42 
Line43 ---
Line44 **Page 269**
Line45 
Line46 Self-Describing Value
Line47 An alternative to adding detail to the assertion is to build the detail into values
Line48 in the assertion. We can take this in the same spirit as the idea that comments
Line49 are a hint that the code needs to be improved: if we have to add detail to an
Line50 assertion, maybe that’s a hint that we could make the failure more obvious.
Line51 In the customer example above, we could improve the failure message by setting
Line52 the account identiﬁer in the test Customer to the self-describing value "a customer
Line53 account id":
Line54 ComparisonFailure: expected:<[a customer account id]> but was:<[id not set]>
Line55 Now we don’t need to add an explanatory message, because the value itself
Line56 explains its role.
Line57 We might be able to do more when we’re working with reference types. For
Line58 example, in a test that has this setup:
Line59 Date startDate = new Date(1000);
Line60 Date endDate = new Date(2000);
Line61 the failure message reports that a payment date is wrong but doesn’t describe
Line62 where the wrong value might have come from:
Line63 java.lang.AssertionError: payment date
Line64 Expected: <Thu Jan 01 01:00:01 GMT 1970>
Line65      got: <Thu Jan 01 01:00:02 GMT 1970>
Line66 What we really want to know is the meaning of these dates. If we force the
Line67 display string:
Line68 Date startDate = namedDate(1000, "startDate");
Line69 Date endDate = namedDate(2000, "endDate");
Line70 Date namedDate(long timeValue, final String name) {
Line71     return new Date(timeValue) { public String toString() { return name; } };
Line72 }
Line73 we get a message that describes the role that each date plays:
Line74 java.lang.AssertionError: payment date
Line75 Expected: <startDate>
Line76      got: <endDate>
Line77 which makes it clear that we’ve assigned the wrong ﬁeld to the payment date.1
Line78 1. This is yet another motivation for deﬁning more domain types to hide the basic types
Line79 in the language. As we discussed in “Domain Types Are Better Than Strings”
Line80 (page 213), it gives us somewhere to hang useful behavior like this.
Line81 269
Line82 Self-Describing Value
Line83 
Line84 
Line85 ---
