Line1 # Introducing AuctionSniper (pp.123-126)
Line2 
Line3 ---
Line4 **Page 123**
Line5 
Line6 Chapter 13
Line7 The Sniper Makes a Bid
Line8 In which we extract an AuctionSniper class and tease out its dependen-
Line9 cies. We plug our new class into the rest of the application, using an
Line10 empty implementation of auction until we’re ready to start sending
Line11 commands. We close the loop back to the auction house with an
Line12 XMPPAuction class. We continue to carve new types out of the code.
Line13 Introducing AuctionSniper
Line14 A New Class, with Dependencies
Line15 Our application accepts Price events from the auction, but cannot interpret them
Line16 yet. We need code that will perform two actions when the currentPrice() method
Line17 is called: send a higher bid to the auction and update the status in the user inter-
Line18 face. We could extend Main, but that class is looking rather messy—it’s already
Line19 doing too many things at once. It feels like this is a good time to introduce
Line20 what we should call an “Auction Sniper,” the component at the heart of our
Line21 application, so we create an AuctionSniper class. Some of its intended behavior
Line22 is currently buried in Main, and a good start would be to extract it into our new
Line23 class—although, as we’ll see in a moment, it will take a little effort.
Line24 Given that an AuctionSniper should respond to Price events, we decide to
Line25 make it implement AuctionEventListener rather than Main. The question is what
Line26 to do about the user interface. If we consider moving this method:
Line27 public void auctionClosed() {
Line28   SwingUtilities.invokeLater(new Runnable() {
Line29     public void run() {
Line30        ui.showStatus(MainWindow.STATUS_LOST);
Line31     }
Line32   });
Line33 }
Line34 does it really make sense for an AuctionSniper to know about the implementation
Line35 details of the user interface, such as the use of the Swing thread? We’d be at risk
Line36 of breaking the “single responsibility” principle again. Surely an AuctionSniper
Line37 ought to be concerned with bidding policy and only notify status changes in
Line38 its terms?
Line39 123
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 124**
Line46 
Line47 Our solution is to insulate the AuctionSniper by introducing a new relationship:
Line48 it will notify a SniperListener of changes in its status. The interface and the ﬁrst
Line49 unit test look like this:
Line50 public interface SniperListener extends EventListener {
Line51   void sniperLost();
Line52 }
Line53 @RunWith(JMock.class)
Line54 public class AuctionSniperTest {
Line55   private final Mockery context = new Mockery();
Line56   private final SniperListener sniperListener = 
Line57                                       context.mock(SniperListener.class);
Line58   private final AuctionSniper sniper = new AuctionSniper(sniperListener);
Line59   @Test public void
Line60 reportsLostWhenAuctionCloses() {
Line61     context.checking(new Expectations() {{
Line62       one(sniperListener).sniperLost();
Line63     }});
Line64     sniper.auctionClosed();
Line65   }
Line66 }
Line67 which says that Sniper should report that it has lost if it receives a Close event
Line68 from the auction.
Line69 The failure report says:
Line70 not all expectations were satisfied
Line71 expectations:
Line72 ! expected exactly 1 time, never invoked: SniperListener.sniperLost();
Line73 which we can make pass with a simple implementation:
Line74 public class AuctionSniper implements AuctionEventListener {
Line75   private final SniperListener sniperListener;
Line76   public AuctionSniper(SniperListener sniperListener) {
Line77     this.sniperListener = sniperListener;
Line78   }
Line79 public void auctionClosed() {
Line80     sniperListener.sniperLost();
Line81   }
Line82   public void currentPrice(int price, int increment) {
Line83 // TODO Auto-generated method stub
Line84   }
Line85 }
Line86 Finally, we retroﬁt the new AuctionSniper by having Main implement
Line87 SniperListener.
Line88 Chapter 13
Line89 The Sniper Makes a Bid
Line90 124
Line91 
Line92 
Line93 ---
Line94 
Line95 ---
Line96 **Page 125**
Line97 
Line98 public class Main implements SniperListener { […]
Line99   private void joinAuction(XMPPConnection connection, String itemId) 
Line100     throws XMPPException 
Line101   {
Line102     disconnectWhenUICloses(connection);
Line103     Chat chat = connection.getChatManager().createChat(
Line104         auctionId(itemId, connection), 
Line105         new AuctionMessageTranslator(new AuctionSniper(this)));
Line106     this.notToBeGCd = chat;
Line107     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line108   }
Line109   public void sniperLost() {
Line110     SwingUtilities.invokeLater(new Runnable() {
Line111       public void run() {
Line112         ui.showStatus(MainWindow.STATUS_LOST);
Line113       }
Line114     });
Line115   }
Line116 }
Line117 Our working end-to-end test still passes and our broken one still fails at the
Line118 same place, so we haven’t made things worse. The new structure looks like
Line119 Figure 13.1.
Line120 Figure 13.1
Line121 Plugging in the AuctionSniper
Line122 Focus, Focus, Focus
Line123 Once again, we’ve noticed complexity in a class and used that to tease out a new
Line124 concept from our initial skeleton implementation. Now we have a Sniper to re-
Line125 spond to events from the translator. As you’ll see shortly, this is a better structure
Line126 for expressing what the code does and for unit testing. We also think that the
Line127 sniperLost() method is clearer than its previous incarnation, auctionClosed(),
Line128 since there’s now a closer match between its name and what it does—that is,
Line129 reports a lost auction.
Line130 Isn’t this wasteful ﬁddling, gold-plating the code while time slips by? Obviously
Line131 we don’t think so, especially when we’re sorting out our ideas this early in the
Line132 project. There are teams that overdo their design effort, but our experience is
Line133 that most teams spend too little time clarifying the code and pay for it in mainte-
Line134 nance overhead. As we’ve shown a couple of times now, the “single responsibil-
Line135 ity” principle is a very effective heuristic for breaking up complexity, and
Line136 125
Line137 Introducing AuctionSniper
Line138 
Line139 
Line140 ---
Line141 
Line142 ---
Line143 **Page 126**
Line144 
Line145 developers shouldn’t be shy about creating new types. We think Main still does
Line146 too much, but we’re not yet sure how best to break it up. We decide to push on
Line147 and see where the code takes us.
Line148 Sending a Bid
Line149 An Auction Interface
Line150 The next step is to have the Sniper send a bid to the auction, so who should the
Line151 Sniper talk to? Extending the SniperListener feels wrong because that relationship
Line152 is about tracking what’s happening in the Sniper, not about making external
Line153 commitments. In the terms deﬁned in “Object Peer Stereotypes” (page 52),
Line154 SniperListener is a notiﬁcation, not a dependency.
Line155 After the usual discussion, we decide to introduce a new collaborator, an
Line156 Auction. Auction and SniperListener represent two different domains in the
Line157 application: Auction is about ﬁnancial transactions, it accepts bids for items in
Line158 the market; and SniperListener is about feedback to the application, it reports
Line159 changes to the current state of the Sniper. The Auction is a dependency, for a
Line160 Sniper cannot function without one, whereas the SniperListener, as we
Line161 discussed above, is not. Introducing the new interface makes the design look like
Line162 Figure 13.2.
Line163 Figure 13.2
Line164 Introducing Auction
Line165 The AuctionSniper Bids
Line166 Now we’re ready to start bidding. The ﬁrst step is to implement the response to
Line167 a Price event, so we start by adding a new unit test for the AuctionSniper. It
Line168 says that the Sniper, when it receives a Price update, sends an incremented bid
Line169 to the auction. It also notiﬁes its listener that it’s now bidding, so we add a
Line170 sniperBidding() method. We’re making an implicit assumption that the Auction
Line171 knows which bidder the Sniper represents, so the Sniper does not have to pass
Line172 in that information with the bid.
Line173 Chapter 13
Line174 The Sniper Makes a Bid
Line175 126
Line176 
Line177 
Line178 ---
