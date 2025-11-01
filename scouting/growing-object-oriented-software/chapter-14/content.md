# Chapter 14: The Sniper Wins the Auction (pp.139-148)

---
**Page 139**

Chapter 14
The Sniper Wins the Auction
In which we add another feature to our Sniper and let it win an auction.
We introduce the concept of state to the Sniper which we test by listen-
ing to its callbacks. We ﬁnd that even this early, one of our refactorings
has paid off.
First, a Failing Test
We have a Sniper that can respond to price changes by bidding more, but it
doesn’t yet know when it’s successful. Our next feature on the to-do list is to
win an auction. This involves an extra state transition, as you can see in
Figure 14.1:
Figure 14.1
A sniper bids, then wins
To represent this, we add an end-to-end test based on sniperMakesAHigherBid-
ButLoses() with a different conclusion—sniperWinsAnAuctionByBiddingHigher().
Here’s the test, with the new features highlighted:
139


---
**Page 140**

public class AuctionSniperEndToEndTest { […]
  @Test public void
sniperWinsAnAuctionByBiddingHigher() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
    auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1000, 98, "other bidder");
    application.hasShownSniperIsBidding();
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
    application.hasShownSniperIsWinning();
    auction.announceClosed();
    application.showsSniperHasWonAuction();
  }
}
In our test infrastructure we add the two methods to check that the user interface
shows the two new states to the ApplicationRunner.
This generates a new failure message:
java.lang.AssertionError: 
Tried to look for...
  exactly 1 JLabel (with name "sniper status")
  in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  in all top level windows
and check that its label text is "Winning"
but...
  all top level windows
  contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  contained 1 JLabel (with name "sniper status")
label text was "Bidding"
Now we know where we’re going, we can implement the feature.
Who Knows about Bidders?
The application knows that the Sniper is winning if it’s the bidder for the last
price that the auction accepted. We have to decide where to put that logic.
Looking again at Figure 13.5 on page 134, one choice would be that the translator
could pass the bidder through to the Sniper and let the Sniper decide. That would
mean that the Sniper would have to know something about how bidders are
identiﬁed by the auction, with a risk of pulling in XMPP details that we’ve been
careful to keep separate. To decide whether it’s winning, the only thing the Sniper
needs to know when a price arrives is, did this price come from me? This is a
Chapter 14
The Sniper Wins the Auction
140


---
**Page 141**

