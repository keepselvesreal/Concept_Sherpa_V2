Line1 # Precise Expectations (pp.277-284)
Line2 
Line3 ---
Line4 **Page 277**
Line5 
Line6 Precise Expectations
Line7 We can extend the concept of being precise about assertions to being precise
Line8 about expectations. Each mock object test should specify just the relevant details
Line9 of the interactions between the object under test and its neighbors. The combined
Line10 unit tests for an object describe its protocol for communicating with the rest of
Line11 the system.
Line12 We’ve built a lot of support into jMock for specifying this communication
Line13 between objects as precisely as it should be. The API is designed to produce tests
Line14 that clearly express how objects relate to each other and that are ﬂexible because
Line15 they’re not too restrictive. This may require a little more test code than some
Line16 of the alternatives, but we ﬁnd that the extra rigor keeps the tests clear.
Line17 Precise Parameter Matching
Line18 We want to be as precise about the values passed in to a method as we are about
Line19 the value it returns. For example, in “Assertions and Expectations” (page 254)
Line20 we showed an expectation where one of the accepted arguments was any type
Line21 of RuntimeException; the speciﬁc class doesn’t matter. Similarly, in “Extracting
Line22 the SnipersTableModel” (page 197), we have this expectation:
Line23 oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId)));
Line24 The method sniperForItem() returns a Matcher that checks only the item identiﬁer
Line25 when given an AuctionSniper. This test doesn’t care about anything else in the
Line26 sniper’s state, such as its current bid or last price, so we don’t make it more
Line27 brittle by checking those values.
Line28 The same precision can be applied to expecting input strings. If, for example,
Line29 we have an auditTrail object to accept the failure message we described
Line30 above, we can write a precise expectation for that auditing:
Line31 oneOf(auditTrail).recordFailure(with(allOf(containsString("strikePrice=92"),
Line32                                            containsString("id=FGD.430"), 
Line33                                            containsString("is expired")))); 
Line34 Allowances and Expectations
Line35 We introduced the concept of allowances in “The Sniper Acquires Some State”
Line36 (page 144). jMock insists that all expectations are met during a test, but al-
Line37 lowances may be matched or not. The point of the distinction is to highlight
Line38 what matters in a particular test. Expectations describe the interactions that are
Line39 essential to the protocol we’re testing: if we send this message to the object, we
Line40 expect to see it send this other message to this neighbor.
Line41 Allowances support the interaction we’re testing. We often use them as stubs
Line42 to feed values into the object, to get the object into the right state for the behavior
Line43 we want to test. We also use them to ignore other interactions that aren’t relevant
Line44 277
Line45 Precise Expectations
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 278**
Line52 
Line53 to the current test. For example, in “Repurposing sniperBidding()” we have a
Line54 test that includes:
Line55 ignoring(auction);
Line56 allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING))); 
Line57                                           then(sniperState.is("bidding"));
Line58 The ignoring() clause says that, in this test, we don’t care about messages
Line59 sent to the auction; they will be covered in other tests. The allowing() clause
Line60 matches any call to sniperStateChanged() with a Sniper that is currently bidding,
Line61 but doesn’t insist that such a call happens. In this test, we use the allowance to
Line62 record what the Sniper has told us about its state. The method aSniperThatIs()
Line63 returns a Matcher that checks only the SniperState when given a SniperSnapshot.
Line64 In other tests we attach “action” clauses to allowances, so that the call will
Line65 return a value or throw an exception. For example, we might have an allowance
Line66 that stubs the catalog to return a price that will be returned for use later in
Line67 the test:
Line68 allowing(catalog).getPriceForItem(item); will(returnValue(74));
Line69 The distinction between allowances and expectations isn’t rigid, but we’ve
Line70 found that this simple rule helps:
Line71 Allow Queries; Expect Commands
Line72 Commands are calls that are likely to have side effects, to change the world outside
Line73 the target object.When we tell the auditTrail above to record a failure, we expect
Line74 that to change the contents of some kind of log. The state of the system will be
Line75 different if we call the method a different number of times.
Line76 Queries don’t change the world, so they can be called any number of times, includ-
Line77 ing none. In our example above, it doesn’t make any difference to the system how
Line78 many times we ask the catalog for a price.
Line79 The rule helps to decouple the test from the tested object. If the implementation
Line80 changes, for example to introduce caching or use a different algorithm, the test
Line81 is still valid. On the other hand, if we were writing a test for a cache, we would
Line82 want to know exactly how often the query was made.
Line83 jMock supports more varied checking of how often a call is made than just
Line84 allowing() and oneOf(). The number of times a call is expected is deﬁned by the
Line85 “cardinality” clause that starts the expectation. In “The AuctionSniper Bids,”
Line86 we saw the example:
Line87 atLeast(1).of(sniperListener).sniperBidding();
Line88 Chapter 24
Line89 Test Flexibility
Line90 278
Line91 
Line92 
Line93 ---
Line94 
Line95 ---
Line96 **Page 279**
Line97 
Line98 which says that we care that this call is made, but not how many times. There
Line99 are other clauses which allow ﬁne-tuning of the number of times a call is expected,
Line100 listed in Appendix A.
Line101 Ignoring Irrelevant Objects
Line102 As you’ve seen, we can simplify a test by “ignoring” collaborators that are not
Line103 relevant to the functionality being exercised. jMock will not check any calls to
Line104 ignored objects. This keeps the test simple and focused, so we can immediately
Line105 see what’s important and changes to one aspect of the code do not break
Line106 unrelated tests.
Line107 As a convenience, jMock will provide “zero” results for ignored methods that
Line108 return a value, depending on the return type:
Line109 “Zero” value
Line110 Type
Line111 false
Line112 Boolean
Line113 0
Line114 Numeric type
Line115 "" (an empty string)
Line116 String
Line117 Empty array
Line118 Array
Line119 An ignored mock
Line120 A type that can be mocked by the Mockery
Line121 null
Line122 Any other type
Line123 The ability to dynamically mock returned types can be a powerful tool for
Line124 narrowing the scope of a test. For example, for code that uses the Java Persistence
Line125 API (JPA), a test can ignore the EntityManagerFactory. The factory will return
Line126 an ignored EntityManager, which will return an ignored EntityTransaction on
Line127 which we can ignore commit() or rollback(). With one ignore clause, the test
Line128 can focus on the code’s domain behavior by disabling everything to do with
Line129 transactions.
Line130 Like all “power tools,” ignoring() should be used with care. A chain of ignored
Line131 objects might suggest that the functionality ought to be pulled out into a new
Line132 collaborator. As programmers, we must also make sure that ignored features are
Line133 tested somewhere, and that there are higher-level tests to make sure everything
Line134 works together. In practice, we usually introduce ignoring() only when writing
Line135 specialized tests after the basics are in place, as for example in “The Sniper
Line136 Acquires Some State” (page 144).
Line137 279
Line138 Precise Expectations
Line139 
Line140 
Line141 ---
Line142 
Line143 ---
Line144 **Page 280**
Line145 
Line146 Invocation Order
Line147 jMock allows invocations on a mock object to be called in any order; the expec-
Line148 tations don’t have to be declared in the same sequence.1 The less we say in the
Line149 tests about the order of interactions, the more ﬂexibility we have with the imple-
Line150 mentation of the code. We also gain ﬂexibility in how we structure the tests; for
Line151 example, we can make test methods more readable by packaging up expectations
Line152 in helper methods.
Line153 Only Enforce Invocation Order When It Matters
Line154 Sometimes the order in which calls are made is signiﬁcant, in which case we add
Line155 explicit constraints to the test. Keeping such constraints to a minimum avoids
Line156 locking down the production code. It also helps us see whether each case is
Line157 necessary—ordered constraints are so uncommon that each use stands out.
Line158 jMock has two mechanisms for constraining invocation order: sequences,
Line159 which deﬁne an ordered list of invocations, and state machines, which can describe
Line160 more sophisticated ordering constraints. Sequences are simpler to understand
Line161 than state machines, but their restrictiveness can make tests brittle if used
Line162 inappropriately.
Line163 Sequences are most useful for conﬁrming that an object sends notiﬁcations to
Line164 its neighbors in the right order. For example, we need an AuctionSearcher object
Line165 that will search its collection of Auctions to ﬁnd which ones match anything from
Line166 a given set of keywords. Whenever it ﬁnds a match, the searcher will notify its
Line167 AuctionSearchListener by calling searchMatched() with the matching auction.
Line168 The searcher will tell the listener that it’s tried all of its available auctions by
Line169 calling searchFinished().
Line170 Our ﬁrst attempt at a test looks like this:
Line171 public class AuctionSearcherTest { […]
Line172   @Test public void
Line173 announcesMatchForOneAuction() {
Line174     final AuctionSearcher auctionSearch = 
Line175                    new AuctionSearcher(searchListener, asList(STUB_AUCTION1));
Line176     context.checking(new Expectations() {{
Line177       oneOf(searchListener).searchMatched(STUB_AUCTION1);
Line178       oneOf(searchListener).searchFinished();
Line179     }});
Line180     auctionSearch.searchFor(KEYWORDS);
Line181   }
Line182 }
Line183 1. Some early mock frameworks were strictly “record/playback”: the actual calls had
Line184 to match the sequence of the expected calls. No frameworks enforce this any more,
Line185 but the misconception is still common.
Line186 Chapter 24
Line187 Test Flexibility
Line188 280
Line189 
Line190 
Line191 ---
Line192 
Line193 ---
Line194 **Page 281**
Line195 
Line196 where searchListener is a mock AuctionSearchListener, KEYWORDS is a set of
Line197 keyword strings, and STUB_AUCTION1 is a stub implementation of Auction that
Line198 will match one of the strings in KEYWORDS.
Line199 The problem with this test is that there’s nothing to stop searchFinished()
Line200 being called before searchMatched(), which doesn’t make sense. We have an in-
Line201 terface for AuctionSearchListener, but we haven’t described its protocol. We
Line202 can ﬁx this by adding a Sequence to describe the relationship between the calls
Line203 to the listener. The test will fail if searchFinished() is called ﬁrst.
Line204 @Test public void
Line205 announcesMatchForOneAuction() {
Line206     final AuctionSearcher auctionSearch = 
Line207                    new AuctionSearcher(searchListener, asList(STUB_AUCTION1));
Line208   context.checking(new Expectations() {{
Line209 Sequence events = context.sequence("events");
Line210     oneOf(searchListener).searchMatched(STUB_AUCTION1); inSequence(events);
Line211     oneOf(searchListener).searchFinished();             inSequence(events);
Line212   }});
Line213   auctionSearch.searchFor(KEYWORDS);
Line214 }
Line215 We continue using this sequence as we add more auctions to match:
Line216 @Test public void
Line217 announcesMatchForTwoAuctions() {
Line218   final AuctionSearcher auctionSearch = new AuctionSearcher(searchListener, 
Line219                    new AuctionSearcher(searchListener, 
Line220                                        asList(STUB_AUCTION1, STUB_AUCTION2));
Line221   context.checking(new Expectations() {{
Line222     Sequence events = context.sequence("events");
Line223     oneOf(searchListener).searchMatched(STUB_AUCTION1); inSequence(events);
Line224 oneOf(searchListener).searchMatched(STUB_AUCTION2); inSequence(events);
Line225     oneOf(searchListener).searchFinished();             inSequence(events);
Line226   }});
Line227   auctionSearch.searchFor(KEYWORDS);
Line228 } 
Line229 But is this overconstraining the protocol? Do we have to match auctions in
Line230 the same order that they’re initialized? Perhaps all we care about is that the right
Line231 matches are made before the search is closed. We can relax the ordering constraint
Line232 with a States object (which we ﬁrst saw in “The Sniper Acquires Some State”
Line233 on page 144).
Line234 A States implements an abstract state machine with named states. We can
Line235 trigger state transitions by attaching a then() clause to an expectation. We
Line236 281
Line237 Precise Expectations
Line238 
Line239 
Line240 ---
Line241 
Line242 ---
Line243 **Page 282**
Line244 
Line245 can enforce that an invocation only happens when object is (or is not) in a
Line246 particular state with a when() clause. We rewrite our test:
Line247 @Test public void
Line248 announcesMatchForTwoAuctions() {
Line249   final AuctionSearcher auctionSearch = new AuctionSearcher(searchListener, 
Line250                    new AuctionSearcher(searchListener, 
Line251                                        asList(STUB_AUCTION1, STUB_AUCTION2));
Line252   context.checking(new Expectations() {{
Line253 States searching = context.states("searching");
Line254     oneOf(searchListener).searchMatched(STUB_AUCTION1); 
Line255 when(searching.isNot("finished"));
Line256     oneOf(searchListener).searchMatched(STUB_AUCTION2); 
Line257 when(searching.isNot("finished"));
Line258     oneOf(searchListener).searchFinished(); then(searching.is("finished"));
Line259   }});
Line260   auctionSearch.searchFor(KEYWORDS);
Line261 } 
Line262 When the test opens, searching is in an undeﬁned (default) state. The searcher
Line263 can report matches as long as searching is not ﬁnished. When the searcher reports
Line264 that it has ﬁnished, the then() clause switches searching to finished, which
Line265 blocks any further matches.
Line266 States and sequences can be used in combination. For example, if our require-
Line267 ments change so that auctions have to be matched in order, we can add a sequence
Line268 for just the matches, in addition to the existing searching states. The new
Line269 sequence would conﬁrm the order of search results and the existing states would
Line270 conﬁrm that the results arrived before the search is ﬁnished. An expectation can
Line271 belong to multiple states and sequences, if that’s what the protocol requires. We
Line272 rarely need such complexity—it’s most common when responding to external
Line273 feeds of events where we don’t own the protocol—and we always take it as a
Line274 hint that something should be broken up into smaller, simpler pieces.
Line275 When Expectation Order Matters
Line276 Actually, the order in which jMock expectations are declared is sometimes signiﬁcant,
Line277 but not because they have to shadow the order of invocation. Expectations are
Line278 appended to a list, and invocations are matched by searching this list in order. If
Line279 there are two expectations that can match an invocation, the one declared ﬁrst will
Line280 win. If that ﬁrst expectation is actually an allowance, the second expectation will
Line281 never see a match and the test will fail.
Line282 Chapter 24
Line283 Test Flexibility
Line284 282
Line285 
Line286 
Line287 ---
Line288 
Line289 ---
Line290 **Page 283**
Line291 
Line292 The Power of jMock States
Line293 jMock States has turned out to be a useful construct. We can use it to model
Line294 each of the three types of participants in a test: the object being tested, its peers,
Line295 and the test itself.
Line296 We can represent our understanding of the state of the object being tested, as
Line297 in the example above. The test listens for the events the object sends out to its
Line298 peers and uses them to trigger state transitions and to reject events that would
Line299 break the object’s protocol.
Line300 As we wrote in “Representing Object State” (page 146), this is a logical repre-
Line301 sentation of the state of the tested object. A States describes what the test ﬁnds
Line302 relevant about the object, not its internal structure. We don’t want to constrain
Line303 the object’s implementation.
Line304 We can represent how a peer changes state as it’s called by the tested object.
Line305 For instance, in the example above, we might want to insist that the listener must
Line306 be ready before it can receive any results, so the searcher must query its state.
Line307 We could add a new States, listenerState:
Line308 allowing(searchListener).isReady(); will(returnValue(true));
Line309                                     then(listenerState.is("ready"));
Line310 oneOf(searchListener).searchMatched(STUB_AUCTION1); 
Line311                                     when(listenerState.is("ready")); 
Line312 Finally, we can represent the state of the test itself. For example, we could
Line313 enforce that some interactions are ignored while the test is being set up:
Line314 ignoring(auction); when(testState.isNot("running"));
Line315 testState.become("running");
Line316 oneOf(auction).bidMore(); when(testState.is("running")); 
Line317 Even More Liberal Expectations
Line318 Finally, jMock has plug-in points to support the deﬁnition of arbitrary expecta-
Line319 tions. For example, we could write an expectation to accept any getter method:
Line320 allowing(aPeerObject).method(startsWith("get")).withNoArguments();
Line321 or to accept a call to one of a set of objects:
Line322 oneOf (anyOf(same(o1),same(o2),same(o3))).method("doSomething");
Line323 Such expectations move us from a statically typed to a dynamically typed world,
Line324 which brings both power and risk. These are our strongest “power tool”
Line325 features—sometimes just what we need but always to be used with care. There’s
Line326 more detail in the jMock documentation.
Line327 283
Line328 Precise Expectations
Line329 
Line330 
Line331 ---
Line332 
Line333 ---
Line334 **Page 284**
Line335 
Line336 “Guinea Pig” Objects
Line337 In the “ports and adapters” architecture we described in “Designing for
Line338 Maintainability” (page 47), the adapters map application domain objects onto
Line339 the system’s technical infrastructure. Most of the adapter implementations we
Line340 see are generic; for example, they often use reﬂection to move values between
Line341 domains. We can apply such mappings to any type of object, which means we
Line342 can change our domain model without touching the mapping code.
Line343 The easiest approach when writing tests for the adapter code is to use types
Line344 from the application domain model, but this makes the test brittle because it
Line345 binds together the application and adapter domains. It introduces a risk of mis-
Line346 leadingly breaking tests when we change the application model, because we
Line347 haven’t separated the concerns.
Line348 Here’s an example. A system uses an XmlMarshaller to marshal objects to and
Line349 from XML so they can be sent across a network. This test exercises XmlMarshaller
Line350 by round-tripping an AuctionClosedEvent object: a type that the production
Line351 system really does send across the network.
Line352 public class XmlMarshallerTest {
Line353   @Test public void 
Line354 marshallsAndUnmarshallsSerialisableFields() {
Line355     XMLMarshaller marshaller = new XmlMarshaller();
Line356     AuctionClosedEvent original = new AuctionClosedEventBuilder().build();
Line357     String xml = marshaller.marshall(original);
Line358     AuctionClosedEvent unmarshalled = marshaller.unmarshall(xml);
Line359     assertThat(unmarshalled, hasSameSerialisableFieldsAs(original));
Line360   }
Line361 }
Line362 Later we decide that our system won’t send an AuctionClosedEvent after all,
Line363 so we should be able to delete the class. Our refactoring attempt will fail because
Line364 AuctionClosedEvent is still being used by the XmlMarshallerTest. The irrelevant
Line365 coupling will force us to rework the test unnecessarily.
Line366 There’s a more signiﬁcant (and subtle) problem when we couple tests to domain
Line367 types: it’s harder to see when test assumptions have been broken. For example,
Line368 our XmlMarshallerTest also checks how the marshaller handles transient and
Line369 non-transient ﬁelds. When we wrote the tests, AuctionClosedEvent included both
Line370 kind of ﬁelds, so we were exercising all the paths through the marshaller. Later,
Line371 we removed the transient ﬁelds from AuctionClosedEvent, which means that we
Line372 have tests that are no longer meaningful but do not fail. Nothing is alerting us
Line373 that we have tests that have stopped working and that important features are
Line374 not being covered.
Line375 Chapter 24
Line376 Test Flexibility
Line377 284
Line378 
Line379 
Line380 ---
