Line1 # Explanatory Assertion Messages (pp.268-268)
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
