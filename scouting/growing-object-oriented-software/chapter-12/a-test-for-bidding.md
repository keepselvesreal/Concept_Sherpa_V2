Line1 # A Test for Bidding (pp.106-112)
Line2 
Line3 ---
Line4 **Page 106**
Line5 
Line6 A Test for Bidding
Line7 Starting with a Test
Line8 Each acceptance test we write should have just enough new requirements to force
Line9 a manageable increase in functionality, so we decide that the next one will add
Line10 some price information. The steps are:
Line11 1.
Line12 Tell the auction to send a price to the Sniper.
Line13 2.
Line14 Check the Sniper has received and responded to the price.
Line15 3.
Line16 Check the auction has received an incremented bid from Sniper.
Line17 To make this pass, the Sniper will have to distinguish between Price and Close
Line18 events from the auction, display the current price, and generate a new bid. We’ll
Line19 also have to extend our stub auction to handle bids. We’ve deferred implementing
Line20 other functionality that will also be required, such as displaying when the Sniper
Line21 has won the auction; we’ll get to that later. Here’s the new test:
Line22 public class AuctionSniperEndToEndTest {
Line23   @Test public void
Line24 sniperMakesAHigherBidButLoses() throws Exception {
Line25     auction.startSellingItem();
Line26     application.startBiddingIn(auction);
Line27     auction.hasReceivedJoinRequestFromSniper(); 1
Line28     auction.reportPrice(1000, 98, "other bidder"); 2
Line29     application.hasShownSniperIsBidding(); 3
Line30     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID); 4
Line31     auction.announceClosed(); 5
Line32     application.showsSniperHasLostAuction();   
Line33   }
Line34 }
Line35 We have three new methods to implement as part of this test.
Line36 1
Line37 We have to wait for the stub auction to receive the Join request before con-
Line38 tinuing with the test. We use this assertion to synchronize the Sniper with
Line39 the auction.
Line40 2
Line41 This method tells the stub auction to send a message back to the Sniper with
Line42 the news that at the moment the price of the item is 1000, the increment for
Line43 the next bid is 98, and the winning bidder is “other bidder.”
Line44 3
Line45 This method asks the ApplicationRunner to check that the Sniper shows that
Line46 it’s now bidding after it’s received the price update message from the auction.
Line47 Chapter 12
Line48 Getting Ready to Bid
Line49 106
Line50 
Line51 
Line52 ---
Line53 
Line54 ---
Line55 **Page 107**
Line56 
Line57 4
Line58 This method asks the stub auction to check that it has received a bid from
Line59 the Sniper that is equal to the last price plus the minimum increment. We
Line60 have to do a fraction more work because the XMPP layer constructs a longer
Line61 name from the basic identiﬁer, so we deﬁne a constant SNIPER_XMPP_ID which
Line62 in practice is sniper@localhost/Auction.
Line63 5
Line64 We reuse the closing logic from the ﬁrst test, as the Sniper still loses the
Line65 auction.
Line66 Unrealistic Money
Line67 We’re using integers to represent value (imagine that auctions are conducted in
Line68 Japanese Yen). In a real system, we would deﬁne a domain type to represent
Line69 monetary values, using a ﬁxed decimal implementation. Here, we simplify the
Line70 representation to make the example code easier to ﬁt onto a printed page.
Line71 Extending the Fake Auction
Line72 We have two methods to write in the FakeAuctionServer to support the end-
Line73 to-end test: reportPrice() has to send a Price message through the chat;
Line74 hasReceivedBid() is a little more complex—it has to check that the auction re-
Line75 ceived the right values from the Sniper. Instead of parsing the incoming message,
Line76 we construct the expected message and just compare strings. We also pull up the
Line77 Matcher clause from the SingleMessageListener to give the FakeAuctionServer
Line78 more ﬂexibility in deﬁning what it will accept as a message. Here’s a ﬁrst cut:
Line79 public class FakeAuctionServer { […]
Line80   public void reportPrice(int price, int increment, String bidder) 
Line81     throws XMPPException 
Line82   {
Line83     currentChat.sendMessage(
Line84         String.format("SOLVersion: 1.1; Event: PRICE; "
Line85                       + "CurrentPrice: %d; Increment: %d; Bidder: %s;",
Line86                       price, increment, bidder));
Line87   }
Line88   public void hasReceivedJoinRequestFromSniper() throws InterruptedException {
Line89     messageListener.receivesAMessage(is(anything()));
Line90   }
Line91   public void hasReceivedBid(int bid, String sniperId) 
Line92     throws InterruptedException 
Line93   {
Line94     assertThat(currentChat.getParticipant(), equalTo(sniperId));
Line95     messageListener.receivesAMessage(
Line96       equalTo(
Line97         String.format("SOLVersion: 1.1; Command: BID; Price: %d;", bid)));
Line98   }
Line99 }
Line100 107
Line101 A Test for Bidding
Line102 
Line103 
Line104 ---
Line105 
Line106 ---
Line107 **Page 108**
Line108 
Line109 public class SingleMessageListener implements MessageListener { […]
Line110   @SuppressWarnings("unchecked")
Line111   public void receivesAMessage(Matcher<? super String> messageMatcher) 
Line112     throws InterruptedException 
Line113   {
Line114     final Message message = messages.poll(5, TimeUnit.SECONDS);
Line115     assertThat("Message", message, is(notNullValue()));
Line116     assertThat(message.getBody(), messageMatcher);
Line117   }
Line118 }
Line119 Looking again, there’s an imbalance between the two “receives” methods. The
Line120 Join method is much more lax than the bid message, in terms of both the contents
Line121 of the message and the sender; we will have to remember to come back later and
Line122 ﬁx it. We defer a great many decisions when developing incrementally, but
Line123 sometimes consistency and symmetry make more sense. We decide to retroﬁt
Line124 more detail into hasReceivedJoinRequestFromSniper() while we have the code
Line125 cracked open. We also extract the message formats and move them to Main
Line126 because we’ll need them to construct raw messages in the Sniper.
Line127 public class FakeAuctionServer { […]
Line128   public void hasReceivedJoinRequestFrom(String sniperId) 
Line129     throws InterruptedException 
Line130   {
Line131 receivesAMessageMatching(sniperId, equalTo(Main.JOIN_COMMAND_FORMAT));
Line132   }
Line133   public void hasReceivedBid(int bid, String sniperId) 
Line134     throws InterruptedException 
Line135   {
Line136 receivesAMessageMatching(sniperId, 
Line137                              equalTo(format(Main.BID_COMMAND_FORMAT, bid)));
Line138   }
Line139   private void receivesAMessageMatching(String sniperId, 
Line140                                         Matcher<? super String> messageMatcher)
Line141     throws InterruptedException 
Line142   {
Line143     messageListener.receivesAMessage(messageMatcher);
Line144     assertThat(currentChat.getParticipant(), equalTo(sniperId));
Line145   }
Line146 }
Line147 Notice that we check the Sniper’s identiﬁer after we check the contents of the
Line148 message. This forces the server to wait until the message has arrived, which means
Line149 that it must have accepted a connection and set up currentChat. Otherwise the
Line150 test would fail by checking the Sniper’s identiﬁer prematurely.
Line151 Chapter 12
Line152 Getting Ready to Bid
Line153 108
Line154 
Line155 
Line156 ---
Line157 
Line158 ---
Line159 **Page 109**
Line160 
Line161 Double-Entry Values
Line162 We’re using the same constant to both create a Join message and check its con-
Line163 tents. By using the same construct, we’re removing duplication and expressing in
Line164 the code a link between the two sides of the system. On the other hand, we’re
Line165 making ourselves vulnerable to getting them both wrong and not having a test to
Line166 catch the invalid content. In this case, the code is so simple that pretty much any
Line167 implementation would do, but the answers become less certain when developing
Line168 something more complex, such as a persistence layer. Do we use the same
Line169 framework to write and read our values? Can we be sure that it’s not just caching
Line170 the results, or that the values are persisted correctly? Should we just write some
Line171 straight database queries to be sure?
Line172 The critical question is, what do we think we’re testing? Here, we think that the
Line173 communication features are more important, that the messages are simple enough
Line174 so we can rely on string constants, and that we’d like to be able to ﬁnd code related
Line175 to message formats in the IDE. Other developers might come to a different
Line176 conclusion and be right for their project.
Line177 We adjust the end-to-end tests to match the new API, watch the test fail, and
Line178 then add the extra detail to the Sniper to make the test pass.
Line179 public class AuctionSniperEndToEndTest {
Line180   @Test public void
Line181 sniperMakesAHigherBidButLoses() throws Exception {
Line182     auction.startSellingItem();
Line183     application.startBiddingIn(auction);
Line184 auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line185     auction.reportPrice(1000, 98, "other bidder");
Line186     application.hasShownSniperIsBidding();
Line187     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line188     auction.announceClosed();                  
Line189     application.showsSniperHasLostAuction();   
Line190   }
Line191 }
Line192 109
Line193 A Test for Bidding
Line194 
Line195 
Line196 ---
Line197 
Line198 ---
Line199 **Page 110**
Line200 
Line201 public class Main { […]
Line202   private void joinAuction(XMPPConnection connection, String itemId) 
Line203     throws XMPPException 
Line204   {
Line205     Chat chat = connection.getChatManager().createChat(
Line206         auctionId(itemId, connection), 
Line207         new MessageListener() {
Line208           public void processMessage(Chat aChat, Message message) {
Line209             SwingUtilities.invokeLater(new Runnable() {
Line210               public void run() {
Line211                 ui.showStatus(MainWindow.STATUS_LOST);
Line212               }
Line213             });
Line214           }
Line215         });
Line216     this.notToBeGCd = chat;
Line217     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line218   }
Line219 }
Line220 A Surprise Failure
Line221 Finally we write the “checking” method on the ApplicationRunner to give us
Line222 our ﬁrst failure. The implementation is simple: we just add another status constant
Line223 and copy the existing method.
Line224 public class ApplicationRunner { […]
Line225 public void hasShownSniperIsBidding() {
Line226     driver.showsSniperStatus(MainWindow.STATUS_BIDDING);
Line227   }
Line228   public void showsSniperHasLostAuction() {
Line229     driver.showsSniperStatus(MainWindow.STATUS_LOST);
Line230   }
Line231 }
Line232 We’re expecting to see something about a missing label text but instead we
Line233 get this:
Line234 java.lang.AssertionError: 
Line235 Expected: is not null
Line236      got: null
Line237 […]
Line238   at auctionsniper.SingleMessageListener.receivesAMessage()
Line239   at auctionsniper.FakeAuctionServer.hasReceivedJoinRequestFromSniper()
Line240   at auctionsniper.AuctionSniperEndToEndTest.sniperMakesAHigherBid()
Line241 […]
Line242 and this on the error stream:
Line243 Chapter 12
Line244 Getting Ready to Bid
Line245 110
Line246 
Line247 
Line248 ---
Line249 
Line250 ---
Line251 **Page 111**
Line252 
Line253 conflict(409)
Line254   at jivesoftware.smack.SASLAuthentication.bindResourceAndEstablishSession()
Line255   at jivesoftware.smack.SASLAuthentication.authenticate()
Line256   at jivesoftware.smack.XMPPConnection.login()
Line257   at jivesoftware.smack.XMPPConnection.login()
Line258   at auctionsniper.Main.connection()
Line259   at auctionsniper.Main.main()
Line260 After some investigation we realize what’s happened. We’ve introduced a second
Line261 test which tries to connect using the same account and resource name as the ﬁrst.
Line262 The server is conﬁgured, like Southabee’s On-Line, to reject multiple open con-
Line263 nections, so the second test fails because the server thinks that the ﬁrst is still
Line264 connected. In production, our application would work because we’d stop the
Line265 whole process when closing, which would break the connection. Our little com-
Line266 promise (of starting the application in a new thread) has caught us out. The Right
Line267 Thing to do here is to add a callback to disconnect the client when we close the
Line268 window so that the application will clean up after itself:
Line269 public class Main { […]
Line270   private void joinAuction(XMPPConnection connection, String itemId) 
Line271     throws XMPPException 
Line272   {
Line273 disconnectWhenUICloses(connection);
Line274     Chat chat = connection.getChatManager().createChat(
Line275 […]
Line276     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line277   }
Line278   private void disconnectWhenUICloses(final XMPPConnection connection) {
Line279     ui.addWindowListener(new WindowAdapter() {
Line280       @Override public void windowClosed(WindowEvent e) {
Line281 connection.disconnect();
Line282       }
Line283     });
Line284   }
Line285 }
Line286 Now we get the failure we expected, because the Sniper has no way to start
Line287 bidding.
Line288 java.lang.AssertionError: 
Line289 Tried to look for...
Line290     exactly 1 JLabel (with name "sniper status")
Line291     in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line292     in all top level windows
Line293 and check that its label text is "Bidding"
Line294 but...
Line295     all top level windows
Line296     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line297     contained 1 JLabel (with name "sniper status")
Line298 label text was "Lost"
Line299 […]
Line300   at auctionsniper.AuctionSniperDriver.showsSniperStatus()
Line301   at auctionsniper.ApplicationRunner.hasShownSniperIsBidding()
Line302   at auctionsniper.AuctionSniperEndToEndTest.sniperMakesAHigherBidButLoses()
Line303 111
Line304 A Test for Bidding
Line305 
Line306 
Line307 ---
Line308 
Line309 ---
Line310 **Page 112**
Line311 
Line312 Outside-In Development
Line313 This failure deﬁnes the target for our next coding episode. It tells us, at a high
Line314 level, what we’re aiming for—we just have to ﬁll in implementation until it
Line315 passes.
Line316 Our approach to test-driven development is to start with the outside event that
Line317 triggers the behavior we want to implement and work our way into the code an
Line318 object at a time, until we reach a visible effect (such as a sent message or log entry)
Line319 indicating that we’ve achieved our goal. The end-to-end test shows us the end
Line320 points of that process, so we can explore our way through the space in the middle.
Line321 In the following sections, we build up the types we need to implement our
Line322 Auction Sniper. We’ll take it slowly, strictly by the TDD rules, to show how the
Line323 process works. In real projects, we sometimes design a bit further ahead to get
Line324 a sense of the bigger picture, but much of the time this is what we actually do.
Line325 It produces the right results and forces us to ask the right questions.
Line326 Inﬁnite Attention to Detail?
Line327 We caught the resource clash because, by luck or insight, our server conﬁguration
Line328 matched that of Southabee’s On-Line. We might have used an alternative setting
Line329 which allows new connections to kick off existing ones, which would have resulted
Line330 in the tests passing but with a confusing conﬂict message from the Smack library
Line331 on the error stream. This would have worked ﬁne in development, but with a
Line332 risk of Snipers starting to fail in production.
Line333 How can we hope to catch all the conﬁguration options in an entire system?
Line334 At some level we can’t, and this is at the heart of what professional testers do.
Line335 What we can do is push to exercise as much as possible of the system as early as
Line336 possible, and to do so repeatedly. We can also help ourselves cope with total
Line337 system complexity by keeping the quality of its components high and by constantly
Line338 pushing to simplify. If that sounds expensive, consider the cost of ﬁnding and
Line339 ﬁxing a transient bug like this one in a busy production system.
Line340 The AuctionMessageTranslator
Line341 Teasing Out a New Class
Line342 Our entry point to the Sniper is where we receive a message from the auction
Line343 through the Smack library: it’s the event that triggers the next round of behavior
Line344 we want to make work. In practice, this means that we need a class implementing
Line345 MessageListener to attach to the Chat. When this class receives a raw message
Line346 from the auction, it will translate it into something that represents an auction
Line347 event within our code which, eventually, will prompt a Sniper action and a change
Line348 in the user interface.
Line349 Chapter 12
Line350 Getting Ready to Bid
Line351 112
Line352 
Line353 
Line354 ---
