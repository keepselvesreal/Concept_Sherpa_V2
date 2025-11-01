# Chapter 15: Towards a Real User Interface (pp.149-174)

---
**Page 149**

Chapter 15
Towards a Real User Interface
In which we grow the user interface from a label to a table. We achieve
this by adding a feature at a time, instead of taking the risk of replacing
the whole thing in one go. We discover that some of the choices we
made are no longer valid, so we dare to change existing code. We
continue to refactor and sense that a more interesting structure is
starting to appear.
A More Realistic Implementation
What Do We Have to Do Next?
So far, we’ve been making do with a simple label in the user interface. That’s
been effective for helping us clarify the structure of the application and prove
that our ideas work, but the next tasks coming up will need more, and the client
wants to see something that looks closer to Figure 9.1. We will need to show
more price details from the auction and handle multiple items.
The simplest option would be just to add more text into the label, but we think
this is the right time to introduce more structure into the user interface. We de-
ferred putting effort into this part of the application, and we think we should
catch up now to be ready for the more complex requirements we’re about to
implement. We decide to make the obvious choice, given our use of Swing, and
replace the label with a table component. This decision gives us a clear direction
for where our design should go next.
The Swing pattern for using a JTable is to associate it with a TableModel. The
table component queries the model for values to present, and the model notiﬁes
the table when those values change. In our application, the relationships will
look like Figure 15.1.  We call the new class SnipersTableModel because we want
it to support multiple Snipers. It will accept updates from the Snipers and provide
a representation of those values to its JTable.
The question is how to get there from here.
149


---
**Page 150**

Figure 15.1
Swing table model for the AuctionSniper
Replacing JLabel
We want to get the pieces into place with a minimum of change, without tearing
the whole application apart. The smallest step we can think of is to replace the
existing implementation (a JLabel) with a single-cell JTable, from which we can
then grow the additional functionality. We start, of course, with the test, changing
our harness to look for a cell in a table, rather than a label.
public class AuctionSniperDriver extends JFrameDriver { […]
  public void showsSniperStatus(String statusText) {
new JTableDriver(this).hasCell(withLabelText(equalTo(statusText)));
  }
}
This generates a failure message because we don’t yet have a table.
[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
contained 0 JTable ()
Chapter 15
Towards a Real User Interface
150


---
**Page 151**

We ﬁx this test by retroﬁtting a minimal JTable implementation. From now
on, we want to speed up our narrative, so we’ll just show the end result. If we
were feeling cautious we would ﬁrst add an empty table, to ﬁx the immediate
failure, and then add its contents. It turns out that we don’t have to change any
existing classes outside MainWindow because it encapsulates the act of updating
the status. Here’s the new code:
public class MainWindow extends JFrame { […]
private final SnipersTableModel snipers = new SnipersTableModel();
  public MainWindow() {
    super(APPLICATION_TITLE);
    setName(MainWindow.MAIN_WINDOW_NAME);
fillContentPane(makeSnipersTable());
    pack();
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setVisible(true);
  }
  private void fillContentPane(JTable snipersTable) {
    final Container contentPane = getContentPane();
    contentPane.setLayout(new BorderLayout());
    contentPane.add(new JScrollPane(snipersTable), BorderLayout.CENTER);
  }
  private JTable makeSnipersTable() {
    final JTable snipersTable = new JTable(snipers);
    snipersTable.setName(SNIPERS_TABLE_NAME);
    return snipersTable;
  }
  public void showStatusText(String statusText) {
snipers.setStatusText(statusText);
  }
}
public class SnipersTableModel extends AbstractTableModel {
  private String statusText = STATUS_JOINING;
  public int getColumnCount() { return 1; }
  public int getRowCount() { return 1; }
  public Object getValueAt(int rowIndex, int columnIndex) { return statusText; }
  public void setStatusText(String newStatusText) {
    statusText = newStatusText;
    fireTableRowsUpdated(0, 0);
  }
}
151
A More Realistic Implementation


---
**Page 152**

Still Ugly
As you can see, the SnipersTableModel really is a minimal implementation; the
only value that can vary is the statusText. It inherits most of its behavior from
the Swing AbstractTableModel, including the infrastructure for notifying the
JTable of data changes. The result is as ugly as our previous version, except that
now the JTable adds a default column title “A”, as in Figure 15.2. We’ll work
on the presentation in a moment.
Figure 15.2
Sniper with a single-cell table
Displaying Price Details
First, a Failing Test
Our next task is to display information about the Sniper’s position in the auction:
item identiﬁer, last auction price, last bid, status. These values come from updates
from the auction and the state held within the application. We need to pass them
through from their source to the table model and then render them in the display.
Of course, we start with the test. Given that this feature should be part of the
basic functionality of the application, not separate from what we already have,
we update our existing acceptance tests—starting with just one test so we don’t
break everything at once. Here’s the new version:
public class AuctionSniperEndToEndTest {
  @Test public void
sniperWinsAnAuctionByBiddingHigher() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
    auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1000, 98, "other bidder");
    application.hasShownSniperIsBidding(1000, 1098); // last price, last bid
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
    application.hasShownSniperIsWinning(1098); // winning bid
    auction.announceClosed();
    application.showsSniperHasWonAuction(1098); // last price
  }
}
Chapter 15
Towards a Real User Interface
152


