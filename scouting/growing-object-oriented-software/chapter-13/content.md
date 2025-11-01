# Chapter 13: The Sniper Makes a Bid (pp.123-138)

---
**Page 123**

Chapter 13
The Sniper Makes a Bid
In which we extract an AuctionSniper class and tease out its dependen-
cies. We plug our new class into the rest of the application, using an
empty implementation of auction until we’re ready to start sending
commands. We close the loop back to the auction house with an
XMPPAuction class. We continue to carve new types out of the code.
Introducing AuctionSniper
A New Class, with Dependencies
Our application accepts Price events from the auction, but cannot interpret them
yet. We need code that will perform two actions when the currentPrice() method
is called: send a higher bid to the auction and update the status in the user inter-
face. We could extend Main, but that class is looking rather messy—it’s already
doing too many things at once. It feels like this is a good time to introduce
what we should call an “Auction Sniper,” the component at the heart of our
application, so we create an AuctionSniper class. Some of its intended behavior
is currently buried in Main, and a good start would be to extract it into our new
class—although, as we’ll see in a moment, it will take a little effort.
Given that an AuctionSniper should respond to Price events, we decide to
make it implement AuctionEventListener rather than Main. The question is what
to do about the user interface. If we consider moving this method:
public void auctionClosed() {
  SwingUtilities.invokeLater(new Runnable() {
    public void run() {
       ui.showStatus(MainWindow.STATUS_LOST);
    }
  });
}
does it really make sense for an AuctionSniper to know about the implementation
details of the user interface, such as the use of the Swing thread? We’d be at risk
of breaking the “single responsibility” principle again. Surely an AuctionSniper
ought to be concerned with bidding policy and only notify status changes in
its terms?
123


---
**Page 124**

Our solution is to insulate the AuctionSniper by introducing a new relationship:
it will notify a SniperListener of changes in its status. The interface and the ﬁrst
unit test look like this:
public interface SniperListener extends EventListener {
  void sniperLost();
}
@RunWith(JMock.class)
public class AuctionSniperTest {
  private final Mockery context = new Mockery();
  private final SniperListener sniperListener = 
                                      context.mock(SniperListener.class);
  private final AuctionSniper sniper = new AuctionSniper(sniperListener);
  @Test public void
reportsLostWhenAuctionCloses() {
    context.checking(new Expectations() {{
      one(sniperListener).sniperLost();
    }});
    sniper.auctionClosed();
  }
}
which says that Sniper should report that it has lost if it receives a Close event
from the auction.
The failure report says:
not all expectations were satisfied
expectations:
! expected exactly 1 time, never invoked: SniperListener.sniperLost();
which we can make pass with a simple implementation:
public class AuctionSniper implements AuctionEventListener {
  private final SniperListener sniperListener;
  public AuctionSniper(SniperListener sniperListener) {
    this.sniperListener = sniperListener;
  }
public void auctionClosed() {
    sniperListener.sniperLost();
  }
  public void currentPrice(int price, int increment) {
// TODO Auto-generated method stub
  }
}
Finally, we retroﬁt the new AuctionSniper by having Main implement
SniperListener.
Chapter 13
The Sniper Makes a Bid
124


---
**Page 125**

public class Main implements SniperListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
    disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager().createChat(
        auctionId(itemId, connection), 
        new AuctionMessageTranslator(new AuctionSniper(this)));
    this.notToBeGCd = chat;
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
  public void sniperLost() {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        ui.showStatus(MainWindow.STATUS_LOST);
      }
    });
  }
}
Our working end-to-end test still passes and our broken one still fails at the
same place, so we haven’t made things worse. The new structure looks like
Figure 13.1.
Figure 13.1
Plugging in the AuctionSniper
Focus, Focus, Focus
Once again, we’ve noticed complexity in a class and used that to tease out a new
concept from our initial skeleton implementation. Now we have a Sniper to re-
spond to events from the translator. As you’ll see shortly, this is a better structure
for expressing what the code does and for unit testing. We also think that the
sniperLost() method is clearer than its previous incarnation, auctionClosed(),
since there’s now a closer match between its name and what it does—that is,
reports a lost auction.
Isn’t this wasteful ﬁddling, gold-plating the code while time slips by? Obviously
we don’t think so, especially when we’re sorting out our ideas this early in the
project. There are teams that overdo their design effort, but our experience is
that most teams spend too little time clarifying the code and pay for it in mainte-
nance overhead. As we’ve shown a couple of times now, the “single responsibil-
ity” principle is a very effective heuristic for breaking up complexity, and
125
Introducing AuctionSniper


