# Chapter 27: Testing Asynchronous Code (pp.315-360)

---
**Page 315**

Chapter 27
Testing Asynchronous Code
I can spell banana but I never know when to stop.
—Johnny Mercer (songwriter)
Introduction
Some tests must cope with asynchronous behavior—whether they’re end-to-end
tests probing a system from the outside or, as we’ve just seen, unit tests exercising
multithreaded code. These tests trigger some activity within the system to run
concurrently with the test’s thread. The critical difference from “normal” tests,
where there is no concurrency, is that control returns to the test before the tested
activity is complete—returning from the call to the target code does not mean
that it’s ready to be checked.
For example, this test assumes that a Set has ﬁnished adding an element when
the add() method returns. Asserting that set has a size of one veriﬁes that it did
not store duplicate elements.
@Test public void storesUniqueElements() {
  Set set = new HashSet<String>();
  set.add("bananana");
  set.add("bananana");
  assertThat(set.size(), equalTo(1));
}
By contrast, this system test is asynchronous. The holdingOfStock() method
synchronously downloads a stock report by HTTP, but the send() method sends
an asynchronous message to a server that updates its records of stocks held.
@Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
  Date tradeDate = new Date();
  send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
  send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
  assertThat(holdingOfStock("A", tradeDate), equalTo(0));
}
The transmission and processing of a trade message happens concurrently with
the test, so the server might not have received or processed the messages yet
315


---
**Page 316**

when the test makes its assertion. The value of the stock holding that the assertion
checks will depend on timings: how long the messages take to reach the server,
how long the server takes to update its database, and how long the test takes to
run. The test might ﬁre the assertion after both messages have been processed
(passing correctly), after one message (failing incorrectly), or before either
message (passing, but testing nothing at all).
As you can see from this small example, with an asynchronous test we have
to be careful about its coordination with the system it’s testing. Otherwise, it can
become unreliable, failing intermittently when the system is working or, worse,
passing when the system is broken.
Current testing frameworks provide little support for dealing with asynchrony.
They mostly assume that the tests run in a single thread of control, leaving the
programmer to build the scaffolding needed to test concurrent behavior. In this
chapter we describe some practices for writing reliable, responsive tests for
asynchronous code.
Sampling or Listening
The fundamental difﬁculty with testing asynchronous code is that a test triggers
activity that runs concurrently with the test and therefore cannot immediately
check the outcome of the activity. The test will not block until the activity has
ﬁnished. If the activity fails, it will not throw an exception back into the test, so
the test cannot recognize if the activity is still running or has failed. The test
therefore has to wait for the activity to complete successfully and fail if this
doesn’t happen within a given timeout period.
Wait for Success
An asynchronous test must wait for success and use timeouts to detect failure.
This implies that every tested activity must have an observable effect: a test
must affect the system so that its observable state becomes different. This sounds
obvious but it drives how we think about writing asynchronous tests. If an activ-
ity has no observable effect, there is nothing the test can wait for, and therefore
no way for the test to synchronize with the system it is testing.
There are two ways a test can observe the system: by sampling its observable
state or by listening for events that it sends out. Of these, sampling is often the
only option because many systems don’t send any monitoring events. It’s quite
common for a test to include both techniques to interact with different “ends”
of its system. For example, the Auction Sniper end-to-end tests sample the user
interface for display changes, through the WindowLicker framework, but listen
for chat events in the fake auction server.
Chapter 27
Testing Asynchronous Code
316


---
**Page 317**

Beware of Flickering Tests
A test can fail intermittently if its timeout is too close to the time the tested behavior
normally takes to run, or if it doesn’t synchronize correctly with the system. On a
small system, an occasional ﬂickering test might not cause problems—the test will
most likely pass during the next build—but it’s risky. As the test suite grows, it be-
comes increasingly difﬁcult to get a test run in which none of the ﬂickering tests fail.
Flickering tests can mask real defects. If the system itself occasionally fails, the
tests that accurately detect those failures will seem to be ﬂickering. If the suite
contains unreliable tests, intermittent failures detected by reliable tests can easily
be ignored. We need to make sure we understand what the real problem is before
we ignore ﬂickering tests.
Allowing ﬂickering tests is bad for the team. It breaks the culture of quality where
things should “just work,” and even a few ﬂickering tests can make a team stop
paying attention to broken builds. It also breaks the habit of feedback. We should
be paying attention to why the tests are ﬂickering and whether that means we
should improve the design of both the tests and code. Of course, there might be
times when we have to compromise and decide to live with a ﬂickering test for the
moment, but this should be done reluctantly and include a plan for when it will
be ﬁxed.
As we saw in the last chapter, synchronizing by simply making each test wait
for a ﬁxed time is not practical. The test suite for a system of any size will take
too long to run. We know we’ll have to wait for failing tests to time out, but
succeeding tests should be able to ﬁnish as soon as there’s a response from
the code.
Succeed Fast
Make asynchronous tests detect success as quickly as possible so that they provide
rapid feedback.
Of the two observation strategies we outlined in the previous section, listening
for events is the quickest. The test thread can block, waiting for an event from
the system. It will wake up and check the result as soon as it receives an event.
The alternative—sampling—means repeatedly polling the target system for a
state change, with a short delay between polls. The frequency of this polling has
to be tuned to the system under test, to balance the need for a fast response
against the load it imposes on the target system. In the worst case, fast polling
might slow the system enough to make the tests unreliable.
317
Sampling or Listening


---
**Page 318**

Put the Timeout Values in One Place
Both observation strategies use a timeout to detect that the system has failed.
Again, there’s a balance to be struck between a timeout that’s too short, which will
make the tests unreliable, and one that’s too long, which will make failing tests too
slow. This balance can be different in different environments, and will change as
the system grows over time.
When the timeout duration is deﬁned in one place, it’s easy to ﬁnd and change.
The team can adjust its value to ﬁnd the right balance between speed and reliability
as the system develops.
Two Implementations
Scattering ad hoc sleeps and timeouts throughout the tests makes them difﬁcult
to understand, because it leaves too much implementation detail in the tests
themselves. Synchronization and assertion is just the sort of behavior that’s
suitable for factoring out into subordinate objects because it usually turns into
a bad case of duplication if we don’t. It’s also just the sort of tricky code that we
want to get right once and not have to change again.
In this section, we’ll show an example implementation of each observation
strategy.
Capturing Notiﬁcations
An event-based assertion waits for an event by blocking on a monitor until it
gets notiﬁed or times out. When the monitor is notiﬁed, the test thread wakes
up and continues if it ﬁnds that the expected event has arrived, or blocks again.
If the test times out, then it raises a failure.
NotificationTrace is an example of how to record and test notiﬁcations sent
by the system. The setup of the test will arrange for the tested code to call
append() when the event happens, for example by plugging in an event listener
that will call the method when triggered. In the body of the test, the test thread
calls containsNotification() to wait for the expected notiﬁcation or fail if it
times out. For example:
trace.containsNotification(startsWith("WANTED"));
will wait for a notiﬁcation string that starts with WANTED.
Within NotificationTrace, incoming notiﬁcations are stored in a list trace,
which is protected by a lock traceLock. The class is generic, so we don’t specify
the type of these notiﬁcations, except to say that the matchers we pass into
containsNotification() must be compatible with that type. The implementation
uses Timeout and NotificationStream classes that we’ll describe later.
Chapter 27
Testing Asynchronous Code
318


---
**Page 319**

