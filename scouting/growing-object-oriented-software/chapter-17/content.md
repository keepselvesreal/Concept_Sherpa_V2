# Chapter 17: Teasing Apart Main (pp.191-204)

---
**Page 191**

Chapter 17
Teasing Apart Main
In which we slice up our application, shufﬂing behavior around to
isolate the XMPP and user interface code from the sniping logic. We
achieve this incrementally, changing one concept at a time without
breaking the whole application. We ﬁnally put a stake through the
heart of notToBeGCd.
Finding a Role
We’ve convinced ourselves that we need to do some surgery on Main, but what
do we want our improved Main to do?
For programs that are more than trivial, we like to think of our top-level class
as a “matchmaker,” ﬁnding components and introducing them to each other.
Once that job is done it drops into the background and waits for the application to
ﬁnish. On a larger scale, this what the current generation of application containers
do, except that the relationships are often encoded in XML.
In its current form, Main acts as a matchmaker but it’s also implementing some
of the components, which means it has too many responsibilities. One clue is to
look at its imports:
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import javax.swing.SwingUtilities;
import org.jivesoftware.smack.Chat;
import org.jivesoftware.smack.XMPPConnection;
import org.jivesoftware.smack.XMPPException;
import auctionsniper.ui.MainWindow;
import auctionsniper.ui.SnipersTableModel;
import auctionsniper.AuctionMessageTranslator;
import auctionsniper.XMPPAuction;
We’re importing code from three unrelated packages, plus the auctionsniper
package itself. In fact, we have a package loop in that the top-level and
UI packages depend on each other. Java, unlike some other languages, tolerates
package loops, but they’re not something we should be pleased with.
191


---
**Page 192**

We think we should extract some of this behavior from Main, and the XMPP
features look like a good ﬁrst candidate. The use of the Smack should be an
implementation detail that is irrelevant to the rest of the application.
Extracting the Chat
Isolating the Chat
Most 
of 
the 
action 
happens 
in 
the 
implementation 
of
UserRequestListener.joinAuction() within Main. We notice that we’ve inter-
leaved different domain levels, auction sniping and chatting, in this one unit of
code. We’d like to split them up. Here it is again:
public class Main { […]
  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
    public void joinAuction(String itemId) {
      snipers.addSniper(SniperSnapshot.joining(itemId));
        Chat chat = connection.getChatManager()
                                 .createChat(auctionId(itemId, connection), null);
        notToBeGCd.add(chat); 
        Auction auction = new XMPPAuction(chat);
chat.addMessageListener(
               new AuctionMessageTranslator(connection.getUser(),
                     new AuctionSniper(itemId, auction, 
                           new SwingThreadSniperListener(snipers))));
        auction.join();
      }
    });
  }
}
The object that locks this code into Smack is the chat; we refer to it several times:
to avoid garbage collection, to attach it to the Auction implementation, and to
attach the message listener. If we can gather together the auction- and Sniper-
related code, we can move the chat elsewhere, but that’s tricky while there’s still
a dependency loop between the XMPPAuction, Chat, and AuctionSniper.
Looking again, the Sniper actually plugs in to the AuctionMessageTranslator
as an AuctionEventListener. Perhaps using an Announcer to bind the two together,
rather than a direct link, would give us the ﬂexibility we need. It would also make
sense to have the Sniper as a notiﬁcation, as deﬁned in “Object Peer Stereotypes”
(page 52). The result is:
Chapter 17
Teasing Apart Main
192


---
**Page 193**

