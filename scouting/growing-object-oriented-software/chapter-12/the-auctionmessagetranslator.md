Line1 # The AuctionMessageTranslator (pp.112-118)
Line2 
Line3 ---
Line4 **Page 112**
Line5 
Line6 Outside-In Development
Line7 This failure deﬁnes the target for our next coding episode. It tells us, at a high
Line8 level, what we’re aiming for—we just have to ﬁll in implementation until it
Line9 passes.
Line10 Our approach to test-driven development is to start with the outside event that
Line11 triggers the behavior we want to implement and work our way into the code an
Line12 object at a time, until we reach a visible effect (such as a sent message or log entry)
Line13 indicating that we’ve achieved our goal. The end-to-end test shows us the end
Line14 points of that process, so we can explore our way through the space in the middle.
Line15 In the following sections, we build up the types we need to implement our
Line16 Auction Sniper. We’ll take it slowly, strictly by the TDD rules, to show how the
Line17 process works. In real projects, we sometimes design a bit further ahead to get
Line18 a sense of the bigger picture, but much of the time this is what we actually do.
Line19 It produces the right results and forces us to ask the right questions.
Line20 Inﬁnite Attention to Detail?
Line21 We caught the resource clash because, by luck or insight, our server conﬁguration
Line22 matched that of Southabee’s On-Line. We might have used an alternative setting
Line23 which allows new connections to kick off existing ones, which would have resulted
Line24 in the tests passing but with a confusing conﬂict message from the Smack library
Line25 on the error stream. This would have worked ﬁne in development, but with a
Line26 risk of Snipers starting to fail in production.
Line27 How can we hope to catch all the conﬁguration options in an entire system?
Line28 At some level we can’t, and this is at the heart of what professional testers do.
Line29 What we can do is push to exercise as much as possible of the system as early as
Line30 possible, and to do so repeatedly. We can also help ourselves cope with total
Line31 system complexity by keeping the quality of its components high and by constantly
Line32 pushing to simplify. If that sounds expensive, consider the cost of ﬁnding and
Line33 ﬁxing a transient bug like this one in a busy production system.
Line34 The AuctionMessageTranslator
Line35 Teasing Out a New Class
Line36 Our entry point to the Sniper is where we receive a message from the auction
Line37 through the Smack library: it’s the event that triggers the next round of behavior
Line38 we want to make work. In practice, this means that we need a class implementing
Line39 MessageListener to attach to the Chat. When this class receives a raw message
Line40 from the auction, it will translate it into something that represents an auction
Line41 event within our code which, eventually, will prompt a Sniper action and a change
Line42 in the user interface.
Line43 Chapter 12
Line44 Getting Ready to Bid
Line45 112
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 113**
Line52 
Line53 We already have such a class in Main—it’s anonymous and its responsibilities
Line54 aren’t very obvious:
Line55 new MessageListener() {
Line56   public void processMessage(Chat aChat, Message message) {
Line57     SwingUtilities.invokeLater(new Runnable() {
Line58       public void run() {
Line59         ui.showStatus(MainWindow.STATUS_LOST);
Line60       }
Line61     });
Line62   }
Line63 }
Line64 This code implicitly accepts a Close message (the only kind of message we
Line65 have so far) and implements the Sniper’s response. We’d like to make this situation
Line66 explicit before we add more features. We start by promoting the anonymous
Line67 class to a top-level class in its own right, which means it needs a name. From our
Line68 description in the paragraph above, we pick up the word “translate” and call it
Line69 an AuctionMessageTranslator, because it will translate messages from the auction.
Line70 The catch is that the current anonymous class picks up the ui ﬁeld from Main.
Line71 We’ll have to attach something to our newly promoted class so that it can respond
Line72 to a message. The most obvious thing to do is pass it the MainWindow but we’re
Line73 unhappy about creating a dependency on a user interface component. That would
Line74 make it hard to unit-test, because we’d have to query the state of a component
Line75 that’s running in the Swing event thread.
Line76 More signiﬁcantly, such a dependency would break the “single responsibility”
Line77 principle which says that unpacking raw messages from the auction is quite
Line78 enough for one class to do, without also having to know how to present the
Line79 Sniper status. As we wrote in “Designing for Maintainability” (page 47), we
Line80 want to maintain a separation of concerns.
Line81 Given these constraints, we decide that our new AuctionMessageTranslator
Line82 will delegate the handling of an interpreted event to a collaborator, which we will
Line83 represent with an AuctionEventListener interface; we can pass an object that
Line84 implements it into the translator on construction. We don’t yet know what’s in
Line85 this interface and we haven’t yet begun to think about its implementation. Our
Line86 immediate concern is to get the message translation to work; the rest can wait.
Line87 So far the design looks like Figure 12.1 (types that belong to external frameworks,
Line88 such as Chat, are shaded):
Line89 Figure 12.1
Line90 The AuctionMessageTranslator
Line91 113
Line92 The AuctionMessageTranslator
Line93 
Line94 
Line95 ---
Line96 
Line97 ---
Line98 **Page 114**
Line99 
Line100 The First Unit Test
Line101 We start with the simpler event type. As we’ve seen, a Close event has no
Line102 values—it’s a simple trigger. When the translator receives one, we want it to call
Line103 its listener appropriately.
Line104 As this is our ﬁrst unit test, we’ll build it up very slowly to show the process
Line105 (later, we will move faster). We start with the test method name. JUnit picks up
Line106 test methods by reﬂection, so we can make their names as long and descriptive
Line107 as we like because we never have to include them in code. The ﬁrst test says that
Line108 the translator will tell anything that’s listening that the auction has closed when
Line109 it receives a raw Close message.
Line110 package test.auctionsniper;
Line111 public class AuctionMessageTranslatorTest {
Line112   @Test public void
Line113 notifiesAuctionClosedWhenCloseMessageReceived() {
Line114 // nothing yet
Line115   }
Line116 }
Line117 Put Tests in a Different Package
Line118 We’ve adopted a habit of putting tests in a different package from the code they’re
Line119 exercising.We want to make sure we’re driving the code through its public interfaces,
Line120 like any other client, rather than opening up a package-scoped back door for testing.
Line121 We also ﬁnd that, as the application and test code grows, separate packages make
Line122 navigation in modern IDEs easier.
Line123 The next step is to add the action that will trigger the behavior we want to
Line124 test—in this case, sending a Close message. We already know what this will look
Line125 like since it’s a call to the Smack MessageListener interface.
Line126 public class AuctionMessageTranslatorTest {
Line127   public static final Chat UNUSED_CHAT = null;
Line128 private final AuctionMessageTranslator translator = 
Line129                                               new AuctionMessageTranslator();
Line130   @Test public void
Line131 notfiesAuctionClosedWhenCloseMessageReceived() {
Line132 Message message = new Message();
Line133     message.setBody("SOLVersion: 1.1; Event: CLOSE;");
Line134     translator.processMessage(UNUSED_CHAT, message);
Line135   }
Line136 }
Line137 Chapter 12
Line138 Getting Ready to Bid
Line139 114
Line140 
Line141 
Line142 ---
Line143 
Line144 ---
Line145 **Page 115**
Line146 
Line147 Use null When an Argument Doesn’t Matter
Line148 UNUSED_CHAT is a meaningful name for a constant that is deﬁned as null.We pass
Line149 it into processMessage() instead of a real Chat object because the Chat class is
Line150 difﬁcult to instantiate—its constructor is package-scoped and we’d have to ﬁll in a
Line151 chain of dependencies to create one. As it happens, we don’t need one anyway
Line152 for the current functionality, so we just pass in a null value to satisfy the compiler
Line153 but use a named constant to make clear its signiﬁcance.
Line154 To be clear, this null is not a null object [Woolf98] which may be called and will
Line155 do nothing in response. This null is just a placeholder and will fail if called during
Line156 the test.
Line157 We generate a skeleton implementation from the MessageListener interface.
Line158 package auctionsniper;
Line159 public class AuctionMessageTranslator implements MessageListener {
Line160   public void processMessage(Chat chat, Message message) {
Line161 // TODO Fill in here
Line162   }
Line163 }
Line164 Next, we want a check that shows whether the translation has taken
Line165 place—which should fail since we haven’t implemented anything yet. We’ve al-
Line166 ready decided that we want our translator to notify its listener when the Close
Line167 event occurs, so we’ll describe that expected behavior in our test.
Line168 @RunWith(JMock.class) 
Line169 public class AuctionMessageTranslatorTest {
Line170   private final Mockery context = new Mockery();
Line171   private final AuctionEventListener listener = 
Line172                               context.mock(AuctionEventListener.class); 
Line173   private final AuctionMessageTranslator translator = 
Line174                                         new AuctionMessageTranslator();
Line175   @Test public void
Line176 notfiesAuctionClosedWhenCloseMessageReceived() {
Line177     context.checking(new Expectations() {{
Line178 oneOf(listener).auctionClosed();
Line179     }});
Line180     Message message = new Message();
Line181     message.setBody("SOLVersion: 1.1; Event: CLOSE;");
Line182     translator.processMessage(UNUSED_CHAT, message);
Line183   }
Line184 }
Line185 115
Line186 The AuctionMessageTranslator
Line187 
Line188 
Line189 ---
Line190 
Line191 ---
Line192 **Page 116**
Line193 
Line194 This is more or less the kind of unit test we described at the end of Chapter 2,
Line195 so we won’t go over its structure again here except to emphasize the highlighted
Line196 expectation line. This is the most signiﬁcant line in the test, our declaration of
Line197 what matters about the translator’s effect on its environment. It says that when
Line198 we send an appropriate message to the translator, we expect it to call the listener’s
Line199 auctionClosed() method exactly once.
Line200 We get a failure that shows that we haven’t implemented the behavior we need:
Line201 not all expectations were satisfied
Line202 expectations:
Line203   ! expected once, never invoked: auctionEventListener.auctionClosed()
Line204 what happened before this: nothing!
Line205   at org.jmock.Mockery.assertIsSatisfied(Mockery.java:199)
Line206   […]
Line207   at org.junit.internal.runners.JUnit4ClassRunner.run()
Line208 The critical phrase is this one:
Line209 expected once, never invoked: auctionEventListener.auctionClosed()
Line210 which tells us that we haven’t called the listener as we should have.
Line211 We need to do two things to make the test pass. First, we need to connect the
Line212 translator and listener so that they can communicate. We decide to pass the lis-
Line213 tener into the translator’s constructor; it’s simple and ensures that the translator
Line214 is always set up correctly with a listener—the Java type system won’t let us forget.
Line215 The test setup looks like this:
Line216 public class AuctionMessageTranslatorTest {
Line217   private final Mockery context = new Mockery();
Line218   private final AuctionEventListener listener = 
Line219                                      context.mock(AuctionEventListener.class);
Line220   private final AuctionMessageTranslator translator = 
Line221                                        new AuctionMessageTranslator(listener);
Line222 The second thing we need to do is call the auctionClosed() method. Actually,
Line223 that’s all we need to do to make this test pass, since we haven’t deﬁned any other
Line224 behavior.
Line225 public void processMessage(Chat chat, Message message) {
Line226     listener.auctionClosed();
Line227   }
Line228 The test passes. This might feel like cheating since we haven’t actually unpacked
Line229 a message. What we have done is ﬁgured out where the pieces are and got them
Line230 into a test harness—and locked down one piece of functionality that should
Line231 continue to work as we add more features.
Line232 Chapter 12
Line233 Getting Ready to Bid
Line234 116
Line235 
Line236 
Line237 ---
Line238 
Line239 ---
Line240 **Page 117**
Line241 
Line242 Simpliﬁed Test Setup
Line243 You might have noticed that all the ﬁelds in the test class are final. As we described
Line244 in Chapter 3, JUnit creates a new instance of the test class for each test method,
Line245 so the ﬁelds are recreated for each test method. We exploit this by declaring as
Line246 many ﬁelds as possible as final and initializing them during construction, which
Line247 ﬂushes out any circular dependencies. Steve likes to think of this visually as creating
Line248 a lattice of objects that acts a frame to support the test.
Line249 Sometimes, as you’ll see later in this example, we can’t lock everything down and
Line250 have to attach a dependency directly, but most of the time we can. Any exceptions
Line251 will attract our attention and highlight a possible dependency loop. NUnit, on the
Line252 other hand, reuses the same instance of the test class, so in that case we’d have
Line253 to renew any supporting test values and objects explicitly.
Line254 Closing the User Interface Loop
Line255 Now we have the beginnings of our new component, we can retroﬁt it into
Line256 the Sniper to make sure we don’t drift too far from working code. Previously,
Line257 Main updated the Sniper user interface, so now we make it implement
Line258 AuctionEventListener and move the functionality to the new auctionClosed()
Line259 method.
Line260 public class Main implements AuctionEventListener { […]
Line261   private void joinAuction(XMPPConnection connection, String itemId) 
Line262     throws XMPPException 
Line263   {
Line264     disconnectWhenUICloses(connection);
Line265     Chat chat = connection.getChatManager().createChat(
Line266         auctionId(itemId, connection), 
Line267 new AuctionMessageTranslator(this));
Line268     chat.sendMessage(JOIN_COMMAND_FORMAT);
Line269     notToBeGCd = chat; 
Line270   }
Line271   public void auctionClosed() {
Line272     SwingUtilities.invokeLater(new Runnable() {
Line273       public void run() {
Line274         ui.showStatus(MainWindow.STATUS_LOST);
Line275       }
Line276     });
Line277   }
Line278 }
Line279 The structure now looks like Figure 12.2.
Line280 117
Line281 The AuctionMessageTranslator
Line282 
Line283 
Line284 ---
Line285 
Line286 ---
Line287 **Page 118**
Line288 
Line289 Figure 12.2
Line290 Introducing the AuctionMessageTranslator
Line291 What Have We Achieved?
Line292 In this baby step, we’ve extracted a single feature of our application into a separate
Line293 class, which means the functionality now has a name and can be unit-tested.
Line294 We’ve also made Main a little simpler, now that it’s no longer concerned with
Line295 interpreting the text of messages from the auction. This is not yet a big deal but
Line296 we will show, as the Sniper application grows, how this approach helps us keep
Line297 code clean and ﬂexible, with clear responsibilities and relationships between its
Line298 components.
Line299 Unpacking a Price Message
Line300 Introducing Message Event Types
Line301 We’re about to introduce a second auction message type, the current price update.
Line302 The Sniper needs to distinguish between the two, so we take another look at the
Line303 message formats in Chapter 9 that Southabee’s On-Line have sent us. They’re
Line304 simple—just a single line with a few name/value pairs. Here are examples for
Line305 the formats again:
Line306 SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
Line307 SOLVersion: 1.1; Event: CLOSE;
Line308 At ﬁrst, being object-oriented enthusiasts, we try to model these messages as
Line309 types, but we’re not clear enough about the behavior to justify any meaningful
Line310 structure, so we back off the idea. We decide to start with a simplistic solution
Line311 and adapt from there.
Line312 The Second Test
Line313 The introduction of a different Price event in our second test will force us to
Line314 parse the incoming message. This test has the same structure as the ﬁrst one but
Line315 gets a different input string and expects us to call a different method on the lis-
Line316 tener. A Price message includes details of the last bid, which we need to unpack
Line317 and pass to the listener, so we include them in the signature of the new method
Line318 currentPrice(). Here’s the test:
Line319 @Test public void
Line320 notifiesBidDetailsWhenCurrentPriceMessageReceived() {
Line321 Chapter 12
Line322 Getting Ready to Bid
Line323 118
Line324 
Line325 
Line326 ---
