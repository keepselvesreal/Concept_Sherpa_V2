Line1 # Displaying the Failure (pp.218-219)
Line2 
Line3 ---
Line4 **Page 218**
Line5 
Line6 such as the event type or current price. We write a couple of tests to conﬁrm that
Line7 we can catch these, for example:
Line8 @Test public void
Line9 notifiesAuctionFailedWhenEventTypeMissing() {
Line10   context.checking(new Expectations() {{  
Line11     exactly(1).of(listener).auctionFailed(); 
Line12   }});
Line13   Message message = new Message();
Line14   message.setBody("SOLVersion: 1.1; CurrentPrice: 234; Increment: 5; Bidder: "
Line15                   + SNIPER_ID + ";");
Line16   translator.processMessage(UNUSED_CHAT, message);
Line17 }
Line18 Our ﬁx is to throw an exception whenever we try to get a value that has not
Line19 been set, and we deﬁne MissingValueException for this purpose.
Line20 public static class AuctionEvent { […]
Line21   private String get(String name) throws MissingValueException {
Line22     String value = values.get(name);
Line23 if (null == value) {
Line24       throw new MissingValueException(name);
Line25     }
Line26     return value;
Line27   }
Line28 }
Line29 Displaying the Failure
Line30 We added an auctionFailed() method to AuctionEventListener while unit-
Line31 testing AuctionMessageTranslator. This triggers a compiler warning in
Line32 AuctionSniper, so we added an empty implementation to keep going. Now
Line33 it’s time to make it work, which turns out to be easy. We write some tests in
Line34 AuctionSniperTest for the new state transitions, for example:
Line35 @Test public void
Line36 reportsFailedIfAuctionFailsWhenBidding() {
Line37   ignoringAuction();
Line38   allowingSniperBidding();
Line39   expectSniperToFailWhenItIs("bidding");
Line40   sniper.currentPrice(123, 45, PriceSource.FromOtherBidder); 
Line41   sniper.auctionFailed(); 
Line42 }
Line43 private void expectSniperToFailWhenItIs(final String state) {
Line44   context.checking(new Expectations() {{
Line45     atLeast(1).of(sniperListener).sniperStateChanged(
Line46         new SniperSnapshot(ITEM_ID, 00, 0, SniperState.FAILED)); 
Line47                                     when(sniperState.is(state));
Line48   }});
Line49 }
Line50 Chapter 19
Line51 Handling Failure
Line52 218
Line53 
Line54 
Line55 ---
Line56 
Line57 ---
Line58 **Page 219**
Line59 
Line60 We’ve added a couple more helper methods: ignoringAuction() says that we
Line61 don’t care what happens to auction, allowing events to pass through so we can
Line62 get to the failure; and, expectSniperToFailWhenItIs() describes what a failure
Line63 should look like, including the previous state of the Sniper.
Line64 All we have to do is add a failed() transition to SniperSnapshot and use it
Line65 in the new method.
Line66 public class AuctionSniper implements AuctionEventListener {
Line67   public void auctionFailed() {
Line68     snapshot = snapshot.failed();
Line69     listeners.announce().sniperStateChanged(snapshot);
Line70   } […]
Line71 public class SniperSnapshot {
Line72   public SniperSnapshot failed() {
Line73     return new SniperSnapshot(itemId, 0, 0, SniperState.FAILED);
Line74   } […]
Line75 This displays the failure, as we can see in Figure 19.1.
Line76 Figure 19.1
Line77 The Sniper shows a failed auction
Line78 The end-to-end test, however, still fails. The synchronization hook we added
Line79 reveals that we haven’t disconnected the Sniper from receiving further events
Line80 from the auction.
Line81 Disconnecting the Sniper
Line82 We turn off a Sniper by removing its AuctionMessageTranslator from its Chat’s
Line83 set of MessageListeners. We can do this safely while processing a message because
Line84 Chat stores its listeners in a thread-safe “copy on write” collection. One obvious
Line85 place to do this is within processMessage() in AuctionMessageTranslator, which
Line86 receives the Chat as an argument, but we have two doubts about this. First, as
Line87 we pointed out in Chapter 12, constructing a real Chat is painful. Most of the
Line88 mocking frameworks support creating a mock class, but it makes us uncomfort-
Line89 able because then we’re deﬁning a relationship with an implementation, not a
Line90 role—we’re being too precise about our dependencies. Second, we might be as-
Line91 signing too many responsibilities to AuctionMessageTranslator; it would have
Line92 to translate the message and decide what to do when it fails.
Line93 219
Line94 Disconnecting the Sniper
Line95 
Line96 
Line97 ---
