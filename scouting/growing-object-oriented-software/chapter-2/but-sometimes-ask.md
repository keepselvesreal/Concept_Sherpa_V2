Line1 # But Sometimes Ask (pp.17-18)
Line2 
Line3 ---
Line4 **Page 17**
Line5 
Line6 Tell, Don’t Ask
Line7 We have objects sending each other messages, so what do they say? Our experi-
Line8 ence is that the calling object should describe what it wants in terms of the role
Line9 that its neighbor plays, and let the called object decide how to make that happen.
Line10 This is commonly known as the “Tell, Don’t Ask” style or, more formally, the
Line11 Law of Demeter. Objects make their decisions based only on the information
Line12 they hold internally or that which came with the triggering message; they avoid
Line13 navigating to other objects to make things happen. Followed consistently, this
Line14 style produces more ﬂexible code because it’s easy to swap objects that play the
Line15 same role. The caller sees nothing of their internal structure or the structure of
Line16 the rest of the system behind the role interface.
Line17 When we don’t follow the style, we can end up with what’s known as “train
Line18 wreck” code, where a series of getters is chained together like the carriages in a
Line19 train. Here’s one case we found on the Internet:
Line20 ((EditSaveCustomizer) master.getModelisable()
Line21   .getDockablePanel()
Line22     .getCustomizer())
Line23       .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
Line24 After some head scratching, we realized what this fragment was meant to say:
Line25 master.allowSavingOfCustomisations();
Line26 This wraps all that implementation detail up behind a single call. The client of
Line27 master no longer needs to know anything about the types in the chain. We’ve
Line28 reduced the risk that a design change might cause ripples in remote parts of the
Line29 codebase.
Line30 As well as hiding information, there’s a more subtle beneﬁt from “Tell, Don’t
Line31 Ask.” It forces us to make explicit and so name the interactions between objects,
Line32 rather than leaving them implicit in the chain of getters. The shorter version
Line33 above is much clearer about what it’s for, not just how it happens to be
Line34 implemented.
Line35 But Sometimes Ask
Line36 Of course we don’t “tell” everything;1 we “ask” when getting information from
Line37 values and collections, or when using a factory to create new objects. Occasion-
Line38 ally, we also ask objects about their state when searching or ﬁltering, but we still
Line39 want to maintain expressiveness and avoid “train wrecks.”
Line40 For example (to continue with the metaphor), if we naively wanted to spread
Line41 reserved seats out across the whole of a train, we might start with something like:
Line42 1. Although that’s an interesting exercise to try, to stretch your technique.
Line43 17
Line44 But Sometimes Ask
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 18**
Line51 
Line52 public class Train {
Line53   private final List<Carriage> carriages […]
Line54   private int percentReservedBarrier = 70;
Line55   public void reserveSeats(ReservationRequest request) {
Line56     for (Carriage carriage : carriages) {
Line57       if (carriage.getSeats().getPercentReserved() < percentReservedBarrier) {
Line58         request.reserveSeatsIn(carriage);
Line59         return;
Line60       }
Line61     }
Line62     request.cannotFindSeats();
Line63   }
Line64 }
Line65 We shouldn’t expose the internal structure of Carriage to implement this, not
Line66 least because there may be different types of carriages within a train. Instead, we
Line67 should ask the question we really want answered, instead of asking for the
Line68 information to help us ﬁgure out the answer ourselves:
Line69 public void reserveSeats(ReservationRequest request) {
Line70   for (Carriage carriage : carriages) {
Line71     if (carriage.hasSeatsAvailableWithin(percentReservedBarrier)) {
Line72       request.reserveSeatsIn(carriage);
Line73       return;
Line74     }
Line75   }
Line76   request.cannotFindSeats();
Line77 } 
Line78 Adding a query method moves the behavior to the most appropriate object,
Line79 gives it an explanatory name, and makes it easier to test.
Line80 We try to be sparing with queries on objects (as opposed to values) because
Line81 they can allow information to “leak” out of the object, making the system a little
Line82 bit more rigid. At a minimum, we make a point of writing queries that describe
Line83 the intention of the calling object, not just the implementation.
Line84 Unit-Testing the Collaborating Objects
Line85 We appear to have painted ourselves into a corner. We’re insisting on focused
Line86 objects that send commands to each other and don’t expose any way to query
Line87 their state, so it looks like we have nothing available to assert in a unit test. For
Line88 example, in Figure 2.4, the circled object will send messages to one or more of
Line89 its three neighbors when invoked. How can we test that it does so correctly
Line90 without exposing any of its internal state?
Line91 One option is to replace the target object’s neighbors in a test with substitutes,
Line92 or mock objects, as in Figure 2.5. We can specify how we expect the target object
Line93 to communicate with its mock neighbors for a triggering event; we call these
Line94 speciﬁcations expectations. During the test, the mock objects assert that they
Line95 Chapter 2
Line96 Test-Driven Development with Objects
Line97 18
Line98 
Line99 
Line100 ---
