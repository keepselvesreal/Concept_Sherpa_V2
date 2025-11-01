# Chapter 12: Getting Ready to Bid (pp.105-122)

---
**Page 105**

Chapter 12
Getting Ready to Bid
In which we write an end-to-end test so that we can make the Sniper
bid in an auction. We start to interpret the messages in the auction
protocol and discover some new classes in the process. We write our
ﬁrst unit tests and then refactor out a helper class. We describe every
last detail of this effort to show what we were thinking at the time.
An Introduction to the Market
Now, to continue with the skeleton metaphor, we start to ﬂesh out the application.
The core behavior of a Sniper is that it makes a higher bid on an item in an auction
when there’s a change in price. Going back to our to-do list, we revisit the next
couple of items:
•
Single item: join, bid, and lose. When a price comes in, send a bid raised
by the minimum increment deﬁned by the auction. This amount will be
included in the price update information.
•
Single item: join, bid, and win. Distinguish which bidder is currently winning
the auction and don’t bid against ourselves.
We know there’ll be more coming, but this is a coherent slice of functionality
that will allow us to explore the design and show concrete progress.
In any distributed system similar to this one there are lots of interesting failure
and timing issues, but our application only has to deal with the client side of the
protocol. We rely on the underlying XMPP protocol to deal with many common
distributed programming problems; in particular, we expect it to ensure that
messages between a bidder and an auction arrive in the same order in which they
were sent.
As we described in Chapter 5, we start the next feature with an acceptance
test. We used our ﬁrst test in the previous chapter to help ﬂush out the structure
of our application. From now on, we can use acceptance tests to show incremental
progress.
105


---
**Page 106**

A Test for Bidding
Starting with a Test
Each acceptance test we write should have just enough new requirements to force
a manageable increase in functionality, so we decide that the next one will add
some price information. The steps are:
1.
Tell the auction to send a price to the Sniper.
2.
Check the Sniper has received and responded to the price.
3.
Check the auction has received an incremented bid from Sniper.
To make this pass, the Sniper will have to distinguish between Price and Close
events from the auction, display the current price, and generate a new bid. We’ll
also have to extend our stub auction to handle bids. We’ve deferred implementing
other functionality that will also be required, such as displaying when the Sniper
has won the auction; we’ll get to that later. Here’s the new test:
public class AuctionSniperEndToEndTest {
  @Test public void
sniperMakesAHigherBidButLoses() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
    auction.hasReceivedJoinRequestFromSniper(); 1
    auction.reportPrice(1000, 98, "other bidder"); 2
    application.hasShownSniperIsBidding(); 3
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID); 4
    auction.announceClosed(); 5
    application.showsSniperHasLostAuction();   
  }
}
We have three new methods to implement as part of this test.
1
We have to wait for the stub auction to receive the Join request before con-
tinuing with the test. We use this assertion to synchronize the Sniper with
the auction.
2
This method tells the stub auction to send a message back to the Sniper with
the news that at the moment the price of the item is 1000, the increment for
the next bid is 98, and the winning bidder is “other bidder.”
3
This method asks the ApplicationRunner to check that the Sniper shows that
it’s now bidding after it’s received the price update message from the auction.
Chapter 12
Getting Ready to Bid
106


---
**Page 107**

