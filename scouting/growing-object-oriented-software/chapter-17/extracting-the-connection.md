Line1 # Extracting the Connection (pp.195-197)
Line2 
Line3 ---
Line4 **Page 195**
Line5 
Line6 @Test public void
Line7 receivesEventsFromAuctionServerAfterJoining() throws Exception {
Line8   CountDownLatch auctionWasClosed = new CountDownLatch(1);
Line9   Auction auction =  new XMPPAuction(connection, auctionServer.getItemId());
Line10   auction.addAuctionEventListener(auctionClosedListener(auctionWasClosed));
Line11   auction.join();
Line12   server.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line13   server.announceClosed();
Line14   assertTrue("should have been closed", auctionWasClosed.await(2, SECONDS)); 
Line15 } 
Line16 private AuctionEventListener 
Line17 auctionClosedListener(final CountDownLatch auctionWasClosed) {
Line18   return new AuctionEventListener() {
Line19     public void auctionClosed() { auctionWasClosed.countDown(); }
Line20     public void currentPrice(int price, int increment, PriceSource priceSource) { 
Line21 // not implemented
Line22     }
Line23   };
Line24 }
Line25 Looking over the result, we can see that it makes sense for XMPPAuction to en-
Line26 capsulate a Chat as now it hides everything to do with communicating between
Line27 a request listener and an auction service, including translating the messages. We
Line28 can also see that the AuctionMessageTranslator is internal to this encapsulation,
Line29 the Sniper doesn’t need to see it. So, to recognize our new structure, we move
Line30 XMPPAuction and AuctionMessageTranslator into a new auctionsniper.xmpp
Line31 package, and the tests into equivalent xmpp test packages.
Line32 Compromising on a Constructor
Line33 We have one doubt about this implementation: the constructor includes some real
Line34 behavior. Our experience is that busy constructors enforce assumptions that one
Line35 day we will want to break, especially when testing, so we prefer to keep them very
Line36 simple—just setting the ﬁelds. For now, we convince ourselves that this is “veneer”
Line37 code, a bridge to an external library, that can only be integration-tested because
Line38 the Smack classes have just the kind of complicated constructors we try to avoid.
Line39 Extracting the Connection
Line40 The next thing to remove from Main is direct references to the XMPPConnection.
Line41 We can wrap these up in a factory class that will create an instance of an Auction
Line42 for a given item, so it will have a method like
Line43 Auction auction = <factory>.auctionFor(item id);
Line44 195
Line45 Extracting the Connection
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 196**
Line52 
Line53 We struggle for a while over what to call this new type, since it should have a
Line54 name that reﬂects the language of auctions. In the end, we decide that the concept
Line55 that arranges auctions is an “auction house,” so that’s what we call our new type:
Line56 public interface AuctionHouse {
Line57   Auction auctionFor(String itemId);
Line58 }
Line59 The end result of this refactoring is:
Line60 public class Main { […]
Line61   public static void main(String... args) throws Exception {
Line62     Main main = new Main();
Line63 XMPPAuctionHouse auctionHouse = 
Line64       XMPPAuctionHouse.connect(
Line65         args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
Line66     main.disconnectWhenUICloses(auctionHouse);
Line67     main.addUserRequestListenerFor(auctionHouse);
Line68   }
Line69   private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
Line70     ui.addUserRequestListener(new UserRequestListener() {
Line71       public void joinAuction(String itemId) {
Line72         snipers.addSniper(SniperSnapshot.joining(itemId));
Line73 Auction auction = auctionHouse.auctionFor(itemId);
Line74         notToBeGCd.add(auction);
Line75 […]
Line76       }
Line77     }
Line78   }
Line79 }
Line80 Figure 17.2
Line81 With XMPPAuctionHouse extracted
Line82 Chapter 17
Line83 Teasing Apart Main
Line84 196
Line85 
Line86 
Line87 ---
Line88 
Line89 ---
Line90 **Page 197**
Line91 
Line92 Implementing XMPPAuctionHouse is straightforward; we transfer there all the
Line93 code related to connection, including the generation of the Jabber ID from
Line94 the auction item ID. Main is now simpler, with just one import for all the XMPP
Line95 code, auctionsniper.xmpp.XMPPAuctionHouse. The new version looks like
Line96 Figure 17.2.
Line97 For consistency, we retroﬁt XMPPAuctionHouse to the integration test for
Line98 XMPPAuction, instead of creating XMPPAuctions directly as it does now, and rename
Line99 the test to XMPPAuctionHouseTest.
Line100 Our ﬁnal touch is to move the relevant constants from Main where we’d left
Line101 them: the message formats to XMPPAuction and the connection identiﬁer format
Line102 to XMPPAuctionHouse. This reassures us that we’re moving in the right direction,
Line103 since we’re narrowing the scope of where these constants are used.
Line104 Extracting the SnipersTableModel
Line105 Sniper Launcher
Line106 Finally, we’d like to do something about the direct reference to the
Line107 SnipersTableModel and the related SwingThreadSniperListener—and the awful
Line108 notToBeGCd. We think we can get there, but it’ll take a couple of steps.
Line109 The ﬁrst step is to turn the anonymous implementation of UserRequestListener
Line110 into a proper class so we can understand its dependencies. We decide to call the
Line111 new class SniperLauncher, since it will respond to a request to join an auction
Line112 by “launching” a Sniper. One nice effect is that we can make notToBeGCd local
Line113 to the new class.
Line114 public class SniperLauncher implements UserRequestListener {
Line115   private final ArrayList<Auction> notToBeGCd = new ArrayList<Auction>();
Line116   private final AuctionHouse auctionHouse;
Line117   private final SnipersTableModel snipers;
Line118   public SniperLauncher(AuctionHouse auctionHouse, SnipersTableModel snipers) {
Line119 // set the fields 
Line120   }
Line121   public void joinAuction(String itemId) {
Line122 snipers.addSniper(SniperSnapshot.joining(itemId));
Line123       Auction auction = auctionHouse.auctionFor(itemId);
Line124       notToBeGCd.add(auction);
Line125       AuctionSniper sniper = 
Line126         new AuctionSniper(itemId, auction, 
Line127                           new SwingThreadSniperListener(snipers));
Line128       auction.addAuctionEventListener(snipers);
Line129       auction.join();
Line130   }
Line131 }
Line132 With the SniperLauncher separated out, it becomes even clearer that the
Line133 Swing features don’t ﬁt here. There’s a clue in that our use of snipers, the
Line134 197
Line135 Extracting the SnipersTableModel
Line136 
Line137 
Line138 ---