choice, not an identiﬁer, so we’ll represent it with an enumeration PriceSource
which we include in AuctionEventListener.1
Incidentally, PriceSource is an example of a value type. We want code that
describes the domain of Sniping—not, say, a boolean which we would have to
interpret every time we read it; there’s more discussion in “Value Types”
(page 59).
public interface AuctionEventListener extends EventListener {
enum PriceSource {
    FromSniper, FromOtherBidder;
  };
[…]
We take the view that determining whether this is our price or not is part of
the translator’s role. We extend currentPrice() with a new parameter and
change the translator’s unit tests; note that we change the name of the existing
test to include the extra feature. We also take the opportunity to pass the Sniper
identiﬁer to the translator in SNIPER_ID. This ties the setup of the translator to
the input message in the second test.
public class AuctionMessageTranslatorTest { […]
  private final AuctionMessageTranslator translator = 
                    new AuctionMessageTranslator(SNIPER_ID, listener);
  @Test public void
  notifiesBidDetailsWhenCurrentPriceMessageReceivedFromOtherBidder() {
    context.checking(new Expectations() {{
      exactly(1).of(listener).currentPrice(192, 7, PriceSource.FromOtherBidder);
    }});
    Message message = new Message();
    message.setBody(
"SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
                   );
    translator.processMessage(UNUSED_CHAT, message);
  }
  @Test public void
notifiesBidDetailsWhenCurrentPriceMessageReceivedFromSniper() {
    context.checking(new Expectations() {{
      exactly(1).of(listener).currentPrice(234, 5, PriceSource.FromSniper);
    }});
    Message message = new Message();
    message.setBody(
"SOLVersion: 1.1; Event: PRICE; CurrentPrice: 234; Increment: 5; Bidder: " 
      + SNIPER_ID + ";");
    translator.processMessage(UNUSED_CHAT, message);
  }
}
1. Some developers we know have an allergic reaction to nested types. In Java, we use
them as a form of ﬁne-grained scoping. In this case, PriceSource is always used
together with AuctionEventListener, so it makes sense to bind the two together.
141
Who Knows about Bidders?


---
**Page 142**

The new test fails:
unexpected invocation: 
  auctionEventListener.currentPrice(<192>, <7>, <FromOtherBidder>)
expectations:
! expected once, never invoked: 
    auctionEventListener.currentPrice(<192>, <7>, <FromSniper>)
      parameter 0 matched: <192>
      parameter 1 matched: <7>
      parameter 2 did not match: <FromSniper>, because was <FromOtherBidder>
what happened before this: nothing!
The ﬁx is to compare the Sniper identiﬁer to the bidder from the event message.
public class AuctionMessageTranslator implements MessageListener {  […]
private final String sniperId;
  public void processMessage(Chat chat, Message message) {
[…]
    } else if (EVENT_TYPE_PRICE.equals(type)) {
      listener.currentPrice(event.currentPrice(), 
                            event.increment(), 
event.isFrom(sniperId));
    }
  }
  public static class AuctionEvent { […]
public PriceSource isFrom(String sniperId) {
      return sniperId.equals(bidder()) ? FromSniper : FromOtherBidder;
    }
    private String bidder() { return get("Bidder"); }
  }
}
The work we did in “Tidying Up the Translator” (page 135) to separate the
different responsibilities within the translator has paid off here. All we had to
do was add a couple of extra methods to AuctionEvent to get a very readable
solution.
Finally, to get all the code through the compiler, we ﬁx joinAuction() in Main
to pass in the new constructor parameter for the translator. We can get a correctly
structured identiﬁer from connection.
private void joinAuction(XMPPConnection connection, String itemId) {
[…]
  Auction auction = new XMPPAuction(chat);
  chat.addMessageListener(
      new AuctionMessageTranslator(
connection.getUser(), 
             new AuctionSniper(auction, new SniperStateDisplayer())));
  auction.join();
}
Chapter 14
The Sniper Wins the Auction
142


---
**Page 143**

The Sniper Has More to Say
Our immediate end-to-end test failure tells us that we should make the user inter-
face show when the Sniper is winning. Our next implementation step is to follow
through by ﬁxing the AuctionSniper to interpret the isFromSniper parameter
we’ve just added. Once again we start with a unit test.
public class AuctionSniperTest { […]
  @Test public void
reportsIsWinningWhenCurrentPriceComesFromSniper() {
    context.checking(new Expectations() {{
      atLeast(1).of(sniperListener).sniperWinning();
    }});
    sniper.currentPrice(123, 45, PriceSource.FromSniper);
  }
}
To get through the compiler, we add the new sniperWinning() method to
SniperListener which, in turn, means that we add an empty implementation
to SniperStateDisplayer.
The test fails:
unexpected invocation: auction.bid(<168>)
expectations:
! expected at least 1 time, never invoked: sniperListener.sniperWinning()
what happened before this: nothing!
This failure is a nice example of trapping a method that we didn’t expect. We set
no expectations on the auction, so calls to any of its methods will fail the test.
If you compare this test to bidsHigherAndReportsBiddingWhenNewPriceArrives()
in “The AuctionSniper Bids” (page 126) you’ll also see that we drop the price
and increment variables and just feed in numbers. That’s because, in this test,
there’s no calculation to do, so we don’t need to reference them in an expectation.
They’re just details to get us to the interesting behavior.
The ﬁx is straightforward:
public class AuctionSniper implements AuctionEventListener { […]
  public void currentPrice(int price, int increment, PriceSource priceSource) {
switch (priceSource) {
    case FromSniper:
      sniperListener.sniperWinning();
      break;
    case FromOtherBidder:
      auction.bid(price + increment); 
      sniperListener.sniperBidding();
      break;
    }
  } 
}
143
The Sniper Has More to Say


