Line1 # But Database Tests Are S-l-o-w! (pp.300-300)
Line2 
Line3 ---
Line4 **Page 300**
Line5 
Line6 The ﬁx is to make sure that there’s a persisted AuctionSite before we save a
Line7 new AuctionSiteCredentials. The AuctionSiteCredentialsBuilder delegates
Line8 to another builder to create the AuctionSite for the AuctionSiteCredentials
Line9 under construction (see “Combining Builders” on page 261). We ensure referential
Line10 integrity by wrapping the AuctionSite builder in a Decorator [Gamma94] that
Line11 persists the AuctionSite before it is associated with the AuctionSiteCredentials.
Line12 This is why we call the entity builder within a transaction—some of the related
Line13 builders will perform database operations that require an active transaction.
Line14 public class PersistabilityTest { […]
Line15   final List<? extends Builder<?>> persistentObjectBuilders = Arrays.asList(
Line16   new AddressBuilder(),
Line17   new PayMateDetailsBuilder(),
Line18   new CreditCardDetailsBuilder(),
Line19   new AuctionSiteBuilder(),
Line20   new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())),
Line21   new CustomerBuilder()
Line22     .usingAuctionSites(
Line23       new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())))
Line24     .withPaymentMethods(
Line25       new CreditCardDetailsBuilder(),
Line26       new PayMateDetailsBuilder()));
Line27   private <T> Builder<T> persisted(final Builder<T> builder) {
Line28     return new Builder<T>() {
Line29       public T build() {
Line30         T entity = builder.build();
Line31         entityManager.persist(entity);
Line32         return entity;
Line33       }
Line34     };    
Line35   }
Line36 }
Line37 But Database Tests Are S-l-o-w!
Line38 Tests that run against realistic infrastructure are much slower than unit tests that
Line39 run everything in memory. We can unit-test our code by deﬁning a clean interface
Line40 to the persistence infrastructure (deﬁned in terms of our code’s domain) and using
Line41 a mock persistence implementation—as we described in “Only Mock Types That
Line42 You Own” (page 69). We then test the implementation of this interface with
Line43 ﬁne-grained integration tests so we don’t have to bring up the entire system to
Line44 test the technical layers.
Line45 This lets us organize our tests into a chain of phases: unit tests that run very
Line46 quickly in memory; slower integration tests that reach outside the process, usually
Line47 through third-party APIs, and that depend on the conﬁguration of external services
Line48 such as databases and messaging brokers; and, ﬁnally, end-to-end tests that run
Line49 against a system packaged and deployed into a production-like environment.
Line50 This gives us rapid feedback if we break the application’s core logic, and incre-
Line51 mental feedback about integration at increasingly coarse levels of granularity.
Line52 Chapter 25
Line53 Testing Persistence
Line54 300
