Line1 # Finding a Role (pp.191-192)
Line2 
Line3 ---
Line4 **Page 191**
Line5 
Line6 Chapter 17
Line7 Teasing Apart Main
Line8 In which we slice up our application, shufﬂing behavior around to
Line9 isolate the XMPP and user interface code from the sniping logic. We
Line10 achieve this incrementally, changing one concept at a time without
Line11 breaking the whole application. We ﬁnally put a stake through the
Line12 heart of notToBeGCd.
Line13 Finding a Role
Line14 We’ve convinced ourselves that we need to do some surgery on Main, but what
Line15 do we want our improved Main to do?
Line16 For programs that are more than trivial, we like to think of our top-level class
Line17 as a “matchmaker,” ﬁnding components and introducing them to each other.
Line18 Once that job is done it drops into the background and waits for the application to
Line19 ﬁnish. On a larger scale, this what the current generation of application containers
Line20 do, except that the relationships are often encoded in XML.
Line21 In its current form, Main acts as a matchmaker but it’s also implementing some
Line22 of the components, which means it has too many responsibilities. One clue is to
Line23 look at its imports:
Line24 import java.awt.event.WindowAdapter;
Line25 import java.awt.event.WindowEvent;
Line26 import java.util.ArrayList;
Line27 import javax.swing.SwingUtilities;
Line28 import org.jivesoftware.smack.Chat;
Line29 import org.jivesoftware.smack.XMPPConnection;
Line30 import org.jivesoftware.smack.XMPPException;
Line31 import auctionsniper.ui.MainWindow;
Line32 import auctionsniper.ui.SnipersTableModel;
Line33 import auctionsniper.AuctionMessageTranslator;
Line34 import auctionsniper.XMPPAuction;
Line35 We’re importing code from three unrelated packages, plus the auctionsniper
Line36 package itself. In fact, we have a package loop in that the top-level and
Line37 UI packages depend on each other. Java, unlike some other languages, tolerates
Line38 package loops, but they’re not something we should be pleased with.
Line39 191
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 192**
Line46 
Line47 We think we should extract some of this behavior from Main, and the XMPP
Line48 features look like a good ﬁrst candidate. The use of the Smack should be an
Line49 implementation detail that is irrelevant to the rest of the application.
Line50 Extracting the Chat
Line51 Isolating the Chat
Line52 Most 
Line53 of 
Line54 the 
Line55 action 
Line56 happens 
Line57 in 
Line58 the 
Line59 implementation 
Line60 of
Line61 UserRequestListener.joinAuction() within Main. We notice that we’ve inter-
Line62 leaved different domain levels, auction sniping and chatting, in this one unit of
Line63 code. We’d like to split them up. Here it is again:
Line64 public class Main { […]
Line65   private void addUserRequestListenerFor(final XMPPConnection connection) {
Line66     ui.addUserRequestListener(new UserRequestListener() {
Line67     public void joinAuction(String itemId) {
Line68       snipers.addSniper(SniperSnapshot.joining(itemId));
Line69         Chat chat = connection.getChatManager()
Line70                                  .createChat(auctionId(itemId, connection), null);
Line71         notToBeGCd.add(chat); 
Line72         Auction auction = new XMPPAuction(chat);
Line73 chat.addMessageListener(
Line74                new AuctionMessageTranslator(connection.getUser(),
Line75                      new AuctionSniper(itemId, auction, 
Line76                            new SwingThreadSniperListener(snipers))));
Line77         auction.join();
Line78       }
Line79     });
Line80   }
Line81 }
Line82 The object that locks this code into Smack is the chat; we refer to it several times:
Line83 to avoid garbage collection, to attach it to the Auction implementation, and to
Line84 attach the message listener. If we can gather together the auction- and Sniper-
Line85 related code, we can move the chat elsewhere, but that’s tricky while there’s still
Line86 a dependency loop between the XMPPAuction, Chat, and AuctionSniper.
Line87 Looking again, the Sniper actually plugs in to the AuctionMessageTranslator
Line88 as an AuctionEventListener. Perhaps using an Announcer to bind the two together,
Line89 rather than a direct link, would give us the ﬂexibility we need. It would also make
Line90 sense to have the Sniper as a notiﬁcation, as deﬁned in “Object Peer Stereotypes”
Line91 (page 52). The result is:
Line92 Chapter 17
Line93 Teasing Apart Main
Line94 192
Line95 
Line96 
Line97 ---