public class Main { […]
  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
      public void joinAuction(String itemId) {
        Chat chat = connection.[…]
        Announcer<AuctionEventListener> auctionEventListeners = 
            Announcer.to(AuctionEventListener.class);
        chat.addMessageListener(
            new AuctionMessageTranslator(
                connection.getUser(),
auctionEventListeners.announce()));
        notToBeGCd.add(chat);
        Auction auction = new XMPPAuction(chat);
auctionEventListeners.addListener(
           new AuctionSniper(itemId, auction, new SwingThreadSniperListener(snipers)));
        auction.join();
      }
    }
  }
}
This looks worse, but the interesting bit is the last three lines. If you squint, it
looks like everything is described in terms of Auctions and Snipers (there’s still
the Swing thread issue, but we did tell you to squint).
Encapsulating the Chat
From here, we can push everything to do with chat, its setup, and the use of the
Announcer, into XMPPAuction, adding management methods to the Auction inter-
face for its AuctionEventListeners. We’re just showing the end result here, but
we changed the code incrementally so that nothing was broken for more than a
few minutes.
public final class XMPPAuction implements Auction { […]
  private final Announcer<AuctionEventListener> auctionEventListeners = […]
  private final Chat chat;
  public XMPPAuction(XMPPConnection connection, String itemId) {
    chat = connection.getChatManager().createChat(
             auctionId(itemId, connection),
             new AuctionMessageTranslator(connection.getUser(), 
                                          auctionEventListeners.announce()));
  } 
  private static String auctionId(String itemId, XMPPConnection connection) { 
    return String.format(AUCTION_ID_FORMAT, itemId, connection.getServiceName());
  }
}
193
Extracting the Chat


---
**Page 194**

Apart from the garbage collection “wart,” this removes any references to Chat
from Main.
public class Main { […]
  private void addUserRequestListenerFor(final XMPPConnection connection) {
    ui.addUserRequestListener(new UserRequestListener() {
      public void joinAuction(String itemId) {
          snipers.addSniper(SniperSnapshot.joining(itemId));
          Auction auction = new XMPPAuction(connection, itemId);
          notToBeGCd.add(auction);
auction.addAuctionEventListener(
                  new AuctionSniper(itemId, auction, 
                                    new SwingThreadSniperListener(snipers)));
auction.join();
      }
    });
  }
}
Figure 17.1
With XMPPAuction extracted
Writing a New Test
We also write a new integration test for the expanded XMPPAuction to show that
it can create a Chat and attach a listener. We use some of our existing end-to-end
test infrastructure, such as FakeAuctionServer, and a CountDownLatch from the
Java concurrency libraries to wait for a response.
Chapter 17
Teasing Apart Main
194


---
**Page 195**

@Test public void
receivesEventsFromAuctionServerAfterJoining() throws Exception {
  CountDownLatch auctionWasClosed = new CountDownLatch(1);
  Auction auction =  new XMPPAuction(connection, auctionServer.getItemId());
  auction.addAuctionEventListener(auctionClosedListener(auctionWasClosed));
  auction.join();
  server.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
  server.announceClosed();
  assertTrue("should have been closed", auctionWasClosed.await(2, SECONDS)); 
} 
private AuctionEventListener 
auctionClosedListener(final CountDownLatch auctionWasClosed) {
  return new AuctionEventListener() {
    public void auctionClosed() { auctionWasClosed.countDown(); }
    public void currentPrice(int price, int increment, PriceSource priceSource) { 
// not implemented
    }
  };
}
Looking over the result, we can see that it makes sense for XMPPAuction to en-
capsulate a Chat as now it hides everything to do with communicating between
a request listener and an auction service, including translating the messages. We
can also see that the AuctionMessageTranslator is internal to this encapsulation,
the Sniper doesn’t need to see it. So, to recognize our new structure, we move
XMPPAuction and AuctionMessageTranslator into a new auctionsniper.xmpp
package, and the tests into equivalent xmpp test packages.
Compromising on a Constructor
We have one doubt about this implementation: the constructor includes some real
behavior. Our experience is that busy constructors enforce assumptions that one
day we will want to break, especially when testing, so we prefer to keep them very
simple—just setting the ﬁelds. For now, we convince ourselves that this is “veneer”
code, a bridge to an external library, that can only be integration-tested because
the Smack classes have just the kind of complicated constructors we try to avoid.
Extracting the Connection
The next thing to remove from Main is direct references to the XMPPConnection.
We can wrap these up in a factory class that will create an instance of an Auction
for a given item, so it will have a method like
Auction auction = <factory>.auctionFor(item id);
195
Extracting the Connection