---
**Page 153**

public class ApplicationRunner {
private String itemId;
  public void startBiddingIn(final FakeAuctionServer auction) {
itemId = auction.getItemId();
[…]
  }
[…]
  public void hasShownSniperIsBidding(int lastPrice, int lastBid) {
    driver.showsSniperStatus(itemId, lastPrice, lastBid, 
                             MainWindow.STATUS_BIDDING);
  }
  public void hasShownSniperIsWinning(int winningBid) {
    driver.showsSniperStatus(itemId, winningBid, winningBid, 
                             MainWindow.STATUS_WINNING);
  }
  public void showsSniperHasWonAuction(int lastPrice) {
    driver.showsSniperStatus(itemId, lastPrice, lastPrice, 
                             MainWindow.STATUS_WON);
  }
}
public class AuctionSniperDriver extends JFrameDriver {
[…]
  public void showsSniperStatus(String itemId, int lastPrice, int lastBid, 
                                String statusText)
  {
    JTableDriver table = new JTableDriver(this);
    table.hasRow(
      matching(withLabelText(itemId), withLabelText(valueOf(lastPrice)), 
               withLabelText(valueOf(lastBid)), withLabelText(statusText)));
  }
}
We need the item identiﬁer so the test can look for it in the row, so we make
the ApplicationRunner hold on it when connecting to an auction. We extend the
AuctionSniperDriver to look for a table row that shows the item identiﬁer, last
price, last bid, and sniper status.
The test fails because the row has no details, only the status text:
[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTable ()
 it is not with row with cells 
   <label with text "item-54321">, <label with text "1000">, 
   <label with text "1098">, <label with text "Bidding">
because 
      in row 0: component 0 text was "Bidding"
153
Displaying Price Details


---
**Page 154**

Sending the State out of the Sniper
With an acceptance test to show us where we want to get to, we can ﬁll in the
steps along the way. As usual, we work “outside-in,” from the event that triggers
the behavior; in this case it’s a price update from Southabee’s On-Line.
Following along the sequence of method calls, we don’t have to change
AuctionMessageTranslator, so we start by looking at AuctionSniper and its
unit tests.
AuctionSniper notiﬁes changes in its state to neighbors that implement the
SniperListener interface which, as you might remember, has four callback
methods, one for each state of the Sniper. Now we also need to pass in the current
state of the Sniper when we notify a listener. We could add the same set of argu-
ments to each method, but that would be duplication; so, we introduce a value
type to carry the Sniper’s state. This is an example of “bundling up” that we
described in “Value Types” (page 59). Here’s a ﬁrst cut:
public class SniperState {
  public final String itemId;
  public final int lastPrice;
  public final int lastBid;
  public SniperState(String itemId, int lastPrice, int lastBid) {
    this.itemId = itemId;
    this.lastPrice = lastPrice;
    this.lastBid = lastBid;
  }
}
To save effort, we use the reﬂective builders from the Apache commons.lang
library to implement equals(), hashCode(), and toString() in the new class. We
could argue that we’re being premature with these features, but in practice we’ll
need them in a moment when we write our unit tests.
Public Final Fields
We’ve adopted a habit of using public ﬁnal ﬁelds in value types, at least while we’re
in the process of sorting out what the type should do. It makes it obvious that the
value is immutable and reduces the overhead of maintaining getters when the class
isn’t yet stable. Our ambition, which we might not achieve, is to replace all ﬁeld
access with meaningful action methods on the type. We’ll see how that pans out.
We don’t want to break all the tests at once, so we start with an easy one. In
this test there’s no history, all we have to do in the Sniper is construct a
SniperState from information available at the time and pass it to the listener.
Chapter 15
Towards a Real User Interface
154


---
**Page 155**

public class AuctionSniperTest { […]
  @Test public void
bidsHigherAndReportsBiddingWhenNewPriceArrives() {
    final int price = 1001;
    final int increment = 25;
    final int bid = price + increment;
    context.checking(new Expectations() {{
      one(auction).bid(bid);
      atLeast(1).of(sniperListener).sniperBidding(
new SniperState(ITEM_ID, price, bid));
    }});
    sniper.currentPrice(price, increment, PriceSource.FromOtherBidder);
  }
}
Then we make the test pass:
public class AuctionSniper implements AuctionEventListener { […]
  public void currentPrice(int price, int increment, PriceSource priceSource) {
    isWinning = priceSource == PriceSource.FromSniper;
    if (isWinning) {
      sniperListener.sniperWinning();
    } else {
int bid = price + increment;
      auction.bid(bid);
      sniperListener.sniperBidding(new SniperState(itemId, price, bid));
    }
  }
}
To get the code to compile, we also add the state argument to the
sniperBidding() method in 
SniperStateDisplayer, which implements
SniperListener, but don’t yet do anything with it.
The one signiﬁcant change is that the Sniper needs access to the item identiﬁer
so it can construct a SniperState. Given that the Sniper doesn’t need this value
for any other reason, we could have kept it in the SniperStateDisplayer and
added it in when an event passes through, but we think it’s reasonable that the
Sniper has access to this information. We decide to pass the identiﬁer into the
AuctionSniper constructor; it’s available at the time, and we don’t want to get
it from the Auction object which may have its own form of identiﬁer for an item.
We have one other test that refers to the sniperBidding() method, but only
as an “allowance.” We use a matcher that says that, since it’s only supporting
the interesting part of the test, we don’t care about the contents of the state object.
allowing(sniperListener).sniperBidding(with(any(SniperState.class)));
Showing a Bidding Sniper
We’ll take larger steps for the next task—presenting the state in the user
interface—as there are some new moving parts, including a new unit test. The
155
Displaying Price Details


---
**Page 156**

ﬁrst version of the code will be clumsier than we would like but, as you’ll soon
see, there’ll be interesting opportunities for cleaning up.
Our very ﬁrst step is to pass the new state parameter, which we’ve been ignor-
ing, through MainWindow to a new method in SnipersTableModel. While we’re at
it, we notice that just passing events through MainWindow isn’t adding much value,
so we make a note to deal with that later.
public class SniperStateDisplayer implements SniperListener { […]
  public void sniperBidding(final SniperState state) {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() { 
ui.sniperStatusChanged(state, MainWindow.STATUS_BIDDING);
      } 
    });
  }
}
public class MainWindow extends JFrame { […]
  public void sniperStatusChanged(SniperState sniperState, String statusText) {
    snipers.sniperStatusChanged(sniperState, statusText);
  }
}
To get the new values visible on screen, we need to ﬁx SnipersTableModel so
that it makes them available to its JTable, starting with a unit test. We take a
small design leap by introducing a Java enum to represent the columns in the
table—it’s more meaningful than just using integers.
public enum Column {
  ITEM_IDENTIFIER,
  LAST_PRICE,
  LAST_BID,
  SNIPER_STATUS;
  public static Column at(int offset) { return values()[offset]; }
}
The table model needs to do two things when its state changes: hold onto the
new values and notify the table that they’ve changed. Here’s the test:
@RunWith(JMock.class)
public class SnipersTableModelTest {
  private final Mockery context = new Mockery();
  private TableModelListener listener = context.mock(TableModelListener.class);
  private final SnipersTableModel model = new SnipersTableModel();
  @Before public void attachModelListener() {  1
    model.addTableModelListener(listener);
  }
  @Test public void
hasEnoughColumns() {  2
    assertThat(model.getColumnCount(), equalTo(Column.values().length));
  }
Chapter 15
Towards a Real User Interface
156


---
**Page 157**

