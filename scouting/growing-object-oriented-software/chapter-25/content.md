# Chapter 25: Testing Persistence (pp.289-300)

---
**Page 289**

Chapter 25
Testing Persistence
It is always during a passing state of mind that we make lasting
resolutions.
—Marcel Proust
Introduction
As we saw in Chapter 8, when we deﬁne an abstraction in terms of a third-party
API, we have to test that our abstraction behaves as we expect when integrated
with that API, but cannot use our tests to get feedback about its design.
A common example is an abstraction implemented using a persistence mecha-
nism, such as Object/Relational Mapping (ORM). ORM hides a lot of sophisti-
cated functionality behind a simple API. When we build an abstraction upon an
ORM, we need to test that our implementation sends correct queries, has correctly
conﬁgured the mappings between our objects and the relational schema, uses a
dialect of SQL that is compatible with the database, performs updates and deletes
that are compatible with the integrity constraints of the database, interacts
correctly with the transaction manager, releases external resources in a timely
manner, does not trip over any bugs in the database driver, and much more.
When testing persistence code, we also have more to worry about with respect
to the quality of our tests. There are components running in the background that
the test must set up correctly. Those components have persistent state that could
make tests interfere with each other. Our test code has to deal with all this extra
complexity. We need to spend additional effort to ensure that our tests remain
readable and to generate reasonable diagnostics that pinpoint why tests fail—to
tell us in which component the failure occurred and why.
This chapter describes some techniques for dealing with this complexity. The
example code uses the standard Java Persistence API (JPA), but the techniques
will work just as well with other persistence mechanisms, such as Java Data
Objects (JDO), open source ORM technologies like Hibernate, or even when
dumping objects to ﬁles using a data-mapping mechanism such as XStream1 or
the standard Java API for XML Binding (JAXB).2
1. http://xstream.codehaus.org
2. Apologies for all the acronyms. The Java standardization process does not require
standards to have memorable names.
289


---
**Page 290**

An Example Scenario
The examples in this chapter will all use the same scenario. We now have a web
service that performs auction sniping on behalf of our customers.
A customer can log in to different auction sites and has one or more payment
methods by which they pay for our service and the lots they bid for. The system
supports two payment methods: credit cards and an online payment service called
PayMate. A customer has a contact address and, if they have a credit card, the
card has a billing address.
This domain model is represented in our system by the persistent entities shown
in Figure 25.1 (which only includes the ﬁelds that show what the purpose of the
entity is.)
Figure 25.1
Persistent entities
Isolate Tests That Affect Persistent State
Since persistent data hangs around from one test to the next, we have to take
extra care to ensure that persistence tests are isolated from one another. JUnit
cannot do this for us, so the test ﬁxture must ensure that the test starts with its
persistent resources in a known state.
For database code, this means deleting rows from the database tables before
the test starts. The process of cleaning the database depends on the database’s
integrity constraints. It might only be possible to clear tables in a strict order.
Furthermore, if some tables have foreign key constraints between them that
cascade deletes, cleaning one table will automatically clean others.
Chapter 25
Testing Persistence
290


---
**Page 291**

Clean Up Persistent Data at the Start of a Test, Not at the End
Each test should initialize the persistent store to a known state when it starts.When
a test is run individually, it will leave data in the persistent store that can help you
diagnose test failures. When it is run as part of a suite, the next test will clean up
the persistent state ﬁrst, so tests will be isolated from each other. We used this
technique in “Recording the Failure” (page 221) when we cleared the log before
starting the application at the start of the test.
The order in which tables must be cleaned up should be captured in one place
because it must be kept up-to-date as the database schema evolves. It’s an ideal
candidate to be extracted into a subordinate object to be used by any test that
uses the database:
public class DatabaseCleaner {
  private static final Class<?>[] ENTITY_TYPES = { 
    Customer.class, 
    PaymentMethod.class,
    AuctionSiteCredentials.class,
    AuctionSite.class,
    Address.class
  };
  private final EntityManager entityManager;
  public DatabaseCleaner(EntityManager entityManager) {
    this.entityManager = entityManager;
  }
  public void clean() throws SQLException {
    EntityTransaction transaction = entityManager.getTransaction();
    transaction.begin();
    for (Class<?> entityType : ENTITY_TYPES) {
      deleteEntities(entityType);
    }
    transaction.commit();
  }
  private void deleteEntities(Class<?> entityType) {
    entityManager
      .createQuery("delete from " + entityNameOf(entityType)) 
      .executeUpdate();
  }
}
291
Isolate Tests That Affect Persistent State


---
**Page 292**