public class NotificationTrace<T> {
  private final Object traceLock = new Object();
  private final List<T> trace = new ArrayList<T>(); 1
  private long timeoutMs;
// constructors and accessors to configure the timeout […]
  public void append(T message) { 2
    synchronized (traceLock) {
      trace.add(message);
traceLock.notifyAll();
    }
  }
  public void containsNotification(Matcher<? super T> criteria) 3
    throws InterruptedException 
  { 
    Timeout timeout = new Timeout(timeoutMs); 
    synchronized (traceLock) {
      NotificationStream<T> stream = new NotificationStream<T>(trace, criteria);
      while (! stream.hasMatched()) {
        if (timeout.hasTimedOut()) {
          throw new AssertionError(failureDescriptionFrom(criteria));
        }
        timeout.waitOn(traceLock);
      }
    }
  }
  private String failureDescriptionFrom(Matcher<? super T> matcher) {  […] 
    // Construct a description of why there was no match, 
    // including the matcher and all the received messages. 
}
1
We store notiﬁcations in a list so that they’re available to us for other queries
and so that we can include them in a description if the test fails (we don’t
show how the description is constructed).
2
The append() method, called from a worker thread, appends a new notiﬁca-
tion to the trace, and then tells any threads waiting on traceLock to wake
up because there’s been a change. This is called by the test infrastructure
when triggered by an event in the system.
3
The containsNotification() method, called from the test thread, searches
through all the notiﬁcations it has received so far. If it ﬁnds a notiﬁcation
that matches the given criteria, it returns. Otherwise, it waits until more
notiﬁcations arrive and checks again. If it times out while waiting, then it
fails the test.
The nested NotificationStream class searches the unexamined elements in its
list for one that matches the given criteria. It allows the list to grow between calls
to hasMatched() and picks up after the last element it looked at.
319
Two Implementations


---
**Page 320**

private static class NotificationStream<N> {
  private final List<N> notifications;
  private final Matcher<? super N> criteria;
  private int next = 0;
  public NotificationStream(List<N> notifications, Matcher<? super N> criteria) {
    this.notifications = notifications;
    this.criteria = criteria;
  }
  public boolean hasMatched() {
    while (next < notifications.size()) {
      if (criteria.matches(notifications.get(next)))
        return true;
      next++;
    }
    return false;
  }
}
NotificationTrace is one example of a simple coordination class between test
and worker threads. It uses a simple approach, although it does avoid a possible
race condition where a background thread delivers a notiﬁcation before the test
thread has started waiting. Another implementation, for example, might have
containsNotification() only search messages received after the previous call.
What is appropriate depends on the context of the test.
Polling for Changes
A sample-based assertion repeatedly samples some visible effect of the system
through a “probe,” waiting for the probe to detect that the system has entered
an expected state. There are two aspects to the process of sampling: polling the
system and failure reporting, and probing the system for a given state. Separating
the two helps us think clearly about the behavior, and different tests can reuse the
polling with different probes.
Poller is an example of how to poll a system. It repeatedly calls its probe, with
a short delay between samples, until the system is ready or the poller times out.
The poller drives a probe that actually checks the target system, which we’ve
abstracted behind a Probe interface.
public interface Probe {
  boolean isSatisfied();
  void sample();
  void describeFailureTo(Description d);
}
The probe’s sample() method takes a snapshot of the system state that the test
is interested in. The isSatisfied() method returns true if that state meets the
test’s acceptance criteria. To simplify the poller logic, we allow isSatisfied()
to be called before sample().
Chapter 27
Testing Asynchronous Code
320


---
**Page 321**

public class Poller {
  private long timeoutMillis;
  private long pollDelayMillis;
// constructors and accessors to configure the timeout […]
  public void check(Probe probe) throws InterruptedException {
    Timeout timeout = new Timeout(timeoutMillis);
    while (! probe.isSatisfied()) {
      if (timeout.hasTimedOut()) {
        throw new AssertionError(describeFailureOf(probe));
      }
      Thread.sleep(pollDelayMillis);
      probe.sample();
    }
  }
  private String describeFailureOf(Probe probe) { […] 
}
This simple implementation delegates synchronization with the system to
the probe. A more sophisticated version might implement synchronization in the
poller, so it could be shared between probes. The similarity to NotificationTrace
is obvious, and we could have pulled out a common abstract structure, but we
wanted to keep the designs clear for now.
To poll, for example, for the length of a ﬁle, we would write this line in a test:
assertEventually(fileLength("data.txt", is(greaterThan(2000))));
This wraps up the construction of our sampling code in a more expressive
assertion. The helper methods to implement this are:
public static void assertEventually(Probe probe) throws InterruptedException {
  new Poller(1000L, 100L).check(probe);
}
public static Probe fileLength(String path, final Matcher<Integer> matcher) {
  final File file = new File(path);
  return new Probe() {
    private long lastFileLength = NOT_SET;
    public void sample() { lastFileLength = file.length(); }
    public boolean isSatisfied() { 
      return lastFileLength != NOT_SET && matcher.matches(lastFileLength);
    }
    public void describeFailureTo(Description d) {
      d.appendText("length was ").appendValue(lastFileLength);
    }
  };
}
Separating the act of sampling from checking whether the sample is satisfactory
makes the structure of the probe clearer. We can hold on to the sample result to
report the unsatisfactory result we found if there’s a failure.
321
Two Implementations


---
**Page 322**

Timing Out
Finally we show the Timeout class that the two example assertion classes use. It
packages up time checking and synchronization:
public class Timeout {
 private final long endTime;
  public Timeout(long duration) {
    this.endTime = System.currentTimeMillis() + duration;
  }
  public boolean hasTimedOut() { return timeRemaining() <= 0; }
  public void waitOn(Object lock) throws InterruptedException {
    long waitTime = timeRemaining();
    if (waitTime > 0) lock.wait(waitTime);
  }
  private long timeRemaining() { return endTime - System.currentTimeMillis(); }
}
Retroﬁtting a Probe
We can now rewrite the test from the introduction. Instead of making an assertion
about the current holding of a stock, the test must wait for the holding of the
stock to reach the expected level within an acceptable time limit.
@Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
  Date tradeDate = new Date();
  send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
  send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
}
Previously, the holdingOfStock() method returned a value to be compared.
Now it returns a Probe that samples the system’s holding and returns if it meets
the acceptance criteria deﬁned by a Hamcrest matcher—in this case equalTo(0).
Runaway Tests
Unfortunately, the new version of the test is still unreliable, even though we’re
now sampling for a result. The assertion is waiting for the holding to become
zero, which is what we started out with, so it’s possible for the test to pass before
the system has even begun processing. This test can run ahead of the system
without actually testing anything.
Chapter 27
Testing Asynchronous Code
322


---
**Page 323**

The worst aspect of runaway tests is that they give false positive results, so
broken code looks like it’s working. We don’t often review tests that pass, so it’s
easy to miss this kind of failure until something breaks down the line. Even more
tricky, the code might have worked when we ﬁrst wrote it, as the tests happened
to synchronize correctly during development, but now it’s broken and we
can’t tell.
Beware of Tests That Return the System to the Same State
Be careful when an asynchronous test asserts that the system returns to a previous
state. Unless it also asserts that the system enters an intermediate state before
asserting the initial state, the test will run ahead of the system.
To stop the test running ahead of the system, we must add assertions that wait
for the system to enter an intermediate state. Here, for example, we make sure
that the ﬁrst trade event has been processed before asserting the effect of the
second event:
@Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
  Date tradeDate = new Date();
  send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
assertEventually(holdingOfStock("A", tradeDate, equalTo(10)));
  send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
  assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
}
Similarly, in Chapter 14, we check all the displayed states in the acceptance
tests for the Auction Sniper user interface:
auction.reportPrice(1098, 97, ApplicationRunner.SNIPER_XMPP_ID);
application.hasShownSniperIsWinning();
auction.announceClosed();
application.hasShownSniperHasWon();
We want to make sure that the sniper has responded to each message before
continuing on to the next one.
Lost Updates
A signiﬁcant difference between tests that sample and those that listen for events
is that polling can miss state changes that are later overwritten, Figure 27.1.
323
Lost Updates


---
**Page 324**

Figure 27.1
A test that polls can miss changes in the system
under test
If the test can record notiﬁcations from the system, it can look through its
records to ﬁnd signiﬁcant notiﬁcations.
Figure 27.2
A test that records notiﬁcations will not lose updates
To be reliable, a sampling test must make sure that its system is stable before
triggering any further interactions. Sampling tests need to be structured as a series
of phases, as shown in Figure 27.3. In each phase, the test sends a stimulus to
prompt a change in the observable state of the system, and then waits until that
change becomes visible or times out.
Figure 27.3
Phases of a sampling test
Chapter 27
Testing Asynchronous Code
324


---
**Page 325**

This shows the limits of how precise we can be with a sampling test. All the
test can do between “stimulate” and “sample” is wait. We can write more
reliable tests by not confusing the different steps in the loop and only triggering
further changes once we’ve detected that the system is stable by observing a
change in its sampled state.
Testing That an Action Has No Effect
Asynchronous tests look for changes in a system, so to test that something has
not changed takes a little ingenuity. Synchronous tests don’t have this problem
because they completely control the execution of the tested code. After invoking
the target object, synchronous tests can query its state or check that it hasn’t
made any unexpected calls to its neighbors.
If an asynchronous test waits for something not to happen, it cannot even be
sure that the system has started before it checks the result. For example, if we
want to show that trades in another region are not counted in the stock holding,
then this test:
@Test public void doesNotShowTradesInOtherRegions() {
  send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
.inTradingRegion(OTHER_REGION));
  assertEventually(holdingOfStock("A", tradeDate, equalTo(0)));
}
cannot tell whether the system has correctly ignored the trade or just not received
it yet. The most obvious workaround is for the test to wait for a ﬁxed period of
time and then check that the unwanted event did not occur. Unfortunately, this
makes the test run slowly even when successful, and so breaks our rule of
“succeed fast.”
Instead, the test should trigger a behavior that is detectable and use that to
detect that the system has stabilized. The skill here is in picking a behavior that
will not interfere with the test’s assertions and that will complete after the tested
behavior. For example, we could add another trade event to the regions example.
This shows that the out-of-region event is excluded because its quantity is not
included in the total holding.
@Test public void doesNotShowTradesInOtherRegions() {
  send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(10)
                    .inTradingRegion(OTHER_REGION));
  send(aTradeEvent().ofType(BUY).forStock("A").withQuantity(66)
                    .inTradingRegion(SAME_REGION));
  assertEventually(holdingOfStock("A", tradeDate, equalTo(66)));
}
Of course, this test assumes that trade events are processed in sequence, not
in parallel, so that the second event cannot overtake the ﬁrst and give a false
positive. That’s why such tests are not completely “black box” but have to make
assumptions about the structure of the system. This might make these tests
325
Testing That an Action Has No Effect


---
**Page 326**

brittle—they would misreport if the system changes the assumptions they’ve been
built on. One response is to add a test to conﬁrm those expectations—in this
case, perhaps a stress test to conﬁrm event processing order and alert the team
if circumstances change. That said, there should already be other tests that conﬁrm
those assumptions, so it may be enough just to associate these tests, for example
by grouping them in the same test package.
Distinguish Synchronizations and Assertions
We have one mechanism for synchronizing a test with its system and for making
assertions about that system—wait for an observable condition and time out if
it doesn’t happen. The only difference between the two activities is our interpre-
tation of what they mean. As always, we want to make our intentions explicit,
but it’s especially important here because there’s a risk that someone may look
at the test later and remove what looks like a duplicate assertion, accidentally
introducing a race condition.
We often adopt a naming scheme to distinguish between synchronizations and
assertions. For example, we might have waitUntil() and assertEventually()
methods to express the purpose of different checks that share an underlying
implementation.
Alternatively, we might reserve the term “assert” for synchronous tests and
use a different naming conventions in asynchronous tests, as we did in the Auction
Sniper example.
Externalize Event Sources
Some systems trigger their own events internally. The most common example is
using a timer to schedule activities. This might include repeated actions that run
frequently, such as bundling up emails for forwarding, or follow-up actions that
run days or even weeks in the future, such as conﬁrming a delivery date.
Hidden timers are very difﬁcult to work with because they make it hard to tell
when the system is in a stable state for a test to make its assertions. Waiting for
a repeated action to run is too slow to “succeed fast,” to say nothing of an action
scheduled a month from now. We also don’t want tests to break unpredictably
because of interference from a scheduled activity that’s just kicked in. Trying to
test a system by coinciding timers is just too brittle.
The only solution is to make the system deterministic by decoupling it from
its own scheduling. We can pull event generation out into a shared service that
is driven externally. For example, in one project we implemented the system’s
scheduler as a web service. System components scheduled activities by making
HTTP requests to the scheduler, which triggered activities by making HTTP
“postbacks.” In another project, the scheduler published notiﬁcations onto a
message bus topic that the components listened to.
Chapter 27
Testing Asynchronous Code
326


---
**Page 327**

With this separation in place, tests can step the system through its behavior
by posing as the scheduler and generating events deterministically. Now we can
run system tests quickly and reliably. This is a nice example of a testing require-
ment leading to a better design. We’ve been forced to abstract out scheduling,
which means we won’t have multiple implementations hidden in the system.
Usually, introducing such an event infrastructure turns out to be useful for
monitoring and administration.
There’s a trade-off too, of course. Our tests are no longer exercising the entire
system. We’ve prioritized test speed and reliability over ﬁdelity. We compensate
by keeping the scheduler’s API as simple as possible and testing it rigorously
(another advantage). We would probably also write a few slow tests, running in
a separate build, that exercise the whole system together including the real
scheduler.
327
Externalize Event Sources