  @Test public void
setsSniperValuesInColumns() {
    context.checking(new Expectations() {{
      one(listener).tableChanged(with(aRowChangedEvent()));  3
    }});
    model.sniperStatusChanged(new SniperState("item id", 555, 666),  4
                              MainWindow.STATUS_BIDDING);
    assertColumnEquals(Column.ITEM_IDENTIFIER, "item id"); 5
    assertColumnEquals(Column.LAST_PRICE, 555);
    assertColumnEquals(Column.LAST_BID, 666);
    assertColumnEquals(Column.SNIPER_STATUS, MainWindow.STATUS_BIDDING);
  }
  private void assertColumnEquals(Column column, Object expected) {
    final int rowIndex = 0;
    final int columnIndex = column.ordinal();
    assertEquals(expected, model.getValueAt(rowIndex, columnIndex);
  }
  private Matcher<TableModelEvent> aRowChangedEvent() { 6
    return samePropertyValuesAs(new TableModelEvent(model, 0));
  }
}
1
We attach a mock implementation of TableModelListener to the model. This
is one of the few occasions where we break our rule “Only Mock Types That
You Own” (page 69) because the table model design ﬁts our design approach
so well.
2
We add a ﬁrst test to make sure we’re rendering the right number of columns.
Later, we’ll do something about the column titles.
3
This expectation checks that we notify any attached JTable that the contents
have changed.
4
This is the event that triggers the behavior we want to test.
5
We assert that the table model returns the right values in the right columns.
We hard-code the row number because we’re still assuming that there is
only one.
6
There’s no speciﬁc equals() method on TableModelEvent, so we use a
matcher that will reﬂectively compare the property values of any event it re-
ceives against an expected example. Again, we hard-code the row number.
After the usual red/green cycle, we end up with an implementation that looks
like this:
157
Displaying Price Details


---
**Page 158**

public class SnipersTableModel extends AbstractTableModel {
  private final static SniperState STARTING_UP = new SniperState("", 0, 0);
  private String statusText = MainWindow.STATUS_JOINING;
  private SniperState sniperState = STARTING_UP; 1
[…]
  public int getColumnCount() { 2
    return Column.values().length; 
  }
  public int getRowCount() {
    return 1;
  }
  public Object getValueAt(int rowIndex, int columnIndex) { 3
    switch (Column.at(columnIndex)) {
    case ITEM_IDENTIFIER:
      return sniperState.itemId;
    case LAST_PRICE:
      return sniperState.lastPrice;
    case LAST_BID:
      return sniperState.lastBid;
    case SNIPER_STATUS:
      return statusText;
    default:
      throw new IllegalArgumentException("No column at " + columnIndex);
    }
  }
  public void sniperStatusChanged(SniperState newSniperState, 4
                                  String newStatusText) 
  { 
    sniperState = newSniperState;
    statusText = newStatusText;
    fireTableRowsUpdated(0, 0);
  }
}
1
We provide an initial SniperState with “empty” values so that the table
model will work before the Sniper has connected.
2
For the dimensions, we just return the numbers of values in Column or a
hard-coded row count.
3
This method unpacks the value to return depending on the column that is
speciﬁed. The advantage of using an enum is that the compiler will help with
missing branches in the switch statement (although it still insists on a default
case). We’re not keen on using switch, as it’s not object-oriented, so we’ll
keep an eye on this too.
4
The Sniper-speciﬁc method. It sets the ﬁelds and then triggers its clients to
update.
If we run our acceptance test again, we ﬁnd we’ve made some progress. It’s
gone past the Bidding check and now fails because the last price column, “B”,
has not yet been updated. Interestingly, the status column shows Winning correctly,
because that code is still working.
Chapter 15
Towards a Real User Interface
158


---
**Page 159**

[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTable ()
 it is not with row with cells 
   <label with text "item-54321">, <label with text "1098">, 
   <label with text "1098">, <label with text "Winning">
because 
      in row 0: component 1 text was "1000"
and the proof is in Figure 15.3.
Figure 15.3
Sniper showing a row of detail
Simplifying Sniper Events
Listening to the Mood Music
We have one kind of Sniper event, Bidding, that we can handle all the way
through our application. Now we have to do the same thing to Winning, Lost,
and Won.
Frankly, that’s just dull. There’s too much repetitive work needed to make the
other cases work—setting them up in the Sniper and passing them through
the layers. Something’s wrong with the design. We toss this one around for a
while and eventually notice that we would have a subtle duplication in our code
if we just carried on. We would be splitting the transmission of the Sniper state
into two mechanisms: the choice of listener method and the state object. That’s
one mechanism too many.
We realize that we could collapse our events into one notiﬁcation that includes
the prices and the Sniper status. Of course we’re transmitting the same information
whichever mechanism we choose—but, looking at the chain of methods calls,
it would be simpler to have just one method and pass everything through in
SniperState.
Having made this choice, can we do it cleanly without ripping up the
metaphorical ﬂoorboards? We believe we can—but ﬁrst, one more clariﬁcation.
We want to start by creating a type to represent the Sniper’s status (winning,
losing, etc.) in the auction, but the terms “status” and “state” are too close to
distinguish easily. We kick around some vocabulary and eventually decide that
a better term for what we now call SniperState would be SniperSnapshot: a
description of the Sniper’s relationship with the auction at this moment in time.
This frees up the name SniperState to describe whether the Sniper is winning,
losing, and so on, which matches the terminology of the state machine we drew
159
Simplifying Sniper Events


---
**Page 160**

in Figure 9.3 on page 78. Renaming the SniperState takes a moment, and we
change the value in Column from SNIPER_STATUS to SNIPER_STATE.
20/20 Hindsight
We’ve just gone through not one but two of those forehead-slapping moments that
make us wonder why we didn’t see it the ﬁrst time around. Surely, if we’d spent
more time on the design, we wouldn’t have to change it now? Sometimes that’s
true. Our experience, however, is that nothing shakes out a design like trying to
implement it, and between us we know just a handful of people who are smart
enough to get their designs always right. Our coping mechanism is to get into the
critical areas of the code early and to allow ourselves to change our collective mind
when we could do better. We rely on our skills, on taking small steps, and on the
tests to protect us when we make changes.
Repurposing sniperBidding()
Our ﬁrst step is to take the method that does most of what we want,
sniperBidding(), and rework it to ﬁt our new scheme. We create an enum that
takes the SniperState name we’ve just freed up and add it to SniperSnapshot;
we take the sniperState ﬁeld out of the method arguments; and, ﬁnally, we re-
name the method to sniperStateChanged() to match its intended new role. We
push the changes through to get the following code:
public enum SniperState {
  JOINING,
  BIDDING,
  WINNING,
  LOST,
  WON;
}
public class AuctionSniper implements AuctionEventListener { […]
  public void currentPrice(int price, int increment, PriceSource priceSource) {
    isWinning = priceSource == PriceSource.FromSniper;
    if (isWinning) {
      sniperListener.sniperWinning();
    } else {
      final int bid = price + increment;
      auction.bid(bid);
      sniperListener.sniperStateChanged(
        new SniperSnapshot(itemId, price, bid, SniperState.BIDDING));
    }
  }
}
Chapter 15
Towards a Real User Interface
160


---
**Page 161**

In the table model, we use simple indexing to translate the enum into displayable
text.
public class SnipersTableModel extends AbstractTableModel { […]
private static String[] STATUS_TEXT = { MainWindow.STATUS_JOINING, 
                                          MainWindow.STATUS_BIDDING };
  public void sniperStateChanged(SniperSnapshot newSnapshot) {
    this.snapshot = newSnapshot;
    this.state = STATUS_TEXT[newSnapshot.state.ordinal()];
    fireTableRowsUpdated(0, 0);
  }
}
We make some minor changes to the test code, to get it through the compiler,
plus one more interesting adjustment. You might remember that we wrote an
expectation clause that ignored the details of the SniperState:
allowing(sniperListener).sniperBidding(with(any(SniperState.class)));
We can no longer rely on the choice of method to distinguish between different
events, so we have to dig into the new SniperSnapshot object to make sure we’re
matching the right one. We rewrite the expectation with a custom matcher that
checks just the state:
public class AuctionSniperTest {
[…]
  context.checking(new Expectations() {{
    ignoring(auction);
    allowing(sniperListener).sniperStateChanged(
                               with(aSniperThatIs(BIDDING))); 
                                                then(sniperState.is("bidding"));
    atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
  }});
[…]
  private Matcher<SniperSnapshot> aSniperThatIs(final SniperState state) {
    return new FeatureMatcher<SniperSnapshot, SniperState>(
             equalTo(state), "sniper that is ", "was") 
    {
      @Override
      protected SniperState featureValueOf(SniperSnapshot actual) {
        return actual.state;
      }
    };
  }
}
161
Simplifying Sniper Events


---
**Page 162**

Lightweight Extensions to jMock
We added a small helper method aSniperThatIs() to package up our specializa-
tion of FeatureMatcher behind a descriptive name. You’ll see that the method
name is intended to make the expectation code read well (or as well as we can
manage in Java).We did the same earlier in the chapter with aRowChangedEvent().
As we discussed in “Different Levels of Language” on page 51, we’re effectively
writing extensions to a language that’s embedded in Java. jMock was designed to
be extensible in this way, so that programmers can plug in features described in
terms of the code they’re testing.You could think of these little helper methods as
creating new nouns in jMock’s expectation language.
Filling In the Numbers
Now we’re in a position to feed the missing price to the user interface, which
means changing the listener call from sniperWinning() to sniperStateChanged()
so that the listener will receive the value in a SniperSnapshot. We start by
changing the test to expect the different listener call, and to trigger the event by
calling currentPrice() twice: once to force the Sniper to bid, and again to tell
the Sniper that it’s winning.
public class AuctionSniperTest { […]
  @Test public void
reportsIsWinningWhenCurrentPriceComesFromSniper() {
    context.checking(new Expectations() {{
      ignoring(auction);
      allowing(sniperListener).sniperStateChanged(
                                 with(aSniperThatIs(BIDDING))); 
                                               then(sniperState.is("bidding"));
atLeast(1).of(sniperListener).sniperStateChanged(
                               new SniperSnapshot(ITEM_ID, 135, 135, WINNING)); 
                                               when(sniperState.is("bidding"));
    }});
sniper.currentPrice(123, 12, PriceSource.FromOtherBidder);
    sniper.currentPrice(135, 45, PriceSource.FromSniper);
  }
}
We change AuctionSniper to retain its most recent values by holding on to the
last snapshot. We also add some helper methods to SniperSnapshot, and ﬁnd
that our implementation starts to simplify.
Chapter 15
Towards a Real User Interface
162


---
**Page 163**

public class AuctionSniper implements AuctionEventListener { […]
private SniperSnapshot snapshot;
  public AuctionSniper(String itemId, Auction auction, SniperListener sniperListener)
  {
    this.auction = auction;
    this.sniperListener = sniperListener;
this.snapshot = SniperSnapshot.joining(itemId);
  }
  public void currentPrice(int price, int increment, PriceSource priceSource) {
    isWinning = priceSource == PriceSource.FromSniper;
    if (isWinning) {
snapshot = snapshot.winning(price);
    } else {
      final int bid = price + increment;
      auction.bid(bid);
snapshot = snapshot.bidding(price, bid);
    }
sniperListener.sniperStateChanged(snapshot);
  }
}
public class SniperSnapshot { […]
  public SniperSnapshot bidding(int newLastPrice, int newLastBid) {
    return new SniperSnapshot(itemId, newLastPrice, newLastBid, SniperState.BIDDING);
  }
  public SniperSnapshot winning(int newLastPrice) {
    return new SniperSnapshot(itemId, newLastPrice, lastBid, SniperState.WINNING);
  }
  public static SniperSnapshot joining(String itemId) {
    return new SniperSnapshot(itemId, 0, 0, SniperState.JOINING);
  }
}
Nearly a State Machine
We’ve added some constructor methods to SniperSnapshot that provide a clean
mechanism for moving between snapshot states. It’s not a full state machine, in
that we don’t enforce only “legal” transitions, but it’s a hint, and it nicely packages
up the getting and setting of ﬁelds.
We remove sniperWinning() from SniperListener and its implementations,
and add a value for winning to SnipersTableModel.STATUS_TEXT.
Now, the end-to-end test passes.
163
Simplifying Sniper Events


---
**Page 164**

Follow Through
Converting Won and Lost
This works, but we still have two notiﬁcation methods in SniperListener left to
convert before we can say we’re done: sniperWon() and sniperLost(). Again,
we replace these with sniperStateChanged() and add two new values to
SniperState.
Plugging these changes in, we ﬁnd that the code simpliﬁes further. We drop
the isWinning ﬁeld from the Sniper and move some decision-making into
SniperSnapshot, which will know whether the Sniper is winning or losing,
and SniperState.
public class AuctionSniper implements AuctionEventListener { […]
  public void auctionClosed() {
snapshot = snapshot.closed();
    notifyChange();
  }
  public void currentPrice(int price, int increment, PriceSource priceSource) {
switch(priceSource) {
    case FromSniper:
      snapshot = snapshot.winning(price); 
      break;
case FromOtherBidder:
      int bid = price + increment;
      auction.bid(bid);
      snapshot = snapshot.bidding(price, bid); 
      break;
    }
notifyChange();
  }
  private void notifyChange() {
    sniperListener.sniperStateChanged(snapshot);
  }
}
We note, with smug satisfaction, that AuctionSniper no longer refers to
SniperState; it’s hidden in SniperSnapshot.
public class SniperSnapshot { […]
  public SniperSnapshot closed() {
    return new SniperSnapshot(itemId, lastPrice, lastBid, state.whenAuctionClosed());
  }
}
Chapter 15
Towards a Real User Interface
164


---
**Page 165**

public enum SniperState {
  JOINING {
    @Override public SniperState whenAuctionClosed() { return LOST; }
  },
  BIDDING {
    @Override public SniperState whenAuctionClosed() { return LOST; }
  },
  WINNING {
    @Override public SniperState whenAuctionClosed() { return WON; }
  },
  LOST,
  WON;
  public SniperState whenAuctionClosed() {
    throw new Defect("Auction is already closed");
  }
}
We would have preferred to use a ﬁeld to implement whenAuctionClosed(). It
turns out that the compiler cannot handle an enum referring to one of its values
which has not yet been deﬁned, so we have to put up with the syntax noise of
overridden methods.
Not Too Small to Test
At ﬁrst SniperState looked too simple to unit-test—after all, it’s exercised through
the AuctionSniper tests—but we thought we should keep ourselves honest.
Writing the test showed that our simple implementation didn’t handle re-closing an
auction, which shouldn’t happen, so we added an exception. It would be better to
write the code so that this case is impossible, but we can’t see how to do that
right now.
A Defect Exception
In most systems we build, we end up writing a runtime exception called something
like Defect (or perhaps StupidProgrammerMistakeException). We throw this
when the code reaches a condition that could only be caused by a programming
error, rather than a failure in the runtime environment.
165
Follow Through


---
**Page 166**

Trimming the Table Model
We remove the accessor setStatusText() that sets the state display string in
SnipersTableModel, as everything uses sniperStatusChanged() now. While we’re
at it, we move the description string constants for the Sniper state over from
MainWindow.
public class SnipersTableModel extends AbstractTableModel { […]
private final static String[] STATUS_TEXT = { 
    "Joining", "Bidding", "Winning", "Lost", "Won" 
  };
  public Object getValueAt(int rowIndex, int columnIndex) {
    switch (Column.at(columnIndex)) {
    case ITEM_IDENTIFIER:
      return snapshot.itemId;
    case LAST_PRICE:
      return snapshot.lastPrice;
    case LAST_BID:
      return snapshot.lastBid;
    case SNIPER_STATE:
      return textFor(snapshot.state);
    default:
      throw new IllegalArgumentException("No column at" + columnIndex);
    }
  }
  public void sniperStateChanged(SniperSnapshot newSnapshot) {
this.snapshot = newSnapshot;
    fireTableRowsUpdated(0, 0);
  }
  public static String textFor(SniperState state) {
    return STATUS_TEXT[state.ordinal()];
  }
}
The helper method, textFor(), helps with readability, and we also use it to get
hold of the display strings in tests since the constants are no longer accessible
from MainWindow.
Object-Oriented Column
We still have a couple of things to do before we ﬁnish this task. We start by
removing all the old test code that didn’t specify the price details, ﬁlling in the
expected values in the tests as required. The tests still run.
The next change is to replace the switch statement which is noisy, not very
object-oriented, and includes an unnecessary default: clause just to satisfy the
compiler. It’s served its purpose, which was to get us through the previous coding
stage. We add a method to Column that will extract the appropriate ﬁeld:
Chapter 15
Towards a Real User Interface
166


---
**Page 167**

public enum Column {
  ITEM_IDENTIFIER {
    @Override public Object valueIn(SniperSnapshot snapshot) {
      return snapshot.itemId;
    }
  },
  LAST_PRICE {
    @Override public Object valueIn(SniperSnapshot snapshot) {
      return snapshot.lastPrice;
    }
  },
  LAST_BID{
    @Override public Object valueIn(SniperSnapshot snapshot) {
      return snapshot.lastBid;
    }    
  },
  SNIPER_STATE {
    @Override public Object valueIn(SniperSnapshot snapshot) {
      return SnipersTableModel.textFor(snapshot.state);
    }    
  };
abstract public Object valueIn(SniperSnapshot snapshot);
[…]
}
and the code in SnipersTableModel becomes negligible:
public class SnipersTableModel extends AbstractTableModel { […]
  public Object getValueAt(int rowIndex, int columnIndex) {
    return Column.at(columnIndex).valueIn(snapshot);
  }
}
Of course, we write a unit test for Column. It may seem unnecessary now, but
it will protect us when we make changes and forget to keep the column mapping
up to date.
Shortening the Event Path
Finally, we see that we have some forwarding calls that we no longer need.
MainWindow just forwards the update and SniperStateDisplayer has collapsed
to almost nothing.
public class MainWindow extends JFrame { […]
  public void sniperStateChanged(SniperSnapshot snapshot) {
    snipers.sniperStateChanged(snapshot);
  }
}
167
Follow Through


---
**Page 168**

public class SniperStateDisplayer implements SniperListener { […]
  public void sniperStateChanged(final SniperSnapshot snapshot) {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() { mainWindow.sniperStateChanged(snapshot); } 
    });
  }
}
SniperStateDisplayer still serves a useful purpose, which is to push updates
onto the Swing event thread, but it no longer does any translation between do-
mains in the code, and the call to MainWindow is unnecessary. We decide to sim-
plify the connections by making SnipersTableModel implement SniperListener.
We change SniperStateDisplayer to be a Decorator and rename it to
SwingThreadSniperListener, and we rewire Main so that the Sniper connects
to the table model rather than the window.
 public class Main { […]
private final SnipersTableModel snipers = new SnipersTableModel();
  private MainWindow ui;
  public Main() throws Exception {
    SwingUtilities.invokeAndWait(new Runnable() { 
      public void run() { ui = new MainWindow(snipers); }
    });
  }
  private void joinAuction(XMPPConnection connection, String itemId) {
[…]
    Auction auction = new XMPPAuction(chat);
    chat.addMessageListener(
        new AuctionMessageTranslator(
            connection.getUser(),
            new AuctionSniper(itemId, auction, 
new SwingThreadSniperListener(snipers))));
    auction.join();
  }
}
The new structure looks like Figure 15.4.
Final Polish
A Test for Column Titles
To make the user interface presentable, we need to ﬁll in the column titles which,
as we saw in Figure 15.3, are still missing. This isn’t difﬁcult, since most of the
implementation is built into Swing’s TableModel. As always, we start with
the acceptance test. We add extra validation to AuctionSniperDriver that will
be called by the method in ApplicationRunner that starts up the Sniper. For good
measure, we throw in a check for the application’s displayed title.
Chapter 15
Towards a Real User Interface
168


