Line1 # Introduction (pp.229-230)
Line2 
Line3 ---
Line4 **Page 229**
Line5 
Line6 Chapter 20
Line7 Listening to the Tests
Line8 You can see a lot just by observing.
Line9 —Yogi Berra
Line10 Introduction
Line11 Sometimes we ﬁnd it difﬁcult to write a test for some functionality we want to
Line12 add to our code. In our experience, this usually means that our design can be
Line13 improved—perhaps the class is too tightly coupled to its environment or does
Line14 not have clear responsibilities. When this happens, we ﬁrst check whether it’s an
Line15 opportunity to improve our code, before working around the design by making
Line16 the test more complicated or using more sophisticated tools. We’ve found
Line17 that the qualities that make an object easy to test also make our code responsive
Line18 to change.
Line19 The trick is to let our tests drive our design (that’s why it’s called test-driven
Line20 development). TDD is about testing code, verifying its externally visible qualities
Line21 such as functionality and performance. TDD is also about feedback on the code’s
Line22 internal qualities: the coupling and cohesion of its classes, dependencies that are
Line23 explicit or hidden, and effective information hiding—the qualities that keep the
Line24 code maintainable.
Line25 With practice, we’ve become more sensitive to the rough edges in our tests, so
Line26 we can use them for rapid feedback about the design. Now when we ﬁnd a feature
Line27 that’s difﬁcult to test, we don’t just ask ourselves how to test it, but also why is
Line28 it difﬁcult to test.
Line29 In this chapter, we look at some common “test smells” that we’ve encountered
Line30 and discuss what they might imply about the design of the code. There are two
Line31 categories of test smell to consider. One is where the test itself is not well
Line32 written—it may be unclear or brittle. Meszaros [Meszaros07] covers several such
Line33 patterns in his “Test Smells” chapter. This chapter is concerned with the other
Line34 category, where a test is highlighting that the target code is the problem. Meszaros
Line35 has one pattern for this, called “Hard-to-Test Code.” We’ve picked out some
Line36 common cases that we’ve seen that are relevant to our approach to TDD.
Line37 229
Line38 
Line39 
Line40 ---
Line41 
Line42 ---
Line43 **Page 230**
Line44 
Line45 I Need to Mock an Object I Can’t Replace (without Magic)
Line46 Singletons Are Dependencies
Line47 One interpretation of reducing complexity in code is making commonly useful
Line48 objects accessible through a global structure, usually implemented as a singleton.
Line49 Any code that needs access to a feature can just refer to it by its global name
Line50 instead of receiving it as an argument. Here’s a common example:
Line51 Date now = new Date();
Line52 Under the covers, the constructor calls the singleton System and sets the new
Line53 instance to the current time using System.currentTimeMillis(). This is a conve-
Line54 nient technique, but it comes at a cost. Let’s say we want to write a test like this:
Line55 @Test public void rejectsRequestsNotWithinTheSameDay() {
Line56   receiver.acceptRequest(FIRST_REQUEST);
Line57 // the next day
Line58   assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
Line59 }
Line60 The implementation looks like this:
Line61 public boolean acceptRequest(Request request) {
Line62   final Date now = new Date();
Line63   if (dateOfFirstRequest == null) {
Line64     dateOfFirstRequest = now;
Line65    } else if (firstDateIsDifferentFrom(now)) {
Line66     return false;
Line67   }
Line68 // process the request
Line69   return true;
Line70 }
Line71 where dateOfFirstRequest is a ﬁeld and firstDateIsDifferentFrom() is a helper
Line72 method that hides the unpleasantness of working with the Java date library.
Line73 To test this timeout, we must either make the test wait overnight or do some-
Line74 thing clever (perhaps with aspects or byte-code manipulation) to intercept the
Line75 constructor and return suitable Date values for the test. This difﬁculty in testing
Line76 is a hint that we should change the code. To make the test easier, we need to
Line77 control how Date objects are created, so we introduce a Clock and pass it into
Line78 the Receiver. If we stub Clock, the test might look like this:
Line79 @Test public void rejectsRequestsNotWithinTheSameDay() {
Line80   Receiver receiver = new Receiver(stubClock);
Line81   stubClock.setNextDate(TODAY);
Line82   receiver.acceptRequest(FIRST_REQUEST);
Line83   stubClock.setNextDate(TOMORROW);
Line84   assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
Line85 }
Line86 Chapter 20
Line87 Listening to the Tests
Line88 230
Line89 
Line90 
Line91 ---
