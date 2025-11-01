# Chapter 20: Listening to the Tests (pp.229-246)

---
**Page 229**

Chapter 20
Listening to the Tests
You can see a lot just by observing.
—Yogi Berra
Introduction
Sometimes we ﬁnd it difﬁcult to write a test for some functionality we want to
add to our code. In our experience, this usually means that our design can be
improved—perhaps the class is too tightly coupled to its environment or does
not have clear responsibilities. When this happens, we ﬁrst check whether it’s an
opportunity to improve our code, before working around the design by making
the test more complicated or using more sophisticated tools. We’ve found
that the qualities that make an object easy to test also make our code responsive
to change.
The trick is to let our tests drive our design (that’s why it’s called test-driven
development). TDD is about testing code, verifying its externally visible qualities
such as functionality and performance. TDD is also about feedback on the code’s
internal qualities: the coupling and cohesion of its classes, dependencies that are
explicit or hidden, and effective information hiding—the qualities that keep the
code maintainable.
With practice, we’ve become more sensitive to the rough edges in our tests, so
we can use them for rapid feedback about the design. Now when we ﬁnd a feature
that’s difﬁcult to test, we don’t just ask ourselves how to test it, but also why is
it difﬁcult to test.
In this chapter, we look at some common “test smells” that we’ve encountered
and discuss what they might imply about the design of the code. There are two
categories of test smell to consider. One is where the test itself is not well
written—it may be unclear or brittle. Meszaros [Meszaros07] covers several such
patterns in his “Test Smells” chapter. This chapter is concerned with the other
category, where a test is highlighting that the target code is the problem. Meszaros
has one pattern for this, called “Hard-to-Test Code.” We’ve picked out some
common cases that we’ve seen that are relevant to our approach to TDD.
229


---
**Page 230**