---
**Page 196**

We struggle for a while over what to call this new type, since it should have a
name that reﬂects the language of auctions. In the end, we decide that the concept
that arranges auctions is an “auction house,” so that’s what we call our new type:
public interface AuctionHouse {
  Auction auctionFor(String itemId);
}
The end result of this refactoring is:
public class Main { […]
  public static void main(String... args) throws Exception {
    Main main = new Main();
XMPPAuctionHouse auctionHouse = 
      XMPPAuctionHouse.connect(
        args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
    main.disconnectWhenUICloses(auctionHouse);
    main.addUserRequestListenerFor(auctionHouse);
  }
  private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
    ui.addUserRequestListener(new UserRequestListener() {
      public void joinAuction(String itemId) {
        snipers.addSniper(SniperSnapshot.joining(itemId));
Auction auction = auctionHouse.auctionFor(itemId);
        notToBeGCd.add(auction);
[…]
      }
    }
  }
}
Figure 17.2
With XMPPAuctionHouse extracted
Chapter 17
Teasing Apart Main
196


---
**Page 197**

Implementing XMPPAuctionHouse is straightforward; we transfer there all the
code related to connection, including the generation of the Jabber ID from
the auction item ID. Main is now simpler, with just one import for all the XMPP
code, auctionsniper.xmpp.XMPPAuctionHouse. The new version looks like
Figure 17.2.
For consistency, we retroﬁt XMPPAuctionHouse to the integration test for
XMPPAuction, instead of creating XMPPAuctions directly as it does now, and rename
the test to XMPPAuctionHouseTest.
Our ﬁnal touch is to move the relevant constants from Main where we’d left
them: the message formats to XMPPAuction and the connection identiﬁer format
to XMPPAuctionHouse. This reassures us that we’re moving in the right direction,
since we’re narrowing the scope of where these constants are used.
Extracting the SnipersTableModel
Sniper Launcher
Finally, we’d like to do something about the direct reference to the
SnipersTableModel and the related SwingThreadSniperListener—and the awful
notToBeGCd. We think we can get there, but it’ll take a couple of steps.
The ﬁrst step is to turn the anonymous implementation of UserRequestListener
into a proper class so we can understand its dependencies. We decide to call the
new class SniperLauncher, since it will respond to a request to join an auction
by “launching” a Sniper. One nice effect is that we can make notToBeGCd local
to the new class.
public class SniperLauncher implements UserRequestListener {
  private final ArrayList<Auction> notToBeGCd = new ArrayList<Auction>();
  private final AuctionHouse auctionHouse;
  private final SnipersTableModel snipers;
  public SniperLauncher(AuctionHouse auctionHouse, SnipersTableModel snipers) {
// set the fields 
  }
  public void joinAuction(String itemId) {
snipers.addSniper(SniperSnapshot.joining(itemId));
      Auction auction = auctionHouse.auctionFor(itemId);
      notToBeGCd.add(auction);
      AuctionSniper sniper = 
        new AuctionSniper(itemId, auction, 
                          new SwingThreadSniperListener(snipers));
      auction.addAuctionEventListener(snipers);
      auction.join();
  }
}
With the SniperLauncher separated out, it becomes even clearer that the
Swing features don’t ﬁt here. There’s a clue in that our use of snipers, the
197
Extracting the SnipersTableModel


---
**Page 198**

SnipersTableModel, is clumsy: we tell it about the new Sniper by giving it an
initial SniperSnapshot, and we attach it to both the Sniper and the auction.
There’s also some hidden duplication in that we create an initial SniperSnaphot
both here and in the AuctionSniper constructor.
Stepping back, we ought to simplify this class so that all it does is establish a
new AuctionSniper. It can delegate the process of accepting the new Sniper into
the application to a new role which we’ll call a SniperCollector, implemented
in the SnipersTableModel.
public static class SniperLauncher implements UserRequestListener {
  private final AuctionHouse auctionHouse;
  private final SniperCollector collector;
[…]
  public void joinAuction(String itemId) {
      Auction auction = auctionHouse.auctionFor(itemId);
AuctionSniper sniper = new AuctionSniper(itemId, auction);
      auction.addAuctionEventListener(sniper);
collector.addSniper(sniper);
      auction.join();
  }
}
The one behavior that we want to conﬁrm is that we only join the auction after
everything else is set up. With the code now isolated, we can jMock a States to
check the ordering.
public class SniperLauncherTest {
  private final States auctionState = context.states("auction state")
.startsAs("not joined");
[…]
  @Test public void
addsNewSniperToCollectorAndThenJoinsAuction() {
    final String itemId = "item 123";
    context.checking(new Expectations() {{
      allowing(auctionHouse).auctionFor(itemId); will(returnValue(auction));
      oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId))); 
when(auctionState.is("not joined"));
      oneOf(sniperCollector).addSniper(with(sniperForItem(item))); 
when(auctionState.is("not joined"));
      one(auction).join(); then(auctionState.is("joined"));
    }});
    launcher.joinAuction(itemId);
  }
}
where sniperForItem() returns a Matcher that matches any AuctionSniper
associated with the given item identiﬁer.
We extend SnipersTableModel to fulﬁll its new role: now it accepts
AuctionSnipers rather than SniperSnapshots. To make this work, we have to
convert a Sniper’s listener from a dependency to a notiﬁcation, so that we can
Chapter 17
Teasing Apart Main
198


