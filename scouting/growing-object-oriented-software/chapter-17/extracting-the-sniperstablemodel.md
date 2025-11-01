Line1 # Extracting the SnipersTableModel (pp.197-201)
Line2 
Line3 ---
Line4 **Page 197**
Line5 
Line6 Implementing XMPPAuctionHouse is straightforward; we transfer there all the
Line7 code related to connection, including the generation of the Jabber ID from
Line8 the auction item ID. Main is now simpler, with just one import for all the XMPP
Line9 code, auctionsniper.xmpp.XMPPAuctionHouse. The new version looks like
Line10 Figure 17.2.
Line11 For consistency, we retroﬁt XMPPAuctionHouse to the integration test for
Line12 XMPPAuction, instead of creating XMPPAuctions directly as it does now, and rename
Line13 the test to XMPPAuctionHouseTest.
Line14 Our ﬁnal touch is to move the relevant constants from Main where we’d left
Line15 them: the message formats to XMPPAuction and the connection identiﬁer format
Line16 to XMPPAuctionHouse. This reassures us that we’re moving in the right direction,
Line17 since we’re narrowing the scope of where these constants are used.
Line18 Extracting the SnipersTableModel
Line19 Sniper Launcher
Line20 Finally, we’d like to do something about the direct reference to the
Line21 SnipersTableModel and the related SwingThreadSniperListener—and the awful
Line22 notToBeGCd. We think we can get there, but it’ll take a couple of steps.
Line23 The ﬁrst step is to turn the anonymous implementation of UserRequestListener
Line24 into a proper class so we can understand its dependencies. We decide to call the
Line25 new class SniperLauncher, since it will respond to a request to join an auction
Line26 by “launching” a Sniper. One nice effect is that we can make notToBeGCd local
Line27 to the new class.
Line28 public class SniperLauncher implements UserRequestListener {
Line29   private final ArrayList<Auction> notToBeGCd = new ArrayList<Auction>();
Line30   private final AuctionHouse auctionHouse;
Line31   private final SnipersTableModel snipers;
Line32   public SniperLauncher(AuctionHouse auctionHouse, SnipersTableModel snipers) {
Line33 // set the fields 
Line34   }
Line35   public void joinAuction(String itemId) {
Line36 snipers.addSniper(SniperSnapshot.joining(itemId));
Line37       Auction auction = auctionHouse.auctionFor(itemId);
Line38       notToBeGCd.add(auction);
Line39       AuctionSniper sniper = 
Line40         new AuctionSniper(itemId, auction, 
Line41                           new SwingThreadSniperListener(snipers));
Line42       auction.addAuctionEventListener(snipers);
Line43       auction.join();
Line44   }
Line45 }
Line46 With the SniperLauncher separated out, it becomes even clearer that the
Line47 Swing features don’t ﬁt here. There’s a clue in that our use of snipers, the
Line48 197
Line49 Extracting the SnipersTableModel
Line50 
Line51 
Line52 ---
Line53 
Line54 ---
Line55 **Page 198**
Line56 
Line57 SnipersTableModel, is clumsy: we tell it about the new Sniper by giving it an
Line58 initial SniperSnapshot, and we attach it to both the Sniper and the auction.
Line59 There’s also some hidden duplication in that we create an initial SniperSnaphot
Line60 both here and in the AuctionSniper constructor.
Line61 Stepping back, we ought to simplify this class so that all it does is establish a
Line62 new AuctionSniper. It can delegate the process of accepting the new Sniper into
Line63 the application to a new role which we’ll call a SniperCollector, implemented
Line64 in the SnipersTableModel.
Line65 public static class SniperLauncher implements UserRequestListener {
Line66   private final AuctionHouse auctionHouse;
Line67   private final SniperCollector collector;
Line68 […]
Line69   public void joinAuction(String itemId) {
Line70       Auction auction = auctionHouse.auctionFor(itemId);
Line71 AuctionSniper sniper = new AuctionSniper(itemId, auction);
Line72       auction.addAuctionEventListener(sniper);
Line73 collector.addSniper(sniper);
Line74       auction.join();
Line75   }
Line76 }
Line77 The one behavior that we want to conﬁrm is that we only join the auction after
Line78 everything else is set up. With the code now isolated, we can jMock a States to
Line79 check the ordering.
Line80 public class SniperLauncherTest {
Line81   private final States auctionState = context.states("auction state")
Line82 .startsAs("not joined");
Line83 […]
Line84   @Test public void
Line85 addsNewSniperToCollectorAndThenJoinsAuction() {
Line86     final String itemId = "item 123";
Line87     context.checking(new Expectations() {{
Line88       allowing(auctionHouse).auctionFor(itemId); will(returnValue(auction));
Line89       oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId))); 
Line90 when(auctionState.is("not joined"));
Line91       oneOf(sniperCollector).addSniper(with(sniperForItem(item))); 
Line92 when(auctionState.is("not joined"));
Line93       one(auction).join(); then(auctionState.is("joined"));
Line94     }});
Line95     launcher.joinAuction(itemId);
Line96   }
Line97 }
Line98 where sniperForItem() returns a Matcher that matches any AuctionSniper
Line99 associated with the given item identiﬁer.
Line100 We extend SnipersTableModel to fulﬁll its new role: now it accepts
Line101 AuctionSnipers rather than SniperSnapshots. To make this work, we have to
Line102 convert a Sniper’s listener from a dependency to a notiﬁcation, so that we can
Line103 Chapter 17
Line104 Teasing Apart Main
Line105 198
Line106 
Line107 
Line108 ---
Line109 
Line110 ---
Line111 **Page 199**
Line112 
Line113 add a listener after construction. We also change SnipersTableModel to use the
Line114 new API and disallow adding SniperSnapshots.
Line115 public class SnipersTableModel extends AbstractTableModel 
Line116     implements SniperListener, SniperCollector
Line117 {
Line118   private final ArrayList<AuctionSniper> notToBeGCd = […]
Line119   public void addSniper(AuctionSniper sniper) {
Line120     notToBeGCd.add(sniper);
Line121     addSniperSnapshot(sniper.getSnapshot());
Line122     sniper.addSniperListener(new SwingThreadSniperListener(this));
Line123   }
Line124   private void addSniperSnapshot(SniperSnapshot sniperSnapshot) {
Line125     snapshots.add(sniperSnapshot);
Line126     int row = snapshots.size() - 1;
Line127     fireTableRowsInserted(row, row);
Line128    }
Line129 }
Line130 One change that suggests that we’re heading in the right direction is that the
Line131 SwingThreadSniperListener is now packaged up in the Swing part of the code,
Line132 not in the generic SniperLauncher.
Line133 Sniper Portfolio
Line134 As a next step, we realize that we don’t yet have anything that represents all our
Line135 sniping activity and that we might call our portfolio. At the moment, the
Line136 SnipersTableModel is implicitly responsible for both maintaining a record of
Line137 our sniping and displaying that record. It also pulls a Swing implementation detail
Line138 into Main.
Line139 We want a clearer separation of concerns, so we extract a SniperPortfolio
Line140 to maintain our Snipers, which we make our new implementer of
Line141 SniperCollector. We push the creation of the SnipersTableModel into MainWindow,
Line142 and make it a PortfolioListener so the portfolio can tell it when we add or
Line143 remove a Sniper.
Line144 public interface PortfolioListener extends EventListener {
Line145   void sniperAdded(AuctionSniper sniper);
Line146 }
Line147 public class MainWindow extends JFrame {
Line148   private JTable makeSnipersTable(SniperPortfolio portfolio) { 
Line149 SnipersTableModel model = new SnipersTableModel();
Line150     portfolio.addPortfolioListener(model);
Line151     JTable snipersTable = new JTable(model); 
Line152     snipersTable.setName(SNIPERS_TABLE_NAME); 
Line153     return snipersTable; 
Line154   }
Line155 }
Line156 199
Line157 Extracting the SnipersTableModel
Line158 
Line159 
Line160 ---
Line161 
Line162 ---
Line163 **Page 200**
Line164 
Line165 This makes our top-level code very simple—it just binds together the user
Line166 interface and sniper creation through the portfolio:
Line167 public class Main {  […]
Line168   private final SniperPortfolio portfolio = new SniperPortfolio();
Line169   public Main() throws Exception {
Line170     SwingUtilities.invokeAndWait(new Runnable() {
Line171       public void run() {
Line172         ui = new MainWindow(portfolio);
Line173       }
Line174     });
Line175   }
Line176   private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
Line177     ui.addUserRequestListener(new SniperLauncher(auctionHouse, portfolio));
Line178   }
Line179 }
Line180 Even better, since SniperPortfolio maintains a list of all the Snipers, we can
Line181 ﬁnally get rid of notToBeGCd.
Line182 This refactoring takes us to the structure shown in Figure 17.3. We’ve separated
Line183 the code into three components: one for the core application, one for XMPP
Line184 communication, and one for Swing display. We’ll return to this in a moment.
Line185 Figure 17.3
Line186 With the SniperPortfolio
Line187 Chapter 17
Line188 Teasing Apart Main
Line189 200
Line190 
Line191 
Line192 ---
Line193 
Line194 ---
Line195 **Page 201**
Line196 
Line197 Now that we’ve cleaned up, we can cross the next item off our list: Figure 17.4.
Line198 Figure 17.4
Line199 Adding items through the user interface
Line200 Observations
Line201 Incremental Architecture
Line202 This restructuring of Main is a key moment in the development of the application.
Line203 As Figure 17.5 shows, we now have a structure that matches the “ports and
Line204 adapters” architecture we described in “Designing for Maintainability” (page 47).
Line205 There is core domain code (for example, AuctionSniper) which depends on
Line206 bridging code (for example, SnipersTableModel) that drives or responds to
Line207 technical code (for example, JTable). We’ve kept the domain code free of any
Line208 reference to the external infrastructure. The contents of our auctionsniper
Line209 package deﬁne a model of our auction sniping business, using a self-contained
Line210 language. The exception is Main, which is our entry point and binds the domain
Line211 model and infrastructure together.
Line212 What’s important for the purposes of this example, is that we arrived at this
Line213 design incrementally, by adding features and repeatedly following heuristics.
Line214 Although we rely on our experience to guide our decisions, we reached this
Line215 solution almost automatically by just following the code and taking care to keep
Line216 it clean.
Line217 201
Line218 Observations
Line219 
Line220 
Line221 ---
