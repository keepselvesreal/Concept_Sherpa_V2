Line1 # Detecting the Failure (pp.217-218)
Line2 
Line3 ---
Line4 **Page 217**
Line5 
Line6 […] but... 
Line7   it is not table with row with cells 
Line8     <label with text "item-54321">, <label with text "0">, 
Line9     <label with text "0">, <label with text "Failed">
Line10    because 
Line11 in row 0: component 1 text was "500"
Line12      in row 1: component 0 text was "item-65432"
Line13 It shows that there are two rows in the table: the second is for the other auction,
Line14 and the ﬁrst is showing that the current price is 500 when it should have been
Line15 ﬂushed to 0. This failure is our marker for what we need to build next.
Line16 Detecting the Failure
Line17 The failure will actually occur in the AuctionMessageTranslator (last shown in
Line18 Chapter 14) which will throw a runtime exception when it tries to parse the
Line19 message. The Smack library drops exceptions thrown by MessageHandlers,
Line20 so we have to make sure that our handler catches everything. As we write
Line21 a unit test for a failure in the translator, we realize that we need to report a
Line22 new type of auction event, so we add an auctionFailed() method to the
Line23 AuctionEventListener interface.
Line24 @Test public void
Line25 notifiesAuctionFailedWhenBadMessageReceived() {
Line26   context.checking(new Expectations() {{  
Line27     exactly(1).of(listener).auctionFailed(); 
Line28   }});
Line29   Message message = new Message();
Line30   message.setBody("a bad message");
Line31   translator.processMessage(UNUSED_CHAT, message);
Line32 }
Line33 This fails with an ArrayIndexOutOfBoundsException when it tries to unpack a
Line34 name/value pair from the string. We could be precise about which exceptions to
Line35 catch but in practice it doesn’t really matter here: we either parse the message or
Line36 we don’t, so to make the test pass we extract the bulk of processMessage() into
Line37 a translate() method and wrap a try/catch block around it.
Line38 public class AuctionMessageTranslator implements MessageListener {
Line39   public void processMessage(Chat chat, Message message) {
Line40     try {
Line41 translate(message.getBody());
Line42     } catch (Exception parseException) {
Line43       listener.auctionFailed();
Line44     }
Line45   }
Line46 While we’re here, there’s another failure mode we’d like to check. It’s possible
Line47 that a message is well-formed but incomplete: it might be missing one of its ﬁelds
Line48 217
Line49 Detecting the Failure
Line50 
Line51 
Line52 ---
Line53 
Line54 ---
Line55 **Page 218**
Line56 
Line57 such as the event type or current price. We write a couple of tests to conﬁrm that
Line58 we can catch these, for example:
Line59 @Test public void
Line60 notifiesAuctionFailedWhenEventTypeMissing() {
Line61   context.checking(new Expectations() {{  
Line62     exactly(1).of(listener).auctionFailed(); 
Line63   }});
Line64   Message message = new Message();
Line65   message.setBody("SOLVersion: 1.1; CurrentPrice: 234; Increment: 5; Bidder: "
Line66                   + SNIPER_ID + ";");
Line67   translator.processMessage(UNUSED_CHAT, message);
Line68 }
Line69 Our ﬁx is to throw an exception whenever we try to get a value that has not
Line70 been set, and we deﬁne MissingValueException for this purpose.
Line71 public static class AuctionEvent { […]
Line72   private String get(String name) throws MissingValueException {
Line73     String value = values.get(name);
Line74 if (null == value) {
Line75       throw new MissingValueException(name);
Line76     }
Line77     return value;
Line78   }
Line79 }
Line80 Displaying the Failure
Line81 We added an auctionFailed() method to AuctionEventListener while unit-
Line82 testing AuctionMessageTranslator. This triggers a compiler warning in
Line83 AuctionSniper, so we added an empty implementation to keep going. Now
Line84 it’s time to make it work, which turns out to be easy. We write some tests in
Line85 AuctionSniperTest for the new state transitions, for example:
Line86 @Test public void
Line87 reportsFailedIfAuctionFailsWhenBidding() {
Line88   ignoringAuction();
Line89   allowingSniperBidding();
Line90   expectSniperToFailWhenItIs("bidding");
Line91   sniper.currentPrice(123, 45, PriceSource.FromOtherBidder); 
Line92   sniper.auctionFailed(); 
Line93 }
Line94 private void expectSniperToFailWhenItIs(final String state) {
Line95   context.checking(new Expectations() {{
Line96     atLeast(1).of(sniperListener).sniperStateChanged(
Line97         new SniperSnapshot(ITEM_ID, 00, 0, SniperState.FAILED)); 
Line98                                     when(sniperState.is(state));
Line99   }});
Line100 }
Line101 Chapter 19
Line102 Handling Failure
Line103 218
Line104 
Line105 
Line106 ---