---
**Page 199**

add a listener after construction. We also change SnipersTableModel to use the
new API and disallow adding SniperSnapshots.
public class SnipersTableModel extends AbstractTableModel 
    implements SniperListener, SniperCollector
{
  private final ArrayList<AuctionSniper> notToBeGCd = […]
  public void addSniper(AuctionSniper sniper) {
    notToBeGCd.add(sniper);
    addSniperSnapshot(sniper.getSnapshot());
    sniper.addSniperListener(new SwingThreadSniperListener(this));
  }
  private void addSniperSnapshot(SniperSnapshot sniperSnapshot) {
    snapshots.add(sniperSnapshot);
    int row = snapshots.size() - 1;
    fireTableRowsInserted(row, row);
   }
}
One change that suggests that we’re heading in the right direction is that the
SwingThreadSniperListener is now packaged up in the Swing part of the code,
not in the generic SniperLauncher.
Sniper Portfolio
As a next step, we realize that we don’t yet have anything that represents all our
sniping activity and that we might call our portfolio. At the moment, the
SnipersTableModel is implicitly responsible for both maintaining a record of
our sniping and displaying that record. It also pulls a Swing implementation detail
into Main.
We want a clearer separation of concerns, so we extract a SniperPortfolio
to maintain our Snipers, which we make our new implementer of
SniperCollector. We push the creation of the SnipersTableModel into MainWindow,
and make it a PortfolioListener so the portfolio can tell it when we add or
remove a Sniper.
public interface PortfolioListener extends EventListener {
  void sniperAdded(AuctionSniper sniper);
}
public class MainWindow extends JFrame {
  private JTable makeSnipersTable(SniperPortfolio portfolio) { 
SnipersTableModel model = new SnipersTableModel();
    portfolio.addPortfolioListener(model);
    JTable snipersTable = new JTable(model); 
    snipersTable.setName(SNIPERS_TABLE_NAME); 
    return snipersTable; 
  }
}
199
Extracting the SnipersTableModel


---
**Page 200**

This makes our top-level code very simple—it just binds together the user
interface and sniper creation through the portfolio:
public class Main {  […]
  private final SniperPortfolio portfolio = new SniperPortfolio();
  public Main() throws Exception {
    SwingUtilities.invokeAndWait(new Runnable() {
      public void run() {
        ui = new MainWindow(portfolio);
      }
    });
  }
  private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
    ui.addUserRequestListener(new SniperLauncher(auctionHouse, portfolio));
  }
}
Even better, since SniperPortfolio maintains a list of all the Snipers, we can
ﬁnally get rid of notToBeGCd.
This refactoring takes us to the structure shown in Figure 17.3. We’ve separated
the code into three components: one for the core application, one for XMPP
communication, and one for Swing display. We’ll return to this in a moment.
Figure 17.3
With the SniperPortfolio
Chapter 17
Teasing Apart Main
200


