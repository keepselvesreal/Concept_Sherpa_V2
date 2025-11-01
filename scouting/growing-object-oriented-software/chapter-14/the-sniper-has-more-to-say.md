Line1 # The Sniper Has More to Say (pp.143-144)
Line2 
Line3 ---
Line4 **Page 143**
Line5 
Line6 The Sniper Has More to Say
Line7 Our immediate end-to-end test failure tells us that we should make the user inter-
Line8 face show when the Sniper is winning. Our next implementation step is to follow
Line9 through by ﬁxing the AuctionSniper to interpret the isFromSniper parameter
Line10 we’ve just added. Once again we start with a unit test.
Line11 public class AuctionSniperTest { […]
Line12   @Test public void
Line13 reportsIsWinningWhenCurrentPriceComesFromSniper() {
Line14     context.checking(new Expectations() {{
Line15       atLeast(1).of(sniperListener).sniperWinning();
Line16     }});
Line17     sniper.currentPrice(123, 45, PriceSource.FromSniper);
Line18   }
Line19 }
Line20 To get through the compiler, we add the new sniperWinning() method to
Line21 SniperListener which, in turn, means that we add an empty implementation
Line22 to SniperStateDisplayer.
Line23 The test fails:
Line24 unexpected invocation: auction.bid(<168>)
Line25 expectations:
Line26 ! expected at least 1 time, never invoked: sniperListener.sniperWinning()
Line27 what happened before this: nothing!
Line28 This failure is a nice example of trapping a method that we didn’t expect. We set
Line29 no expectations on the auction, so calls to any of its methods will fail the test.
Line30 If you compare this test to bidsHigherAndReportsBiddingWhenNewPriceArrives()
Line31 in “The AuctionSniper Bids” (page 126) you’ll also see that we drop the price
Line32 and increment variables and just feed in numbers. That’s because, in this test,
Line33 there’s no calculation to do, so we don’t need to reference them in an expectation.
Line34 They’re just details to get us to the interesting behavior.
Line35 The ﬁx is straightforward:
Line36 public class AuctionSniper implements AuctionEventListener { […]
Line37   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line38 switch (priceSource) {
Line39     case FromSniper:
Line40       sniperListener.sniperWinning();
Line41       break;
Line42     case FromOtherBidder:
Line43       auction.bid(price + increment); 
Line44       sniperListener.sniperBidding();
Line45       break;
Line46     }
Line47   } 
Line48 }
Line49 143
Line50 The Sniper Has More to Say
Line51 
Line52 
Line53 ---
Line54 
Line55 ---
Line56 **Page 144**
Line57 
Line58 Running the end-to-end tests again shows that we’ve ﬁxed the failure that
Line59 started this chapter (showing Bidding rather than Winning). Now we have to
Line60 make the Sniper win:
Line61 java.lang.AssertionError: 
Line62 Tried to look for...
Line63   exactly 1 JLabel (with name "sniper status")
Line64   in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line65   in all top level windows
Line66 and check that its label text is "Won"
Line67 but...
Line68   all top level windows
Line69   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line70   contained 1 JLabel (with name "sniper status")
Line71 label text was "Lost"
Line72 The Sniper Acquires Some State
Line73 We’re about to introduce a step change in the complexity of the Sniper, if only
Line74 a small one. When the auction closes, we want the Sniper to announce whether
Line75 it has won or lost, which means that it must know whether it was bidding or
Line76 winning at the time. This implies that the Sniper will have to maintain some state,
Line77 which it hasn’t had to so far.
Line78 To get to the functionality we want, we’ll start with the simpler cases where
Line79 the Sniper loses. As Figure 14.2 shows, we’re starting with one- and two-step
Line80 transitions, before adding the additional step that takes the Sniper to the Won state:
Line81 Figure 14.2
Line82 A Sniper bids, then loses
Line83 Chapter 14
Line84 The Sniper Wins the Auction
Line85 144
Line86 
Line87 
Line88 ---
