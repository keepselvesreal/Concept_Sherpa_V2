Line1 # Removing Duplication at the Point of Use (pp.262-264)
Line2 
Line3 ---
Line4 **Page 262**
Line5 
Line6 This should encourage us to introduce domain types, which, as we wrote in
Line7 “Domain Types Are Better Than Strings” (page 213), leads to more expressive
Line8 and maintainable code.
Line9 Removing Duplication at the Point of Use
Line10 We’ve made the process of assembling complex objects for tests simpler and more
Line11 expressive by using test data builders. Now, let’s look at how we can structure
Line12 our tests to make the best use of these builders in context. We often ﬁnd ourselves
Line13 writing tests with similar code to create supporting objects and pass them to the
Line14 code under test, so we want to clean up this duplication. We’ve found that some
Line15 refactorings are better than others; here’s an example.
Line16 First, Remove Duplication
Line17 We have a system that processes orders asynchronously. The test feeds orders
Line18 into the system, tracks their progress on a monitor, and then looks for them in
Line19 a user interface. We’ve packaged up all the infrastructure so the test looks like this:
Line20 @Test public void reportsTotalSalesOfOrderedProducts() {
Line21   Order order1 = anOrder()
Line22     .withLine("Deerstalker Hat", 1)
Line23     .withLine("Tweed Cape", 1)
Line24     .withCustomersReference(1234)
Line25     .build();
Line26   requestSender.send(order1);
Line27   progressMonitor.waitForCompletion(order1);
Line28   Order order2 = anOrder()
Line29     .withLine("Deerstalker Hat", 1)
Line30     .withCustomersReference(5678)
Line31     .build();
Line32   requestSender.send(order2);
Line33   progressMonitor.waitForCompletion(order2);
Line34   TotalSalesReport report = gui.openSalesReport();
Line35   report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
Line36   report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
Line37 }
Line38 There’s an obvious duplication in the way the orders are created, sent, and
Line39 tracked. Our ﬁrst thought might be to pull that into a helper method:
Line40 @Test public void reportsTotalSalesOfOrderedProducts() {
Line41 submitOrderFor("Deerstalker Hat", "Tweed Cape");
Line42 submitOrderFor("Deerstalker Hat");
Line43   TotalSalesReport report = gui.openSalesReport();
Line44   report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
Line45   report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
Line46 }
Line47 Chapter 22
Line48 Constructing Complex Test Data
Line49 262
Line50 
Line51 
Line52 ---
Line53 
Line54 ---
Line55 **Page 263**
Line56 
Line57 void submitOrderFor(String ... products) {
Line58   OrderBuilder orderBuilder = anOrder()
Line59     .withCustomersReference(nextCustomerReference());
Line60   for (String product : products) {
Line61     orderBuilder = orderBuilder.withLine(product, 1);
Line62   }
Line63   Order order = orderBuilder.build();
Line64   requestSender.send(order);
Line65   progressMonitor.waitForCompletion(order);
Line66 }
Line67 This refactoring works ﬁne when there’s a single case but, like the object
Line68 mother pattern, does not scale well when we have variation. As we deal with
Line69 orders with different contents, amendments, cancellations, and so on, we end up
Line70 with this sort of mess:
Line71 void submitOrderFor(String ... products) { […]
Line72 void submitOrderFor(String product, int count, 
Line73                     String otherProduct, int otherCount) { […]
Line74 void submitOrderFor(String product, double discount) { […]
Line75 void submitOrderFor(String product, String giftVoucherCode) { […]
Line76 We think a bit harder about what varies between tests and what is common,
Line77 and realize that a better alternative is to pass the builder through, not its argu-
Line78 ments; it’s similar to when we started combining builders. The helper method
Line79 can use the builder to add any supporting detail to the order before feeding it
Line80 into the system:
Line81 @Test public void reportsTotalSalesOfOrderedProducts() {
Line82 sendAndProcess(anOrder()
Line83     .withLine("Deerstalker Hat", 1)
Line84     .withLine("Tweed Cape", 1));
Line85 sendAndProcess(anOrder()
Line86     .withLine("Deerstalker Hat", 1));
Line87   TotalSalesReport report = gui.openSalesReport();
Line88   report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
Line89   report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
Line90 }
Line91 void sendAndProcess(OrderBuilder orderDetails) {
Line92   Order order = orderDetails
Line93     .withDefaultCustomersReference(nextCustomerReference())
Line94     .build();
Line95   requestSender.send(order);
Line96   progressMonitor.waitForCompletion(order);
Line97 }
Line98 263
Line99 Removing Duplication at the Point of Use
Line100 
Line101 
Line102 ---
Line103 
Line104 ---
Line105 **Page 264**
Line106 
Line107 Then, Raise the Game
Line108 The test code is looking better, but it still reads like a script. We can change its
Line109 emphasis to what behavior is expected, rather than how the test is implemented,
Line110 by rewording some of the names:
Line111 @Test public void reportsTotalSalesOfOrderedProducts() {
Line112 havingReceived(anOrder()
Line113       .withLine("Deerstalker Hat", 1)
Line114       .withLine("Tweed Cape", 1));
Line115 havingReceived(anOrder()
Line116       .withLine("Deerstalker Hat", 1));
Line117   TotalSalesReport report = gui.openSalesReport();
Line118   report.displaysTotalSalesFor("Deerstalker Hat", equalTo(2));
Line119   report.displaysTotalSalesFor("Tweed Cape", equalTo(1));
Line120 }
Line121 @Test public void takesAmendmentsIntoAccountWhenCalculatingTotalSales() {
Line122   Customer theCustomer = aCustomer().build();
Line123 havingReceived(anOrder().from(theCustomer)
Line124     .withLine("Deerstalker Hat", 1)
Line125     .withLine("Tweed Cape", 1));
Line126 havingReceived(anOrderAmendment().from(theCustomer)
Line127     .withLine("Deerstalker Hat", 2));
Line128   TotalSalesReport report = user.openSalesReport();
Line129   report.containsTotalSalesFor("Deerstalker Hat", equalTo(2));
Line130   report.containsTotalSalesFor("Tweed Cape", equalTo(1));
Line131 }
Line132 We started with a test that looked procedural, extracted some of its behavior
Line133 into builder objects, and ended up with a declarative description of what the
Line134 feature does. We’re nudging the test code towards the sort of language we could
Line135 use when discussing the feature with someone else, even someone non-technical;
Line136 we push everything else into supporting code.
Line137 Communication First
Line138 We use test data builders to reduce duplication and make the test code more ex-
Line139 pressive. It’s another technique that reﬂects our obsession with the language of
Line140 code, driven by the principle that code is there to be read. Combined with factory
Line141 methods and test scaffolding, test data builders help us write more literate,
Line142 declarative tests that describe the intention of a feature, not just a sequence of
Line143 steps to drive it.
Line144 Using these techniques, we can even use higher-level tests to communicate di-
Line145 rectly with non-technical stakeholders, such as business analysts. If they’re willing
Line146 Chapter 22
Line147 Constructing Complex Test Data
Line148 264
Line149 
Line150 
Line151 ---
