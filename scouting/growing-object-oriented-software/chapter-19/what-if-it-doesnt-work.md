Line1 # What If It Doesn't Work? (pp.215-217)
Line2 
Line3 ---
Line4 **Page 215**
Line5 
Line6 Chapter 19
Line7 Handling Failure
Line8 In which we address the reality of programming in an imperfect world,
Line9 and add failure reporting. We add a new auction event that reports
Line10 failure. We attach a new event listener that will turn off the Sniper if
Line11 it fails. We also write a message to a log and write a unit test that mocks
Line12 a class, for which we’re very sorry.
Line13 To avoid trying your patience any further, we close our example here.
Line14 So far, we’ve been prepared to assume that everything just works. This might be
Line15 reasonable if the application is not supposed to last—perhaps it’s acceptable if
Line16 it just crashes and we restart it or, as in this case, we’ve been mainly concerned
Line17 with demonstrating and exploring the domain. Now it’s time to start being explicit
Line18 about how we deal with failures.
Line19 What If It Doesn’t Work?
Line20 Our product people are concerned that Southabee’s On-Line has a reputation
Line21 for occasionally failing and sending incorrectly structured messages, so they want
Line22 us to show that we can cope. It turns out that the system we talk to is actually
Line23 an aggregator for multiple auction feeds, so the failure of an individual auction
Line24 does not imply that the whole system is unsafe. Our policy will be that when we
Line25 receive a message that we cannot interpret, we will mark that auction as Failed
Line26 and ignore any further updates, since it means we can no longer be sure what’s
Line27 happening. Once an auction has failed, we make no attempt to recover.1
Line28 In practice, reporting a message failure means that we ﬂush the price and bid
Line29 values, and show the status as Failed for the offending item. We also record the
Line30 event somewhere so that we can deal with it later. We could make the display
Line31 of the failure more obvious, for example by coloring the row, but we’ll keep this
Line32 version simple and leave any extras as an exercise for the reader.
Line33 The end-to-end test shows that a working Sniper receives a bad message, dis-
Line34 plays and records the failure, and then ignores further updates from this auction:
Line35 1. We admit that it’s unlikely that an auction site that regularly garbles its messages
Line36 will survive for long, but it’s a simple example to work through. We also doubt that
Line37 any serious bidder will be happy to let their bid lie hanging, not knowing whether
Line38 they’ve bought something or lost to a rival. On the other hand, we’ve seen less plau-
Line39 sible systems succeed in the world, propped up by an army of special handling, so
Line40 perhaps you can let us get away with this one.
Line41 215
Line42 
Line43 
Line44 ---
Line45 
Line46 ---
Line47 **Page 216**
Line48 
Line49 @Test public void
Line50 sniperReportsInvalidAuctionMessageAndStopsRespondingToEvents()
Line51     throws Exception 
Line52 {
Line53   String brokenMessage = "a broken message";
Line54   auction.startSellingItem();
Line55   auction2.startSellingItem();
Line56   application.startBiddingIn(auction, auction2);
Line57   auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line58   auction.reportPrice(500, 20, "other bidder");
Line59   auction.hasReceivedBid(520, ApplicationRunner.SNIPER_XMPP_ID);
Line60   auction.sendInvalidMessageContaining(brokenMessage);
Line61   application.showsSniperHasFailed(auction);
Line62   auction.reportPrice(520, 21, "other bidder");
Line63 waitForAnotherAuctionEvent();
Line64   application.reportsInvalidMessage(auction, brokenMessage);
Line65   application.showsSniperHasFailed(auction);
Line66 }
Line67 private void waitForAnotherAuctionEvent() throws Exception {
Line68   auction2.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
Line69   auction2.reportPrice(600, 6, "other bidder");
Line70   application.hasShownSniperIsBidding(auction2, 600, 606);
Line71 }
Line72 where sendInvalidMessageContaining() sends the given invalid string via a chat
Line73 to the Sniper, and showsSniperHasFailed() checks that the status for the item is
Line74 Failed and that the price values have been zeroed. We park the implementation
Line75 of reportsInvalidMessage() for the moment; we’ll come back to it later in this
Line76 chapter.
Line77 Testing That Something Doesn’t Happen
Line78 You’ll have noticed the waitForAnotherAuctionEvent() method which forces an
Line79 unrelated Sniper event and then waits for it to work through the system. Without
Line80 this call, it would be possible for the ﬁnal showSniperHasFailed() check to pass
Line81 incorrectly because it would pick up the previous Sniper state—before the system
Line82 has had time to process the relevant price event. The additional event holds back
Line83 the test just long enough to make sure that the system has caught up. See
Line84 Chapter 27 for more on testing with asynchrony.
Line85 To get this test to fail appropriately, we add a FAILED value to the SniperState
Line86 enumeration, with an associated text mapping in SnipersTabelModel. The
Line87 test fails:
Line88 Chapter 19
Line89 Handling Failure
Line90 216
Line91 
Line92 
Line93 ---
Line94 
Line95 ---
Line96 **Page 217**
Line97 
Line98 […] but... 
Line99   it is not table with row with cells 
Line100     <label with text "item-54321">, <label with text "0">, 
Line101     <label with text "0">, <label with text "Failed">
Line102    because 
Line103 in row 0: component 1 text was "500"
Line104      in row 1: component 0 text was "item-65432"
Line105 It shows that there are two rows in the table: the second is for the other auction,
Line106 and the ﬁrst is showing that the current price is 500 when it should have been
Line107 ﬂushed to 0. This failure is our marker for what we need to build next.
Line108 Detecting the Failure
Line109 The failure will actually occur in the AuctionMessageTranslator (last shown in
Line110 Chapter 14) which will throw a runtime exception when it tries to parse the
Line111 message. The Smack library drops exceptions thrown by MessageHandlers,
Line112 so we have to make sure that our handler catches everything. As we write
Line113 a unit test for a failure in the translator, we realize that we need to report a
Line114 new type of auction event, so we add an auctionFailed() method to the
Line115 AuctionEventListener interface.
Line116 @Test public void
Line117 notifiesAuctionFailedWhenBadMessageReceived() {
Line118   context.checking(new Expectations() {{  
Line119     exactly(1).of(listener).auctionFailed(); 
Line120   }});
Line121   Message message = new Message();
Line122   message.setBody("a bad message");
Line123   translator.processMessage(UNUSED_CHAT, message);
Line124 }
Line125 This fails with an ArrayIndexOutOfBoundsException when it tries to unpack a
Line126 name/value pair from the string. We could be precise about which exceptions to
Line127 catch but in practice it doesn’t really matter here: we either parse the message or
Line128 we don’t, so to make the test pass we extract the bulk of processMessage() into
Line129 a translate() method and wrap a try/catch block around it.
Line130 public class AuctionMessageTranslator implements MessageListener {
Line131   public void processMessage(Chat chat, Message message) {
Line132     try {
Line133 translate(message.getBody());
Line134     } catch (Exception parseException) {
Line135       listener.auctionFailed();
Line136     }
Line137   }
Line138 While we’re here, there’s another failure mode we’d like to check. It’s possible
Line139 that a message is well-formed but incomplete: it might be missing one of its ﬁelds
Line140 217
Line141 Detecting the Failure
Line142 
Line143 
Line144 ---
