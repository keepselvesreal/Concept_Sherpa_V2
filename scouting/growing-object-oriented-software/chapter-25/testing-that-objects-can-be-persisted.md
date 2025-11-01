Line1 # Testing That Objects Can Be Persisted (pp.297-300)
Line2 
Line3 ---
Line4 **Page 297**
Line5 
Line6 This implementation looks trivial—it’s so much shorter than its test—but it
Line7 relies on a lot of XML conﬁguration that we haven’t included and on a third-party
Line8 framework that implements the EntityManager’s simple API.
Line9 On Patterns and Type Names
Line10 The CustomerBase interface and PersistentCustomerBase class implement the
Line11 repository or data access object pattern (often abbreviated to DAO).We have not
Line12 used the terms “Repository,” “DataAccessObject,” or “DAO” in the name of the
Line13 interface or class that implements it because:
Line14 •
Line15 Using such terms leaks knowledge about the underlying technology layers
Line16 (persistence) into the application domain, and so breaks the “ports and
Line17 adapters” architecture.The objects that use a CustomerBase are persistence-
Line18 agnostic: they do not care whether the Customer objects they interact with
Line19 are written to disk or not.The Customer objects are also persistence-agnostic:
Line20 a program does not need to have a database to create and use Customer
Line21 objects. Only PersistentCustomerBase knows how it maps Customer objects
Line22 in and out of persistent storage.
Line23 •
Line24 We prefer not to name classes or interfaces after patterns; what matters
Line25 to us is their relationship to other classes in the system. The clients of
Line26 CustomerBase do not care what patterns it uses. As the system evolves, we
Line27 might make the CustomerBase class work in some other way and the name
Line28 would then be misleading.
Line29 •
Line30 We avoid generic words like “data,” “object,” or “access” in type names.We
Line31 try to give each class a name that identiﬁes a concept within its domain or
Line32 expresses how it bridges between the application and technical domains.
Line33 Testing That Objects Can Be Persisted
Line34 The PersistentCustomerBase relies on so much conﬁguration and underlying
Line35 third-party code that the error messages from its test can be difﬁcult to diagnose.
Line36 A test failure could be caused by a defect in a query, the mapping of the Customer
Line37 class, the mapping of any of the classes that it uses, the conﬁguration of the ORM,
Line38 invalid database connection parameters, or a misconﬁguration of the database
Line39 itself.
Line40 We can write more tests to help us pinpoint the cause of a persistence failure
Line41 when it occurs. A useful test is to “round-trip” instances of all persistent entity
Line42 types through the database to check that the mappings are conﬁgured correctly
Line43 for each class.
Line44 Round-trip tests are useful whenever we reﬂectively translate objects to and
Line45 from other forms. Many serialization and mapping technologies have the same
Line46 advantages and difﬁculties as ORM. The mapping can be deﬁned by compact,
Line47 297
Line48 Testing That Objects Can Be Persisted
Line49 
Line50 
Line51 ---
Line52 
Line53 ---
Line54 **Page 298**
Line55 
Line56 declarative code or conﬁguration, but misconﬁguration creates defects that are
Line57 difﬁcult to diagnose. We use round-trip tests so we can quickly identify the cause
Line58 of such defects.
Line59 Round-Tripping Persistent Objects
Line60 We can use a list of “test data builders” (page 257) to represent the persistent
Line61 entity types. This makes it easy for the test to instantiate each instance. We can
Line62 also use builder types more than once, with differing set-ups, to create entities
Line63 for round-tripping in different states or with different relationships to other
Line64 entities.
Line65 This test loops through a list of builders (we’ll show how we create
Line66 the list in a moment). For each builder, it creates and persists an entity in
Line67 one transaction, and retrieves and compares the result in another. As in the
Line68 last test, we have two
Line69 transactor methods that perform transactions.
Line70 The setup method is persistedObjectFrom() and the query method is
Line71 assertReloadsWithSameStateAs().
Line72 public class PersistabilityTest { […]
Line73   final List<? extends Builder<?>> persistentObjectBuilders = […]
Line74   @Test public void roundTripsPersistentObjects() throws Exception {
Line75     for (Builder<?> builder : persistentObjectBuilders) {
Line76       assertCanBePersisted(builder);
Line77     }
Line78   }
Line79   private void assertCanBePersisted(Builder<?> builder) throws Exception {
Line80     try {
Line81       assertReloadsWithSameStateAs(persistedObjectFrom(builder));
Line82     } catch (PersistenceException e) {
Line83       throw new PersistenceException("could not round-trip " + typeNameFor(builder), e);
Line84     }
Line85   }
Line86   private Object persistedObjectFrom(final Builder<?> builder) throws Exception {
Line87     return transactor.performQuery(new QueryUnitOfWork() {
Line88       public Object query() throws Exception {
Line89         Object original = builder.build(); 
Line90         entityManager.persist(original); 
Line91         return original; 
Line92       }
Line93     });
Line94   }
Line95   private void assertReloadsWithSameStateAs(final Object original) throws Exception {
Line96 transactor.perform(new UnitOfWork() {
Line97       public void work() throws Exception {
Line98         assertThat(entityManager.find(original.getClass(), idOf(original));  
Line99                    hasSamePersistenFieldsAs(original)); 
Line100       }
Line101     });
Line102   }
Line103 Chapter 25
Line104 Testing Persistence
Line105 298
Line106 
Line107 
Line108 ---
Line109 
Line110 ---
Line111 **Page 299**
Line112 
Line113 private String typeNameFor(Builder<?> builder) {
Line114     return builder.getClass().getSimpleName().replace("Builder", "");
Line115   }
Line116 }
Line117 The persistedObjectFrom() method asks its given builder to create an entity
Line118 instance which it persists within a transaction. Then it returns the new instance
Line119 to the test, for later comparison; QueryUnitOfWork is a variant of UnitOfWork that
Line120 allows us to return a value from a transaction.
Line121 The assertReloadsWithSameStateAs() method extracts the persistence identiﬁer
Line122 that the EntityManager assigned to the expected object (using reﬂection), and
Line123 uses that identiﬁer to ask the EntityManager to retrieve another copy of the entity
Line124 from the database. Then it calls a custom matcher that uses reﬂection to check
Line125 that the two copies of the entity have the same values in their persistent ﬁelds.
Line126 On the Use of Reﬂection
Line127 We have repeatedly stated that we should test through an object’s public API, so
Line128 that our tests give us useful feedback about the design of that API. So, why are
Line129 we using reﬂection here to bypass our objects’ encapsulation boundaries and
Line130 reach into their private state? Why are we using the persistence API in a way we
Line131 wouldn’t do in production code?
Line132 We’re using these round-trip tests to test-drive the conﬁguration of the ORM, as
Line133 it maps our objects into the database. We’re not test-driving the design of the ob-
Line134 jects themselves. The state of our objects is encapsulated and hidden from other
Line135 objects in the system. The ORM uses reﬂection to save that state to, and retrieve
Line136 it from, the database—so here, we use the same technique as the ORM does to
Line137 verify its behavior.
Line138 Round-Tripping Related Entities
Line139 Creating a list of builders is complicated when there are relationships between
Line140 entities, and saving of one entity is not cascaded to its related entities. This is the
Line141 case when an entity refers to reference data that is never created during a
Line142 transaction.
Line143 For example, our system knows about a limited number of auction sites. Cus-
Line144 tomers have AuctionSiteCredentials that refer to those sites. When the system
Line145 creates a Customer entity, it associates it with existing AuctionSites that it loads
Line146 from the database. Saving the Customer will save its AuctionSiteCredentials,
Line147 but won’t save the referenced AuctionSites because they should already exist in
Line148 the database. At the same time, we must associate a new AuctionSiteCredentials
Line149 with an AuctionSite that is already in the database, or we will violate referential
Line150 integrity constraints when we save.
Line151 299
Line152 Testing That Objects Can Be Persisted
Line153 
Line154 
Line155 ---
Line156 
Line157 ---
Line158 **Page 300**
Line159 
Line160 The ﬁx is to make sure that there’s a persisted AuctionSite before we save a
Line161 new AuctionSiteCredentials. The AuctionSiteCredentialsBuilder delegates
Line162 to another builder to create the AuctionSite for the AuctionSiteCredentials
Line163 under construction (see “Combining Builders” on page 261). We ensure referential
Line164 integrity by wrapping the AuctionSite builder in a Decorator [Gamma94] that
Line165 persists the AuctionSite before it is associated with the AuctionSiteCredentials.
Line166 This is why we call the entity builder within a transaction—some of the related
Line167 builders will perform database operations that require an active transaction.
Line168 public class PersistabilityTest { […]
Line169   final List<? extends Builder<?>> persistentObjectBuilders = Arrays.asList(
Line170   new AddressBuilder(),
Line171   new PayMateDetailsBuilder(),
Line172   new CreditCardDetailsBuilder(),
Line173   new AuctionSiteBuilder(),
Line174   new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())),
Line175   new CustomerBuilder()
Line176     .usingAuctionSites(
Line177       new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())))
Line178     .withPaymentMethods(
Line179       new CreditCardDetailsBuilder(),
Line180       new PayMateDetailsBuilder()));
Line181   private <T> Builder<T> persisted(final Builder<T> builder) {
Line182     return new Builder<T>() {
Line183       public T build() {
Line184         T entity = builder.build();
Line185         entityManager.persist(entity);
Line186         return entity;
Line187       }
Line188     };    
Line189   }
Line190 }
Line191 But Database Tests Are S-l-o-w!
Line192 Tests that run against realistic infrastructure are much slower than unit tests that
Line193 run everything in memory. We can unit-test our code by deﬁning a clean interface
Line194 to the persistence infrastructure (deﬁned in terms of our code’s domain) and using
Line195 a mock persistence implementation—as we described in “Only Mock Types That
Line196 You Own” (page 69). We then test the implementation of this interface with
Line197 ﬁne-grained integration tests so we don’t have to bring up the entire system to
Line198 test the technical layers.
Line199 This lets us organize our tests into a chain of phases: unit tests that run very
Line200 quickly in memory; slower integration tests that reach outside the process, usually
Line201 through third-party APIs, and that depend on the conﬁguration of external services
Line202 such as databases and messaging brokers; and, ﬁnally, end-to-end tests that run
Line203 against a system packaged and deployed into a production-like environment.
Line204 This gives us rapid feedback if we break the application’s core logic, and incre-
Line205 mental feedback about integration at increasingly coarse levels of granularity.
Line206 Chapter 25
Line207 Testing Persistence
Line208 300
