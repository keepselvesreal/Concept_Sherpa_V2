Line1 # Unit-Testing the Collaborating Objects (pp.18-19)
Line2 
Line3 ---
Line4 **Page 18**
Line5 
Line6 public class Train {
Line7   private final List<Carriage> carriages […]
Line8   private int percentReservedBarrier = 70;
Line9   public void reserveSeats(ReservationRequest request) {
Line10     for (Carriage carriage : carriages) {
Line11       if (carriage.getSeats().getPercentReserved() < percentReservedBarrier) {
Line12         request.reserveSeatsIn(carriage);
Line13         return;
Line14       }
Line15     }
Line16     request.cannotFindSeats();
Line17   }
Line18 }
Line19 We shouldn’t expose the internal structure of Carriage to implement this, not
Line20 least because there may be different types of carriages within a train. Instead, we
Line21 should ask the question we really want answered, instead of asking for the
Line22 information to help us ﬁgure out the answer ourselves:
Line23 public void reserveSeats(ReservationRequest request) {
Line24   for (Carriage carriage : carriages) {
Line25     if (carriage.hasSeatsAvailableWithin(percentReservedBarrier)) {
Line26       request.reserveSeatsIn(carriage);
Line27       return;
Line28     }
Line29   }
Line30   request.cannotFindSeats();
Line31 } 
Line32 Adding a query method moves the behavior to the most appropriate object,
Line33 gives it an explanatory name, and makes it easier to test.
Line34 We try to be sparing with queries on objects (as opposed to values) because
Line35 they can allow information to “leak” out of the object, making the system a little
Line36 bit more rigid. At a minimum, we make a point of writing queries that describe
Line37 the intention of the calling object, not just the implementation.
Line38 Unit-Testing the Collaborating Objects
Line39 We appear to have painted ourselves into a corner. We’re insisting on focused
Line40 objects that send commands to each other and don’t expose any way to query
Line41 their state, so it looks like we have nothing available to assert in a unit test. For
Line42 example, in Figure 2.4, the circled object will send messages to one or more of
Line43 its three neighbors when invoked. How can we test that it does so correctly
Line44 without exposing any of its internal state?
Line45 One option is to replace the target object’s neighbors in a test with substitutes,
Line46 or mock objects, as in Figure 2.5. We can specify how we expect the target object
Line47 to communicate with its mock neighbors for a triggering event; we call these
Line48 speciﬁcations expectations. During the test, the mock objects assert that they
Line49 Chapter 2
Line50 Test-Driven Development with Objects
Line51 18
Line52 
Line53 
Line54 ---
Line55 
Line56 ---
Line57 **Page 19**
Line58 
Line59 Figure 2.4
Line60 Unit-testing an object in isolation
Line61 Figure 2.5
Line62 Testing an object with mock objects
Line63 have been called as expected; they also implement any stubbed behavior needed
Line64 to make the rest of the test work.
Line65 With this infrastructure in place, we can change the way we approach TDD.
Line66 Figure 2.5 implies that we’re just trying to test the target object and that we al-
Line67 ready know what its neighbors look like. In practice, however, those collaborators
Line68 don’t need to exist when we’re writing a unit test. We can use the test to help us
Line69 tease out the supporting roles our object needs, deﬁned as Java interfaces, and
Line70 ﬁll in real implementations as we develop the rest of the system. We call this in-
Line71 terface discovery; you’ll see an example when we extract an AuctionEventListener
Line72 in Chapter 12.
Line73 Support for TDD with Mock Objects
Line74 To support this style of test-driven programming, we need to create mock in-
Line75 stances of the neighboring objects, deﬁne expectations on how they’re called and
Line76 then check them, and implement any stub behavior we need to get through the
Line77 test. In practice, the runtime structure of a test with mock objects usually looks
Line78 like Figure 2.6.
Line79 19
Line80 Support for TDD with Mock Objects
Line81 
Line82 
Line83 ---