We use an array, ENTITY_TYPES, to ensure that the entity types (and, therefore,
database tables) are cleaned in an order that does not violate referential integrity
when rows are deleted from the database.3 We add DatabaseCleaner to a setup
method, to initialize the database before each test. For example:
public class ExamplePersistenceTest {
  final EntityManagerFactory factory = 
                                Persistence.createEntityManagerFactory("example");
  final EntityManager entityManager = factory.createEntityManager();
  @Before
  public void cleanDatabase() throws Exception {
new DatabaseCleaner(entityManager).clean();
  }
[…]
}
For brevity, we won’t show this cleanup in the test examples. You should assume
that every persistence test starts with the database in a known, clean state.
Make Tests Transaction Boundaries Explicit
A common technique to isolate tests that use a transactional resource (such as a
database) is to run each test in a transaction which is then rolled back at the end
of the test. The idea is to leave the persistent state the same after the test as before.
The problem with this technique is that it doesn’t test what happens on commit,
which is a signiﬁcant event. The ORM ﬂushes the state of the objects it is man-
aging in memory to the database. The database, in turn, checks its integrity
constraints. A test that never commits does not fully exercise how the code under
test interacts with the database. Neither can it test interactions between distinct
transactions. Another disadvantage of rolling back is that the test discards data
that might be useful for diagnosing failures.
Tests should explicitly delineate transactions. We also prefer to make transac-
tion boundaries stand out, so they’re easy to see when reading the test. We usu-
ally extract transaction management into a subordinate object, called a transactor,
that runs a unit of work within a transaction. In this case, the transactor will
coordinate JPA transactions, so we call it a JPATransactor.4
3. We’ve left entityNameOf() out of this code excerpt. The JPA says the the name of an
entity is derived from its related Java class but doesn’t provide a standard API to do
so. We implemented just enough of this mapping to allow DatabaseCleaner to work.
4. In other systems, tests might also use a JMSTransactor for coordinating transactions
in a Java Messaging Service (JMS) broker, or a JTATransactor for coordinating
distributed transactions via the standard Java Transaction API (JTA).
Chapter 25
Testing Persistence
292


---
**Page 293**

public interface UnitOfWork {
  void work() throws Exception;
}
public class JPATransactor { 
  private final EntityManager entityManager;
  public JPATransactor(EntityManager entityManager) { 
    this.entityManager = entityManager; 
  } 
  public void perform(UnitOfWork unitOfWork) throws Exception { 
    EntityTransaction transaction = entityManager.getTransaction();
    transaction.begin(); 
    try { 
      unitOfWork.work(); 
      transaction.commit(); 
    } 
    catch (PersistenceException e) { 
      throw e; 
    } 
    catch (Exception e) { 
      transaction.rollback(); 
      throw e; 
    } 
  } 
}
The transactor is called by passing in a UnitOfWork, usually created as an
anonymous class:
transactor.perform(new UnitOfWork() { 
  public void work() throws Exception {
    customers.addCustomer(aNewCustomer());
  }
});
This pattern is so useful that we regularly use it in our production code as well.
We’ll show more of how the transactor is used in the next section.
“Container-Managed” Transactions
Many Java applications use declarative container-managed transactions, where
the application framework manages the application’s transaction boundaries.The
framework starts each transaction when it receives a request to an application
component, includes the application’s transactional resources in transaction, and
commits or rolls back the transaction when the request succeeds or fails. Java EE
is the canonical example of such frameworks in the Java world.
293
Make Tests Transaction Boundaries Explicit


---
**Page 294**

The techniques we describe in this chapter are compatible with this kind of
framework.We have used them to test applications built within Java EE and Spring,
and with “plain old” Java programs that use JPA, Hibernate, or JDBC directly.
The frameworks wrap transaction management around the objects that make
use of transactional resources, so there’s nothing in their code to mark the appli-
cation’s transaction boundaries. The tests for those objects, however, need to
manage transactions explicitly—which is what a transactor is for.
In the tests, the transactor uses the same transaction manager as the application,
conﬁgured in the same way. This ensures that the tests and the full application
run the same transactional code. It should make no difference whether a trans-
action is controlled by a block wrapped around our code by the framework, or by
a transactor in our tests. But if we’ve made a mistake and it does make a difference,
our end-to-end tests should catch such failures by exercising the application code
in the container.
Testing an Object That Performs Persistence Operations
Now that we’ve got some test scaffolding we can write tests for an object that
performs persistence.
In our domain model, a customer base represents all the customers we know
about. We can add customers to our customer base and ﬁnd customers that match
certain criteria. For example, we need to ﬁnd customers with credit cards that
are about to expire so that we can send them a reminder to update their payment
details.
public interface CustomerBase {  […]
  void addCustomer(Customer customer);
  List<Customer> customersWithExpiredCreditCardsAt(Date deadline);
}
When unit-testing code that calls a CustomerBase to ﬁnd and notify the
relevant customers, we can mock the interface. In a deployed system, however,
this code will call a real implementation of CustomerBase that is backed by JPA
to save and load customer information from a database. We must also test that
this persistent implementation works correctly—that the queries it makes and
the object/relational mappings are correct. For example, below is a test of the
customersWithExpiredCreditCardsAt() query. There are two helper methods
that interact with customerBase within a transaction: addCustomer() adds a set
of example customers, and assertCustomersExpiringOn() queries for customers
with expired cards.
Chapter 25
Testing Persistence
294


