Line1 # Runaway Tests (pp.322-323)
Line2 
Line3 ---
Line4 **Page 322**
Line5 
Line6 Timing Out
Line7 Finally we show the Timeout class that the two example assertion classes use. It
Line8 packages up time checking and synchronization:
Line9 public class Timeout {
Line10  private final long endTime;
Line11   public Timeout(long duration) {
Line12     this.endTime = System.currentTimeMillis() + duration;
Line13   }
Line14   public boolean hasTimedOut() { return timeRemaining() <= 0; }
Line15   public void waitOn(Object lock) throws InterruptedException {
Line16     long waitTime = timeRemaining();
Line17     if (waitTime > 0) lock.wait(waitTime);
Line18   }
Line19   private long timeRemaining() { return endTime - System.currentTimeMillis(); }
Line20 }
Line21 Retroﬁtting a Probe
Line22 We can now rewrite the test from the introduction. Instead of making an assertion
Line23 about the current holding of a stock, the test must wait for the holding of the
Line24 stock to reach the expected level within an acceptable time limit.
Line25 @Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
Line26   Date tradeDate = new Date();
Line27   send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
Line28   send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
Line29 assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line30 }
Line31 Previously, the holdingOfStock() method returned a value to be compared.
Line32 Now it returns a Probe that samples the system’s holding and returns if it meets
Line33 the acceptance criteria deﬁned by a Hamcrest matcher—in this case equalTo(0).
Line34 Runaway Tests
Line35 Unfortunately, the new version of the test is still unreliable, even though we’re
Line36 now sampling for a result. The assertion is waiting for the holding to become
Line37 zero, which is what we started out with, so it’s possible for the test to pass before
Line38 the system has even begun processing. This test can run ahead of the system
Line39 without actually testing anything.
Line40 Chapter 27
Line41 Testing Asynchronous Code
Line42 322
Line43 
Line44 
Line45 ---
Line46 
Line47 ---
Line48 **Page 323**
Line49 
Line50 The worst aspect of runaway tests is that they give false positive results, so
Line51 broken code looks like it’s working. We don’t often review tests that pass, so it’s
Line52 easy to miss this kind of failure until something breaks down the line. Even more
Line53 tricky, the code might have worked when we ﬁrst wrote it, as the tests happened
Line54 to synchronize correctly during development, but now it’s broken and we
Line55 can’t tell.
Line56 Beware of Tests That Return the System to the Same State
Line57 Be careful when an asynchronous test asserts that the system returns to a previous
Line58 state. Unless it also asserts that the system enters an intermediate state before
Line59 asserting the initial state, the test will run ahead of the system.
Line60 To stop the test running ahead of the system, we must add assertions that wait
Line61 for the system to enter an intermediate state. Here, for example, we make sure
Line62 that the ﬁrst trade event has been processed before asserting the effect of the
Line63 second event:
Line64 @Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
Line65   Date tradeDate = new Date();
Line66   send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
Line67 assertEventually(holdingOfStock("A", tradeDate, equalTo(10)));
Line68   send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
Line69   assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
Line70 }
Line71 Similarly, in Chapter 14, we check all the displayed states in the acceptance
Line72 tests for the Auction Sniper user interface:
Line73 auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line74 application.hasShownSniperIsWinning();
Line75 auction.announceClosed();
Line76 application.hasShownSniperHasWon();
Line77 We want to make sure that the sniper has responded to each message before
Line78 continuing on to the next one.
Line79 Lost Updates
Line80 A signiﬁcant difference between tests that sample and those that listen for events
Line81 is that polling can miss state changes that are later overwritten, Figure 27.1.
Line82 323
Line83 Lost Updates
Line84 
Line85 
Line86 ---