---
**Page 144**

Running the end-to-end tests again shows that we’ve ﬁxed the failure that
started this chapter (showing Bidding rather than Winning). Now we have to
make the Sniper win:
java.lang.AssertionError: 
Tried to look for...
  exactly 1 JLabel (with name "sniper status")
  in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  in all top level windows
and check that its label text is "Won"
but...
  all top level windows
  contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
  contained 1 JLabel (with name "sniper status")
label text was "Lost"
The Sniper Acquires Some State
We’re about to introduce a step change in the complexity of the Sniper, if only
a small one. When the auction closes, we want the Sniper to announce whether
it has won or lost, which means that it must know whether it was bidding or
winning at the time. This implies that the Sniper will have to maintain some state,
which it hasn’t had to so far.
To get to the functionality we want, we’ll start with the simpler cases where
the Sniper loses. As Figure 14.2 shows, we’re starting with one- and two-step
transitions, before adding the additional step that takes the Sniper to the Won state:
Figure 14.2
A Sniper bids, then loses
Chapter 14
The Sniper Wins the Auction
144


---
**Page 145**

We start by revisiting an existing unit test and adding a new one. These tests
will pass with the current implementation; they’re there to ensure that we don’t
break the behavior when we add further transitions.
This introduces some new jMock syntax, states. The idea is to allow us to
make assertions about the internal state of the object under test. We’ll come back
to this idea in a moment.
public class AuctionSniperTest { […]
  private final States sniperState = context.states("sniper"); 1
  @Test public void
  reportsLostIfAuctionClosesImmediately() { 2
    context.checking(new Expectations() {{
      atLeast(1).of(sniperListener).sniperLost();
    }});
    sniper.auctionClosed();
  }
  @Test public void
reportsLostIfAuctionClosesWhenBidding() {
    context.checking(new Expectations() {{
      ignoring(auction); 3
      allowing(sniperListener).sniperBidding(); 
                              then(sniperState.is("bidding")); 4
atLeast(1).of(sniperListener).sniperLost(); 
                              when(sniperState.is("bidding")); 5
    }});
    sniper.currentPrice(123, 45, PriceSource.FromOtherBidder); 6
    sniper.auctionClosed();
  }
}
1
We want to keep track of the Sniper’s current state, as signaled by the events
it sends out, so we ask context for a placeholder. The default state is null.
2
We keep our original test, but now it will apply where there are no price
updates.
3
The Sniper will call auction but we really don’t care about that in this test,
so we tell the test to ignore this collaborator completely.
4
When the Sniper sends out a bidding event, it’s telling us that it’s in a bidding
state, which we record here. We use the allowing() clause to communicate
that this is a supporting part of the test, not the part we really care about;
see the note below.
5
This is the phrase that matters, the expectation that we want to assert. If the
Sniper isn’t bidding when it makes this call, the test will fail.
145
The Sniper Acquires Some State


---
**Page 146**

