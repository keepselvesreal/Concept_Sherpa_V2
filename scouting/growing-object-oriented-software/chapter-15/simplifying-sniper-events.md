Line1 # Simplifying Sniper Events (pp.159-164)
Line2 
Line3 ---
Line4 **Page 159**
Line5 
Line6 […] but...
Line7     all top level windows
Line8     contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line9     contained 1 JTable ()
Line10  it is not with row with cells 
Line11    <label with text "item-54321">, <label with text "1098">, 
Line12    <label with text "1098">, <label with text "Winning">
Line13 because 
Line14       in row 0: component 1 text was "1000"
Line15 and the proof is in Figure 15.3.
Line16 Figure 15.3
Line17 Sniper showing a row of detail
Line18 Simplifying Sniper Events
Line19 Listening to the Mood Music
Line20 We have one kind of Sniper event, Bidding, that we can handle all the way
Line21 through our application. Now we have to do the same thing to Winning, Lost,
Line22 and Won.
Line23 Frankly, that’s just dull. There’s too much repetitive work needed to make the
Line24 other cases work—setting them up in the Sniper and passing them through
Line25 the layers. Something’s wrong with the design. We toss this one around for a
Line26 while and eventually notice that we would have a subtle duplication in our code
Line27 if we just carried on. We would be splitting the transmission of the Sniper state
Line28 into two mechanisms: the choice of listener method and the state object. That’s
Line29 one mechanism too many.
Line30 We realize that we could collapse our events into one notiﬁcation that includes
Line31 the prices and the Sniper status. Of course we’re transmitting the same information
Line32 whichever mechanism we choose—but, looking at the chain of methods calls,
Line33 it would be simpler to have just one method and pass everything through in
Line34 SniperState.
Line35 Having made this choice, can we do it cleanly without ripping up the
Line36 metaphorical ﬂoorboards? We believe we can—but ﬁrst, one more clariﬁcation.
Line37 We want to start by creating a type to represent the Sniper’s status (winning,
Line38 losing, etc.) in the auction, but the terms “status” and “state” are too close to
Line39 distinguish easily. We kick around some vocabulary and eventually decide that
Line40 a better term for what we now call SniperState would be SniperSnapshot: a
Line41 description of the Sniper’s relationship with the auction at this moment in time.
Line42 This frees up the name SniperState to describe whether the Sniper is winning,
Line43 losing, and so on, which matches the terminology of the state machine we drew
Line44 159
Line45 Simplifying Sniper Events
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 160**
Line52 
Line53 in Figure 9.3 on page 78. Renaming the SniperState takes a moment, and we
Line54 change the value in Column from SNIPER_STATUS to SNIPER_STATE.
Line55 20/20 Hindsight
Line56 We’ve just gone through not one but two of those forehead-slapping moments that
Line57 make us wonder why we didn’t see it the ﬁrst time around. Surely, if we’d spent
Line58 more time on the design, we wouldn’t have to change it now? Sometimes that’s
Line59 true. Our experience, however, is that nothing shakes out a design like trying to
Line60 implement it, and between us we know just a handful of people who are smart
Line61 enough to get their designs always right. Our coping mechanism is to get into the
Line62 critical areas of the code early and to allow ourselves to change our collective mind
Line63 when we could do better. We rely on our skills, on taking small steps, and on the
Line64 tests to protect us when we make changes.
Line65 Repurposing sniperBidding()
Line66 Our ﬁrst step is to take the method that does most of what we want,
Line67 sniperBidding(), and rework it to ﬁt our new scheme. We create an enum that
Line68 takes the SniperState name we’ve just freed up and add it to SniperSnapshot;
Line69 we take the sniperState ﬁeld out of the method arguments; and, ﬁnally, we re-
Line70 name the method to sniperStateChanged() to match its intended new role. We
Line71 push the changes through to get the following code:
Line72 public enum SniperState {
Line73   JOINING,
Line74   BIDDING,
Line75   WINNING,
Line76   LOST,
Line77   WON;
Line78 }
Line79 public class AuctionSniper implements AuctionEventListener { […]
Line80   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line81     isWinning = priceSource == PriceSource.FromSniper;
Line82     if (isWinning) {
Line83       sniperListener.sniperWinning();
Line84     } else {
Line85       final int bid = price + increment;
Line86       auction.bid(bid);
Line87       sniperListener.sniperStateChanged(
Line88         new SniperSnapshot(itemId, price, bid, SniperState.BIDDING));
Line89     }
Line90   }
Line91 }
Line92 Chapter 15
Line93 Towards a Real User Interface
Line94 160
Line95 
Line96 
Line97 ---
Line98 
Line99 ---
Line100 **Page 161**
Line101 
Line102 In the table model, we use simple indexing to translate the enum into displayable
Line103 text.
Line104 public class SnipersTableModel extends AbstractTableModel { […]
Line105 private static String[] STATUS_TEXT = { MainWindow.STATUS_JOINING, 
Line106                                           MainWindow.STATUS_BIDDING };
Line107   public void sniperStateChanged(SniperSnapshot newSnapshot) {
Line108     this.snapshot = newSnapshot;
Line109     this.state = STATUS_TEXT[newSnapshot.state.ordinal()];
Line110     fireTableRowsUpdated(0, 0);
Line111   }
Line112 }
Line113 We make some minor changes to the test code, to get it through the compiler,
Line114 plus one more interesting adjustment. You might remember that we wrote an
Line115 expectation clause that ignored the details of the SniperState:
Line116 allowing(sniperListener).sniperBidding(with(any(SniperState.class)));
Line117 We can no longer rely on the choice of method to distinguish between different
Line118 events, so we have to dig into the new SniperSnapshot object to make sure we’re
Line119 matching the right one. We rewrite the expectation with a custom matcher that
Line120 checks just the state:
Line121 public class AuctionSniperTest {
Line122 […]
Line123   context.checking(new Expectations() {{
Line124     ignoring(auction);
Line125     allowing(sniperListener).sniperStateChanged(
Line126                                with(aSniperThatIs(BIDDING))); 
Line127                                                 then(sniperState.is("bidding"));
Line128     atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
Line129   }});
Line130 […]
Line131   private Matcher<SniperSnapshot> aSniperThatIs(final SniperState state) {
Line132     return new FeatureMatcher<SniperSnapshot, SniperState>(
Line133              equalTo(state), "sniper that is ", "was") 
Line134     {
Line135       @Override
Line136       protected SniperState featureValueOf(SniperSnapshot actual) {
Line137         return actual.state;
Line138       }
Line139     };
Line140   }
Line141 }
Line142 161
Line143 Simplifying Sniper Events
Line144 
Line145 
Line146 ---
Line147 
Line148 ---
Line149 **Page 162**
Line150 
Line151 Lightweight Extensions to jMock
Line152 We added a small helper method aSniperThatIs() to package up our specializa-
Line153 tion of FeatureMatcher behind a descriptive name. You’ll see that the method
Line154 name is intended to make the expectation code read well (or as well as we can
Line155 manage in Java).We did the same earlier in the chapter with aRowChangedEvent().
Line156 As we discussed in “Different Levels of Language” on page 51, we’re effectively
Line157 writing extensions to a language that’s embedded in Java. jMock was designed to
Line158 be extensible in this way, so that programmers can plug in features described in
Line159 terms of the code they’re testing.You could think of these little helper methods as
Line160 creating new nouns in jMock’s expectation language.
Line161 Filling In the Numbers
Line162 Now we’re in a position to feed the missing price to the user interface, which
Line163 means changing the listener call from sniperWinning() to sniperStateChanged()
Line164 so that the listener will receive the value in a SniperSnapshot. We start by
Line165 changing the test to expect the different listener call, and to trigger the event by
Line166 calling currentPrice() twice: once to force the Sniper to bid, and again to tell
Line167 the Sniper that it’s winning.
Line168 public class AuctionSniperTest { […]
Line169   @Test public void
Line170 reportsIsWinningWhenCurrentPriceComesFromSniper() {
Line171     context.checking(new Expectations() {{
Line172       ignoring(auction);
Line173       allowing(sniperListener).sniperStateChanged(
Line174                                  with(aSniperThatIs(BIDDING))); 
Line175                                                then(sniperState.is("bidding"));
Line176 atLeast(1).of(sniperListener).sniperStateChanged(
Line177                                new SniperSnapshot(ITEM_ID, 135, 135, WINNING)); 
Line178                                                when(sniperState.is("bidding"));
Line179     }});
Line180 sniper.currentPrice(123, 12, PriceSource.FromOtherBidder);
Line181     sniper.currentPrice(135, 45, PriceSource.FromSniper);
Line182   }
Line183 }
Line184 We change AuctionSniper to retain its most recent values by holding on to the
Line185 last snapshot. We also add some helper methods to SniperSnapshot, and ﬁnd
Line186 that our implementation starts to simplify.
Line187 Chapter 15
Line188 Towards a Real User Interface
Line189 162
Line190 
Line191 
Line192 ---
Line193 
Line194 ---
Line195 **Page 163**
Line196 
Line197 public class AuctionSniper implements AuctionEventListener { […]
Line198 private SniperSnapshot snapshot;
Line199   public AuctionSniper(String itemId, Auction auction, SniperListener sniperListener)
Line200   {
Line201     this.auction = auction;
Line202     this.sniperListener = sniperListener;
Line203 this.snapshot = SniperSnapshot.joining(itemId);
Line204   }
Line205   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line206     isWinning = priceSource == PriceSource.FromSniper;
Line207     if (isWinning) {
Line208 snapshot = snapshot.winning(price);
Line209     } else {
Line210       final int bid = price + increment;
Line211       auction.bid(bid);
Line212 snapshot = snapshot.bidding(price, bid);
Line213     }
Line214 sniperListener.sniperStateChanged(snapshot);
Line215   }
Line216 }
Line217 public class SniperSnapshot { […]
Line218   public SniperSnapshot bidding(int newLastPrice, int newLastBid) {
Line219     return new SniperSnapshot(itemId, newLastPrice, newLastBid, SniperState.BIDDING);
Line220   }
Line221   public SniperSnapshot winning(int newLastPrice) {
Line222     return new SniperSnapshot(itemId, newLastPrice, lastBid, SniperState.WINNING);
Line223   }
Line224   public static SniperSnapshot joining(String itemId) {
Line225     return new SniperSnapshot(itemId, 0, 0, SniperState.JOINING);
Line226   }
Line227 }
Line228 Nearly a State Machine
Line229 We’ve added some constructor methods to SniperSnapshot that provide a clean
Line230 mechanism for moving between snapshot states. It’s not a full state machine, in
Line231 that we don’t enforce only “legal” transitions, but it’s a hint, and it nicely packages
Line232 up the getting and setting of ﬁelds.
Line233 We remove sniperWinning() from SniperListener and its implementations,
Line234 and add a value for winning to SnipersTableModel.STATUS_TEXT.
Line235 Now, the end-to-end test passes.
Line236 163
Line237 Simplifying Sniper Events
Line238 
Line239 
Line240 ---
Line241 
Line242 ---
Line243 **Page 164**
Line244 
Line245 Follow Through
Line246 Converting Won and Lost
Line247 This works, but we still have two notiﬁcation methods in SniperListener left to
Line248 convert before we can say we’re done: sniperWon() and sniperLost(). Again,
Line249 we replace these with sniperStateChanged() and add two new values to
Line250 SniperState.
Line251 Plugging these changes in, we ﬁnd that the code simpliﬁes further. We drop
Line252 the isWinning ﬁeld from the Sniper and move some decision-making into
Line253 SniperSnapshot, which will know whether the Sniper is winning or losing,
Line254 and SniperState.
Line255 public class AuctionSniper implements AuctionEventListener { […]
Line256   public void auctionClosed() {
Line257 snapshot = snapshot.closed();
Line258     notifyChange();
Line259   }
Line260   public void currentPrice(int price, int increment, PriceSource priceSource) {
Line261 switch(priceSource) {
Line262     case FromSniper:
Line263       snapshot = snapshot.winning(price); 
Line264       break;
Line265 case FromOtherBidder:
Line266       int bid = price + increment;
Line267       auction.bid(bid);
Line268       snapshot = snapshot.bidding(price, bid); 
Line269       break;
Line270     }
Line271 notifyChange();
Line272   }
Line273   private void notifyChange() {
Line274     sniperListener.sniperStateChanged(snapshot);
Line275   }
Line276 }
Line277 We note, with smug satisfaction, that AuctionSniper no longer refers to
Line278 SniperState; it’s hidden in SniperSnapshot.
Line279 public class SniperSnapshot { […]
Line280   public SniperSnapshot closed() {
Line281     return new SniperSnapshot(itemId, lastPrice, lastBid, state.whenAuctionClosed());
Line282   }
Line283 }
Line284 Chapter 15
Line285 Towards a Real User Interface
Line286 164
Line287 
Line288 
Line289 ---