---
**Page 126**

developers shouldn’t be shy about creating new types. We think Main still does
too much, but we’re not yet sure how best to break it up. We decide to push on
and see where the code takes us.
Sending a Bid
An Auction Interface
The next step is to have the Sniper send a bid to the auction, so who should the
Sniper talk to? Extending the SniperListener feels wrong because that relationship
is about tracking what’s happening in the Sniper, not about making external
commitments. In the terms deﬁned in “Object Peer Stereotypes” (page 52),
SniperListener is a notiﬁcation, not a dependency.
After the usual discussion, we decide to introduce a new collaborator, an
Auction. Auction and SniperListener represent two different domains in the
application: Auction is about ﬁnancial transactions, it accepts bids for items in
the market; and SniperListener is about feedback to the application, it reports
changes to the current state of the Sniper. The Auction is a dependency, for a
Sniper cannot function without one, whereas the SniperListener, as we
discussed above, is not. Introducing the new interface makes the design look like
Figure 13.2.
Figure 13.2
Introducing Auction
The AuctionSniper Bids
Now we’re ready to start bidding. The ﬁrst step is to implement the response to
a Price event, so we start by adding a new unit test for the AuctionSniper. It
says that the Sniper, when it receives a Price update, sends an incremented bid
to the auction. It also notiﬁes its listener that it’s now bidding, so we add a
sniperBidding() method. We’re making an implicit assumption that the Auction
knows which bidder the Sniper represents, so the Sniper does not have to pass
in that information with the bid.
Chapter 13
The Sniper Makes a Bid
126


---
**Page 127**

public class AuctionSniperTest {
private final Auction auction = context.mock(Auction.class);
  private final AuctionSniper sniper = 
                    new AuctionSniper(auction, sniperListener);
[…]
  @Test public void
bidsHigherAndReportsBiddingWhenNewPriceArrives() {
    final int price = 1001;
    final int increment = 25;
    context.checking(new Expectations() {{
      one(auction).bid(price + increment);
      atLeast(1).of(sniperListener).sniperBidding();
    }});
    sniper.currentPrice(price, increment);
  }
}
The failure report is:
not all expectations were satisfied
expectations:
  ! expected once, never invoked: auction.bid(<1026>)
  ! expected at least 1 time, never invoked: sniperListener.sniperBidding()
what happened before this: nothing!
When writing the test, we realized that we don’t actually care if the Sniper
notiﬁes the listener more than once that it’s bidding; it’s just a status update,
so we use an atLeast(1) clause for the listener’s expectation. On the other hand,
we do care that we send a bid exactly once, so we use a one() clause for its ex-
pectation. In practice, of course, we’ll probably only call the listener once, but
this loosening of the conditions in the test expresses our intent about the two
relationships. The test says that the listener is a more forgiving collaborator, in
terms of how it’s called, than the Auction. We also retroﬁt the atLeast(1) clause
to the other test method.
How Should We Describe Expected Values?
We’ve speciﬁed the expected bid value by adding the price and increment.There
are different opinions about whether test values should just be literals with “obvious”
values, or expressed in terms of the calculation they represent. Writing out the
calculation may make the test more readable but risks reimplementing the target
code in the test, and in some cases the calculation will be too complicated to repro-
duce. Here, we decide that the calculation is so trivial that we can just write it into
the test.
127
Sending a Bid


---
**Page 128**

jMock Expectations Don’t Need to Be Matched in Order
This is our ﬁrst test with more than one expectation, so we’ll point out that the order
in which expectations are declared does not have to match the order in which the
methods are called in the code. If the calling order does matter, the expectations
should include a sequence clause, which is described in Appendix A.
The implementation to make the test pass is simple.
public interface Auction {
  void bid(int amount);
}
public class AuctionSniper implements AuctionEventListener {  […]
  private final SniperListener sniperListener;
private final Auction auction;
  public AuctionSniper(Auction auction, SniperListener sniperListener) {
this.auction = auction;
    this.sniperListener = sniperListener;
  }
  public void currentPrice(int price, int increment) {
    auction.bid(price + increment);
    sniperListener.sniperBidding();
  }
}
Successfully Bidding with the AuctionSniper
Now we have to fold our new AuctionSniper back into the application. The easy
part is displaying the bidding status, the (slightly) harder part is sending the bid
back to the auction. Our ﬁrst job is to get the code through the compiler. We
implement the new sniperBidding() method on Main and, to avoid having
code that doesn’t compile for too long, we pass the AuctionSniper a null
implementation of Auction.
Chapter 13
The Sniper Makes a Bid
128


