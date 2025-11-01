Line1 # Emphasizing the Domain Model with Factory Methods (pp.261-262)
Line2 
Line3 ---
Line4 **Page 261**
Line5 
Line6 Combining Builders
Line7 Where a test data builder for an object uses other “built” objects, we can pass
Line8 in those builders as arguments rather than their objects. This will simplify the
Line9 test code by removing the build() methods. The result is easier to read because
Line10 it emphasizes the important information—what is being built—rather than the
Line11 mechanics of building it. For example, this code builds an order with no postcode,
Line12 but it’s dominated by the builder infrastructure:
Line13 Order orderWithNoPostcode = new OrderBuilder()
Line14   .fromCustomer(
Line15     new CustomerBuilder()
Line16         .withAddress(new AddressBuilder().withNoPostcode().build())
Line17         .build())
Line18     .build();
Line19 We can remove much of the noise by passing around builders:
Line20 Order order = new OrderBuilder()
Line21   .fromCustomer(
Line22      new CustomerBuilder()
Line23       .withAddress(new AddressBuilder().withNoPostcode())))
Line24   .build();
Line25 Emphasizing the Domain Model with Factory Methods
Line26 We can further reduce the noise in the test code by wrapping up the construction
Line27 of the builders in factory methods:
Line28 Order order = 
Line29 anOrder().fromCustomer(
Line30 aCustomer().withAddress(anAddress().withNoPostcode())).build();
Line31 As we compress the test code, the duplication in the builders becomes more
Line32 obtrusive; we have the name of the constructed type in both the “with” and
Line33 “builder” methods. We can take advantage of Java’s method overloading by
Line34 collapsing this to a single with() method, letting the Java type system ﬁgure out
Line35 which ﬁeld to update:
Line36 Order order = 
Line37   anOrder().from(aCustomer().with(anAddress().withNoPostcode())).build();
Line38 Obviously, this will only work with one argument of each type. For example,
Line39 if we introduce a Postcode, we can use overloading, whereas the rest of the builder
Line40 methods must have explicit names because they use String:
Line41 Address aLongerAddress = anAddress()
Line42     .withStreet("221b Baker Street")
Line43     .withCity("London")
Line44     .with(postCode("NW1", "3RX"))
Line45     .build();
Line46 261
Line47 Emphasizing the Domain Model with Factory Methods
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 262**
Line54 
Line55 This should encourage us to introduce domain types, which, as we wrote in
Line56 “Domain Types Are Better Than Strings” (page 213), leads to more expressive
Line57 and maintainable code.
Line58 Removing Duplication at the Point of Use
Line59 We’ve made the process of assembling complex objects for tests simpler and more
Line60 expressive by using test data builders. Now, let’s look at how we can structure
Line61 our tests to make the best use of these builders in context. We often ﬁnd ourselves
Line62 writing tests with similar code to create supporting objects and pass them to the
Line63 code under test, so we want to clean up this duplication. We’ve found that some
Line64 refactorings are better than others; here’s an example.
Line65 First, Remove Duplication
Line66 We have a system that processes orders asynchronously. The test feeds orders
Line67 into the system, tracks their progress on a monitor, and then looks for them in
Line68 a user interface. We’ve packaged up all the infrastructure so the test looks like this:
Line69 @Test public void reportsTotalSalesOfOrderedProducts() {
Line70   Order order1 = anOrder()
Line71     .withLine("Deerstalker Hat", 1)
Line72     .withLine("Tweed Cape", 1)
Line73     .withCustomersReference(1234)
Line74     .build();
Line75   requestSender.send(order1);
Line76   progressMonitor.waitForCompletion(order1);
Line77   Order order2 = anOrder()
Line78     .withLine("Deerstalker Hat", 1)
Line79     .withCustomersReference(5678)
Line80     .build();
Line81   requestSender.send(order2);
Line82   progressMonitor.waitForCompletion(order2);
Line83   TotalSalesReport report = gui.openSalesReport();
Line84   report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
Line85   report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
Line86 }
Line87 There’s an obvious duplication in the way the orders are created, sent, and
Line88 tracked. Our ﬁrst thought might be to pull that into a helper method:
Line89 @Test public void reportsTotalSalesOfOrderedProducts() {
Line90 submitOrderFor("Deerstalker Hat", "Tweed Cape");
Line91 submitOrderFor("Deerstalker Hat");
Line92   TotalSalesReport report = gui.openSalesReport();
Line93   report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
Line94   report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
Line95 }
Line96 Chapter 22
Line97 Constructing Complex Test Data
Line98 262
Line99 
Line100 
Line101 ---