4
This method asks the stub auction to check that it has received a bid from
the Sniper that is equal to the last price plus the minimum increment. We
have to do a fraction more work because the XMPP layer constructs a longer
name from the basic identiﬁer, so we deﬁne a constant SNIPER_XMPP_ID which
in practice is sniper@localhost/Auction.
5
We reuse the closing logic from the ﬁrst test, as the Sniper still loses the
auction.
Unrealistic Money
We’re using integers to represent value (imagine that auctions are conducted in
Japanese Yen). In a real system, we would deﬁne a domain type to represent
monetary values, using a ﬁxed decimal implementation. Here, we simplify the
representation to make the example code easier to ﬁt onto a printed page.
Extending the Fake Auction
We have two methods to write in the FakeAuctionServer to support the end-
to-end test: reportPrice() has to send a Price message through the chat;
hasReceivedBid() is a little more complex—it has to check that the auction re-
ceived the right values from the Sniper. Instead of parsing the incoming message,
we construct the expected message and just compare strings. We also pull up the
Matcher clause from the SingleMessageListener to give the FakeAuctionServer
more ﬂexibility in deﬁning what it will accept as a message. Here’s a ﬁrst cut:
public class FakeAuctionServer { […]
  public void reportPrice(int price, int increment, String bidder) 
    throws XMPPException 
  {
    currentChat.sendMessage(
        String.format("SOLVersion: 1.1; Event: PRICE; "
                      + "CurrentPrice: %d; Increment: %d; Bidder: %s;",
                      price, increment, bidder));
  }
  public void hasReceivedJoinRequestFromSniper() throws InterruptedException {
    messageListener.receivesAMessage(is(anything()));
  }
  public void hasReceivedBid(int bid, String sniperId) 
    throws InterruptedException 
  {
    assertThat(currentChat.getParticipant(), equalTo(sniperId));
    messageListener.receivesAMessage(
      equalTo(
        String.format("SOLVersion: 1.1; Command: BID; Price: %d;", bid)));
  }
}
107
A Test for Bidding


---
**Page 108**

public class SingleMessageListener implements MessageListener { […]
  @SuppressWarnings("unchecked")
  public void receivesAMessage(Matcher<? super String> messageMatcher) 
    throws InterruptedException 
  {
    final Message message = messages.poll(5, TimeUnit.SECONDS);
    assertThat("Message", message, is(notNullValue()));
    assertThat(message.getBody(), messageMatcher);
  }
}
Looking again, there’s an imbalance between the two “receives” methods. The
Join method is much more lax than the bid message, in terms of both the contents
of the message and the sender; we will have to remember to come back later and
ﬁx it. We defer a great many decisions when developing incrementally, but
sometimes consistency and symmetry make more sense. We decide to retroﬁt
more detail into hasReceivedJoinRequestFromSniper() while we have the code
cracked open. We also extract the message formats and move them to Main
because we’ll need them to construct raw messages in the Sniper.
public class FakeAuctionServer { […]
  public void hasReceivedJoinRequestFrom(String sniperId) 
    throws InterruptedException 
  {
receivesAMessageMatching(sniperId, equalTo(Main.JOIN_COMMAND_FORMAT));
  }
  public void hasReceivedBid(int bid, String sniperId) 
    throws InterruptedException 
  {
receivesAMessageMatching(sniperId, 
                             equalTo(format(Main.BID_COMMAND_FORMAT, bid)));
  }
  private void receivesAMessageMatching(String sniperId, 
                                        Matcher<? super String> messageMatcher)
    throws InterruptedException 
  {
    messageListener.receivesAMessage(messageMatcher);
    assertThat(currentChat.getParticipant(), equalTo(sniperId));
  }
}
Notice that we check the Sniper’s identiﬁer after we check the contents of the
message. This forces the server to wait until the message has arrived, which means
that it must have accepted a connection and set up currentChat. Otherwise the
test would fail by checking the Sniper’s identiﬁer prematurely.
Chapter 12
Getting Ready to Bid
108


---
**Page 109**

Double-Entry Values
We’re using the same constant to both create a Join message and check its con-
tents. By using the same construct, we’re removing duplication and expressing in
the code a link between the two sides of the system. On the other hand, we’re
making ourselves vulnerable to getting them both wrong and not having a test to
catch the invalid content. In this case, the code is so simple that pretty much any
implementation would do, but the answers become less certain when developing
something more complex, such as a persistence layer. Do we use the same
framework to write and read our values? Can we be sure that it’s not just caching
the results, or that the values are persisted correctly? Should we just write some
straight database queries to be sure?
The critical question is, what do we think we’re testing? Here, we think that the
communication features are more important, that the messages are simple enough
so we can rely on string constants, and that we’d like to be able to ﬁnd code related
to message formats in the IDE. Other developers might come to a different
conclusion and be right for their project.
We adjust the end-to-end tests to match the new API, watch the test fail, and
then add the extra detail to the Sniper to make the test pass.
public class AuctionSniperEndToEndTest {
  @Test public void
sniperMakesAHigherBidButLoses() throws Exception {
    auction.startSellingItem();
    application.startBiddingIn(auction);
auction.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
    auction.reportPrice(1000, 98, "other bidder");
    application.hasShownSniperIsBidding();
    auction.hasReceivedBid(1098, ApplicationRunner.SNIPER_XMPP_ID);
    auction.announceClosed();                  
    application.showsSniperHasLostAuction();   
  }
}
109
A Test for Bidding