---
**Page 129**

public class Main implements SniperListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
Auction nullAuction = new Auction() {
      public void bid(int amount) {}
    };
    disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager().createChat(
        auctionId(itemId, connection), 
        new AuctionMessageTranslator(new AuctionSniper(nullAuction, this)));
    this.notToBeGCd = chat;
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
  public void sniperBidding() {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        ui.showStatus(MainWindow.STATUS_BIDDING);
      }
    });
  }
}
So, what goes in the Auction implementation? It needs access to the chat so it
can send a bid message. To create the chat we need a translator, the translator
needs a Sniper, and the Sniper needs an auction. We have a dependency loop
which we need to break.
Looking again at our design, there are a couple of places we could intervene,
but it turns out that the ChatManager API is misleading. It does not require a
MessageListener to create a Chat, even though the createChat() methods imply
that it does. In our terms, the MessageListener is a notiﬁcation; we can pass in
null when we create the Chat and add a MessageListener later.
Expressing Intent in API
We were only able to discover that we could pass null as a MessageListener
because we have the source code to the Smack library. This isn’t clear from the
API because, presumably, the authors wanted to enforce the right behavior and
it’s not clear why anyone would want a Chat without a listener. An alternative would
have been to provide equivalent creation methods that don’t take a listener, but
that would lead to API bloat. There isn’t an obvious best approach here, except to
note that including well-structured source code with the distribution makes libraries
much easier to work with.
129
Sending a Bid


---
**Page 130**

Now we can restructure our connection code and use the Chat to send back
a bid.
public class Main implements SniperListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
    disconnectWhenUICloses(connection);
    final Chat chat = 
      connection.getChatManager().createChat(auctionId(itemId, connection), null);
    this.notToBeGCd = chat;
    Auction auction = new Auction() {
      public void bid(int amount) {
        try {
          chat.sendMessage(String.format(BID_COMMAND_FORMAT, amount));
        } catch (XMPPException e) {
          e.printStackTrace();
        }
      }
    };
    chat.addMessageListener(
           new AuctionMessageTranslator(new AuctionSniper(auction, this)));
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
}
Null Implementation
A null implementation is similar to a null object [Woolf98]: both are implementations
that respond to a protocol by not doing anything—but the intention is different. A
null object is usually one implementation amongst many, introduced to reduce
complexity in the code that calls the protocol. We deﬁne a null implementation as
a temporary empty implementation, introduced to allow the programmer to make
progress by deferring effort and intended to be replaced.
The End-to-End Tests Pass
Now the end-to-end tests pass: the Sniper can lose without making a bid, and
lose after making a bid. We can cross off another item on the to-do list, but that
includes just catching and printing the XMPPException. Normally, we regard this
as a very bad practice but we wanted to see the tests pass and get some structure
into the code—and we know that the end-to-end tests will fail anyway if there’s
a problem sending a message. To make sure we don’t forget, we add another
to-do item to ﬁnd a better solution, Figure 13.3.
Chapter 13
The Sniper Makes a Bid
130


---
**Page 131**

Figure 13.3
One step forward
Tidying Up the Implementation
Extracting XMPPAuction
Our end-to-end test passes, but we haven’t ﬁnished because our new implemen-
tation feels messy. We notice that the activity in joinAuction() crosses multiple
domains: managing chats, sending bids, creating snipers, and so on. We need to
clean up. To start, we notice that we’re sending auction commands from two
different levels, at the top and from within the Auction. Sending commands to
an auction sounds like the sort of thing that our Auction object should do, so it
makes sense to package that up together. We add a new method to the interface,
extend our anonymous implementation, and then extract it to a (temporarily)
nested class—for which we need a name. The distinguishing feature of this imple-
mentation of Auction is that it’s based on the messaging infrastructure, so we
call our new class XMPPAuction.
131
Tidying Up the Implementation


