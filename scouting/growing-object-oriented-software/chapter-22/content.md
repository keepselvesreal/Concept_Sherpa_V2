# Chapter 22: Constructing Complex Test Data (pp.257-266)

---
**Page 257**

Chapter 22
Constructing Complex Test
Data
Many attempts to communicate are nulliﬁed by saying too much.
—Robert Greenleaf
Introduction
If we are strict about our use of constructors and immutable value objects, con-
structing objects in tests can be a chore. In production code, we construct such
objects in relatively few places and all the required values are available to hand
from, for example, user input, a database query, or a received message. In tests,
however, we have to provide all the constructor arguments every time we want
to create an object:
@Test public void chargesCustomerForTotalCostOfAllOrderedItems() {
  Order order = new Order(
      new Customer("Sherlock Holmes",
          new Address("221b Baker Street", 
                      "London", 
                      new PostCode("NW1", "3RX"))));
  order.addLine(new OrderLine("Deerstalker Hat", 1));
  order.addLine(new OrderLine("Tweed Cape", 1));
[…]
}
The code to create all these objects makes the tests hard to read, ﬁlling them
with information that doesn’t contribute to the behavior being tested. It also
makes tests brittle, as changes to the constructor arguments or the structure of
the objects will break many tests. The object mother pattern [Schuh01] is one
attempt to avoid this problem. An object mother is a class that contains a number
of factory methods [Gamma94] that create objects for use in tests. For example,
we could write an object mother for orders:
Order order = ExampleOrders.newDeerstalkerAndCapeOrder();
An object mother makes tests more readable by packaging up the code that
creates new object structures and giving it a name. It also helps with maintenance
since its features can be reused between tests. On the other hand, the object
257


---
**Page 258**

mother pattern does not cope well with variation in the test data—every minor
difference requires a new factory method:
Order order1 = ExampleOrders.newDeerstalkerAndCapeAndSwordstickOrder();
Order order2 = ExampleOrders.newDeerstalkerAndBootsOrder();
[…]
Over time, an object mother may itself become too messy to support, either
full of duplicated code or refactored into an inﬁnity of ﬁne-grained methods.
Test Data Builders
Another solution is to use the builder pattern to build instances in tests, most
often for values. For a class that requires complex setup, we create a test data
builder that has a ﬁeld for each constructor parameter, initialized to a safe value.
The builder has “chainable” public methods for overwriting the values in its
ﬁelds and, by convention, a build() method that is called last to create a new
instance of the target object from the ﬁeld values.1 An optional reﬁnement is to
add a static factory method for the builder itself so that it’s clearer in the test
what is being built. For example, a builder for Order objects might look like:
public class OrderBuilder {
  private Customer customer = new CustomerBuilder().build();
  private List<OrderLine> lines = new ArrayList<OrderLine>();
  private BigDecimal discountRate = BigDecimal.ZERO;
  public static OrderBuilder anOrder() {
    return new OrderBuilder();
  }
  public OrderBuilder withCustomer(Customer customer) {
    this.customer = customer;
    return this;
  }
  public OrderBuilder withOrderLines(OrderLines lines) {
    this.lines = lines;
    return this;
  }
  public OrderBuilder withDiscount(BigDecimal discountRate) {
    this.discountRate = discountRate;
    return this;
  }
  public Order build() {
    Order order = new Order(customer);
    for (OrderLine line : lines) order.addLine(line);
      order.setDiscountRate(discountRate);
    }
  }
}
1. This pattern is essentially the same as a Smalltalk cascade.
Chapter 22
Constructing Complex Test Data
258


---
**Page 259**

Tests that just need an Order object and are not concerned with its contents
can create one in a single line:
Order order = new OrderBuilder().build();
Tests that need particular values within an object can specify just those values
that are relevant and use defaults for the rest. This makes the test more expressive
because it includes only the values that are relevant to the expected results.
For example, if a test needed an Order for a Customer with no postcode, we
would write:
new OrderBuilder()
  .fromCustomer(
     new CustomerBuilder()
      .withAddress(new AddressBuilder().withNoPostcode().build())
      .build())
  .build();
We ﬁnd that test data builders help keep tests expressive and resilient to change.
First, they wrap up most of the syntax noise when creating new objects. Second,
they make the default case simple, and special cases not much more complicated.
Third, they protect the test against changes in the structure of its objects. If we
add an argument to a constructor, then all we have to change is the relevant
builder and those tests that drove the need for the new argument.
A ﬁnal beneﬁt is that we can write test code that’s easier to read and spot errors,
because each builder method identiﬁes the purpose of its parameter. For example,
in this code it’s not obvious that “London” has been passed in as the second
street line rather than the city name:
TestAddresses.newAddress("221b Baker Street", "London", "NW1 6XE");
A test data builder makes the mistake more obvious:
new AddressBuilder()
  .withStreet("221b Baker Street")
  .withStreet2("London")
  .withPostCode("NW1 6XE")
  .build();
