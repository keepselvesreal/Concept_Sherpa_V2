Line1 # Mocking Concrete Classes (pp.235-237)
Line2 
Line3 ---
Line4 **Page 235**
Line5 
Line6 course, we will still need to write an implementation of support and some focused
Line7 integration tests to go with it.
Line8 But That’s Crazy Talk…
Line9 The idea of encapsulating support reporting sounds like over-design, but it’s
Line10 worth thinking about for a moment. It means we’re writing code in terms of our
Line11 intent (helping the support people) rather than implementation (logging), so it’s
Line12 more expressive. All the support reporting is handled in a few known places, so
Line13 it’s easier to be consistent about how things are reported and to encourage reuse.
Line14 It can also help us structure and control our reporting in terms of the application
Line15 domain, rather than in terms of Java packages. Finally, the act of writing a test
Line16 for each report helps us avoid the “I don’t know what to do with this exception,
Line17 so I’ll log it and carry on” syndrome, which leads to log bloat and production
Line18 failures because we haven’t handled obscure error conditions.
Line19 One objection we’ve heard is, “I can’t pass in a logger for testing because I’ve
Line20 got logging all over my domain objects. I’d have to pass one around everywhere.”
Line21 We think this is a test smell that is telling us that we haven’t clariﬁed our design
Line22 enough. Perhaps some of our support logging should really be diagnostic logging,
Line23 or we’re logging more than we need because of something that we wrote when
Line24 we hadn’t yet understood the behavior. Most likely, there’s still too much dupli-
Line25 cation in our domain code and we haven’t yet found the “choke points” where
Line26 most of the production logging should go.
Line27 So what about diagnostic logging? Is it disposable scaffolding that should be
Line28 taken down once the job is done, or essential infrastructure that should be tested
Line29 and maintained? That depends on the system, but once we’ve made the distinction
Line30 we have more freedom to think about using different techniques for support and
Line31 diagnostic logging. We might even decide that in-line code is the wrong technique
Line32 for diagnostic logging because it interferes with the readability of the production
Line33 code that matters. Perhaps we could weave in some aspects instead (since that’s
Line34 the canonical example of their use); perhaps not—but at least we’ve now
Line35 clariﬁed the choice.
Line36 One ﬁnal data point. One of us once worked on a system where so much
Line37 content was written to the logs that they had to be deleted after a week to ﬁt on
Line38 the disks. This made maintenance very difﬁcult as the relevant logs were usually
Line39 gone by the time a bug was assigned to be ﬁxed. If they’d logged nothing at all,
Line40 the system would have run faster with no loss of useful information.
Line41 Mocking Concrete Classes
Line42 One approach to interaction testing is to mock concrete classes rather than inter-
Line43 faces. The technique is to inherit from the class you want to mock and override
Line44 the methods that will be called within the test, either manually or with any of
Line45 235
Line46 Mocking Concrete Classes
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 236**
Line53 
Line54 the mocking frameworks. We think this is a technique that should be used only
Line55 when you really have no other options.
Line56 Here’s an example of mocking by hand. The test veriﬁes that the music centre
Line57 starts the CD player at the requested time. Assume that setting the schedule on
Line58 a CdPlayer object involves triggering some behavior we don’t want in the test,
Line59 so we override scheduleToStartAt() and verify afterwards that we’ve called it
Line60 with the right argument.
Line61 public class MusicCentreTest {
Line62   @Test public void 
Line63 startsCdPlayerAtTimeRequested() {
Line64     final MutableTime scheduledTime = new MutableTime();
Line65     CdPlayer player = new CdPlayer() {
Line66       @Override public void scheduleToStartAt(Time startTime) {
Line67         scheduledTime.set(startTime);
Line68       }
Line69     }
Line70     MusicCentre centre = new MusicCentre(player);
Line71     centre.startMediaAt(LATER);
Line72     assertEquals(LATER, scheduledTime.get());
Line73   }
Line74 }
Line75 The problem with this approach is that it leaves the relationship between the
Line76 CdPlayer and MusicCentre implicit. We hope we’ve made clear by now that our
Line77 intention in test-driven development is to use mock objects to bring out relation-
Line78 ships between objects. If we subclass, there’s nothing in the domain code to make
Line79 such a relationship visible—just methods on an object. This makes it harder to
Line80 see if the service that supports this relationship might be relevant elsewhere, and
Line81 we’ll have to do the analysis again next time we work with the class. To make
Line82 the point, here’s a possible implementation of CdPlayer:
Line83 public class CdPlayer {
Line84   public void scheduleToStartAt(Time startTime) { […]
Line85   public void stop() { […]
Line86   public void gotoTrack(int trackNumber) { […]
Line87   public void spinUpDisk() { […]
Line88   public void eject() { […]
Line89 }
Line90 It turns out that our MusicCentre only uses the starting and stopping methods
Line91 on the CdPlayer; the rest are used by some other part of the system. We would
Line92 be overspecifying the MusicCentre by requiring it to talk to a CdPlayer; what it
Line93 actually needs is a ScheduledDevice. Robert Martin made the point (back in
Line94 1996) in his Interface Segregation Principle that “Clients should not be forced
Line95 to depend upon interfaces that they do not use,” but that’s exactly what we do
Line96 when we mock a concrete class.
Line97 Chapter 20
Line98 Listening to the Tests
Line99 236
Line100 
Line101 
Line102 ---
Line103 
Line104 ---
Line105 **Page 237**
Line106 
Line107 There’s a more subtle but powerful reason for not mocking concrete classes.
Line108 When we extract an interface as part of our test-driven development process, we
Line109 have to think up a name to describe the relationship we’ve just discovered—in
Line110 this example, the ScheduledDevice. We ﬁnd that this makes us think harder about
Line111 the domain and teases out concepts that we might otherwise miss. Once something
Line112 has a name, we can talk about it.
Line113 “Break Glass in Case of Emergency”
Line114 There are a few occasions when we have to put up with this smell. The least un-
Line115 acceptable situation is where we’re working with legacy code that we control
Line116 but can’t change all at once. Alternatively, we might be working with third-party
Line117 code that we can’t change at all (see Chapter 8). We ﬁnd that it’s almost always
Line118 better to write a veneer over an external library rather than mock it directly—but
Line119 occasionally, it’s just not worth it. We broke the rule with Logger in Chapter 19
Line120 but apologized a lot and felt bad about it. In any case, these are unfortunate but
Line121 necessary compromises that we would try to work our way out of when possible.
Line122 The longer we leave them in the code, the more likely it is that some brittleness
Line123 in the design will cause us grief.
Line124 Above all, do not override a class’ internal features—this just locks down your
Line125 test to the quirks of the current implementation. Only override visible methods.
Line126 This rule also prohibits exposing internal methods just to override them in a test.
Line127 If you can’t get to the structure you need, then the tests are telling you that it’s
Line128 time to break up the class into smaller, composable features.
Line129 Don’t Mock Values
Line130 There’s no point in writing mocks for values (which should be immutable any-
Line131 way). Just create an instance and use it. For example, in this test Video holds
Line132 details of a part of a show:
Line133 @Test public void sumsTotalRunningTime() {
Line134   Show show = new Show();
Line135   Video video1 = context.mock(Video.class); // Don't do this
Line136   Video video2 = context.mock(Video.class);
Line137   context.checking(new Expectations(){{
Line138     one(video1).time(); will(returnValue(40));
Line139     one(video2).time(); will(returnValue(23));
Line140   }});
Line141   show.add(video1);
Line142   show.add(video2);
Line143   assertEqual(63, show.runningTime())
Line144 }
Line145 237
Line146 Don’t Mock Values
Line147 
Line148 
Line149 ---