---
**Page 132**

public class Main implements SniperListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) {
    disconnectWhenUICloses(connection);
    final Chat chat = 
      connection.getChatManager().createChat(auctionId(itemId, connection), 
                                             null);
    this.notToBeGCd = chat;
    Auction auction = new XMPPAuction(chat);
    chat.addMessageListener(
        new AuctionMessageTranslator(new AuctionSniper(auction, this)));
auction.join();
  }
  public static class XMPPAuction implements Auction {
    private final Chat chat;
    public XMPPAuction(Chat chat) {
      this.chat = chat;
    }
    public void bid(int amount) {
      sendMessage(format(BID_COMMAND_FORMAT, amount));
    }
    public void join() {
      sendMessage(JOIN_COMMAND_FORMAT);
    }
    private void sendMessage(final String message) {
      try {
        chat.sendMessage(message);
      } catch (XMPPException e) {
        e.printStackTrace();
      }
    }
  }
}
We’re starting to see a clearer model of the domain. The line auction.join()
expresses our intent more clearly than the previous detailed implementation of
sending a string to a chat. The new design looks like Figure 13.4  and we promote
XMPPAuction to be a top-level class.
We still think joinAuction() is unclear, and we’d like to pull the XMPP-related
detail out of Main, but we’re not ready to do that yet. Another point to keep
in mind.
Chapter 13
The Sniper Makes a Bid
132


---
**Page 133**

Figure 13.4
Closing the loop with an XMPPAuction
Extracting the User Interface
The other activity in Main is implementing the user interface and showing the
current state in response to events from the Sniper. We’re not really happy that
Main implements SniperListener; again, it feels like mixing different responsibil-
ities (starting the application and responding to events). We decide to extract the
SniperListener behavior into a nested helper class, for which the best name we
can ﬁnd is SniperStateDisplayer. This new class is our bridge between two do-
mains: it translates Sniper events into a representation that Swing can display,
which includes dealing with Swing threading. We plug an instance of the new
class into the AuctionSniper.
public class Main { // doesn't implement SniperListener
  private MainWindow ui;
  private void joinAuction(XMPPConnection connection, String itemId) {
    disconnectWhenUICloses(connection);
    final Chat chat = 
      connection.getChatManager().createChat(auctionId(itemId, connection), null);
    this.notToBeGCd = chat;
    Auction auction = new XMPPAuction(chat);
    chat.addMessageListener(
        new AuctionMessageTranslator(
            connection.getUser(),
            new AuctionSniper(auction, new SniperStateDisplayer())));
    auction.join();
  }
[…]
133
Tidying Up the Implementation


---
**Page 134**

  public class SniperStateDisplayer implements SniperListener {
    public void sniperBidding() {
      showStatus(MainWindow.STATUS_BIDDING);
    }
    public void sniperLost() {
      showStatus(MainWindow.STATUS_LOST);
    }
    public void sniperWinning() {
      showStatus(MainWindow.STATUS_WINNING);
    }
    private void showStatus(final String status) {
      SwingUtilities.invokeLater(new Runnable() {
        public void run() { ui.showStatus(status); } 
      });
    }
  }
}
Figure 13.5 shows how we’ve reduced Main so much that it no longer partici-
pates in the running application (for clarity, we’ve left out the WindowAdapter
that closes the connection). It has one job which is to create the various compo-
nents and introduce them to each other. We’ve marked MainWindow as external,
even though it’s one of ours, to represent the Swing framework.
Figure 13.5
Extracting SniperStateDisplayer
Chapter 13
The Sniper Makes a Bid
134


---
**Page 135**

