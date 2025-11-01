Line1 # An Introduction to the Market (pp.105-106)
Line2 
Line3 ---
Line4 **Page 105**
Line5 
Line6 Chapter 12
Line7 Getting Ready to Bid
Line8 In which we write an end-to-end test so that we can make the Sniper
Line9 bid in an auction. We start to interpret the messages in the auction
Line10 protocol and discover some new classes in the process. We write our
Line11 ﬁrst unit tests and then refactor out a helper class. We describe every
Line12 last detail of this effort to show what we were thinking at the time.
Line13 An Introduction to the Market
Line14 Now, to continue with the skeleton metaphor, we start to ﬂesh out the application.
Line15 The core behavior of a Sniper is that it makes a higher bid on an item in an auction
Line16 when there’s a change in price. Going back to our to-do list, we revisit the next
Line17 couple of items:
Line18 •
Line19 Single item: join, bid, and lose. When a price comes in, send a bid raised
Line20 by the minimum increment deﬁned by the auction. This amount will be
Line21 included in the price update information.
Line22 •
Line23 Single item: join, bid, and win. Distinguish which bidder is currently winning
Line24 the auction and don’t bid against ourselves.
Line25 We know there’ll be more coming, but this is a coherent slice of functionality
Line26 that will allow us to explore the design and show concrete progress.
Line27 In any distributed system similar to this one there are lots of interesting failure
Line28 and timing issues, but our application only has to deal with the client side of the
Line29 protocol. We rely on the underlying XMPP protocol to deal with many common
Line30 distributed programming problems; in particular, we expect it to ensure that
Line31 messages between a bidder and an auction arrive in the same order in which they
Line32 were sent.
Line33 As we described in Chapter 5, we start the next feature with an acceptance
Line34 test. We used our ﬁrst test in the previous chapter to help ﬂush out the structure
Line35 of our application. From now on, we can use acceptance tests to show incremental
Line36 progress.
Line37 105
Line38 
Line39 
Line40 ---
Line41 
Line42 ---
Line43 **Page 106**
Line44 
Line45 A Test for Bidding
Line46 Starting with a Test
Line47 Each acceptance test we write should have just enough new requirements to force
Line48 a manageable increase in functionality, so we decide that the next one will add
Line49 some price information. The steps are:
Line50 1.
Line51 Tell the auction to send a price to the Sniper.
Line52 2.
Line53 Check the Sniper has received and responded to the price.
Line54 3.
Line55 Check the auction has received an incremented bid from Sniper.
Line56 To make this pass, the Sniper will have to distinguish between Price and Close
Line57 events from the auction, display the current price, and generate a new bid. We’ll
Line58 also have to extend our stub auction to handle bids. We’ve deferred implementing
Line59 other functionality that will also be required, such as displaying when the Sniper
Line60 has won the auction; we’ll get to that later. Here’s the new test:
Line61 public class AuctionSniperEndToEndTest {
Line62   @Test public void
Line63 sniperMakesAHigherBidButLoses() throws Exception {
Line64     auction.startSellingItem();
Line65     application.startBiddingIn(auction);
Line66     auction.hasReceivedJoinRequestFromSniper(); 1
Line67     auction.reportPrice(1000, 98, "other bidder"); 2
Line68     application.hasShownSniperIsBidding(); 3
Line69     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID); 4
Line70     auction.announceClosed(); 5
Line71     application.showsSniperHasLostAuction();   
Line72   }
Line73 }
Line74 We have three new methods to implement as part of this test.
Line75 1
Line76 We have to wait for the stub auction to receive the Join request before con-
Line77 tinuing with the test. We use this assertion to synchronize the Sniper with
Line78 the auction.
Line79 2
Line80 This method tells the stub auction to send a message back to the Sniper with
Line81 the news that at the moment the price of the item is 1000, the increment for
Line82 the next bid is 98, and the winning bidder is “other bidder.”
Line83 3
Line84 This method asks the ApplicationRunner to check that the Sniper shows that
Line85 it’s now bidding after it’s received the price update message from the auction.
Line86 Chapter 12
Line87 Getting Ready to Bid
Line88 106
Line89 
Line90 
Line91 ---
