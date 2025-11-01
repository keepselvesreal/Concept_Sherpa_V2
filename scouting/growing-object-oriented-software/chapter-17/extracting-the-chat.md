Line1 # Extracting the Chat (pp.192-195)
Line2 
Line3 ---
Line4 **Page 192**
Line5 
Line6 We think we should extract some of this behavior from Main, and the XMPP
Line7 features look like a good ﬁrst candidate. The use of the Smack should be an
Line8 implementation detail that is irrelevant to the rest of the application.
Line9 Extracting the Chat
Line10 Isolating the Chat
Line11 Most 
Line12 of 
Line13 the 
Line14 action 
Line15 happens 
Line16 in 
Line17 the 
Line18 implementation 
Line19 of
Line20 UserRequestListener.joinAuction() within Main. We notice that we’ve inter-
Line21 leaved different domain levels, auction sniping and chatting, in this one unit of
Line22 code. We’d like to split them up. Here it is again:
Line23 public class Main { […]
Line24   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line25     ui.addUserRequestListener(new UserRequestListener() {
Line26     public void joinAuction(String itemId) {
Line27       snipers.addSniper(SniperSnapshot.joining(itemId));
Line28         Chat chat = connection.getChatManager()
Line29                                  .createChat(auctionId(itemId, connection), null);
Line30         notToBeGCd.add(chat); 
Line31         Auction auction = new XMPPAuction(chat);
Line32 chat.addMessageListener(
Line33                new AuctionMessageTranslator(connection.getUser(),
Line34                      new AuctionSniper(itemId, auction, 
Line35                            new SwingThreadSniperListener(snipers))));
Line36         auction.join();
Line37       }
Line38     });
Line39   }
Line40 }
Line41 The object that locks this code into Smack is the chat; we refer to it several times:
Line42 to avoid garbage collection, to attach it to the Auction implementation, and to
Line43 attach the message listener. If we can gather together the auction- and Sniper-
Line44 related code, we can move the chat elsewhere, but that’s tricky while there’s still
Line45 a dependency loop between the XMPPAuction, Chat, and AuctionSniper.
Line46 Looking again, the Sniper actually plugs in to the AuctionMessageTranslator
Line47 as an AuctionEventListener. Perhaps using an Announcer to bind the two together,
Line48 rather than a direct link, would give us the ﬂexibility we need. It would also make
Line49 sense to have the Sniper as a notiﬁcation, as deﬁned in “Object Peer Stereotypes”
Line50 (page 52). The result is:
Line51 Chapter 17
Line52 Teasing Apart Main
Line53 192
Line54 
Line55 
Line56 ---
Line57 
Line58 ---
Line59 **Page 193**
Line60 
Line61 public class Main { […]
Line62   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line63     ui.addUserRequestListener(new UserRequestListener() {
Line64       public void joinAuction(String itemId) {
Line65         Chat chat = connection.[…]
Line66         Announcer<AuctionEventListener> auctionEventListeners = 
Line67             Announcer.to(AuctionEventListener.class);
Line68         chat.addMessageListener(
Line69             new AuctionMessageTranslator(
Line70                 connection.getUser(),
Line71 auctionEventListeners.announce()));
Line72         notToBeGCd.add(chat);
Line73         Auction auction = new XMPPAuction(chat);
Line74 auctionEventListeners.addListener(
Line75            new AuctionSniper(itemId, auction, new SwingThreadSniperListener(snipers)));
Line76         auction.join();
Line77       }
Line78     }
Line79   }
Line80 }
Line81 This looks worse, but the interesting bit is the last three lines. If you squint, it
Line82 looks like everything is described in terms of Auctions and Snipers (there’s still
Line83 the Swing thread issue, but we did tell you to squint).
Line84 Encapsulating the Chat
Line85 From here, we can push everything to do with chat, its setup, and the use of the
Line86 Announcer, into XMPPAuction, adding management methods to the Auction inter-
Line87 face for its AuctionEventListeners. We’re just showing the end result here, but
Line88 we changed the code incrementally so that nothing was broken for more than a
Line89 few minutes.
Line90 public final class XMPPAuction implements Auction { […]
Line91   private final Announcer<AuctionEventListener> auctionEventListeners = […]
Line92   private final Chat chat;
Line93   public XMPPAuction(XMPPConnection connection, String itemId) {
Line94     chat = connection.getChatManager().createChat(
Line95              auctionId(itemId, connection),
Line96              new AuctionMessageTranslator(connection.getUser(), 
Line97                                           auctionEventListeners.announce()));
Line98   } 
Line99   private static String auctionId(String itemId, XMPPConnection connection) { 
Line100     return String.format(AUCTION_ID_FORMAT, itemId, connection.getServiceName());
Line101   }
Line102 }
Line103 193
Line104 Extracting the Chat
Line105 
Line106 
Line107 ---
Line108 
Line109 ---
Line110 **Page 194**
Line111 
Line112 Apart from the garbage collection “wart,” this removes any references to Chat
Line113 from Main.
Line114 public class Main { […]
Line115   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line116     ui.addUserRequestListener(new UserRequestListener() {
Line117       public void joinAuction(String itemId) {
Line118           snipers.addSniper(SniperSnapshot.joining(itemId));
Line119           Auction auction = new XMPPAuction(connection, itemId);
Line120           notToBeGCd.add(auction);
Line121 auction.addAuctionEventListener(
Line122                   new AuctionSniper(itemId, auction, 
Line123                                     new SwingThreadSniperListener(snipers)));
Line124 auction.join();
Line125       }
Line126     });
Line127   }
Line128 }
Line129 Figure 17.1
Line130 With XMPPAuction extracted
Line131 Writing a New Test
Line132 We also write a new integration test for the expanded XMPPAuction to show that
Line133 it can create a Chat and attach a listener. We use some of our existing end-to-end
Line134 test infrastructure, such as FakeAuctionServer, and a CountDownLatch from the
Line135 Java concurrency libraries to wait for a response.
Line136 Chapter 17
Line137 Teasing Apart Main
Line138 194
Line139 
Line140 
Line141 ---
Line142 
Line143 ---
Line144 **Page 195**
Line145 
Line146 @Test public void
Line147 receivesEventsFromAuctionServerAfterJoining() throws Exception {
Line148   CountDownLatch auctionWasClosed = new CountDownLatch(1);
Line149   Auction auction =  new XMPPAuction(connection, auctionServer.getItemId());
Line150   auction.addAuctionEventListener(auctionClosedListener(auctionWasClosed));
Line151   auction.join();
Line152   server.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line153   server.announceClosed();
Line154   assertTrue("should have been closed", auctionWasClosed.await(2, SECONDS)); 
Line155 } 
Line156 private AuctionEventListener 
Line157 auctionClosedListener(final CountDownLatch auctionWasClosed) {
Line158   return new AuctionEventListener() {
Line159     public void auctionClosed() { auctionWasClosed.countDown(); }
Line160     public void currentPrice(int price, int increment, PriceSource priceSource) { 
Line161 // not implemented
Line162     }
Line163   };
Line164 }
Line165 Looking over the result, we can see that it makes sense for XMPPAuction to en-
Line166 capsulate a Chat as now it hides everything to do with communicating between
Line167 a request listener and an auction service, including translating the messages. We
Line168 can also see that the AuctionMessageTranslator is internal to this encapsulation,
Line169 the Sniper doesn’t need to see it. So, to recognize our new structure, we move
Line170 XMPPAuction and AuctionMessageTranslator into a new auctionsniper.xmpp
Line171 package, and the tests into equivalent xmpp test packages.
Line172 Compromising on a Constructor
Line173 We have one doubt about this implementation: the constructor includes some real
Line174 behavior. Our experience is that busy constructors enforce assumptions that one
Line175 day we will want to break, especially when testing, so we prefer to keep them very
Line176 simple—just setting the ﬁelds. For now, we convince ourselves that this is “veneer”
Line177 code, a bridge to an external library, that can only be integration-tested because
Line178 the Smack classes have just the kind of complicated constructors we try to avoid.
Line179 Extracting the Connection
Line180 The next thing to remove from Main is direct references to the XMPPConnection.
Line181 We can wrap these up in a factory class that will create an instance of an Auction
Line182 for a given item, so it will have a method like
Line183 Auction auction = <factory>.auctionFor(item id);
Line184 195
Line185 Extracting the Connection
Line186 
Line187 
Line188 ---
