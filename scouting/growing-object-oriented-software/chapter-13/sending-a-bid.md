Line1 # Sending a Bid (pp.126-131)
Line2 
Line3 ---
Line4 **Page 126**
Line5 
Line6 developers shouldn’t be shy about creating new types. We think Main still does
Line7 too much, but we’re not yet sure how best to break it up. We decide to push on
Line8 and see where the code takes us.
Line9 Sending a Bid
Line10 An Auction Interface
Line11 The next step is to have the Sniper send a bid to the auction, so who should the
Line12 Sniper talk to? Extending the SniperListener feels wrong because that relationship
Line13 is about tracking what’s happening in the Sniper, not about making external
Line14 commitments. In the terms deﬁned in “Object Peer Stereotypes” (page 52),
Line15 SniperListener is a notiﬁcation, not a dependency.
Line16 After the usual discussion, we decide to introduce a new collaborator, an
Line17 Auction. Auction and SniperListener represent two different domains in the
Line18 application: Auction is about ﬁnancial transactions, it accepts bids for items in
Line19 the market; and SniperListener is about feedback to the application, it reports
Line20 changes to the current state of the Sniper. The Auction is a dependency, for a
Line21 Sniper cannot function without one, whereas the SniperListener, as we
Line22 discussed above, is not. Introducing the new interface makes the design look like
Line23 Figure 13.2.
Line24 Figure 13.2
Line25 Introducing Auction
Line26 The AuctionSniper Bids
Line27 Now we’re ready to start bidding. The ﬁrst step is to implement the response to
Line28 a Price event, so we start by adding a new unit test for the AuctionSniper. It
Line29 says that the Sniper, when it receives a Price update, sends an incremented bid
Line30 to the auction. It also notiﬁes its listener that it’s now bidding, so we add a
Line31 sniperBidding() method. We’re making an implicit assumption that the Auction
Line32 knows which bidder the Sniper represents, so the Sniper does not have to pass
Line33 in that information with the bid.
Line34 Chapter 13
Line35 The Sniper Makes a Bid
Line36 126
Line37 
Line38 
Line39 ---
Line40 
Line41 ---
Line42 **Page 127**
Line43 
Line44 public class AuctionSniperTest {
Line45 private final Auction auction = context.mock(Auction.class);
Line46   private final AuctionSniper sniper = 
Line47                     new AuctionSniper(auction, sniperListener);
Line48 […]
Line49   @Test public void
Line50 bidsHigherAndReportsBiddingWhenNewPriceArrives() {
Line51     final int price = 1001;
Line52     final int increment = 25;
Line53     context.checking(new Expectations() {{
Line54       one(auction).bid(price + increment);
Line55       atLeast(1).of(sniperListener).sniperBidding();
Line56     }});
Line57     sniper.currentPrice(price, increment);
Line58   }
Line59 }
Line60 The failure report is:
Line61 not all expectations were satisfied
Line62 expectations:
Line63   ! expected once, never invoked: auction.bid(<1026>)
Line64   ! expected at least 1 time, never invoked: sniperListener.sniperBidding()
Line65 what happened before this: nothing!
Line66 When writing the test, we realized that we don’t actually care if the Sniper
Line67 notiﬁes the listener more than once that it’s bidding; it’s just a status update,
Line68 so we use an atLeast(1) clause for the listener’s expectation. On the other hand,
Line69 we do care that we send a bid exactly once, so we use a one() clause for its ex-
Line70 pectation. In practice, of course, we’ll probably only call the listener once, but
Line71 this loosening of the conditions in the test expresses our intent about the two
Line72 relationships. The test says that the listener is a more forgiving collaborator, in
Line73 terms of how it’s called, than the Auction. We also retroﬁt the atLeast(1) clause
Line74 to the other test method.
Line75 How Should We Describe Expected Values?
Line76 We’ve speciﬁed the expected bid value by adding the price and increment.There
Line77 are different opinions about whether test values should just be literals with “obvious”
Line78 values, or expressed in terms of the calculation they represent. Writing out the
Line79 calculation may make the test more readable but risks reimplementing the target
Line80 code in the test, and in some cases the calculation will be too complicated to repro-
Line81 duce. Here, we decide that the calculation is so trivial that we can just write it into
Line82 the test.
Line83 127
Line84 Sending a Bid
Line85 
Line86 
Line87 ---
Line88 
Line89 ---
Line90 **Page 128**
Line91 
Line92 jMock Expectations Don’t Need to Be Matched in Order
Line93 This is our ﬁrst test with more than one expectation, so we’ll point out that the order
Line94 in which expectations are declared does not have to match the order in which the
Line95 methods are called in the code. If the calling order does matter, the expectations
Line96 should include a sequence clause, which is described in Appendix A.
Line97 The implementation to make the test pass is simple.
Line98 public interface Auction {
Line99   void bid(int amount);
Line100 }
Line101 public class AuctionSniper implements AuctionEventListener {  […]
Line102   private final SniperListener sniperListener;
Line103 private final Auction auction;
Line104   public AuctionSniper(Auction auction, SniperListener sniperListener) {
Line105 this.auction = auction;
Line106     this.sniperListener = sniperListener;
Line107   }
Line108   public void currentPrice(int price, int increment) {
Line109     auction.bid(price + increment);
Line110     sniperListener.sniperBidding();
Line111   }
Line112 }
Line113 Successfully Bidding with the AuctionSniper
Line114 Now we have to fold our new AuctionSniper back into the application. The easy
Line115 part is displaying the bidding status, the (slightly) harder part is sending the bid
Line116 back to the auction. Our ﬁrst job is to get the code through the compiler. We
Line117 implement the new sniperBidding() method on Main and, to avoid having
Line118 code that doesn’t compile for too long, we pass the AuctionSniper a null
Line119 implementation of Auction.
Line120 Chapter 13
Line121 The Sniper Makes a Bid
Line122 128
Line123 
Line124 
Line125 ---
Line126 
Line127 ---
Line128 **Page 129**
Line129 
Line130 public class Main implements SniperListener { […]
Line131   private void joinAuction(XMPPConnection connection, String itemId) 
Line132     throws XMPPException 
Line133   {
Line134 Auction nullAuction = new Auction() {
Line135       public void bid(int amount) {}
Line136     };
Line137     disconnectWhenUICloses(connection);
Line138     Chat chat = connection.getChatManager().createChat(
Line139         auctionId(itemId, connection), 
Line140         new AuctionMessageTranslator(new AuctionSniper(nullAuction, this)));
Line141     this.notToBeGCd = chat;
Line142     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line143   }
Line144   public void sniperBidding() {
Line145     SwingUtilities.invokeLater(new Runnable() {
Line146       public void run() {
Line147         ui.showStatus(MainWindow.STATUS_BIDDING);
Line148       }
Line149     });
Line150   }
Line151 }
Line152 So, what goes in the Auction implementation? It needs access to the chat so it
Line153 can send a bid message. To create the chat we need a translator, the translator
Line154 needs a Sniper, and the Sniper needs an auction. We have a dependency loop
Line155 which we need to break.
Line156 Looking again at our design, there are a couple of places we could intervene,
Line157 but it turns out that the ChatManager API is misleading. It does not require a
Line158 MessageListener to create a Chat, even though the createChat() methods imply
Line159 that it does. In our terms, the MessageListener is a notiﬁcation; we can pass in
Line160 null when we create the Chat and add a MessageListener later.
Line161 Expressing Intent in API
Line162 We were only able to discover that we could pass null as a MessageListener
Line163 because we have the source code to the Smack library. This isn’t clear from the
Line164 API because, presumably, the authors wanted to enforce the right behavior and
Line165 it’s not clear why anyone would want a Chat without a listener. An alternative would
Line166 have been to provide equivalent creation methods that don’t take a listener, but
Line167 that would lead to API bloat. There isn’t an obvious best approach here, except to
Line168 note that including well-structured source code with the distribution makes libraries
Line169 much easier to work with.
Line170 129
Line171 Sending a Bid
Line172 
Line173 
Line174 ---
Line175 
Line176 ---
Line177 **Page 130**
Line178 
Line179 Now we can restructure our connection code and use the Chat to send back
Line180 a bid.
Line181 public class Main implements SniperListener { […]
Line182   private void joinAuction(XMPPConnection connection, String itemId) 
Line183     throws XMPPException 
Line184   {
Line185     disconnectWhenUICloses(connection);
Line186     final Chat chat = 
Line187       connection.getChatManager().createChat(auctionId(itemId, connection), null);
Line188     this.notToBeGCd = chat;
Line189     Auction auction = new Auction() {
Line190       public void bid(int amount) {
Line191         try {
Line192           chat.sendMessage(String.format(BID_COMMAND_FORMAT, amount));
Line193         } catch (XMPPException e) {
Line194           e.printStackTrace();
Line195         }
Line196       }
Line197     };
Line198     chat.addMessageListener(
Line199            new AuctionMessageTranslator(new AuctionSniper(auction, this)));
Line200     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line201   }
Line202 }
Line203 Null Implementation
Line204 A null implementation is similar to a null object [Woolf98]: both are implementations
Line205 that respond to a protocol by not doing anything—but the intention is different. A
Line206 null object is usually one implementation amongst many, introduced to reduce
Line207 complexity in the code that calls the protocol. We deﬁne a null implementation as
Line208 a temporary empty implementation, introduced to allow the programmer to make
Line209 progress by deferring effort and intended to be replaced.
Line210 The End-to-End Tests Pass
Line211 Now the end-to-end tests pass: the Sniper can lose without making a bid, and
Line212 lose after making a bid. We can cross off another item on the to-do list, but that
Line213 includes just catching and printing the XMPPException. Normally, we regard this
Line214 as a very bad practice but we wanted to see the tests pass and get some structure
Line215 into the code—and we know that the end-to-end tests will fail anyway if there’s
Line216 a problem sending a message. To make sure we don’t forget, we add another
Line217 to-do item to ﬁnd a better solution, Figure 13.3.
Line218 Chapter 13
Line219 The Sniper Makes a Bid
Line220 130
Line221 
Line222 
Line223 ---
Line224 
Line225 ---
Line226 **Page 131**
Line227 
Line228 Figure 13.3
Line229 One step forward
Line230 Tidying Up the Implementation
Line231 Extracting XMPPAuction
Line232 Our end-to-end test passes, but we haven’t ﬁnished because our new implemen-
Line233 tation feels messy. We notice that the activity in joinAuction() crosses multiple
Line234 domains: managing chats, sending bids, creating snipers, and so on. We need to
Line235 clean up. To start, we notice that we’re sending auction commands from two
Line236 different levels, at the top and from within the Auction. Sending commands to
Line237 an auction sounds like the sort of thing that our Auction object should do, so it
Line238 makes sense to package that up together. We add a new method to the interface,
Line239 extend our anonymous implementation, and then extract it to a (temporarily)
Line240 nested class—for which we need a name. The distinguishing feature of this imple-
Line241 mentation of Auction is that it’s based on the messaging infrastructure, so we
Line242 call our new class XMPPAuction.
Line243 131
Line244 Tidying Up the Implementation
Line245 
Line246 
Line247 ---
