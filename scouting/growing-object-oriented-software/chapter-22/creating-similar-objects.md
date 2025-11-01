Line1 # Creating Similar Objects (pp.259-261)
Line2 
Line3 ---
Line4 **Page 259**
Line5 
Line6 Tests that just need an Order object and are not concerned with its contents
Line7 can create one in a single line:
Line8 Order order = new OrderBuilder().build();
Line9 Tests that need particular values within an object can specify just those values
Line10 that are relevant and use defaults for the rest. This makes the test more expressive
Line11 because it includes only the values that are relevant to the expected results.
Line12 For example, if a test needed an Order for a Customer with no postcode, we
Line13 would write:
Line14 new OrderBuilder()
Line15   .fromCustomer(
Line16      new CustomerBuilder()
Line17       .withAddress(new AddressBuilder().withNoPostcode().build())
Line18       .build())
Line19   .build();
Line20 We ﬁnd that test data builders help keep tests expressive and resilient to change.
Line21 First, they wrap up most of the syntax noise when creating new objects. Second,
Line22 they make the default case simple, and special cases not much more complicated.
Line23 Third, they protect the test against changes in the structure of its objects. If we
Line24 add an argument to a constructor, then all we have to change is the relevant
Line25 builder and those tests that drove the need for the new argument.
Line26 A ﬁnal beneﬁt is that we can write test code that’s easier to read and spot errors,
Line27 because each builder method identiﬁes the purpose of its parameter. For example,
Line28 in this code it’s not obvious that “London” has been passed in as the second
Line29 street line rather than the city name:
Line30 TestAddresses.newAddress("221b Baker Street", "London", "NW1 6XE");
Line31 A test data builder makes the mistake more obvious:
Line32 new AddressBuilder()
Line33   .withStreet("221b Baker Street")
Line34   .withStreet2("London")
Line35   .withPostCode("NW1 6XE")
Line36   .build();
Line37 Creating Similar Objects
Line38 We can use builders when we need to create multiple similar objects. The most
Line39 obvious approach is to create a new builder for each new object, but this leads
Line40 to duplication and makes the test code harder to work with. For example, these
Line41 two orders are identical apart from the discount. If we didn’t highlight the
Line42 difference, it would be difﬁcult to ﬁnd:
Line43 259
Line44 Creating Similar Objects
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 260**
Line51 
Line52 Order orderWithSmallDiscount = new OrderBuilder()
Line53   .withLine("Deerstalker Hat", 1)
Line54   .withLine("Tweed Cape", 1)
Line55   .withDiscount(0.10)
Line56   .build();
Line57 Order orderWithLargeDiscount = new OrderBuilder()
Line58   .withLine("Deerstalker Hat", 1)
Line59   .withLine("Tweed Cape", 1)
Line60   .withDiscount(0.25)
Line61   .build(); 
Line62 Instead, we can initialize a single builder with the common state and then, for
Line63 each object to be built, deﬁne the differing values and call its build() method:
Line64 OrderBuilder hatAndCape = new OrderBuilder()
Line65   .withLine("Deerstalker Hat", 1)
Line66   .withLine("Tweed Cape", 1);
Line67 Order orderWithSmallDiscount = hatAndCape.withDiscount(0.10).build();
Line68 Order orderWithLargeDiscount = hatAndCape.withDiscount(0.25).build();
Line69 This produces a more focused test with less code. We can name the builder
Line70 after the features that are common, and the domain objects after their differences.
Line71 This technique works best if the objects differ by the same ﬁelds. If the objects
Line72 vary by different ﬁelds, each build() will pick up the changes from the previous
Line73 uses. For example, it’s not obvious in this code that orderWithGiftVoucher will
Line74 carry the 10% discount as well as a gift voucher:
Line75 Order orderWithDiscount = hatAndCape.withDiscount(0.10).build(); 
Line76 Order orderWithGiftVoucher = hatAndCape.withGiftVoucher("abc").build(); 
Line77 To avoid this problem, we could add a copy constructor or a method that
Line78 duplicates the state from another builder:
Line79 Order orderWithDiscount = new OrderBuilder(hatAndCape)
Line80   .withDiscount(0.10)
Line81   .build();
Line82 Order orderWithGiftVoucher = new OrderBuilder(hatAndCape)
Line83   .withGiftVoucher("abc")
Line84   .build();
Line85 Alternatively, we could add a factory method that returns a copy of the builder
Line86 with its current state:
Line87 Order orderWithDiscount = hatAndCape.but().withDiscount(0.10).build();
Line88 Order orderWithGiftVoucher = hatAndCape.but().withGiftVoucher("abc").build(); 
Line89 For complex setups, the safest option is to make the “with” methods functional
Line90 and have each one return a new copy of the builder instead of itself.
Line91 Chapter 22
Line92 Constructing Complex Test Data
Line93 260
Line94 
Line95 
Line96 ---
Line97 
Line98 ---
Line99 **Page 261**
Line100 
Line101 Combining Builders
Line102 Where a test data builder for an object uses other “built” objects, we can pass
Line103 in those builders as arguments rather than their objects. This will simplify the
Line104 test code by removing the build() methods. The result is easier to read because
Line105 it emphasizes the important information—what is being built—rather than the
Line106 mechanics of building it. For example, this code builds an order with no postcode,
Line107 but it’s dominated by the builder infrastructure:
Line108 Order orderWithNoPostcode = new OrderBuilder()
Line109   .fromCustomer(
Line110     new CustomerBuilder()
Line111         .withAddress(new AddressBuilder().withNoPostcode().build())
Line112         .build())
Line113     .build();
Line114 We can remove much of the noise by passing around builders:
Line115 Order order = new OrderBuilder()
Line116   .fromCustomer(
Line117      new CustomerBuilder()
Line118       .withAddress(new AddressBuilder().withNoPostcode())))
Line119   .build();
Line120 Emphasizing the Domain Model with Factory Methods
Line121 We can further reduce the noise in the test code by wrapping up the construction
Line122 of the builders in factory methods:
Line123 Order order = 
Line124 anOrder().fromCustomer(
Line125 aCustomer().withAddress(anAddress().withNoPostcode())).build();
Line126 As we compress the test code, the duplication in the builders becomes more
Line127 obtrusive; we have the name of the constructed type in both the “with” and
Line128 “builder” methods. We can take advantage of Java’s method overloading by
Line129 collapsing this to a single with() method, letting the Java type system ﬁgure out
Line130 which ﬁeld to update:
Line131 Order order = 
Line132   anOrder().from(aCustomer().with(anAddress().withNoPostcode())).build();
Line133 Obviously, this will only work with one argument of each type. For example,
Line134 if we introduce a Postcode, we can use overloading, whereas the rest of the builder
Line135 methods must have explicit names because they use String:
Line136 Address aLongerAddress = anAddress()
Line137     .withStreet("221b Baker Street")
Line138     .withCity("London")
Line139     .with(postCode("NW1", "3RX"))
Line140     .build();
Line141 261
Line142 Emphasizing the Domain Model with Factory Methods
Line143 
Line144 
Line145 ---