---
**Page 110**

public class Main { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
    Chat chat = connection.getChatManager().createChat(
        auctionId(itemId, connection), 
        new MessageListener() {
          public void processMessage(Chat aChat, Message message) {
            SwingUtilities.invokeLater(new Runnable() {
              public void run() {
                ui.showStatus(MainWindow.STATUS_LOST);
              }
            });
          }
        });
    this.notToBeGCd = chat;
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
}
A Surprise Failure
Finally we write the “checking” method on the ApplicationRunner to give us
our ﬁrst failure. The implementation is simple: we just add another status constant
and copy the existing method.
public class ApplicationRunner { […]
public void hasShownSniperIsBidding() {
    driver.showsSniperStatus(MainWindow.STATUS_BIDDING);
  }
  public void showsSniperHasLostAuction() {
    driver.showsSniperStatus(MainWindow.STATUS_LOST);
  }
}
We’re expecting to see something about a missing label text but instead we
get this:
java.lang.AssertionError: 
Expected: is not null
     got: null
[…]
  at auctionsniper.SingleMessageListener.receivesAMessage()
  at auctionsniper.FakeAuctionServer.hasReceivedJoinRequestFromSniper()
  at auctionsniper.AuctionSniperEndToEndTest.sniperMakesAHigherBid()
[…]
and this on the error stream:
Chapter 12
Getting Ready to Bid
110


---
**Page 111**

conflict(409)
  at jivesoftware.smack.SASLAuthentication.bindResourceAndEstablishSession()
  at jivesoftware.smack.SASLAuthentication.authenticate()
  at jivesoftware.smack.XMPPConnection.login()
  at jivesoftware.smack.XMPPConnection.login()
  at auctionsniper.Main.connection()
  at auctionsniper.Main.main()
After some investigation we realize what’s happened. We’ve introduced a second
test which tries to connect using the same account and resource name as the ﬁrst.
The server is conﬁgured, like Southabee’s On-Line, to reject multiple open con-
nections, so the second test fails because the server thinks that the ﬁrst is still
connected. In production, our application would work because we’d stop the
whole process when closing, which would break the connection. Our little com-
promise (of starting the application in a new thread) has caught us out. The Right
Thing to do here is to add a callback to disconnect the client when we close the
window so that the application will clean up after itself:
public class Main { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager().createChat(
[…]
    chat.sendMessage(JOIN_COMMAND_FORMAT);
  }
  private void disconnectWhenUICloses(final XMPPConnection connection) {
    ui.addWindowListener(new WindowAdapter() {
      @Override public void windowClosed(WindowEvent e) {
connection.disconnect();
      }
    });
  }
}
Now we get the failure we expected, because the Sniper has no way to start
bidding.
java.lang.AssertionError: 
Tried to look for...
    exactly 1 JLabel (with name "sniper status")
    in exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    in all top level windows
and check that its label text is "Bidding"
but...
    all top level windows
    contained 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    contained 1 JLabel (with name "sniper status")
label text was "Lost"
[…]
  at auctionsniper.AuctionSniperDriver.showsSniperStatus()
  at auctionsniper.ApplicationRunner.hasShownSniperIsBidding()
  at auctionsniper.AuctionSniperEndToEndTest.sniperMakesAHigherBidButLoses()
111
A Test for Bidding


---
**Page 112**

