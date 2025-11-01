Line1 # A More Realistic Implementation (pp.149-152)
Line2 
Line3 ---
Line4 **Page 149**
Line5 
Line6 Chapter 15
Line7 Towards a Real User Interface
Line8 In which we grow the user interface from a label to a table. We achieve
Line9 this by adding a feature at a time, instead of taking the risk of replacing
Line10 the whole thing in one go. We discover that some of the choices we
Line11 made are no longer valid, so we dare to change existing code. We
Line12 continue to refactor and sense that a more interesting structure is
Line13 starting to appear.
Line14 A More Realistic Implementation
Line15 What Do We Have to Do Next?
Line16 So far, we’ve been making do with a simple label in the user interface. That’s
Line17 been effective for helping us clarify the structure of the application and prove
Line18 that our ideas work, but the next tasks coming up will need more, and the client
Line19 wants to see something that looks closer to Figure 9.1. We will need to show
Line20 more price details from the auction and handle multiple items.
Line21 The simplest option would be just to add more text into the label, but we think
Line22 this is the right time to introduce more structure into the user interface. We de-
Line23 ferred putting effort into this part of the application, and we think we should
Line24 catch up now to be ready for the more complex requirements we’re about to
Line25 implement. We decide to make the obvious choice, given our use of Swing, and
Line26 replace the label with a table component. This decision gives us a clear direction
Line27 for where our design should go next.
Line28 The Swing pattern for using a JTable is to associate it with a TableModel. The
Line29 table component queries the model for values to present, and the model notiﬁes
Line30 the table when those values change. In our application, the relationships will
Line31 look like Figure 15.1.  We call the new class SnipersTableModel because we want
Line32 it to support multiple Snipers. It will accept updates from the Snipers and provide
Line33 a representation of those values to its JTable.
Line34 The question is how to get there from here.
Line35 149
Line36 
Line37 
Line38 ---
Line39 
Line40 ---
Line41 **Page 150**
Line42 
Line43 Figure 15.1
Line44 Swing table model for the AuctionSniper
Line45 Replacing JLabel
Line46 We want to get the pieces into place with a minimum of change, without tearing
Line47 the whole application apart. The smallest step we can think of is to replace the
Line48 existing implementation (a JLabel) with a single-cell JTable, from which we can
Line49 then grow the additional functionality. We start, of course, with the test, changing
Line50 our harness to look for a cell in a table, rather than a label.
Line51 public class AuctionSniperDriver extends JFrameDriver { […]
Line52   public void showsSniperStatus(String statusText) {
Line53 new JTableDriver(this).hasCell(withLabelText(equalTo(statusText)));
Line54   }
Line55 }
Line56 This generates a failure message because we don’t yet have a table.
Line57 […] but...
Line58     all top level windows
Line59     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line60 contained 0 JTable ()
Line61 Chapter 15
Line62 Towards a Real User Interface
Line63 150
Line64 
Line65 
Line66 ---
Line67 
Line68 ---
Line69 **Page 151**
Line70 
Line71 We ﬁx this test by retroﬁtting a minimal JTable implementation. From now
Line72 on, we want to speed up our narrative, so we’ll just show the end result. If we
Line73 were feeling cautious we would ﬁrst add an empty table, to ﬁx the immediate
Line74 failure, and then add its contents. It turns out that we don’t have to change any
Line75 existing classes outside MainWindow because it encapsulates the act of updating
Line76 the status. Here’s the new code:
Line77 public class MainWindow extends JFrame { […]
Line78 private final SnipersTableModel snipers = new SnipersTableModel();
Line79   public MainWindow() {
Line80     super(APPLICATION_TITLE);
Line81     setName(MainWindow.MAIN_WINDOW_NAME);
Line82 fillContentPane(makeSnipersTable());
Line83     pack();
Line84     setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
Line85     setVisible(true);
Line86   }
Line87   private void fillContentPane(JTable snipersTable) {
Line88     final Container contentPane = getContentPane();
Line89     contentPane.setLayout(new BorderLayout());
Line90     contentPane.add(new JScrollPane(snipersTable), BorderLayout.CENTER);
Line91   }
Line92   private JTable makeSnipersTable() {
Line93     final JTable snipersTable = new JTable(snipers);
Line94     snipersTable.setName(SNIPERS_TABLE_NAME);
Line95     return snipersTable;
Line96   }
Line97   public void showStatusText(String statusText) {
Line98 snipers.setStatusText(statusText);
Line99   }
Line100 }
Line101 public class SnipersTableModel extends AbstractTableModel {
Line102   private String statusText = STATUS_JOINING;
Line103   public int getColumnCount() { return 1; }
Line104   public int getRowCount() { return 1; }
Line105   public Object getValueAt(int rowIndex, int columnIndex) { return statusText; }
Line106   public void setStatusText(String newStatusText) {
Line107     statusText = newStatusText;
Line108     fireTableRowsUpdated(0, 0);
Line109   }
Line110 }
Line111 151
Line112 A More Realistic Implementation
Line113 
Line114 
Line115 ---
Line116 
Line117 ---
Line118 **Page 152**
Line119 
Line120 Still Ugly
Line121 As you can see, the SnipersTableModel really is a minimal implementation; the
Line122 only value that can vary is the statusText. It inherits most of its behavior from
Line123 the Swing AbstractTableModel, including the infrastructure for notifying the
Line124 JTable of data changes. The result is as ugly as our previous version, except that
Line125 now the JTable adds a default column title “A”, as in Figure 15.2. We’ll work
Line126 on the presentation in a moment.
Line127 Figure 15.2
Line128 Sniper with a single-cell table
Line129 Displaying Price Details
Line130 First, a Failing Test
Line131 Our next task is to display information about the Sniper’s position in the auction:
Line132 item identiﬁer, last auction price, last bid, status. These values come from updates
Line133 from the auction and the state held within the application. We need to pass them
Line134 through from their source to the table model and then render them in the display.
Line135 Of course, we start with the test. Given that this feature should be part of the
Line136 basic functionality of the application, not separate from what we already have,
Line137 we update our existing acceptance tests—starting with just one test so we don’t
Line138 break everything at once. Here’s the new version:
Line139 public class AuctionSniperEndToEndTest {
Line140   @Test public void
Line141 sniperWinsAnAuctionByBiddingHigher() throws Exception {
Line142     auction.startSellingItem();
Line143     application.startBiddingIn(auction);
Line144     auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line145     auction.reportPrice(1000, 98, "other bidder");
Line146     application.hasShownSniperIsBidding(1000, 1098); // last price, last bid
Line147     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line148     auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
Line149     application.hasShownSniperIsWinning(1098); // winning bid
Line150     auction.announceClosed();
Line151     application.showsSniperHasWonAuction(1098); // last price
Line152   }
Line153 }
Line154 Chapter 15
Line155 Towards a Real User Interface
Line156 152
Line157 
Line158 
Line159 ---