---
**Page 295**

public class PersistentCustomerBaseTest { […]
  final PersistentCustomerBase customerBase = 
                                 new PersistentCustomerBase(entityManager);
  @Test
  @SuppressWarnings("unchecked")
  public void findsCustomersWithCreditCardsThatAreAboutToExpire() throws Exception {
    final String deadline = "6 Jun 2009";
    addCustomers(
      aCustomer().withName("Alice (Expired)")
        .withPaymentMethods(aCreditCard().withExpiryDate(date("1 Jan 2009"))),
      aCustomer().withName("Bob (Expired)")
        .withPaymentMethods(aCreditCard().withExpiryDate(date("5 Jun 2009"))),
      aCustomer().withName("Carol (Valid)")
        .withPaymentMethods(aCreditCard().withExpiryDate(date(deadline))),
      aCustomer().withName("Dave (Valid)")
        .withPaymentMethods(aCreditCard().withExpiryDate(date("7 Jun 2009")))
    );
    assertCustomersExpiringOn(date(deadline), 
                              containsInAnyOrder(customerNamed("Alice (Expired)"), 
                                                 customerNamed("Bob (Expired)")));
  }
  private void addCustomers(final CustomerBuilder... customers) throws Exception {
transactor.perform(new UnitOfWork() {
      public void work() throws Exception {
        for (CustomerBuilder customer : customers) { 
customerBase.addCustomer(customer.build());
        }
      }
    });
  }
  private void assertCustomersExpiringOn(final Date date, 
                                         final Matcher<Iterable<Customer>> matcher)
    throws Exception 
  {
transactor.perform(new UnitOfWork() {
      public void work() throws Exception {
        assertThat(customerBase.customersWithExpiredCreditCardsAsOf(date), matcher);
      }
    });
  }
}
We call addCustomers() with CustomerBuilders set up to include a name and
an expiry date for the credit card. The expiry date is the signiﬁcant ﬁeld for this
test, so we create customers with expiry dates before, on, and after the deadline to
demonstrate the boundary condition. We also set the name of each customer
to identify the instances in a failure (notice that the names self-describe the relevant
status of each customer). An alternative to matching on name would have been
to use each object’s persistence identiﬁer, which is assigned by JPA. That would
have been more complex to work with (it’s not exposed as a property on
Customer), and would not be self-describing.
295
Testing an Object That Performs Persistence Operations


---
**Page 296**

The assertCustomersExpiringOn() method runs the query we’re testing for
the given deadline and checks that the result conforms to the Hamcrest matcher
we pass in. The containsInAnyOrder() method returns a matcher that checks
that there’s a sub-matcher for each of the elements in a collection. We’ve written
a customerNamed() method to return a custom matcher that tests whether an
object is a Customer with a given name (there’s more on custom matchers in
Appendix B). So, this test says that we expect to receive back exactly two Customer
objects, named "Alice (Expired)" and "Bob (Expired)".
The test implicitly exercises CustomerBase.addCustomer() by calling it to set
up the database for the query. Thinking further, what we actually care about is
the relationship between the result of calling addCustomer() and subsequent
queries, so we probably won’t test addCustomer() independently. If there’s an
effect of addCustomer() that is not visible through some feature of the system,
then we’d have to ask some hard questions about its purpose before writing a
special test query to cover it.
Better Test Structure with Matchers
This test includes a nice example of using Hamcrest to create a clean test structure.
The test method constructs a matcher, which gives a concise description of a valid
result for the query. It passes the matcher to assertCustomersExpiringOn(),
which just runs the query and passes the result to the matcher. We have a clean
separation between the test method, which knows what is expected to be retrieved,
and the query/assert method, which knows how to make a query and can be used
in other tests.
Here is an implementation of PersistentCustomerBase that passes the test:
public class PersistentCustomerBase implements CustomerBase {
  private final EntityManager entityManager;
  public PersistentCustomerBase(EntityManager entityManager) {
    this.entityManager = entityManager;
  }
  public void addCustomer(Customer customer) {
    entityManager.persist(customer);
  }
  public List<Customer> customersWithExpiredCreditCardsAt(Date deadline) {
    Query query = entityManager.createQuery(
        "select c from Customer c, CreditCardDetails d " +
        "where d member of c.paymentMethods " +
        "  and d.expiryDate < :deadline");
    query.setParameter("deadline", deadline);
    return query.getResultList();
  }
}
Chapter 25
Testing Persistence
296