Outside-In Development
This failure deﬁnes the target for our next coding episode. It tells us, at a high
level, what we’re aiming for—we just have to ﬁll in implementation until it
passes.
Our approach to test-driven development is to start with the outside event that
triggers the behavior we want to implement and work our way into the code an
object at a time, until we reach a visible effect (such as a sent message or log entry)
indicating that we’ve achieved our goal. The end-to-end test shows us the end
points of that process, so we can explore our way through the space in the middle.
In the following sections, we build up the types we need to implement our
Auction Sniper. We’ll take it slowly, strictly by the TDD rules, to show how the
process works. In real projects, we sometimes design a bit further ahead to get
a sense of the bigger picture, but much of the time this is what we actually do.
It produces the right results and forces us to ask the right questions.
Inﬁnite Attention to Detail?
We caught the resource clash because, by luck or insight, our server conﬁguration
matched that of Southabee’s On-Line. We might have used an alternative setting
which allows new connections to kick off existing ones, which would have resulted
in the tests passing but with a confusing conﬂict message from the Smack library
on the error stream. This would have worked ﬁne in development, but with a
risk of Snipers starting to fail in production.
How can we hope to catch all the conﬁguration options in an entire system?
At some level we can’t, and this is at the heart of what professional testers do.
What we can do is push to exercise as much as possible of the system as early as
possible, and to do so repeatedly. We can also help ourselves cope with total
system complexity by keeping the quality of its components high and by constantly
pushing to simplify. If that sounds expensive, consider the cost of ﬁnding and
ﬁxing a transient bug like this one in a busy production system.
The AuctionMessageTranslator
Teasing Out a New Class
Our entry point to the Sniper is where we receive a message from the auction
through the Smack library: it’s the event that triggers the next round of behavior
we want to make work. In practice, this means that we need a class implementing
MessageListener to attach to the Chat. When this class receives a raw message
from the auction, it will translate it into something that represents an auction
event within our code which, eventually, will prompt a Sniper action and a change
in the user interface.
Chapter 12
Getting Ready to Bid
112


---
**Page 113**

We already have such a class in Main—it’s anonymous and its responsibilities
aren’t very obvious:
new MessageListener() {
  public void processMessage(Chat aChat, Message message) {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        ui.showStatus(MainWindow.STATUS_LOST);
      }
    });
  }
}
This code implicitly accepts a Close message (the only kind of message we
have so far) and implements the Sniper’s response. We’d like to make this situation
explicit before we add more features. We start by promoting the anonymous
class to a top-level class in its own right, which means it needs a name. From our
description in the paragraph above, we pick up the word “translate” and call it
an AuctionMessageTranslator, because it will translate messages from the auction.
The catch is that the current anonymous class picks up the ui ﬁeld from Main.
We’ll have to attach something to our newly promoted class so that it can respond
to a message. The most obvious thing to do is pass it the MainWindow but we’re
unhappy about creating a dependency on a user interface component. That would
make it hard to unit-test, because we’d have to query the state of a component
that’s running in the Swing event thread.
More signiﬁcantly, such a dependency would break the “single responsibility”
principle which says that unpacking raw messages from the auction is quite
enough for one class to do, without also having to know how to present the
Sniper status. As we wrote in “Designing for Maintainability” (page 47), we
want to maintain a separation of concerns.
Given these constraints, we decide that our new AuctionMessageTranslator
will delegate the handling of an interpreted event to a collaborator, which we will
represent with an AuctionEventListener interface; we can pass an object that
implements it into the translator on construction. We don’t yet know what’s in
this interface and we haven’t yet begun to think about its implementation. Our
immediate concern is to get the message translation to work; the rest can wait.
So far the design looks like Figure 12.1 (types that belong to external frameworks,
such as Chat, are shaded):
Figure 12.1
The AuctionMessageTranslator
113
The AuctionMessageTranslator


---
**Page 114**

