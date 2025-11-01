# Chapter 16: Sniping for Multiple Items (pp.175-190)

---
**Page 175**

Chapter 16
Sniping for Multiple Items
In which we bid for multiple items, splitting the per-connection code
from the per-auction code. We use the table model we just introduced
to display the additional bids. We extend the user interface to allow
users to add items dynamically. We’re pleased to ﬁnd that we don’t
have to change the tests, just their implementation. We tease out a
“user request listener” concept, which means we can test some features
more directly. We leave the code in a bit of a mess.
Testing for Multiple Items
A Tale of Two Items
The next task on our to-do list is to be able to snipe for multiple items at the
same time. We already have much of the machinery we’ll need in place, since our
user interface is based on a table, so some minor structural changes are all we
need to make this work. Looking ahead in the list, we could combine this change
with adding items through the user interface, but we don’t think we need to do
that yet. Just focusing on this one task means we can clarify the distinction be-
tween those features that belong to the Sniper’s connection to the auction house,
and those that belong to an individual auction. So far we’ve speciﬁed the item
on the command line, but we can extend that to pass multiple items in the
argument list.
As always, we start with a test. We want our new test to show that the appli-
cation can bid for and win two different items, so we start by looking at the tests
we already have. Our current test for a successful bid, in “First, a Failing Test”
(page 152), assumes that the application has only one auction—it’s implicit in
code such as:
application.hasShownSniperIsBidding(1000, 1098);
We prepare for multiple items by passing an auction into each of the
ApplicationRunner calls, so the code now looks like:
application.hasShownSniperIsBidding(auction, 1000, 1098);
Within the ApplicationRunner, we remove the itemId ﬁeld and instead extract
the item identiﬁer from the auction parameters.
175


---
**Page 176**

public void hasShownSniperIsBidding(FakeAuctionServer auction, 
                                    int lastPrice, int lastBid) 
{
  driver.showsSniperStatus(auction.getItemId(), lastPrice, lastBid, 
                           textFor(SniperState.BIDDING));
}
The rest is similar, which means we can write a new test:
public class AuctionSniperEndToEndTest {
  private final FakeAuctionServer auction = new FakeAuctionServer("item-54321");  
private final FakeAuctionServer auction2 = new FakeAuctionServer("item-65432");
  @Test public void
sniperBidsForMultipleItems() throws Exception {
    auction.startSellingItem();
auction2.startSellingItem();
    application.startBiddingIn(auction, auction2);
    auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
auction2.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1000, 98, "other bidder");
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
auction2.reportPrice(500, 21, "other bidder");
    auction2.hasReceivedBid(521, ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);    
auction2.reportPrice(521, 22, ApplicationRunner.SNIPER_XMPP_ID);
    application.hasShownSniperIsWinning(auction, 1098);
application.hasShownSniperIsWinning(auction2, 521);
    auction.announceClosed();
auction2.announceClosed();
    application.showsSniperHasWonAuction(auction, 1098);
application.showsSniperHasWonAuction(auction2, 521);
  }
}
Following the protocol convention, we also remember to add a new user,
auction-item-65432, to the chat server to represent the new auction.
Avoiding False Positives
We group the showsSniper methods together instead of pairing them with their
associated auction triggers. This is to catch a problem that we found in an earlier
version where each checking method would pick up the most recent change—the
one we’d just triggered in the previous call. Grouping the checking methods together
gives us conﬁdence that they’re both valid at the same time.
Chapter 16
Sniping for Multiple Items
176


---
**Page 177**