I Need to Mock an Object I Can’t Replace (without Magic)
Singletons Are Dependencies
One interpretation of reducing complexity in code is making commonly useful
objects accessible through a global structure, usually implemented as a singleton.
Any code that needs access to a feature can just refer to it by its global name
instead of receiving it as an argument. Here’s a common example:
Date now = new Date();
Under the covers, the constructor calls the singleton System and sets the new
instance to the current time using System.currentTimeMillis(). This is a conve-
nient technique, but it comes at a cost. Let’s say we want to write a test like this:
@Test public void rejectsRequestsNotWithinTheSameDay() {
  receiver.acceptRequest(FIRST_REQUEST);
// the next day
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
The implementation looks like this:
public boolean acceptRequest(Request request) {
  final Date now = new Date();
  if (dateOfFirstRequest == null) {
    dateOfFirstRequest = now;
   } else if (firstDateIsDifferentFrom(now)) {
    return false;
  }
// process the request
  return true;
}
where dateOfFirstRequest is a ﬁeld and firstDateIsDifferentFrom() is a helper
method that hides the unpleasantness of working with the Java date library.
To test this timeout, we must either make the test wait overnight or do some-
thing clever (perhaps with aspects or byte-code manipulation) to intercept the
constructor and return suitable Date values for the test. This difﬁculty in testing
is a hint that we should change the code. To make the test easier, we need to
control how Date objects are created, so we introduce a Clock and pass it into
the Receiver. If we stub Clock, the test might look like this:
@Test public void rejectsRequestsNotWithinTheSameDay() {
  Receiver receiver = new Receiver(stubClock);
  stubClock.setNextDate(TODAY);
  receiver.acceptRequest(FIRST_REQUEST);
  stubClock.setNextDate(TOMORROW);
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
Chapter 20
Listening to the Tests
230


---
**Page 231**

and the implementation like this:
public boolean acceptRequest(Request request) {
  final Date now = clock.now();
  if (dateOfFirstRequest == null) {
   dateOfFirstRequest = now;
  } else if (firstDateIsDifferentFrom(now)) {
   return false;
  }
// process the request
  return true;
}
Now we can test the Receiver without any special tricks. More importantly,
however, we’ve made it obvious that Receiver is dependent on time—we can’t
even create one without a Clock. Some argue that this is breaking encapsulation
by exposing the internals of a Receiver—we should be able to just create an in-
stance and not worry—but we’ve seen so many systems that are impossible to
test because the developers did not isolate the concept of time. We want to know
about this dependency, especially when the service is rolled out across the world,
and New York and London start complaining about different results.
From Procedures to Objects
Having taken the trouble to introduce a Clock object, we start wondering if our
code is missing a concept: date checking in terms of our domain. A Receiver
doesn’t need to know all the details of a calendar system, such as time zones and
locales; it just need to know if the date has changed for this application. There’s
a clue in the fragment:
firstDateIsDifferentFrom(now)
which means that we’ve had to wrap up some date manipulation code in Receiver.
It’s the wrong object; that kind of work should be done in Clock. We write the
test again:
@Test public void rejectsRequestsNotWithinTheSameDay() {
  Receiver receiver = new Receiver(clock);
  context.checking(new Expectations() {{
   allowing(clock).now(); will(returnValue(NOW));
one(clock).dayHasChangedFrom(NOW); will(returnValue(false));
  }});
  receiver.acceptRequest(FIRST_REQUEST);
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
The implementation looks like this:
231
I Need to Mock an Object I Can’t Replace (without Magic)


---
**Page 232**

public boolean acceptRequest(Request request) {
  if (dateOfFirstRequest == null) {
   dateOfFirstRequest = clock.now();
  } else if (clock.dayHasChangedFrom(dateOfFirstRequest)) {
   return false;
  }
// process the request
  return true;
}
This version of Receiver is more focused: it doesn’t need to know how to dis-
tinguish one date from another and it only needs to get a date to set the ﬁrst
value. The Clock interface deﬁnes exactly those date services Receiver needs from
its environment.
But we think we can push this further. Receiver only retains a date so that it
can detect a change of day; perhaps we should delegate all the date functionality
to another object which, for want of a better name, we’ll call a SameDayChecker.
@Test public void rejectsRequestsOutsideAllowedPeriod() {
  Receiver receiver = new Receiver(sameDayChecker);
  context.checking(new Expectations() {{
allowing(sameDayChecker).hasExpired(); will(returnValue(false));
  }});
  assertFalse("too late now", receiver.acceptRequest(REQUEST));
}
with an implementation like this:
public boolean acceptRequest(Request request) {
  if (sameDayChecker.hasExpired()) {
   return false;
  }
// process the request
  return true;
}
All the logic about dates has been separated out from Receiver, which can
concentrate on processing the request. With two objects, we can make sure that
each behavior (date checking and request processing) is unit-tested cleanly.
Implicit Dependencies Are Still Dependencies
We can hide a dependency from the caller of a component by using a global
value to bypass encapsulation, but that doesn’t make the dependency go away—it
just makes it inaccessible. For example, Steve once had to work with a Microsoft
.Net library that couldn’t be loaded without installing ActiveDirectory—which
wasn’t actually required for the features he wanted to use and which he couldn’t
install on his machine anyway. The library developer was trying to be helpful
and to make it “just work,” but the result was that Steve couldn’t get it to work
at all.
Chapter 20
Listening to the Tests
232


---
**Page 233**

One goal of object orientation as a technique for structuring code is to make
the boundaries of an object clearly visible. An object should only deal with values
and instances that are either local—created and managed within its scope—or
passed in explicitly, as we emphasized in “Context Independence” (page 54).
In the example above, the act of making date checking testable forced us to
make the Receiver’s requirements more explicit and to think more clearly about
the domain.
Use the Same Techniques to Break Dependencies in Unit Tests
as in Production Code
There are several frameworks available that use techniques such as manipulating
class loaders or bytecodes to allow unit tests to break dependencies without
changing the target code. As a rule, these are advanced techniques that most
developers would not use when writing production code. Sometimes these tools
really are necessary, but developers should be aware that they come with a
hidden cost.
Unit-testing tools that let the programmer sidestep poor dependency management
in the design waste a valuable source of feedback.When the developers eventually
do need to address these design weaknesses to add some urgent feature, they
will ﬁnd it harder to do. The poor structure will have inﬂuenced other parts of the
system that rely on it, and any understanding of the original intent will have
evaporated. As with dirty pots and pans, it’s easier to get the grease off before it’s
been baked in.
Logging Is a Feature
We have a more contentious example of working with objects that are hard to
replace: logging. Take a look at these two lines of code:
log.error("Lost touch with Reality after " + timeout + "seconds");
log.trace("Distance traveled in the wilderness: " + distance);
These are two separate features that happen to share an implementation. Let
us explain.
•
Support logging (errors and info) is part of the user interface of the appli-
cation. These messages are intended to be tracked by support staff, as well
as perhaps system administrators and operators, to diagnose a failure or
monitor the progress of the running system.
•
Diagnostic logging (debug and trace) is infrastructure for programmers.
These messages should not be turned on in production because they’re in-
tended to help the programmers understand what’s going on inside the
system they’re developing.
233
Logging Is a Feature


---
**Page 234**

Given this distinction, we should consider using different techniques for these
two type of logging. Support logging should be test-driven from somebody’s re-
quirements, such as auditing or failure recovery. The tests will make sure we’ve
thought about what each message is for and made sure it works. The tests will
also protect us from breaking any tools and scripts that other people write to
analyze these log messages. Diagnostic logging, on the other hand, is driven by
the programmers’ need for ﬁne-grained tracking of what’s happening in the sys-
tem. It’s scaffolding—so it probably doesn’t need to be test-driven and the mes-
sages might not need to be as consistent as those for support logs. After all, didn’t
we just agree that these messages are not to be used in production?
Notiﬁcation Rather Than Logging
To get back to the point of the chapter, writing unit tests against static global
objects, including loggers, is clumsy. We have to either read from the ﬁle system
or manage an extra appender object for testing; we have to remember to clean
up afterwards so that tests don’t interfere with each other and set the right level
on the right logger. The noise in the test reminds us that our code is working at
two levels: our domain and the logging infrastructure. Here’s a common example
of code with logging:
Location location = tracker.getCurrentLocation();
for (Filter filter : filters) {
  filter.selectFor(location);
if (logger.isInfoEnabled()) {
    logger.info("Filter " + filter.getName() + ", " + filter.getDate()
                 + " selected for " + location.getName() 
                 + ", is current: " + tracker.isCurrent(location));
  }
}
Notice the shift in vocabulary and style between the functional part of the
loop and the (emphasized) logging part. The code is doing two things at
once—something to do with locations and rendering support information—which
breaks the single responsibility principle. Maybe we could do this instead:
Location location = tracker.getCurrentLocation();
for (Filter filter : filters) {
  filter.selectFor(location);
support.notifyFiltering(tracker, location, filter);}
where the support object might be implemented by a logger, a message bus,
pop-up windows, or whatever’s appropriate; this detail is not relevant to the
code at this level.
This code is also easier to test, as you saw in Chapter 19. We, not the logging
framework, own the support object, so we can pass in a mock implementation
at our convenience and keep it local to the test case. The other simpliﬁcation is
that now we’re testing for objects, rather than formatted contents of a string. Of
Chapter 20
Listening to the Tests
234


---
**Page 235**

course, we will still need to write an implementation of support and some focused
integration tests to go with it.
But That’s Crazy Talk…
The idea of encapsulating support reporting sounds like over-design, but it’s
worth thinking about for a moment. It means we’re writing code in terms of our
intent (helping the support people) rather than implementation (logging), so it’s
more expressive. All the support reporting is handled in a few known places, so
it’s easier to be consistent about how things are reported and to encourage reuse.
It can also help us structure and control our reporting in terms of the application
domain, rather than in terms of Java packages. Finally, the act of writing a test
for each report helps us avoid the “I don’t know what to do with this exception,
so I’ll log it and carry on” syndrome, which leads to log bloat and production
failures because we haven’t handled obscure error conditions.
One objection we’ve heard is, “I can’t pass in a logger for testing because I’ve
got logging all over my domain objects. I’d have to pass one around everywhere.”
We think this is a test smell that is telling us that we haven’t clariﬁed our design
enough. Perhaps some of our support logging should really be diagnostic logging,
or we’re logging more than we need because of something that we wrote when
we hadn’t yet understood the behavior. Most likely, there’s still too much dupli-
cation in our domain code and we haven’t yet found the “choke points” where
most of the production logging should go.
So what about diagnostic logging? Is it disposable scaffolding that should be
taken down once the job is done, or essential infrastructure that should be tested
and maintained? That depends on the system, but once we’ve made the distinction
we have more freedom to think about using different techniques for support and
diagnostic logging. We might even decide that in-line code is the wrong technique
for diagnostic logging because it interferes with the readability of the production
code that matters. Perhaps we could weave in some aspects instead (since that’s
the canonical example of their use); perhaps not—but at least we’ve now
clariﬁed the choice.
One ﬁnal data point. One of us once worked on a system where so much
content was written to the logs that they had to be deleted after a week to ﬁt on
the disks. This made maintenance very difﬁcult as the relevant logs were usually
gone by the time a bug was assigned to be ﬁxed. If they’d logged nothing at all,
the system would have run faster with no loss of useful information.
Mocking Concrete Classes
One approach to interaction testing is to mock concrete classes rather than inter-
faces. The technique is to inherit from the class you want to mock and override
the methods that will be called within the test, either manually or with any of
235
Mocking Concrete Classes


---
**Page 236**

the mocking frameworks. We think this is a technique that should be used only
when you really have no other options.
Here’s an example of mocking by hand. The test veriﬁes that the music centre
starts the CD player at the requested time. Assume that setting the schedule on
a CdPlayer object involves triggering some behavior we don’t want in the test,
so we override scheduleToStartAt() and verify afterwards that we’ve called it
with the right argument.
public class MusicCentreTest {
  @Test public void 
startsCdPlayerAtTimeRequested() {
    final MutableTime scheduledTime = new MutableTime();
    CdPlayer player = new CdPlayer() {
      @Override public void scheduleToStartAt(Time startTime) {
        scheduledTime.set(startTime);
      }
    }
    MusicCentre centre = new MusicCentre(player);
    centre.startMediaAt(LATER);
    assertEquals(LATER, scheduledTime.get());
  }
}
The problem with this approach is that it leaves the relationship between the
CdPlayer and MusicCentre implicit. We hope we’ve made clear by now that our
intention in test-driven development is to use mock objects to bring out relation-
ships between objects. If we subclass, there’s nothing in the domain code to make
such a relationship visible—just methods on an object. This makes it harder to
see if the service that supports this relationship might be relevant elsewhere, and
we’ll have to do the analysis again next time we work with the class. To make
the point, here’s a possible implementation of CdPlayer:
public class CdPlayer {
  public void scheduleToStartAt(Time startTime) { […]
  public void stop() { […]
  public void gotoTrack(int trackNumber) { […]
  public void spinUpDisk() { […]
  public void eject() { […]
}
It turns out that our MusicCentre only uses the starting and stopping methods
on the CdPlayer; the rest are used by some other part of the system. We would
be overspecifying the MusicCentre by requiring it to talk to a CdPlayer; what it
actually needs is a ScheduledDevice. Robert Martin made the point (back in
1996) in his Interface Segregation Principle that “Clients should not be forced
to depend upon interfaces that they do not use,” but that’s exactly what we do
when we mock a concrete class.
Chapter 20
Listening to the Tests
236


---
**Page 237**

There’s a more subtle but powerful reason for not mocking concrete classes.
When we extract an interface as part of our test-driven development process, we
have to think up a name to describe the relationship we’ve just discovered—in
this example, the ScheduledDevice. We ﬁnd that this makes us think harder about
the domain and teases out concepts that we might otherwise miss. Once something
has a name, we can talk about it.
“Break Glass in Case of Emergency”
There are a few occasions when we have to put up with this smell. The least un-
acceptable situation is where we’re working with legacy code that we control
but can’t change all at once. Alternatively, we might be working with third-party
code that we can’t change at all (see Chapter 8). We ﬁnd that it’s almost always
better to write a veneer over an external library rather than mock it directly—but
occasionally, it’s just not worth it. We broke the rule with Logger in Chapter 19
but apologized a lot and felt bad about it. In any case, these are unfortunate but
necessary compromises that we would try to work our way out of when possible.
The longer we leave them in the code, the more likely it is that some brittleness
in the design will cause us grief.
Above all, do not override a class’ internal features—this just locks down your
test to the quirks of the current implementation. Only override visible methods.
This rule also prohibits exposing internal methods just to override them in a test.
If you can’t get to the structure you need, then the tests are telling you that it’s
time to break up the class into smaller, composable features.
Don’t Mock Values
There’s no point in writing mocks for values (which should be immutable any-
way). Just create an instance and use it. For example, in this test Video holds
details of a part of a show:
@Test public void sumsTotalRunningTime() {
  Show show = new Show();
  Video video1 = context.mock(Video.class); // Don't do this
  Video video2 = context.mock(Video.class);
  context.checking(new Expectations(){{
    one(video1).time(); will(returnValue(40));
    one(video2).time(); will(returnValue(23));
  }});
  show.add(video1);
  show.add(video2);
  assertEqual(63, show.runningTime())
}
237
Don’t Mock Values


---
**Page 238**

Here, it’s not worth creating an interface/implementation pair to control which
time values are returned; just create instances with the appropriate times and
use them.
There are a couple of heuristics for when a class is likely to be a value and so
not worth mocking. First, its values are immutable—although that might also
mean that it’s an adjustment object, as described in “Object Peer Stereotypes”
(page 52). Second, we can’t think of a meaningful name for a class that would
implement an interface for the type. If Video were an interface, what would we
call its class other than VideoImpl or something equally vague? We discuss class
naming in “Impl Classes Are Meaningless” on page 63.
If you’re tempted to mock a value because it’s too complicated to set up an
instance, consider writing a builder; see Chapter 22.
Bloated Constructor
Sometimes during the TDD process, we end up with a constructor that has a
long, unwieldy list of arguments. We most likely got there by adding the object’s
dependencies one at a time, and it got out of hand. This is not dreadful, since
the process helped us sort out the design of the class and its neighbors, but now
it’s time to clean up. We will still need the functionality that depends on all the
current constructor arguments, so we should see if there’s any implicit structure
there that we can tease out.
One possibility is that some of the arguments together deﬁne a concept that
should be packaged up and replaced with a new object to represent it. Here’s a
small example:
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker, 
                          AuditTrail auditor, 
                          CounterPartyFinder counterpartyFinder,
                          LocationFinder locationFinder,
                          DomesticNotifier domesticNotifier,
                          ImportedNotifier importedNotifier) 
  {
// set the fields here
  }
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage, counterpartyFinder);
    auditor.recordReceiptOf(unpacked);
// some other activity here
    if (locationFinder.isDomestic(unpacked)) {
      domesticNotifier.notify(unpacked.asDomesticMessage());
    } else {
      importedNotifier.notify(unpacked.asImportedMessage())
    }
  }
}
Chapter 20
Listening to the Tests
238


---
**Page 239**

Just the thought of writing expectations for all these objects makes us wilt,
which suggests that things are too complicated. A ﬁrst step is to notice that the
unpacker and counterpartyFinder are always used together—they’re ﬁxed at
construction and one calls the other. We can remove one argument by pushing
the counterpartyFinder into the unpacker.
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker, 
                          AuditTrail auditor, 
                          LocationFinder locationFinder,
                          DomesticNotifier domesticNotifier,
                          ImportedNotifier importedNotifier) { […]
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage);
// etc.
  }
Then there’s the triple of locationFinder and the two notiﬁers, which seem
to go together. It might make sense to package them into a MessageDispatcher.
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker, 
                          AuditTrail auditor, 
MessageDispatcher dispatcher) { […]
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage);
    auditor.recordReceiptOf(unpacked);
// some other activity here
dispatcher.dispatch(unpacked);
  }
}
Although we’ve forced this example to ﬁt within a section, it shows that being
sensitive to complexity in the tests can help us clarify our designs. Now we have
a message handling object that clearly performs the usual three stages:
receive, process, and forward. We’ve pulled out the message routing code (the
MessageDispatcher), so the MessageProcessor has fewer responsibilities and we
know where to put routing decisions when things get more complicated. You
might also notice that this code is easier to unit-test.
When extracting implicit components, we start by looking for two conditions:
arguments that are always used together in the class, and those that have the
same lifetime. Once we’ve found a coincidence, we have the harder task of ﬁnding
a good name that explains the concept.
As an aside, one sign that a design is developing nicely is that this kind of
change is easy to integrate. All we have to do is ﬁnd where the MessageProcessor
is created and change this:
239
Bloated Constructor


