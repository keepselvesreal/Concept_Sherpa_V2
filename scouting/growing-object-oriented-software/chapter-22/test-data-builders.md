Line1 # Test Data Builders (pp.258-259)
Line2 
Line3 ---
Line4 **Page 258**
Line5 
Line6 mother pattern does not cope well with variation in the test data—every minor
Line7 difference requires a new factory method:
Line8 Order order1 = ExampleOrders.newDeerstalkerAndCapeAndSwordstickOrder();
Line9 Order order2 = ExampleOrders.newDeerstalkerAndBootsOrder();
Line10 […]
Line11 Over time, an object mother may itself become too messy to support, either
Line12 full of duplicated code or refactored into an inﬁnity of ﬁne-grained methods.
Line13 Test Data Builders
Line14 Another solution is to use the builder pattern to build instances in tests, most
Line15 often for values. For a class that requires complex setup, we create a test data
Line16 builder that has a ﬁeld for each constructor parameter, initialized to a safe value.
Line17 The builder has “chainable” public methods for overwriting the values in its
Line18 ﬁelds and, by convention, a build() method that is called last to create a new
Line19 instance of the target object from the ﬁeld values.1 An optional reﬁnement is to
Line20 add a static factory method for the builder itself so that it’s clearer in the test
Line21 what is being built. For example, a builder for Order objects might look like:
Line22 public class OrderBuilder {
Line23   private Customer customer = new CustomerBuilder().build();
Line24   private List<OrderLine> lines = new ArrayList<OrderLine>();
Line25   private BigDecimal discountRate = BigDecimal.ZERO;
Line26   public static OrderBuilder anOrder() {
Line27     return new OrderBuilder();
Line28   }
Line29   public OrderBuilder withCustomer(Customer customer) {
Line30     this.customer = customer;
Line31     return this;
Line32   }
Line33   public OrderBuilder withOrderLines(OrderLines lines) {
Line34     this.lines = lines;
Line35     return this;
Line36   }
Line37   public OrderBuilder withDiscount(BigDecimal discountRate) {
Line38     this.discountRate = discountRate;
Line39     return this;
Line40   }
Line41   public Order build() {
Line42     Order order = new Order(customer);
Line43     for (OrderLine line : lines) order.addLine(line);
Line44       order.setDiscountRate(discountRate);
Line45     }
Line46   }
Line47 }
Line48 1. This pattern is essentially the same as a Smalltalk cascade.
Line49 Chapter 22
Line50 Constructing Complex Test Data
Line51 258
Line52 
Line53 
Line54 ---
Line55 
Line56 ---
Line57 **Page 259**
Line58 
Line59 Tests that just need an Order object and are not concerned with its contents
Line60 can create one in a single line:
Line61 Order order = new OrderBuilder().build();
Line62 Tests that need particular values within an object can specify just those values
Line63 that are relevant and use defaults for the rest. This makes the test more expressive
Line64 because it includes only the values that are relevant to the expected results.
Line65 For example, if a test needed an Order for a Customer with no postcode, we
Line66 would write:
Line67 new OrderBuilder()
Line68   .fromCustomer(
Line69      new CustomerBuilder()
Line70       .withAddress(new AddressBuilder().withNoPostcode().build())
Line71       .build())
Line72   .build();
Line73 We ﬁnd that test data builders help keep tests expressive and resilient to change.
Line74 First, they wrap up most of the syntax noise when creating new objects. Second,
Line75 they make the default case simple, and special cases not much more complicated.
Line76 Third, they protect the test against changes in the structure of its objects. If we
Line77 add an argument to a constructor, then all we have to change is the relevant
Line78 builder and those tests that drove the need for the new argument.
Line79 A ﬁnal beneﬁt is that we can write test code that’s easier to read and spot errors,
Line80 because each builder method identiﬁes the purpose of its parameter. For example,
Line81 in this code it’s not obvious that “London” has been passed in as the second
Line82 street line rather than the city name:
Line83 TestAddresses.newAddress("221b Baker Street", "London", "NW1 6XE");
Line84 A test data builder makes the mistake more obvious:
Line85 new AddressBuilder()
Line86   .withStreet("221b Baker Street")
Line87   .withStreet2("London")
Line88   .withPostCode("NW1 6XE")
Line89   .build();
Line90 Creating Similar Objects
Line91 We can use builders when we need to create multiple similar objects. The most
Line92 obvious approach is to create a new builder for each new object, but this leads
Line93 to duplication and makes the test code harder to work with. For example, these
Line94 two orders are identical apart from the discount. If we didn’t highlight the
Line95 difference, it would be difﬁcult to ﬁnd:
Line96 259
Line97 Creating Similar Objects
Line98 
Line99 
Line100 ---
