Line1 # Who Knows about Bidders? (pp.140-143)
Line2 
Line3 ---
Line4 **Page 140**
Line5 
Line6 public class AuctionSniperEndToEndTest { […]
Line7   @Test public void
Line8 sniperWinsAnAuctionByBiddingHigher() throws Exception {
Line9     auction.startSellingItem();
Line10     application.startBiddingIn(auction);
Line11     auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line12     auction.reportPrice(1000, 98, "other bidder");
Line13     application.hasShownSniperIsBidding();
Line14     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line15 auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line16     application.hasShownSniperIsWinning();
Line17     auction.announceClosed();
Line18     application.showsSniperHasWonAuction();
Line19   }
Line20 }
Line21 In our test infrastructure we add the two methods to check that the user interface
Line22 shows the two new states to the ApplicationRunner.
Line23 This generates a new failure message:
Line24 java.lang.AssertionError: 
Line25 Tried to look for...
Line26   exactly 1 JLabel (with name "sniper status")
Line27   in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line28   in all top level windows
Line29 and check that its label text is "Winning"
Line30 but...
Line31   all top level windows
Line32   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line33   contained 1 JLabel (with name "sniper status")
Line34 label text was "Bidding"
Line35 Now we know where we’re going, we can implement the feature.
Line36 Who Knows about Bidders?
Line37 The application knows that the Sniper is winning if it’s the bidder for the last
Line38 price that the auction accepted. We have to decide where to put that logic.
Line39 Looking again at Figure 13.5 on page 134, one choice would be that the translator
Line40 could pass the bidder through to the Sniper and let the Sniper decide. That would
Line41 mean that the Sniper would have to know something about how bidders are
Line42 identiﬁed by the auction, with a risk of pulling in XMPP details that we’ve been
Line43 careful to keep separate. To decide whether it’s winning, the only thing the Sniper
Line44 needs to know when a price arrives is, did this price come from me? This is a
Line45 Chapter 14
Line46 The Sniper Wins the Auction
Line47 140
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 141**
Line54 
Line55 choice, not an identiﬁer, so we’ll represent it with an enumeration PriceSource
Line56 which we include in AuctionEventListener.1
Line57 Incidentally, PriceSource is an example of a value type. We want code that
Line58 describes the domain of Sniping—not, say, a boolean which we would have to
Line59 interpret every time we read it; there’s more discussion in “Value Types”
Line60 (page 59).
Line61 public interface AuctionEventListener extends EventListener {
Line62 enum PriceSource {
Line63     FromSniper, FromOtherBidder;
Line64   };
Line65 […]
Line66 We take the view that determining whether this is our price or not is part of
Line67 the translator’s role. We extend currentPrice() with a new parameter and
Line68 change the translator’s unit tests; note that we change the name of the existing
Line69 test to include the extra feature. We also take the opportunity to pass the Sniper
Line70 identiﬁer to the translator in SNIPER_ID. This ties the setup of the translator to
Line71 the input message in the second test.
Line72 public class AuctionMessageTranslatorTest { […]
Line73   private final AuctionMessageTranslator translator = 
Line74                     new AuctionMessageTranslator(SNIPER_ID, listener);
Line75   @Test public void
Line76   notifiesBidDetailsWhenCurrentPriceMessageReceivedFromOtherBidder() {
Line77     context.checking(new Expectations() {{
Line78       exactly(1).of(listener).currentPrice(192, 7, PriceSource.FromOtherBidder);
Line79     }});
Line80     Message message = new Message();
Line81     message.setBody(
Line82 "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
Line83                    );
Line84     translator.processMessage(UNUSED_CHAT, message);
Line85   }
Line86   @Test public void
Line87 notifiesBidDetailsWhenCurrentPriceMessageReceivedFromSniper() {
Line88     context.checking(new Expectations() {{
Line89       exactly(1).of(listener).currentPrice(234, 5, PriceSource.FromSniper);
Line90     }});
Line91     Message message = new Message();
Line92     message.setBody(
Line93 "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 234; Increment: 5; Bidder: " 
Line94       + SNIPER_ID + ";");
Line95     translator.processMessage(UNUSED_CHAT, message);
Line96   }
Line97 }
Line98 1. Some developers we know have an allergic reaction to nested types. In Java, we use
Line99 them as a form of ﬁne-grained scoping. In this case, PriceSource is always used
Line100 together with AuctionEventListener, so it makes sense to bind the two together.
Line101 141
Line102 Who Knows about Bidders?
Line103 
Line104 
Line105 ---
Line106 
Line107 ---
Line108 **Page 142**
Line109 
Line110 The new test fails:
Line111 unexpected invocation: 
Line112   auctionEventListener.currentPrice(<192>, <7>, <FromOtherBidder>)
Line113 expectations:
Line114 ! expected once, never invoked: 
Line115     auctionEventListener.currentPrice(<192>, <7>, <FromSniper>)
Line116       parameter 0 matched: <192>
Line117       parameter 1 matched: <7>
Line118       parameter 2 did not match: <FromSniper>, because was <FromOtherBidder>
Line119 what happened before this: nothing!
Line120 The ﬁx is to compare the Sniper identiﬁer to the bidder from the event message.
Line121 public class AuctionMessageTranslator implements MessageListener {  […]
Line122 private final String sniperId;
Line123   public void processMessage(Chat chat, Message message) {
Line124 […]
Line125     } else if (EVENT_TYPE_PRICE.equals(type)) {
Line126       listener.currentPrice(event.currentPrice(), 
Line127                             event.increment(), 
Line128 event.isFrom(sniperId));
Line129     }
Line130   }
Line131   public static class AuctionEvent { […]
Line132 public PriceSource isFrom(String sniperId) {
Line133       return sniperId.equals(bidder()) ? FromSniper : FromOtherBidder;
Line134     }
Line135     private String bidder() { return get("Bidder"); }
Line136   }
Line137 }
Line138 The work we did in “Tidying Up the Translator” (page 135) to separate the
Line139 different responsibilities within the translator has paid off here. All we had to
Line140 do was add a couple of extra methods to AuctionEvent to get a very readable
Line141 solution.
Line142 Finally, to get all the code through the compiler, we ﬁx joinAuction() in Main
Line143 to pass in the new constructor parameter for the translator. We can get a correctly
Line144 structured identiﬁer from connection.
Line145 private void joinAuction(XMPPConnection connection, String itemId) {
Line146 […]
Line147   Auction auction = new XMPPAuction(chat);
Line148   chat.addMessageListener(
Line149       new AuctionMessageTranslator(
Line150 connection.getUser(), 
Line151              new AuctionSniper(auction, new SniperStateDisplayer())));
Line152   auction.join();
Line153 }
Line154 Chapter 14
Line155 The Sniper Wins the Auction
Line156 142
Line157 
Line158 
Line159 ---
Line160 
Line161 ---
Line162 **Page 143**
Line163 
Line164 The Sniper Has More to Say
Line165 Our immediate end-to-end test failure tells us that we should make the user inter-
Line166 face show when the Sniper is winning. Our next implementation step is to follow
Line167 through by ﬁxing the AuctionSniper to interpret the isFromSniper parameter
Line168 we’ve just added. Once again we start with a unit test.
Line169 public class AuctionSniperTest { […]
Line170   @Test public void
Line171 reportsIsWinningWhenCurrentPriceComesFromSniper() {
Line172     context.checking(new Expectations() {{
Line173       atLeast(1).of(sniperListener).sniperWinning();
Line174     }});
Line175     sniper.currentPrice(123, 45, PriceSource.FromSniper);
Line176   }
Line177 }
Line178 To get through the compiler, we add the new sniperWinning() method to
Line179 SniperListener which, in turn, means that we add an empty implementation
Line180 to SniperStateDisplayer.
Line181 The test fails:
Line182 unexpected invocation: auction.bid(<168>)
Line183 expectations:
Line184 ! expected at least 1 time, never invoked: sniperListener.sniperWinning()
Line185 what happened before this: nothing!
Line186 This failure is a nice example of trapping a method that we didn’t expect. We set
Line187 no expectations on the auction, so calls to any of its methods will fail the test.
Line188 If you compare this test to bidsHigherAndReportsBiddingWhenNewPriceArrives()
Line189 in “The AuctionSniper Bids” (page 126) you’ll also see that we drop the price
Line190 and increment variables and just feed in numbers. That’s because, in this test,
Line191 there’s no calculation to do, so we don’t need to reference them in an expectation.
Line192 They’re just details to get us to the interesting behavior.
Line193 The ﬁx is straightforward:
Line194 public class AuctionSniper implements AuctionEventListener { […]
Line195   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line196 switch (priceSource) {
Line197     case FromSniper:
Line198       sniperListener.sniperWinning();
Line199       break;
Line200     case FromOtherBidder:
Line201       auction.bid(price + increment); 
Line202       sniperListener.sniperBidding();
Line203       break;
Line204     }
Line205   } 
Line206 }
Line207 143
Line208 The Sniper Has More to Say
Line209 
Line210 
Line211 ---