---
**Page 240**

messageProcessor = 
  new MessageProcessor(new XmlMessageUnpacker(), 
                       auditor, counterpartyFinder, 
                       locationFinder, domesticNotifier,
                       importedNotifier);
to this:
messageProcessor = 
  new MessageProcessor(new XmlMessageUnpacker(counterpartyFinder),
                       auditor,
new MessageDispatcher(
                         locationFinder, 
                         domesticNotifier, importedNotifier));
Later we can reduce the syntax noise by extracting out the creation of the
MessageDispatcher.
Confused Object
Another diagnosis for a “bloated constructor” might be that the object itself is
too large because it has too many responsibilities. For example,
public class Handset {
  public Handset(Network network, Camera camera, Display display, 
                DataNetwork dataNetwork, AddressBook addressBook,
                Storage storage, Tuner tuner, …)
  {
// set the fields here
  }
  public void placeCallTo(DirectoryNumber number) { 
    network.openVoiceCallTo(number);
  }
  public void takePicture() { 
    Frame frame = storage.allocateNewFrame();
    camera.takePictureInto(frame);
    display.showPicture(frame);
  }
  public void showWebPage(URL url) {
    display.renderHtml(dataNetwork.retrievePage(url));
  }
  public void showAddress(SearchTerm searchTerm) {
    display.showAddress(addressBook.findAddress(searchTerm));
  } 
  public void playRadio(Frequency frequency) {
    tuner.tuneTo(frequency);
    tuner.play();
  }
// and so on
}
Like our mobile phones, this class has several unrelated responsibilities which
force it to pull in many dependencies. And, like our phones, the class is confusing
to use because unrelated features interfere with each other. We’re prepared to
Chapter 20
Listening to the Tests
240