Tidying Up the Translator
Finally, 
we 
fulﬁll 
our 
promise 
to 
ourselves 
and 
return 
to 
the
AuctionMessageTranslator. We start trying to reduce the noise by adding
constants and static imports, with some helper methods to reduce duplication.
Then we realize that much of the code is about manipulating the map of
name/value pairs and is rather procedural. We can do a better job by extracting
an inner class, AuctionEvent, to encapsulate the unpacking of the message con-
tents. We have conﬁdence that we can refactor the class safely because it’s
protected by its unit tests.
public class AuctionMessageTranslator implements MessageListener { 
  private final AuctionEventListener listener;
  public AuctionMessageTranslator(AuctionEventListener listener) {
    this.listener = listener;
  }
  public void processMessage(Chat chat, Message message) { 
AuctionEvent event = AuctionEvent.from(message.getBody());
    String eventType = event.type();
    if ("CLOSE".equals(eventType)) { 
      listener.auctionClosed(); 
    } if ("PRICE".equals(eventType)) { 
      listener.currentPrice(event.currentPrice(), event.increment()); 
    } 
  }
  private static class AuctionEvent {
    private final Map<String, String> fields = new HashMap<String, String>();  
    public String type() { return get("Event"); }
    public int currentPrice() { return getInt("CurrentPrice"); }
    public int increment() { return getInt("Increment"); }
    private int getInt(String fieldName) {
      return Integer.parseInt(get(fieldName));
    }
    private String get(String fieldName) { return fields.get(fieldName); }
    private void addField(String field) {
      String[] pair = field.split(":");
      fields.put(pair[0].trim(), pair[1].trim());
    }
    static AuctionEvent from(String messageBody) {
      AuctionEvent event = new AuctionEvent();
      for (String field : fieldsIn(messageBody)) {
        event.addField(field);
      }
      return event;
    }
    static String[] fieldsIn(String messageBody) {
      return messageBody.split(";");
    }
  }
}
135
Tidying Up the Implementation


---
**Page 136**

This is an example of “breaking out” that we described in “Value Types”
(page 59). It may not be obvious, but AuctionEvent is a value: it’s
immutable and there are no interesting differences between two instances
with the same contents. This refactoring separates the concerns within
AuctionMessageTranslator: the top level deals with events and listeners, and
the inner object deals with parsing strings.
Encapsulate Collections
We’ve developed a habit of packaging up common types, such as collections, in
our own classes, even though Java generics avoid the need to cast objects. We’re
trying to use the language of the problem we’re working on, rather than the language
of Java constructs. In our two versions of processMessage(), the ﬁrst has lots of
incidental noise about looking up and parsing values.The second is written in terms
of auction events, so there’s less of a conceptual gap between the domain and
the code.
Our rule of thumb is that we try to limit passing around types with generics (the
types enclosed in angle brackets). Particularly when applied to collections, we view
it as a form of duplication. It’s a hint that there’s a domain concept that should be
extracted into a type.
Defer Decisions
There’s a technique we’ve used a couple of times now, which is to introduce a
null implementation of a method (or even a type) to get us through the next step.
This helps us focus on the immediate task without getting dragged into thinking
about the next signiﬁcant chunk of functionality. The null Auction, for example,
allowed us to plug in a new relationship we’d discovered in a unit test without
getting pulled into messaging issues. That, in turn, meant we could stop and
think about the dependencies between our objects without the pressure of having
a broken compilation.
Keep the Code Compiling
We try to minimize the time when we have code that does not compile by keeping
changes incremental. When we have compilation failures, we can’t be quite sure
where the boundaries of our changes are, since the compiler can’t tell us. This, in
turn, means that we can’t check in to our source repository, which we like to do
often.The more code we have open, the more we have to keep in our heads which,
ironically, usually means we move more slowly. One of the great discoveries of
test-driven development is just how ﬁne-grained our development steps can be.
Chapter 13
The Sniper Makes a Bid
136


---
**Page 137**

Emergent Design
What we hope is becoming clear from this chapter is how we’re growing a design
from what looks like an unpromising start. We alternate, more or less, between
adding features and reﬂecting on—and cleaning up—the code that results. The
cleaning up stage is essential, since without it we would end up with an unmain-
tainable mess. We’re prepared to defer refactoring code if we’re not yet clear
what to do, conﬁdent that we will take the time when we’re ready. In the mean-
time, we keep our code as clean as possible, moving in small increments and using
techniques such as null implementation to minimize the time when it’s broken.
Figure 13.5 shows that we’re building up a layer around our core implementa-
tion that “protects” it from its external dependencies. We think this is just good
practice, but what’s interesting is that we’re getting there incrementally, by
looking for features in classes that either go together or don’t. Of course we’re
inﬂuenced by our experience of working on similar codebases, but we’re trying
hard to follow what the code is telling us instead of imposing our preconceptions.
Sometimes, when we do this, we ﬁnd that the domain takes us in the most
surprising directions.
137
Emergent Design


---
**Page 138**

This page intentionally left blank 