---
**Page 328**

This page intentionally left blank 


---
**Page 329**

Afterword
A Brief History of Mock
Objects
Tim Mackinnon
Introduction
The ideas and concepts behind mock objects didn’t materialise in a single day.
There’s a long history of experimentation, discussion, and collaboration between
many different developers who have taken the seed of an idea and grown it into
something more profound. The ﬁnal result—the topic of this book—should help
you with your software development; but the background story of “The Making
of Mock Objects” is also interesting—and a testament to the dedication of the
people involved. I hope revisiting this history will inspire you too to challenge
your thoughts on what is possible and to experiment with new practices.
Origins
The story began on a roundabout1 near Archway station in London in late 1999.
That evening, several members of a London-based software architecture group2
met to discuss topical issues in software. The discussion turned to experiences
with Agile Software Development and I mentioned the impact that writing tests
seemed to be having on our code. This was before the ﬁrst Extreme Programming
book had been published, and teams like ours were still exploring how to do
test-driven development—including what constituted a good test. In particular,
I had noticed a tendency to add “getter” methods to our objects to facilitate
testing. This felt wrong, since it could be seen as violating object-oriented princi-
ples, so I was interested in the thoughts of the other members. The conversation
was quite lively—mainly centering on the tension between pragmatism in testing
and pure object-oriented design. We also had a recent example of a colleague,
1. “Roundabout” is the UK term for a trafﬁc circle.
2. On this occasion, they were Tim Mackinnon, Peter Marks, Ivan Moore, and John
Nolan.
329


---
**Page 330**

Oli Bye, stubbing out the Java Servlet API for testing a web application without
a server.
I particularly remember from that evening a crude diagram of an onion3 and
its metaphor of the many layers of software, along with the mantra “No Getters!
Period!” The discussion revolved around how to safely peel back and test layers
of that onion without impacting its design. The solution was to focus on the
composition of software components (the group had discussed Brad Cox’s ideas
on software components many times before). It was an interesting collision of
opinions, and the emphasis on composition—now referred to as dependency
injection—gave us a technique for eliminating the getters we were “pragmatically”
adding to objects so we could write tests for them.
The following day, our small team at Connextra4 started putting the idea into
practice. We removed the getters from sections of our code and used a composi-
tional strategy by adding constructors that took the objects we wanted to test
via getters as parameters. At ﬁrst this felt cumbersome, and our two recent
graduate recruits were not convinced. I, however, had a Smalltalk background,
so to me the idea of composition and delegation felt right. Enforcing a “no getters”
rule seemed like a way to achieve a more object-oriented feeling in the Java
language we were using.
We stuck to it for several days and started to see some patterns emerging. More
of our conversations were about expecting things to happen between our
objects, and we frequently had variables with names like expectedURL and
expectedServiceName  in our injected objects. On the other hand, when our tests
failed we were tired of stepping through in a debugger to see what went wrong.
We started adding variables with names like actualURL and actualServiceName
to allow the injected test objects to throw exceptions with helpful messages.
Printing the expected and actual values side-by-side showed us immediately what
the problem was.
Over the course of several weeks we refactored these ideas into a group of
classes: ExpectationValue for single values, ExpectationList for multiple values
in a particular order, and ExpectationSet for unique values in any order. Later,
Tung Mac also added ExpectationCounter for situations where we didn’t want
to specify explicit values but just count the number of calls. It started to feel as
if something interesting was happening, but it seemed so obvious to me that there
wasn’t really much to describe. One afternoon, Peter Marks decided that we
should come up with name for what we were doing—so we could at least package
the code—and, after a few suggestions, proposed “mock.” We could use it both
as a noun and a verb, and it refactored nicely into our code, so we adopted it.
3. Initially drawn by John Nolan.
4. The team consisted of Tim Mackinnon, Tung Mac, and Matthew Cooke, with
direction from Peter Marks and John Nolan. Connextra is now part of Bet Genius.
Afterword 
A Brief History of Mock Objects
330


---
**Page 331**

Spreading the Word
Around this time, we5 also started the London Extreme Tuesday Club (XTC) to
share experiences of Extreme Programming with other teams. During one meeting,
I described our refactoring experiments and explained that I felt that it helped
our junior developers write better object-oriented code. I ﬁnished the story by
saying, “But this is such an obvious technique that I’m sure most people do it
eventually anyway.” Steve pointed out that the most obvious things aren’t always
so obvious and are usually difﬁcult to describe. He thought this could make a
great paper if we could sort the wood from the trees, so we decided to collaborate
with another XTC member (Philip Craig) and write something for the XP2000
conference. If nothing else, we wanted to go to Sardinia.
We began to pick apart the ideas and give them a consistent set of names,
studying real code examples to understand the essence of the technique. We
backported new concepts we discovered to the original Connextra codebase to
validate their effectiveness. This was an exciting time and I recall that it took
many late nights to reﬁne our ideas—although we were still struggling to come
up with an accurate “elevator pitch” for mock objects. We knew what it felt like
when using them to drive great code, but describing this experience to other
developers who weren’t part of the XTC was still challenging.
The XP2000 paper [Mackinnon00] and the initial mock objects library had a
mixed reception—for some it was revolutionary, for others it was unnecessary
overhead. In retrospect, the fact that Java didn’t have good reﬂection when we
started meant that many of the steps were manual, or augmented with code
generation tools.6 This turned people off—they couldn’t separate the idea from
the implementation.
Another Generation
The story continues when Nat Pryce took the ideas and implemented them in
Ruby. He exploited Ruby’s reﬂection to write expectations directly into the test
as blocks. Inﬂuenced by his PhD work on protocols between components, his li-
brary changed the emphasis from asserting parameter values to asserting messages
sent between objects. Nat then ported his implementation to Java, using the new
Proxy type in Java 1.3 and deﬁning expectations with “constraint” objects. When
Nat showed us this work, it immediately clicked. He donated his library to the
mock objects project and visited the Connextra ofﬁces where we worked together
to add features that the Connextra developers needed.
5. With Tim Mackinnon, Oli Bye, Paul Simmons, and Steve Freeman. Oli coined the
name XTC.
6. This later changed as Java 1.1 was released, which improved reﬂection, and as others
who had read our paper wrote more tools, such as Tammo Freese’s Easymock.
331
Another Generation


---
**Page 332**

With Nat in the ofﬁce where mock objects were being used constantly, we
were driven to use his improvements to provide more descriptive failure messages.
We had seen our developers getting bogged down when the reason for a test
failure was not obvious enough (later, we observed that this was often a hint
that an object had too many responsibilities). Now, constraints allowed us to
write tests that were more expressive and provided better failure diagnostics, as
the constraint objects could explain what went wrong.7 For example, a failure
on a stringBegins constraint could produce a message like:
Expected a string parameter beginning with "http" 
  but was called with a value of "ftp.domain.com"
We released the new improved version of Nat’s library under the name Dynamock.
As we improved the library, more programmers started using it, which intro-
duced new requirements. We started adding more and more options to the API
until, eventually, it became too complicated to maintain—especially as we had
to support multiple versions of Java. Meanwhile, Steve tired of the the duplication
in the syntax required to set up expectations, so he introduced a version of a
Smalltalk cascade—multiple calls to the same object.
Then Steve noticed that in a statically typed language like Java, a cascade could
return a chain of interfaces to control when methods are made available to the
caller—in effect, we could use types to encode a workﬂow. Steve also wanted to
improve the programming experience by guiding the new generation of IDEs
to prompt with the “right” completion options. Over the course of a year, Steve
and Nat, with much input from the rest of us, pushed the idea hard to produce
jMock, an expressive API over our original Dynamock framework. This was also
ported to C# as NMock. At some point in this process, they realized that
they were actually writing a language in Java which could be used to write
expectations; they wrote this up later in an OOPLSA paper [Freeman06].
Consolidation
Through our experience in Connextra and other companies, and through giving
many presentations, we improved our understanding and communication of the
ideas of mock objects. Steve (inspired by some of the early lean software material)
coined the term “needs-driven development,” and Joe Walnes, another colleague,
drew a nice visualisation of islands of objects communicating with each other.
Joe also had the insight of using mock objects to drive the design of interfaces
between objects. At the time, we were struggling to promote the idea of using
mock objects as a design tool; many people (including some authors) saw it only
as a technique for speeding up unit tests. Joe cut through all the conceptual
barriers with his simple heuristic of “Only mock types you own.”
7. Later, Steve talked Charlie Poole into including constraints in NUnit. It took some
extra years to have matchers (the latest version of constraints) adopted by JUnit.
Afterword 
A Brief History of Mock Objects
332


---
**Page 333**

We took all these ideas and wrote a second conference paper, “Mock Roles
not Objects” [Freeman04]. Our initial description had focused too much on im-
plementation, whereas the critical idea was that the technique emphasizes the
roles that objects play for each other. When developers are using mock objects
well, I observe them drawing diagrams of what they want to test, or using CRC
cards to roleplay relationships—these then translate nicely into mock objects and
tests that drive the required code.
Since then, Nat and Steve have reworked jMock to produce jMock2, and Joe
has extracted constraints into the Hamcrest library (now adopted by JUnit).
There’s also now a wide selection of mock object libraries, in many different
languages.
The results have been worth the effort. I think we can ﬁnally say that there is
now a well-documented and polished technique that helps you write better soft-
ware. From those humble “no getters” beginnings, this book summarizes years
of experience from all of us who have collaborated, and adds Steve and Nat’s
language expertise and careful attention to detail to produce something that is
greater than the sum of its parts.
333
Consolidation


---
**Page 334**

This page intentionally left blank 


---
**Page 335**

Appendix A
jMock2 Cheat Sheet
Introduction
We use jMock2 as our mock object framework throughout this book. This
chapter summarizes its features and shows some examples of how to use them.
We’re using JUnit 4.6 (we assume you’re familiar with it); jMock also supports
JUnit3. Full documentation is available at www.jmock.org.
We’ll show the structure of a jMock unit test and describe what its features
do. Here’s a whole example:
import org.jmock.Expectations;
import org.jmock.Mockery;
import org.jmock.integration.junit4.JMock;
import org.jmock.integration.junit4.JUnit4Mockery;
@RunWith(JMock.class)
public class TurtleDriverTest {
  private final Mockery context = new JUnit4Mockery();
  private final Turtle turtle = context.mock(Turtle.class);
  @Test public void 
goesAMinimumDistance() {
    final Turtle turtle2 = context.mock(Turtle.class, "turtle2");
    final TurtleDriver driver = new TurtleDriver(turtle1, turtle2); // set up
    context.checking(new Expectations() {{ // expectations
      ignoring (turtle2);
      allowing (turtle).flashLEDs(); 
      oneOf (turtle).turn(45);
      oneOf (turtle).forward(with(greaterThan(20)));  
      atLeast(1).of (turtle).stop();
    }});
    driver.goNext(45); // call the code
    assertTrue("driver has moved", driver.hasMoved()); // further assertions
  }
}
335