Creating Similar Objects
We can use builders when we need to create multiple similar objects. The most
obvious approach is to create a new builder for each new object, but this leads
to duplication and makes the test code harder to work with. For example, these
two orders are identical apart from the discount. If we didn’t highlight the
difference, it would be difﬁcult to ﬁnd:
259
Creating Similar Objects


---
**Page 260**

Order orderWithSmallDiscount = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1)
  .withDiscount(0.10)
  .build();
Order orderWithLargeDiscount = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1)
  .withDiscount(0.25)
  .build(); 
Instead, we can initialize a single builder with the common state and then, for
each object to be built, deﬁne the differing values and call its build() method:
OrderBuilder hatAndCape = new OrderBuilder()
  .withLine("Deerstalker Hat", 1)
  .withLine("Tweed Cape", 1);
Order orderWithSmallDiscount = hatAndCape.withDiscount(0.10).build();
Order orderWithLargeDiscount = hatAndCape.withDiscount(0.25).build();
This produces a more focused test with less code. We can name the builder
after the features that are common, and the domain objects after their differences.
This technique works best if the objects differ by the same ﬁelds. If the objects
vary by different ﬁelds, each build() will pick up the changes from the previous
uses. For example, it’s not obvious in this code that orderWithGiftVoucher will
carry the 10% discount as well as a gift voucher:
Order orderWithDiscount = hatAndCape.withDiscount(0.10).build(); 
Order orderWithGiftVoucher = hatAndCape.withGiftVoucher("abc").build(); 
To avoid this problem, we could add a copy constructor or a method that
duplicates the state from another builder:
Order orderWithDiscount = new OrderBuilder(hatAndCape)
  .withDiscount(0.10)
  .build();
Order orderWithGiftVoucher = new OrderBuilder(hatAndCape)
  .withGiftVoucher("abc")
  .build();
Alternatively, we could add a factory method that returns a copy of the builder
with its current state:
Order orderWithDiscount = hatAndCape.but().withDiscount(0.10).build();
Order orderWithGiftVoucher = hatAndCape.but().withGiftVoucher("abc").build(); 
For complex setups, the safest option is to make the “with” methods functional
and have each one return a new copy of the builder instead of itself.
Chapter 22
Constructing Complex Test Data
260


---
**Page 261**

Combining Builders
Where a test data builder for an object uses other “built” objects, we can pass
in those builders as arguments rather than their objects. This will simplify the
test code by removing the build() methods. The result is easier to read because
it emphasizes the important information—what is being built—rather than the
mechanics of building it. For example, this code builds an order with no postcode,
but it’s dominated by the builder infrastructure:
Order orderWithNoPostcode = new OrderBuilder()
  .fromCustomer(
    new CustomerBuilder()
        .withAddress(new AddressBuilder().withNoPostcode().build())
        .build())
    .build();
We can remove much of the noise by passing around builders:
Order order = new OrderBuilder()
  .fromCustomer(
     new CustomerBuilder()
      .withAddress(new AddressBuilder().withNoPostcode())))
  .build();
Emphasizing the Domain Model with Factory Methods
We can further reduce the noise in the test code by wrapping up the construction
of the builders in factory methods:
Order order = 
anOrder().fromCustomer(
aCustomer().withAddress(anAddress().withNoPostcode())).build();
As we compress the test code, the duplication in the builders becomes more
obtrusive; we have the name of the constructed type in both the “with” and
“builder” methods. We can take advantage of Java’s method overloading by
collapsing this to a single with() method, letting the Java type system ﬁgure out
which ﬁeld to update:
Order order = 
  anOrder().from(aCustomer().with(anAddress().withNoPostcode())).build();
Obviously, this will only work with one argument of each type. For example,
if we introduce a Postcode, we can use overloading, whereas the rest of the builder
methods must have explicit names because they use String:
Address aLongerAddress = anAddress()
    .withStreet("221b Baker Street")
    .withCity("London")
    .with(postCode("NW1", "3RX"))
    .build();
261
Emphasizing the Domain Model with Factory Methods


---
**Page 262**

This should encourage us to introduce domain types, which, as we wrote in
“Domain Types Are Better Than Strings” (page 213), leads to more expressive
and maintainable code.
Removing Duplication at the Point of Use
We’ve made the process of assembling complex objects for tests simpler and more
expressive by using test data builders. Now, let’s look at how we can structure
our tests to make the best use of these builders in context. We often ﬁnd ourselves
writing tests with similar code to create supporting objects and pass them to the
code under test, so we want to clean up this duplication. We’ve found that some
refactorings are better than others; here’s an example.
First, Remove Duplication
We have a system that processes orders asynchronously. The test feeds orders
into the system, tracks their progress on a monitor, and then looks for them in
a user interface. We’ve packaged up all the infrastructure so the test looks like this:
@Test public void reportsTotalSalesOfOrderedProducts() {
  Order order1 = anOrder()
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1)
    .withCustomersReference(1234)
    .build();
  requestSender.send(order1);
  progressMonitor.waitForCompletion(order1);
  Order order2 = anOrder()
    .withLine("Deerstalker Hat", 1)
    .withCustomersReference(5678)
    .build();
  requestSender.send(order2);
  progressMonitor.waitForCompletion(order2);
  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}
