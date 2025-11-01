Line1 # The Sniper Wins (pp.146-148)
Line2 
Line3 ---
Line4 **Page 146**
Line5 
Line6 6
Line7 This is our ﬁrst test where we need a sequence of events to get the Sniper
Line8 into the state we want to test. We just call its methods in order.
Line9 Allowances
Line10 jMock distinguishes between allowed and expected invocations. An allowing()
Line11 clause says that the object might make this call, but it doesn’t have to—unlike an
Line12 expectation which will fail the test if the call isn’t made. We make the distinction to
Line13 help express what is important in a test (the underlying implementation is actually
Line14 the same): expectations are what we want to conﬁrm to have happened; allowances
Line15 are supporting infrastructure that helps get the tested objects into the right state,
Line16 or they’re side effects we don’t care about. We return to this topic in “Allowances
Line17 and Expectations” (page 277) and we describe the API in Appendix A.
Line18 Representing Object State
Line19 In cases like this, we want to make assertions about an object’s behavior depending
Line20 on its state, but we don’t want to break encapsulation by exposing how that state
Line21 is implemented. Instead, the test can listen to the notiﬁcation events that the Sniper
Line22 provides to tell interested collaborators about its state in their terms. jMock provides
Line23 States objects, so that tests can record and make assertions about the state of
Line24 an object when something signiﬁcant happens, i.e. when it calls its neighbors; see
Line25 Appendix A for the syntax.
Line26 This is a “logical” representation of what’s going on inside the object, in this case
Line27 the Sniper. It allows the test to describe what it ﬁnds relevant about the Sniper, re-
Line28 gardless of how the Sniper is actually implemented. As you’ll see shortly, this sep-
Line29 aration will allow us to make radical changes to the implementation of the Sniper
Line30 without changing the tests.
Line31 The unit test name reportsLostIfAuctionClosesWhenBidding is very similar
Line32 to the expectation it enforces:
Line33 atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
Line34 That’s not an accident. We put a lot of effort into ﬁguring out which abstractions
Line35 jMock should support and developing a style that expresses the essential intent
Line36 of a unit test.
Line37 The Sniper Wins
Line38 Finally, we can close the loop and have the Sniper win a bid. The next test
Line39 introduces the Won event.
Line40 Chapter 14
Line41 The Sniper Wins the Auction
Line42 146
Line43 
Line44 
Line45 ---
Line46 
Line47 ---
Line48 **Page 147**
Line49 
Line50 @Test public void
Line51 reportsWonIfAuctionClosesWhenWinning() {
Line52   context.checking(new Expectations() {{
Line53     ignoring(auction);
Line54     allowing(sniperListener).sniperWinning();  then(sniperState.is("winning"));
Line55     atLeast(1).of(sniperListener).sniperWon(); when(sniperState.is("winning"));
Line56   }});
Line57   sniper.currentPrice(123, 45, true);
Line58   sniper.auctionClosed();
Line59 }
Line60 It has the same structure but represents when the Sniper has won. The test fails
Line61 because the Sniper called sniperLost().
Line62 unexpected invocation: sniperListener.sniperLost()
Line63 expectations:
Line64   allowed, never invoked: 
Line65     auction.<any method>(<any parameters>) was[]; 
Line66   allowed, already invoked 1 time: sniperListener.sniperWinning(); 
Line67                                      then sniper is winning
Line68   expected at least 1 time, never invoked: sniperListener.sniperWon();
Line69                                              when sniper is winning
Line70 states:
Line71   sniper is winning
Line72 what happened before this:
Line73   sniperListener.sniperWinning()
Line74 We add a ﬂag to represent the Sniper’s state, and implement the new
Line75 sniperWon() method in the SniperStateDisplayer.
Line76 public class AuctionSniper implements AuctionEventListener { […]
Line77 private boolean isWinning = false;
Line78   public void auctionClosed() {
Line79 if (isWinning) {
Line80       sniperListener.sniperWon();
Line81     } else {
Line82       sniperListener.sniperLost();
Line83     }
Line84   }
Line85   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line86 isWinning = priceSource == PriceSource.FromSniper;
Line87     if (isWinning) {
Line88       sniperListener.sniperWinning();
Line89     } else {
Line90       auction.bid(price + increment);
Line91       sniperListener.sniperBidding();
Line92     }
Line93   }
Line94 }
Line95 public class SniperStateDisplayer implements SniperListener { […]
Line96   public void sniperWon() {
Line97     showStatus(MainWindow.STATUS_WON);
Line98   }
Line99 }
Line100 147
Line101 The Sniper Wins
Line102 
Line103 
Line104 ---
Line105 
Line106 ---
Line107 **Page 148**
Line108 
Line109 Having previously made a fuss about PriceSource, are we being inconsistent
Line110 here by using a boolean for isWinning? Our excuse is that we did try an enum
Line111 for the Sniper state, but it just looked too complicated. The ﬁeld is private to
Line112 AuctionSniper, which is small enough so it’s easy to change later and the code
Line113 reads well.
Line114 The unit and end-to-end tests all pass now, so we can cross off another item
Line115 from the to-do list in Figure 14.3.
Line116 Figure 14.3
Line117 The Sniper wins
Line118 There are more tests we could write—for example, to describe the transitions
Line119 from bidding to winning and back again, but we’ll leave those as an exercise for
Line120 you, Dear Reader. Instead, we’ll move on to the next signiﬁcant change in
Line121 functionality.
Line122 Making Steady Progress
Line123 As always, we made steady progress by adding little slices of functionality. First
Line124 we made the Sniper show when it’s winning, then when it has won. We used
Line125 empty implementations to get us through the compiler when we weren’t ready
Line126 to ﬁll in the code, and we stayed focused on the immediate task.
Line127 One of the pleasant surprises is that, now the code is growing a little, we’re
Line128 starting to see some of our earlier effort pay off as new features just ﬁt into the
Line129 existing structure. The next tasks we have to implement will shake this up.
Line130 Chapter 14
Line131 The Sniper Wins the Auction
Line132 148