---
**Page 336**

Test Fixture Class
First, we set up the test ﬁxture class by creating its Mockery.
import org.jmock.Expectations;
import org.jmock.Mockery;
import org.jmock.integration.junit4.JMock;
import org.jmock.integration.junit4.JUnit4Mockery;
@RunWith(JMock.class)
public class TurtleDriverTest {
  private final Mockery context = new JUnit4Mockery();
[…]
}
For the object under test, a Mockery represents its context—the neighboring
objects it will communicate with. The test will tell the mockery to create
mock objects, to set expectations on the mock objects, and to check at the end
of the test that those expectations have been met. By convention, the mockery is
stored in an instance variable named context.
A test written with JUnit4 does not need to extend a speciﬁc base class but
must specify that it uses jMock with the @RunWith(JMock.class) attribute.1 This
tells the JUnit runner to ﬁnd a Mockery ﬁeld in the test class and to assert (at the
right time in the test lifecycle) that its expectations have been met. This requires
that there should be exactly one mockery ﬁeld in the test class. The class
JUnit4Mockery will report expectation failures as JUnit4 test failures.
Creating Mock Objects
This test uses two mock turtles, which we ask the mockery to create. The ﬁrst is
a ﬁeld in the test class:
private final Turtle turtle = context.mock(Turtle.class);
The second is local to the test, so it’s held in a variable:
final Turtle turtle2 = context.mock(Turtle.class, "turtle2");
The variable has to be ﬁnal so that the anonymous expectations block has access
to it—we’ll return to this soon. This second mock turtle has a speciﬁed name,
turtle2. Any mock can be given a name which will be used in the report if the
test fails; the default name is the type of the object. If there’s more than one mock
object of the same type, jMock enforces that only one uses the default name; the
others must be given names when declared. This is so that failure reports can
make clear which mock instance is which when describing the state of the test.
1. At the time of writing, JUnit was introducing the concept of Rule. We expect to extend
the jMock API to adopt this technique.
Appendix A
jMock2 Cheat Sheet
336


---
**Page 337**

Tests with Expectations
A test sets up its expectations in one or more expectation blocks, for example:
context.checking(new Expectations() {{ 
oneOf (turtle).turn(45);
}}); 
An expectation block can contain any number of expectations. A test can
contain multiple expectation blocks; expectations in later blocks are appended
to those in earlier blocks. Expectation blocks can be interleaved with calls to the
code under test.
What’s with the Double Braces?
The most disconcerting syntax element in jMock is its use of double braces in an
expectations block. It’s a hack, but with a purpose. If we reformat an expectations
block, we get this:
context.checking(new Expectations() {
  {
    oneOf (turtle).turn(45);
  }
});
We’re passing to the checking() method an anonymous subclass of Expectations
(ﬁrst set of braces). Within that subclass, we have an instance initialization block
(second set of braces) that Java will call after the constructor.Within the initialization
block, we can reference the enclosing Expectations object, so oneOf() is actually
an instance method—as are all of the expectation structure clauses we describe
in the next section.
The purpose of this baroque structure is to provide a scope for building up
expectations. All the code in the expectation block is deﬁned within an anonymous
instance of Expectations, which collects the expectation components that the
code generates. The scoping to an instance allows us to make this collection im-
plicit, which requires less code. It also improves our experience in the IDE, since
code completion will be more focused, as in Figure A.1.
Referring back to the discussion in “Building Up to Higher-Level Programming”
(page 65), Expectations is an example of the Builder pattern.
337
Tests with Expectations


---
**Page 338**

Figure A.1
Narrowed scope gives better code completion
Expectations
Expectations have the following structure:
invocation-count(mock-object).method(argument-constraints);
inSequence(sequence-name);
when(state-machine.is(state-name));
will(action);
then(state-machine.is(new-state-name));
The invocation-count and mock-object are required, all the other clauses are
optional. You can give an expectation any number of inSequence, when, will,
and then clauses. Here are some common examples:
oneOf (turtle).turn(45); // The turtle must be told exactly once to turn 45 degrees.
atLeast(1).of (turtle).stop(); // The turtle must be told at least once to stop.
allowing (turtle).flashLEDs(); // The turtle may be told any number of times, 
                               // including none, to flash its LEDs.
allowing (turtle).queryPen(); will(returnValue(PEN_DOWN));
// The turtle may be asked about its pen any  
                               // number of times and will always return PEN_DOWN.
ignoring (turtle2); // turtle2 may be told to do anything. This test ignores it.
Invocation Count
The invocation count is required to describe how often we expect a call to be
made during the run of the test. It starts the deﬁnition of an expectation.
exactly(n).of
The invocation is expected exactly n times.
oneOf
The invocation is expected exactly once. This is a convenience shorthand for
exactly(1).of
Appendix A
jMock2 Cheat Sheet
338


---
**Page 339**

atLeast(n).of
The invocation is expected at least n times.
atMost(n).of
The invocation is expected at most n times.
between(min, max).of
The invocation is expected at least min times and at most max times.
allowing
ignoring
The invocation is allowed any number of times including none. These
clauses are equivalent to atLeast(0).of, but we use them to highlight that
the expectation is a stub—that it’s there to get the test through to the
interesting part of the behavior.
never
The invocation is not expected. This is the default behavior if no expectation
has been set. We use this clause to emphasize to the reader of a test that an
invocation should not be called.
allowing, ignoring, and never can also be applied to an object as a whole.
For example, ignoring(turtle2) says to allow all calls to turtle2. Similarly,
never(turtle2) says to fail if any calls are made to turtle2 (which is the same
as not specifying any expectations on the object). If we add method expectations,
we can be more precise, for example:
allowing(turtle2).log(with(anything()));
never(turtle2).stop(); 
will allow log messages to be sent to the turtle, but fail if it’s told to stop. In
practice, while allowing precise invocations is common, blocking individual
methods is rarely useful.
Methods
Expected methods are speciﬁed by calling the method on the mock object within
an expectation block. This deﬁnes the name of the method and what argument
values are acceptable. Values passed to the method in an expectation will be
compared for equality:
oneOf (turtle).turn(45); // matches turn() called with 45
oneOf (calculator).add(2, 2); // matches add() called with 2 and 2
Invocation matching can be made more ﬂexible by using matchers as arguments
wrapped in with() clauses:
339
Expectations


---
**Page 340**

oneOf(calculator).add(with(lessThan(15)), with(any(int.class)));
// matches add() called with a number less than 15 and any other number
Either all the arguments must be matchers or all must be values:
oneOf(calculator).add(with(lessThan(15)), 22); // this doesn't work!
Argument Matchers
The most commonly used matchers are deﬁned in the Expectations class:
equal(o)
The argument is equal to o, as deﬁned by calling o.equals() with the actual
value received during the test. This also recursively compares the contents
of arrays.
same(o)
The argument is the same object as o.
any(Class<T> type)
The argument is any value, including null. The type argument is required
to force Java to type-check the argument at compile time.
a(Class<T> type)
an(Class<T> type)
The argument is an instance of type or of one of its subtypes.
aNull(Class<T> type)
The argument is null. The type argument is to force Java to type-check the
argument at compile time.
aNonNull(Class<T> type)
The argument is not null. The type argument is to force Java to type-check
the argument at compile time.
not(m)
The argument does not match the matcher m.
anyOf(m1, m2, m3, […])
The argument matches at least one of the matchers m1, m2, m3, […].
allOf(m1, m2, m3, […])
The argument matches all of the matchers m1, m2, m3, […].
More matchers are available from static factory methods of the Hamcrest
Matchers class, which can be statically imported into the test class. For more
precision, custom matchers can be written using the Hamcrest library.
Appendix A
jMock2 Cheat Sheet
340


---
**Page 341**

Actions
An expectation can also specify an action to perform when it is matched, by
adding a will() clause after the invocation. For example, this expectation will
return PEN_DOWN when queryPen() is called:
allowing (turtle).queryPen(); will(returnValue(PEN_DOWN));
jMock provides several standard actions, and programmers can provide custom
actions by implementing the Action interface. The standard actions are:
will(returnValue(v))
Return v to the caller.
will(returnIterator(c))
Return an iterator for collection c to the caller.
will(returnIterator(v1, v2, […], vn))
Return a new iterator over elements v1 to v2 on each invocation.
will(throwException(e))
Throw exception e when called.
will(doAll(a1, a2, […], an))
Perform all the actions a1 to an on every invocation.
Sequences
The order in which expectations are speciﬁed does not have to match the order
in which their invocations are called. If invocation order is signiﬁcant, it can be
enforced in a test by adding a Sequence. A test can create more than one sequence
and an expectation can be part of more than once sequence at a time. The syntax
for creating a Sequence is:
Sequence sequence-variable = context.sequence("sequence-name"); 
To expect a sequence of invocations, create a Sequence object, write the expec-
tations in the expected order, and add an inSequence() clause to each relevant
expectation. Expectations in a sequence can have any invocation count. For
example:
context.checking(new Expectations() {{
  final Sequence drawing = context.sequence("drawing");
  allowing (turtle).queryColor(); will(returnValue(BLACK));
  atLeast(1).of (turtle).forward(10); inSequence(drawing);
  oneOf (turtle).turn(45);    inSequence(drawing);
  oneOf (turtle).forward(10); inSequence(drawing);
}});
341
Expectations


---
**Page 342**

Here, the queryColor() call is not in the sequence and can take place at
any time.
States
Invocations can be constrained to occur only when a condition is true, where a
condition is deﬁned as a state machine that is in a given state. State machines can
switch between states speciﬁed by state names. A test can create multiple state
machines, and an invocation can be constrained to one or more conditions. The
syntax for creating a state machine is:
States state-machine-name =
         context.states("state-machine-name").startsAs("initial-state");
