Line1 # Testing an Object That Performs Persistence Operations (pp.294-297)
Line2 
Line3 ---
Line4 **Page 294**
Line5 
Line6 The techniques we describe in this chapter are compatible with this kind of
Line7 framework.We have used them to test applications built within Java EE and Spring,
Line8 and with “plain old” Java programs that use JPA, Hibernate, or JDBC directly.
Line9 The frameworks wrap transaction management around the objects that make
Line10 use of transactional resources, so there’s nothing in their code to mark the appli-
Line11 cation’s transaction boundaries. The tests for those objects, however, need to
Line12 manage transactions explicitly—which is what a transactor is for.
Line13 In the tests, the transactor uses the same transaction manager as the application,
Line14 conﬁgured in the same way. This ensures that the tests and the full application
Line15 run the same transactional code. It should make no difference whether a trans-
Line16 action is controlled by a block wrapped around our code by the framework, or by
Line17 a transactor in our tests. But if we’ve made a mistake and it does make a difference,
Line18 our end-to-end tests should catch such failures by exercising the application code
Line19 in the container.
Line20 Testing an Object That Performs Persistence Operations
Line21 Now that we’ve got some test scaffolding we can write tests for an object that
Line22 performs persistence.
Line23 In our domain model, a customer base represents all the customers we know
Line24 about. We can add customers to our customer base and ﬁnd customers that match
Line25 certain criteria. For example, we need to ﬁnd customers with credit cards that
Line26 are about to expire so that we can send them a reminder to update their payment
Line27 details.
Line28 public interface CustomerBase {  […]
Line29   void addCustomer(Customer customer);
Line30   List<Customer> customersWithExpiredCreditCardsAt(Date deadline);
Line31 }
Line32 When unit-testing code that calls a CustomerBase to ﬁnd and notify the
Line33 relevant customers, we can mock the interface. In a deployed system, however,
Line34 this code will call a real implementation of CustomerBase that is backed by JPA
Line35 to save and load customer information from a database. We must also test that
Line36 this persistent implementation works correctly—that the queries it makes and
Line37 the object/relational mappings are correct. For example, below is a test of the
Line38 customersWithExpiredCreditCardsAt() query. There are two helper methods
Line39 that interact with customerBase within a transaction: addCustomer() adds a set
Line40 of example customers, and assertCustomersExpiringOn() queries for customers
Line41 with expired cards.
Line42 Chapter 25
Line43 Testing Persistence
Line44 294
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 295**
Line51 
Line52 public class PersistentCustomerBaseTest { […]
Line53   final PersistentCustomerBase customerBase = 
Line54                                  new PersistentCustomerBase(entityManager);
Line55   @Test
Line56   @SuppressWarnings("unchecked")
Line57   public void findsCustomersWithCreditCardsThatAreAboutToExpire() throws Exception {
Line58     final String deadline = "6 Jun 2009";
Line59     addCustomers(
Line60       aCustomer().withName("Alice (Expired)")
Line61         .withPaymentMethods(aCreditCard().withExpiryDate(date("1 Jan 2009"))),
Line62       aCustomer().withName("Bob (Expired)")
Line63         .withPaymentMethods(aCreditCard().withExpiryDate(date("5 Jun 2009"))),
Line64       aCustomer().withName("Carol (Valid)")
Line65         .withPaymentMethods(aCreditCard().withExpiryDate(date(deadline))),
Line66       aCustomer().withName("Dave (Valid)")
Line67         .withPaymentMethods(aCreditCard().withExpiryDate(date("7 Jun 2009")))
Line68     );
Line69     assertCustomersExpiringOn(date(deadline), 
Line70                               containsInAnyOrder(customerNamed("Alice (Expired)"), 
Line71                                                  customerNamed("Bob (Expired)")));
Line72   }
Line73   private void addCustomers(final CustomerBuilder... customers) throws Exception {
Line74 transactor.perform(new UnitOfWork() {
Line75       public void work() throws Exception {
Line76         for (CustomerBuilder customer : customers) { 
Line77 customerBase.addCustomer(customer.build());
Line78         }
Line79       }
Line80     });
Line81   }
Line82   private void assertCustomersExpiringOn(final Date date, 
Line83                                          final Matcher<Iterable<Customer>> matcher)
Line84     throws Exception 
Line85   {
Line86 transactor.perform(new UnitOfWork() {
Line87       public void work() throws Exception {
Line88         assertThat(customerBase.customersWithExpiredCreditCardsAsOf(date), matcher);
Line89       }
Line90     });
Line91   }
Line92 }
Line93 We call addCustomers() with CustomerBuilders set up to include a name and
Line94 an expiry date for the credit card. The expiry date is the signiﬁcant ﬁeld for this
Line95 test, so we create customers with expiry dates before, on, and after the deadline to
Line96 demonstrate the boundary condition. We also set the name of each customer
Line97 to identify the instances in a failure (notice that the names self-describe the relevant
Line98 status of each customer). An alternative to matching on name would have been
Line99 to use each object’s persistence identiﬁer, which is assigned by JPA. That would
Line100 have been more complex to work with (it’s not exposed as a property on
Line101 Customer), and would not be self-describing.
Line102 295
Line103 Testing an Object That Performs Persistence Operations
Line104 
Line105 
Line106 ---
Line107 
Line108 ---
Line109 **Page 296**
Line110 
Line111 The assertCustomersExpiringOn() method runs the query we’re testing for
Line112 the given deadline and checks that the result conforms to the Hamcrest matcher
Line113 we pass in. The containsInAnyOrder() method returns a matcher that checks
Line114 that there’s a sub-matcher for each of the elements in a collection. We’ve written
Line115 a customerNamed() method to return a custom matcher that tests whether an
Line116 object is a Customer with a given name (there’s more on custom matchers in
Line117 Appendix B). So, this test says that we expect to receive back exactly two Customer
Line118 objects, named "Alice (Expired)" and "Bob (Expired)".
Line119 The test implicitly exercises CustomerBase.addCustomer() by calling it to set
Line120 up the database for the query. Thinking further, what we actually care about is
Line121 the relationship between the result of calling addCustomer() and subsequent
Line122 queries, so we probably won’t test addCustomer() independently. If there’s an
Line123 effect of addCustomer() that is not visible through some feature of the system,
Line124 then we’d have to ask some hard questions about its purpose before writing a
Line125 special test query to cover it.
Line126 Better Test Structure with Matchers
Line127 This test includes a nice example of using Hamcrest to create a clean test structure.
Line128 The test method constructs a matcher, which gives a concise description of a valid
Line129 result for the query. It passes the matcher to assertCustomersExpiringOn(),
Line130 which just runs the query and passes the result to the matcher. We have a clean
Line131 separation between the test method, which knows what is expected to be retrieved,
Line132 and the query/assert method, which knows how to make a query and can be used
Line133 in other tests.
Line134 Here is an implementation of PersistentCustomerBase that passes the test:
Line135 public class PersistentCustomerBase implements CustomerBase {
Line136   private final EntityManager entityManager;
Line137   public PersistentCustomerBase(EntityManager entityManager) {
Line138     this.entityManager = entityManager;
Line139   }
Line140   public void addCustomer(Customer customer) {
Line141     entityManager.persist(customer);
Line142   }
Line143   public List<Customer> customersWithExpiredCreditCardsAt(Date deadline) {
Line144     Query query = entityManager.createQuery(
Line145         "select c from Customer c, CreditCardDetails d " +
Line146         "where d member of c.paymentMethods " +
Line147         "  and d.expiryDate < :deadline");
Line148     query.setParameter("deadline", deadline);
Line149     return query.getResultList();
Line150   }
Line151 }
Line152 Chapter 25
Line153 Testing Persistence
Line154 296
Line155 
Line156 
Line157 ---
Line158 
Line159 ---
Line160 **Page 297**
Line161 
Line162 This implementation looks trivial—it’s so much shorter than its test—but it
Line163 relies on a lot of XML conﬁguration that we haven’t included and on a third-party
Line164 framework that implements the EntityManager’s simple API.
Line165 On Patterns and Type Names
Line166 The CustomerBase interface and PersistentCustomerBase class implement the
Line167 repository or data access object pattern (often abbreviated to DAO).We have not
Line168 used the terms “Repository,” “DataAccessObject,” or “DAO” in the name of the
Line169 interface or class that implements it because:
Line170 •
Line171 Using such terms leaks knowledge about the underlying technology layers
Line172 (persistence) into the application domain, and so breaks the “ports and
Line173 adapters” architecture.The objects that use a CustomerBase are persistence-
Line174 agnostic: they do not care whether the Customer objects they interact with
Line175 are written to disk or not.The Customer objects are also persistence-agnostic:
Line176 a program does not need to have a database to create and use Customer
Line177 objects. Only PersistentCustomerBase knows how it maps Customer objects
Line178 in and out of persistent storage.
Line179 •
Line180 We prefer not to name classes or interfaces after patterns; what matters
Line181 to us is their relationship to other classes in the system. The clients of
Line182 CustomerBase do not care what patterns it uses. As the system evolves, we
Line183 might make the CustomerBase class work in some other way and the name
Line184 would then be misleading.
Line185 •
Line186 We avoid generic words like “data,” “object,” or “access” in type names.We
Line187 try to give each class a name that identiﬁes a concept within its domain or
Line188 expresses how it bridges between the application and technical domains.
Line189 Testing That Objects Can Be Persisted
Line190 The PersistentCustomerBase relies on so much conﬁguration and underlying
Line191 third-party code that the error messages from its test can be difﬁcult to diagnose.
Line192 A test failure could be caused by a defect in a query, the mapping of the Customer
Line193 class, the mapping of any of the classes that it uses, the conﬁguration of the ORM,
Line194 invalid database connection parameters, or a misconﬁguration of the database
Line195 itself.
Line196 We can write more tests to help us pinpoint the cause of a persistence failure
Line197 when it occurs. A useful test is to “round-trip” instances of all persistent entity
Line198 types through the database to check that the mappings are conﬁgured correctly
Line199 for each class.
Line200 Round-trip tests are useful whenever we reﬂectively translate objects to and
Line201 from other forms. Many serialization and mapping technologies have the same
Line202 advantages and difﬁculties as ORM. The mapping can be deﬁned by compact,
Line203 297
Line204 Testing That Objects Can Be Persisted
Line205 
Line206 
Line207 ---
