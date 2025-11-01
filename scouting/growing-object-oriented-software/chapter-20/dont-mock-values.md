Line1 # Don't Mock Values (pp.237-238)
Line2 
Line3 ---
Line4 **Page 237**
Line5 
Line6 There’s a more subtle but powerful reason for not mocking concrete classes.
Line7 When we extract an interface as part of our test-driven development process, we
Line8 have to think up a name to describe the relationship we’ve just discovered—in
Line9 this example, the ScheduledDevice. We ﬁnd that this makes us think harder about
Line10 the domain and teases out concepts that we might otherwise miss. Once something
Line11 has a name, we can talk about it.
Line12 “Break Glass in Case of Emergency”
Line13 There are a few occasions when we have to put up with this smell. The least un-
Line14 acceptable situation is where we’re working with legacy code that we control
Line15 but can’t change all at once. Alternatively, we might be working with third-party
Line16 code that we can’t change at all (see Chapter 8). We ﬁnd that it’s almost always
Line17 better to write a veneer over an external library rather than mock it directly—but
Line18 occasionally, it’s just not worth it. We broke the rule with Logger in Chapter 19
Line19 but apologized a lot and felt bad about it. In any case, these are unfortunate but
Line20 necessary compromises that we would try to work our way out of when possible.
Line21 The longer we leave them in the code, the more likely it is that some brittleness
Line22 in the design will cause us grief.
Line23 Above all, do not override a class’ internal features—this just locks down your
Line24 test to the quirks of the current implementation. Only override visible methods.
Line25 This rule also prohibits exposing internal methods just to override them in a test.
Line26 If you can’t get to the structure you need, then the tests are telling you that it’s
Line27 time to break up the class into smaller, composable features.
Line28 Don’t Mock Values
Line29 There’s no point in writing mocks for values (which should be immutable any-
Line30 way). Just create an instance and use it. For example, in this test Video holds
Line31 details of a part of a show:
Line32 @Test public void sumsTotalRunningTime() {
Line33   Show show = new Show();
Line34   Video video1 = context.mock(Video.class); // Don't do this
Line35   Video video2 = context.mock(Video.class);
Line36   context.checking(new Expectations(){{
Line37     one(video1).time(); will(returnValue(40));
Line38     one(video2).time(); will(returnValue(23));
Line39   }});
Line40   show.add(video1);
Line41   show.add(video2);
Line42   assertEqual(63, show.runningTime())
Line43 }
Line44 237
Line45 Don’t Mock Values
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 238**
Line52 
Line53 Here, it’s not worth creating an interface/implementation pair to control which
Line54 time values are returned; just create instances with the appropriate times and
Line55 use them.
Line56 There are a couple of heuristics for when a class is likely to be a value and so
Line57 not worth mocking. First, its values are immutable—although that might also
Line58 mean that it’s an adjustment object, as described in “Object Peer Stereotypes”
Line59 (page 52). Second, we can’t think of a meaningful name for a class that would
Line60 implement an interface for the type. If Video were an interface, what would we
Line61 call its class other than VideoImpl or something equally vague? We discuss class
Line62 naming in “Impl Classes Are Meaningless” on page 63.
Line63 If you’re tempted to mock a value because it’s too complicated to set up an
Line64 instance, consider writing a builder; see Chapter 22.
Line65 Bloated Constructor
Line66 Sometimes during the TDD process, we end up with a constructor that has a
Line67 long, unwieldy list of arguments. We most likely got there by adding the object’s
Line68 dependencies one at a time, and it got out of hand. This is not dreadful, since
Line69 the process helped us sort out the design of the class and its neighbors, but now
Line70 it’s time to clean up. We will still need the functionality that depends on all the
Line71 current constructor arguments, so we should see if there’s any implicit structure
Line72 there that we can tease out.
Line73 One possibility is that some of the arguments together deﬁne a concept that
Line74 should be packaged up and replaced with a new object to represent it. Here’s a
Line75 small example:
Line76 public class MessageProcessor {
Line77   public MessageProcessor(MessageUnpacker unpacker, 
Line78                           AuditTrail auditor, 
Line79                           CounterPartyFinder counterpartyFinder,
Line80                           LocationFinder locationFinder,
Line81                           DomesticNotifier domesticNotifier,
Line82                           ImportedNotifier importedNotifier) 
Line83   {
Line84 // set the fields here
Line85   }
Line86   public void onMessage(Message rawMessage) {
Line87     UnpackedMessage unpacked = unpacker.unpack(rawMessage, counterpartyFinder);
Line88     auditor.recordReceiptOf(unpacked);
Line89 // some other activity here
Line90     if (locationFinder.isDomestic(unpacked)) {
Line91       domesticNotifier.notify(unpacked.asDomesticMessage());
Line92     } else {
Line93       importedNotifier.notify(unpacked.asImportedMessage())
Line94     }
Line95   }
Line96 }
Line97 Chapter 20
Line98 Listening to the Tests
Line99 238
Line100 
Line101 
Line102 ---
