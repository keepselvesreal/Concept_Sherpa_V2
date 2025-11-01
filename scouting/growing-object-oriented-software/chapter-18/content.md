# Chapter 18: Filling In the Details (pp.205-214)

---
**Page 205**

Chapter 18
Filling In the Details
In which we introduce a stop price so we don’t bid inﬁnitely, which
means we can now be losing an auction that hasn’t yet closed. We add
a new ﬁeld to the user interface and push it through to the Sniper. We
realize we should have created an Item type much earlier.
A More Useful Application
So far the functionality has been prioritized to attract potential customers by
giving them a sense of what the application will look like. We can show items
being added and some features of sniping. It’s not a very useful application be-
cause, amongst other things, there’s no upper limit for bidding on an item—it
could be very expensive to deploy.
This is a common pattern when using Agile Development techniques to work
on a new project. The team is ﬂexible enough to respond to how the needs of
the sponsors change over time: at the beginning, the emphasis might be on
proving the concept to attract enough support to continue; later, the emphasis
might be on implementing enough functionality to be ready to deploy; later still,
the emphasis might change to providing more options to support a wider range
of users.
This dynamic is very different from both a ﬁxed design approach, where the
structure of the development has to be approved before work can begin, and a
code-and-ﬁx approach, where the system might be initially successful but not
resilient enough to adapt to its changing role.
Stop When We’ve Had Enough
Our next most pressing task (especially after recent crises in the ﬁnancial markets)
is to be able to set an upper limit, the “stop price,” for our bid for an item.
Introducing a Losing State
With the introduction of a stop price, it’s possible for a Sniper to be losing before
the auction has closed. We could implement this by just marking the Sniper as
Lost when it hits its stop price, but the users want to know the ﬁnal price when
the auction has ﬁnished after they’ve dropped out, so we model this as an extra
state. Once a Sniper has been outbid at its stop price, it will never be able to win,
205


---
**Page 206**

so the only option left is to wait for the auction to close, accepting updates of
any new (higher) prices from other bidders.
We adapt the state machine we drew in Figure 9.3 to include the new
transitions. The result is Figure 18.1.
Figure 18.1
A bidder may now be losing
The First Failing Test
Of course we start with a failing test. We won’t go through all the cases here,
but this example will take us through the essentials. First, we write an end-to-
end test to describe the new feature. It shows a scenario where our Sniper bids
for an item but loses because it bumps into its stop price, and other bidders
continue until the auction closes.
@Test public void sniperLosesAnAuctionWhenThePriceIsTooHigh() throws Exception {
  auction.startSellingItem();
application.startBiddingWithStopPrice(auction, 1100);
  auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID); 
  auction.reportPrice(1000, 98, "other bidder"); 
  application.hasShownSniperIsBidding(auction, 1000, 1098);
  auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
  auction.reportPrice(1197, 10, "third party");
application.hasShownSniperIsLosing(auction, 1197, 1098);
  auction.reportPrice(1207, 10, "fourth party");
application.hasShownSniperIsLosing(auction, 1207, 1098);
  auction.announceClosed();
  application.showsSniperHasLostAuction(auction, 1207, 1098); 
}
Chapter 18
Filling In the Details
206


---
**Page 207**

