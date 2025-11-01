Line1 # Building the Test Rig (pp.89-95)
Line2 
Line3 ---
Line4 **Page 89**
Line5 
Line6 Chapter 11
Line7 Passing the First Test
Line8 In which we write test infrastructure to drive our non-existent applica-
Line9 tion, so that we can make the ﬁrst test fail. We repeatedly fail the test
Line10 and ﬁx symptoms, until we have a minimal working application that
Line11 passes the ﬁrst test. We step through this very slowly to show how the
Line12 process works.
Line13 Building the Test Rig
Line14 At the start of every test run, our test script starts up the Openﬁre server, creates
Line15 accounts for the Sniper and the auction, and then runs the tests. Each test will
Line16 start instances of the application and the fake auction, and then test their com-
Line17 munication through the server. At ﬁrst, we’ll run everything on the same host.
Line18 Later, as the infrastructure stabilizes, we can consider running different compo-
Line19 nents on different machines, which will be a better match to the real deployment.
Line20 This leaves us with two components to write for the test infrastructure:
Line21 ApplicationRunner and FakeAuctionServer.
Line22 Setting Up the Openﬁre Server
Line23 At the time of writing, we were using version 3.6 of Openﬁre. For these end-to-
Line24 end tests, we set up our local server with three user accounts and passwords:
Line25 sniper
Line26 sniper
Line27 auction-item-54321
Line28 auction
Line29 auction-item-65432
Line30 auction
Line31 For desktop development, we usually started the server by hand and left it running.
Line32 We set it up to not store ofﬂine messages, which meant there was no persistent
Line33 state. In the System Manager, we edited the “System Name” property to be
Line34 localhost, so the tests would run consistently. Finally, we set the resource policy
Line35 to “Never kick,” which will not allow a new resource to log in if there’s a conﬂict.
Line36 89
Line37 
Line38 
Line39 ---
Line40 
Line41 ---
Line42 **Page 90**
Line43 
Line44 The Application Runner
Line45 An ApplicationRunner is an object that wraps up all management and commu-
Line46 nicating with the Swing application we’re building. It runs the application as if
Line47 from the command line, obtaining and holding a reference to its main window
Line48 for querying the state of the GUI and for shutting down the application at the
Line49 end of the test.
Line50 We don’t have to do much here, because we can rely on WindowLicker to do
Line51 the hard work: ﬁnd and control Swing GUI components, synchronize with
Line52 Swing’s threads and event queue, and wrap that all up behind a simple API.1
Line53 WindowLicker has the concept of a ComponentDriver: an object that can manip-
Line54 ulate a feature in a Swing user interface. If a ComponentDriver can’t ﬁnd the
Line55 Swing component it refers to, it will time out with an error. For this test, we’re
Line56 looking for a label component that shows a given string; if our application doesn’t
Line57 produce this label, we’ll get an exception. Here’s the implementation (with the
Line58 constants left out for clarity) and some explanation:
Line59 public class ApplicationRunner {
Line60   public static final String SNIPER_ID = "sniper";
Line61   public static final String SNIPER_PASSWORD = "sniper";
Line62   private AuctionSniperDriver driver;
Line63   public void startBiddingIn(final FakeAuctionServer auction) {
Line64     Thread thread = new Thread("Test Application") {
Line65       @Override public void run() { 1
Line66         try {
Line67           Main.main(XMPP_HOSTNAME, SNIPER_ID, SNIPER_PASSWORD, auction.getItemId()); 2
Line68         } catch (Exception e) {                                                    
Line69           e.printStackTrace(); 3
Line70         }
Line71       }
Line72     };
Line73     thread.setDaemon(true);
Line74     thread.start();
Line75     driver = new AuctionSniperDriver(1000); 4
Line76     driver.showsSniperStatus(STATUS_JOINING); 5
Line77   }
Line78   public void showsSniperHasLostAuction() {
Line79     driver.showsSniperStatus(STATUS_LOST);  6
Line80   }
Line81   public void stop() {
Line82     if (driver != null) {
Line83       driver.dispose(); 7
Line84     }
Line85   }
Line86 }
Line87 1. We’re assuming that you know how Swing works; there are many other books that
Line88 do a good job of describing it. The essential point here is that it’s an event-driven
Line89 framework that creates its own internal threads to dispatch events, so we can’t be
Line90 precise about when things will happen.
Line91 Chapter 11
Line92 Passing the First Test
Line93 90
Line94 
Line95 
Line96 ---
Line97 
Line98 ---
Line99 **Page 91**
Line100 
Line101 1
Line102 We call the application through its main() function to make sure we’ve as-
Line103 sembled the pieces correctly. We’re following the convention that the entry
Line104 point to the application is a Main class in the top-level package. WindowLicker
Line105 can control Swing components if they’re in the same JVM, so we start the
Line106 Sniper in a new thread. Ideally, the test would start the Sniper in a new pro-
Line107 cess, but that would be much harder to test; we think this is a reasonable
Line108 compromise.
Line109 2
Line110 To keep things simple at this stage, we’ll assume that we’re only bidding for
Line111 one item and pass the identiﬁer to main().
Line112 3
Line113 If main() throws an exception, we just print it out. Whatever test we’re
Line114 running will fail and we can look for the stack trace in the output. Later,
Line115 we’ll handle exceptions properly.
Line116 4
Line117 We turn down the timeout period for ﬁnding frames and components. The
Line118 default values are longer than we need for a simple application like this one
Line119 and will slow down the tests when they fail. We use one second, which is
Line120 enough to smooth over minor runtime delays.
Line121 5
Line122 We wait for the status to change to Joining so we know that the application
Line123 has attempted to connect. This assertion says that somewhere in the user
Line124 interface there’s a label that describes the Sniper’s state.
Line125 6
Line126 When the Sniper loses the auction, we expect it to show a Lost status. If this
Line127 doesn’t happen, the driver will throw an exception.
Line128 7
Line129 After the test, we tell the driver to dispose of the window to make sure it
Line130 won’t be picked up in another test before being garbage-collected.
Line131 The AuctionSniperDriver is simply an extension of a WindowLicker
Line132 JFrameDriver specialized for our tests:
Line133 public class AuctionSniperDriver extends JFrameDriver {
Line134   public AuctionSniperDriver(int timeoutMillis) {
Line135     super(new GesturePerformer(), 
Line136           JFrameDriver.topLevelFrame(
Line137             named(Main.MAIN_WINDOW_NAME), 
Line138             showingOnScreen()),
Line139             new AWTEventQueueProber(timeoutMillis, 100));
Line140   }
Line141   public void showsSniperStatus(String statusText) {
Line142     new JLabelDriver(
Line143       this, named(Main.SNIPER_STATUS_NAME)).hasText(equalTo(statusText));
Line144   }
Line145 }
Line146 91
Line147 Building the Test Rig
Line148 
Line149 
Line150 ---
Line151 
Line152 ---
Line153 **Page 92**
Line154 
Line155 On construction, it attempts to ﬁnd a visible top-level window for the Auction
Line156 Sniper within the given timeout. The method showsSniperStatus() looks for the
Line157 relevant label in the user interface and conﬁrms that it shows the given status.
Line158 If the driver cannot ﬁnd a feature it expects, it will throw an exception and fail
Line159 the test.
Line160 The Fake Auction
Line161 A FakeAuctionServer is a substitute server that allows the test to check how the
Line162 Auction Sniper interacts with an auction using XMPP messages. It has three re-
Line163 sponsibilities: it must connect to the XMPP broker and accept a request to join
Line164 the chat from the Sniper; it must receive chat messages from the Sniper or fail if
Line165 no message arrives within some timeout; and, it must allow the test to send
Line166 messages back to the Sniper as speciﬁed by Southabee’s On-Line.
Line167 Smack (the XMPP client library) is event-driven, so the fake auction has to
Line168 register listener objects for it to call back. There are two levels of events: events
Line169 about a chat, such as people joining, and events within a chat, such as messages
Line170 being received. We need to listen for both.
Line171 We’ll start by implementing the startSellingItem() method. First, it connects
Line172 to the XMPP broker, using the item identiﬁer to construct the login name; then
Line173 it registers a ChatManagerListener. Smack will call this listener with a Chat object
Line174 that represents the session when a Sniper connects in. The fake auction holds on
Line175 to the chat so it can exchange messages with the Sniper.
Line176 Figure 11.1
Line177 Smack objects and callbacks
Line178 Chapter 11
Line179 Passing the First Test
Line180 92
Line181 
Line182 
Line183 ---
Line184 
Line185 ---
Line186 **Page 93**
Line187 
Line188 So far, we have:
Line189 public class FakeAuctionServer {
Line190   public static final String ITEM_ID_AS_LOGIN = "auction-%s"; 
Line191   public static final String AUCTION_RESOURCE = "Auction";
Line192   public static final String XMPP_HOSTNAME = "localhost";
Line193   private static final String AUCTION_PASSWORD = "auction";
Line194   private final String itemId;
Line195   private final XMPPConnection connection;
Line196   private Chat currentChat;
Line197   public FakeAuctionServer(String itemId) {
Line198     this.itemId = itemId;
Line199     this.connection = new XMPPConnection(XMPP_HOSTNAME);
Line200   }
Line201   public void startSellingItem() throws XMPPException {
Line202     connection.connect(); 
Line203     connection.login(format(ITEM_ID_AS_LOGIN, itemId), 
Line204                      AUCTION_PASSWORD, AUCTION_RESOURCE);
Line205     connection.getChatManager().addChatListener(
Line206       new ChatManagerListener() {
Line207         public void chatCreated(Chat chat, boolean createdLocally) {
Line208           currentChat = chat;
Line209         }
Line210       });
Line211   }
Line212   public String getItemId() {
Line213     return itemId;
Line214   }
Line215 }
Line216 A Minimal Fake Implementation
Line217 We want to emphasize again that this fake is a minimal implementation just to
Line218 support testing. For example, we use a single instance variable to hold the chat
Line219 object. A real auction server would manage multiple chats for all the bidders—but
Line220 this is a fake; its only purpose is to support the test, so it only needs one chat.
Line221 Next, we have to add a MessageListener to the chat to accept messages from
Line222 the Sniper. This means that we need to coordinate between the thread that
Line223 runs the test and the Smack thread that feeds messages to the listener—the test
Line224 has to wait for messages to arrive and time out if they don’t—so we’ll use a
Line225 single-element BlockingQueue from the java.util.concurrent package. Just as
Line226 we only have one chat in the test, we expect to process only one message at a
Line227 time. To make our intentions clearer, we wrap the queue in a helper class
Line228 SingleMessageListener. Here’s the rest of FakeAuctionServer:
Line229 93
Line230 Building the Test Rig
Line231 
Line232 
Line233 ---
Line234 
Line235 ---
Line236 **Page 94**
Line237 
Line238 public class FakeAuctionServer {
Line239 private final SingleMessageListener messageListener = new SingleMessageListener();
Line240   public void startSellingItem() throws XMPPException {
Line241     connection.connect(); 
Line242     connection.login(format(ITEM_ID_AS_LOGIN, itemId), 
Line243                      AUCTION_PASSWORD, AUCTION_RESOURCE);
Line244     connection.getChatManager().addChatListener(
Line245       new ChatManagerListener() {
Line246         public void chatCreated(Chat chat, boolean createdLocally) {
Line247           currentChat = chat;
Line248 chat.addMessageListener(messageListener);
Line249         }
Line250       });
Line251   }
Line252   public void hasReceivedJoinRequestFromSniper() throws InterruptedException {
Line253     messageListener.receivesAMessage(); 1
Line254   }
Line255   public void announceClosed() throws XMPPException {
Line256     currentChat.sendMessage(new Message()); 2
Line257   }
Line258   public void stop() {
Line259     connection.disconnect(); 3
Line260   }
Line261 }
Line262 public class SingleMessageListener implements MessageListener {
Line263   private final ArrayBlockingQueue<Message> messages = 
Line264                               new ArrayBlockingQueue<Message>(1);
Line265   public void processMessage(Chat chat, Message message) {
Line266     messages.add(message);
Line267   }
Line268   public void receivesAMessage() throws InterruptedException {
Line269     assertThat("Message", messages.poll(5, SECONDS), is(notNullValue())); 4
Line270   }
Line271 }
Line272 1
Line273 The test needs to know when a Join message has arrived. We just check
Line274 whether any message has arrived, since the Sniper will only be sending Join
Line275 messages to start with; we’ll ﬁll in more detail as we grow the application.
Line276 This implementation will fail if no message is received within 5 seconds.
Line277 2
Line278 The test needs to be able to simulate the auction announcing when it closes,
Line279 which is why we held onto the currentChat when it opened. As with the
Line280 Join request, the fake auction just sends an empty message, since this is
Line281 the only event we support so far.
Line282 3
Line283 stop() closes the connection.
Line284 Chapter 11
Line285 Passing the First Test
Line286 94
Line287 
Line288 
Line289 ---
Line290 
Line291 ---
Line292 **Page 95**
Line293 
Line294 4
Line295 The clause is(notNullValue()) uses the Hamcrest matcher syntax. We de-
Line296 scribe Matchers in “Methods” (page 339); for now, it’s enough to know that
Line297 this checks that the Listener has received a message within the timeout period.
Line298 The Message Broker
Line299 There’s one more component to mention which doesn’t involve any coding—the
Line300 installation of an XMPP message broker. We set up an instance of Openﬁre on
Line301 our local host. The Sniper and fake auction in our end-to-end tests, even though
Line302 they’re running in the same process, will communicate through this server. We
Line303 also set up logins to match the small number of item identiﬁers that we’ll be using
Line304 in our tests.
Line305 A Working Compromise
Line306 As we wrote before, we are cheating a little at this stage to keep development
Line307 moving. We want all the developers to have their own environments so they don’t
Line308 interfere with each other when running their tests. For example, we’ve seen teams
Line309 make their lives very complicated because they didn’t want to create a database
Line310 instance for each developer. In a professional organization, we would also expect
Line311 to see at least one test rig that represents the production environment, including
Line312 the distribution of processing across a network and a build cycle that uses it to
Line313 make sure the system works.
Line314 Failing and Passing the Test
Line315 We have enough infrastructure in place to run the test and watch it fail. For the
Line316 rest of this chapter we’ll add functionality, a tiny slice at a time, until eventually
Line317 we make the test pass. When we ﬁrst started using this technique, it felt too fussy:
Line318 “Just write the code, we know what to do!” Over time, we realized that it didn’t
Line319 take any longer and that our progress was much more predictable. Focusing on
Line320 just one aspect at a time helps us to make sure we understand it; as a rule, when
Line321 we get something working, it stays working. Where there’s no need to discuss
Line322 the solution, many of these steps take hardly any time at all—they take longer
Line323 to explain than to implement.
Line324 We start by writing a build script for ant. We’ll skip over the details of its
Line325 content, since it’s standard practice these days, but the important point is that
Line326 we always have a single command that reliably compiles, builds, deploys, and
Line327 tests the application, and that we run it repeatedly. We only start coding once
Line328 we have an automated build and test working.
Line329 At this stage, we’ll describe each step, discussing each test failure in turn. Later
Line330 we’ll speed up the pace.
Line331 95
Line332 Failing and Passing the Test
Line333 
Line334 
Line335 ---
