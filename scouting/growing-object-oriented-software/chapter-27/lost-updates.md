Line1 # Lost Updates (pp.323-325)
Line2 
Line3 ---
Line4 **Page 323**
Line5 
Line6 The worst aspect of runaway tests is that they give false positive results, so
Line7 broken code looks like it’s working. We don’t often review tests that pass, so it’s
Line8 easy to miss this kind of failure until something breaks down the line. Even more
Line9 tricky, the code might have worked when we ﬁrst wrote it, as the tests happened
Line10 to synchronize correctly during development, but now it’s broken and we
Line11 can’t tell.
Line12 Beware of Tests That Return the System to the Same State
Line13 Be careful when an asynchronous test asserts that the system returns to a previous
Line14 state. Unless it also asserts that the system enters an intermediate state before
Line15 asserting the initial state, the test will run ahead of the system.
Line16 To stop the test running ahead of the system, we must add assertions that wait
Line17 for the system to enter an intermediate state. Here, for example, we make sure
Line18 that the ﬁrst trade event has been processed before asserting the effect of the
Line19 second event:
Line20 @Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
Line21   Date tradeDate = new Date();
Line22   send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
Line23 assertEventually(holdingOfStock("A", tradeDate, equalTo(10)));
Line24   send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
Line25   assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line26 }
Line27 Similarly, in Chapter 14, we check all the displayed states in the acceptance
Line28 tests for the Auction Sniper user interface:
Line29 auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line30 application.hasShownSniperIsWinning();
Line31 auction.announceClosed();
Line32 application.hasShownSniperHasWon();
Line33 We want to make sure that the sniper has responded to each message before
Line34 continuing on to the next one.
Line35 Lost Updates
Line36 A signiﬁcant difference between tests that sample and those that listen for events
Line37 is that polling can miss state changes that are later overwritten, Figure 27.1.
Line38 323
Line39 Lost Updates
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 324**
Line46 
Line47 Figure 27.1
Line48 A test that polls can miss changes in the system
Line49 under test
Line50 If the test can record notiﬁcations from the system, it can look through its
Line51 records to ﬁnd signiﬁcant notiﬁcations.
Line52 Figure 27.2
Line53 A test that records notiﬁcations will not lose updates
Line54 To be reliable, a sampling test must make sure that its system is stable before
Line55 triggering any further interactions. Sampling tests need to be structured as a series
Line56 of phases, as shown in Figure 27.3. In each phase, the test sends a stimulus to
Line57 prompt a change in the observable state of the system, and then waits until that
Line58 change becomes visible or times out.
Line59 Figure 27.3
Line60 Phases of a sampling test
Line61 Chapter 27
Line62 Testing Asynchronous Code
Line63 324
Line64 
Line65 
Line66 ---
Line67 
Line68 ---
Line69 **Page 325**
Line70 
Line71 This shows the limits of how precise we can be with a sampling test. All the
Line72 test can do between “stimulate” and “sample” is wait. We can write more
Line73 reliable tests by not confusing the different steps in the loop and only triggering
Line74 further changes once we’ve detected that the system is stable by observing a
Line75 change in its sampled state.
Line76 Testing That an Action Has No Effect
Line77 Asynchronous tests look for changes in a system, so to test that something has
Line78 not changed takes a little ingenuity. Synchronous tests don’t have this problem
Line79 because they completely control the execution of the tested code. After invoking
Line80 the target object, synchronous tests can query its state or check that it hasn’t
Line81 made any unexpected calls to its neighbors.
Line82 If an asynchronous test waits for something not to happen, it cannot even be
Line83 sure that the system has started before it checks the result. For example, if we
Line84 want to show that trades in another region are not counted in the stock holding,
Line85 then this test:
Line86 @Test public void doesNotShowTradesInOtherRegions() {
Line87   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
Line88 .inTradingRegion(OTHER_REGION));
Line89   assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line90 }
Line91 cannot tell whether the system has correctly ignored the trade or just not received
Line92 it yet. The most obvious workaround is for the test to wait for a ﬁxed period of
Line93 time and then check that the unwanted event did not occur. Unfortunately, this
Line94 makes the test run slowly even when successful, and so breaks our rule of
Line95 “succeed fast.”
Line96 Instead, the test should trigger a behavior that is detectable and use that to
Line97 detect that the system has stabilized. The skill here is in picking a behavior that
Line98 will not interfere with the test’s assertions and that will complete after the tested
Line99 behavior. For example, we could add another trade event to the regions example.
Line100 This shows that the out-of-region event is excluded because its quantity is not
Line101 included in the total holding.
Line102 @Test public void doesNotShowTradesInOtherRegions() {
Line103   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
Line104                     .inTradingRegion(OTHER_REGION));
Line105   send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(66)
Line106                     .inTradingRegion(SAME_REGION));
Line107   assertEventually(holdingOfStock("A", tradeDate, equalTo(66)));
Line108 }
Line109 Of course, this test assumes that trade events are processed in sequence, not
Line110 in parallel, so that the second event cannot overtake the ﬁrst and give a false
Line111 positive. That’s why such tests are not completely “black box” but have to make
Line112 assumptions about the structure of the system. This might make these tests
Line113 325
Line114 Testing That an Action Has No Effect
Line115 
Line116 
Line117 ---
