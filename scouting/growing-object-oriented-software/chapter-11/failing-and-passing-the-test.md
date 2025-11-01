Line1 # Failing and Passing the Test (pp.95-102)
Line2 
Line3 ---
Line4 **Page 95**
Line5 
Line6 4
Line7 The clause is(notNullValue()) uses the Hamcrest matcher syntax. We de-
Line8 scribe Matchers in “Methods” (page 339); for now, it’s enough to know that
Line9 this checks that the Listener has received a message within the timeout period.
Line10 The Message Broker
Line11 There’s one more component to mention which doesn’t involve any coding—the
Line12 installation of an XMPP message broker. We set up an instance of Openﬁre on
Line13 our local host. The Sniper and fake auction in our end-to-end tests, even though
Line14 they’re running in the same process, will communicate through this server. We
Line15 also set up logins to match the small number of item identiﬁers that we’ll be using
Line16 in our tests.
Line17 A Working Compromise
Line18 As we wrote before, we are cheating a little at this stage to keep development
Line19 moving. We want all the developers to have their own environments so they don’t
Line20 interfere with each other when running their tests. For example, we’ve seen teams
Line21 make their lives very complicated because they didn’t want to create a database
Line22 instance for each developer. In a professional organization, we would also expect
Line23 to see at least one test rig that represents the production environment, including
Line24 the distribution of processing across a network and a build cycle that uses it to
Line25 make sure the system works.
Line26 Failing and Passing the Test
Line27 We have enough infrastructure in place to run the test and watch it fail. For the
Line28 rest of this chapter we’ll add functionality, a tiny slice at a time, until eventually
Line29 we make the test pass. When we ﬁrst started using this technique, it felt too fussy:
Line30 “Just write the code, we know what to do!” Over time, we realized that it didn’t
Line31 take any longer and that our progress was much more predictable. Focusing on
Line32 just one aspect at a time helps us to make sure we understand it; as a rule, when
Line33 we get something working, it stays working. Where there’s no need to discuss
Line34 the solution, many of these steps take hardly any time at all—they take longer
Line35 to explain than to implement.
Line36 We start by writing a build script for ant. We’ll skip over the details of its
Line37 content, since it’s standard practice these days, but the important point is that
Line38 we always have a single command that reliably compiles, builds, deploys, and
Line39 tests the application, and that we run it repeatedly. We only start coding once
Line40 we have an automated build and test working.
Line41 At this stage, we’ll describe each step, discussing each test failure in turn. Later
Line42 we’ll speed up the pace.
Line43 95
Line44 Failing and Passing the Test
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 96**
Line51 
Line52 First User Interface
Line53 Test Failure
Line54 The test can’t ﬁnd a user interface component with the name "Auction Sniper
Line55 Main".
Line56 java.lang.AssertionError: 
Line57 Tried to look for...
Line58     exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line59     in all top level windows
Line60 but...
Line61     all top level windows
Line62 contained 0 JFrame (with name "Auction Sniper Main" and showing on screen)
Line63 […]
Line64   at auctionsniper.ApplicationRunner.stop()
Line65   at auctionsniper.AuctionSniperEndToEndTest.stopApplication()
Line66 […]
Line67 WindowLicker is verbose in its error reporting, trying to make failures easy
Line68 to understand. In this case, we couldn’t even ﬁnd the top-level frame so JUnit
Line69 failed before even starting the test. The stack trace comes from the @After method
Line70 that stops the application.
Line71 Implementation
Line72 We need a top-level window for our application. We write a MainWindow class in
Line73 the auctionsniper.ui package that extends Swing’s JFrame, and call it from
Line74 main(). All it will do is create a window with the right name.
Line75 public class Main {
Line76   private MainWindow ui;
Line77   public Main() throws Exception {
Line78 startUserInterface()
Line79   }
Line80   public static void main(String... args) throws Exception {
Line81     Main main = new Main();
Line82   }
Line83   private void startUserInterface() throws Exception {
Line84     SwingUtilities.invokeAndWait(new Runnable() {
Line85       public void run() {
Line86         ui = new MainWindow();
Line87       }
Line88     });
Line89   }
Line90 }
Line91 Chapter 11
Line92 Passing the First Test
Line93 96
Line94 
Line95 
Line96 ---
Line97 
Line98 ---
Line99 **Page 97**
Line100 
Line101 public class MainWindow extends JFrame {
Line102   public MainWindow() {
Line103     super("Auction Sniper");
Line104     setName(MAIN_WINDOW_NAME);
Line105     setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
Line106     setVisible(true);
Line107   }
Line108 }
Line109 Unfortunately, this is a little messy because Swing requires us to create the
Line110 user interface on its event dispatch thread. We’ve further complicated the imple-
Line111 mentation so we can hang on to the main window object in our code. It’s not
Line112 strictly necessary here but we thought we’d get it over with.
Line113 Notes
Line114 The user interface in Figure 11.2 really is minimal. It does not look like much
Line115 but it conﬁrms that we can start up an application window and connect to it.
Line116 Our test still fails, but we’ve moved on a step. Now we know that our harness
Line117 is working, which is one less thing to worry about as we move on to more
Line118 interesting functionality.
Line119 Figure 11.2
Line120 Just a top-level window
Line121 Showing the Sniper State
Line122 Test Failure
Line123 The test ﬁnds a top-level window, but no display of the current state of the Sniper.
Line124 To start with, the Sniper should show Joining while waiting for the auction to
Line125 respond.
Line126 java.lang.AssertionError: 
Line127 Tried to look for...
Line128     exactly 1 JLabel (with name "sniper status")
Line129     in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line130     in all top level windows
Line131 and check that its label text is "Joining"
Line132 but...
Line133     all top level windows
Line134     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line135 contained 0 JLabel (with name "sniper status")
Line136   at com.objogate.wl.AWTEventQueueProber.check()
Line137 […]
Line138   at AuctionSniperDriver.showsSniperStatus()
Line139   at ApplicationRunner.startBiddingIn()
Line140   at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
Line141 […]
Line142 97
Line143 Failing and Passing the Test
Line144 
Line145 
Line146 ---
Line147 
Line148 ---
Line149 **Page 98**
Line150 
Line151 Implementation
Line152 We add a label representing the Sniper’s state to MainWindow.
Line153 public class MainWindow extends JFrame {
Line154   public static final String SNIPER_STATUS_NAME = "sniper status";
Line155   private final JLabel sniperStatus = createLabel(STATUS_JOINING);
Line156   public MainWindow() {
Line157     super("Auction Sniper");
Line158     setName(MAIN_WINDOW_NAME);
Line159 add(sniperStatus);
Line160     pack();
Line161     setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
Line162     setVisible(true);
Line163   }
Line164   private static JLabel createLabel(String initialText) {
Line165     JLabel result = new JLabel(initialText);
Line166     result.setName(SNIPER_STATUS_NAME);
Line167     result.setBorder(new LineBorder(Color.BLACK));
Line168     return result;
Line169   }
Line170 }
Line171 Notes
Line172 Another minimal change, but now we can show some content in our application,
Line173 as in Figure 11.3.
Line174 Figure 11.3
Line175 Showing Joining status
Line176 Connecting to the Auction
Line177 Test Failure
Line178 Our user interface is working, but the auction does not receive a Join request
Line179 from the Sniper.
Line180 java.lang.AssertionError: 
Line181 Expected: is not null
Line182 got: null
Line183   at org.junit.Assert.assertThat()
Line184   at SingleMessageListener.receivesAMessage()
Line185   at FakeAuctionServer.hasReceivedJoinRequestFromSniper()
Line186   at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
Line187 […]
Line188 Chapter 11
Line189 Passing the First Test
Line190 98
Line191 
Line192 
Line193 ---
Line194 
Line195 ---
Line196 **Page 99**
Line197 
Line198 This failure message is a bit cryptic, but the names in the stack trace tell us
Line199 what’s wrong.
Line200 Implementation
Line201 We write a simplistic implementation to get us past this failure. It connects to
Line202 the chat in Main and sends an empty message. We create a null MessageListener
Line203 to allow us to create a Chat for sending the empty initial message, since we don’t
Line204 yet care about receiving messages.
Line205 public class Main {
Line206   private static final int ARG_HOSTNAME = 0;
Line207   private static final int ARG_USERNAME = 1;
Line208   private static final int ARG_PASSWORD = 2;
Line209   private static final int ARG_ITEM_ID  = 3;
Line210   public static final String AUCTION_RESOURCE = "Auction";
Line211   public static final String ITEM_ID_AS_LOGIN = "auction-%s";
Line212   public static final String AUCTION_ID_FORMAT = 
Line213                                ITEM_ID_AS_LOGIN + "@%s/" + AUCTION_RESOURCE;
Line214 […]
Line215   public static void main(String... args) throws Exception {
Line216     Main main = new Main();
Line217     XMPPConnection connection = connectTo(args[ARG_HOSTNAME], 
Line218                                           args[ARG_USERNAME], 
Line219                                           args[ARG_PASSWORD]);
Line220     Chat chat = connection.getChatManager().createChat(
Line221         auctionId(args[ARG_ITEM_ID], connection), 
Line222         new MessageListener() {
Line223           public void processMessage(Chat aChat, Message message) {
Line224 // nothing yet
Line225           }
Line226         });
Line227     chat.sendMessage(new Message());
Line228   }
Line229   private static XMPPConnection 
Line230 connectTo(String hostname, String username, String password) 
Line231       throws XMPPException
Line232   {
Line233     XMPPConnection connection = new XMPPConnection(hostname);
Line234     connection.connect();
Line235     connection.login(username, password, AUCTION_RESOURCE);
Line236     return connection;
Line237   }
Line238   private static String auctionId(String itemId, XMPPConnection connection) {
Line239     return String.format(AUCTION_ID_FORMAT, itemId, 
Line240                          connection.getServiceName()); 
Line241   }
Line242 […]
Line243 }
Line244 99
Line245 Failing and Passing the Test
Line246 
Line247 
Line248 ---
Line249 
Line250 ---
Line251 **Page 100**
Line252 
Line253 Notes
Line254 This shows that we can establish a connection from the Sniper to the auction,
Line255 which means we had to sort out details such as interpreting the item and user
Line256 credentials from the command-line arguments and using the Smack library. We’re
Line257 leaving the message contents until later because we only have one message type,
Line258 so sending an empty value is enough to prove the connection.
Line259 This implementation may seem gratuitously naive—after all, we should be able
Line260 to design a structure for something as simple as this, but we’ve often found it
Line261 worth writing a small amount of ugly code and seeing how it falls out. It helps
Line262 us to test our ideas before we’ve gone too far, and sometimes the results can be
Line263 surprising. The important point is to make sure we don’t leave it ugly.
Line264 We make a point of keeping the connection code out of the Swing
Line265 invokeAndWait() call that creates the MainWindow, because we want the user
Line266 interface to settle before we try anything more complicated.
Line267 Receiving a Response from the Auction
Line268 Test Failure
Line269 With a connection established, the Sniper should receive and display the Lost
Line270 response from the auction. It doesn’t yet:
Line271 java.lang.AssertionError: 
Line272 Tried to look for...
Line273     exactly 1 JLabel (with name "sniper status")
Line274     in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line275     in all top level windows
Line276 and check that its label text is "Lost"
Line277 but...
Line278     all top level windows
Line279     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line280     contained 1 JLabel (with name "sniper status")
Line281 label text was "Joining"
Line282 […]
Line283   at AuctionSniperDriver.showsSniperStatus()
Line284   at ApplicationRunner.showsSniperHasLostAuction()
Line285   at AuctionSniperEndToEndTest.sniperJoinsAuctionUntilAuctionCloses()
Line286 […]
Line287 Implementation
Line288 We need to attach the user interface to the chat so it can receive the response
Line289 from the auction, so we create a connection and pass it to Main to create the Chat
Line290 object. joinAuction() creates a MessageListener that sets the status label, using
Line291 an invokeLater() call to avoid blocking the Smack library. As with the Join
Line292 message, we don’t bother with the contents of the incoming message since there’s
Line293 only one possible response the auction can send at the moment. While we’re at
Line294 it, we rename connect() to connection() to make the code read better.
Line295 Chapter 11
Line296 Passing the First Test
Line297 100
Line298 
Line299 
Line300 ---
Line301 
Line302 ---
Line303 **Page 101**
Line304 
Line305 public class Main {
Line306   @SuppressWarnings("unused") private Chat notToBeGCd;
Line307 […]
Line308   public static void main(String... args) throws Exception {
Line309     Main main = new Main();
Line310 main.joinAuction(
Line311       connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]), 
Line312       args[ARG_ITEM_ID]);
Line313   }
Line314   private void joinAuction(XMPPConnection connection, String itemId) 
Line315     throws XMPPException
Line316   {
Line317     final Chat chat = connection.getChatManager().createChat(
Line318         auctionId(itemId, connection), 
Line319         new MessageListener() {
Line320           public void processMessage(Chat aChat, Message message) {
Line321 SwingUtilities.invokeLater(new Runnable() {
Line322               public void run() {
Line323                 ui.showStatus(MainWindow.STATUS_LOST);
Line324               }
Line325             });
Line326           }
Line327         });
Line328     this.notToBeGCd = chat;
Line329     chat.sendMessage(new Message());
Line330   }
Line331 Why the Chat Field?
Line332 You’ll notice that we’ve assigned the chat that we create to the ﬁeld notToBeGCd
Line333 in Main. This is to make sure that the chat is not garbage-collected by the Java
Line334 runtime. There’s a note at the top of the ChatManager documentation that says:
Line335 The chat manager keeps track of references to all current chats. It will not
Line336 hold any references in memory on its own so it is necessary to keep a
Line337 reference to the chat object itself.
Line338 If the chat is garbage-collected, the Smack runtime will hand the message to a
Line339 new Chat which it will create for the purpose. In an interactive application, we would
Line340 listen for and show these new chats, but our needs are different, so we add this
Line341 quirk to stop it from happening.
Line342 We made this reference clumsy on purpose—to highlight in the code why we’re
Line343 doing it.We also know that we’re likely to come up with a better solution in a while.
Line344 We implement the display method in the user interface and, ﬁnally, the whole
Line345 test passes.
Line346 101
Line347 Failing and Passing the Test
Line348 
Line349 
Line350 ---
Line351 
Line352 ---
Line353 **Page 102**
Line354 
Line355 public class MainWindow extends JFrame {
Line356 […]
Line357   public void showStatus(String status) {
Line358 sniperStatus.setText(status);
Line359   }
Line360 }
Line361 Notes
Line362 Figure 11.4 is visible conﬁrmation that the code works.
Line363 Figure 11.4
Line364 Showing Lost status
Line365 It may not look like much, but it conﬁrms that a Sniper can establish a
Line366 connection with an auction, accept a response, and display the result.
Line367 The Necessary Minimum
Line368 In one of his school reports, Steve was noted as “a ﬁne judge of the necessary
Line369 minimum.” It seems he’s found his calling in writing software since this is a
Line370 critical skill during iteration zero.
Line371 What we hope you’ve seen in this chapter is the degree of focus that’s required
Line372 to put together your ﬁrst walking skeleton. The point is to design and validate
Line373 the initial structure of the end-to-end system—where end-to-end includes deploy-
Line374 ment to a working environment—to prove that our choices of packages, libraries,
Line375 and tooling will actually work. A sense of urgency will help the team to strip the
Line376 functionality down to the absolute minimum sufﬁcient to test their assumptions.
Line377 That’s why we didn’t put any content in our Sniper messages; it would be a di-
Line378 version from making sure that the communication and event handling work. We
Line379 didn’t sweat too hard over the detailed code design, partly because there isn’t
Line380 much but mainly because we’re just getting the pieces in place; that effort will
Line381 come soon enough.
Line382 Of course, all you see in this chapter are edited highlights. We’ve left out many
Line383 diversions and discussions as we ﬁgured out which pieces to use and how to make
Line384 them work, trawling through product documentation and discussion lists. We’ve
Line385 also left out some of our discussions about what this project is for. Iteration zero
Line386 usually brings up project chartering issues as the team looks for criteria to guide
Line387 its decisions, so the project’s sponsors should expect to ﬁeld some deep questions
Line388 about its purpose.
Line389 Chapter 11
Line390 Passing the First Test
Line391 102
Line392 
Line393 
Line394 ---
