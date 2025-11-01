Line1 # Make Tests Transaction Boundaries Explicit (pp.292-294)
Line2 
Line3 ---
Line4 **Page 292**
Line5 
Line6 We use an array, ENTITY_TYPES, to ensure that the entity types (and, therefore,
Line7 database tables) are cleaned in an order that does not violate referential integrity
Line8 when rows are deleted from the database.3 We add DatabaseCleaner to a setup
Line9 method, to initialize the database before each test. For example:
Line10 public class ExamplePersistenceTest {
Line11   final EntityManagerFactory factory = 
Line12                                 Persistence.createEntityManagerFactory("example");
Line13   final EntityManager entityManager = factory.createEntityManager();
Line14   @Before
Line15   public void cleanDatabase() throws Exception {
Line16 new DatabaseCleaner(entityManager).clean();
Line17   }
Line18 […]
Line19 }
Line20 For brevity, we won’t show this cleanup in the test examples. You should assume
Line21 that every persistence test starts with the database in a known, clean state.
Line22 Make Tests Transaction Boundaries Explicit
Line23 A common technique to isolate tests that use a transactional resource (such as a
Line24 database) is to run each test in a transaction which is then rolled back at the end
Line25 of the test. The idea is to leave the persistent state the same after the test as before.
Line26 The problem with this technique is that it doesn’t test what happens on commit,
Line27 which is a signiﬁcant event. The ORM ﬂushes the state of the objects it is man-
Line28 aging in memory to the database. The database, in turn, checks its integrity
Line29 constraints. A test that never commits does not fully exercise how the code under
Line30 test interacts with the database. Neither can it test interactions between distinct
Line31 transactions. Another disadvantage of rolling back is that the test discards data
Line32 that might be useful for diagnosing failures.
Line33 Tests should explicitly delineate transactions. We also prefer to make transac-
Line34 tion boundaries stand out, so they’re easy to see when reading the test. We usu-
Line35 ally extract transaction management into a subordinate object, called a transactor,
Line36 that runs a unit of work within a transaction. In this case, the transactor will
Line37 coordinate JPA transactions, so we call it a JPATransactor.4
Line38 3. We’ve left entityNameOf() out of this code excerpt. The JPA says the the name of an
Line39 entity is derived from its related Java class but doesn’t provide a standard API to do
Line40 so. We implemented just enough of this mapping to allow DatabaseCleaner to work.
Line41 4. In other systems, tests might also use a JMSTransactor for coordinating transactions
Line42 in a Java Messaging Service (JMS) broker, or a JTATransactor for coordinating
Line43 distributed transactions via the standard Java Transaction API (JTA).
Line44 Chapter 25
Line45 Testing Persistence
Line46 292
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 293**
Line53 
Line54 public interface UnitOfWork {
Line55   void work() throws Exception;
Line56 }
Line57 public class JPATransactor { 
Line58   private final EntityManager entityManager;
Line59   public JPATransactor(EntityManager entityManager) { 
Line60     this.entityManager = entityManager; 
Line61   } 
Line62   public void perform(UnitOfWork unitOfWork) throws Exception { 
Line63     EntityTransaction transaction = entityManager.getTransaction();
Line64     transaction.begin(); 
Line65     try { 
Line66       unitOfWork.work(); 
Line67       transaction.commit(); 
Line68     } 
Line69     catch (PersistenceException e) { 
Line70       throw e; 
Line71     } 
Line72     catch (Exception e) { 
Line73       transaction.rollback(); 
Line74       throw e; 
Line75     } 
Line76   } 
Line77 }
Line78 The transactor is called by passing in a UnitOfWork, usually created as an
Line79 anonymous class:
Line80 transactor.perform(new UnitOfWork() { 
Line81   public void work() throws Exception {
Line82     customers.addCustomer(aNewCustomer());
Line83   }
Line84 });
Line85 This pattern is so useful that we regularly use it in our production code as well.
Line86 We’ll show more of how the transactor is used in the next section.
Line87 “Container-Managed” Transactions
Line88 Many Java applications use declarative container-managed transactions, where
Line89 the application framework manages the application’s transaction boundaries.The
Line90 framework starts each transaction when it receives a request to an application
Line91 component, includes the application’s transactional resources in transaction, and
Line92 commits or rolls back the transaction when the request succeeds or fails. Java EE
Line93 is the canonical example of such frameworks in the Java world.
Line94 293
Line95 Make Tests Transaction Boundaries Explicit
Line96 
Line97 
Line98 ---
Line99 
Line100 ---
Line101 **Page 294**
Line102 
Line103 The techniques we describe in this chapter are compatible with this kind of
Line104 framework.We have used them to test applications built within Java EE and Spring,
Line105 and with “plain old” Java programs that use JPA, Hibernate, or JDBC directly.
Line106 The frameworks wrap transaction management around the objects that make
Line107 use of transactional resources, so there’s nothing in their code to mark the appli-
Line108 cation’s transaction boundaries. The tests for those objects, however, need to
Line109 manage transactions explicitly—which is what a transactor is for.
Line110 In the tests, the transactor uses the same transaction manager as the application,
Line111 conﬁgured in the same way. This ensures that the tests and the full application
Line112 run the same transactional code. It should make no difference whether a trans-
Line113 action is controlled by a block wrapped around our code by the framework, or by
Line114 a transactor in our tests. But if we’ve made a mistake and it does make a difference,
Line115 our end-to-end tests should catch such failures by exercising the application code
Line116 in the container.
Line117 Testing an Object That Performs Persistence Operations
Line118 Now that we’ve got some test scaffolding we can write tests for an object that
Line119 performs persistence.
Line120 In our domain model, a customer base represents all the customers we know
Line121 about. We can add customers to our customer base and ﬁnd customers that match
Line122 certain criteria. For example, we need to ﬁnd customers with credit cards that
Line123 are about to expire so that we can send them a reminder to update their payment
Line124 details.
Line125 public interface CustomerBase {  […]
Line126   void addCustomer(Customer customer);
Line127   List<Customer> customersWithExpiredCreditCardsAt(Date deadline);
Line128 }
Line129 When unit-testing code that calls a CustomerBase to ﬁnd and notify the
Line130 relevant customers, we can mock the interface. In a deployed system, however,
Line131 this code will call a real implementation of CustomerBase that is backed by JPA
Line132 to save and load customer information from a database. We must also test that
Line133 this persistent implementation works correctly—that the queries it makes and
Line134 the object/relational mappings are correct. For example, below is a test of the
Line135 customersWithExpiredCreditCardsAt() query. There are two helper methods
Line136 that interact with customerBase within a transaction: addCustomer() adds a set
Line137 of example customers, and assertCustomersExpiringOn() queries for customers
Line138 with expired cards.
Line139 Chapter 25
Line140 Testing Persistence
Line141 294
Line142 
Line143 
Line144 ---
