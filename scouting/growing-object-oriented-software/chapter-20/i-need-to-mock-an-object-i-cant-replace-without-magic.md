Line1 # I Need to Mock an Object I Can't Replace (without Magic) (pp.230-233)
Line2 
Line3 ---
Line4 **Page 230**
Line5 
Line6 I Need to Mock an Object I Can’t Replace (without Magic)
Line7 Singletons Are Dependencies
Line8 One interpretation of reducing complexity in code is making commonly useful
Line9 objects accessible through a global structure, usually implemented as a singleton.
Line10 Any code that needs access to a feature can just refer to it by its global name
Line11 instead of receiving it as an argument. Here’s a common example:
Line12 Date now = new Date();
Line13 Under the covers, the constructor calls the singleton System and sets the new
Line14 instance to the current time using System.currentTimeMillis(). This is a conve-
Line15 nient technique, but it comes at a cost. Let’s say we want to write a test like this:
Line16 @Test public void rejectsRequestsNotWithinTheSameDay() {
Line17   receiver.acceptRequest(FIRST_REQUEST);
Line18 // the next day
Line19   assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
Line20 }
Line21 The implementation looks like this:
Line22 public boolean acceptRequest(Request request) {
Line23   final Date now = new Date();
Line24   if (dateOfFirstRequest == null) {
Line25     dateOfFirstRequest = now;
Line26    } else if (firstDateIsDifferentFrom(now)) {
Line27     return false;
Line28   }
Line29 // process the request
Line30   return true;
Line31 }
Line32 where dateOfFirstRequest is a ﬁeld and firstDateIsDifferentFrom() is a helper
Line33 method that hides the unpleasantness of working with the Java date library.
Line34 To test this timeout, we must either make the test wait overnight or do some-
Line35 thing clever (perhaps with aspects or byte-code manipulation) to intercept the
Line36 constructor and return suitable Date values for the test. This difﬁculty in testing
Line37 is a hint that we should change the code. To make the test easier, we need to
Line38 control how Date objects are created, so we introduce a Clock and pass it into
Line39 the Receiver. If we stub Clock, the test might look like this:
Line40 @Test public void rejectsRequestsNotWithinTheSameDay() {
Line41   Receiver receiver = new Receiver(stubClock);
Line42   stubClock.setNextDate(TODAY);
Line43   receiver.acceptRequest(FIRST_REQUEST);
Line44   stubClock.setNextDate(TOMORROW);
Line45   assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
Line46 }
Line47 Chapter 20
Line48 Listening to the Tests
Line49 230
Line50 
Line51 
Line52 ---
Line53 
Line54 ---
Line55 **Page 231**
Line56 
Line57 and the implementation like this:
Line58 public boolean acceptRequest(Request request) {
Line59   final Date now = clock.now();
Line60   if (dateOfFirstRequest == null) {
Line61    dateOfFirstRequest = now;
Line62   } else if (firstDateIsDifferentFrom(now)) {
Line63    return false;
Line64   }
Line65 // process the request
Line66   return true;
Line67 }
Line68 Now we can test the Receiver without any special tricks. More importantly,
Line69 however, we’ve made it obvious that Receiver is dependent on time—we can’t
Line70 even create one without a Clock. Some argue that this is breaking encapsulation
Line71 by exposing the internals of a Receiver—we should be able to just create an in-
Line72 stance and not worry—but we’ve seen so many systems that are impossible to
Line73 test because the developers did not isolate the concept of time. We want to know
Line74 about this dependency, especially when the service is rolled out across the world,
Line75 and New York and London start complaining about different results.
Line76 From Procedures to Objects
Line77 Having taken the trouble to introduce a Clock object, we start wondering if our
Line78 code is missing a concept: date checking in terms of our domain. A Receiver
Line79 doesn’t need to know all the details of a calendar system, such as time zones and
Line80 locales; it just need to know if the date has changed for this application. There’s
Line81 a clue in the fragment:
Line82 firstDateIsDifferentFrom(now)
Line83 which means that we’ve had to wrap up some date manipulation code in Receiver.
Line84 It’s the wrong object; that kind of work should be done in Clock. We write the
Line85 test again:
Line86 @Test public void rejectsRequestsNotWithinTheSameDay() {
Line87   Receiver receiver = new Receiver(clock);
Line88   context.checking(new Expectations() {{
Line89    allowing(clock).now(); will(returnValue(NOW));
Line90 one(clock).dayHasChangedFrom(NOW); will(returnValue(false));
Line91   }});
Line92   receiver.acceptRequest(FIRST_REQUEST);
Line93   assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
Line94 }
Line95 The implementation looks like this:
Line96 231
Line97 I Need to Mock an Object I Can’t Replace (without Magic)
Line98 
Line99 
Line100 ---
Line101 
Line102 ---
Line103 **Page 232**
Line104 
Line105 public boolean acceptRequest(Request request) {
Line106   if (dateOfFirstRequest == null) {
Line107    dateOfFirstRequest = clock.now();
Line108   } else if (clock.dayHasChangedFrom(dateOfFirstRequest)) {
Line109    return false;
Line110   }
Line111 // process the request
Line112   return true;
Line113 }
Line114 This version of Receiver is more focused: it doesn’t need to know how to dis-
Line115 tinguish one date from another and it only needs to get a date to set the ﬁrst
Line116 value. The Clock interface deﬁnes exactly those date services Receiver needs from
Line117 its environment.
Line118 But we think we can push this further. Receiver only retains a date so that it
Line119 can detect a change of day; perhaps we should delegate all the date functionality
Line120 to another object which, for want of a better name, we’ll call a SameDayChecker.
Line121 @Test public void rejectsRequestsOutsideAllowedPeriod() {
Line122   Receiver receiver = new Receiver(sameDayChecker);
Line123   context.checking(new Expectations() {{
Line124 allowing(sameDayChecker).hasExpired(); will(returnValue(false));
Line125   }});
Line126   assertFalse("too late now", receiver.acceptRequest(REQUEST));
Line127 }
Line128 with an implementation like this:
Line129 public boolean acceptRequest(Request request) {
Line130   if (sameDayChecker.hasExpired()) {
Line131    return false;
Line132   }
Line133 // process the request
Line134   return true;
Line135 }
Line136 All the logic about dates has been separated out from Receiver, which can
Line137 concentrate on processing the request. With two objects, we can make sure that
Line138 each behavior (date checking and request processing) is unit-tested cleanly.
Line139 Implicit Dependencies Are Still Dependencies
Line140 We can hide a dependency from the caller of a component by using a global
Line141 value to bypass encapsulation, but that doesn’t make the dependency go away—it
Line142 just makes it inaccessible. For example, Steve once had to work with a Microsoft
Line143 .Net library that couldn’t be loaded without installing ActiveDirectory—which
Line144 wasn’t actually required for the features he wanted to use and which he couldn’t
Line145 install on his machine anyway. The library developer was trying to be helpful
Line146 and to make it “just work,” but the result was that Steve couldn’t get it to work
Line147 at all.
Line148 Chapter 20
Line149 Listening to the Tests
Line150 232
Line151 
Line152 
Line153 ---
Line154 
Line155 ---
Line156 **Page 233**
Line157 
Line158 One goal of object orientation as a technique for structuring code is to make
Line159 the boundaries of an object clearly visible. An object should only deal with values
Line160 and instances that are either local—created and managed within its scope—or
Line161 passed in explicitly, as we emphasized in “Context Independence” (page 54).
Line162 In the example above, the act of making date checking testable forced us to
Line163 make the Receiver’s requirements more explicit and to think more clearly about
Line164 the domain.
Line165 Use the Same Techniques to Break Dependencies in Unit Tests
Line166 as in Production Code
Line167 There are several frameworks available that use techniques such as manipulating
Line168 class loaders or bytecodes to allow unit tests to break dependencies without
Line169 changing the target code. As a rule, these are advanced techniques that most
Line170 developers would not use when writing production code. Sometimes these tools
Line171 really are necessary, but developers should be aware that they come with a
Line172 hidden cost.
Line173 Unit-testing tools that let the programmer sidestep poor dependency management
Line174 in the design waste a valuable source of feedback.When the developers eventually
Line175 do need to address these design weaknesses to add some urgent feature, they
Line176 will ﬁnd it harder to do. The poor structure will have inﬂuenced other parts of the
Line177 system that rely on it, and any understanding of the original intent will have
Line178 evaporated. As with dirty pots and pans, it’s easier to get the grease off before it’s
Line179 been baked in.
Line180 Logging Is a Feature
Line181 We have a more contentious example of working with objects that are hard to
Line182 replace: logging. Take a look at these two lines of code:
Line183 log.error("Lost touch with Reality after " + timeout + "seconds");
Line184 log.trace("Distance traveled in the wilderness: " + distance);
Line185 These are two separate features that happen to share an implementation. Let
Line186 us explain.
Line187 •
Line188 Support logging (errors and info) is part of the user interface of the appli-
Line189 cation. These messages are intended to be tracked by support staff, as well
Line190 as perhaps system administrators and operators, to diagnose a failure or
Line191 monitor the progress of the running system.
Line192 •
Line193 Diagnostic logging (debug and trace) is infrastructure for programmers.
Line194 These messages should not be turned on in production because they’re in-
Line195 tended to help the programmers understand what’s going on inside the
Line196 system they’re developing.
Line197 233
Line198 Logging Is a Feature
Line199 
Line200 
Line201 ---
