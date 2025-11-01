Line1 # Testing for Multiple Items (pp.175-183)
Line2 
Line3 ---
Line4 **Page 175**
Line5 
Line6 Chapter 16
Line7 Sniping for Multiple Items
Line8 In which we bid for multiple items, splitting the per-connection code
Line9 from the per-auction code. We use the table model we just introduced
Line10 to display the additional bids. We extend the user interface to allow
Line11 users to add items dynamically. We’re pleased to ﬁnd that we don’t
Line12 have to change the tests, just their implementation. We tease out a
Line13 “user request listener” concept, which means we can test some features
Line14 more directly. We leave the code in a bit of a mess.
Line15 Testing for Multiple Items
Line16 A Tale of Two Items
Line17 The next task on our to-do list is to be able to snipe for multiple items at the
Line18 same time. We already have much of the machinery we’ll need in place, since our
Line19 user interface is based on a table, so some minor structural changes are all we
Line20 need to make this work. Looking ahead in the list, we could combine this change
Line21 with adding items through the user interface, but we don’t think we need to do
Line22 that yet. Just focusing on this one task means we can clarify the distinction be-
Line23 tween those features that belong to the Sniper’s connection to the auction house,
Line24 and those that belong to an individual auction. So far we’ve speciﬁed the item
Line25 on the command line, but we can extend that to pass multiple items in the
Line26 argument list.
Line27 As always, we start with a test. We want our new test to show that the appli-
Line28 cation can bid for and win two different items, so we start by looking at the tests
Line29 we already have. Our current test for a successful bid, in “First, a Failing Test”
Line30 (page 152), assumes that the application has only one auction—it’s implicit in
Line31 code such as:
Line32 application.hasShownSniperIsBidding(1000, 1098);
Line33 We prepare for multiple items by passing an auction into each of the
Line34 ApplicationRunner calls, so the code now looks like:
Line35 application.hasShownSniperIsBidding(auction, 1000, 1098);
Line36 Within the ApplicationRunner, we remove the itemId ﬁeld and instead extract
Line37 the item identiﬁer from the auction parameters.
Line38 175
Line39 
Line40 
Line41 ---
Line42 
Line43 ---
Line44 **Page 176**
Line45 
Line46 public void hasShownSniperIsBidding(FakeAuctionServer auction, 
Line47                                     int lastPrice, int lastBid) 
Line48 {
Line49   driver.showsSniperStatus(auction.getItemId(), lastPrice, lastBid, 
Line50                            textFor(SniperState.BIDDING));
Line51 }
Line52 The rest is similar, which means we can write a new test:
Line53 public class AuctionSniperEndToEndTest {
Line54   private final FakeAuctionServer auction = new FakeAuctionServer("item-54321");  
Line55 private final FakeAuctionServer auction2 = new FakeAuctionServer("item-65432");
Line56   @Test public void
Line57 sniperBidsForMultipleItems() throws Exception {
Line58     auction.startSellingItem();
Line59 auction2.startSellingItem();
Line60     application.startBiddingIn(auction, auction2);
Line61     auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line62 auction2.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line63     auction.reportPrice(1000, 98, "other bidder");
Line64     auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
Line65 auction2.reportPrice(500, 21, "other bidder");
Line66     auction2.hasReceivedBid(521, ApplicationRunner.SNIPER_XMPP_ID);
Line67     auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);    
Line68 auction2.reportPrice(521, 22, ApplicationRunner.SNIPER_XMPP_ID);
Line69     application.hasShownSniperIsWinning(auction, 1098);
Line70 application.hasShownSniperIsWinning(auction2, 521);
Line71     auction.announceClosed();
Line72 auction2.announceClosed();
Line73     application.showsSniperHasWonAuction(auction, 1098);
Line74 application.showsSniperHasWonAuction(auction2, 521);
Line75   }
Line76 }
Line77 Following the protocol convention, we also remember to add a new user,
Line78 auction-item-65432, to the chat server to represent the new auction.
Line79 Avoiding False Positives
Line80 We group the showsSniper methods together instead of pairing them with their
Line81 associated auction triggers. This is to catch a problem that we found in an earlier
Line82 version where each checking method would pick up the most recent change—the
Line83 one we’d just triggered in the previous call. Grouping the checking methods together
Line84 gives us conﬁdence that they’re both valid at the same time.
Line85 Chapter 16
Line86 Sniping for Multiple Items
Line87 176
Line88 
Line89 
Line90 ---
Line91 
Line92 ---
Line93 **Page 177**
Line94 
Line95 The ApplicationRunner
Line96 The one signiﬁcant change we have to make in the ApplicationRunner is to the
Line97 startBiddingIn() method. Now it needs to accept a variable number of auctions
Line98 passed through to the Sniper’s command line. The conversion is a bit messy since
Line99 we have to unpack the item identiﬁers and append them to the end of the other
Line100 command-line arguments—this is the best we can do with Java arrays:
Line101 public class ApplicationRunner { […]s
Line102   public void startBiddingIn(final FakeAuctionServer... auctions) {
Line103     Thread thread = new Thread("Test Application") {
Line104       @Override public void run() {
Line105         try {
Line106           Main.main(arguments(auctions));
Line107         } catch (Throwable e) {
Line108 […]
Line109 for (FakeAuctionServer auction : auctions) {
Line110       driver.showsSniperStatus(auction.getItemId(), 0, 0, textFor(JOINING));
Line111 }
Line112   }
Line113   protected static String[] arguments(FakeAuctionServer... auctions) {
Line114     String[] arguments = new String[auctions.length + 3];
Line115     arguments[0] = XMPP_HOSTNAME;
Line116     arguments[1] = SNIPER_ID;
Line117     arguments[2] = SNIPER_PASSWORD;
Line118     for (int i = 0; i < auctions.length; i++) {
Line119       arguments[i + 3] = auctions[i].getItemId();
Line120     }
Line121     return arguments;
Line122   }
Line123 }
Line124 We run the test and watch it fail.
Line125 java.lang.AssertionError: 
Line126 Expected: is not null
Line127      got: null
Line128   at auctionsniper.SingleMessageListener.receivesAMessage()
Line129 A Diversion, Fixing the Failure Message
Line130 We ﬁrst saw this cryptic failure message in Chapter 11. It wasn’t so bad then
Line131 because it could only occur in one place and there wasn’t much code to test
Line132 anyway. Now it’s more annoying because we have to ﬁnd this method:
Line133 public void receivesAMessage(Matcher<? super String> messageMatcher) 
Line134   throws InterruptedException 
Line135 {
Line136   final Message message = messages.poll(5, TimeUnit.SECONDS);
Line137   assertThat(message, is(notNullValue()));
Line138   assertThat(message.getBody(), messageMatcher);
Line139 }
Line140 177
Line141 Testing for Multiple Items
Line142 
Line143 
Line144 ---
Line145 
Line146 ---
Line147 **Page 178**
Line148 
Line149 and ﬁgure out what we’re missing. We’d like to combine these two assertions and
Line150 provide a more meaningful failure. We could write a custom matcher for the
Line151 message body but, given that the structure of Message is not going to change
Line152 soon, we can use a PropertyMatcher, like this:
Line153 public void receivesAMessage(Matcher<? super String> messageMatcher) 
Line154   throws InterruptedException 
Line155 {
Line156   final Message message = messages.poll(5, TimeUnit.SECONDS);
Line157   assertThat(message, hasProperty("body", messageMatcher));
Line158 }
Line159 which produces this more helpful failure report:
Line160 java.lang.AssertionError: 
Line161 Expected: hasProperty("body", "SOLVersion: 1.1; Command: JOIN;")
Line162      got: null
Line163 With slightly more effort, we could have extended a FeatureMatcher to extract
Line164 the message body with a nicer failure report. There’s not much difference, expect
Line165 that it would be statically type-checked. Now back to business.
Line166 Restructuring Main
Line167 The test is failing because the Sniper is not sending a Join message for the second
Line168 auction. We must change Main to interpret the additional arguments. Just to
Line169 remind you, the current structure of the code is:
Line170 public class Main {
Line171   public Main() throws Exception {
Line172     SwingUtilities.invokeAndWait(new Runnable() {
Line173       public void run() {
Line174         ui = new MainWindow(snipers);
Line175       }
Line176     });
Line177   }
Line178   public static void main(String... args) throws Exception {
Line179     Main main = new Main();
Line180     main.joinAuction(
Line181       connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]), 
Line182       args[ARG_ITEM_ID]);
Line183   }
Line184   private void joinAuction(XMPPConnection connection, String itemId) {
Line185     disconnectWhenUICloses(connection);
Line186     Chat chat = connection.getChatManager()
Line187                             .createChat(auctionId(itemId, connection), null);
Line188 […]
Line189   }    
Line190 }
Line191 Chapter 16
Line192 Sniping for Multiple Items
Line193 178
Line194 
Line195 
Line196 ---
Line197 
Line198 ---
Line199 **Page 179**
Line200 
Line201 To add multiple items, we need to distinguish between the code that establishes
Line202 a connection to the auction server and the code that joins an auction. We start
Line203 by holding on to connection so we can reuse it with multiple chats; the result is
Line204 not very object-oriented but we want to wait and see how the structure develops.
Line205 We also change notToBeGCd from a single value to a collection.
Line206 public class Main {
Line207   public static void main(String... args) throws Exception {
Line208     Main main = new Main();
Line209 XMPPConnection connection = 
Line210        connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
Line211 main.disconnectWhenUICloses(connection);
Line212     main.joinAuction(connection, args[ARG_ITEM_ID]);
Line213   }
Line214   private void joinAuction(XMPPConnection connection, String itemId) {
Line215     Chat chat = connection.getChatManager()
Line216                             .createChat(auctionId(itemId, connection), null);
Line217 notToBeGCd.add(chat);
Line218     Auction auction = new XMPPAuction(chat);
Line219     chat.addMessageListener(
Line220         new AuctionMessageTranslator(
Line221             connection.getUser(),
Line222             new AuctionSniper(itemId, auction, 
Line223                               new SwingThreadSniperListener(snipers))));
Line224     auction.join();
Line225   }
Line226 }
Line227 We loop through each of the items that we’ve been given:
Line228 public static void main(String... args) throws Exception {
Line229   Main main = new Main();
Line230   XMPPConnection connection = 
Line231     connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
Line232   main.disconnectWhenUICloses(connection);
Line233 for (int i = 3; i < args.length; i++) {
Line234     main.joinAuction(connection, args[i]);
Line235   }
Line236 }
Line237 This is ugly, but it does show us a separation between the code for the single
Line238 connection and multiple auctions. We have a hunch it’ll be cleaned up before long.
Line239 The end-to-end test now shows us that display cannot handle the additional
Line240 item we’ve just fed in. The table model is still hard-coded to support one row,
Line241 so one of the items will be ignored:
Line242 […] but...
Line243   it is not table with row with cells 
Line244     <label with text "item-65432">, <label with text "521">, 
Line245     <label with text "521">, <label with text "Winning">
Line246   because 
Line247 in row 0: component 0 text was "item-54321"
Line248 179
Line249 Testing for Multiple Items
Line250 
Line251 
Line252 ---
Line253 
Line254 ---
Line255 **Page 180**
Line256 
Line257 Incidentally, this result is a nice example of why we needed to be aware of timing
Line258 in end-to-end tests. This test might fail when looking for auction1 or auction2.
Line259 The asynchrony of the system means that we can’t tell which will arrive ﬁrst.
Line260 Extending the Table Model
Line261 The SnipersTableModel needs to know about multiple items, so we add a new
Line262 method to tell it when the Sniper joins an auction. We’ll call this method
Line263 from Main.joinAuction() so we show that context ﬁrst, writing an empty
Line264 implementation in SnipersTableModel to satisfy the compiler:
Line265 private void 
Line266 joinAuction(XMPPConnection connection, String itemId) throws Exception {
Line267 safelyAddItemToModel(itemId);
Line268 […]
Line269 }
Line270 private void safelyAddItemToModel(final String itemId) throws Exception {
Line271   SwingUtilities.invokeAndWait(new Runnable() {
Line272     public void run() {
Line273       snipers.addSniper(SniperSnapshot.joining(itemId));
Line274     }
Line275   });
Line276 }
Line277 We have to wrap the call in an invokeAndWait() because it’s changing the state
Line278 of the user interface from outside the Swing thread.
Line279 The implementation of SnipersTableModel itself is single-threaded, so we can
Line280 write direct unit tests for it—starting with this one for adding a Sniper:
Line281 @Test public void
Line282 notifiesListenersWhenAddingASniper() {
Line283     SniperSnapshot joining = SniperSnapshot.joining("item123");
Line284     context.checking(new Expectations() { {
Line285       one(listener).tableChanged(with(anInsertionAtRow(0)));
Line286     }});
Line287     assertEquals(0, model.getRowCount());
Line288     model.addSniper(joining);
Line289     assertEquals(1, model.getRowCount());
Line290     assertRowMatchesSnapshot(0, joining);
Line291 }
Line292 This is similar to the test for updating the Sniper state that we wrote in
Line293 “Showing a Bidding Sniper” (page 155), except that we’re calling the new method
Line294 and matching a different TableModelEvent. We also package up the comparison
Line295 of the table row values into a helper method assertRowMatchesSnapshot().
Line296 We make this test pass by replacing the single SniperSnapshot ﬁeld with a
Line297 collection and triggering the extra table event. These changes break the existing
Line298 Sniper update test, because there’s no longer a default Sniper, so we ﬁx it:
Line299 Chapter 16
Line300 Sniping for Multiple Items
Line301 180
Line302 
Line303 
Line304 ---
Line305 
Line306 ---
Line307 **Page 181**
Line308 
Line309 @Test public void 
Line310 setsSniperValuesInColumns() { 
Line311   SniperSnapshot joining = SniperSnapshot.joining("item id");
Line312   SniperSnapshot bidding = joining.bidding(555, 666);
Line313   context.checking(new Expectations() {{ 
Line314 allowing(listener).tableChanged(with(anyInsertionEvent()));
Line315     one(listener).tableChanged(with(aChangeInRow(0))); 
Line316   }}); 
Line317 model.addSniper(joining);
Line318   model.sniperStateChanged(bidding);
Line319   assertRowMatchesSnapshot(0, bidding);
Line320 }
Line321 We have to add a Sniper to the model. This triggers an insertion event which
Line322 isn’t relevant to this test—it’s just supporting infrastructure—so we add an
Line323 allowing() clause to let the insertion through. The clause uses a more forgiving
Line324 matcher that checks only the type of the event, not its scope. We also change
Line325 the matcher for the update event (the one we do care about) to be precise about
Line326 which row it’s checking.
Line327 Then we write more unit tests to drive out the rest of the functionality. For
Line328 these, we’re not interested in the TableModelEvents, so we ignore the listener
Line329 altogether.
Line330 @Test public void 
Line331 holdsSnipersInAdditionOrder() {
Line332   context.checking(new Expectations() { {
Line333     ignoring(listener);
Line334   }});
Line335   model.addSniper(SniperSnapshot.joining("item 0"));
Line336   model.addSniper(SniperSnapshot.joining("item 1"));
Line337   assertEquals("item 0", cellValue(0, Column.ITEM_IDENTIFIER));
Line338   assertEquals("item 1", cellValue(1, Column.ITEM_IDENTIFIER));
Line339 }
Line340 updatesCorrectRowForSniper() { […]
Line341 throwsDefectIfNoExistingSniperForAnUpdate() { […]
Line342 The implementation is obvious. The only point of interest is that we add an
Line343 isForSameItemAs() method to SniperSnapshot so that it can decide whether it’s
Line344 referring to the same item, instead of having the table model extract and compare
Line345 identiﬁers.1 It’s a clearer division of responsibilities, with the advantage that we
Line346 can change its implementation without changing the table model. We also decide
Line347 that not ﬁnding a relevant entry is a programming error.
Line348 1. This avoids the “feature envy” code smell [Fowler99].
Line349 181
Line350 Testing for Multiple Items
Line351 
Line352 
Line353 ---
Line354 
Line355 ---
Line356 **Page 182**
Line357 
Line358 public void sniperStateChanged(SniperSnapshot newSnapshot) {
Line359   int row = rowMatching(newSnapshot);
Line360   snapshots.set(row, newSnapshot);
Line361   fireTableRowsUpdated(row, row);
Line362 }
Line363 private int rowMatching(SniperSnapshot snapshot) {
Line364   for (int i = 0; i < snapshots.size(); i++) {
Line365     if (newSnapshot.isForSameItemAs(snapshots.get(i))) {
Line366       return i;
Line367     }
Line368   }
Line369   throw new Defect("Cannot find match for " + snapshot);
Line370 }
Line371 This makes the current end-to-end test pass—so we can cross off the task from
Line372 our to-do list, Figure 16.1.
Line373 Figure 16.1
Line374 The Sniper handles multiple items
Line375 The End of Off-by-One Errors?
Line376 Interacting with the table model requires indexing into a logical grid of cells. We
Line377 ﬁnd that this is a case where TDD is particularly helpful. Getting indexing right can
Line378 be tricky, except in the simplest cases, and writing tests ﬁrst clariﬁes the boundary
Line379 conditions and then checks that our implementation is correct. We’ve both lost too
Line380 much time in the past searching for indexing bugs buried deep in the code.
Line381 Chapter 16
Line382 Sniping for Multiple Items
Line383 182
Line384 
Line385 
Line386 ---
Line387 
Line388 ---
Line389 **Page 183**
Line390 
Line391 Adding Items through the User Interface
Line392 A Simpler Design
Line393 The buyers and user interface designers are still working through their ideas, but
Line394 they have managed to simplify their original design by moving the item entry
Line395 into a top bar instead of a pop-up dialog. The current version of the design looks
Line396 like Figure 16.2, so we need to add a text ﬁeld and a button to the display.
Line397 Figure 16.2
Line398 The Sniper with input ﬁelds in its bar
Line399 Making Progress While We Can
Line400 The design of user interfaces is outside the scope of this book. For a project of any
Line401 size, a user experience professional will consider all sorts of macro- and micro-
Line402 details to provide the user with a coherent experience, so one route that some
Line403 teams take is to try to lock down the interface design before coding. Our experience,
Line404 and that of others like Jeff Patton, is that we can make development progress whilst
Line405 the design is being sorted out. We can build to the team’s current understanding
Line406 of the features and keep our code (and attitude) ﬂexible to respond to design ideas
Line407 as they ﬁrm up—and perhaps even feed our experience back into the process.
Line408 Update the Test
Line409 Looking back at AuctionSniperEndToEndTest, it already expresses everything we
Line410 want the application to do: it describes how the Sniper connects to one or more
Line411 auctions and bids. The change is that we want to describe a different implemen-
Line412 tation of some of that behavior (establishing the connection through the user
Line413 interface rather than the command line) which happens in the ApplicationRunner.
Line414 We need a restructuring similar to the one we just made in Main, splitting the
Line415 connection from the individual auctions. We pull out a startSniper() method
Line416 that starts up and checks the Sniper, and then start bidding for each auction
Line417 in turn.
Line418 183
Line419 Adding Items through the User Interface
Line420 
Line421 
Line422 ---
