Line1 # Testing That an Action Has No Effect (pp.325-326)
Line2 
Line3 ---
Line4 **Page 325**
Line5 
Line6 This shows the limits of how precise we can be with a sampling test. All the
Line7 test can do between “stimulate” and “sample” is wait. We can write more
Line8 reliable tests by not confusing the different steps in the loop and only triggering
Line9 further changes once we’ve detected that the system is stable by observing a
Line10 change in its sampled state.
Line11 Testing That an Action Has No Effect
Line12 Asynchronous tests look for changes in a system, so to test that something has
Line13 not changed takes a little ingenuity. Synchronous tests don’t have this problem
Line14 because they completely control the execution of the tested code. After invoking
Line15 the target object, synchronous tests can query its state or check that it hasn’t
Line16 made any unexpected calls to its neighbors.
Line17 If an asynchronous test waits for something not to happen, it cannot even be
Line18 sure that the system has started before it checks the result. For example, if we
Line19 want to show that trades in another region are not counted in the stock holding,
Line20 then this test:
Line21 @Test public void doesNotShowTradesInOtherRegions() {
Line22   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
Line23 .inTradingRegion(OTHER_REGION));
Line24   assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line25 }
Line26 cannot tell whether the system has correctly ignored the trade or just not received
Line27 it yet. The most obvious workaround is for the test to wait for a ﬁxed period of
Line28 time and then check that the unwanted event did not occur. Unfortunately, this
Line29 makes the test run slowly even when successful, and so breaks our rule of
Line30 “succeed fast.”
Line31 Instead, the test should trigger a behavior that is detectable and use that to
Line32 detect that the system has stabilized. The skill here is in picking a behavior that
Line33 will not interfere with the test’s assertions and that will complete after the tested
Line34 behavior. For example, we could add another trade event to the regions example.
Line35 This shows that the out-of-region event is excluded because its quantity is not
Line36 included in the total holding.
Line37 @Test public void doesNotShowTradesInOtherRegions() {
Line38   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
Line39                     .inTradingRegion(OTHER_REGION));
Line40   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(66)
Line41                     .inTradingRegion(SAME_REGION));
Line42   assertEventually(holdingOfStock("A", tradeDate, equalTo(66)));
Line43 }
Line44 Of course, this test assumes that trade events are processed in sequence, not
Line45 in parallel, so that the second event cannot overtake the ﬁrst and give a false
Line46 positive. That’s why such tests are not completely “black box” but have to make
Line47 assumptions about the structure of the system. This might make these tests
Line48 325
Line49 Testing That an Action Has No Effect
Line50 
Line51 
Line52 ---
Line53 
Line54 ---
Line55 **Page 326**
Line56 
Line57 brittle—they would misreport if the system changes the assumptions they’ve been
Line58 built on. One response is to add a test to conﬁrm those expectations—in this
Line59 case, perhaps a stress test to conﬁrm event processing order and alert the team
Line60 if circumstances change. That said, there should already be other tests that conﬁrm
Line61 those assumptions, so it may be enough just to associate these tests, for example
Line62 by grouping them in the same test package.
Line63 Distinguish Synchronizations and Assertions
Line64 We have one mechanism for synchronizing a test with its system and for making
Line65 assertions about that system—wait for an observable condition and time out if
Line66 it doesn’t happen. The only difference between the two activities is our interpre-
Line67 tation of what they mean. As always, we want to make our intentions explicit,
Line68 but it’s especially important here because there’s a risk that someone may look
Line69 at the test later and remove what looks like a duplicate assertion, accidentally
Line70 introducing a race condition.
Line71 We often adopt a naming scheme to distinguish between synchronizations and
Line72 assertions. For example, we might have waitUntil() and assertEventually()
Line73 methods to express the purpose of different checks that share an underlying
Line74 implementation.
Line75 Alternatively, we might reserve the term “assert” for synchronous tests and
Line76 use a different naming conventions in asynchronous tests, as we did in the Auction
Line77 Sniper example.
Line78 Externalize Event Sources
Line79 Some systems trigger their own events internally. The most common example is
Line80 using a timer to schedule activities. This might include repeated actions that run
Line81 frequently, such as bundling up emails for forwarding, or follow-up actions that
Line82 run days or even weeks in the future, such as conﬁrming a delivery date.
Line83 Hidden timers are very difﬁcult to work with because they make it hard to tell
Line84 when the system is in a stable state for a test to make its assertions. Waiting for
Line85 a repeated action to run is too slow to “succeed fast,” to say nothing of an action
Line86 scheduled a month from now. We also don’t want tests to break unpredictably
Line87 because of interference from a scheduled activity that’s just kicked in. Trying to
Line88 test a system by coinciding timers is just too brittle.
Line89 The only solution is to make the system deterministic by decoupling it from
Line90 its own scheduling. We can pull event generation out into a shared service that
Line91 is driven externally. For example, in one project we implemented the system’s
Line92 scheduler as a web service. System components scheduled activities by making
Line93 HTTP requests to the scheduler, which triggered activities by making HTTP
Line94 “postbacks.” In another project, the scheduler published notiﬁcations onto a
Line95 message bus topic that the components listened to.
Line96 Chapter 27
Line97 Testing Asynchronous Code
Line98 326
Line99 
Line100 
Line101 ---