The First Unit Test
We start with the simpler event type. As we’ve seen, a Close event has no
values—it’s a simple trigger. When the translator receives one, we want it to call
its listener appropriately.
As this is our ﬁrst unit test, we’ll build it up very slowly to show the process
(later, we will move faster). We start with the test method name. JUnit picks up
test methods by reﬂection, so we can make their names as long and descriptive
as we like because we never have to include them in code. The ﬁrst test says that
the translator will tell anything that’s listening that the auction has closed when
it receives a raw Close message.
package test.auctionsniper;
public class AuctionMessageTranslatorTest {
  @Test public void
notifiesAuctionClosedWhenCloseMessageReceived() {
// nothing yet
  }
}
Put Tests in a Different Package
We’ve adopted a habit of putting tests in a different package from the code they’re
exercising.We want to make sure we’re driving the code through its public interfaces,
like any other client, rather than opening up a package-scoped back door for testing.
We also ﬁnd that, as the application and test code grows, separate packages make
navigation in modern IDEs easier.
The next step is to add the action that will trigger the behavior we want to
test—in this case, sending a Close message. We already know what this will look
like since it’s a call to the Smack MessageListener interface.
public class AuctionMessageTranslatorTest {
  public static final Chat UNUSED_CHAT = null;
private final AuctionMessageTranslator translator = 
                                              new AuctionMessageTranslator();
  @Test public void
notfiesAuctionClosedWhenCloseMessageReceived() {
Message message = new Message();
    message.setBody("SOLVersion: 1.1; Event: CLOSE;");
    translator.processMessage(UNUSED_CHAT, message);
  }
}
Chapter 12
Getting Ready to Bid
114


---
**Page 115**

Use null When an Argument Doesn’t Matter
UNUSED_CHAT is a meaningful name for a constant that is deﬁned as null.We pass
it into processMessage() instead of a real Chat object because the Chat class is
difﬁcult to instantiate—its constructor is package-scoped and we’d have to ﬁll in a
chain of dependencies to create one. As it happens, we don’t need one anyway
for the current functionality, so we just pass in a null value to satisfy the compiler
but use a named constant to make clear its signiﬁcance.
To be clear, this null is not a null object [Woolf98] which may be called and will
do nothing in response. This null is just a placeholder and will fail if called during
the test.
We generate a skeleton implementation from the MessageListener interface.
package auctionsniper;
public class AuctionMessageTranslator implements MessageListener {
  public void processMessage(Chat chat, Message message) {
// TODO Fill in here
  }
}
Next, we want a check that shows whether the translation has taken
place—which should fail since we haven’t implemented anything yet. We’ve al-
ready decided that we want our translator to notify its listener when the Close
event occurs, so we’ll describe that expected behavior in our test.
@RunWith(JMock.class) 
public class AuctionMessageTranslatorTest {
  private final Mockery context = new Mockery();
  private final AuctionEventListener listener = 
                              context.mock(AuctionEventListener.class); 
  private final AuctionMessageTranslator translator = 
                                        new AuctionMessageTranslator();
  @Test public void
notfiesAuctionClosedWhenCloseMessageReceived() {
    context.checking(new Expectations() {{
oneOf(listener).auctionClosed();
    }});
    Message message = new Message();
    message.setBody("SOLVersion: 1.1; Event: CLOSE;");
    translator.processMessage(UNUSED_CHAT, message);
  }
}
115
The AuctionMessageTranslator


---
**Page 116**

This is more or less the kind of unit test we described at the end of Chapter 2,
so we won’t go over its structure again here except to emphasize the highlighted
expectation line. This is the most signiﬁcant line in the test, our declaration of
what matters about the translator’s effect on its environment. It says that when
we send an appropriate message to the translator, we expect it to call the listener’s
auctionClosed() method exactly once.
We get a failure that shows that we haven’t implemented the behavior we need:
not all expectations were satisfied
expectations:
  ! expected once, never invoked: auctionEventListener.auctionClosed()
what happened before this: nothing!
  at org.jmock.Mockery.assertIsSatisfied(Mockery.java:199)
  […]
  at org.junit.internal.runners.JUnit4ClassRunner.run()
