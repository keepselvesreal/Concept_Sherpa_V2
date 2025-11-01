Line1 # Unpacking a Price Message (pp.118-121)
Line2 
Line3 ---
Line4 **Page 118**
Line5 
Line6 Figure 12.2
Line7 Introducing the AuctionMessageTranslator
Line8 What Have We Achieved?
Line9 In this baby step, we’ve extracted a single feature of our application into a separate
Line10 class, which means the functionality now has a name and can be unit-tested.
Line11 We’ve also made Main a little simpler, now that it’s no longer concerned with
Line12 interpreting the text of messages from the auction. This is not yet a big deal but
Line13 we will show, as the Sniper application grows, how this approach helps us keep
Line14 code clean and ﬂexible, with clear responsibilities and relationships between its
Line15 components.
Line16 Unpacking a Price Message
Line17 Introducing Message Event Types
Line18 We’re about to introduce a second auction message type, the current price update.
Line19 The Sniper needs to distinguish between the two, so we take another look at the
Line20 message formats in Chapter 9 that Southabee’s On-Line have sent us. They’re
Line21 simple—just a single line with a few name/value pairs. Here are examples for
Line22 the formats again:
Line23 SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
Line24 SOLVersion: 1.1; Event: CLOSE;
Line25 At ﬁrst, being object-oriented enthusiasts, we try to model these messages as
Line26 types, but we’re not clear enough about the behavior to justify any meaningful
Line27 structure, so we back off the idea. We decide to start with a simplistic solution
Line28 and adapt from there.
Line29 The Second Test
Line30 The introduction of a different Price event in our second test will force us to
Line31 parse the incoming message. This test has the same structure as the ﬁrst one but
Line32 gets a different input string and expects us to call a different method on the lis-
Line33 tener. A Price message includes details of the last bid, which we need to unpack
Line34 and pass to the listener, so we include them in the signature of the new method
Line35 currentPrice(). Here’s the test:
Line36 @Test public void
Line37 notifiesBidDetailsWhenCurrentPriceMessageReceived() {
Line38 Chapter 12
Line39 Getting Ready to Bid
Line40 118
Line41 
Line42 
Line43 ---
Line44 
Line45 ---
Line46 **Page 119**
Line47 
Line48 context.checking(new Expectations() {{
Line49 exactly(1).of(listener).currentPrice(192, 7);
Line50   }});
Line51   Message message = new Message();
Line52     message.setBody(
Line53 "SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
Line54                    );
Line55   translator.processMessage(UNUSED_CHAT, message);
Line56 }
Line57 To get through the compiler, we add a method to the listener; this takes just
Line58 a keystroke in the IDE:1
Line59 public interface AuctionEventListener {
Line60   void auctionClosed();
Line61 void currentPrice(int price, int increment);
Line62 }
Line63 The test fails.
Line64 unexpected invocation: auctionEventListener.auctionClosed()
Line65 expectations:
Line66   ! expected once, never invoked: auctionEventListener.currentPrice(<192>, <7>)
Line67 what happened before this: nothing!
Line68 […]
Line69   at $Proxy6.auctionClosed()
Line70   at auctionsniper.AuctionMessageTranslator.processMessage()
Line71   at AuctionMessageTranslatorTest.translatesPriceMessagesAsAuctionPriceEvents()
Line72 […]
Line73   at JUnit4ClassRunner.run(JUnit4ClassRunner.java:42)
Line74 This time the critical phrase is:
Line75 unexpected invocation: auctionEventListener.auctionClosed()
Line76 which means that the code called the wrong method, auctionClosed(), during
Line77 the test. The Mockery isn’t expecting this call so it fails immediately, showing us
Line78 in the stack trace the line that triggered the failure (you can see the workings of
Line79 the Mockery in the line $Proxy6.auctionClosed() which is the runtime substitute
Line80 for a real AuctionEventListener). Here, the place where the code failed is obvious,
Line81 so we can just ﬁx it.
Line82 Our ﬁrst version is rough, but it passes the test.
Line83 1. Modern development environments, such as Eclipse and IDEA, will ﬁll in a missing
Line84 method on request. This means that we can write the call we’d like to make and ask
Line85 the tool to ﬁll in the declaration for us.
Line86 119
Line87 Unpacking a Price Message
Line88 
Line89 
Line90 ---
Line91 
Line92 ---
Line93 **Page 120**
Line94 
Line95 public class AuctionMessageTranslator implements MessageListener {
Line96   private final AuctionEventListener listener;
Line97   public AuctionMessageTranslator(AuctionEventListener listener) {
Line98     this.listener = listener;
Line99   }
Line100   public void processMessage(Chat chat, Message message) {
Line101     HashMap<String, String> event = unpackEventFrom(message);
Line102     String type = event.get("Event");
Line103     if ("CLOSE".equals(type)) {
Line104       listener.auctionClosed();
Line105     } else if ("PRICE".equals(type)) {
Line106       listener.currentPrice(Integer.parseInt(event.get("CurrentPrice")), 
Line107                             Integer.parseInt(event.get("Increment")));
Line108     }
Line109   }
Line110   private HashMap<String, String> unpackEventFrom(Message message) {
Line111     HashMap<String, String> event = new HashMap<String, String>();  
Line112     for (String element : message.getBody().split(";")) {
Line113       String[] pair = element.split(":");
Line114       event.put(pair[0].trim(), pair[1].trim());
Line115     }
Line116     return event;
Line117   }
Line118 }
Line119 This implementation breaks the message body into a set of key/value pairs,
Line120 which it interprets as an auction event so it can notify the AuctionEventListener.
Line121 We also have to ﬁx the FakeAuctionServer to send a real Close event rather than
Line122 the current empty message, otherwise the end-to-end tests will fail incorrectly.
Line123 public void announceClosed() throws XMPPException {
Line124 currentChat.sendMessage("SOLVersion: 1.1; Event: CLOSE;");
Line125 }
Line126 Running our end-to-end test again reminds us that we’re still working on the
Line127 bidding feature. The test shows that the Sniper status label still displays Joining
Line128 rather than Bidding.
Line129 Discovering Further Work
Line130 This code passes the unit test, but there’s something missing. It assumes that the
Line131 message is correctly structured and has the right version. Given that the message
Line132 will be coming from an outside system, this feels risky, so we need to add some
Line133 error handling. We don’t want to break the ﬂow of getting features to work, so
Line134 we add error handling to the to-do list to come back to it later (Figure 12.3).
Line135 Chapter 12
Line136 Getting Ready to Bid
Line137 120
Line138 
Line139 
Line140 ---
Line141 
Line142 ---
Line143 **Page 121**
Line144 
Line145 Figure 12.3
Line146 Added tasks for handling errors
Line147 We’re also concerned that the translator is not as clear as it could be about
Line148 what it’s doing, with its parsing and the dispatching activities mixed together.
Line149 We make a note to address this class as soon as we’ve passed the acceptance
Line150 test, which isn’t far off.
Line151 Finish the Job
Line152 Most of the work in this chapter has been trying to decide what we want to say
Line153 and how to say it: we write a high-level end-to-end test to describe what the
Line154 Sniper should implement; we write long unit test names to tell us what a class
Line155 does; we extract new classes to tease apart ﬁne-grained aspects of the functional-
Line156 ity; and we write lots of little methods to keep each layer of code at a consistent
Line157 level of abstraction. But ﬁrst, we write a rough implementation to prove that we
Line158 know how to make the code do what’s required and then we refactor—which
Line159 we’ll do in the next chapter.
Line160 We cannot emphasize strongly enough that “ﬁrst-cut” code is not ﬁnished. It’s
Line161 good enough to sort out our ideas and make sure we have everything in place,
Line162 but it’s unlikely to express its intentions cleanly. That will make it a drag on
Line163 productivity as it’s read repeatedly over the lifetime of the code. It’s like carpentry
Line164 without sanding—eventually someone ends up with a nasty splinter.
Line165 121
Line166 Finish the Job
Line167 
Line168 
Line169 ---
