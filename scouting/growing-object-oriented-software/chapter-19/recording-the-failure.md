Line1 # Recording the Failure (pp.221-225)
Line2 
Line3 ---
Line4 **Page 221**
Line5 
Line6 Recording the Failure
Line7 Now we want to return to the end-to-end test and the reportsInvalidMessage()
Line8 method that we parked. Our requirement is that the Sniper application must log
Line9 a message about these failures so that the user’s organization can recover the
Line10 situation. This means that our test should look for a log ﬁle and check its contents.
Line11 Filling In the Test
Line12 We implement the missing check and ﬂush the log before each test, delegating
Line13 the management of the log ﬁle to an AuctionLogDriver class which uses the
Line14 Apache Commons IO library. It also cheats slightly by resetting the log manager
Line15 (we’re not really supposed to be in the same address space), since deleting the
Line16 log ﬁle can confuse a cached logger.
Line17 public class ApplicationRunner { […]
Line18 private AuctionLogDriver logDriver = new AuctionLogDriver();
Line19   public void reportsInvalidMessage(FakeAuctionServer auction, String message)
Line20     throws IOException 
Line21   {
Line22 logDriver.hasEntry(containsString(message));
Line23   }
Line24   public void startBiddingWithStopPrice(FakeAuctionServer auction, int stopPrice) {
Line25     startSniper();
Line26     openBiddingFor(auction, stopPrice);
Line27   }  
Line28   private startSniper() {
Line29 logDriver.clearLog()
Line30     Thread thread = new Thread("Test Application") {
Line31       @Override public void run() { // Start the application […]
Line32   }
Line33 }
Line34 public class AuctionLogDriver {
Line35   public static final String LOG_FILE_NAME = "auction-sniper.log";
Line36   private final File logFile = new File(LOG_FILE_NAME);
Line37   public void hasEntry(Matcher<String> matcher) throws IOException  {
Line38     assertThat(FileUtils.readFileToString(logFile), matcher); 
Line39   }
Line40   public void clearLog() {
Line41     logFile.delete();
Line42     LogManager.getLogManager().reset(); 
Line43   }
Line44 }
Line45 This new check only reassures us that we’ve fed a message through the system
Line46 and into some kind of log record—it tells us that the pieces ﬁt together. We’ll
Line47 write a more thorough test of the contents of a log record later. The end-to-end
Line48 test now fails because, of course, there’s no log ﬁle to read.
Line49 221
Line50 Recording the Failure
Line51 
Line52 
Line53 ---
Line54 
Line55 ---
Line56 **Page 222**
Line57 
Line58 Failure Reporting in the Translator
Line59 Once again, the ﬁrst change is in the AuctionMessageTranslator. We’d like
Line60 the record to include the auction identiﬁer, the received message, and
Line61 the thrown exception. The “single responsibility” principle suggests that the
Line62 AuctionMessageTranslator should not be responsible for deciding how to report
Line63 the event, so we invent a new collaborator to handle this task. We call it
Line64 XMPPFailureReporter:
Line65 public interface XMPPFailureReporter {
Line66   void cannotTranslateMessage(String auctionId, String failedMessage, 
Line67                               Exception exception);
Line68 }
Line69 We amend our existing failure tests, wrapping up message creation and common
Line70 expectations in helper methods, for example:
Line71 @Test public void
Line72 notifiesAuctionFailedWhenBadMessageReceived() {
Line73   String badMessage = "a bad message";
Line74 expectFailureWithMessage(badMessage);
Line75   translator.processMessage(UNUSED_CHAT, message(badMessage));
Line76 }
Line77 private Message message(String body) {
Line78   Message message = new Message();
Line79   message.setBody(body);
Line80   return message;
Line81 }
Line82 private void expectFailureWithMessage(final String badMessage) {
Line83   context.checking(new Expectations() {{  
Line84     oneOf(listener).auctionFailed(); 
Line85 oneOf(failureReporter).cannotTranslateMessage(
Line86                              with(SNIPER_ID), with(badMessage),
Line87                              with(any(Exception.class)));
Line88   }});
Line89 }
Line90 The new reporter is a dependency for the translator, so we feed it in through
Line91 the constructor and call it just before notifying any listeners. We know that
Line92 message.getBody() will not throw an exception, it’s just a simple bean, so we
Line93 can leave it outside the catch block.
Line94 public class AuctionMessageTranslator implements MessageListener {
Line95   public void processMessage(Chat chat, Message message) {
Line96     String messageBody = message.getBody();
Line97     try {
Line98       translate(messageBody);
Line99     } catch (RuntimeException exception) {
Line100 failureReporter.cannotTranslateMessage(sniperId, messageBody, exception);
Line101       listener.auctionFailed();
Line102     }
Line103   }  […]
Line104 The unit test passes.
Line105 Chapter 19
Line106 Handling Failure
Line107 222
Line108 
Line109 
Line110 ---
Line111 
Line112 ---
Line113 **Page 223**
Line114 
Line115 Generating the Log Message
Line116 The next stage is to implement the XMPPFailureReporter with something that
Line117 generates a log ﬁle. This is where we actually check the format and contents of
Line118 a log entry. We start a class LoggingXMPPFailureReporter and decide to use Java’s
Line119 built-in logging framework. We could make the tests for this new class write and
Line120 read from a real ﬁle. Instead, we decide that ﬁle access is sufﬁciently covered by
Line121 the end-to-end test we’ve just set up, so we’ll run everything in memory to
Line122 reduce the test’s dependencies. We’re conﬁdent we can take this shortcut, because
Line123 the example is so simple; for more complex behavior we would write some
Line124 integration tests.
Line125 The Java logging framework has no interfaces, so we have to be more concrete
Line126 than we’d like. Exceptionally, we decide to use a class-based mock to override
Line127 the relevant method in Logger; in jMock we turn on class-based mocking
Line128 with the setImposteriser() call. The AfterClass annotation tells JUnit to call
Line129 resetLogging() after all the tests have run to ﬂush any changes we might have
Line130 made to the logging environment.
Line131 @RunWith(JMock.class)
Line132 public class LoggingXMPPFailureReporterTest {
Line133   private final Mockery context = new Mockery() {{
Line134 setImposteriser(ClassImposteriser.INSTANCE);
Line135   }};
Line136   final Logger logger = context.mock(Logger.class);
Line137   final LoggingXMPPFailureReporter reporter = new LoggingXMPPFailureReporter(logger);
Line138 @AfterClass
Line139   public static void resetLogging() {
Line140     LogManager.getLogManager().reset();
Line141   }
Line142   @Test public void
Line143 writesMessageTranslationFailureToLog() {
Line144     context.checking(new Expectations() {{
Line145       oneOf(logger).severe("<auction id> "
Line146                          + "Could not translate message \"bad message\" "
Line147                          + "because \"java.lang.Exception: bad\"");
Line148     }});
Line149     reporter.cannotTranslateMessage("auction id", "bad message", new Exception("bad"));
Line150   }
Line151 }
Line152 We pass this test with an implementation that just calls the logger with a string
Line153 formatted from the inputs to cannotTranslateMessage().
Line154 Breaking Our Own Rules?
Line155 We already wrote that we don’t like to mock classes, and we go on about it further
Line156 in Chapter 20. So, how come we’re doing it here?
Line157 223
Line158 Recording the Failure
Line159 
Line160 
Line161 ---
Line162 
Line163 ---
Line164 **Page 224**
Line165 
Line166 What we care about in this test is the rendering of the values into a failure message
Line167 with a severity level. The class is very limited, just a shim above the logging layer,
Line168 so we don’t think it’s worth introducing another level of indirection to deﬁne the
Line169 logging role. As we wrote before, we also don’t think it worth running against a real
Line170 ﬁle since that introduces dependencies (and, even worse, asynchrony) not really
Line171 relevant to the functionality we’re developing. We also believe that, as part of the
Line172 Java runtime, the logging API is unlikely to change.
Line173 So, just this once, as a special favor, setting no precedents, making no promises,
Line174 we mock the Logger class. There are a couple more points worth making before we
Line175 move on. First, we would not do this for a class that is internal to our code, because
Line176 then we would be able write an interface to describe the role it’s playing. Second,
Line177 if the LoggingXMPPFailureReporter were to grow in complexity, we would probably
Line178 ﬁnd ourselves discovering a supporting message formatter class that could be
Line179 tested directly.
Line180 Closing the Loop
Line181 Now we have the pieces in place to make the whole end-to-end test pass. We
Line182 plug an instance of the LoggingXMPPFailureReporter into the XMPPAuctionHouse
Line183 so that, via its XMPPAuctions, every AuctionMessageTranslator is constructed
Line184 with the reporter. We also move the constant that deﬁnes the log ﬁle name there
Line185 from AuctionLogDriver, and deﬁne a new XMPPAuctionException to gather up
Line186 any failures within the package.
Line187 public class XMPPAuctionHouse implements AuctionHouse {
Line188   public XMPPAuctionHouse(XMPPConnection connection) 
Line189     throws XMPPAuctionException 
Line190   {
Line191     this.connection = connection;
Line192 this.failureReporter = new LoggingXMPPFailureReporter(makeLogger());
Line193   }
Line194   public Auction auctionFor(String itemId) {
Line195     return new XMPPAuction(connection, auctionId(itemId, connection), failureReporter);
Line196   } 
Line197   private Logger makeLogger() throws XMPPAuctionException {
Line198     Logger logger = Logger.getLogger(LOGGER_NAME);
Line199     logger.setUseParentHandlers(false);
Line200     logger.addHandler(simpleFileHandler());
Line201     return logger;
Line202   }
Line203   private FileHandler simpleFileHandler() throws XMPPAuctionException {
Line204     try {
Line205       FileHandler handler = new FileHandler(LOG_FILE_NAME);
Line206       handler.setFormatter(new SimpleFormatter());
Line207       return handler;
Line208     } catch (Exception e) {
Line209       throw new XMPPAuctionException("Could not create logger FileHandler " 
Line210                                    + getFullPath(LOG_FILE_NAME), e);
Line211     }
Line212   } […]
Line213 Chapter 19
Line214 Handling Failure
Line215 224
Line216 
Line217 
Line218 ---
Line219 
Line220 ---
Line221 **Page 225**
Line222 
Line223 The end-to-end test passes completely and we can cross another item off our
Line224 list: Figure 19.2.
Line225 Figure 19.2
Line226 The Sniper reports failed messages from an auction
Line227 Observations
Line228 “Inverse Salami” Development
Line229 We hope that by now you’re getting a sense of the rhythm of incrementally
Line230 growing software, adding functionality in thin but coherent slices. For each new
Line231 feature, write some tests that show what it should do, work through each of
Line232 those tests changing just enough code to make it pass, restructure the code as
Line233 needed either to open up space for new functionality or to reveal new
Line234 concepts—then ship it. We discuss how this ﬁts into the larger development picture
Line235 in Chapter 5. In static languages, such as Java and C#, we can often use the
Line236 compiler to help us navigate the chain of implementation dependencies: change
Line237 the code to accept the new triggering event, see what breaks, ﬁx that breakage,
Line238 see what that change breaks in turn, and repeat the process until the
Line239 functionality works.
Line240 The skill is in learning how to divide requirements up into incremental slices,
Line241 always having something working, always adding just one more feature. The
Line242 process should feel relentless—it just keeps moving. To make this work, we have
Line243 to understand how to change the code incrementally and, critically, keep the
Line244 code well structured so that we can take it wherever we need to go (and we
Line245 don’t know where that is yet). This is why the refactoring part of a test-driven
Line246 225
Line247 Observations
Line248 
Line249 
Line250 ---