The critical phrase is this one:
expected once, never invoked: auctionEventListener.auctionClosed()
which tells us that we haven’t called the listener as we should have.
We need to do two things to make the test pass. First, we need to connect the
translator and listener so that they can communicate. We decide to pass the lis-
tener into the translator’s constructor; it’s simple and ensures that the translator
is always set up correctly with a listener—the Java type system won’t let us forget.
The test setup looks like this:
public class AuctionMessageTranslatorTest {
  private final Mockery context = new Mockery();
  private final AuctionEventListener listener = 
                                     context.mock(AuctionEventListener.class);
  private final AuctionMessageTranslator translator = 
                                       new AuctionMessageTranslator(listener);
The second thing we need to do is call the auctionClosed() method. Actually,
that’s all we need to do to make this test pass, since we haven’t deﬁned any other
behavior.
public void processMessage(Chat chat, Message message) {
    listener.auctionClosed();
  }
The test passes. This might feel like cheating since we haven’t actually unpacked
a message. What we have done is ﬁgured out where the pieces are and got them
into a test harness—and locked down one piece of functionality that should
continue to work as we add more features.
Chapter 12
Getting Ready to Bid
116


---
**Page 117**

Simpliﬁed Test Setup
You might have noticed that all the ﬁelds in the test class are final. As we described
in Chapter 3, JUnit creates a new instance of the test class for each test method,
so the ﬁelds are recreated for each test method. We exploit this by declaring as
many ﬁelds as possible as final and initializing them during construction, which
ﬂushes out any circular dependencies. Steve likes to think of this visually as creating
a lattice of objects that acts a frame to support the test.
Sometimes, as you’ll see later in this example, we can’t lock everything down and
have to attach a dependency directly, but most of the time we can. Any exceptions
will attract our attention and highlight a possible dependency loop. NUnit, on the
other hand, reuses the same instance of the test class, so in that case we’d have
to renew any supporting test values and objects explicitly.
Closing the User Interface Loop
Now we have the beginnings of our new component, we can retroﬁt it into
the Sniper to make sure we don’t drift too far from working code. Previously,
Main updated the Sniper user interface, so now we make it implement
AuctionEventListener and move the functionality to the new auctionClosed()
method.
public class Main implements AuctionEventListener { […]
  private void joinAuction(XMPPConnection connection, String itemId) 
    throws XMPPException 
  {
    disconnectWhenUICloses(connection);
    Chat chat = connection.getChatManager().createChat(
        auctionId(itemId, connection), 
new AuctionMessageTranslator(this));
    chat.sendMessage(JOIN_COMMAND_FORMAT);
    notToBeGCd = chat; 
  }
  public void auctionClosed() {
    SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        ui.showStatus(MainWindow.STATUS_LOST);
      }
    });
  }
}
The structure now looks like Figure 12.2.
117
The AuctionMessageTranslator


---
**Page 118**

Figure 12.2
Introducing the AuctionMessageTranslator
What Have We Achieved?
In this baby step, we’ve extracted a single feature of our application into a separate
class, which means the functionality now has a name and can be unit-tested.
We’ve also made Main a little simpler, now that it’s no longer concerned with
interpreting the text of messages from the auction. This is not yet a big deal but
we will show, as the Sniper application grows, how this approach helps us keep
code clean and ﬂexible, with clear responsibilities and relationships between its
components.
Unpacking a Price Message
Introducing Message Event Types
We’re about to introduce a second auction message type, the current price update.
The Sniper needs to distinguish between the two, so we take another look at the
message formats in Chapter 9 that Southabee’s On-Line have sent us. They’re
simple—just a single line with a few name/value pairs. Here are examples for
the formats again:
SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
SOLVersion: 1.1; Event: CLOSE;
At ﬁrst, being object-oriented enthusiasts, we try to model these messages as
types, but we’re not clear enough about the behavior to justify any meaningful
structure, so we back off the idea. We decide to start with a simplistic solution
and adapt from there.
The Second Test
The introduction of a different Price event in our second test will force us to
parse the incoming message. This test has the same structure as the ﬁrst one but
gets a different input string and expects us to call a different method on the lis-
tener. A Price message includes details of the last bid, which we need to unpack
and pass to the listener, so we include them in the signature of the new method
currentPrice(). Here’s the test:
@Test public void
notifiesBidDetailsWhenCurrentPriceMessageReceived() {
Chapter 12
Getting Ready to Bid
118


---
**Page 119**

  context.checking(new Expectations() {{
exactly(1).of(listener).currentPrice(192, 7);
  }});
  Message message = new Message();
    message.setBody(
"SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;"
                   );
  translator.processMessage(UNUSED_CHAT, message);
}
To get through the compiler, we add a method to the listener; this takes just
a keystroke in the IDE:1
public interface AuctionEventListener {
  void auctionClosed();
void currentPrice(int price, int increment);
}
The test fails.
unexpected invocation: auctionEventListener.auctionClosed()
expectations:
  ! expected once, never invoked: auctionEventListener.currentPrice(<192>, <7>)
