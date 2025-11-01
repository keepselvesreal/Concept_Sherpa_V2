Line1 # The Sniper Acquires Some State (pp.144-146)
Line2 
Line3 ---
Line4 **Page 144**
Line5 
Line6 Running the end-to-end tests again shows that we’ve ﬁxed the failure that
Line7 started this chapter (showing Bidding rather than Winning). Now we have to
Line8 make the Sniper win:
Line9 java.lang.AssertionError: 
Line10 Tried to look for...
Line11   exactly 1 JLabel (with name "sniper status")
Line12   in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line13   in all top level windows
Line14 and check that its label text is "Won"
Line15 but...
Line16   all top level windows
Line17   contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
Line18   contained 1 JLabel (with name "sniper status")
Line19 label text was "Lost"
Line20 The Sniper Acquires Some State
Line21 We’re about to introduce a step change in the complexity of the Sniper, if only
Line22 a small one. When the auction closes, we want the Sniper to announce whether
Line23 it has won or lost, which means that it must know whether it was bidding or
Line24 winning at the time. This implies that the Sniper will have to maintain some state,
Line25 which it hasn’t had to so far.
Line26 To get to the functionality we want, we’ll start with the simpler cases where
Line27 the Sniper loses. As Figure 14.2 shows, we’re starting with one- and two-step
Line28 transitions, before adding the additional step that takes the Sniper to the Won state:
Line29 Figure 14.2
Line30 A Sniper bids, then loses
Line31 Chapter 14
Line32 The Sniper Wins the Auction
Line33 144
Line34 
Line35 
Line36 ---
Line37 
Line38 ---
Line39 **Page 145**
Line40 
Line41 We start by revisiting an existing unit test and adding a new one. These tests
Line42 will pass with the current implementation; they’re there to ensure that we don’t
Line43 break the behavior when we add further transitions.
Line44 This introduces some new jMock syntax, states. The idea is to allow us to
Line45 make assertions about the internal state of the object under test. We’ll come back
Line46 to this idea in a moment.
Line47 public class AuctionSniperTest { […]
Line48   private final States sniperState = context.states("sniper"); 1
Line49   @Test public void
Line50   reportsLostIfAuctionClosesImmediately() { 2
Line51     context.checking(new Expectations() {{
Line52       atLeast(1).of(sniperListener).sniperLost();
Line53     }});
Line54     sniper.auctionClosed();
Line55   }
Line56   @Test public void
Line57 reportsLostIfAuctionClosesWhenBidding() {
Line58     context.checking(new Expectations() {{
Line59       ignoring(auction); 3
Line60       allowing(sniperListener).sniperBidding(); 
Line61                               then(sniperState.is("bidding")); 4
Line62 atLeast(1).of(sniperListener).sniperLost(); 
Line63                               when(sniperState.is("bidding")); 5
Line64     }});
Line65     sniper.currentPrice(123, 45, PriceSource.FromOtherBidder); 6
Line66     sniper.auctionClosed();
Line67   }
Line68 }
Line69 1
Line70 We want to keep track of the Sniper’s current state, as signaled by the events
Line71 it sends out, so we ask context for a placeholder. The default state is null.
Line72 2
Line73 We keep our original test, but now it will apply where there are no price
Line74 updates.
Line75 3
Line76 The Sniper will call auction but we really don’t care about that in this test,
Line77 so we tell the test to ignore this collaborator completely.
Line78 4
Line79 When the Sniper sends out a bidding event, it’s telling us that it’s in a bidding
Line80 state, which we record here. We use the allowing() clause to communicate
Line81 that this is a supporting part of the test, not the part we really care about;
Line82 see the note below.
Line83 5
Line84 This is the phrase that matters, the expectation that we want to assert. If the
Line85 Sniper isn’t bidding when it makes this call, the test will fail.
Line86 145
Line87 The Sniper Acquires Some State
Line88 
Line89 
Line90 ---
Line91 
Line92 ---
Line93 **Page 146**
Line94 
Line95 6
Line96 This is our ﬁrst test where we need a sequence of events to get the Sniper
Line97 into the state we want to test. We just call its methods in order.
Line98 Allowances
Line99 jMock distinguishes between allowed and expected invocations. An allowing()
Line100 clause says that the object might make this call, but it doesn’t have to—unlike an
Line101 expectation which will fail the test if the call isn’t made. We make the distinction to
Line102 help express what is important in a test (the underlying implementation is actually
Line103 the same): expectations are what we want to conﬁrm to have happened; allowances
Line104 are supporting infrastructure that helps get the tested objects into the right state,
Line105 or they’re side effects we don’t care about. We return to this topic in “Allowances
Line106 and Expectations” (page 277) and we describe the API in Appendix A.
Line107 Representing Object State
Line108 In cases like this, we want to make assertions about an object’s behavior depending
Line109 on its state, but we don’t want to break encapsulation by exposing how that state
Line110 is implemented. Instead, the test can listen to the notiﬁcation events that the Sniper
Line111 provides to tell interested collaborators about its state in their terms. jMock provides
Line112 States objects, so that tests can record and make assertions about the state of
Line113 an object when something signiﬁcant happens, i.e. when it calls its neighbors; see
Line114 Appendix A for the syntax.
Line115 This is a “logical” representation of what’s going on inside the object, in this case
Line116 the Sniper. It allows the test to describe what it ﬁnds relevant about the Sniper, re-
Line117 gardless of how the Sniper is actually implemented. As you’ll see shortly, this sep-
Line118 aration will allow us to make radical changes to the implementation of the Sniper
Line119 without changing the tests.
Line120 The unit test name reportsLostIfAuctionClosesWhenBidding is very similar
Line121 to the expectation it enforces:
Line122 atLeast(1).of(sniperListener).sniperLost(); when(sniperState.is("bidding"));
Line123 That’s not an accident. We put a lot of effort into ﬁguring out which abstractions
Line124 jMock should support and developing a style that expresses the essential intent
Line125 of a unit test.
Line126 The Sniper Wins
Line127 Finally, we can close the loop and have the Sniper win a bid. The next test
Line128 introduces the Won event.
Line129 Chapter 14
Line130 The Sniper Wins the Auction
Line131 146
Line132 
Line133 
Line134 ---