6
This is our ﬁrst test where we need a sequence of events to get the Sniper
into the state we want to test. We just call its methods in order.
Allowances
jMock distinguishes between allowed and expected invocations. An allowing()
clause says that the object might make this call, but it doesn’t have to—unlike an
expectation which will fail the test if the call isn’t made. We make the distinction to
help express what is important in a test (the underlying implementation is actually
the same): expectations are what we want to conﬁrm to have happened; allowances
are supporting infrastructure that helps get the tested objects into the right state,
or they’re side effects we don’t care about. We return to this topic in “Allowances
and Expectations” (page 277) and we describe the API in Appendix A.
Representing Object State
In cases like this, we want to make assertions about an object’s behavior depending
on its state, but we don’t want to break encapsulation by exposing how that state
is implemented. Instead, the test can listen to the notiﬁcation events that the Sniper
provides to tell interested collaborators about its state in their terms. jMock provides
States objects, so that tests can record and make assertions about the state of
an object when something signiﬁcant happens, i.e. when it calls its neighbors; see
Appendix A for the syntax.
This is a “logical” representation of what’s going on inside the object, in this case
the Sniper. It allows the test to describe what it ﬁnds relevant about the Sniper, re-
gardless of how the Sniper is actually implemented. As you’ll see shortly, this sep-
aration will allow us to make radical changes to the implementation of the Sniper
without changing the tests.
The unit test name reportsLostIfAuctionClosesWhenBidding is very similar
to the expectation it enforces:
atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
That’s not an accident. We put a lot of effort into ﬁguring out which abstractions
jMock should support and developing a style that expresses the essential intent
of a unit test.
The Sniper Wins
Finally, we can close the loop and have the Sniper win a bid. The next test
introduces the Won event.
Chapter 14
The Sniper Wins the Auction
146


---
**Page 147**

@Test public void
reportsWonIfAuctionClosesWhenWinning() {
  context.checking(new Expectations() {{
    ignoring(auction);
    allowing(sniperListener).sniperWinning();  then(sniperState.is("winning"));
    atLeast(1).of(sniperListener).sniperWon(); when(sniperState.is("winning"));
  }});
  sniper.currentPrice(123, 45, true);
  sniper.auctionClosed();
}
It has the same structure but represents when the Sniper has won. The test fails
because the Sniper called sniperLost().
unexpected invocation: sniperListener.sniperLost()
expectations:
  allowed, never invoked: 
    auction.<any method>(<any parameters>) was[]; 
  allowed, already invoked 1 time: sniperListener.sniperWinning(); 
                                     then sniper is winning
  expected at least 1 time, never invoked: sniperListener.sniperWon();
                                             when sniper is winning
states:
  sniper is winning
what happened before this:
  sniperListener.sniperWinning()
We add a ﬂag to represent the Sniper’s state, and implement the new
sniperWon() method in the SniperStateDisplayer.
public class AuctionSniper implements AuctionEventListener { […]
private boolean isWinning = false;
  public void auctionClosed() {
if (isWinning) {
      sniperListener.sniperWon();
    } else {
      sniperListener.sniperLost();
    }
  }
  public void currentPrice(int price, int increment, PriceSource priceSource) {
isWinning = priceSource == PriceSource.FromSniper;
    if (isWinning) {
      sniperListener.sniperWinning();
    } else {
      auction.bid(price + increment);
      sniperListener.sniperBidding();
    }
  }
}
public class SniperStateDisplayer implements SniperListener { […]
  public void sniperWon() {
    showStatus(MainWindow.STATUS_WON);
  }
}
147
The Sniper Wins


---
**Page 148**

Having previously made a fuss about PriceSource, are we being inconsistent
here by using a boolean for isWinning? Our excuse is that we did try an enum
for the Sniper state, but it just looked too complicated. The ﬁeld is private to
AuctionSniper, which is small enough so it’s easy to change later and the code
reads well.
The unit and end-to-end tests all pass now, so we can cross off another item
from the to-do list in Figure 14.3.
Figure 14.3
The Sniper wins
There are more tests we could write—for example, to describe the transitions
from bidding to winning and back again, but we’ll leave those as an exercise for
you, Dear Reader. Instead, we’ll move on to the next signiﬁcant change in
functionality.
Making Steady Progress
As always, we made steady progress by adding little slices of functionality. First
we made the Sniper show when it’s winning, then when it has won. We used
empty implementations to get us through the compiler when we weren’t ready
to ﬁll in the code, and we stayed focused on the immediate task.
One of the pleasant surprises is that, now the code is growing a little, we’re
starting to see some of our earlier effort pay off as new features just ﬁt into the
existing structure. The next tasks we have to implement will shake this up.
Chapter 14
The Sniper Wins the Auction
148