---
**Page 241**

put up with these compromises in a handset because we don’t have enough
pockets for all the devices it includes, but that doesn’t apply to code. This class
should be broken up; Michael Feathers describes some techniques for doing so
in Chapter 20 of [Feathers04].
An associated smell for this kind of class is that its test suite will look confused
too. The tests for its various features will have no relationship with each other,
so we’ll be able to make major changes in one area without touching others. If
we can break up the test class into slices that don’t share anything, it might be
best to go ahead and slice up the object too.
Too Many Dependencies
A third diagnosis for a bloated constructor might be that not all of the arguments
are dependencies, one of the peer stereotypes we deﬁned in “Object Peer
Stereotypes” (page 52). As discussed in that section, we insist on dependencies
being passed in to the constructor, but notiﬁcations and adjustments can be set
to defaults and reconﬁgured later. When a constructor is too large, and we don’t
believe there’s an implicit new type amongst the arguments, we can use more
default values and only overwrite them for particular test cases.
Here’s an example—it’s not quite bad enough to need ﬁxing, but it’ll do to
make the point. The application is a racing game; players can try out different
conﬁgurations of car and driving style to see which one wins.1 A RacingCar
represents a competitor within a race:
public class RacingCar {
  private final Track track;
  private Tyres tyres;
  private Suspension suspension;
  private Wing frontWing;
  private Wing backWing;
  private double fuelLoad;
  private CarListener listener;
  private DrivingStrategy driver;
  public RacingCar(Track track, DrivingStrategy driver, Tyres tyres, 
                  Suspension suspension, Wing frontWing, Wing backWing, 
                  double fuelLoad, CarListener listener)
  {
    this.track = track;
    this.driver = driver;
    this.tyres = tyres;
    this.suspension = suspension;
    this.frontWing = frontWing;
    this.backWing = backWing;
    this.fuelLoad = fuelLoad;
    this.listener = listener;
  }
}
1. Nat once worked in a job that involved following the Formula One circuit.
241
Too Many Dependencies


