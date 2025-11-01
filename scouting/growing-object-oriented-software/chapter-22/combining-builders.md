Line1 # Combining Builders (pp.261-261)
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
