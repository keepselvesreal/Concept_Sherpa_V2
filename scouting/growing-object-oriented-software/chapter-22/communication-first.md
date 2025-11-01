Line1 # Communication First (pp.264-266)
Line2 
Line3 ---
Line4 **Page 264**
Line5 
Line6 Then, Raise the Game
Line7 The test code is looking better, but it still reads like a script. We can change its
Line8 emphasis to what behavior is expected, rather than how the test is implemented,
Line9 by rewording some of the names:
Line10 @Test public void reportsTotalSalesOfOrderedProducts() {
Line11 havingReceived(anOrder()
Line12       .withLine("Deerstalker Hat", 1)
Line13       .withLine("Tweed Cape", 1));
Line14 havingReceived(anOrder()
Line15       .withLine("Deerstalker Hat", 1));
Line16   TotalSalesReport report = gui.openSalesReport();
Line17   report.displaysTotalSalesFor("Deerstalker Hat", equalTo(2));
Line18   report.displaysTotalSalesFor("Tweed Cape", equalTo(1));
Line19 }
Line20 @Test public void takesAmendmentsIntoAccountWhenCalculatingTotalSales() {
Line21   Customer theCustomer = aCustomer().build();
Line22 havingReceived(anOrder().from(theCustomer)
Line23     .withLine("Deerstalker Hat", 1)
Line24     .withLine("Tweed Cape", 1));
Line25 havingReceived(anOrderAmendment().from(theCustomer)
Line26     .withLine("Deerstalker Hat", 2));
Line27   TotalSalesReport report = user.openSalesReport();
Line28   report.containsTotalSalesFor("Deerstalker Hat", equalTo(2));
Line29   report.containsTotalSalesFor("Tweed Cape", equalTo(1));
Line30 }
Line31 We started with a test that looked procedural, extracted some of its behavior
Line32 into builder objects, and ended up with a declarative description of what the
Line33 feature does. We’re nudging the test code towards the sort of language we could
Line34 use when discussing the feature with someone else, even someone non-technical;
Line35 we push everything else into supporting code.
Line36 Communication First
Line37 We use test data builders to reduce duplication and make the test code more ex-
Line38 pressive. It’s another technique that reﬂects our obsession with the language of
Line39 code, driven by the principle that code is there to be read. Combined with factory
Line40 methods and test scaffolding, test data builders help us write more literate,
Line41 declarative tests that describe the intention of a feature, not just a sequence of
Line42 steps to drive it.
Line43 Using these techniques, we can even use higher-level tests to communicate di-
Line44 rectly with non-technical stakeholders, such as business analysts. If they’re willing
Line45 Chapter 22
Line46 Constructing Complex Test Data
Line47 264
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 265**
Line54 
Line55 to ignore the obscure punctuation, we can use the tests to help us narrow down
Line56 exactly what a feature should do, and why.
Line57 There are other tools that are designed to foster collaboration across the
Line58 technical and non-technical members in a team, such as FIT [Mugridge05]. We’ve
Line59 found, as have others such as the LiFT team [LIFT], that we can achieve much
Line60 of this while staying within our development toolset—and, of course, we can
Line61 write better tests for ourselves.
Line62 265
Line63 Communication First
Line64 
Line65 
Line66 ---
Line67 
Line68 ---
Line69 **Page 266**
Line70 
Line71 This page intentionally left blank