---
**Page 201**

Now that we’ve cleaned up, we can cross the next item off our list: Figure 17.4.
Figure 17.4
Adding items through the user interface
Observations
Incremental Architecture
This restructuring of Main is a key moment in the development of the application.
As Figure 17.5 shows, we now have a structure that matches the “ports and
adapters” architecture we described in “Designing for Maintainability” (page 47).
There is core domain code (for example, AuctionSniper) which depends on
bridging code (for example, SnipersTableModel) that drives or responds to
technical code (for example, JTable). We’ve kept the domain code free of any
reference to the external infrastructure. The contents of our auctionsniper
package deﬁne a model of our auction sniping business, using a self-contained
language. The exception is Main, which is our entry point and binds the domain
model and infrastructure together.
What’s important for the purposes of this example, is that we arrived at this
design incrementally, by adding features and repeatedly following heuristics.
Although we rely on our experience to guide our decisions, we reached this
solution almost automatically by just following the code and taking care to keep
it clean.
201
Observations


---
**Page 202**

Figure 17.5
The application now has a “ports and adapters”
architecture
Three-Point Contact
We wrote this refactoring up in detail because we wanted to make some points
along the way and to show that we can do signiﬁcant refactorings incrementally.
When we’re not sure what to do next or how to get there from here, one way of
coping is to scale down the individual changes we make, as Kent Beck showed
in [Beck02]. By repeatedly ﬁxing local problems in the code, we ﬁnd we can ex-
plore the design safely, never straying more than a few minutes from working
code. Usually this is enough to lead us towards a better design, and we can always
backtrack and take another path if it doesn’t work out.
One way to think of this is the rock climbing rule of “three-point contact.”
Trained climbers only move one limb at a time (a hand or a foot), to minimize
the risk of falling off. Each move is minimal and safe, but combining enough of
them will get you to the top of the route.
In “elapsed time,” this refactoring didn’t take much longer than the time you
spent reading it, which we think is a good return for the clearer separation of
concerns. With experience, we’ve learned to recognize fault lines in code so we
can often take a more direct route.
Chapter 17
Teasing Apart Main
202


---
**Page 203**

Dynamic as Well as Static Design
We did encounter one small bump whilst working on the code for this chapter.
Steve was extracting the SniperPortfolio and got stuck trying to ensure that the
sniperAdded() method was called within the Swing thread. Eventually he remem-
bered that the event is triggered by a button click anyway, so he was already
covered.
What we learn from this (apart from the need for pairing while writing book
examples) is that we should consider more than one view when refactoring code.
Refactoring is, after all, a design activity, which means we still need all the skills
we were taught—except that now we need them all the time rather than periodi-
cally. Refactoring is so focused on static structure (classes and interfaces) that
it’s easy to lose sight of an application’s dynamic structure (instances and threads).
Sometimes we just need to step back and draw out, say, an interaction diagram
like Figure 17.6:
Figure 17.6
An Interaction Diagram
An Alternative Fix to notToBeGCd
Our chosen ﬁx relies on the SniperPortfolio holding onto the reference. That’s
likely to be the case in practice, but if it ever changes we will get transient failures
that are hard to track down. We’re relying on a side effect of the application to
ﬁx an issue in the XMPP code.
An alternative would be to say that it’s a Smack problem, so our XMPP layer
should deal with it. We could make the XMPPAuctionHouse hang on to the
XMPPAuctions it creates, in which case we’d to have to add a lifecycle listener of
some sort to tell us when we’re ﬁnished with an Auction and can release it. There
is no obvious choice here; we just have to look at the circumstances and exercise
some judgment.
203
Observations


---
**Page 204**

This page intentionally left blank 


