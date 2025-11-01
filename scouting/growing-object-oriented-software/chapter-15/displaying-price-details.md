Line1 # Displaying Price Details (pp.152-159)
Line2 
Line3 ---
Line4 **Page 152**
Line5 
Line6 Still Ugly
Line7 As you can see, the SnipersTableModel really is a minimal implementation; the
Line8 only value that can vary is the statusText. It inherits most of its behavior from
Line9 the Swing AbstractTableModel, including the infrastructure for notifying the
Line10 JTable of data changes. The result is as ugly as our previous version, except that
Line11 now the JTable adds a default column title “A”, as in Figure 15.2. We’ll work
Line12 on the presentation in a moment.
Line13 Figure 15.2
Line14 Sniper with a single-cell table
Line15 Displaying Price Details
Line16 First, a Failing Test
Line17 Our next task is to display information about the Sniper’s position in the auction:
Line18 item identiﬁer, last auction price, last bid, status. These values come from updates
Line19 from the auction and the state held within the application. We need to pass them
Line20 through from their source to the table model and then render them in the display.
Line21 Of course, we start with the test. Given that this feature should be part of the
Line22 basic functionality of the application, not separate from what we already have,
Line23 we update our existing acceptance tests—starting with just one test so we don’t
Line24 break everything at once. Here’s the new version:
Line25 public class AuctionSniperEndToEndTest {
Line26   @Test public void
Line27 sniperWinsAnAuctionByBiddingHigher() throws Exception {
Line28     auction.startSellingItem();
Line29     application.startBiddingIn(auction);
Line30     auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line31     auction.reportPrice(1000, 98, "other bidder");
Line32     application.hasShownSniperIsBidding(1000, 1098); // last price, last bid
Line33     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line34     auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line35     application.hasShownSniperIsWinning(1098); // winning bid
Line36     auction.announceClosed();
Line37     application.showsSniperHasWonAuction(1098); // last price
Line38   }
Line39 }
Line40 Chapter 15
Line41 Towards a Real User Interface
Line42 152
Line43 
Line44 
Line45 ---
Line46 
Line47 ---
Line48 **Page 153**
Line49 
Line50 public class ApplicationRunner {
Line51 private String itemId;
Line52   public void startBiddingIn(final FakeAuctionServer auction) {
Line53 itemId = auction.getItemId();
Line54 […]
Line55   }
Line56 […]
Line57   public void hasShownSniperIsBidding(int lastPrice, int lastBid) {
Line58     driver.showsSniperStatus(itemId, lastPrice, lastBid, 
Line59                              MainWindow.STATUS_BIDDING);
Line60   }
Line61   public void hasShownSniperIsWinning(int winningBid) {
Line62     driver.showsSniperStatus(itemId, winningBid, winningBid, 
Line63                              MainWindow.STATUS_WINNING);
Line64   }
Line65   public void showsSniperHasWonAuction(int lastPrice) {
Line66     driver.showsSniperStatus(itemId, lastPrice, lastPrice, 
Line67                              MainWindow.STATUS_WON);
Line68   }
Line69 }
Line70 public class AuctionSniperDriver extends JFrameDriver {
Line71 […]
Line72   public void showsSniperStatus(String itemId, int lastPrice, int lastBid, 
Line73                                 String statusText)
Line74   {
Line75     JTableDriver table = new JTableDriver(this);
Line76     table.hasRow(
Line77       matching(withLabelText(itemId), withLabelText(valueOf(lastPrice)), 
Line78                withLabelText(valueOf(lastBid)), withLabelText(statusText)));
Line79   }
Line80 }
Line81 We need the item identiﬁer so the test can look for it in the row, so we make
Line82 the ApplicationRunner hold on it when connecting to an auction. We extend the
Line83 AuctionSniperDriver to look for a table row that shows the item identiﬁer, last
Line84 price, last bid, and sniper status.
Line85 The test fails because the row has no details, only the status text:
Line86 […] but...
Line87     all top level windows
Line88     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line89     contained 1 JTable ()
Line90  it is not with row with cells 
Line91    <label with text "item-54321">, <label with text "1000">, 
Line92    <label with text "1098">, <label with text "Bidding">
Line93 because 
Line94       in row 0: component 0 text was "Bidding"
Line95 153
Line96 Displaying Price Details
Line97 
Line98 
Line99 ---
Line100 
Line101 ---
Line102 **Page 154**
Line103 
Line104 Sending the State out of the Sniper
Line105 With an acceptance test to show us where we want to get to, we can ﬁll in the
Line106 steps along the way. As usual, we work “outside-in,” from the event that triggers
Line107 the behavior; in this case it’s a price update from Southabee’s On-Line.
Line108 Following along the sequence of method calls, we don’t have to change
Line109 AuctionMessageTranslator, so we start by looking at AuctionSniper and its
Line110 unit tests.
Line111 AuctionSniper notiﬁes changes in its state to neighbors that implement the
Line112 SniperListener interface which, as you might remember, has four callback
Line113 methods, one for each state of the Sniper. Now we also need to pass in the current
Line114 state of the Sniper when we notify a listener. We could add the same set of argu-
Line115 ments to each method, but that would be duplication; so, we introduce a value
Line116 type to carry the Sniper’s state. This is an example of “bundling up” that we
Line117 described in “Value Types” (page 59). Here’s a ﬁrst cut:
Line118 public class SniperState {
Line119   public final String itemId;
Line120   public final int lastPrice;
Line121   public final int lastBid;
Line122   public SniperState(String itemId, int lastPrice, int lastBid) {
Line123     this.itemId = itemId;
Line124     this.lastPrice = lastPrice;
Line125     this.lastBid = lastBid;
Line126   }
Line127 }
Line128 To save effort, we use the reﬂective builders from the Apache commons.lang
Line129 library to implement equals(), hashCode(), and toString() in the new class. We
Line130 could argue that we’re being premature with these features, but in practice we’ll
Line131 need them in a moment when we write our unit tests.
Line132 Public Final Fields
Line133 We’ve adopted a habit of using public ﬁnal ﬁelds in value types, at least while we’re
Line134 in the process of sorting out what the type should do. It makes it obvious that the
Line135 value is immutable and reduces the overhead of maintaining getters when the class
Line136 isn’t yet stable. Our ambition, which we might not achieve, is to replace all ﬁeld
Line137 access with meaningful action methods on the type. We’ll see how that pans out.
Line138 We don’t want to break all the tests at once, so we start with an easy one. In
Line139 this test there’s no history, all we have to do in the Sniper is construct a
Line140 SniperState from information available at the time and pass it to the listener.
Line141 Chapter 15
Line142 Towards a Real User Interface
Line143 154
Line144 
Line145 
Line146 ---
Line147 
Line148 ---
Line149 **Page 155**
Line150 
Line151 public class AuctionSniperTest { […]
Line152   @Test public void
Line153 bidsHigherAndReportsBiddingWhenNewPriceArrives() {
Line154     final int price = 1001;
Line155     final int increment = 25;
Line156     final int bid = price + increment;
Line157     context.checking(new Expectations() {{
Line158       one(auction).bid(bid);
Line159       atLeast(1).of(sniperListener).sniperBidding(
Line160 new SniperState(ITEM_ID, price, bid));
Line161     }});
Line162     sniper.currentPrice(price, increment, PriceSource.FromOtherBidder);
Line163   }
Line164 }
Line165 Then we make the test pass:
Line166 public class AuctionSniper implements AuctionEventListener { […]
Line167   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line168     isWinning = priceSource == PriceSource.FromSniper;
Line169     if (isWinning) {
Line170       sniperListener.sniperWinning();
Line171     } else {
Line172 int bid = price + increment;
Line173       auction.bid(bid);
Line174       sniperListener.sniperBidding(new SniperState(itemId, price, bid));
Line175     }
Line176   }
Line177 }
Line178 To get the code to compile, we also add the state argument to the
Line179 sniperBidding() method in 
Line180 SniperStateDisplayer, which implements
Line181 SniperListener, but don’t yet do anything with it.
Line182 The one signiﬁcant change is that the Sniper needs access to the item identiﬁer
Line183 so it can construct a SniperState. Given that the Sniper doesn’t need this value
Line184 for any other reason, we could have kept it in the SniperStateDisplayer and
Line185 added it in when an event passes through, but we think it’s reasonable that the
Line186 Sniper has access to this information. We decide to pass the identiﬁer into the
Line187 AuctionSniper constructor; it’s available at the time, and we don’t want to get
Line188 it from the Auction object which may have its own form of identiﬁer for an item.
Line189 We have one other test that refers to the sniperBidding() method, but only
Line190 as an “allowance.” We use a matcher that says that, since it’s only supporting
Line191 the interesting part of the test, we don’t care about the contents of the state object.
Line192 allowing(sniperListener).sniperBidding(with(any(SniperState.class)));
Line193 Showing a Bidding Sniper
Line194 We’ll take larger steps for the next task—presenting the state in the user
Line195 interface—as there are some new moving parts, including a new unit test. The
Line196 155
Line197 Displaying Price Details
Line198 
Line199 
Line200 ---
Line201 
Line202 ---
Line203 **Page 156**
Line204 
Line205 ﬁrst version of the code will be clumsier than we would like but, as you’ll soon
Line206 see, there’ll be interesting opportunities for cleaning up.
Line207 Our very ﬁrst step is to pass the new state parameter, which we’ve been ignor-
Line208 ing, through MainWindow to a new method in SnipersTableModel. While we’re at
Line209 it, we notice that just passing events through MainWindow isn’t adding much value,
Line210 so we make a note to deal with that later.
Line211 public class SniperStateDisplayer implements SniperListener { […]
Line212   public void sniperBidding(final SniperState state) {
Line213     SwingUtilities.invokeLater(new Runnable() {
Line214       public void run() { 
Line215 ui.sniperStatusChanged(state, MainWindow.STATUS_BIDDING);
Line216       } 
Line217     });
Line218   }
Line219 }
Line220 public class MainWindow extends JFrame { […]
Line221   public void sniperStatusChanged(SniperState sniperState, String statusText) {
Line222     snipers.sniperStatusChanged(sniperState, statusText);
Line223   }
Line224 }
Line225 To get the new values visible on screen, we need to ﬁx SnipersTableModel so
Line226 that it makes them available to its JTable, starting with a unit test. We take a
Line227 small design leap by introducing a Java enum to represent the columns in the
Line228 table—it’s more meaningful than just using integers.
Line229 public enum Column {
Line230   ITEM_IDENTIFIER,
Line231   LAST_PRICE,
Line232   LAST_BID,
Line233   SNIPER_STATUS;
Line234   public static Column at(int offset) { return values()[offset]; }
Line235 }
Line236 The table model needs to do two things when its state changes: hold onto the
Line237 new values and notify the table that they’ve changed. Here’s the test:
Line238 @RunWith(JMock.class)
Line239 public class SnipersTableModelTest {
Line240   private final Mockery context = new Mockery();
Line241   private TableModelListener listener = context.mock(TableModelListener.class);
Line242   private final SnipersTableModel model = new SnipersTableModel();
Line243   @Before public void attachModelListener() {  1
Line244     model.addTableModelListener(listener);
Line245   }
Line246   @Test public void
Line247 hasEnoughColumns() {  2
Line248     assertThat(model.getColumnCount(), equalTo(Column.values().length));
Line249   }
Line250 Chapter 15
Line251 Towards a Real User Interface
Line252 156
Line253 
Line254 
Line255 ---
Line256 
Line257 ---
Line258 **Page 157**
Line259 
Line260 @Test public void
Line261 setsSniperValuesInColumns() {
Line262     context.checking(new Expectations() {{
Line263       one(listener).tableChanged(with(aRowChangedEvent()));  3
Line264     }});
Line265     model.sniperStatusChanged(new SniperState("item id", 555, 666),  4
Line266                               MainWindow.STATUS_BIDDING);
Line267     assertColumnEquals(Column.ITEM_IDENTIFIER, "item id"); 5
Line268     assertColumnEquals(Column.LAST_PRICE, 555);
Line269     assertColumnEquals(Column.LAST_BID, 666);
Line270     assertColumnEquals(Column.SNIPER_STATUS, MainWindow.STATUS_BIDDING);
Line271   }
Line272   private void assertColumnEquals(Column column, Object expected) {
Line273     final int rowIndex = 0;
Line274     final int columnIndex = column.ordinal();
Line275     assertEquals(expected, model.getValueAt(rowIndex, columnIndex);
Line276   }
Line277   private Matcher<TableModelEvent> aRowChangedEvent() { 6
Line278     return samePropertyValuesAs(new TableModelEvent(model, 0));
Line279   }
Line280 }
Line281 1
Line282 We attach a mock implementation of TableModelListener to the model. This
Line283 is one of the few occasions where we break our rule “Only Mock Types That
Line284 You Own” (page 69) because the table model design ﬁts our design approach
Line285 so well.
Line286 2
Line287 We add a ﬁrst test to make sure we’re rendering the right number of columns.
Line288 Later, we’ll do something about the column titles.
Line289 3
Line290 This expectation checks that we notify any attached JTable that the contents
Line291 have changed.
Line292 4
Line293 This is the event that triggers the behavior we want to test.
Line294 5
Line295 We assert that the table model returns the right values in the right columns.
Line296 We hard-code the row number because we’re still assuming that there is
Line297 only one.
Line298 6
Line299 There’s no speciﬁc equals() method on TableModelEvent, so we use a
Line300 matcher that will reﬂectively compare the property values of any event it re-
Line301 ceives against an expected example. Again, we hard-code the row number.
Line302 After the usual red/green cycle, we end up with an implementation that looks
Line303 like this:
Line304 157
Line305 Displaying Price Details
Line306 
Line307 
Line308 ---
Line309 
Line310 ---
Line311 **Page 158**
Line312 
Line313 public class SnipersTableModel extends AbstractTableModel {
Line314   private final static SniperState STARTING_UP = new SniperState("", 0, 0);
Line315   private String statusText = MainWindow.STATUS_JOINING;
Line316   private SniperState sniperState = STARTING_UP; 1
Line317 […]
Line318   public int getColumnCount() { 2
Line319     return Column.values().length; 
Line320   }
Line321   public int getRowCount() {
Line322     return 1;
Line323   }
Line324   public Object getValueAt(int rowIndex, int columnIndex) { 3
Line325     switch (Column.at(columnIndex)) {
Line326     case ITEM_IDENTIFIER:
Line327       return sniperState.itemId;
Line328     case LAST_PRICE:
Line329       return sniperState.lastPrice;
Line330     case LAST_BID:
Line331       return sniperState.lastBid;
Line332     case SNIPER_STATUS:
Line333       return statusText;
Line334     default:
Line335       throw new IllegalArgumentException("No column at " + columnIndex);
Line336     }
Line337   }
Line338   public void sniperStatusChanged(SniperState newSniperState, 4
Line339                                   String newStatusText) 
Line340   { 
Line341     sniperState = newSniperState;
Line342     statusText = newStatusText;
Line343     fireTableRowsUpdated(0, 0);
Line344   }
Line345 }
Line346 1
Line347 We provide an initial SniperState with “empty” values so that the table
Line348 model will work before the Sniper has connected.
Line349 2
Line350 For the dimensions, we just return the numbers of values in Column or a
Line351 hard-coded row count.
Line352 3
Line353 This method unpacks the value to return depending on the column that is
Line354 speciﬁed. The advantage of using an enum is that the compiler will help with
Line355 missing branches in the switch statement (although it still insists on a default
Line356 case). We’re not keen on using switch, as it’s not object-oriented, so we’ll
Line357 keep an eye on this too.
Line358 4
Line359 The Sniper-speciﬁc method. It sets the ﬁelds and then triggers its clients to
Line360 update.
Line361 If we run our acceptance test again, we ﬁnd we’ve made some progress. It’s
Line362 gone past the Bidding check and now fails because the last price column, “B”,
Line363 has not yet been updated. Interestingly, the status column shows Winning correctly,
Line364 because that code is still working.
Line365 Chapter 15
Line366 Towards a Real User Interface
Line367 158
Line368 
Line369 
Line370 ---
Line371 
Line372 ---
Line373 **Page 159**
Line374 
Line375 […] but...
Line376     all top level windows
Line377     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line378     contained 1 JTable ()
Line379  it is not with row with cells 
Line380    <label with text "item-54321">, <label with text "1098">, 
Line381    <label with text "1098">, <label with text "Winning">
Line382 because 
Line383       in row 0: component 1 text was "1000"
Line384 and the proof is in Figure 15.3.
Line385 Figure 15.3
Line386 Sniper showing a row of detail
Line387 Simplifying Sniper Events
Line388 Listening to the Mood Music
Line389 We have one kind of Sniper event, Bidding, that we can handle all the way
Line390 through our application. Now we have to do the same thing to Winning, Lost,
Line391 and Won.
Line392 Frankly, that’s just dull. There’s too much repetitive work needed to make the
Line393 other cases work—setting them up in the Sniper and passing them through
Line394 the layers. Something’s wrong with the design. We toss this one around for a
Line395 while and eventually notice that we would have a subtle duplication in our code
Line396 if we just carried on. We would be splitting the transmission of the Sniper state
Line397 into two mechanisms: the choice of listener method and the state object. That’s
Line398 one mechanism too many.
Line399 We realize that we could collapse our events into one notiﬁcation that includes
Line400 the prices and the Sniper status. Of course we’re transmitting the same information
Line401 whichever mechanism we choose—but, looking at the chain of methods calls,
Line402 it would be simpler to have just one method and pass everything through in
Line403 SniperState.
Line404 Having made this choice, can we do it cleanly without ripping up the
Line405 metaphorical ﬂoorboards? We believe we can—but ﬁrst, one more clariﬁcation.
Line406 We want to start by creating a type to represent the Sniper’s status (winning,
Line407 losing, etc.) in the auction, but the terms “status” and “state” are too close to
Line408 distinguish easily. We kick around some vocabulary and eventually decide that
Line409 a better term for what we now call SniperState would be SniperSnapshot: a
Line410 description of the Sniper’s relationship with the auction at this moment in time.
Line411 This frees up the name SniperState to describe whether the Sniper is winning,
Line412 losing, and so on, which matches the terminology of the state machine we drew
Line413 159
Line414 Simplifying Sniper Events
Line415 
Line416 
Line417 ---
