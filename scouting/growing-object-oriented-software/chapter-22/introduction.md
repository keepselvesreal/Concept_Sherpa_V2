Line1 # Introduction (pp.257-258)
Line2 
Line3 ---
Line4 **Page 257**
Line5 
Line6 Chapter 22
Line7 Constructing Complex Test
Line8 Data
Line9 Many attempts to communicate are nulliﬁed by saying too much.
Line10 —Robert Greenleaf
Line11 Introduction
Line12 If we are strict about our use of constructors and immutable value objects, con-
Line13 structing objects in tests can be a chore. In production code, we construct such
Line14 objects in relatively few places and all the required values are available to hand
Line15 from, for example, user input, a database query, or a received message. In tests,
Line16 however, we have to provide all the constructor arguments every time we want
Line17 to create an object:
Line18 @Test public void chargesCustomerForTotalCostOfAllOrderedItems() {
Line19   Order order = new Order(
Line20       new Customer("Sherlock Holmes",
Line21           new Address("221b Baker Street", 
Line22                       "London", 
Line23                       new PostCode("NW1", "3RX"))));
Line24   order.addLine(new OrderLine("Deerstalker Hat", 1));
Line25   order.addLine(new OrderLine("Tweed Cape", 1));
Line26 […]
Line27 }
Line28 The code to create all these objects makes the tests hard to read, ﬁlling them
Line29 with information that doesn’t contribute to the behavior being tested. It also
Line30 makes tests brittle, as changes to the constructor arguments or the structure of
Line31 the objects will break many tests. The object mother pattern [Schuh01] is one
Line32 attempt to avoid this problem. An object mother is a class that contains a number
Line33 of factory methods [Gamma94] that create objects for use in tests. For example,
Line34 we could write an object mother for orders:
Line35 Order order = ExampleOrders.newDeerstalkerAndCapeOrder();
Line36 An object mother makes tests more readable by packaging up the code that
Line37 creates new object structures and giving it a name. It also helps with maintenance
Line38 since its features can be reused between tests. On the other hand, the object
Line39 257
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 258**
Line46 
Line47 mother pattern does not cope well with variation in the test data—every minor
Line48 difference requires a new factory method:
Line49 Order order1 = ExampleOrders.newDeerstalkerAndCapeAndSwordstickOrder();
Line50 Order order2 = ExampleOrders.newDeerstalkerAndBootsOrder();
Line51 […]
Line52 Over time, an object mother may itself become too messy to support, either
Line53 full of duplicated code or refactored into an inﬁnity of ﬁne-grained methods.
Line54 Test Data Builders
Line55 Another solution is to use the builder pattern to build instances in tests, most
Line56 often for values. For a class that requires complex setup, we create a test data
Line57 builder that has a ﬁeld for each constructor parameter, initialized to a safe value.
Line58 The builder has “chainable” public methods for overwriting the values in its
Line59 ﬁelds and, by convention, a build() method that is called last to create a new
Line60 instance of the target object from the ﬁeld values.1 An optional reﬁnement is to
Line61 add a static factory method for the builder itself so that it’s clearer in the test
Line62 what is being built. For example, a builder for Order objects might look like:
Line63 public class OrderBuilder {
Line64   private Customer customer = new CustomerBuilder().build();
Line65   private List<OrderLine> lines = new ArrayList<OrderLine>();
Line66   private BigDecimal discountRate = BigDecimal.ZERO;
Line67   public static OrderBuilder anOrder() {
Line68     return new OrderBuilder();
Line69   }
Line70   public OrderBuilder withCustomer(Customer customer) {
Line71     this.customer = customer;
Line72     return this;
Line73   }
Line74   public OrderBuilder withOrderLines(OrderLines lines) {
Line75     this.lines = lines;
Line76     return this;
Line77   }
Line78   public OrderBuilder withDiscount(BigDecimal discountRate) {
Line79     this.discountRate = discountRate;
Line80     return this;
Line81   }
Line82   public Order build() {
Line83     Order order = new Order(customer);
Line84     for (OrderLine line : lines) order.addLine(line);
Line85       order.setDiscountRate(discountRate);
Line86     }
Line87   }
Line88 }
Line89 1. This pattern is essentially the same as a Smalltalk cascade.
Line90 Chapter 22
Line91 Constructing Complex Test Data
Line92 258
Line93 
Line94 
Line95 ---
