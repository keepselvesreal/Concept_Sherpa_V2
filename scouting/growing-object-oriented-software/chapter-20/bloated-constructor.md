Line1 # Bloated Constructor (pp.238-240)
Line2 
Line3 ---
Line4 **Page 238**
Line5 
Line6 Here, it’s not worth creating an interface/implementation pair to control which
Line7 time values are returned; just create instances with the appropriate times and
Line8 use them.
Line9 There are a couple of heuristics for when a class is likely to be a value and so
Line10 not worth mocking. First, its values are immutable—although that might also
Line11 mean that it’s an adjustment object, as described in “Object Peer Stereotypes”
Line12 (page 52). Second, we can’t think of a meaningful name for a class that would
Line13 implement an interface for the type. If Video were an interface, what would we
Line14 call its class other than VideoImpl or something equally vague? We discuss class
Line15 naming in “Impl Classes Are Meaningless” on page 63.
Line16 If you’re tempted to mock a value because it’s too complicated to set up an
Line17 instance, consider writing a builder; see Chapter 22.
Line18 Bloated Constructor
Line19 Sometimes during the TDD process, we end up with a constructor that has a
Line20 long, unwieldy list of arguments. We most likely got there by adding the object’s
Line21 dependencies one at a time, and it got out of hand. This is not dreadful, since
Line22 the process helped us sort out the design of the class and its neighbors, but now
Line23 it’s time to clean up. We will still need the functionality that depends on all the
Line24 current constructor arguments, so we should see if there’s any implicit structure
Line25 there that we can tease out.
Line26 One possibility is that some of the arguments together deﬁne a concept that
Line27 should be packaged up and replaced with a new object to represent it. Here’s a
Line28 small example:
Line29 public class MessageProcessor {
Line30   public MessageProcessor(MessageUnpacker unpacker, 
Line31                           AuditTrail auditor, 
Line32                           CounterPartyFinder counterpartyFinder,
Line33                           LocationFinder locationFinder,
Line34                           DomesticNotifier domesticNotifier,
Line35                           ImportedNotifier importedNotifier) 
Line36   {
Line37 // set the fields here
Line38   }
Line39   public void onMessage(Message rawMessage) {
Line40     UnpackedMessage unpacked = unpacker.unpack(rawMessage, counterpartyFinder);
Line41     auditor.recordReceiptOf(unpacked);
Line42 // some other activity here
Line43     if (locationFinder.isDomestic(unpacked)) {
Line44       domesticNotifier.notify(unpacked.asDomesticMessage());
Line45     } else {
Line46       importedNotifier.notify(unpacked.asImportedMessage())
Line47     }
Line48   }
Line49 }
Line50 Chapter 20
Line51 Listening to the Tests
Line52 238
Line53 
Line54 
Line55 ---
Line56 
Line57 ---
Line58 **Page 239**
Line59 
Line60 Just the thought of writing expectations for all these objects makes us wilt,
Line61 which suggests that things are too complicated. A ﬁrst step is to notice that the
Line62 unpacker and counterpartyFinder are always used together—they’re ﬁxed at
Line63 construction and one calls the other. We can remove one argument by pushing
Line64 the counterpartyFinder into the unpacker.
Line65 public class MessageProcessor {
Line66   public MessageProcessor(MessageUnpacker unpacker, 
Line67                           AuditTrail auditor, 
Line68                           LocationFinder locationFinder,
Line69                           DomesticNotifier domesticNotifier,
Line70                           ImportedNotifier importedNotifier) { […]
Line71   public void onMessage(Message rawMessage) {
Line72     UnpackedMessage unpacked = unpacker.unpack(rawMessage);
Line73 // etc.
Line74   }
Line75 Then there’s the triple of locationFinder and the two notiﬁers, which seem
Line76 to go together. It might make sense to package them into a MessageDispatcher.
Line77 public class MessageProcessor {
Line78   public MessageProcessor(MessageUnpacker unpacker, 
Line79                           AuditTrail auditor, 
Line80 MessageDispatcher dispatcher) { […]
Line81   public void onMessage(Message rawMessage) {
Line82     UnpackedMessage unpacked = unpacker.unpack(rawMessage);
Line83     auditor.recordReceiptOf(unpacked);
Line84 // some other activity here
Line85 dispatcher.dispatch(unpacked);
Line86   }
Line87 }
Line88 Although we’ve forced this example to ﬁt within a section, it shows that being
Line89 sensitive to complexity in the tests can help us clarify our designs. Now we have
Line90 a message handling object that clearly performs the usual three stages:
Line91 receive, process, and forward. We’ve pulled out the message routing code (the
Line92 MessageDispatcher), so the MessageProcessor has fewer responsibilities and we
Line93 know where to put routing decisions when things get more complicated. You
Line94 might also notice that this code is easier to unit-test.
Line95 When extracting implicit components, we start by looking for two conditions:
Line96 arguments that are always used together in the class, and those that have the
Line97 same lifetime. Once we’ve found a coincidence, we have the harder task of ﬁnding
Line98 a good name that explains the concept.
Line99 As an aside, one sign that a design is developing nicely is that this kind of
Line100 change is easy to integrate. All we have to do is ﬁnd where the MessageProcessor
Line101 is created and change this:
Line102 239
Line103 Bloated Constructor
Line104 
Line105 
Line106 ---
Line107 
Line108 ---
Line109 **Page 240**
Line110 
Line111 messageProcessor = 
Line112   new MessageProcessor(new XmlMessageUnpacker(), 
Line113                        auditor, counterpartyFinder, 
Line114                        locationFinder, domesticNotifier,
Line115                        importedNotifier);
Line116 to this:
Line117 messageProcessor = 
Line118   new MessageProcessor(new XmlMessageUnpacker(counterpartyFinder),
Line119                        auditor,
Line120 new MessageDispatcher(
Line121                          locationFinder, 
Line122                          domesticNotifier, importedNotifier));
Line123 Later we can reduce the syntax noise by extracting out the creation of the
Line124 MessageDispatcher.
Line125 Confused Object
Line126 Another diagnosis for a “bloated constructor” might be that the object itself is
Line127 too large because it has too many responsibilities. For example,
Line128 public class Handset {
Line129   public Handset(Network network, Camera camera, Display display, 
Line130                 DataNetwork dataNetwork, AddressBook addressBook,
Line131                 Storage storage, Tuner tuner, …)
Line132   {
Line133 // set the fields here
Line134   }
Line135   public void placeCallTo(DirectoryNumber number) { 
Line136     network.openVoiceCallTo(number);
Line137   }
Line138   public void takePicture() { 
Line139     Frame frame = storage.allocateNewFrame();
Line140     camera.takePictureInto(frame);
Line141     display.showPicture(frame);
Line142   }
Line143   public void showWebPage(URL url) {
Line144     display.renderHtml(dataNetwork.retrievePage(url));
Line145   }
Line146   public void showAddress(SearchTerm searchTerm) {
Line147     display.showAddress(addressBook.findAddress(searchTerm));
Line148   } 
Line149   public void playRadio(Frequency frequency) {
Line150     tuner.tuneTo(frequency);
Line151     tuner.play();
Line152   }
Line153 // and so on
Line154 }
Line155 Like our mobile phones, this class has several unrelated responsibilities which
Line156 force it to pull in many dependencies. And, like our phones, the class is confusing
Line157 to use because unrelated features interfere with each other. We’re prepared to
Line158 Chapter 20
Line159 Listening to the Tests
Line160 240
Line161 
Line162 
Line163 ---
