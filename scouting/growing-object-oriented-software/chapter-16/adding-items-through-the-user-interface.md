Line1 # Adding Items through the User Interface (pp.183-189)
Line2 
Line3 ---
Line4 **Page 183**
Line5 
Line6 Adding Items through the User Interface
Line7 A Simpler Design
Line8 The buyers and user interface designers are still working through their ideas, but
Line9 they have managed to simplify their original design by moving the item entry
Line10 into a top bar instead of a pop-up dialog. The current version of the design looks
Line11 like Figure 16.2, so we need to add a text ﬁeld and a button to the display.
Line12 Figure 16.2
Line13 The Sniper with input ﬁelds in its bar
Line14 Making Progress While We Can
Line15 The design of user interfaces is outside the scope of this book. For a project of any
Line16 size, a user experience professional will consider all sorts of macro- and micro-
Line17 details to provide the user with a coherent experience, so one route that some
Line18 teams take is to try to lock down the interface design before coding. Our experience,
Line19 and that of others like Jeff Patton, is that we can make development progress whilst
Line20 the design is being sorted out. We can build to the team’s current understanding
Line21 of the features and keep our code (and attitude) ﬂexible to respond to design ideas
Line22 as they ﬁrm up—and perhaps even feed our experience back into the process.
Line23 Update the Test
Line24 Looking back at AuctionSniperEndToEndTest, it already expresses everything we
Line25 want the application to do: it describes how the Sniper connects to one or more
Line26 auctions and bids. The change is that we want to describe a different implemen-
Line27 tation of some of that behavior (establishing the connection through the user
Line28 interface rather than the command line) which happens in the ApplicationRunner.
Line29 We need a restructuring similar to the one we just made in Main, splitting the
Line30 connection from the individual auctions. We pull out a startSniper() method
Line31 that starts up and checks the Sniper, and then start bidding for each auction
Line32 in turn.
Line33 183
Line34 Adding Items through the User Interface
Line35 
Line36 
Line37 ---
Line38 
Line39 ---
Line40 **Page 184**
Line41 
Line42 public class ApplicationRunner {
Line43   public void startBiddingIn(final FakeAuctionServer... auctions) {
Line44     startSniper();
Line45     for (FakeAuctionServer auction : auctions) {
Line46 final String itemId = auction.getItemId();
Line47       driver.startBiddingFor(itemId);
Line48       driver.showsSniperStatus(itemId, 0, 0, textFor(SniperState.JOINING));
Line49     }
Line50   }
Line51   private void startSniper() {
Line52 // as before without the call to showsSniperStatus()
Line53   }
Line54 […]
Line55 }
Line56 The other change to the test infrastructure is implementing the new method
Line57 startBiddingFor() in AuctionSniperDriver. This ﬁnds and ﬁlls in the text ﬁeld
Line58 for the item identiﬁer, then ﬁnds and clicks on the Join Auction button.
Line59 public class AuctionSniperDriver extends JFrameDriver {
Line60   @SuppressWarnings("unchecked")
Line61   public void startBiddingFor(String itemId) {
Line62     itemIdField().replaceAllText(itemId); 
Line63     bidButton().click(); 
Line64   }
Line65   private JTextFieldDriver itemIdField() {
Line66     JTextFieldDriver newItemId = 
Line67       new JTextFieldDriver(this, JTextField.class, named(MainWindow.NEW_ITEM_ID_NAME));
Line68     newItemId.focusWithMouse();
Line69     return newItemId;
Line70   }
Line71   private JButtonDriver bidButton() {
Line72     return new JButtonDriver(this, JButton.class, named(MainWindow.JOIN_BUTTON_NAME));
Line73   }
Line74 […]
Line75 }
Line76 Neither of these components exist yet, so the test fails looking for the text ﬁeld.
Line77 […] but...
Line78     all top level windows
Line79     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line80 contained 0 JTextField (with name "item id")
Line81 Adding an Action Bar
Line82 We address this failure by adding a new panel across the top to contain the
Line83 text ﬁeld for the identiﬁer and the Join Auction button, wrapping up the activity
Line84 in a makeControls() method to help express our intent. We realize that this code
Line85 isn’t very exciting, but we want to show its structure now before we add any
Line86 behavior.
Line87 Chapter 16
Line88 Sniping for Multiple Items
Line89 184
Line90 
Line91 
Line92 ---
Line93 
Line94 ---
Line95 **Page 185**
Line96 
Line97 public class MainWindow extends JFrame {
Line98   public MainWindow(TableModel snipers) {
Line99     super(APPLICATION_TITLE);
Line100     setName(MainWindow.MAIN_WINDOW_NAME);
Line101     fillContentPane(makeSnipersTable(snipers), makeControls());
Line102 […]
Line103   }
Line104   private JPanel makeControls() {
Line105     JPanel controls = new JPanel(new FlowLayout());
Line106     final JTextField itemIdField = new JTextField();
Line107     itemIdField.setColumns(25);
Line108     itemIdField.setName(NEW_ITEM_ID_NAME);
Line109     controls.add(itemIdField);
Line110     JButton joinAuctionButton = new JButton("Join Auction");
Line111     joinAuctionButton.setName(JOIN_BUTTON_NAME);
Line112     controls.add(joinAuctionButton);
Line113     return controls;
Line114   }
Line115 […]
Line116 }
Line117 With the action bar in place, our next test fails because we don’t create the
Line118 identiﬁed rows in the table model.
Line119 […] but...
Line120    all top level windows
Line121    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line122    contained 1 JTable ()
Line123 it is not with row with cells
Line124    <label with text "item-54321">, <label with text "0">, 
Line125    <label with text "0">, <label with text "Joining">
Line126 A Design Moment
Line127 Now what do we do? To review our position: we have a broken acceptance
Line128 test pending, we have the user interface structure but no behavior, and the
Line129 SnipersTableModel still handles only one Sniper at a time. Our goal is that, when
Line130 we click on the Join Auction button, the application will attempt to join the
Line131 auction speciﬁed in the item ﬁeld and add a new row to the list of auctions to
Line132 show that the request is being handled.
Line133 In practice, this means that we need a Swing ActionListener for the JButton
Line134 that will use the text from the JTextField as an item identiﬁer for the new session.
Line135 Its implementation will add a row to the SnipersTableModel and create a new
Line136 Chat to the Southabee’s On-Line server. The catch is that everything to do with
Line137 connections is in Main, whereas the button and the text ﬁeld are in MainWindow.
Line138 This is a distinction we’d like to maintain, since it keeps the responsibilities of
Line139 the two classes focused.
Line140 185
Line141 Adding Items through the User Interface
Line142 
Line143 
Line144 ---
Line145 
Line146 ---
Line147 **Page 186**
Line148 
Line149 We stop for a moment to think about the structure of the code, using the CRC
Line150 cards we mentioned in “Roles, Responsibilities, Collaborators” on page 16 to
Line151 help us visualize our ideas. After some discussion, we remind ourselves that the
Line152 job of MainWindow is to manage our UI components and their interactions; it
Line153 shouldn’t also have to manage concepts such as “connection” or “chat.” When
Line154 a user interaction implies an action outside the user interface, MainWindow should
Line155 delegate to a collaborating object.
Line156 To express this, we decide to add a listener to MainWindow to notify neighboring
Line157 objects about such requests. We call the new collaborator a UserRequestListener
Line158 since it will be responsible for handling requests made by the user:
Line159 public interface UserRequestListener extends EventListener {
Line160   void joinAuction(String itemId);
Line161 }
Line162 Another Level of Testing
Line163 We want to write a test for our proposed new behavior, but we can’t just write
Line164 a simple unit test because of Swing threading. We can’t be sure that the Swing
Line165 code will have ﬁnished running by the time we check any assertions at the end
Line166 of the test, so we need something that will wait until the tested code has
Line167 stabilized—what we usually call an integration test because it’s testing how our
Line168 code works with a third-party library. We can use WindowLicker for this level
Line169 of testing as well as for our end-to-end tests. Here’s the new test:
Line170 public class MainWindowTest {
Line171   private final SnipersTableModel tableModel = new SnipersTableModel();
Line172   private final MainWindow mainWindow = new MainWindow(tableModel);
Line173   private final AuctionSniperDriver driver = new AuctionSniperDriver(100);
Line174   @Test public void
Line175 makesUserRequestWhenJoinButtonClicked() {
Line176     final ValueMatcherProbe<String> buttonProbe = 
Line177       new ValueMatcherProbe<String>(equalTo("an item-id"), "join request");
Line178     mainWindow.addUserRequestListener(
Line179         new UserRequestListener() {
Line180           public void joinAuction(String itemId) {
Line181             buttonProbe.setReceivedValue(itemId);
Line182           }
Line183         });
Line184     driver.startBiddingFor("an item-id");
Line185     driver.check(buttonProbe);
Line186   }
Line187 }
Line188 Chapter 16
Line189 Sniping for Multiple Items
Line190 186
Line191 
Line192 
Line193 ---
Line194 
Line195 ---
Line196 **Page 187**
Line197 
Line198 WindowLicker Probes
Line199 In WindowLicker, a probe is an object that checks for a given state. A driver’s
Line200 check() method repeatedly ﬁres the given probe until it’s satisﬁed or times out. In
Line201 this test, we use a ValueMatcherProbe, which compares a value against a Ham-
Line202 crest matcher, to wait for the UserRequestListener’s joinAuction() to be called
Line203 with the right auction identiﬁer.
Line204 We create an empty implementation of MainWindow.addUserRequestListener,
Line205 to get through the compiler, and the test fails:
Line206 Tried to look for...
Line207     join request "an item-id"
Line208 but...
Line209     join request "an item-id". Received nothing
Line210 To make this test pass, we ﬁll in the request listener infrastructure in MainWindow
Line211 using Announcer, a utility class that manages collections of listeners.2 We add a
Line212 Swing ActionListener that extracts the item identiﬁer and announces it to the
Line213 request listeners. The relevant parts of MainWindow look like this:
Line214 public class MainWindow extends JFrame {
Line215   private final Announcer<UserRequestListener> userRequests = 
Line216                                      Announcer.to(UserRequestListener.class); 
Line217   public void addUserRequestListener(UserRequestListener userRequestListener) {
Line218     userRequests.addListener(userRequestListener); 
Line219   } 
Line220 […]
Line221   private JPanel makeControls(final SnipersTableModel snipers) {
Line222 […]
Line223     joinAuctionButton.addActionListener(new ActionListener() {
Line224       public void actionPerformed(ActionEvent e) {
Line225 userRequests.announce().joinAuction(itemIdField.getText());
Line226       }
Line227     });
Line228 […]
Line229   }
Line230 }
Line231 To emphasize the point here, we’ve converted an ActionListener event, which
Line232 is internal to the user interface framework, to a UserRequestListener event,
Line233 which is about users interacting with an auction. These are two separate domains
Line234 and MainWindow’s job is to translate from one to the other. MainWindow is
Line235 not concerned with how any implementation of UserRequestListener might
Line236 work—that would be too much responsibility.
Line237 2.
Line238 Announcer is included in the examples that ship with jMock.
Line239 187
Line240 Adding Items through the User Interface
Line241 
Line242 
Line243 ---
Line244 
Line245 ---
Line246 **Page 188**
Line247 
Line248 Micro-Hubris
Line249 In case this level of testing seems like overkill, when we ﬁrst wrote this example
Line250 we managed to return the text ﬁeld’s name, not its text—one was item-id and the
Line251 other was item id. This is just the sort of bug that’s easy to let slip through and a
Line252 nightmare to unpick in end-to-end tests—which is why we like to also write
Line253 integration-level tests.
Line254 Implementing the UserRequestListener
Line255 We return to Main to see where we can plug in our new UserRequestListener.
Line256 The changes are minor because we did most of the work when we restructured
Line257 the class earlier in this chapter. We decide to preserve most of the existing
Line258 code for now (even though it’s not quite the right shape) until we’ve made
Line259 more progress, so we just inline our previous joinAuction() method into the
Line260 UserRequestListener’s. We’re also pleased to remove the safelyAddItemToModel()
Line261 wrapper, since the UserRequestListener will be called on the Swing thread. This
Line262 is not obvious from the code as it stands; we make a note to address that later.
Line263 public class Main {
Line264   public static void main(String... args) throws Exception {
Line265     Main main = new Main();
Line266     XMPPConnection connection = 
Line267       connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
Line268     main.disconnectWhenUICloses(connection);
Line269 main.addUserRequestListenerFor(connection);
Line270   }
Line271   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line272     ui.addUserRequestListener(new UserRequestListener() {
Line273       public void joinAuction(String itemId) {
Line274 snipers.addSniper(SniperSnapshot.joining(itemId));
Line275         Chat chat = connection.getChatManager()
Line276                                  .createChat(auctionId(itemId, connection), null);
Line277         notToBeGCd.add(chat); 
Line278         Auction auction = new XMPPAuction(chat);
Line279         chat.addMessageListener(
Line280                new AuctionMessageTranslator(connection.getUser(),
Line281                      new AuctionSniper(itemId, auction, 
Line282                                        new SwingThreadSniperListener(snipers))));
Line283         auction.join();
Line284       }
Line285     });
Line286   }
Line287 }
Line288 We try our end-to-end tests again and ﬁnd that they pass. Slightly stunned, we
Line289 break for coffee.
Line290 Chapter 16
Line291 Sniping for Multiple Items
Line292 188
Line293 
Line294 
Line295 ---
Line296 
Line297 ---
Line298 **Page 189**
Line299 
Line300 Observations
Line301 Making Steady Progress
Line302 We’re starting to see more payback from some of our restructuring work. It was
Line303 pretty easy to convert the end-to-end test to handle multiple items, and most of
Line304 the implementation consisted of teasing apart code that was already working.
Line305 We’ve been careful to keep class responsibilities focused—except for the one
Line306 place, Main, where we’ve put all our working compromises.
Line307 We made an effort to stay honest about writing enough tests, which has forced
Line308 us to consider a couple of edge cases we might otherwise have left. We also intro-
Line309 duced a new intermediate-level “integration” test to allow us to work out the
Line310 implementation of the user interface without dragging in the rest of the system.
Line311 TDD Conﬁdential
Line312 We don’t write up everything that went into the development of our
Line313 examples—that would be boring and waste paper—but we think it’s worth a
Line314 note about what happened with this one. It took us a couple of attempts to get
Line315 this design pointing in the right direction because we were trying to allocate be-
Line316 havior to the wrong objects. What kept us honest was that for each attempt to
Line317 write tests that were focused and made sense, the setup and our assertions kept
Line318 drifting apart. Once we’d broken through our inadequacies as programmers, the
Line319 tests became much clearer.
Line320 Ship It?
Line321 So now that everything works we can get on with more features, right? Wrong.
Line322 We don’t believe that “working” is the same thing as “ﬁnished.” We’ve left quite
Line323 a design mess in Main as we sorted out our ideas, with functionality from various
Line324 slices of the application all jumbled into one, as in Figure 16.3.  Apart from the
Line325 confusion this leaves, most of this code is not really testable except through the
Line326 end-to-end tests. We can get away with that now, while the code is still small,
Line327 but it will be difﬁcult to sustain as the application grows. More importantly,
Line328 perhaps, we’re not getting any unit-test feedback about the internal quality of
Line329 the code.
Line330 We might put this code into production if we knew the code was never going
Line331 to change or there was an emergency. We know that the ﬁrst isn’t true, because
Line332 the application isn’t ﬁnished yet, and being in a hurry is not really a crisis. We
Line333 know we will be working in this code again soon, so we can either clean up now,
Line334 while it’s still fresh in our minds, or re-learn it every time we touch it. Given that
Line335 we’re trying to make an educational point here, you’ve probably guessed
Line336 what we’ll do next.
Line337 189
Line338 Observations
Line339 
Line340 
Line341 ---