There’s an obvious duplication in the way the orders are created, sent, and
tracked. Our ﬁrst thought might be to pull that into a helper method:
@Test public void reportsTotalSalesOfOrderedProducts() {
submitOrderFor("Deerstalker Hat", "Tweed Cape");
submitOrderFor("Deerstalker Hat");
  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}
Chapter 22
Constructing Complex Test Data
262


---
**Page 263**

void submitOrderFor(String ... products) {
  OrderBuilder orderBuilder = anOrder()
    .withCustomersReference(nextCustomerReference());
  for (String product : products) {
    orderBuilder = orderBuilder.withLine(product, 1);
  }
  Order order = orderBuilder.build();
  requestSender.send(order);
  progressMonitor.waitForCompletion(order);
}
This refactoring works ﬁne when there’s a single case but, like the object
mother pattern, does not scale well when we have variation. As we deal with
orders with different contents, amendments, cancellations, and so on, we end up
with this sort of mess:
void submitOrderFor(String ... products) { […]
void submitOrderFor(String product, int count, 
                    String otherProduct, int otherCount) { […]
void submitOrderFor(String product, double discount) { […]
void submitOrderFor(String product, String giftVoucherCode) { […]
We think a bit harder about what varies between tests and what is common,
and realize that a better alternative is to pass the builder through, not its argu-
ments; it’s similar to when we started combining builders. The helper method
can use the builder to add any supporting detail to the order before feeding it
into the system:
@Test public void reportsTotalSalesOfOrderedProducts() {
sendAndProcess(anOrder()
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1));
sendAndProcess(anOrder()
    .withLine("Deerstalker Hat", 1));
  TotalSalesReport report = gui.openSalesReport();
  report.checkDisplayedTotalSalesFor("Deerstalker Hat", is(equalTo(2)));
  report.checkDisplayedTotalSalesFor("Tweed Cape", is(equalTo(1)));
}
void sendAndProcess(OrderBuilder orderDetails) {
  Order order = orderDetails
    .withDefaultCustomersReference(nextCustomerReference())
    .build();
  requestSender.send(order);
  progressMonitor.waitForCompletion(order);
}
263
Removing Duplication at the Point of Use


---
**Page 264**

Then, Raise the Game
The test code is looking better, but it still reads like a script. We can change its
emphasis to what behavior is expected, rather than how the test is implemented,
by rewording some of the names:
@Test public void reportsTotalSalesOfOrderedProducts() {
havingReceived(anOrder()
      .withLine("Deerstalker Hat", 1)
      .withLine("Tweed Cape", 1));
havingReceived(anOrder()
      .withLine("Deerstalker Hat", 1));
  TotalSalesReport report = gui.openSalesReport();
  report.displaysTotalSalesFor("Deerstalker Hat", equalTo(2));
  report.displaysTotalSalesFor("Tweed Cape", equalTo(1));
}
@Test public void takesAmendmentsIntoAccountWhenCalculatingTotalSales() {
  Customer theCustomer = aCustomer().build();
havingReceived(anOrder().from(theCustomer)
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1));
havingReceived(anOrderAmendment().from(theCustomer)
    .withLine("Deerstalker Hat", 2));
  TotalSalesReport report = user.openSalesReport();
  report.containsTotalSalesFor("Deerstalker Hat", equalTo(2));
  report.containsTotalSalesFor("Tweed Cape", equalTo(1));
}
We started with a test that looked procedural, extracted some of its behavior
into builder objects, and ended up with a declarative description of what the
feature does. We’re nudging the test code towards the sort of language we could
use when discussing the feature with someone else, even someone non-technical;
we push everything else into supporting code.
Communication First
We use test data builders to reduce duplication and make the test code more ex-
pressive. It’s another technique that reﬂects our obsession with the language of
code, driven by the principle that code is there to be read. Combined with factory
methods and test scaffolding, test data builders help us write more literate,
declarative tests that describe the intention of a feature, not just a sequence of
steps to drive it.
Using these techniques, we can even use higher-level tests to communicate di-
rectly with non-technical stakeholders, such as business analysts. If they’re willing
Chapter 22
Constructing Complex Test Data
264


---
**Page 265**

to ignore the obscure punctuation, we can use the tests to help us narrow down
exactly what a feature should do, and why.
There are other tools that are designed to foster collaboration across the
technical and non-technical members in a team, such as FIT [Mugridge05]. We’ve
found, as have others such as the LiFT team [LIFT], that we can achieve much
of this while staying within our development toolset—and, of course, we can
write better tests for ourselves.
265
Communication First


---
**Page 266**

This page intentionally left blank 