---
**Page 297**

This implementation looks trivial—it’s so much shorter than its test—but it
relies on a lot of XML conﬁguration that we haven’t included and on a third-party
framework that implements the EntityManager’s simple API.
On Patterns and Type Names
The CustomerBase interface and PersistentCustomerBase class implement the
repository or data access object pattern (often abbreviated to DAO).We have not
used the terms “Repository,” “DataAccessObject,” or “DAO” in the name of the
interface or class that implements it because:
•
Using such terms leaks knowledge about the underlying technology layers
(persistence) into the application domain, and so breaks the “ports and
adapters” architecture.The objects that use a CustomerBase are persistence-
agnostic: they do not care whether the Customer objects they interact with
are written to disk or not.The Customer objects are also persistence-agnostic:
a program does not need to have a database to create and use Customer
objects. Only PersistentCustomerBase knows how it maps Customer objects
in and out of persistent storage.
•
We prefer not to name classes or interfaces after patterns; what matters
to us is their relationship to other classes in the system. The clients of
CustomerBase do not care what patterns it uses. As the system evolves, we
might make the CustomerBase class work in some other way and the name
would then be misleading.
•
We avoid generic words like “data,” “object,” or “access” in type names.We
try to give each class a name that identiﬁes a concept within its domain or
expresses how it bridges between the application and technical domains.
Testing That Objects Can Be Persisted
The PersistentCustomerBase relies on so much conﬁguration and underlying
third-party code that the error messages from its test can be difﬁcult to diagnose.
A test failure could be caused by a defect in a query, the mapping of the Customer
class, the mapping of any of the classes that it uses, the conﬁguration of the ORM,
invalid database connection parameters, or a misconﬁguration of the database
itself.
We can write more tests to help us pinpoint the cause of a persistence failure
when it occurs. A useful test is to “round-trip” instances of all persistent entity
types through the database to check that the mappings are conﬁgured correctly
for each class.
Round-trip tests are useful whenever we reﬂectively translate objects to and
from other forms. Many serialization and mapping technologies have the same
advantages and difﬁculties as ORM. The mapping can be deﬁned by compact,
297
Testing That Objects Can Be Persisted


---
**Page 298**

declarative code or conﬁguration, but misconﬁguration creates defects that are
difﬁcult to diagnose. We use round-trip tests so we can quickly identify the cause
of such defects.
Round-Tripping Persistent Objects
We can use a list of “test data builders” (page 257) to represent the persistent
entity types. This makes it easy for the test to instantiate each instance. We can
also use builder types more than once, with differing set-ups, to create entities
for round-tripping in different states or with different relationships to other
entities.
This test loops through a list of builders (we’ll show how we create
the list in a moment). For each builder, it creates and persists an entity in
one transaction, and retrieves and compares the result in another. As in the
last test, we have two
transactor methods that perform transactions.
The setup method is persistedObjectFrom() and the query method is
assertReloadsWithSameStateAs().
public class PersistabilityTest { […]
  final List<? extends Builder<?>> persistentObjectBuilders = […]
  @Test public void roundTripsPersistentObjects() throws Exception {
    for (Builder<?> builder : persistentObjectBuilders) {
      assertCanBePersisted(builder);
    }
  }
  private void assertCanBePersisted(Builder<?> builder) throws Exception {
    try {
      assertReloadsWithSameStateAs(persistedObjectFrom(builder));
    } catch (PersistenceException e) {
      throw new PersistenceException("could not round-trip " + typeNameFor(builder), e);
    }
  }
  private Object persistedObjectFrom(final Builder<?> builder) throws Exception {
    return transactor.performQuery(new QueryUnitOfWork() {
      public Object query() throws Exception {
        Object original = builder.build(); 
        entityManager.persist(original); 
        return original; 
      }
    });
  }
  private void assertReloadsWithSameStateAs(final Object original) throws Exception {
transactor.perform(new UnitOfWork() {
      public void work() throws Exception {
        assertThat(entityManager.find(original.getClass(), idOf(original));  
                   hasSamePersistenFieldsAs(original)); 
      }
    });
  }
Chapter 25
Testing Persistence
298


---
**Page 299**