The initial state is optional; if not speciﬁed, the state machine starts in an unnamed
initial state.
Add these clauses to expectations to constrain them to match invocations in
a given state, or to switch the state of a state machine after an invocation:
when(stateMachine.is("state-name"));
Constrains the last expectation to occur only when stateMachine is in the
state "state-name".
when(stateMachine.isNot("state-name"));
Constrains the last expectation to occur only when stateMachine is not in
the state "state-name".
then(stateMachine.is("state-name"));
Changes stateMachine to be in the state "state-name" when the invocation
occurs.
This example allows turtle to move only when the pen is down:
context.checking(new Expectations() {{
  final States pen = context.states("pen").startsAs("up");
  allowing (turtle).queryColor(); will(returnValue(BLACK));
  allowing (turtle).penDown();        then(pen.is("down"));
  allowing (turtle).penUp();          then(pen.is("up"));
  atLeast(1).of (turtle).forward(15); when(pen.is("down"));
  one (turtle).turn(90);              when(pen.is("down"));
  one (turtle).forward(10);           when(pen.is("down"));
}} 
Notice that expectations with states do not deﬁne a sequence; they can be com-
bined with Sequence constraints if order is signiﬁcant. As before, the queryColor()
call is not included in the states, and so can be called at any time.
Appendix A
jMock2 Cheat Sheet
342


---
**Page 343**

Appendix B
Writing a Hamcrest Matcher
Introduction
Although Hamcrest 1.2 comes with a large library of matchers, sometimes these
do not let you specify an assertion or expectation accurately enough to convey
what you mean or to keep your tests ﬂexible. In such cases, you can easily deﬁne
a new matcher that seamlessly extends the JUnit and jMock APIs.
A matcher is an object that implements the org.hamcrest.Matcher interface:
public interface SelfDescribing {
  void describeTo(Description description);
}
public interface Matcher<T> extends SelfDescribing {
  boolean matches(Object item);
  void describeMismatch(Object item, Description mismatchDescription);
}
A matcher does two things:
•
Reports whether a parameter value meets the constraint (the matches()
method);
•
Generates a readable description to be included in test failure messages (the
describeTo() method inherited from the SelfDescribing interface and
the describeMismatch() method).
A New Matcher Type
As an example, we will write a new matcher that tests whether a string starts
with a given preﬁx. It can be used in tests as shown below. Note that the
matcher seamlessly extends the assertion: there is no visible difference between
built-in and third-party matchers at the point of use.
@Test public void exampleTest() {
[…]
  assertThat(someString, startsWith("Cheese"));
}
343


---
**Page 344**

To write a new matcher, we must implement two things: a new class that im-
plements the Matcher interface and the startsWith() factory function for our
assertions to read well when we use the new matcher in our tests.
To write a matcher type, we extend one of Hamcrest’s abstract base classes,
rather than implementing the Matcher interface directly.1 For our needs, we can
extend TypeSafeMatcher<String>, which checks for nulls and type safety, casts
the matched Object to a String, and calls the template methods [Gamma94] in
our subclass.
public class StringStartsWithMatcher extends TypeSafeMatcher<String> {
  private final String expectedPrefix;
  public StringStartsWithMatcher(String expectedPrefix) {
    this.expectedPrefix = expectedPrefix;
  }
  @Override
  protected boolean matchesSafely(String actual) {
    return actual.startsWith(expectedPrefix);
  }
  @Override
  public void describeTo(Description matchDescription) {
    matchDescription.appendText("a string starting with ")
                    .appendValue(expectedPrefix);
  }
  @Override protected void
describeMismatchSafely(String actual, Description mismatchDescription) {
    String actualPrefix = 
             actual.substring(0, Math.min(actual.length(), expectedPrefix.length()));
    mismatchDescription.appendText("started with ")
                       .appendValue(actualPrefix);
  }
}
Matcher Objects Must Be Stateless
When dispatching each invocation, jMock uses the matchers to ﬁnd an expectation
that matches the invocation’s arguments. This means that it will call the matchers
many times during the test, maybe even after the expectation has already been
matched and invoked. In fact, jMock gives no guarantees of when and how many
times it will call the matchers. This has no effect on stateless matchers, but the
behavior of stateful matchers is unpredictable.
If you want to maintain state in response to invocations, write a custom jMock
Action, not a Matcher.
1. This lets the Hamcrest team add methods to the Matcher interface without breaking
all the code that implements that interface, because they can also add a default
implementation to the base class.
Appendix B
Writing a Hamcrest Matcher
344


---
**Page 345**

The text generated by the describeTo() and describeMismatch() must follow
certain grammatical conventions to ﬁt into the error messages generated by
JUnit and jMock. Although JUnit and jMock generate different messages,
matcher descriptions that complete the sentence “expected description but it
mismatch-description” will work with both libraries. That sentence completed
with the StringStartsWithMatcher’s descriptions would be something like:
expected a string starting with "Cheese" but it started with "Bananas"
To make the new matcher ﬁt seamlessly into JUnit and jMock, we also write
a factory method that creates an instance of the StringStartsWithMatcher.
public static Matcher<String> aStringStartingWith(String prefix ) {
    return new StringStartsWithMatcher(prefix);
}
The point of the factory method is to make the test code read clearly, so
consider how it will look when used in an assertion or expectation.
And that’s all there is to writing a matcher.
345
A New Matcher Type


---
**Page 346**

This page intentionally left blank 


---
**Page 347**

Bibliography
 
[Abelson96] Abelson, Harold and Gerald Sussman. Structure and Interpretation of
Computer Programs. MIT Press, 1996, ISBN 978-0262011532.
[Beck99] Beck, Kent. Extreme Programming Explained: Embrace Change. Addison-
Wesley, 1999, ISBN 978-0321278654.
[Beck02] Beck, Kent. Test Driven Development: By Example. Addison-Wesley, 2002, ISBN
978-0321146530.
[Begel08] Begel, Andrew and Beth Simon. “Struggles of New College Graduates in Their
First Software Development Job.” In: SIGCSE Bulletin, 40, no. 1 (March 2008):
226–230, ACM, ISSN 0097-8418.
[Cockburn04] Cockburn, Alistair. Crystal Clear: A Human-Powered Methodology for
Small Teams. Addison-Wesley Professional, October 29, 2004, ISBN 0201699478.
[Cockburn08] Cockburn, Alistair. Hexagonal Architecture: Ports and Adapters (“Object
Structural”). June 19, 2008, http://alistair.cockburn.us/ Hexagonal+architecture.
[Cohn05] Cohn, Mike. Agile Estimating and Planning. Prentice Hall, 2005, ISBN
978-0131479418.
[Demeyer03] Demeyer, Serge, Stéphane Ducasse, and Oscar Nierstrasz. Object-Oriented
Reengineering Patterns. http://scg.unibe.ch/download/oorp/.
[Evans03] Evans, Eric. Domain-Driven Design: Tackling Complexity in the Heart of
Software. Addison-Wesley, 2003, ISBN 978-0321125217.
[Feathers04] Feathers, Michael. Working Effectively with Legacy Code. Prentice Hall,
2004, ISBN 978-0131177055.
[Fowler99] Fowler, Martin. Refactoring: Improving the Design of Existing Code.
Addison-Wesley, 1999, ISBN 978-0201485677.
[Freeman04] Freeman, Steve, Tim Mackinnon, Nat Pryce, and Joe Walnes. “Mock
Roles, Not Objects.” In: Companion to the 19th ACM SIGPLAN Conference
on Object-Oriented Programming Systems, Languages, and Applications,
OOPLSA, Vancouver, BC, October 2004, New York: ACM, ISBN 1581138334,
http://portal.acm.org/citation.cfm?doid=1028664.1028765 .
[Freeman06] Freeman, Steve and Nat Pryce. “Evolving an Embedded Domain-Speciﬁc
Language in Java.” In: Companion to the 21st ACM SIGPLAN Conference on Object-
Oriented Programming Systems, Languages, and Applications, OOPLSA, Portland,
Oregon, October 2006, New York: ACM, http://www.jmock.org/oopsla06.pdf.
[Gall03] Gall, John. The Systems Bible: The Beginner’s Guide to Systems Large and Small.
General Systemantics Pr/Liberty, 2003, ISBN 978-0961825171.
[Gamma94] Gamma, Erich, Richard Helm, Ralph Johnson, and John Vlissides. Design
Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley, 1994.
347


---
**Page 348**

[Graham93] Graham, Paul. On Lisp. Prentice Hall, 1993, ISBN 0130305529,
http://www.paulgraham.com/onlisp.html.
[Hunt99] Hunt, Andrew and David Thomas. The Pragmatic Programmer: From Journey-
man to Master. Addison-Wesley Professional, October 30, 1999, ISBN 020161622X.
[Kay98] Kay, Alan. Email Message Sent to the Squeak Mailing List. October 10, 1998,
http://lists.squeakfoundation.org/pipermail/squeak-dev/1998-October/017019.html.
[Kerievsky04] Kerievsky, Joshua. Refactoring to Patterns. Addison-Wesley, 2004, ISBN
978-0321213358.
[Kernighan76] Kernighan, Brian and P. J. Plauger. Software Tools. Addison-Wesley, 1976,
ISBN 978-0201036695.
[Lieberherr88] Lieberherr, Karl, Ian Holland, and Arthur Riel. “Object-Oriented Program-
ming: An Objective Sense of Style.” In: OOPSLA, 23, no. 11 (1988): 323–334.
[LIFT] Framework for Literate Functional Testing. https://lift.dev.java.net/.
[Mackinnon00] Mackinnon, Tim, Steve Freeman, and Philip Craig. “Endo-Testing:
Unit Testing with Mock Objects.” In: Giancarlo Succi and Michele Marchesi,
Extreme Programming Examined, Addison-Wesley, 2001, pp. 287–301, ISBN 978-
0201710403.
[Magee06] Magee, Jeff and Jeff Kramer. Concurrency: State Models & Java Programs.
Wiley, 2006, ISBN 978-0470093559.
[Martin02] Martin, Robert C. Agile Software Development, Principles, Patterns, and
Practices. Prentice Hall, 2002, ISBN 978-0135974445.
[Meszaros07] Meszaros, Gerard. xUnit Test Patterns: Refactoring Test Code. Addison-
Wesley, 2007, ISBN 978-0131495050.
[Meyer91] Meyer, Betrand. Eiffel: The Language. Prentice Hall, 1991, ISBN 978-
0132479257.
[Mugridge05] Mugridge, Rick and Ward Cunningham. Fit for Developing Software:
Framework for Integrated Tests. Prentice Hall, 2005, ISBN 978-0321269348.
[Schuh01] Schuh, Peter and Stephanie Punke. ObjectMother: Easing Test Object Creation
In XP. XP Universe, 2001.
[Schwaber01] Schwaber, Ken and Mike Beedle. Agile Software Development with Scrum.
Prentice Hall, 2001, ISBN 978-0130676344.
[Shore07] Shore, James and Shane Warden. The Art of Agile Development. O’Reilly
Media, 2007, ISBN 978-0596527679.
[Wirfs-Brock03] Wirfs-Brock, Rebecca and Alan McKean. Object Design: Roles,
Responsibilities, and Collaborations. Addison-Wesley, 2003, ISBN 0201379430.
[Woolf98] Woolf, Bobby. “Null Object.” In: Pattern Languages of Program Design 3.
Edited by Robert Martin, Dirk Riehle, and Frank Buschmann. Addison-Wesley, 1998,
http://www.cse.wustl.edu/~schmidt/PLoP-96/woolf1.ps.gz.
[Yourdon79] Yourdon, Edward and Larry Constantine. Structured Design: Fundamentals
of a Discipline of Computer Program and Systems Design. Prentice Hall, 1979, ISBN
978-0138544713.
Bibliography 
348


---
**Page 349**

A
a(), jMock, 340
AbstractTableModel class, 152
acceptance tests, 4, 7–10
failing, 6–7, 39–40, 42, 271
for changed requirements, 40
for completed features, 40
for degenerate cases, 41
for new features, 6, 39–40, 105, 225
readability of, 42
Action interface, 341, 344
ActionListener interface, 185, 187
ActiveDirectory, 232
adapters, 48, 70–71, 284, 297
addSniper(), 180
addUserRequestListenerFor(), 187
adjustments, 52–53, 238
mocking, 58
@After annotation, 23, 96
@AfterClass annotation, 223
Agile Development, 35, 47, 81, 83, 205, 329
aliasing, 50
allOf(), Hamcrest, 340
allowances, 146, 277–279
allowing(), jMock, 145–146, 181, 211, 243,
278, 278, 339
an(), jMock, 340
announce(), jMock, 187
announceClosed(), 106–107, 176
Announcer class, 187, 192
aNonNull(), jMock, 340
ant build tool, 95
aNull(), jMock, 340
any(), Hamcrest, 340
anyOf(), Hamcrest, 340
Apache Commons IO library, 221
application model, 48
ApplicationRunner class, 85, 89–92,
106–107, 140, 153, 168, 175–177, 183,
207, 254
aRowChangedEvent(), 157, 162
ArrayIndexOutOfBoundsException, 217
aSniperThatIs(), 161–162, 278
assertColumnEquals(), 157
assertEquals(), JUnit, 21–22, 276
assertEventually(), 321–323, 326
assertFalse(), JUnit, 24, 255
assertions, 22, 254–255
extending, 343–345
failing, 24, 268
messages for, 268
naming, 86
narrowness of, 255, 275–276
quantity of, 252
vs. synchronizations, 326
vs. test setup, 211
assertIsSatisﬁed(), JUnit, 271
assertNull(), JUnit, 21–22
assertRowMatchesSnapshot(), 180
assertThat(), JUnit, 24–25, 253–255, 268,
276
assertTrue(), JUnit, 21–22, 24, 255
asynchrony, 87, 180, 216, 262
testing, 315–327
atLeast(), jMock, 127, 278, 339
atMost(), jMock, 339
AtomicBigCounter class, 311–312
AtomicInteger class, 309–310
attachModelListener(), Swing, 156–157
Auction interface, 62, 126–131, 136, 155,
193, 203
Auction Sniper, 75–226
bidding, 79, 84, 105–121, 126–131, 162
for multiple items, 175
stopping, 79, 205–213
connecting, 108, 111, 179, 183
disconnecting, 219–220
displaying state of, 97–98, 128, 144–146,
152–155, 159–160, 171, 323
failing, 215–217
joining auctions, 79, 84, 91, 94, 98–100,
179–181, 184–186, 197–199
losing, 79, 84, 91, 100–102, 125, 130,
164, 205–206
portfolio of, 199
refactoring, 191–203
Index
 
349


---
**Page 350**

Auction Sniper (continued)
synchronizing, 106, 301
table model for, 149–152, 156–160, 166
translating messages from auction,
112–118, 139–142, 217
updating current price, 118–121
user interface of, 79, 84, 96–97, 149–173,
183–188, 207–208, 212, 316
walking skeleton for, 79, 83–88
when an auction is closed, 84, 94
winning, 79, 139–148, 162–164
auctionClosed(), 25, 58, 116–117,
119–120, 123–125
AuctionEvent class, 134–136
AuctionEventListener interface, 19, 26, 61,
113, 117, 120, 123–124, 141, 192–193,
217–220
auctionFailed(), 217–220
AuctionHouse interface, 196, 210
AuctionLogDriver class, 221, 224
AuctionMessageTranslator class, 25–27, 61,
112–118, 134–136, 154, 192, 195,
217–219, 222, 224, 226
AuctionMessageTranslatorTest class, 141
AuctionSearchStressTests class, 307–309
AuctionSniper class, 62, 123–134, 154–155,
172–173, 192, 198–199, 208, 210–212
AuctionSniperDriver class, 91, 153, 168,
184, 207, 254
AuctionSniperEndToEndTest class, 85, 152,
183
AuctionSniperTest class, 218
B
@Before annotation, 23
between(), jMock, 339
bidsHigherAndReportsBiddingWhenNew-
PriceArrives(), 127, 143
“Big Design Up Front,” 35
BlockingQueue class, 93
breaking out technique, 59–61, 136
budding off technique, 59, 61–62, 209
build
automated, 9, 36–37, 95
features included in, 8
from the start of a project, 31
build(), 258–261
Builder pattern, 66, 337
builders. See test data builders, 254
bundling up technique, 59–60, 62, 154
C
C# programming language, 225
cannotTranslateMessage(), 222–223
CatalogTest class, 21, 23
Chat class, 112, 115, 129–130, 185, 192,
219
encapsulating, 193–195
chatDisconnectorFor(), 220, 226
ChatManager class, 101, 129
ChatManagerListener interface, 92
check(), WindowLicker, 187
checking(), jMock, 210, 337
classes, 14
coherent, 12
context-independent, 55
encapsulating collections into, 136
helper, 93
hierarchy of, 16, 67
internal features of, 237
loosely coupled, 11–12
mocking, 223–224, 235–237
naming, 63, 159–160, 238, 285, 297
tightly coupled, 12
Clock interface, 230–232
code
adapting, 172
assumptions about, 42
cleaning up, 60, 118, 125, 131, 137, 245,
262–264
compiling, 136
declarative layer of, 65
difﬁcult to test, 44, 229
external quality of, 10–11
implementation layer of, 65
internal quality of, 10–11, 60
loosely coupled, 11–12
maintenance of, 12, 125
readability of, 51, 162, 173, 226, 247
reimplementing, 60
tightly coupled, 12
code smells, 63, 181
cohesion, 11–12
collaborators, 16, 279
collections
encapsulating, 136
vs. domain types, 213
commands, 78, 278
commit(), 279
communication patterns, 14, 58
communication protocols, 58, 63
Index
350


---
**Page 351**

ComponentDriver, 90
“composite simpler than the sum of its
parts,” 53–54, 60, 62
concurrency, 301–306, 309, 313–316
connect(), Smack, 100
connection(), 100
Connextra, 330–332
constants, 255
constructors
bloated, 238–242
real behavior in, 195
container-managed transactions, 293
containsTotalSalesFor(), 264
context independence, 54–57, 233, 305
CountDownLatch class, 194
coupling, 11–12
CRC cards, 16, 186, 333
createChat(), Smack, 129
Crystal Clear, 1
currentPrice(), 118–120, 123, 141,
162–163
currentTimeMillis(), java.lang.System,
230
customer tests. See acceptance tests
D
DAO (Data Access Object), 297
database tests. See persistence tests
DatabaseCleaner class, 291–292
databases
cleaning up before testing, 290–292
operations with active transactions in, 300
data-driven tests, 24
date manipulation, 230–233
“debug hell,” 267
Decorator pattern, 168, 300
Defect exception, 165
dependencies, 52–53, 126
breaking in unit tests, 233
explicit, 14
hidden, 273
implicit, 57, 232–233
knowing about, 231
loops of, 117, 129, 192
mocking, 58
on user interface components, 113
quantity of, 57, 241–242, 273
scoping, 62
using compiler for navigating, 225
dependency injections, 330
deployment, 4, 9
automated, 35–37
from the start of a project, 31
importance for testing, 32
describeMismatch(), Hamcrest, 343–345
describeTo(), Hamcrest, 343–345
design
changing, 172
clarifying, 235
feedback on, 6
quality of, 273
DeterministicExecutor class, 303–304
development
from inputs to outputs, 43, 61
incremental, 4, 36, 73, 79, 136, 201, 303
iterative, 4
of user interface, 183
working compromises during, 90, 95
disconnect(), Smack, 111
disconnectWhenUICloses(), 111, 179
domain model, 15, 48, 59, 71, 290
domain types, 213, 262, 269
domain-speciﬁc language, embedded in Java,
332
“Don’t Repeat Yourself” principle, 248
duplication, 262–264, 273, 275
Dynamock library, 332
E
Eclipse development environment, 119
encapsulation, 49–50, 55
end-to-end tests, 8–10
asynchronous, 87
brittleness of, 87
early, 32–33
failing, 87
for event-based systems, 87
for existing systems, 33, 37
on synchronization, 313
running, 11
simulating input and output events, 43
slowness of, 87, 300
EntityManager class, 279, 297, 299
EntityManagerFactory class, 279
EntityTransaction class, 279
equal(), jMock, 340
equals(), java.lang.Object, 154
equalTo(), Hamcrest, 322
error messages. See failure messages
event-based systems, 86–87
351
Index


---
**Page 352**

events, 78
external, 71, 326–327
listening for, 316–317, 323–325
processed in sequence, 325–326
exactly(), jMock, 338
exceptions, 22
catching, 253–254
on hidden threads, 302
runtime, 165
with helpful messages, 330
Executor interface, 303, 305
“Expect Unexpected Changes” principle, 45
Expectation jMock class, 64
ExpectationCounter jMock class, 330
expectations, 18, 27, 64–66, 146, 254–255,
277–279, 338
blocks of, 337, 339
checking after test’s body, 271
clear descriptions of, 25
narrowness of, 255, 277–283
order of, 128, 282, 341–342
quantity of, 242–244, 252
specifying actions to perform, 341
Expectations jMock class, 66, 337, 340
ExpectationSet jMock class, 330
ExpectationValue jMock class, 330
expectFailureWithMessage(), 222
expectSniperToFailWhenItIs(), 219, 253
F
failed(), 219
failure messages, 268–269, 276
clearness of, 42
self-explanatory, 24–25, 343
failures, 41
detecting, 217–218
diagnostics for, 267–273, 297, 302–307,
332
displaying, 218–219
handling, 215–226
messages about, 255
recording, 221–225, 291
writing down while developing, 41
FakeAuctionServer class, 86, 89, 92–95,
107–110, 120, 176, 194, 254, 276
FeatureMatcher Hamcrest class, 162, 178
feedback, 4, 229, 233
from automated deployment, 35–36
incremental, 300
loops of, 4–5, 8, 40
on design, 6, 299
on failure cases, 41
on implementations, 6
rapid, 317
Findbugs, 313
ﬁxtures, 23
functional tests. See acceptance tests
G
garbage collection, 23, 91, 101, 192–194
getBody(), Smack, 222
getColumnCount(), Swing, 158
getValueAt(), Swing, 158
H
Hamcrest library, 21, 24–25, 95, 268, 274,
296, 322, 333, 340, 343–345
hasColumnTitles(), 169
hasEnoughColumns(), 156–157
hashCode(), java.lang.Object, 154
hasProperty(), Hamcrest, 178
hasReceivedBid(), 106–107
hasReceivedJoinRequestFrom(), 109, 176
hasReceivedJoinRequestFromSniper(),
106–108
hasShownSniperHasWon(), 323
hasShownSniperIsBidding(), 106, 110
hasShownSniperIsLosing(), 206–207
hasShownSniperIsWinning(), 140, 176, 323
hasTitle(), 169
helper methods, 7, 51, 66, 162, 166, 210,
226, 253, 263, 280
naming, 51, 162
Hibernate, 48, 289, 294
HTTP (HyperText Transfer Protocol), 81
I
IDEs
ﬁlling in missing methods on request, 119
navigation in, 114
IETF (Internet Engineering Task Force), 77
ignoring(), jMock, 145, 278–279, 339
ignoringAuction(), 219
IllegalArgumentException, 22
implementations
feedback on, 6
independent of context, 244
null, 130, 136, 180, 218
Index
352


---
**Page 353**

index cards
for technical tasks to be addressed, 41
for to-do lists, 80–81, 103, 120–121,
130–131, 148, 171, 182, 201,
211–212, 225
information hiding, 49, 55–56
initializers, 23
inSequence(), jMock, 338, 341
instanses, 237–238
integration tests, 9–10, 186–188
and threads, 71
difﬁcult to code, 44
for adapters, 70
for persistence implementations, 300
passing, 40
speed of, 300
IntelliJ IDEA, 119, 250
interface discovery, 19
interfaces, 14, 58, 61
callback, 71
implementing, 63–64
mocking, 235
naming, 63–64, 237, 297
narrowness of, 63
pulling, 61, 63
refactoring, 63–64
relationships with, 63
segregating, 236
invocations
allowed, 27, 146
constrained, 342
counting, 338–339
expected, 27, 146
number of, 27
order of, 279–282, 341
invokeAndWait(), Swing, 100, 180
invokeLater(), Swing, 100
isForSameItemAs(), 181
isSatisﬁed(), WindowLicker, 320–321
Item class, 209–211, 213
iteration zero, 83, 102
J
Jabber. See XMPP
Java programming language, 21
arrays in, 177
collections in, 179
logging framework in, 223
method overloading in, 261
package loops in, 191
synchronization errors in, 313
syntax noise of, 253
using compiler to navigate dependencies,
225
Java EE (Java Platform, Enterprise Edition),
293–294, 301
Java Servlet API, 330
JAXB (Java API for XML Binding), 289
JButton Swing component, 185
JDBC (Java Database Connectivity), 294
JDO (Java Data Objects), 289
JFormattedTextField Swing component, 208
JFrame Swing component, 96
JFrameDriver WindowLicker class, 91
JIDs (Jabber IDs), 77, 197
JLabel Swing component, 150
jMock library, 24–27, 274, 332
allowances in, 146
double braces in, 337
expectations in, 25, 64–66, 146
extensions to, 162
generating messages in, 345
states in, 145
using for stress tests, 307
verifying mock objects in, 24
version 2, 21, 25–27, 333, 335–342
JMS (Java Messaging Service), 292
JMSTransactor class, 292
joinAuction(), 100, 131–132, 142,
180–182, 187–188, 192, 208
JPA (Java Persistence API), 279, 289, 294
persistence identiﬁers in, 295
JTA (Java Transaction API), 292
JTable Swing component, 52, 149–157, 170
JTATransactor class, 292–293
JTextField Swing component, 185
JUnit library, 84, 274, 332–333
generating messages in, 345
new instances for each test in, 22, 117
version 4.5, 24
version 4.6, 21, 335
JUnit4Mockery jMock class, 336
L
Law of Demeter. See “Tell, Don’t Ask”
principle
Lisp programming language, 66
literals. See values
locks, 302, 318
log ﬁles, 221–225, 291
cleaning up before testing, 221
generating, 223
353
Index


---
**Page 354**

Logger class, 223–224, 237
logging, 233–235
amount of, 235
diagnostic, 233–235
isolated in a separate class, 226
LoggingXMPPFailureReporter class, 223–224
LTSA tool, 302, 313
M
Main class, 91, 101, 108, 117–118, 123, 126,
132–134, 142, 168, 178–180, 183, 185,
188–203
matchmaker role of, 191
main(), 91, 96
MainWindow class, 96, 100, 113, 134, 151,
156, 166–167, 185–187, 199, 208–209
MainWindowTest class, 186, 209
makeControls(), 184–185
Mars Climate Orbiter disaster, 59
Matcher interface, 25, 268, 343–345
matchers, 24–25, 95, 155, 157, 276, 322,
339–340
combining, 24
custom, 25, 178, 296, 340, 343–345
reversing, 24
stateless, 344
Matchers Hamcrest class, 340
matches(), Hamcrest, 343
meetings, 4
MessageHandler class, 217
MessageListener interface, 93–94, 99,
112–115, 129, 219
messages, 13, 17
between objects, 50, 58
creating and checking in the same
construct, 109
parsing, 118–120
See also failure messages
methods, 13
calling, 65
order of, 128
expected, 339–340
factory, 257–258, 260–261
getter, 329–330
grouping together, 176
ignoring, 279
naming, 86, 173, 250
overloading, 261
side effects of, 51
“sugar,” 65–66
testing, 43
See also helper methods
MissingValueException, 218
mock objects, 18–20, 25–27
creating, 336
for third-party code, 69–71, 157, 300
history of, 329–333
invocation order of, 279–282
naming, 336
to visualize protocols, 58, 61
mockery, 20, 25
Mockery jMock class, 26, 64, 66, 307, 336
mocking
adjustments, 58
classes, 223–224, 235–237
dependencies, 58
interfaces, 235
notiﬁcations, 58
peers, 58
returned types, 279
third-party code, 237
values, 237–238
Moon program, 41
multithreading. See threads
N
.Net, 22, 232
“Never Pass Null between Objects”
principle, 274
never(), jMock, 339
NMock library, 332
not(), Hamcrest, 24, 340
notiﬁcations, 52–53, 126, 192
capturing, 318–320
mocking, 58
order of, 280
recording, 324
notifiesAuctionClosedWhenCloseMessage-
Received(), 114
notifiesAuctionFailedWhenBadMessage-
Received(), 217
notifiesAuctionFailedWhenEventType-
Missing(), 218
notifiesBidDetailsWhenCurrentPrice-
MessageReceivedFromOtherBidder(),
141
notifiesBidDetailsWhenCurrentPrice-
MessageReceivedFromSniper(), 141
notToBeGCd ﬁeld, 101, 179, 197, 200, 203
NullPointerException, 53, 274
NUnit library, 22, 117, 332
Index
354


---
**Page 355**

O
object mother pattern, 257–258
object-oriented programming, 13, 329
objects
abstraction level of, 57
bringing out relationships between, 236
collaborating, 18–20, 52–53, 58, 60–62,
186
communicating, 13–14, 50, 58, 244–245
composite, 53–54
context-independent, 54–55, 233
created by builders, 259–260
difﬁcult to decouple, 273
mutable, 14
sharing references to, 50
naming, 62, 244
null, 22, 115, 130, 242
observable invariants with respect to
concurrency of, 306
passive, 311–312
persistent, 298–299
simplifying, 55
single responsibility of, 51–52
states of, 13, 59, 145–146, 281–283, 299,
306, 342
subordinate, 254, 291–292, 311
tracer, 270–271
validity of, 53
vs. values, 13–14, 51, 59
web of, 13, 64–65
oneOf(), jMock, 278, 337–338
Openﬁre, 86, 89, 95
ORM (Object/Relational Mapping), 289,
297, 299
P
packages
loops of, 191
single responsibility of, 52
pair programming, 4
patterns, naming after, 297
peers, 50
mocking, 58
types of, 52–53
persistence tests, 289–300
and transactions, 292–294
cleaning up at the start, 291
failure diagnostics in, 297
isolating from one another, 290–292
round-trip, 297–300
slowness of, 300
Poller class, 320–321
polling for changes, 317, 320–321, 323–325
PortfolioListener interface, 199
ports, 48
“ports and adapters” architecture, 48, 201,
284, 297
PriceSource enumeration, 141, 148
Probe interface, 320–322
probing a system, 315, 320–322
processMessage(), Smack, 114–115,
135–136, 217, 219
production environment, 95
programming styles, 51
progress measuring, 4, 40
PropertyMatcher Hamcrest class, 178
Q
queries, 278
R
receivesAMessageMatching(), 108
redesign, 7
refactoring, 5–7
code difﬁcult to test, 44–45
importance of, during TDD, 225–226
incremental, 202
writing down while developing, 41
reference types, 269
regression suites, 6, 40
regression tests, 5
releases, 4, 9
planning, 81
to a production system, 35
removeMessageListener(), Smack, 220
reportPrice(), 106–107, 176
reportsInvalidMessage(), 216, 221
reportsLostIfAuctionClosesImmediately(),
145
reportsLostIfAuctionClosesWhenBidding(),
146
repository pattern, 297
resetLogging(), 223
responsibilities, 16, 171, 220, 222
quantity of, 61, 240–241, 332
See also “single responsibility” principle
reverting changes, 267
rock climbing, 202
roles, 16
rollback(), 279
rolling back, 267
Ruby programming language, 331
355
Index


---
**Page 356**

Rule annotation, 24
RuntimeException, 255, 277
runUntilIdle(), 304
@RunWith annotation, 23, 26, 336
S
safelyAddItemToModel(), 180, 188
same(), jMock, 340
sample(), WindowLicker, 320–321
scheduled activities, 326–327
Scrum projects, 1
SelfDescribing interface, 343
sendInvalidMessageContaining(), 216
Sequence jMock class, 341–342
sequences, 279–282, 341–342
servlets, 301, 311
setImposteriser(), jMock, 223
setStatusText(), 166
[Setup] methods, 22
showsSniperHasFailed(), 216
showsSniperHasWonAuction(), 140, 176
showsSniperStatus(), 91–92
“single responsibility” principle, 51–52, 113,
123, 125, 220, 222
SingleMessageListener class, 93–94,
107–108
singleton pattern, 50, 230
Smack library, 86
exceptions in, 217
threads in, 93, 301
Smalltalk programming language
cascade, 258, 330, 332
programming style compared to Java, 330
Sniper application. See Auction Sniper
Sniper class, 62
sniperAdded(), 203
sniperBidding(), 126–128, 155, 160–162
SniperCollector class, 62, 198–199, 245
sniperForItem(), 198
SniperLauncher class, 62, 197–199, 210
SniperListener interface, 124–126, 133,
154–155, 163–164, 168
sniperLost(), 125, 147, 164
sniperMakesAHigherBidButLoses(), 139
SniperPortfolio class, 199–203
sniperReportsInvalidAuctionMessageAnd-
StopsRespondingToEvents(), 216
SniperSnapshot class, 159–164, 173,
180–181, 198–199, 211, 219, 278
SnipersTableModel class, 149, 151–152, 156,
166, 168, 170–171, 180–182, 185,
197–201, 207
SniperState class, 155, 158–161, 207, 216,
278
sniperStateChanged(), 156–164, 278
SniperStateDisplayer class, 133, 147, 155,
167–168
sniperWinning(), 143, 162–163
sniperWinsAnAuctionByBiddingHigher(),
139
sniperWon(), 147, 164
Spring, 294
startBiddingFor(), 184
startBiddingIn(), 177
startBiddingWithStopPrice(), 206–207
startSellingItem(), 92, 176
startSniper(), 183–184
startsWith(), Hamcrest, 343–345
state machines, 279–282, 342
state transition diagrams, 212
States jMock class, 146, 198, 281–283
static analysis tools, 313
stop price, 80, 205–213
stress tests, 306–313
failing, 308–309, 313
on event processing order, 326
on passive objects, 311–312
running in different environments, 313
strings
checking if starts with a given preﬁx,
343–345
comparing, 14
vs. domain types, 213, 262, 269
StringStartsWithMatcher Hamcrest class,
345
stubs, 84, 243, 277, 339
success cases, 41
Swing
manipulating features in, 90
testing, 86–87
threads in, 123, 133, 180, 301
SwingThreadSniperListener interface, 168,
197, 199
Synchroniser jMock class, 307–308,
312–313
synchronizations, 301–314
errors in, 302
testing, 302, 306–310, 313
vs. assertions, 326
Index
356


---
**Page 357**

system
application model of, 48
changing behavior of, 48, 55
concurrency architecture of, 301–302
maintainability of, 47
public drawings of, during development,
34
returning to initial state after a test, 323
simplifying, 112
system tests. See acceptance tests
T
tableChanged(), Swing, 157, 181
TableModel class, 149, 168–171
TableModelEvent class, 157, 180–181
TableModelListener class, 156–157
task runners, 303
TDD (Test-Driven Development), 1, 5, 229
cycle of, 6, 39–45, 271–272
for existing systems, 37
golden rule of, 6
kick-starting, 31–37
sustainable, 227–285
[TearDown] methods, 22
“Tell, Don’t Ask” principle, 17, 54, 245
template methods, 344
test data builders, 238, 258–259
calling within transactions, 300
combining, 261, 300
creating similar objects with, 259–260
lists of, 298–299
removing duplication with, 262–264
wrapping up in factory methods, 261
test runner, 23–24
JMock, 26
Parameterized, 24
“test smells,” 229, 235, 248
beneﬁts of listening to, 244–246
@Test annotation, 22
TestDox convention, 249–250
Test-Driven Development. See TDD
tests
against fake services, 84, 88, 93
against real services, 32, 88, 93
asynchronous, 315–327
at the beginning of a project, 36, 41
brittleness of, 229, 255, 257, 273
cleaning up, 245, 248, 273
decoupling from tested objects, 278
dependencies in, 275
explicit constraints in, 280
failing, 267–273
ﬂexibility of, 273–285
ﬂickering, 317
focused, 273, 277, 279, 279
for late integration, 36
hierarchy of, 9–10
maintaining, 247, 273–274
naming, 44, 248–250, 252, 264, 268, 326
readability of, 247–257, 273, 280
repeatability of, 23
runaway, 322–323
running, 6
sampling, 316–317, 320–325
self-explanatory, 274–275
separate packages for, 114
size of, 45, 268
states of, 283
synchronizing, 301–314, 317
with background threads, 312–313
tightly coupled, 273
triggering detectable behavior, 325
writing, 6
backwards, 252
in a standard form, 251–252
See also acceptance tests, end-to-end tests,
integration tests, persistence tests,
unit tests
textFor(), 166
“the simplest thing that could possibly
work,” 41
then(), jMock, 281–282, 338, 342
third-party code, 69–72
abstractions over, 10
mocking, 69–71, 157, 237, 300
patching, 69
testing integration with, 186–188, 289
value types from, 71
Thor Automagic, 12
threads, 71, 301–315
scheduling, 313
three-point contact, 202
time boxes, 4
Timeout class, 318, 322
timeouts, 230, 312–313, 316–318
timestamps, 276
toString(), java.lang.Object, 154
tracer object, 270–271
“train wreck” code, 17, 50–51, 65
transaction management, 294
transactors, 292–293
translate(), 217
357
Index


---
**Page 358**

translatorFor(), 220, 226, 253
TypeSafeMatcher<String> Hamcrest class,
344
U
unit tests, 4, 9
against static global objects, 234
and threads, 301–314
at the beginning of a project, 43
breaking dependencies in, 233
brittleness of, 245
difﬁcult to code, 44
failing, 8
isolating from each other, 22, 117
length of, 245–246
limiting scope of, 57
naming, 114, 141
on behavior, not methods, 43
on collaborating objects, 18–20
on synchronization, 302, 306–310, 313
passing, 40
readability of, 245–246
simplifying, 62
speed of, 300, 312
structure of, 335–342
writing, 11
Unix, 66
User Experience community, 81, 212
user interface
conﬁguring through, 242
dependencies on, 113
handling user requests, 186
support logging in, 233
working on parallel to development, 183,
212
UserRequestListener interface, 186–188,
208–209, 213
V
value types, 59–60, 141
from third-party code, 71
helper, 59
naming, 173
placeholder, 59, 209
public ﬁnal ﬁelds in, 154
vs. values, 59
with generics, 136
valueIn(), 166–167
ValueMatcherProbe WindowLicker class, 187
values, 255–256
comparing, 22
expected, 127
immutable, 50, 59
mocking, 237–238
mutable, 50
obviously canned, 270
self-describing, 269, 285
side effects of, 51
vs. objects, 13–14, 51, 59
variables, 255–256
global, 50
naming, 209, 330
W
waitForAnotherAuctionEvent(), 216
waitUntil(), 326
walking skeleton, 32–37
for Auction Sniper, 79, 83–88
when(), jMock, 281–282, 338, 342
whenAuctionClosed(), 164–165
will(), jMock, 338, 341
WindowAdapter class, 134
WindowLicker library, 24, 86–87, 186–187,
254, 316
controlling Swing components in, 90–91
error messages in, 96
with(), jMock, 339–340
overloaded, 261
X
XmlMarshaller class, 284–285
XmlMarshallerTest class, 284
XMPP (eXtensible Messaging and Presence
Protocol), 76–77, 105, 203
messages in, 301
reliability of, 81
security of, 81
XMPP message brokers, 84, 86, 95
XMPPAuction class, 62, 131–132, 192–197,
203, 224
XMPPAuctionException, 224
XMPPAuctionHouse class, 62, 196–197, 203,
224
XMPPConnection class, 195–197
XMPPException, 130
XMPPFailureReporter class, 222–223, 226
XP (Extreme Programming), 1, 41, 331
XStream, 289
XTC (London Extreme Tuesday Club), 331
Index
358


---
**Page 359**

 InformIT is a brand of Pearson and the online presence 
for the world’s leading technology publishers. It’s your source 
for reliable and qualified content and knowledge, providing 
access to the top brands, authors, and contributors from 
the tech community.
informIT.com
THE TRUSTED TECHNOLOGY LEARNING SOURCE
LearnIT at InformIT
Looking for a book, eBook, or training video on a new technology? Seeking 
timely and relevant information and tutorials? Looking for expert opinions, 
advice, and tips?  InformIT has the solution.
•
Learn about new releases and special promotions by 
subscribing to a wide variety of newsletters. 
Visit informit.com/newsletters.
•   Access FREE podcasts from experts at informit.com/podcasts.
•   Read the latest author articles and sample chapters at 
informit.com/articles.
•
Access thousands of books and videos in the Safari Books 
Online digital library at safari.informit.com.
• Get tips from expert blogs at informit.com/blogs.
Visit informit.com/learn to discover all the ways you can access the 
hottest technology content.
informIT.com THE TRUSTED TECHNOLOGY LEARNING SOURCE
Are You Part of the IT Crowd?
Connect with Pearson authors and editors via RSS feeds, Facebook, 
Twitter, YouTube, and more! Visit informit.com/socialconnect.


---
**Page 360**

Your purchase of Growing Object-Oriented Software, Guided by Tests includes access 
to a free online edition for 45 days through the Safari Books Online subscription service. 
Nearly every Addison-Wesley Professional book is available online through Safari Books 
Online, along with more than 5,000 other technical books and videos from publishers 
such as Cisco Press, Exam Cram, IBM Press, O’Reilly, Prentice Hall, Que, and Sams. 
SAFARI BOOKS ONLINE allows you to search for a speciﬁ c answer, cut and paste 
code, download chapters, and stay current with emerging technologies. 
Activate your FREE Online Edition at 
www.informit.com/safarifree
STEP 1:  Enter the coupon code: CYMIQVH.
STEP 2:  New Safari users, complete the brief registration form. 
Safari subscribers, just log in.
If you have difﬁ culty registering on Safari or accessing the online edition, 
please e-mail customer-service@safaribooksonline.com
FREE Online 
Edition