The ApplicationRunner
The one signiﬁcant change we have to make in the ApplicationRunner is to the
startBiddingIn() method. Now it needs to accept a variable number of auctions
passed through to the Sniper’s command line. The conversion is a bit messy since
we have to unpack the item identiﬁers and append them to the end of the other
command-line arguments—this is the best we can do with Java arrays:
public class ApplicationRunner { […]s
  public void startBiddingIn(final FakeAuctionServer... auctions) {
    Thread thread = new Thread("Test Application") {
      @Override public void run() {
        try {
          Main.main(arguments(auctions));
        } catch (Throwable e) {
[…]
for (FakeAuctionServer auction : auctions) {
      driver.showsSniperStatus(auction.getItemId(), 0, 0, textFor(JOINING));
}
  }
  protected static String[] arguments(FakeAuctionServer... auctions) {
    String[] arguments = new String[auctions.length + 3];
    arguments[0] = XMPP_HOSTNAME;
    arguments[1] = SNIPER_ID;
    arguments[2] = SNIPER_PASSWORD;
    for (int i = 0; i < auctions.length; i++) {
      arguments[i + 3] = auctions[i].getItemId();
    }
    return arguments;
  }
}
We run the test and watch it fail.
java.lang.AssertionError: 
Expected: is not null
     got: null
  at auctionsniper.SingleMessageListener.receivesAMessage()
A Diversion, Fixing the Failure Message
We ﬁrst saw this cryptic failure message in Chapter 11. It wasn’t so bad then
because it could only occur in one place and there wasn’t much code to test
anyway. Now it’s more annoying because we have to ﬁnd this method:
public void receivesAMessage(Matcher<? super String> messageMatcher) 
  throws InterruptedException 
{
  final Message message = messages.poll(5, TimeUnit.SECONDS);
  assertThat(message, is(notNullValue()));
  assertThat(message.getBody(), messageMatcher);
}
177
Testing for Multiple Items


---
**Page 178**

and ﬁgure out what we’re missing. We’d like to combine these two assertions and
provide a more meaningful failure. We could write a custom matcher for the
message body but, given that the structure of Message is not going to change
soon, we can use a PropertyMatcher, like this:
public void receivesAMessage(Matcher<? super String> messageMatcher) 
  throws InterruptedException 
{
  final Message message = messages.poll(5, TimeUnit.SECONDS);
  assertThat(message, hasProperty("body", messageMatcher));
}
which produces this more helpful failure report:
java.lang.AssertionError: 
Expected: hasProperty("body", "SOLVersion: 1.1; Command: JOIN;")
     got: null
With slightly more effort, we could have extended a FeatureMatcher to extract
the message body with a nicer failure report. There’s not much difference, expect
that it would be statically type-checked. Now back to business.
Restructuring Main
The test is failing because the Sniper is not sending a Join message for the second
auction. We must change Main to interpret the additional arguments. Just to
remind you, the current structure of the code is:
public class Main {
  public Main() throws Exception {
    SwingUtilities.invokeAndWait(new Runnable() {
      public void run() {
        ui = new MainWindow(snipers);
      }
    });
  }
  public static void main(String... args) throws Exception {
    Main main = new Main();
    main.joinAuction(
      connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]), 
      args[ARG_ITEM_ID]);
  }
  private void joinAuction(XMPPConnection connection, String itemId) {
    disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager()
                            .createChat(auctionId(itemId, connection), null);
[…]
  }    
}
Chapter 16
Sniping for Multiple Items
178


---
**Page 179**

To add multiple items, we need to distinguish between the code that establishes
a connection to the auction server and the code that joins an auction. We start
by holding on to connection so we can reuse it with multiple chats; the result is
not very object-oriented but we want to wait and see how the structure develops.
We also change notToBeGCd from a single value to a collection.
public class Main {
  public static void main(String... args) throws Exception {
    Main main = new Main();
XMPPConnection connection = 
       connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
main.disconnectWhenUICloses(connection);
    main.joinAuction(connection, args[ARG_ITEM_ID]);
  }
  private void joinAuction(XMPPConnection connection, String itemId) {
    Chat chat = connection.getChatManager()
                            .createChat(auctionId(itemId, connection), null);
notToBeGCd.add(chat);
    Auction auction = new XMPPAuction(chat);
    chat.addMessageListener(
        new AuctionMessageTranslator(
            connection.getUser(),
            new AuctionSniper(itemId, auction, 
                              new SwingThreadSniperListener(snipers))));
    auction.join();
  }
}
We loop through each of the items that we’ve been given:
public static void main(String... args) throws Exception {
  Main main = new Main();
  XMPPConnection connection = 
    connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
  main.disconnectWhenUICloses(connection);
for (int i = 3; i < args.length; i++) {
    main.joinAuction(connection, args[i]);
  }
}
This is ugly, but it does show us a separation between the code for the single
connection and multiple auctions. We have a hunch it’ll be cleaned up before long.
The end-to-end test now shows us that display cannot handle the additional
item we’ve just fed in. The table model is still hard-coded to support one row,
so one of the items will be ignored:
[…] but...
  it is not table with row with cells 
    <label with text "item-65432">, <label with text "521">, 
    <label with text "521">, <label with text "Winning">
  because 
in row 0: component 0 text was "item-54321"
179
Testing for Multiple Items


---
**Page 180**

Incidentally, this result is a nice example of why we needed to be aware of timing
in end-to-end tests. This test might fail when looking for auction1 or auction2.
The asynchrony of the system means that we can’t tell which will arrive ﬁrst.
Extending the Table Model
The SnipersTableModel needs to know about multiple items, so we add a new
method to tell it when the Sniper joins an auction. We’ll call this method
from Main.joinAuction() so we show that context ﬁrst, writing an empty
implementation in SnipersTableModel to satisfy the compiler:
private void 
joinAuction(XMPPConnection connection, String itemId) throws Exception {
safelyAddItemToModel(itemId);
[…]
}
private void safelyAddItemToModel(final String itemId) throws Exception {
  SwingUtilities.invokeAndWait(new Runnable() {
    public void run() {
      snipers.addSniper(SniperSnapshot.joining(itemId));
    }
  });
}
We have to wrap the call in an invokeAndWait() because it’s changing the state
of the user interface from outside the Swing thread.
The implementation of SnipersTableModel itself is single-threaded, so we can
write direct unit tests for it—starting with this one for adding a Sniper:
@Test public void
notifiesListenersWhenAddingASniper() {
    SniperSnapshot joining = SniperSnapshot.joining("item123");
    context.checking(new Expectations() { {
      one(listener).tableChanged(with(anInsertionAtRow(0)));
    }});
    assertEquals(0, model.getRowCount());
    model.addSniper(joining);
    assertEquals(1, model.getRowCount());
    assertRowMatchesSnapshot(0, joining);
}
This is similar to the test for updating the Sniper state that we wrote in
“Showing a Bidding Sniper” (page 155), except that we’re calling the new method
and matching a different TableModelEvent. We also package up the comparison
of the table row values into a helper method assertRowMatchesSnapshot().
We make this test pass by replacing the single SniperSnapshot ﬁeld with a
collection and triggering the extra table event. These changes break the existing
Sniper update test, because there’s no longer a default Sniper, so we ﬁx it:
Chapter 16
Sniping for Multiple Items
180


---
**Page 181**

@Test public void 
setsSniperValuesInColumns() { 
  SniperSnapshot joining = SniperSnapshot.joining("item id");
  SniperSnapshot bidding = joining.bidding(555, 666);
  context.checking(new Expectations() {{ 
allowing(listener).tableChanged(with(anyInsertionEvent()));
    one(listener).tableChanged(with(aChangeInRow(0))); 
  }}); 
model.addSniper(joining);
  model.sniperStateChanged(bidding);
  assertRowMatchesSnapshot(0, bidding);
}
We have to add a Sniper to the model. This triggers an insertion event which
isn’t relevant to this test—it’s just supporting infrastructure—so we add an
allowing() clause to let the insertion through. The clause uses a more forgiving
matcher that checks only the type of the event, not its scope. We also change
the matcher for the update event (the one we do care about) to be precise about
which row it’s checking.
Then we write more unit tests to drive out the rest of the functionality. For
these, we’re not interested in the TableModelEvents, so we ignore the listener
altogether.
@Test public void 
holdsSnipersInAdditionOrder() {
  context.checking(new Expectations() { {
    ignoring(listener);
  }});
  model.addSniper(SniperSnapshot.joining("item 0"));
  model.addSniper(SniperSnapshot.joining("item 1"));
  assertEquals("item 0", cellValue(0, Column.ITEM_IDENTIFIER));
  assertEquals("item 1", cellValue(1, Column.ITEM_IDENTIFIER));
}
updatesCorrectRowForSniper() { […]
throwsDefectIfNoExistingSniperForAnUpdate() { […]
The implementation is obvious. The only point of interest is that we add an
isForSameItemAs() method to SniperSnapshot so that it can decide whether it’s
referring to the same item, instead of having the table model extract and compare
identiﬁers.1 It’s a clearer division of responsibilities, with the advantage that we
can change its implementation without changing the table model. We also decide
that not ﬁnding a relevant entry is a programming error.
1. This avoids the “feature envy” code smell [Fowler99].
181
Testing for Multiple Items


---
**Page 182**

public void sniperStateChanged(SniperSnapshot newSnapshot) {
  int row = rowMatching(newSnapshot);
  snapshots.set(row, newSnapshot);
  fireTableRowsUpdated(row, row);
}
private int rowMatching(SniperSnapshot snapshot) {
  for (int i = 0; i < snapshots.size(); i++) {
    if (newSnapshot.isForSameItemAs(snapshots.get(i))) {
      return i;
    }
  }
  throw new Defect("Cannot find match for " + snapshot);
}
This makes the current end-to-end test pass—so we can cross off the task from
our to-do list, Figure 16.1.
Figure 16.1
The Sniper handles multiple items
The End of Off-by-One Errors?
Interacting with the table model requires indexing into a logical grid of cells. We
ﬁnd that this is a case where TDD is particularly helpful. Getting indexing right can
be tricky, except in the simplest cases, and writing tests ﬁrst clariﬁes the boundary
conditions and then checks that our implementation is correct. We’ve both lost too
much time in the past searching for indexing bugs buried deep in the code.
Chapter 16
Sniping for Multiple Items
182


---
**Page 183**

Adding Items through the User Interface
A Simpler Design
The buyers and user interface designers are still working through their ideas, but
they have managed to simplify their original design by moving the item entry
into a top bar instead of a pop-up dialog. The current version of the design looks
like Figure 16.2, so we need to add a text ﬁeld and a button to the display.
Figure 16.2
The Sniper with input ﬁelds in its bar
Making Progress While We Can
The design of user interfaces is outside the scope of this book. For a project of any
size, a user experience professional will consider all sorts of macro- and micro-
details to provide the user with a coherent experience, so one route that some
teams take is to try to lock down the interface design before coding. Our experience,
and that of others like Jeff Patton, is that we can make development progress whilst
the design is being sorted out. We can build to the team’s current understanding
of the features and keep our code (and attitude) ﬂexible to respond to design ideas
as they ﬁrm up—and perhaps even feed our experience back into the process.
Update the Test
Looking back at AuctionSniperEndToEndTest, it already expresses everything we
want the application to do: it describes how the Sniper connects to one or more
auctions and bids. The change is that we want to describe a different implemen-
tation of some of that behavior (establishing the connection through the user
interface rather than the command line) which happens in the ApplicationRunner.
We need a restructuring similar to the one we just made in Main, splitting the
connection from the individual auctions. We pull out a startSniper() method
that starts up and checks the Sniper, and then start bidding for each auction
in turn.
183
Adding Items through the User Interface


---
**Page 184**

public class ApplicationRunner {
  public void startBiddingIn(final FakeAuctionServer... auctions) {
    startSniper();
    for (FakeAuctionServer auction : auctions) {
final String itemId = auction.getItemId();
      driver.startBiddingFor(itemId);
      driver.showsSniperStatus(itemId, 0, 0, textFor(SniperState.JOINING));
    }
  }
  private void startSniper() {
// as before without the call to showsSniperStatus()
  }
[…]
}
The other change to the test infrastructure is implementing the new method
startBiddingFor() in AuctionSniperDriver. This ﬁnds and ﬁlls in the text ﬁeld
for the item identiﬁer, then ﬁnds and clicks on the Join Auction button.
public class AuctionSniperDriver extends JFrameDriver {
  @SuppressWarnings("unchecked")
  public void startBiddingFor(String itemId) {
    itemIdField().replaceAllText(itemId); 
    bidButton().click(); 
  }
  private JTextFieldDriver itemIdField() {
    JTextFieldDriver newItemId = 
      new JTextFieldDriver(this, JTextField.class, named(MainWindow.NEW_ITEM_ID_NAME));
    newItemId.focusWithMouse();
    return newItemId;
  }
  private JButtonDriver bidButton() {
    return new JButtonDriver(this, JButton.class, named(MainWindow.JOIN_BUTTON_NAME));
  }
[…]
}
Neither of these components exist yet, so the test fails looking for the text ﬁeld.
[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
contained 0 JTextField (with name "item id")
Adding an Action Bar
We address this failure by adding a new panel across the top to contain the
text ﬁeld for the identiﬁer and the Join Auction button, wrapping up the activity
in a makeControls() method to help express our intent. We realize that this code
isn’t very exciting, but we want to show its structure now before we add any
behavior.
Chapter 16
Sniping for Multiple Items
184


---
**Page 185**

public class MainWindow extends JFrame {
  public MainWindow(TableModel snipers) {
    super(APPLICATION_TITLE);
    setName(MainWindow.MAIN_WINDOW_NAME);
    fillContentPane(makeSnipersTable(snipers), makeControls());
[…]
  }
  private JPanel makeControls() {
    JPanel controls = new JPanel(new FlowLayout());
    final JTextField itemIdField = new JTextField();
    itemIdField.setColumns(25);
    itemIdField.setName(NEW_ITEM_ID_NAME);
    controls.add(itemIdField);
    JButton joinAuctionButton = new JButton("Join Auction");
    joinAuctionButton.setName(JOIN_BUTTON_NAME);
    controls.add(joinAuctionButton);
    return controls;
  }
[…]
}
With the action bar in place, our next test fails because we don’t create the
identiﬁed rows in the table model.
[…] but...
   all top level windows
   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
   contained 1 JTable ()
it is not with row with cells
   <label with text "item-54321">, <label with text "0">, 
   <label with text "0">, <label with text "Joining">
A Design Moment
Now what do we do? To review our position: we have a broken acceptance
test pending, we have the user interface structure but no behavior, and the
SnipersTableModel still handles only one Sniper at a time. Our goal is that, when
we click on the Join Auction button, the application will attempt to join the
auction speciﬁed in the item ﬁeld and add a new row to the list of auctions to
show that the request is being handled.
In practice, this means that we need a Swing ActionListener for the JButton
that will use the text from the JTextField as an item identiﬁer for the new session.
Its implementation will add a row to the SnipersTableModel and create a new
Chat to the Southabee’s On-Line server. The catch is that everything to do with
connections is in Main, whereas the button and the text ﬁeld are in MainWindow.
This is a distinction we’d like to maintain, since it keeps the responsibilities of
the two classes focused.
185
Adding Items through the User Interface


---
**Page 186**

We stop for a moment to think about the structure of the code, using the CRC
cards we mentioned in “Roles, Responsibilities, Collaborators” on page 16 to
help us visualize our ideas. After some discussion, we remind ourselves that the
job of MainWindow is to manage our UI components and their interactions; it
shouldn’t also have to manage concepts such as “connection” or “chat.” When
a user interaction implies an action outside the user interface, MainWindow should
delegate to a collaborating object.
To express this, we decide to add a listener to MainWindow to notify neighboring
objects about such requests. We call the new collaborator a UserRequestListener
since it will be responsible for handling requests made by the user:
public interface UserRequestListener extends EventListener {
  void joinAuction(String itemId);
}
Another Level of Testing
We want to write a test for our proposed new behavior, but we can’t just write
a simple unit test because of Swing threading. We can’t be sure that the Swing
code will have ﬁnished running by the time we check any assertions at the end
of the test, so we need something that will wait until the tested code has
stabilized—what we usually call an integration test because it’s testing how our
code works with a third-party library. We can use WindowLicker for this level
of testing as well as for our end-to-end tests. Here’s the new test:
public class MainWindowTest {
  private final SnipersTableModel tableModel = new SnipersTableModel();
  private final MainWindow mainWindow = new MainWindow(tableModel);
  private final AuctionSniperDriver driver = new AuctionSniperDriver(100);
  @Test public void
makesUserRequestWhenJoinButtonClicked() {
    final ValueMatcherProbe<String> buttonProbe = 
      new ValueMatcherProbe<String>(equalTo("an item-id"), "join request");
    mainWindow.addUserRequestListener(
        new UserRequestListener() {
          public void joinAuction(String itemId) {
            buttonProbe.setReceivedValue(itemId);
          }
        });
    driver.startBiddingFor("an item-id");
    driver.check(buttonProbe);
  }
}
Chapter 16
Sniping for Multiple Items
186


---
**Page 187**

WindowLicker Probes
In WindowLicker, a probe is an object that checks for a given state. A driver’s
check() method repeatedly ﬁres the given probe until it’s satisﬁed or times out. In
this test, we use a ValueMatcherProbe, which compares a value against a Ham-
crest matcher, to wait for the UserRequestListener’s joinAuction() to be called
with the right auction identiﬁer.
We create an empty implementation of MainWindow.addUserRequestListener,
to get through the compiler, and the test fails:
Tried to look for...
    join request "an item-id"
but...
    join request "an item-id". Received nothing
To make this test pass, we ﬁll in the request listener infrastructure in MainWindow
using Announcer, a utility class that manages collections of listeners.2 We add a
Swing ActionListener that extracts the item identiﬁer and announces it to the
request listeners. The relevant parts of MainWindow look like this:
public class MainWindow extends JFrame {
  private final Announcer<UserRequestListener> userRequests = 
                                     Announcer.to(UserRequestListener.class); 
  public void addUserRequestListener(UserRequestListener userRequestListener) {
    userRequests.addListener(userRequestListener); 
  } 
[…]
  private JPanel makeControls(final SnipersTableModel snipers) {
[…]
    joinAuctionButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {
userRequests.announce().joinAuction(itemIdField.getText());
      }
    });
[…]
  }
}
To emphasize the point here, we’ve converted an ActionListener event, which
is internal to the user interface framework, to a UserRequestListener event,
which is about users interacting with an auction. These are two separate domains
and MainWindow’s job is to translate from one to the other. MainWindow is
not concerned with how any implementation of UserRequestListener might
work—that would be too much responsibility.
2.
Announcer is included in the examples that ship with jMock.
187
Adding Items through the User Interface


---
**Page 188**

Micro-Hubris
In case this level of testing seems like overkill, when we ﬁrst wrote this example
we managed to return the text ﬁeld’s name, not its text—one was item-id and the
other was item id. This is just the sort of bug that’s easy to let slip through and a
nightmare to unpick in end-to-end tests—which is why we like to also write
integration-level tests.
Implementing the UserRequestListener
We return to Main to see where we can plug in our new UserRequestListener.
The changes are minor because we did most of the work when we restructured
the class earlier in this chapter. We decide to preserve most of the existing
code for now (even though it’s not quite the right shape) until we’ve made
more progress, so we just inline our previous joinAuction() method into the
UserRequestListener’s. We’re also pleased to remove the safelyAddItemToModel()
wrapper, since the UserRequestListener will be called on the Swing thread. This
is not obvious from the code as it stands; we make a note to address that later.
public class Main {
  public static void main(String... args) throws Exception {
    Main main = new Main();
    XMPPConnection connection = 
      connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
    main.disconnectWhenUICloses(connection);
main.addUserRequestListenerFor(connection);
  }
  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
      public void joinAuction(String itemId) {
snipers.addSniper(SniperSnapshot.joining(itemId));
        Chat chat = connection.getChatManager()
                                 .createChat(auctionId(itemId, connection), null);
        notToBeGCd.add(chat); 
        Auction auction = new XMPPAuction(chat);
        chat.addMessageListener(
               new AuctionMessageTranslator(connection.getUser(),
                     new AuctionSniper(itemId, auction, 
                                       new SwingThreadSniperListener(snipers))));
        auction.join();
      }
    });
  }
}
We try our end-to-end tests again and ﬁnd that they pass. Slightly stunned, we
break for coffee.
Chapter 16
Sniping for Multiple Items
188