---
**Page 169**

Figure 15.4
TableModel as a SniperListener
public class ApplicationRunner { […]
  public void startBiddingIn(final FakeAuctionServer auction) {
    itemId = auction.getItemId();
    Thread thread = new Thread("Test Application") {
[…]
    };
    thread.setDaemon(true);
    thread.start();
    driver = new AuctionSniperDriver(1000);
driver.hasTitle(MainWindow.APPLICATION_TITLE);
driver.hasColumnTitles();
    driver.showsSniperStatus(JOINING.itemId, JOINING.lastPrice, 
                             JOINING.lastBid, textFor(SniperState.JOINING));
  }
}
public class AuctionSniperDriver extends JFrameDriver { […]
  public void hasColumnTitles() {
    JTableHeaderDriver headers = new JTableHeaderDriver(this, JTableHeader.class);
    headers.hasHeaders(matching(withLabelText("Item"), withLabelText("Last Price"),
                                withLabelText("Last Bid"), withLabelText("State")));
  }
}
The test fails:
169
Final Polish


---
**Page 170**

java.lang.AssertionError: 
Tried to look for...
    exactly 1 JTableHeader ()
    in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    in all top level windows
and check that it is with headers with cells 
  <label  with text "Item">, <label with text "Last Price">, 
    <label with text "Last Bid">, <label with text "State">
