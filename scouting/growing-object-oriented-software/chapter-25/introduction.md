Line1 # Introduction (pp.289-290)
Line2 
Line3 ---
Line4 **Page 289**
Line5 
Line6 Chapter 25
Line7 Testing Persistence
Line8 It is always during a passing state of mind that we make lasting
Line9 resolutions.
Line10 —Marcel Proust
Line11 Introduction
Line12 As we saw in Chapter 8, when we deﬁne an abstraction in terms of a third-party
Line13 API, we have to test that our abstraction behaves as we expect when integrated
Line14 with that API, but cannot use our tests to get feedback about its design.
Line15 A common example is an abstraction implemented using a persistence mecha-
Line16 nism, such as Object/Relational Mapping (ORM). ORM hides a lot of sophisti-
Line17 cated functionality behind a simple API. When we build an abstraction upon an
Line18 ORM, we need to test that our implementation sends correct queries, has correctly
Line19 conﬁgured the mappings between our objects and the relational schema, uses a
Line20 dialect of SQL that is compatible with the database, performs updates and deletes
Line21 that are compatible with the integrity constraints of the database, interacts
Line22 correctly with the transaction manager, releases external resources in a timely
Line23 manner, does not trip over any bugs in the database driver, and much more.
Line24 When testing persistence code, we also have more to worry about with respect
Line25 to the quality of our tests. There are components running in the background that
Line26 the test must set up correctly. Those components have persistent state that could
Line27 make tests interfere with each other. Our test code has to deal with all this extra
Line28 complexity. We need to spend additional effort to ensure that our tests remain
Line29 readable and to generate reasonable diagnostics that pinpoint why tests fail—to
Line30 tell us in which component the failure occurred and why.
Line31 This chapter describes some techniques for dealing with this complexity. The
Line32 example code uses the standard Java Persistence API (JPA), but the techniques
Line33 will work just as well with other persistence mechanisms, such as Java Data
Line34 Objects (JDO), open source ORM technologies like Hibernate, or even when
Line35 dumping objects to ﬁles using a data-mapping mechanism such as XStream1 or
Line36 the standard Java API for XML Binding (JAXB).2
Line37 1. http://xstream.codehaus.org
Line38 2. Apologies for all the acronyms. The Java standardization process does not require
Line39 standards to have memorable names.
Line40 289
Line41 
Line42 
Line43 ---
Line44 
Line45 ---
Line46 **Page 290**
Line47 
Line48 An Example Scenario
Line49 The examples in this chapter will all use the same scenario. We now have a web
Line50 service that performs auction sniping on behalf of our customers.
Line51 A customer can log in to different auction sites and has one or more payment
Line52 methods by which they pay for our service and the lots they bid for. The system
Line53 supports two payment methods: credit cards and an online payment service called
Line54 PayMate. A customer has a contact address and, if they have a credit card, the
Line55 card has a billing address.
Line56 This domain model is represented in our system by the persistent entities shown
Line57 in Figure 25.1 (which only includes the ﬁelds that show what the purpose of the
Line58 entity is.)
Line59 Figure 25.1
Line60 Persistent entities
Line61 Isolate Tests That Affect Persistent State
Line62 Since persistent data hangs around from one test to the next, we have to take
Line63 extra care to ensure that persistence tests are isolated from one another. JUnit
Line64 cannot do this for us, so the test ﬁxture must ensure that the test starts with its
Line65 persistent resources in a known state.
Line66 For database code, this means deleting rows from the database tables before
Line67 the test starts. The process of cleaning the database depends on the database’s
Line68 integrity constraints. It might only be possible to clear tables in a strict order.
Line69 Furthermore, if some tables have foreign key constraints between them that
Line70 cascade deletes, cleaning one table will automatically clean others.
Line71 Chapter 25
Line72 Testing Persistence
Line73 290
Line74 
Line75 
Line76 ---
