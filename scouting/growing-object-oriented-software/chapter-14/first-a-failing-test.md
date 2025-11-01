Line1 # First, a Failing Test (pp.139-140)
Line2 
Line3 ---
Line4 **Page 139**
Line5 
Line6 Chapter 14
Line7 The Sniper Wins the Auction
Line8 In which we add another feature to our Sniper and let it win an auction.
Line9 We introduce the concept of state to the Sniper which we test by listen-
Line10 ing to its callbacks. We ﬁnd that even this early, one of our refactorings
Line11 has paid off.
Line12 First, a Failing Test
Line13 We have a Sniper that can respond to price changes by bidding more, but it
Line14 doesn’t yet know when it’s successful. Our next feature on the to-do list is to
Line15 win an auction. This involves an extra state transition, as you can see in
Line16 Figure 14.1:
Line17 Figure 14.1
Line18 A sniper bids, then wins
Line19 To represent this, we add an end-to-end test based on sniperMakesAHigherBid-
Line20 ButLoses() with a different conclusion—sniperWinsAnAuctionByBiddingHigher().
Line21 Here’s the test, with the new features highlighted:
Line22 139
Line23 
Line24 
Line25 ---
Line26 
Line27 ---
Line28 **Page 140**
Line29 
Line30 public class AuctionSniperEndToEndTest { […]
Line31   @Test public void
Line32 sniperWinsAnAuctionByBiddingHigher() throws Exception {
Line33     auction.startSellingItem();
Line34     application.startBiddingIn(auction);
Line35     auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line36     auction.reportPrice(1000, 98, "other bidder");
Line37     application.hasShownSniperIsBidding();
Line38     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line39 auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line40     application.hasShownSniperIsWinning();
Line41     auction.announceClosed();
Line42     application.showsSniperHasWonAuction();
Line43   }
Line44 }
Line45 In our test infrastructure we add the two methods to check that the user interface
Line46 shows the two new states to the ApplicationRunner.
Line47 This generates a new failure message:
Line48 java.lang.AssertionError: 
Line49 Tried to look for...
Line50   exactly 1 JLabel (with name "sniper status")
Line51   in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line52   in all top level windows
Line53 and check that its label text is "Winning"
Line54 but...
Line55   all top level windows
Line56   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line57   contained 1 JLabel (with name "sniper status")
Line58 label text was "Bidding"
Line59 Now we know where we’re going, we can implement the feature.
Line60 Who Knows about Bidders?
Line61 The application knows that the Sniper is winning if it’s the bidder for the last
Line62 price that the auction accepted. We have to decide where to put that logic.
Line63 Looking again at Figure 13.5 on page 134, one choice would be that the translator
Line64 could pass the bidder through to the Sniper and let the Sniper decide. That would
Line65 mean that the Sniper would have to know something about how bidders are
Line66 identiﬁed by the auction, with a risk of pulling in XMPP details that we’ve been
Line67 careful to keep separate. To decide whether it’s winning, the only thing the Sniper
Line68 needs to know when a price arrives is, did this price come from me? This is a
Line69 Chapter 14
Line70 The Sniper Wins the Auction
Line71 140
Line72 
Line73 
Line74 ---