This test introduces two new methods into our test infrastructure, which we
need to ﬁll in to get through the compiler. First, startBiddingWithStopPrice()
passes the new stop price value through the ApplicationRunner to the
AuctionSniperDriver.
public class AuctionSniperDriver extends JFrameDriver {
  public void startBiddingFor(String itemId, int stopPrice) {
    textField(NEW_ITEM_ID_NAME).replaceAllText(itemId); 
textField(NEW_ITEM_STOP_PRICE_NAME).replaceAllText(String.valueOf(stopPrice));
    bidButton().click(); 
  }
[…]
}
This implies that we need a new input ﬁeld in the user interface for the stop price,
so we create a constant to identify it in MainWindow (we’ll ﬁll in the component
itself soon). We also need to support our existing tests which do not have a stop
price, so we change them to use Integer.MAX_VALUE to represent no stop price
at all.
The other new method in ApplicationRunner is hasShownSniperIsLosing(),
which is the same as the other checking methods, except that it uses a new Losing
value in SniperState:
public enum SniperState {
LOSING {
    @Override public SniperState whenAuctionClosed() { return LOST; }
  }, […]
and, to complete the loop, we add a value to the display text in
SnipersTableModel:
private final static String[] STATUS_TEXT = {
  "Joining", "Bidding", "Winning", "Losing", "Lost", "Won" 
};
The failure message says that we have no stop price ﬁeld:
[…] but...
  all top level windows
  contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
contained 0 JTextField (with name "stop price")
Now we have a failing end-to-end test that describes our intentions for the
feature, so we can implement it.
Typing In the Stop Price
To make any progress, we must add a component to the user interface that will
accept a stop price. Our current design, which we saw in Figure 16.2, has only
a ﬁeld for the item identiﬁer but we can easily adjust it to take a stop price in the
top bar.
207
Stop When We’ve Had Enough


---
**Page 208**

For our implementation, we will add a JFormattedTextField for the stop price
that is constrained to accept only integer values, and a couple of labels. The new
top bar looks like Figure 18.2.
Figure 18.2
The Sniper with a stop price ﬁeld in its bar
We get the test failure we expect, which is that the Sniper is not losing because
it continues to bid:
[…] but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JTable ()
   it is not table with row with cells 
     <label with text "item-54321">, <label with text "1098">, 
     <label with text "1197">, <label with text "Losing">
    because 
in row 0: component 1 text was "1197"
Propagating the Stop Price
To make this feature work, we need to pass the stop price from the user interface
to the AuctionSniper, which can then use it to limit further bidding. The chain
starts when MainWindow notiﬁes its UserRequestListener using:
void joinAuction(String itemId);
The obvious thing to do is to add a stopPrice argument to this method and to
the rest of the chain of calls, until it reaches the AuctionSniper class. We want
to make a point here, so we’ll force a slightly different approach to propagating
the new value.
Another way to look at it is that the user interface constructs a description of
the user’s “policy” for the Sniper’s bidding on an item. So far this has only in-
cluded the item’s identiﬁer (“bid on this item”), but now we’re adding a stop
price (“bid up to this amount on this item”) so there’s more structure.
Chapter 18
Filling In the Details
208


---
**Page 209**

We want to make this structure explicit, so we create a new class, Item. We
start with a simple value that just carries the identiﬁer and stop price as public
immutable ﬁelds; we can move behavior into it later.
public class Item {
  public final String identifier;
  public final int stopPrice;
  public Item(String identifier, int stopPrice) { 
    this.identifier = identifier;
    this.stopPrice = stopPrice; 
  }
// also equals(), hashCode(), toString()
} 
Introducing the Item class is an example of budding off that we described in
“Value Types” (page 59). It’s a placeholder type that we use to identify a concept
and that gives us somewhere to attach relevant new features as the code grows.
We push Item into the code and see what breaks, starting with
UserRequestListener:
public interface UserRequestListener extends EventListener {
  void joinAuction(Item item);
}
First we ﬁx MainWindowTest, the integration test we wrote for the Swing imple-
mentation in Chapter 16. The language is already beginning to shift. In the pre-
vious version of this test, the probe variable was called buttonProbe, which
describes the structure of the user interface. That doesn’t make sense any more,
so we’ve renamed it itemProbe, which describes a collaboration between
MainWindow and its neighbors.
@Test public void 
makesUserRequestWhenJoinButtonClicked() { 
  final ValueMatcherProbe<Item> itemProbe = 
    new ValueMatcherProbe<Item>(equalTo(new Item("an item-id", 789)), "item request");
  mainWindow.addUserRequestListener( 
      new UserRequestListener() { 
        public void joinAuction(Item item) { 
itemProbe.setReceivedValue(item); 
        } 
      }); 
  driver.startBiddingFor("an item-id", 789);
  driver.check(itemProbe); 
}
We make this test pass by extracting the stop price value within MainWindow.
209
Stop When We’ve Had Enough


---
**Page 210**

joinAuctionButton.addActionListener(new ActionListener() { 
  public void actionPerformed(ActionEvent e) { 
    userRequests.announce().joinAuction(new Item(itemId(), stopPrice())); 
  } 
  private String itemId() {
    return itemIdField.getText();
  }
  private int stopPrice() { 
    return ((Number)stopPriceField.getValue()).intValue(); 
  } 
});
This pushes Item into SniperLauncher which, in turn, pushes it through to its
dependent types such as AuctionHouse and AuctionSniper. We ﬁx the compilation
errors and make all the tests pass again—except for the outstanding end-to-end
test which we have yet to implement.
We’ve now made explicit another concept in the domain. We realize that an
item’s identiﬁer is only one part of how a user bids in an auction. Now the code
can tell us exactly where decisions are made about bidding choices, so we don’t
have to follow a chain of method calls to see which strings are relevant.
Restraining the AuctionSniper
The last step to ﬁnish the task is to make the AuctionSniper observe the stop
price we’ve just passed to it and stop bidding. In practice, we can ensure that
we’ve covered everything by writing unit tests for each of the new state transitions
drawn in Figure 18.1. Our ﬁrst test triggers the Sniper to start bidding and then
announces a bid outside its limit—the stop price is set to 1234. We’ve also
extracted a common expectation into a helper method.1
@Test public void
doesNotBidAndReportsLosingIfSubsequentPriceIsAboveStopPrice() {
  allowingSniperBidding();
  context.checking(new Expectations() {{
    int bid = 123 + 45;
    allowing(auction).bid(bid);
    atLeast(1).of(sniperListener).sniperStateChanged(
                    new SniperSnapshot(ITEM_ID, 2345, bid, LOSING)); 
                                        when(sniperState.is("bidding"));
  }});
  sniper.currentPrice(123, 45, PriceSource.FromOtherBidder);
  sniper.currentPrice(2345, 25, PriceSource.FromOtherBidder);
}
private void allowingSniperBidding() {
  context.checking(new Expectations() {{ 
    allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING))); 
                                              then(sniperState.is("bidding"));
  }});
} 
1. jMock allows checking() to be called multiple times within a test.
Chapter 18
Filling In the Details
210