  private String typeNameFor(Builder<?> builder) {
    return builder.getClass().getSimpleName().replace("Builder", "");
  }
}
The persistedObjectFrom() method asks its given builder to create an entity
instance which it persists within a transaction. Then it returns the new instance
to the test, for later comparison; QueryUnitOfWork is a variant of UnitOfWork that
allows us to return a value from a transaction.
The assertReloadsWithSameStateAs() method extracts the persistence identiﬁer
that the EntityManager assigned to the expected object (using reﬂection), and
uses that identiﬁer to ask the EntityManager to retrieve another copy of the entity
from the database. Then it calls a custom matcher that uses reﬂection to check
that the two copies of the entity have the same values in their persistent ﬁelds.
On the Use of Reﬂection
We have repeatedly stated that we should test through an object’s public API, so
that our tests give us useful feedback about the design of that API. So, why are
we using reﬂection here to bypass our objects’ encapsulation boundaries and
reach into their private state? Why are we using the persistence API in a way we
wouldn’t do in production code?
We’re using these round-trip tests to test-drive the conﬁguration of the ORM, as
it maps our objects into the database. We’re not test-driving the design of the ob-
jects themselves. The state of our objects is encapsulated and hidden from other
objects in the system. The ORM uses reﬂection to save that state to, and retrieve
it from, the database—so here, we use the same technique as the ORM does to
verify its behavior.
Round-Tripping Related Entities
Creating a list of builders is complicated when there are relationships between
entities, and saving of one entity is not cascaded to its related entities. This is the
case when an entity refers to reference data that is never created during a
transaction.
For example, our system knows about a limited number of auction sites. Cus-
tomers have AuctionSiteCredentials that refer to those sites. When the system
creates a Customer entity, it associates it with existing AuctionSites that it loads
from the database. Saving the Customer will save its AuctionSiteCredentials,
but won’t save the referenced AuctionSites because they should already exist in
the database. At the same time, we must associate a new AuctionSiteCredentials
with an AuctionSite that is already in the database, or we will violate referential
integrity constraints when we save.
299
Testing That Objects Can Be Persisted


---
**Page 300**

The ﬁx is to make sure that there’s a persisted AuctionSite before we save a
new AuctionSiteCredentials. The AuctionSiteCredentialsBuilder delegates
to another builder to create the AuctionSite for the AuctionSiteCredentials
under construction (see “Combining Builders” on page 261). We ensure referential
integrity by wrapping the AuctionSite builder in a Decorator [Gamma94] that
persists the AuctionSite before it is associated with the AuctionSiteCredentials.
This is why we call the entity builder within a transaction—some of the related
builders will perform database operations that require an active transaction.
public class PersistabilityTest { […]
  final List<? extends Builder<?>> persistentObjectBuilders = Arrays.asList(
  new AddressBuilder(),
  new PayMateDetailsBuilder(),
  new CreditCardDetailsBuilder(),
  new AuctionSiteBuilder(),
  new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())),
  new CustomerBuilder()
    .usingAuctionSites(
      new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())))
    .withPaymentMethods(
      new CreditCardDetailsBuilder(),
      new PayMateDetailsBuilder()));
  private <T> Builder<T> persisted(final Builder<T> builder) {
    return new Builder<T>() {
      public T build() {
        T entity = builder.build();
        entityManager.persist(entity);
        return entity;
      }
    };    
  }
}
But Database Tests Are S-l-o-w!
Tests that run against realistic infrastructure are much slower than unit tests that
run everything in memory. We can unit-test our code by deﬁning a clean interface
to the persistence infrastructure (deﬁned in terms of our code’s domain) and using
a mock persistence implementation—as we described in “Only Mock Types That
You Own” (page 69). We then test the implementation of this interface with
ﬁne-grained integration tests so we don’t have to bring up the entire system to
test the technical layers.
This lets us organize our tests into a chain of phases: unit tests that run very
quickly in memory; slower integration tests that reach outside the process, usually
through third-party APIs, and that depend on the conﬁguration of external services
such as databases and messaging brokers; and, ﬁnally, end-to-end tests that run
against a system packaged and deployed into a production-like environment.
This gives us rapid feedback if we break the application’s core logic, and incre-
mental feedback about integration at increasingly coarse levels of granularity.
Chapter 25
Testing Persistence
300