but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTableHeader ()
   it is not with headers with cells 
     <label with text "Item">, <label with text "Last Price">, 
       <label with text "Last Bid">, <label with text "State">
because component 0 text was "A"
Implementing the TableModel
Swing allows a JTable to query its TableModel for the column headers, which is
the mechanism we’ve chosen to use. We already have Column to represent the
columns, so we extend this enum by adding a ﬁeld for the header text which we
reference in SnipersTableModel.
public enum Column {
  ITEM_IDENTIFIER("Item") { […]
  LAST_PRICE("Last Price") { […]
  LAST_BID("Last Bid") { […]
  SNIPER_STATE("State") { […]
public final String name;
  private Column(String name) {
this.name = name;
  }
}
public class SnipersTableModel extends AbstractTableModel implements SniperListener
{ […]
  @Override public String getColumnName(int column) {
    return Column.at(column).name;
  }
}
All we really need to check in the unit test for SniperTablesModel is the link
between a Column value and a column name, but it’s so simple to iterate that we
check them all:
public class SnipersTableModelTest { […]
  @Test public void
setsUpColumnHeadings() {
    for (Column column: Column.values()) {
      assertEquals(column.name, model.getColumnName(column.ordinal()));
    }
  }
}
Chapter 15
Towards a Real User Interface
170


---
**Page 171**

The acceptance test passes, and we can see the result in Figure 15.5.
Figure 15.5
Sniper with column headers
Enough for Now
There’s more we should do, such as set up borders and text alignment, to tune
the user interface. We might do that by associating CellRenderers with each
Column value, or perhaps by introducing a TableColumnModel. We’ll leave those
as an exercise for the reader, since they don’t add any more insight into our
development process.
In the meantime, we can cross off one more task from our to-do list:
Figure 15.6.
Figure 15.6
The Sniper shows price information
Observations
Single Responsibilities
SnipersTableModel has one responsibility: to represent the state of our bidding
in the user interface. It follows the heuristic we described in “No And’s, Or’s, or
171
Observations


---
**Page 172**

But’s” (page 51). We’ve seen too much user interface code that is brittle because
it has business logic mixed in. In this case, we could also have made the model
responsible for deciding whether to bid (“because that would be simpler”), but
that would make it harder to respond when either the user interface or the bidding
policy change. It would be harder to even ﬁnd the bidding policy, which is why
we isolated it in AuctionSniper.
Keyhole Surgery for Software
In this chapter we repeatedly used the practice of adding little slices of behavior
all the way through the system: replace a label with a table, get that working;
show the Sniper bidding, get that working; add the other values, get that
working. In all of these cases, we’ve ﬁgured out where we want to get to (always
allowing that we might discover a better alternative along the way), but we want
to avoid ripping the application apart to get there. Once we start a major rework,
we can’t stop until it’s ﬁnished, we can’t check in without branching, and merging
with rest of the team is harder. There’s a reason that surgeons prefer keyhole
surgery to opening up a patient—it’s less invasive and cheaper.
Programmer Hyper-Sensitivity
We have a well-developed sense of the value of our own time. We keep an eye
out for activities that don’t seem to be making the best of our (doubtless signiﬁ-
cant) talents, such as boiler-plate copying and adapting code: if we had the right
abstraction, we wouldn’t have to bother. Sometimes this just has to be done, es-
pecially when working with existing code—but there are fewer excuses when it’s
our own. Deciding when to change the design requires a good sense for trade-
offs, which implies both sensitivity and technical maturity: “I’m about to repeat
this code with minor variations, that seems dull and wasteful” as against “This
may not be the right time to rework this, I don’t understand it yet.”
We don’t have a simple, reproducible technique here; it requires skill and ex-
perience. Developers should have a habit of reﬂecting on their activity, on the
best way to invest their time for the rest of a coding session. This might mean
carrying on exactly as before, but at least they’ll have thought about it.
Celebrate Changing Your Mind
When the facts change, I change my mind. What do you do, sir?
—John Maynard Keynes
During this chapter, we renamed several features in the code. In many develop-
ment cultures, this is viewed as a sign of weakness, as an inability to do a proper
job. Instead, we think this is an essential part of our development process. Just
Chapter 15
Towards a Real User Interface
172


---
**Page 173**

as we learn more about what the structure should be by using the code we’ve
written, we learn more about the names we’ve chosen when we work with them.
We see how the type and method names ﬁt together and whether the concepts
are clear, which stimulates the discovery of new ideas. If the name of a feature
isn’t right, the only smart thing to do is change it and avoid countless hours of
confusion for all who will read the code later.
This Isn’t the Only Solution
Examples in books, such as this one, tend to read as if there was an inevitability
about the solution. That’s partly because we put effort into making the narrative
ﬂow, but it’s also because presenting one solution tends to drive others out of
the reader’s consciousness. There are other variations we could have considered,
some of which might even resurface as the example develops.
For example, we could argue that AuctionSniper doesn’t need to know whether
it’s won or lost the auction—just whether it should bid or not. At present, the
only part of the application that cares about winning is the user interface, and
it would certainly simplify the AuctionSniper and SniperSnapshot if we moved
that decision away from them. We won’t do that now, because we don’t yet
know if it’s the right choice, but we ﬁnd that kicking around design options
sometimes leads to much better solutions.
173
Observations


---
**Page 174**

This page intentionally left blank 


