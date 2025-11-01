Line1 # Stop When We've Had Enough (pp.205-212)
Line2 
Line3 ---
Line4 **Page 205**
Line5 
Line6 Chapter 18
Line7 Filling In the Details
Line8 In which we introduce a stop price so we don’t bid inﬁnitely, which
Line9 means we can now be losing an auction that hasn’t yet closed. We add
Line10 a new ﬁeld to the user interface and push it through to the Sniper. We
Line11 realize we should have created an Item type much earlier.
Line12 A More Useful Application
Line13 So far the functionality has been prioritized to attract potential customers by
Line14 giving them a sense of what the application will look like. We can show items
Line15 being added and some features of sniping. It’s not a very useful application be-
Line16 cause, amongst other things, there’s no upper limit for bidding on an item—it
Line17 could be very expensive to deploy.
Line18 This is a common pattern when using Agile Development techniques to work
Line19 on a new project. The team is ﬂexible enough to respond to how the needs of
Line20 the sponsors change over time: at the beginning, the emphasis might be on
Line21 proving the concept to attract enough support to continue; later, the emphasis
Line22 might be on implementing enough functionality to be ready to deploy; later still,
Line23 the emphasis might change to providing more options to support a wider range
Line24 of users.
Line25 This dynamic is very different from both a ﬁxed design approach, where the
Line26 structure of the development has to be approved before work can begin, and a
Line27 code-and-ﬁx approach, where the system might be initially successful but not
Line28 resilient enough to adapt to its changing role.
Line29 Stop When We’ve Had Enough
Line30 Our next most pressing task (especially after recent crises in the ﬁnancial markets)
Line31 is to be able to set an upper limit, the “stop price,” for our bid for an item.
Line32 Introducing a Losing State
Line33 With the introduction of a stop price, it’s possible for a Sniper to be losing before
Line34 the auction has closed. We could implement this by just marking the Sniper as
Line35 Lost when it hits its stop price, but the users want to know the ﬁnal price when
Line36 the auction has ﬁnished after they’ve dropped out, so we model this as an extra
Line37 state. Once a Sniper has been outbid at its stop price, it will never be able to win,
Line38 205
Line39 
Line40 
Line41 ---
Line42 
Line43 ---
Line44 **Page 206**
Line45 
Line46 so the only option left is to wait for the auction to close, accepting updates of
Line47 any new (higher) prices from other bidders.
Line48 We adapt the state machine we drew in Figure 9.3 to include the new
Line49 transitions. The result is Figure 18.1.
Line50 Figure 18.1
Line51 A bidder may now be losing
Line52 The First Failing Test
Line53 Of course we start with a failing test. We won’t go through all the cases here,
Line54 but this example will take us through the essentials. First, we write an end-to-
Line55 end test to describe the new feature. It shows a scenario where our Sniper bids
Line56 for an item but loses because it bumps into its stop price, and other bidders
Line57 continue until the auction closes.
Line58 @Test public void sniperLosesAnAuctionWhenThePriceIsTooHigh() throws Exception {
Line59   auction.startSellingItem();
Line60 application.startBiddingWithStopPrice(auction, 1100);
Line61   auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID); 
Line62   auction.reportPrice(1000, 98, "other bidder"); 
Line63   application.hasShownSniperIsBidding(auction, 1000, 1098);
Line64   auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line65   auction.reportPrice(1197, 10, "third party");
Line66 application.hasShownSniperIsLosing(auction, 1197, 1098);
Line67   auction.reportPrice(1207, 10, "fourth party");
Line68 application.hasShownSniperIsLosing(auction, 1207, 1098);
Line69   auction.announceClosed();
Line70   application.showsSniperHasLostAuction(auction, 1207, 1098); 
Line71 }
Line72 Chapter 18
Line73 Filling In the Details
Line74 206
Line75 
Line76 
Line77 ---
Line78 
Line79 ---
Line80 **Page 207**
Line81 
Line82 This test introduces two new methods into our test infrastructure, which we
Line83 need to ﬁll in to get through the compiler. First, startBiddingWithStopPrice()
Line84 passes the new stop price value through the ApplicationRunner to the
Line85 AuctionSniperDriver.
Line86 public class AuctionSniperDriver extends JFrameDriver {
Line87   public void startBiddingFor(String itemId, int stopPrice) {
Line88     textField(NEW_ITEM_ID_NAME).replaceAllText(itemId); 
Line89 textField(NEW_ITEM_STOP_PRICE_NAME).replaceAllText(String.valueOf(stopPrice));
Line90     bidButton().click(); 
Line91   }
Line92 […]
Line93 }
Line94 This implies that we need a new input ﬁeld in the user interface for the stop price,
Line95 so we create a constant to identify it in MainWindow (we’ll ﬁll in the component
Line96 itself soon). We also need to support our existing tests which do not have a stop
Line97 price, so we change them to use Integer.MAX_VALUE to represent no stop price
Line98 at all.
Line99 The other new method in ApplicationRunner is hasShownSniperIsLosing(),
Line100 which is the same as the other checking methods, except that it uses a new Losing
Line101 value in SniperState:
Line102 public enum SniperState {
Line103 LOSING {
Line104     @Override public SniperState whenAuctionClosed() { return LOST; }
Line105   }, […]
Line106 and, to complete the loop, we add a value to the display text in
Line107 SnipersTableModel:
Line108 private final static String[] STATUS_TEXT = {
Line109   "Joining", "Bidding", "Winning", "Losing", "Lost", "Won" 
Line110 };
Line111 The failure message says that we have no stop price ﬁeld:
Line112 […] but...
Line113   all top level windows
Line114   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line115 contained 0 JTextField (with name "stop price")
Line116 Now we have a failing end-to-end test that describes our intentions for the
Line117 feature, so we can implement it.
Line118 Typing In the Stop Price
Line119 To make any progress, we must add a component to the user interface that will
Line120 accept a stop price. Our current design, which we saw in Figure 16.2, has only
Line121 a ﬁeld for the item identiﬁer but we can easily adjust it to take a stop price in the
Line122 top bar.
Line123 207
Line124 Stop When We’ve Had Enough
Line125 
Line126 
Line127 ---
Line128 
Line129 ---
Line130 **Page 208**
Line131 
Line132 For our implementation, we will add a JFormattedTextField for the stop price
Line133 that is constrained to accept only integer values, and a couple of labels. The new
Line134 top bar looks like Figure 18.2.
Line135 Figure 18.2
Line136 The Sniper with a stop price ﬁeld in its bar
Line137 We get the test failure we expect, which is that the Sniper is not losing because
Line138 it continues to bid:
Line139 […] but...
Line140     all top level windows
Line141     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line142     contained 1 JTable ()
Line143    it is not table with row with cells 
Line144      <label with text "item-54321">, <label with text "1098">, 
Line145      <label with text "1197">, <label with text "Losing">
Line146     because 
Line147 in row 0: component 1 text was "1197"
Line148 Propagating the Stop Price
Line149 To make this feature work, we need to pass the stop price from the user interface
Line150 to the AuctionSniper, which can then use it to limit further bidding. The chain
Line151 starts when MainWindow notiﬁes its UserRequestListener using:
Line152 void joinAuction(String itemId);
Line153 The obvious thing to do is to add a stopPrice argument to this method and to
Line154 the rest of the chain of calls, until it reaches the AuctionSniper class. We want
Line155 to make a point here, so we’ll force a slightly different approach to propagating
Line156 the new value.
Line157 Another way to look at it is that the user interface constructs a description of
Line158 the user’s “policy” for the Sniper’s bidding on an item. So far this has only in-
Line159 cluded the item’s identiﬁer (“bid on this item”), but now we’re adding a stop
Line160 price (“bid up to this amount on this item”) so there’s more structure.
Line161 Chapter 18
Line162 Filling In the Details
Line163 208
Line164 
Line165 
Line166 ---
Line167 
Line168 ---
Line169 **Page 209**
Line170 
Line171 We want to make this structure explicit, so we create a new class, Item. We
Line172 start with a simple value that just carries the identiﬁer and stop price as public
Line173 immutable ﬁelds; we can move behavior into it later.
Line174 public class Item {
Line175   public final String identifier;
Line176   public final int stopPrice;
Line177   public Item(String identifier, int stopPrice) { 
Line178     this.identifier = identifier;
Line179     this.stopPrice = stopPrice; 
Line180   }
Line181 // also equals(), hashCode(), toString()
Line182 } 
Line183 Introducing the Item class is an example of budding off that we described in
Line184 “Value Types” (page 59). It’s a placeholder type that we use to identify a concept
Line185 and that gives us somewhere to attach relevant new features as the code grows.
Line186 We push Item into the code and see what breaks, starting with
Line187 UserRequestListener:
Line188 public interface UserRequestListener extends EventListener {
Line189   void joinAuction(Item item);
Line190 }
Line191 First we ﬁx MainWindowTest, the integration test we wrote for the Swing imple-
Line192 mentation in Chapter 16. The language is already beginning to shift. In the pre-
Line193 vious version of this test, the probe variable was called buttonProbe, which
Line194 describes the structure of the user interface. That doesn’t make sense any more,
Line195 so we’ve renamed it itemProbe, which describes a collaboration between
Line196 MainWindow and its neighbors.
Line197 @Test public void 
Line198 makesUserRequestWhenJoinButtonClicked() { 
Line199   final ValueMatcherProbe<Item> itemProbe = 
Line200     new ValueMatcherProbe<Item>(equalTo(new Item("an item-id", 789)), "item request");
Line201   mainWindow.addUserRequestListener( 
Line202       new UserRequestListener() { 
Line203         public void joinAuction(Item item) { 
Line204 itemProbe.setReceivedValue(item); 
Line205         } 
Line206       }); 
Line207   driver.startBiddingFor("an item-id", 789);
Line208   driver.check(itemProbe); 
Line209 }
Line210 We make this test pass by extracting the stop price value within MainWindow.
Line211 209
Line212 Stop When We’ve Had Enough
Line213 
Line214 
Line215 ---
Line216 
Line217 ---
Line218 **Page 210**
Line219 
Line220 joinAuctionButton.addActionListener(new ActionListener() { 
Line221   public void actionPerformed(ActionEvent e) { 
Line222     userRequests.announce().joinAuction(new Item(itemId(), stopPrice())); 
Line223   } 
Line224   private String itemId() {
Line225     return itemIdField.getText();
Line226   }
Line227   private int stopPrice() { 
Line228     return ((Number)stopPriceField.getValue()).intValue(); 
Line229   } 
Line230 });
Line231 This pushes Item into SniperLauncher which, in turn, pushes it through to its
Line232 dependent types such as AuctionHouse and AuctionSniper. We ﬁx the compilation
Line233 errors and make all the tests pass again—except for the outstanding end-to-end
Line234 test which we have yet to implement.
Line235 We’ve now made explicit another concept in the domain. We realize that an
Line236 item’s identiﬁer is only one part of how a user bids in an auction. Now the code
Line237 can tell us exactly where decisions are made about bidding choices, so we don’t
Line238 have to follow a chain of method calls to see which strings are relevant.
Line239 Restraining the AuctionSniper
Line240 The last step to ﬁnish the task is to make the AuctionSniper observe the stop
Line241 price we’ve just passed to it and stop bidding. In practice, we can ensure that
Line242 we’ve covered everything by writing unit tests for each of the new state transitions
Line243 drawn in Figure 18.1. Our ﬁrst test triggers the Sniper to start bidding and then
Line244 announces a bid outside its limit—the stop price is set to 1234. We’ve also
Line245 extracted a common expectation into a helper method.1
Line246 @Test public void
Line247 doesNotBidAndReportsLosingIfSubsequentPriceIsAboveStopPrice() {
Line248   allowingSniperBidding();
Line249   context.checking(new Expectations() {{
Line250     int bid = 123 + 45;
Line251     allowing(auction).bid(bid);
Line252     atLeast(1).of(sniperListener).sniperStateChanged(
Line253                     new SniperSnapshot(ITEM_ID, 2345, bid, LOSING)); 
Line254                                         when(sniperState.is("bidding"));
Line255   }});
Line256   sniper.currentPrice(123, 45, PriceSource.FromOtherBidder);
Line257   sniper.currentPrice(2345, 25, PriceSource.FromOtherBidder);
Line258 }
Line259 private void allowingSniperBidding() {
Line260   context.checking(new Expectations() {{ 
Line261     allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING))); 
Line262                                               then(sniperState.is("bidding"));
Line263   }});
Line264 } 
Line265 1. jMock allows checking() to be called multiple times within a test.
Line266 Chapter 18
Line267 Filling In the Details
Line268 210
Line269 
Line270 
Line271 ---
Line272 
Line273 ---
Line274 **Page 211**
Line275 
Line276 Distinguishing between Test Setup and Assertions
Line277 Once again we’re using the allowing clause to distinguish between the test setup
Line278 (getting the AuctionSniper into the right state) and the signiﬁcant test assertion
Line279 (that the AuctionSniper is now losing). We’re very picky about this kind of
Line280 expressiveness because we’ve found it’s the only way for the tests to remain
Line281 meaningful, and therefore useful, over time.We return to this at length in Chapter 21
Line282 and Chapter 24.
Line283 The other tests are similar:
Line284 doesNotBidAndReportsLosingIfFirstPriceIsAboveStopPrice()
Line285 reportsLostIfAuctionClosesWhenLosing()
Line286 continuesToBeLosingOnceStopPriceHasBeenReached()
Line287 doesNotBidAndReportsLosingIfPriceAfterWinningIsAboveStopPrice()
Line288 We change AuctionSniper, with supporting features in SniperSnapshot and
Line289 Item, to make the test pass:
Line290 public class AuctionSniper { […]
Line291   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line292     switch(priceSource) {
Line293     case FromSniper:
Line294       snapshot = snapshot.winning(price); 
Line295       break;
Line296     case FromOtherBidder:
Line297       int bid = price + increment;
Line298       if (item.allowsBid(bid)) {
Line299         auction.bid(bid);
Line300         snapshot = snapshot.bidding(price, bid);
Line301 } else {
Line302         snapshot = snapshot.losing(price);
Line303       }
Line304       break;
Line305     }
Line306     notifyChange();
Line307   } […]
Line308 public class SniperSnapshot { […]
Line309   public SniperSnapshot losing(int newLastPrice) {
Line310     return new SniperSnapshot(itemId, newLastPrice, lastBid, LOSING);
Line311   } […]
Line312 public class Item { […]
Line313   public boolean allowsBid(int bid) {
Line314     return bid <= stopPrice;
Line315   } […]
Line316 The end-to-end tests pass and we can cross the feature off our list, Figure 18.3.
Line317 211
Line318 Stop When We’ve Had Enough
Line319 
Line320 
Line321 ---
Line322 
Line323 ---
Line324 **Page 212**
Line325 
Line326 Figure 18.3
Line327 The Sniper stops bidding at the stop price
Line328 Observations
Line329 User Interfaces, Incrementally
Line330 It looks like we’re making signiﬁcant changes again to the user interface at a late
Line331 stage in our development. Shouldn’t we have seen this coming? This is an active
Line332 topic for discussion in the Agile User Experience community and, as always, the
Line333 answer is “it depends, but you have more ﬂexibility than you might think.”
Line334 In truth, for a simple application like this it would make sense to work out the
Line335 user interface in more detail at the start, to make sure it’s usable and coherent.
Line336 That said, we also wanted to make a point that we can respond to changing
Line337 needs, especially if we structure our tests and code so that they’re ﬂexible, not a
Line338 dead weight. We all know that requirements will change, especially once we put
Line339 our application into production, so we should be able to respond.
Line340 Other Modeling Techniques Still Work
Line341 Some presentations of TDD appear to suggest that it supersedes all previous
Line342 software design techniques. We think TDD works best when it’s based on skill
Line343 and judgment acquired from as wide an experience as possible—which includes
Line344 taking advantage of older techniques and formats (we hope we’re not being too
Line345 controversial here).
Line346 State transition diagrams are one example of taking another view. We regularly
Line347 come across teams that have never quite ﬁgured out what the valid states and
Line348 transitions are for key concepts in their domain, and applying this simple
Line349 Chapter 18
Line350 Filling In the Details
Line351 212
Line352 
Line353 
Line354 ---