---
**Page 189**

Observations
Making Steady Progress
We’re starting to see more payback from some of our restructuring work. It was
pretty easy to convert the end-to-end test to handle multiple items, and most of
the implementation consisted of teasing apart code that was already working.
We’ve been careful to keep class responsibilities focused—except for the one
place, Main, where we’ve put all our working compromises.
We made an effort to stay honest about writing enough tests, which has forced
us to consider a couple of edge cases we might otherwise have left. We also intro-
duced a new intermediate-level “integration” test to allow us to work out the
implementation of the user interface without dragging in the rest of the system.
TDD Conﬁdential
We don’t write up everything that went into the development of our
examples—that would be boring and waste paper—but we think it’s worth a
note about what happened with this one. It took us a couple of attempts to get
this design pointing in the right direction because we were trying to allocate be-
havior to the wrong objects. What kept us honest was that for each attempt to
write tests that were focused and made sense, the setup and our assertions kept
drifting apart. Once we’d broken through our inadequacies as programmers, the
tests became much clearer.
Ship It?
So now that everything works we can get on with more features, right? Wrong.
We don’t believe that “working” is the same thing as “ﬁnished.” We’ve left quite
a design mess in Main as we sorted out our ideas, with functionality from various
slices of the application all jumbled into one, as in Figure 16.3.  Apart from the
confusion this leaves, most of this code is not really testable except through the
end-to-end tests. We can get away with that now, while the code is still small,
but it will be difﬁcult to sustain as the application grows. More importantly,
perhaps, we’re not getting any unit-test feedback about the internal quality of
the code.
We might put this code into production if we knew the code was never going
to change or there was an emergency. We know that the ﬁrst isn’t true, because
the application isn’t ﬁnished yet, and being in a hurry is not really a crisis. We
know we will be working in this code again soon, so we can either clean up now,
while it’s still fresh in our minds, or re-learn it every time we touch it. Given that
we’re trying to make an educational point here, you’ve probably guessed
what we’ll do next.
189
Observations


---
**Page 190**

This page intentionally left blank 


