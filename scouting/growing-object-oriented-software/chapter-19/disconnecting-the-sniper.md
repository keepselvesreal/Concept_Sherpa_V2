Line1 # Disconnecting the Sniper (pp.219-221)
Line2 
Line3 ---
Line4 **Page 219**
Line5 
Line6 We’ve added a couple more helper methods: ignoringAuction() says that we
Line7 don’t care what happens to auction, allowing events to pass through so we can
Line8 get to the failure; and, expectSniperToFailWhenItIs() describes what a failure
Line9 should look like, including the previous state of the Sniper.
Line10 All we have to do is add a failed() transition to SniperSnapshot and use it
Line11 in the new method.
Line12 public class AuctionSniper implements AuctionEventListener {
Line13   public void auctionFailed() {
Line14     snapshot = snapshot.failed();
Line15     listeners.announce().sniperStateChanged(snapshot);
Line16   } […]
Line17 public class SniperSnapshot {
Line18   public SniperSnapshot failed() {
Line19     return new SniperSnapshot(itemId, 0, 0, SniperState.FAILED);
Line20   } […]
Line21 This displays the failure, as we can see in Figure 19.1.
Line22 Figure 19.1
Line23 The Sniper shows a failed auction
Line24 The end-to-end test, however, still fails. The synchronization hook we added
Line25 reveals that we haven’t disconnected the Sniper from receiving further events
Line26 from the auction.
Line27 Disconnecting the Sniper
Line28 We turn off a Sniper by removing its AuctionMessageTranslator from its Chat’s
Line29 set of MessageListeners. We can do this safely while processing a message because
Line30 Chat stores its listeners in a thread-safe “copy on write” collection. One obvious
Line31 place to do this is within processMessage() in AuctionMessageTranslator, which
Line32 receives the Chat as an argument, but we have two doubts about this. First, as
Line33 we pointed out in Chapter 12, constructing a real Chat is painful. Most of the
Line34 mocking frameworks support creating a mock class, but it makes us uncomfort-
Line35 able because then we’re deﬁning a relationship with an implementation, not a
Line36 role—we’re being too precise about our dependencies. Second, we might be as-
Line37 signing too many responsibilities to AuctionMessageTranslator; it would have
Line38 to translate the message and decide what to do when it fails.
Line39 219
Line40 Disconnecting the Sniper
Line41 
Line42 
Line43 ---
Line44 
Line45 ---
Line46 **Page 220**
Line47 
Line48 Our alternative approach is to attach another object to the translator that im-
Line49 plements this disconnection policy, using the infrastructure we already have for
Line50 notifying AuctionEventListeners.
Line51 public final class XMPPAuction implements Auction {
Line52   public XMPPAuction(XMPPConnection connection, String auctionJID) {
Line53     AuctionMessageTranslator translator = translatorFor(connection);
Line54     this.chat = connection.getChatManager().createChat(auctionJID, translator);
Line55     addAuctionEventListener(chatDisconnectorFor(translator));
Line56   }
Line57   private AuctionMessageTranslator translatorFor(XMPPConnection connection) {
Line58     return new AuctionMessageTranslator(connection.getUser(), 
Line59                                         auctionEventListeners.announce());
Line60   }
Line61 z
Line62   private AuctionEventListener 
Line63 chatDisconnectorFor(final AuctionMessageTranslator translator) {
Line64     return new AuctionEventListener() {
Line65       public void auctionFailed() { 
Line66 chat.removeMessageListener(translator);
Line67       }
Line68       public void auctionClosed(// empty method
Line69       public void currentPrice( // empty method
Line70     };
Line71   } […]
Line72 The end-to-end test, as far as it goes, passes.
Line73 The Composition Shell Game
Line74 The issue in this design episode is not the fundamental complexity of the feature,
Line75 which is constant, but how we divide it up. The design we chose (attaching a dis-
Line76 connection listener) could be argued to be more complicated than its alternative
Line77 (detaching the chat within the translator). It certainly takes more lines of code, but
Line78 that’s not the only metric. Instead, we’re emphasizing the “single responsibility”
Line79 principle, which means each object does just one thing well and the system behavior
Line80 comes from how we assemble those objects.
Line81 Sometimes this feels as if the behavior we’re looking for is always somewhere else
Line82 (as Gertrude Stein said, “There is no there there”), which can be frustrating for
Line83 developers not used to the style. Our experience, on the other hand, is that focused
Line84 responsibilities make the code more maintainable because we don’t have to cut
Line85 through unrelated functionality to get to the piece we need. See Chapter 6 for a
Line86 longer discussion.
Line87 Chapter 19
Line88 Handling Failure
Line89 220
Line90 
Line91 
Line92 ---
Line93 
Line94 ---
Line95 **Page 221**
Line96 
Line97 Recording the Failure
Line98 Now we want to return to the end-to-end test and the reportsInvalidMessage()
Line99 method that we parked. Our requirement is that the Sniper application must log
Line100 a message about these failures so that the user’s organization can recover the
Line101 situation. This means that our test should look for a log ﬁle and check its contents.
Line102 Filling In the Test
Line103 We implement the missing check and ﬂush the log before each test, delegating
Line104 the management of the log ﬁle to an AuctionLogDriver class which uses the
Line105 Apache Commons IO library. It also cheats slightly by resetting the log manager
Line106 (we’re not really supposed to be in the same address space), since deleting the
Line107 log ﬁle can confuse a cached logger.
Line108 public class ApplicationRunner { […]
Line109 private AuctionLogDriver logDriver = new AuctionLogDriver();
Line110   public void reportsInvalidMessage(FakeAuctionServer auction, String message)
Line111     throws IOException 
Line112   {
Line113 logDriver.hasEntry(containsString(message));
Line114   }
Line115   public void startBiddingWithStopPrice(FakeAuctionServer auction, int stopPrice) {
Line116     startSniper();
Line117     openBiddingFor(auction, stopPrice);
Line118   }  
Line119   private startSniper() {
Line120 logDriver.clearLog()
Line121     Thread thread = new Thread("Test Application") {
Line122       @Override public void run() { // Start the application […]
Line123   }
Line124 }
Line125 public class AuctionLogDriver {
Line126   public static final String LOG_FILE_NAME = "auction-sniper.log";
Line127   private final File logFile = new File(LOG_FILE_NAME);
Line128   public void hasEntry(Matcher<String> matcher) throws IOException  {
Line129     assertThat(FileUtils.readFileToString(logFile), matcher); 
Line130   }
Line131   public void clearLog() {
Line132     logFile.delete();
Line133     LogManager.getLogManager().reset(); 
Line134   }
Line135 }
Line136 This new check only reassures us that we’ve fed a message through the system
Line137 and into some kind of log record—it tells us that the pieces ﬁt together. We’ll
Line138 write a more thorough test of the contents of a log record later. The end-to-end
Line139 test now fails because, of course, there’s no log ﬁle to read.
Line140 221
Line141 Recording the Failure
Line142 
Line143 
Line144 ---
