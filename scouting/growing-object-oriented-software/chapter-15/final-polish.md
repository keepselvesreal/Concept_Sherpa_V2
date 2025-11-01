Line1 # Final Polish (pp.168-171)
Line2 
Line3 ---
Line4 **Page 168**
Line5 
Line6 public class SniperStateDisplayer implements SniperListener { […]
Line7   public void sniperStateChanged(final SniperSnapshot snapshot) {
Line8     SwingUtilities.invokeLater(new Runnable() {
Line9       public void run() { mainWindow.sniperStateChanged(snapshot); } 
Line10     });
Line11   }
Line12 }
Line13 SniperStateDisplayer still serves a useful purpose, which is to push updates
Line14 onto the Swing event thread, but it no longer does any translation between do-
Line15 mains in the code, and the call to MainWindow is unnecessary. We decide to sim-
Line16 plify the connections by making SnipersTableModel implement SniperListener.
Line17 We change SniperStateDisplayer to be a Decorator and rename it to
Line18 SwingThreadSniperListener, and we rewire Main so that the Sniper connects
Line19 to the table model rather than the window.
Line20  public class Main { […]
Line21 private final SnipersTableModel snipers = new SnipersTableModel();
Line22   private MainWindow ui;
Line23   public Main() throws Exception {
Line24     SwingUtilities.invokeAndWait(new Runnable() { 
Line25       public void run() { ui = new MainWindow(snipers); }
Line26     });
Line27   }
Line28   private void joinAuction(XMPPConnection connection, String itemId) {
Line29 […]
Line30     Auction auction = new XMPPAuction(chat);
Line31     chat.addMessageListener(
Line32         new AuctionMessageTranslator(
Line33             connection.getUser(),
Line34             new AuctionSniper(itemId, auction, 
Line35 new SwingThreadSniperListener(snipers))));
Line36     auction.join();
Line37   }
Line38 }
Line39 The new structure looks like Figure 15.4.
Line40 Final Polish
Line41 A Test for Column Titles
Line42 To make the user interface presentable, we need to ﬁll in the column titles which,
Line43 as we saw in Figure 15.3, are still missing. This isn’t difﬁcult, since most of the
Line44 implementation is built into Swing’s TableModel. As always, we start with
Line45 the acceptance test. We add extra validation to AuctionSniperDriver that will
Line46 be called by the method in ApplicationRunner that starts up the Sniper. For good
Line47 measure, we throw in a check for the application’s displayed title.
Line48 Chapter 15
Line49 Towards a Real User Interface
Line50 168
Line51 
Line52 
Line53 ---
Line54 
Line55 ---
Line56 **Page 169**
Line57 
Line58 Figure 15.4
Line59 TableModel as a SniperListener
Line60 public class ApplicationRunner { […]
Line61   public void startBiddingIn(final FakeAuctionServer auction) {
Line62     itemId = auction.getItemId();
Line63     Thread thread = new Thread("Test Application") {
Line64 […]
Line65     };
Line66     thread.setDaemon(true);
Line67     thread.start();
Line68     driver = new AuctionSniperDriver(1000);
Line69 driver.hasTitle(MainWindow.APPLICATION_TITLE);
Line70 driver.hasColumnTitles();
Line71     driver.showsSniperStatus(JOINING.itemId, JOINING.lastPrice, 
Line72                              JOINING.lastBid, textFor(SniperState.JOINING));
Line73   }
Line74 }
Line75 public class AuctionSniperDriver extends JFrameDriver { […]
Line76   public void hasColumnTitles() {
Line77     JTableHeaderDriver headers = new JTableHeaderDriver(this, JTableHeader.class);
Line78     headers.hasHeaders(matching(withLabelText("Item"), withLabelText("Last Price"),
Line79                                 withLabelText("Last Bid"), withLabelText("State")));
Line80   }
Line81 }
Line82 The test fails:
Line83 169
Line84 Final Polish
Line85 
Line86 
Line87 ---
Line88 
Line89 ---
Line90 **Page 170**
Line91 
Line92 java.lang.AssertionError: 
Line93 Tried to look for...
Line94     exactly 1 JTableHeader ()
Line95     in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line96     in all top level windows
Line97 and check that it is with headers with cells 
Line98   <label  with text "Item">, <label with text "Last Price">, 
Line99     <label with text "Last Bid">, <label with text "State">
Line100 but...
Line101     all top level windows
Line102     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line103     contained 1 JTableHeader ()
Line104    it is not with headers with cells 
Line105      <label with text "Item">, <label with text "Last Price">, 
Line106        <label with text "Last Bid">, <label with text "State">
Line107 because component 0 text was "A"
Line108 Implementing the TableModel
Line109 Swing allows a JTable to query its TableModel for the column headers, which is
Line110 the mechanism we’ve chosen to use. We already have Column to represent the
Line111 columns, so we extend this enum by adding a ﬁeld for the header text which we
Line112 reference in SnipersTableModel.
Line113 public enum Column {
Line114   ITEM_IDENTIFIER("Item") { […]
Line115   LAST_PRICE("Last Price") { […]
Line116   LAST_BID("Last Bid") { […]
Line117   SNIPER_STATE("State") { […]
Line118 public final String name;
Line119   private Column(String name) {
Line120 this.name = name;
Line121   }
Line122 }
Line123 public class SnipersTableModel extends AbstractTableModel implements SniperListener
Line124 { […]
Line125   @Override public String getColumnName(int column) {
Line126     return Column.at(column).name;
Line127   }
Line128 }
Line129 All we really need to check in the unit test for SniperTablesModel is the link
Line130 between a Column value and a column name, but it’s so simple to iterate that we
Line131 check them all:
Line132 public class SnipersTableModelTest { […]
Line133   @Test public void
Line134 setsUpColumnHeadings() {
Line135     for (Column column: Column.values()) {
Line136       assertEquals(column.name, model.getColumnName(column.ordinal()));
Line137     }
Line138   }
Line139 }
Line140 Chapter 15
Line141 Towards a Real User Interface
Line142 170
Line143 
Line144 
Line145 ---
Line146 
Line147 ---
Line148 **Page 171**
Line149 
Line150 The acceptance test passes, and we can see the result in Figure 15.5.
Line151 Figure 15.5
Line152 Sniper with column headers
Line153 Enough for Now
Line154 There’s more we should do, such as set up borders and text alignment, to tune
Line155 the user interface. We might do that by associating CellRenderers with each
Line156 Column value, or perhaps by introducing a TableColumnModel. We’ll leave those
Line157 as an exercise for the reader, since they don’t add any more insight into our
Line158 development process.
Line159 In the meantime, we can cross off one more task from our to-do list:
Line160 Figure 15.6.
Line161 Figure 15.6
Line162 The Sniper shows price information
Line163 Observations
Line164 Single Responsibilities
Line165 SnipersTableModel has one responsibility: to represent the state of our bidding
Line166 in the user interface. It follows the heuristic we described in “No And’s, Or’s, or
Line167 171
Line168 Observations
Line169 
Line170 
Line171 ---