---
**Page 242**

It turns out that track is the only dependency of a RacingCar; the hint is that
it’s the only ﬁeld that’s ﬁnal. The listener is a notiﬁcation, and everything else
is an adjustment; all of these can be modiﬁed by the user before or during the
race. Here’s a reworked constructor:
public class RacingCar {
  private final Track track;
  private DrivingStrategy driver = DriverTypes.borderlineAggressiveDriving();
  private Tyres tyres = TyreTypes.mediumSlicks();
  private Suspension suspension = SuspensionTypes.mediumStiffness();
  private Wing frontWing = WingTypes.mediumDownforce();
  private Wing backWing = WingTypes.mediumDownforce();
  private double fuelLoad = 0.5;
  private CarListener listener = CarListener.NONE;
  public RacingCar(Track track) {
    this.track = track;
  }
  public void setSuspension(Suspension suspension) { […]
  public void setTyres(Tyres tyres) { […]
  public void setEngine(Engine engine) { […]
  public void setListener(CarListener listener) { […]
}
Now we’ve initialized these peers to common defaults; the user can conﬁgure
them later through the user interface, and we can conﬁgure them in our unit tests.
We’ve initialized the listener to a null object, again this can be changed later
by the object’s environment.
Too Many Expectations
When a test has too many expectations, it’s hard to see what’s important and
what’s really under test. For example, here’s a test:
@Test public void 
decidesCasesWhenFirstPartyIsReady() {
  context.checking(new Expectations(){{
    one(firstPart).isReady(); will(returnValue(true));
    one(organizer).getAdjudicator(); will(returnValue(adjudicator));
    one(adjudicator).findCase(firstParty, issue); will(returnValue(case));
    one(thirdParty).proceedWith(case);
  }});
  claimsProcessor.adjudicateIfReady(thirdParty, issue);
}
that might be implemented like this:
Chapter 20
Listening to the Tests
242


---
**Page 243**

public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
    Adjudicator adjudicator = organization.getAdjudicator();
    Case case = adjudicator.findCase(firstParty, issue);
    thirdParty.proceedWith(case);
  } else{
    thirdParty.adjourn();
  }
}
What makes the test hard to read is that everything is an expectation, so every-
thing looks equally important. We can’t tell what’s signiﬁcant and what’s just
there to get through the test.
In fact, if we look at all the methods we call, there are only two that
have any side effects outside this class: thirdParty.proceedWith() and
thirdParty.adjourn(); it would be an error to call these more than once. All the
other methods are queries; we can call organization.getAdjudicator() repeat-
edly without breaking any behavior. adjudicator.findCase() might go either
way, but it happens to be a lookup so it has no side effects.
We can make our intentions clearer by distinguishing between stubs, simulations
of real behavior that help us get the test to pass, and expectations, assertions we
want to make about how an object interacts with its neighbors. There’s a longer
discussion of this distinction in “Allowances and Expectations” (page 277).
Reworking the test, we get:
@Test public void decidesCasesWhenFirstPartyIsReady() {
  context.checking(new Expectations(){{
allowing(firstPart).isReady(); will(returnValue(true));
allowing(organizer).getAdjudicator(); will(returnValue(adjudicator));
allowing(adjudicator).findCase(firstParty, issue); will(returnValue(case));
    one(thirdParty).proceedWith(case);
  }});
  claimsProcessor.adjudicateIfReady(thirdParty, issue);
}
which is more explicit about how we expect the object to change the world
around it.
Write Few Expectations
A colleague, Romilly Cocking, when he ﬁrst started working with us, was surprised
by how few expectations we usually write in a unit test. Just like “everyone” has
now learned to avoid too many assertions in a test, we try to avoid too many
expectations. If we have more than a few, then either we’re trying to test too large
a unit, or we’re locking down too many of the object’s interactions.
243
Too Many Expectations


---
**Page 244**

Special Bonus Prize
We always have problems coming up with good examples. There’s actually a
better improvement to this code, which is to notice that we’ve pulled out a chain
of objects to get to the case object, exposing dependencies that aren’t relevant
here. Instead, we should have told the nearest object to do the work for us,
like this:
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
organization.adjudicateBetween(firstParty, thirdParty, issue);
  } else {
    thirdParty.adjourn();
  }
}
or, possibly,
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
    thirdParty.startAdjudication(organization, firstParty, issue);
  } else{
    thirdParty.adjourn();
  }
}
which looks more balanced. If you spotted this, we award you a Moment of
Smugness™ to be exercised at your convenience.
What the Tests Will Tell Us (If We’re Listening)
We’ve found these beneﬁts from learning to listen to test smells:
Keep knowledge local
Some of the test smells we’ve identiﬁed, such as needing “magic” to create
mocks, are to do with knowledge leaking between components. If we can
keep knowledge local to an object (either internal or passed in), then its im-
plementation is independent of its context; we can safely move it wherever
we like. Do this consistently and your application, built out of pluggable
components, will be easy to change.
If it’s explicit, we can name it
One reason why we don’t like mocking concrete classes is that we like to
have names for the relationships between objects as well the objects them-
selves. As the legends say, if we have something’s true name, we can control
it. If we can see it, we have a better chance of ﬁnding its other uses and so
reducing duplication.
Chapter 20
Listening to the Tests
244