what happened before this: nothing!
[…]
  at $Proxy6.auctionClosed()
  at auctionsniper.AuctionMessageTranslator.processMessage()
  at AuctionMessageTranslatorTest.translatesPriceMessagesAsAuctionPriceEvents()
[…]
  at JUnit4ClassRunner.run(JUnit4ClassRunner.java:42)
This time the critical phrase is:
unexpected invocation: auctionEventListener.auctionClosed()
which means that the code called the wrong method, auctionClosed(), during
the test. The Mockery isn’t expecting this call so it fails immediately, showing us
in the stack trace the line that triggered the failure (you can see the workings of
the Mockery in the line $Proxy6.auctionClosed() which is the runtime substitute
for a real AuctionEventListener). Here, the place where the code failed is obvious,
so we can just ﬁx it.
Our ﬁrst version is rough, but it passes the test.
1. Modern development environments, such as Eclipse and IDEA, will ﬁll in a missing
method on request. This means that we can write the call we’d like to make and ask
the tool to ﬁll in the declaration for us.
119
Unpacking a Price Message


---
**Page 120**

public class AuctionMessageTranslator implements MessageListener {
  private final AuctionEventListener listener;
  public AuctionMessageTranslator(AuctionEventListener listener) {
    this.listener = listener;
  }
  public void processMessage(Chat chat, Message message) {
    HashMap<String, String> event = unpackEventFrom(message);
    String type = event.get("Event");
    if ("CLOSE".equals(type)) {
      listener.auctionClosed();
    } else if ("PRICE".equals(type)) {
      listener.currentPrice(Integer.parseInt(event.get("CurrentPrice")), 
                            Integer.parseInt(event.get("Increment")));
    }
  }
  private HashMap<String, String> unpackEventFrom(Message message) {
    HashMap<String, String> event = new HashMap<String, String>();  
    for (String element : message.getBody().split(";")) {
      String[] pair = element.split(":");
      event.put(pair[0].trim(), pair[1].trim());
    }
    return event;
  }
}
This implementation breaks the message body into a set of key/value pairs,
which it interprets as an auction event so it can notify the AuctionEventListener.
We also have to ﬁx the FakeAuctionServer to send a real Close event rather than
the current empty message, otherwise the end-to-end tests will fail incorrectly.
public void announceClosed() throws XMPPException {
currentChat.sendMessage("SOLVersion: 1.1; Event: CLOSE;");
}
Running our end-to-end test again reminds us that we’re still working on the
bidding feature. The test shows that the Sniper status label still displays Joining
rather than Bidding.
Discovering Further Work
This code passes the unit test, but there’s something missing. It assumes that the
message is correctly structured and has the right version. Given that the message
will be coming from an outside system, this feels risky, so we need to add some
error handling. We don’t want to break the ﬂow of getting features to work, so
we add error handling to the to-do list to come back to it later (Figure 12.3).
Chapter 12
Getting Ready to Bid
120


---
**Page 121**

Figure 12.3
Added tasks for handling errors
We’re also concerned that the translator is not as clear as it could be about
what it’s doing, with its parsing and the dispatching activities mixed together.
We make a note to address this class as soon as we’ve passed the acceptance
test, which isn’t far off.
Finish the Job
Most of the work in this chapter has been trying to decide what we want to say
and how to say it: we write a high-level end-to-end test to describe what the
Sniper should implement; we write long unit test names to tell us what a class
does; we extract new classes to tease apart ﬁne-grained aspects of the functional-
ity; and we write lots of little methods to keep each layer of code at a consistent
level of abstraction. But ﬁrst, we write a rough implementation to prove that we
know how to make the code do what’s required and then we refactor—which
we’ll do in the next chapter.
We cannot emphasize strongly enough that “ﬁrst-cut” code is not ﬁnished. It’s
good enough to sort out our ideas and make sure we have everything in place,
but it’s unlikely to express its intentions cleanly. That will make it a drag on
productivity as it’s read repeatedly over the lifetime of the code. It’s like carpentry
without sanding—eventually someone ends up with a nasty splinter.
121
Finish the Job


---
**Page 122**

This page intentionally left blank 