---
**Page 211**

Distinguishing between Test Setup and Assertions
Once again we’re using the allowing clause to distinguish between the test setup
(getting the AuctionSniper into the right state) and the signiﬁcant test assertion
(that the AuctionSniper is now losing). We’re very picky about this kind of
expressiveness because we’ve found it’s the only way for the tests to remain
meaningful, and therefore useful, over time.We return to this at length in Chapter 21
and Chapter 24.
The other tests are similar:
doesNotBidAndReportsLosingIfFirstPriceIsAboveStopPrice()
reportsLostIfAuctionClosesWhenLosing()
continuesToBeLosingOnceStopPriceHasBeenReached()
doesNotBidAndReportsLosingIfPriceAfterWinningIsAboveStopPrice()
We change AuctionSniper, with supporting features in SniperSnapshot and
Item, to make the test pass:
public class AuctionSniper { […]
  public void currentPrice(int price, int increment, PriceSource priceSource) {
    switch(priceSource) {
    case FromSniper:
      snapshot = snapshot.winning(price); 
      break;
    case FromOtherBidder:
      int bid = price + increment;
      if (item.allowsBid(bid)) {
        auction.bid(bid);
        snapshot = snapshot.bidding(price, bid);
} else {
        snapshot = snapshot.losing(price);
      }
      break;
    }
    notifyChange();
  } […]
public class SniperSnapshot { […]
  public SniperSnapshot losing(int newLastPrice) {
    return new SniperSnapshot(itemId, newLastPrice, lastBid, LOSING);
  } […]
public class Item { […]
  public boolean allowsBid(int bid) {
    return bid <= stopPrice;
  } […]
The end-to-end tests pass and we can cross the feature off our list, Figure 18.3.
211
Stop When We’ve Had Enough


---
**Page 212**

Figure 18.3
The Sniper stops bidding at the stop price
Observations
User Interfaces, Incrementally
It looks like we’re making signiﬁcant changes again to the user interface at a late
stage in our development. Shouldn’t we have seen this coming? This is an active
topic for discussion in the Agile User Experience community and, as always, the
answer is “it depends, but you have more ﬂexibility than you might think.”
In truth, for a simple application like this it would make sense to work out the
user interface in more detail at the start, to make sure it’s usable and coherent.
That said, we also wanted to make a point that we can respond to changing
needs, especially if we structure our tests and code so that they’re ﬂexible, not a
dead weight. We all know that requirements will change, especially once we put
our application into production, so we should be able to respond.
Other Modeling Techniques Still Work
Some presentations of TDD appear to suggest that it supersedes all previous
software design techniques. We think TDD works best when it’s based on skill
and judgment acquired from as wide an experience as possible—which includes
taking advantage of older techniques and formats (we hope we’re not being too
controversial here).
State transition diagrams are one example of taking another view. We regularly
come across teams that have never quite ﬁgured out what the valid states and
transitions are for key concepts in their domain, and applying this simple
Chapter 18
Filling In the Details
212


---
**Page 213**

formalism often means we can clean up a lucky-dip of snippets of behavior
scattered across the code. What’s nice about state transitions diagrams is that
they map directly onto tests, so we can show that we’ve covered all the
possibilities.
The trick is to understand and use other modeling techniques for support and
guidance, not as an end in themselves—which is how they got a bad name in the
ﬁrst place. When we’re doing TDD and we’re uncertain what to do, sometimes
stepping back and opening a pack of index cards, or sketching out the interactions,
can help us regain direction.
Domain Types Are Better Than Strings
The string is a stark data structure and everywhere it is passed there
is much duplication of process. It is a perfect vehicle for hiding
information.
—Alan Perlis
Looking back, we wish we’d created the Item type earlier, probably when we
extracted UserRequestListener, instead of just using a String to represent the
thing a Sniper bids for. Had we done so, we could have added the stop price to
the existing Item class, and it would have been delivered, by deﬁnition, to where
it was needed.
We might also have noticed sooner that we do not want to index our table on
item identiﬁer but on an Item, which would open up the possibility of trying
multiple policies in a single auction. We’re not saying that we should have de-
signed more speculatively for a need that hasn’t been proved. Rather, when we
take the trouble to express the domain clearly, we often ﬁnd that we have more
options.
It’s often better to deﬁne domain types to wrap not only Strings but other
built-in types too, including collections. All we have to do is remember to apply
our own advice. As you see, sometimes we forget.
213
Observations


---
**Page 214**

This page intentionally left blank 