---
**Page 245**

More names mean more domain information
We ﬁnd that when we emphasize how objects communicate, rather than
what they are, we end up with types and roles deﬁned more in terms of the
domain than of the implementation. This might be because we have a greater
number of smaller abstractions, which gets us further away from the under-
lying language. Somehow we seem to get more domain vocabulary into
the code.
Pass behavior rather than data
We ﬁnd that by applying “Tell, Don’t Ask” consistently, we end up with a
coding style where we tend to pass behavior (in the form of callbacks) into
the system instead of pulling values up through the stack. For example, in
Chapter 17, we introduced a SniperCollector that responds when told about
a new Sniper. Passing this listener into the Sniper creation code gives us
better information hiding than if we’d exposed a collection to be added
to. More precise interfaces give us better information-hiding and clearer
abstractions.
We care about keeping the tests and code clean as we go, because it helps to
ensure that we understand our domain and reduces the risk of being unable
to cope when a new requirement triggers changes to the design. It’s much easier to
keep a codebase clean than to recover from a mess. Once a codebase starts
to “rot,” the developers will be under pressure to botch the code to get the next
job done. It doesn’t take many such episodes to dissipate a team’s good intentions.
We once had a posting to the jMock user list that included this comment:
I was involved in a project recently where jMock was used quite heavily. Looking
back, here’s what I found:
1.
The unit tests were at times unreadable (no idea what they were doing).
2.
Some tests classes would reach 500 lines in addition to inheriting an abstract
class which also would have up to 500 lines.
3.
Refactoring would lead to massive changes in test code.
A unit test shouldn’t be 1000 lines long! It should focus on at most a few
classes and should not need to create a large ﬁxture or perform lots of preparation
just to get the objects into a state where the target feature can be exercised. Such
tests are hard to understand—there’s just so much to remember when reading
them. And, of course, they’re brittle, all the objects in play are too tightly coupled
and too difﬁcult to set to the state the test requires.
Test-driven development can be unforgiving. Poor quality tests can slow devel-
opment to a crawl, and poor internal quality of the system being tested will result
in poor quality tests. By being alert to the internal quality feedback we get from
245
What the Tests Will Tell Us (If We’re Listening)


---
**Page 246**

writing tests, we can nip this problem in the bud, long before our unit tests ap-
proach 1000 lines of code, and end up with tests we can live with. Conversely,
making an effort to write tests that are readable and ﬂexible gives us more feed-
back about the internal quality of the code we are testing. We end up with tests
that help, rather than hinder, continued development.
Chapter 20
Listening to the Tests
246


