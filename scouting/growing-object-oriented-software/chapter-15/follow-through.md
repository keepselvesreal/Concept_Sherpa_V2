Line1 # Follow Through (pp.164-168)
Line2 
Line3 ---
Line4 **Page 164**
Line5 
Line6 Follow Through
Line7 Converting Won and Lost
Line8 This works, but we still have two notiﬁcation methods in SniperListener left to
Line9 convert before we can say we’re done: sniperWon() and sniperLost(). Again,
Line10 we replace these with sniperStateChanged() and add two new values to
Line11 SniperState.
Line12 Plugging these changes in, we ﬁnd that the code simpliﬁes further. We drop
Line13 the isWinning ﬁeld from the Sniper and move some decision-making into
Line14 SniperSnapshot, which will know whether the Sniper is winning or losing,
Line15 and SniperState.
Line16 public class AuctionSniper implements AuctionEventListener { […]
Line17   public void auctionClosed() {
Line18 snapshot = snapshot.closed();
Line19     notifyChange();
Line20   }
Line21   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line22 switch(priceSource) {
Line23     case FromSniper:
Line24       snapshot = snapshot.winning(price); 
Line25       break;
Line26 case FromOtherBidder:
Line27       int bid = price + increment;
Line28       auction.bid(bid);
Line29       snapshot = snapshot.bidding(price, bid); 
Line30       break;
Line31     }
Line32 notifyChange();
Line33   }
Line34   private void notifyChange() {
Line35     sniperListener.sniperStateChanged(snapshot);
Line36   }
Line37 }
Line38 We note, with smug satisfaction, that AuctionSniper no longer refers to
Line39 SniperState; it’s hidden in SniperSnapshot.
Line40 public class SniperSnapshot { […]
Line41   public SniperSnapshot closed() {
Line42     return new SniperSnapshot(itemId, lastPrice, lastBid, state.whenAuctionClosed());
Line43   }
Line44 }
Line45 Chapter 15
Line46 Towards a Real User Interface
Line47 164
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 165**
Line54 
Line55 public enum SniperState {
Line56   JOINING {
Line57     @Override public SniperState whenAuctionClosed() { return LOST; }
Line58   },
Line59   BIDDING {
Line60     @Override public SniperState whenAuctionClosed() { return LOST; }
Line61   },
Line62   WINNING {
Line63     @Override public SniperState whenAuctionClosed() { return WON; }
Line64   },
Line65   LOST,
Line66   WON;
Line67   public SniperState whenAuctionClosed() {
Line68     throw new Defect("Auction is already closed");
Line69   }
Line70 }
Line71 We would have preferred to use a ﬁeld to implement whenAuctionClosed(). It
Line72 turns out that the compiler cannot handle an enum referring to one of its values
Line73 which has not yet been deﬁned, so we have to put up with the syntax noise of
Line74 overridden methods.
Line75 Not Too Small to Test
Line76 At ﬁrst SniperState looked too simple to unit-test—after all, it’s exercised through
Line77 the AuctionSniper tests—but we thought we should keep ourselves honest.
Line78 Writing the test showed that our simple implementation didn’t handle re-closing an
Line79 auction, which shouldn’t happen, so we added an exception. It would be better to
Line80 write the code so that this case is impossible, but we can’t see how to do that
Line81 right now.
Line82 A Defect Exception
Line83 In most systems we build, we end up writing a runtime exception called something
Line84 like Defect (or perhaps StupidProgrammerMistakeException). We throw this
Line85 when the code reaches a condition that could only be caused by a programming
Line86 error, rather than a failure in the runtime environment.
Line87 165
Line88 Follow Through
Line89 
Line90 
Line91 ---
Line92 
Line93 ---
Line94 **Page 166**
Line95 
Line96 Trimming the Table Model
Line97 We remove the accessor setStatusText() that sets the state display string in
Line98 SnipersTableModel, as everything uses sniperStatusChanged() now. While we’re
Line99 at it, we move the description string constants for the Sniper state over from
Line100 MainWindow.
Line101 public class SnipersTableModel extends AbstractTableModel { […]
Line102 private final static String[] STATUS_TEXT = { 
Line103     "Joining", "Bidding", "Winning", "Lost", "Won" 
Line104   };
Line105   public Object getValueAt(int rowIndex, int columnIndex) {
Line106     switch (Column.at(columnIndex)) {
Line107     case ITEM_IDENTIFIER:
Line108       return snapshot.itemId;
Line109     case LAST_PRICE:
Line110       return snapshot.lastPrice;
Line111     case LAST_BID:
Line112       return snapshot.lastBid;
Line113     case SNIPER_STATE:
Line114       return textFor(snapshot.state);
Line115     default:
Line116       throw new IllegalArgumentException("No column at" + columnIndex);
Line117     }
Line118   }
Line119   public void sniperStateChanged(SniperSnapshot newSnapshot) {
Line120 this.snapshot = newSnapshot;
Line121     fireTableRowsUpdated(0, 0);
Line122   }
Line123   public static String textFor(SniperState state) {
Line124     return STATUS_TEXT[state.ordinal()];
Line125   }
Line126 }
Line127 The helper method, textFor(), helps with readability, and we also use it to get
Line128 hold of the display strings in tests since the constants are no longer accessible
Line129 from MainWindow.
Line130 Object-Oriented Column
Line131 We still have a couple of things to do before we ﬁnish this task. We start by
Line132 removing all the old test code that didn’t specify the price details, ﬁlling in the
Line133 expected values in the tests as required. The tests still run.
Line134 The next change is to replace the switch statement which is noisy, not very
Line135 object-oriented, and includes an unnecessary default: clause just to satisfy the
Line136 compiler. It’s served its purpose, which was to get us through the previous coding
Line137 stage. We add a method to Column that will extract the appropriate ﬁeld:
Line138 Chapter 15
Line139 Towards a Real User Interface
Line140 166
Line141 
Line142 
Line143 ---
Line144 
Line145 ---
Line146 **Page 167**
Line147 
Line148 public enum Column {
Line149   ITEM_IDENTIFIER {
Line150     @Override public Object valueIn(SniperSnapshot snapshot) {
Line151       return snapshot.itemId;
Line152     }
Line153   },
Line154   LAST_PRICE {
Line155     @Override public Object valueIn(SniperSnapshot snapshot) {
Line156       return snapshot.lastPrice;
Line157     }
Line158   },
Line159   LAST_BID{
Line160     @Override public Object valueIn(SniperSnapshot snapshot) {
Line161       return snapshot.lastBid;
Line162     }    
Line163   },
Line164   SNIPER_STATE {
Line165     @Override public Object valueIn(SniperSnapshot snapshot) {
Line166       return SnipersTableModel.textFor(snapshot.state);
Line167     }    
Line168   };
Line169 abstract public Object valueIn(SniperSnapshot snapshot);
Line170 […]
Line171 }
Line172 and the code in SnipersTableModel becomes negligible:
Line173 public class SnipersTableModel extends AbstractTableModel { […]
Line174   public Object getValueAt(int rowIndex, int columnIndex) {
Line175     return Column.at(columnIndex).valueIn(snapshot);
Line176   }
Line177 }
Line178 Of course, we write a unit test for Column. It may seem unnecessary now, but
Line179 it will protect us when we make changes and forget to keep the column mapping
Line180 up to date.
Line181 Shortening the Event Path
Line182 Finally, we see that we have some forwarding calls that we no longer need.
Line183 MainWindow just forwards the update and SniperStateDisplayer has collapsed
Line184 to almost nothing.
Line185 public class MainWindow extends JFrame { […]
Line186   public void sniperStateChanged(SniperSnapshot snapshot) {
Line187     snipers.sniperStateChanged(snapshot);
Line188   }
Line189 }
Line190 167
Line191 Follow Through
Line192 
Line193 
Line194 ---
Line195 
Line196 ---
Line197 **Page 168**
Line198 
Line199 public class SniperStateDisplayer implements SniperListener { […]
Line200   public void sniperStateChanged(final SniperSnapshot snapshot) {
Line201     SwingUtilities.invokeLater(new Runnable() {
Line202       public void run() { mainWindow.sniperStateChanged(snapshot); } 
Line203     });
Line204   }
Line205 }
Line206 SniperStateDisplayer still serves a useful purpose, which is to push updates
Line207 onto the Swing event thread, but it no longer does any translation between do-
Line208 mains in the code, and the call to MainWindow is unnecessary. We decide to sim-
Line209 plify the connections by making SnipersTableModel implement SniperListener.
Line210 We change SniperStateDisplayer to be a Decorator and rename it to
Line211 SwingThreadSniperListener, and we rewire Main so that the Sniper connects
Line212 to the table model rather than the window.
Line213  public class Main { […]
Line214 private final SnipersTableModel snipers = new SnipersTableModel();
Line215   private MainWindow ui;
Line216   public Main() throws Exception {
Line217     SwingUtilities.invokeAndWait(new Runnable() { 
Line218       public void run() { ui = new MainWindow(snipers); }
Line219     });
Line220   }
Line221   private void joinAuction(XMPPConnection connection, String itemId) {
Line222 […]
Line223     Auction auction = new XMPPAuction(chat);
Line224     chat.addMessageListener(
Line225         new AuctionMessageTranslator(
Line226             connection.getUser(),
Line227             new AuctionSniper(itemId, auction, 
Line228 new SwingThreadSniperListener(snipers))));
Line229     auction.join();
Line230   }
Line231 }
Line232 The new structure looks like Figure 15.4.
Line233 Final Polish
Line234 A Test for Column Titles
Line235 To make the user interface presentable, we need to ﬁll in the column titles which,
Line236 as we saw in Figure 15.3, are still missing. This isn’t difﬁcult, since most of the
Line237 implementation is built into Swing’s TableModel. As always, we start with
Line238 the acceptance test. We add extra validation to AuctionSniperDriver that will
Line239 be called by the method in ApplicationRunner that starts up the Sniper. For good
Line240 measure, we throw in a check for the application’s displayed title.
Line241 Chapter 15
Line242 Towards a Real User Interface
Line243 168
Line244 
Line245 
Line246 ---
