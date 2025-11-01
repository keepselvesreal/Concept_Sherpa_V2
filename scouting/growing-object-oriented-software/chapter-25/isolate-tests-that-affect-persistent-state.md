Line1 # Isolate Tests That Affect Persistent State (pp.290-292)
Line2 
Line3 ---
Line4 **Page 290**
Line5 
Line6 An Example Scenario
Line7 The examples in this chapter will all use the same scenario. We now have a web
Line8 service that performs auction sniping on behalf of our customers.
Line9 A customer can log in to different auction sites and has one or more payment
Line10 methods by which they pay for our service and the lots they bid for. The system
Line11 supports two payment methods: credit cards and an online payment service called
Line12 PayMate. A customer has a contact address and, if they have a credit card, the
Line13 card has a billing address.
Line14 This domain model is represented in our system by the persistent entities shown
Line15 in Figure 25.1 (which only includes the ﬁelds that show what the purpose of the
Line16 entity is.)
Line17 Figure 25.1
Line18 Persistent entities
Line19 Isolate Tests That Affect Persistent State
Line20 Since persistent data hangs around from one test to the next, we have to take
Line21 extra care to ensure that persistence tests are isolated from one another. JUnit
Line22 cannot do this for us, so the test ﬁxture must ensure that the test starts with its
Line23 persistent resources in a known state.
Line24 For database code, this means deleting rows from the database tables before
Line25 the test starts. The process of cleaning the database depends on the database’s
Line26 integrity constraints. It might only be possible to clear tables in a strict order.
Line27 Furthermore, if some tables have foreign key constraints between them that
Line28 cascade deletes, cleaning one table will automatically clean others.
Line29 Chapter 25
Line30 Testing Persistence
Line31 290
Line32 
Line33 
Line34 ---
Line35 
Line36 ---
Line37 **Page 291**
Line38 
Line39 Clean Up Persistent Data at the Start of a Test, Not at the End
Line40 Each test should initialize the persistent store to a known state when it starts.When
Line41 a test is run individually, it will leave data in the persistent store that can help you
Line42 diagnose test failures. When it is run as part of a suite, the next test will clean up
Line43 the persistent state ﬁrst, so tests will be isolated from each other. We used this
Line44 technique in “Recording the Failure” (page 221) when we cleared the log before
Line45 starting the application at the start of the test.
Line46 The order in which tables must be cleaned up should be captured in one place
Line47 because it must be kept up-to-date as the database schema evolves. It’s an ideal
Line48 candidate to be extracted into a subordinate object to be used by any test that
Line49 uses the database:
Line50 public class DatabaseCleaner {
Line51   private static final Class<?>[] ENTITY_TYPES = { 
Line52     Customer.class, 
Line53     PaymentMethod.class,
Line54     AuctionSiteCredentials.class,
Line55     AuctionSite.class,
Line56     Address.class
Line57   };
Line58   private final EntityManager entityManager;
Line59   public DatabaseCleaner(EntityManager entityManager) {
Line60     this.entityManager = entityManager;
Line61   }
Line62   public void clean() throws SQLException {
Line63     EntityTransaction transaction = entityManager.getTransaction();
Line64     transaction.begin();
Line65     for (Class<?> entityType : ENTITY_TYPES) {
Line66       deleteEntities(entityType);
Line67     }
Line68     transaction.commit();
Line69   }
Line70   private void deleteEntities(Class<?> entityType) {
Line71     entityManager
Line72       .createQuery("delete from " + entityNameOf(entityType)) 
Line73       .executeUpdate();
Line74   }
Line75 }
Line76 291
Line77 Isolate Tests That Affect Persistent State
Line78 
Line79 
Line80 ---
Line81 
Line82 ---
Line83 **Page 292**
Line84 
Line85 We use an array, ENTITY_TYPES, to ensure that the entity types (and, therefore,
Line86 database tables) are cleaned in an order that does not violate referential integrity
Line87 when rows are deleted from the database.3 We add DatabaseCleaner to a setup
Line88 method, to initialize the database before each test. For example:
Line89 public class ExamplePersistenceTest {
Line90   final EntityManagerFactory factory = 
Line91                                 Persistence.createEntityManagerFactory("example");
Line92   final EntityManager entityManager = factory.createEntityManager();
Line93   @Before
Line94   public void cleanDatabase() throws Exception {
Line95 new DatabaseCleaner(entityManager).clean();
Line96   }
Line97 […]
Line98 }
Line99 For brevity, we won’t show this cleanup in the test examples. You should assume
Line100 that every persistence test starts with the database in a known, clean state.
Line101 Make Tests Transaction Boundaries Explicit
Line102 A common technique to isolate tests that use a transactional resource (such as a
Line103 database) is to run each test in a transaction which is then rolled back at the end
Line104 of the test. The idea is to leave the persistent state the same after the test as before.
Line105 The problem with this technique is that it doesn’t test what happens on commit,
Line106 which is a signiﬁcant event. The ORM ﬂushes the state of the objects it is man-
Line107 aging in memory to the database. The database, in turn, checks its integrity
Line108 constraints. A test that never commits does not fully exercise how the code under
Line109 test interacts with the database. Neither can it test interactions between distinct
Line110 transactions. Another disadvantage of rolling back is that the test discards data
Line111 that might be useful for diagnosing failures.
Line112 Tests should explicitly delineate transactions. We also prefer to make transac-
Line113 tion boundaries stand out, so they’re easy to see when reading the test. We usu-
Line114 ally extract transaction management into a subordinate object, called a transactor,
Line115 that runs a unit of work within a transaction. In this case, the transactor will
Line116 coordinate JPA transactions, so we call it a JPATransactor.4
Line117 3. We’ve left entityNameOf() out of this code excerpt. The JPA says the the name of an
Line118 entity is derived from its related Java class but doesn’t provide a standard API to do
Line119 so. We implemented just enough of this mapping to allow DatabaseCleaner to work.
Line120 4. In other systems, tests might also use a JMSTransactor for coordinating transactions
Line121 in a Java Messaging Service (JMS) broker, or a JTATransactor for coordinating
Line122 distributed transactions via the standard Java Transaction API (JTA).
Line123 Chapter 25
Line124 Testing Persistence
Line125 292
Line126 
Line127 
Line128 ---
