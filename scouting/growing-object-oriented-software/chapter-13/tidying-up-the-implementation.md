Line1 # Tidying Up the Implementation (pp.131-136)
Line2 
Line3 ---
Line4 **Page 131**
Line5 
Line6 Figure 13.3
Line7 One step forward
Line8 Tidying Up the Implementation
Line9 Extracting XMPPAuction
Line10 Our end-to-end test passes, but we haven’t ﬁnished because our new implemen-
Line11 tation feels messy. We notice that the activity in joinAuction() crosses multiple
Line12 domains: managing chats, sending bids, creating snipers, and so on. We need to
Line13 clean up. To start, we notice that we’re sending auction commands from two
Line14 different levels, at the top and from within the Auction. Sending commands to
Line15 an auction sounds like the sort of thing that our Auction object should do, so it
Line16 makes sense to package that up together. We add a new method to the interface,
Line17 extend our anonymous implementation, and then extract it to a (temporarily)
Line18 nested class—for which we need a name. The distinguishing feature of this imple-
Line19 mentation of Auction is that it’s based on the messaging infrastructure, so we
Line20 call our new class XMPPAuction.
Line21 131
Line22 Tidying Up the Implementation
Line23 
Line24 
Line25 ---
Line26 
Line27 ---
Line28 **Page 132**
Line29 
Line30 public class Main implements SniperListener { […]
Line31   private void joinAuction(XMPPConnection connection, String itemId) {
Line32     disconnectWhenUICloses(connection);
Line33     final Chat chat = 
Line34       connection.getChatManager().createChat(auctionId(itemId, connection), 
Line35                                              null);
Line36     this.notToBeGCd = chat;
Line37     Auction auction = new XMPPAuction(chat);
Line38     chat.addMessageListener(
Line39         new AuctionMessageTranslator(new AuctionSniper(auction, this)));
Line40 auction.join();
Line41   }
Line42   public static class XMPPAuction implements Auction {
Line43     private final Chat chat;
Line44     public XMPPAuction(Chat chat) {
Line45       this.chat = chat;
Line46     }
Line47     public void bid(int amount) {
Line48       sendMessage(format(BID_COMMAND_FORMAT, amount));
Line49     }
Line50     public void join() {
Line51       sendMessage(JOIN_COMMAND_FORMAT);
Line52     }
Line53     private void sendMessage(final String message) {
Line54       try {
Line55         chat.sendMessage(message);
Line56       } catch (XMPPException e) {
Line57         e.printStackTrace();
Line58       }
Line59     }
Line60   }
Line61 }
Line62 We’re starting to see a clearer model of the domain. The line auction.join()
Line63 expresses our intent more clearly than the previous detailed implementation of
Line64 sending a string to a chat. The new design looks like Figure 13.4  and we promote
Line65 XMPPAuction to be a top-level class.
Line66 We still think joinAuction() is unclear, and we’d like to pull the XMPP-related
Line67 detail out of Main, but we’re not ready to do that yet. Another point to keep
Line68 in mind.
Line69 Chapter 13
Line70 The Sniper Makes a Bid
Line71 132
Line72 
Line73 
Line74 ---
Line75 
Line76 ---
Line77 **Page 133**
Line78 
Line79 Figure 13.4
Line80 Closing the loop with an XMPPAuction
Line81 Extracting the User Interface
Line82 The other activity in Main is implementing the user interface and showing the
Line83 current state in response to events from the Sniper. We’re not really happy that
Line84 Main implements SniperListener; again, it feels like mixing different responsibil-
Line85 ities (starting the application and responding to events). We decide to extract the
Line86 SniperListener behavior into a nested helper class, for which the best name we
Line87 can ﬁnd is SniperStateDisplayer. This new class is our bridge between two do-
Line88 mains: it translates Sniper events into a representation that Swing can display,
Line89 which includes dealing with Swing threading. We plug an instance of the new
Line90 class into the AuctionSniper.
Line91 public class Main { // doesn't implement SniperListener
Line92   private MainWindow ui;
Line93   private void joinAuction(XMPPConnection connection, String itemId) {
Line94     disconnectWhenUICloses(connection);
Line95     final Chat chat = 
Line96       connection.getChatManager().createChat(auctionId(itemId, connection), null);
Line97     this.notToBeGCd = chat;
Line98     Auction auction = new XMPPAuction(chat);
Line99     chat.addMessageListener(
Line100         new AuctionMessageTranslator(
Line101             connection.getUser(),
Line102             new AuctionSniper(auction, new SniperStateDisplayer())));
Line103     auction.join();
Line104   }
Line105 […]
Line106 133
Line107 Tidying Up the Implementation
Line108 
Line109 
Line110 ---
Line111 
Line112 ---
Line113 **Page 134**
Line114 
Line115 public class SniperStateDisplayer implements SniperListener {
Line116     public void sniperBidding() {
Line117       showStatus(MainWindow.STATUS_BIDDING);
Line118     }
Line119     public void sniperLost() {
Line120       showStatus(MainWindow.STATUS_LOST);
Line121     }
Line122     public void sniperWinning() {
Line123       showStatus(MainWindow.STATUS_WINNING);
Line124     }
Line125     private void showStatus(final String status) {
Line126       SwingUtilities.invokeLater(new Runnable() {
Line127         public void run() { ui.showStatus(status); } 
Line128       });
Line129     }
Line130   }
Line131 }
Line132 Figure 13.5 shows how we’ve reduced Main so much that it no longer partici-
Line133 pates in the running application (for clarity, we’ve left out the WindowAdapter
Line134 that closes the connection). It has one job which is to create the various compo-
Line135 nents and introduce them to each other. We’ve marked MainWindow as external,
Line136 even though it’s one of ours, to represent the Swing framework.
Line137 Figure 13.5
Line138 Extracting SniperStateDisplayer
Line139 Chapter 13
Line140 The Sniper Makes a Bid
Line141 134
Line142 
Line143 
Line144 ---
Line145 
Line146 ---
Line147 **Page 135**
Line148 
Line149 Tidying Up the Translator
Line150 Finally, 
Line151 we 
Line152 fulﬁll 
Line153 our 
Line154 promise 
Line155 to 
Line156 ourselves 
Line157 and 
Line158 return 
Line159 to 
Line160 the
Line161 AuctionMessageTranslator. We start trying to reduce the noise by adding
Line162 constants and static imports, with some helper methods to reduce duplication.
Line163 Then we realize that much of the code is about manipulating the map of
Line164 name/value pairs and is rather procedural. We can do a better job by extracting
Line165 an inner class, AuctionEvent, to encapsulate the unpacking of the message con-
Line166 tents. We have conﬁdence that we can refactor the class safely because it’s
Line167 protected by its unit tests.
Line168 public class AuctionMessageTranslator implements MessageListener { 
Line169   private final AuctionEventListener listener;
Line170   public AuctionMessageTranslator(AuctionEventListener listener) {
Line171     this.listener = listener;
Line172   }
Line173   public void processMessage(Chat chat, Message message) { 
Line174 AuctionEvent event = AuctionEvent.from(message.getBody());
Line175     String eventType = event.type();
Line176     if ("CLOSE".equals(eventType)) { 
Line177       listener.auctionClosed(); 
Line178     } if ("PRICE".equals(eventType)) { 
Line179       listener.currentPrice(event.currentPrice(), event.increment()); 
Line180     } 
Line181   }
Line182   private static class AuctionEvent {
Line183     private final Map<String, String> fields = new HashMap<String, String>();  
Line184     public String type() { return get("Event"); }
Line185     public int currentPrice() { return getInt("CurrentPrice"); }
Line186     public int increment() { return getInt("Increment"); }
Line187     private int getInt(String fieldName) {
Line188       return Integer.parseInt(get(fieldName));
Line189     }
Line190     private String get(String fieldName) { return fields.get(fieldName); }
Line191     private void addField(String field) {
Line192       String[] pair = field.split(":");
Line193       fields.put(pair[0].trim(), pair[1].trim());
Line194     }
Line195     static AuctionEvent from(String messageBody) {
Line196       AuctionEvent event = new AuctionEvent();
Line197       for (String field : fieldsIn(messageBody)) {
Line198         event.addField(field);
Line199       }
Line200       return event;
Line201     }
Line202     static String[] fieldsIn(String messageBody) {
Line203       return messageBody.split(";");
Line204     }
Line205   }
Line206 }
Line207 135
Line208 Tidying Up the Implementation
Line209 
Line210 
Line211 ---
Line212 
Line213 ---
Line214 **Page 136**
Line215 
Line216 This is an example of “breaking out” that we described in “Value Types”
Line217 (page 59). It may not be obvious, but AuctionEvent is a value: it’s
Line218 immutable and there are no interesting differences between two instances
Line219 with the same contents. This refactoring separates the concerns within
Line220 AuctionMessageTranslator: the top level deals with events and listeners, and
Line221 the inner object deals with parsing strings.
Line222 Encapsulate Collections
Line223 We’ve developed a habit of packaging up common types, such as collections, in
Line224 our own classes, even though Java generics avoid the need to cast objects. We’re
Line225 trying to use the language of the problem we’re working on, rather than the language
Line226 of Java constructs. In our two versions of processMessage(), the ﬁrst has lots of
Line227 incidental noise about looking up and parsing values.The second is written in terms
Line228 of auction events, so there’s less of a conceptual gap between the domain and
Line229 the code.
Line230 Our rule of thumb is that we try to limit passing around types with generics (the
Line231 types enclosed in angle brackets). Particularly when applied to collections, we view
Line232 it as a form of duplication. It’s a hint that there’s a domain concept that should be
Line233 extracted into a type.
Line234 Defer Decisions
Line235 There’s a technique we’ve used a couple of times now, which is to introduce a
Line236 null implementation of a method (or even a type) to get us through the next step.
Line237 This helps us focus on the immediate task without getting dragged into thinking
Line238 about the next signiﬁcant chunk of functionality. The null Auction, for example,
Line239 allowed us to plug in a new relationship we’d discovered in a unit test without
Line240 getting pulled into messaging issues. That, in turn, meant we could stop and
Line241 think about the dependencies between our objects without the pressure of having
Line242 a broken compilation.
Line243 Keep the Code Compiling
Line244 We try to minimize the time when we have code that does not compile by keeping
Line245 changes incremental. When we have compilation failures, we can’t be quite sure
Line246 where the boundaries of our changes are, since the compiler can’t tell us. This, in
Line247 turn, means that we can’t check in to our source repository, which we like to do
Line248 often.The more code we have open, the more we have to keep in our heads which,
Line249 ironically, usually means we move more slowly. One of the great discoveries of
Line250 test-driven development is just how ﬁne-grained our development steps can be.
Line251 Chapter 13
Line252 The Sniper Makes a Bid
Line253 136
Line254 
Line255 
Line256 ---
