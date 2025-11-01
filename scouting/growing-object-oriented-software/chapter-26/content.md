# Chapter 26: Unit Testing and Threads (pp.301-314)

---
**Page 301**

Chapter 26
Unit Testing and Threads
It is decreed by a merciful Nature that the human brain cannot think
of two things simultaneously.
—Sir Arthur Conan Doyle
Introduction
There’s no getting away from it: concurrency complicates matters. It is a challenge
when doing test-driven development. Unit tests cannot give you as much
conﬁdence in system quality because concurrency and synchronization are system-
wide concerns. When writing tests, you have to worry about getting the synchro-
nization right within the system and between the test and the system. Test failures
are harder to diagnose because exceptions may be swallowed by background
threads or tests may just time out with no clear explanation.
It’s hard to diagnose and correct synchronization problems in existing code,
so it’s worth thinking about the system’s concurrency architecture ahead of
time. You don’t need to design it in great detail, just decide on a broad-brush
architecture and principles by which the system will cope with concurrency.
This design is often prescribed by the frameworks or libraries that an
application uses. For example:
•
Swing dispatches user events on its own thread. If an event handler runs
for a long time, the user interface becomes unresponsive because Swing
does not process user input while the event handler is running. Event call-
backs must spawn “worker” threads to perform long-running tasks, and
those worker threads must synchronize with the event dispatch thread to
update the user interface.
•
A servlet container has a pool of threads that receive HTTP requests and
pass them to servlets for processing. Many threads can be active in the same
servlet instance at once.
•
Java EE containers manage all the threading in the application. The contain-
er guarantees that only one thread will call into a component at a time.
Components cannot start their own threads.
•
The Smack library used by the Auction Sniper application starts a daemon
thread to receive XMPP messages. It will deliver messages on a single thread,
301


---
**Page 302**

but the application must synchronize the Smack thread and the Swing thread
to avoid the GUI components being corrupted.
When you must design a system’s concurrency architecture from scratch, you
can use modeling tools to prove your design free of certain classes of synchroniza-
tion errors, such as deadlock, livelock, or starvation. Design tools that help you
model concurrency are becoming increasingly easy to use. The book Concurrency:
State Models & Java Programs [Magee06] is an introduction to concurrent pro-
gramming that stresses a combination of formal modeling and implementation
and describes how to do the formal modeling with the LTSA analysis tool.
Even with a proven design, however, we have to cross the chasm between design
and implementation. We need to ensure that our components conform to the
architectural constraints of the system. Testing can help at this point. Once we’ve
designed how the system will manage concurrency, we can test-drive the objects
that will ﬁt into that architecture. Unit tests give us conﬁdence that an object
performs its synchronization responsibilities, such as locking its state or blocking
and waking threads. Coarser-grained tests, such as system tests, give us conﬁdence
that the entire system manages concurrency correctly.
Separating Functionality and Concurrency Policy
Objects that cope with multiple threads mix functional concerns with synchro-
nization concerns, either of which can be the cause of test failures. Tests must
also synchronize with the background threads, so that they don’t make assertions
before the threads have ﬁnished working or leave threads running that might
interfere with later tests. Worse, in the presence of threads, unit tests do not
usually report failures well. Exceptions get thrown on the hidden threads, killing
them unexpectedly and breaking the behavior of the tested object. If a test times
out waiting for background threads to ﬁnish, there’s often no diagnostic other
than a basic timeout message. All this makes unit testing difﬁcult.
Searching for Auctions Concurrently
Let’s look at an example. We will extend our Auction Sniper application to let
the user search for auctions of interest. When the user enters search
keywords, the application will run the search concurrently on all auction houses
that the application can connect to. Each AuctionHouse will return a list of
AuctionDescriptions that contain information about its auctions matching the
search keywords. The application will combine the results it receives from all
AuctionHouses and display a single list of auctions to the user. The user can then
decide which of them to bid for.
The concurrent search is performed by an AuctionSearch object which passes
the search keywords to each AuctionHouse and announces the results they return
Chapter 26
Unit Testing and Threads
302


---
**Page 303**

to an AuctionSearchConsumer. Our tests for the Auction Search are complicated
because an AuctionSearch will spawn multiple threads per search, one for each
AuctionHouse. If it hides those threads behind its API, we will have to implement
the searching and notiﬁcation functionality and the synchronization at the same
time. When a test fails, we will have to work out which of those concerns is at
fault. That’s why we prefer our usual practice of incrementally adding
functionality test by test.
It would be easier to test and implement the AuctionSearch if we could tackle
the functional behavior and the synchronization separately. This would allow
us to test the functional behavior within the test thread. We want to separate the
logic that splits a request into multiple tasks from the technical details of how
those tasks are executed concurrently. So we pass a “task runner” in to the
AuctionSearch, which can then delegate managing tasks to the runner instead of
starting threads itself. In our unit tests we’ll give the AuctionSearch a fake task
runner that calls tasks directly. In the real system, we’ll give it a task runner that
creates threads for tasks.
Introducing an Executor
We need an interface between the AuctionHouse and the task runner. We can use
this one from Java’s standard java.util.concurrent package:
public interface Executor {
  void execute(Runnable command);
}
How should we implement Executor in our unit tests? For testing, we need to
run the tasks in the same thread as the test runner instead of creating new task
threads. We could use jMock to mock Executor and write a custom action to
capture all calls so we can run them later, but that sounds too complicated. The
easiest option is to write a class to implement Executor. We can us it to explicitly
run the tasks on the test thread after the call to the tested object has returned.
jMock includes such a class, called DeterministicExecutor. We use this
executor to write our ﬁrst unit test. It checks that AuctionSearch notiﬁes its
AuctionSearchConsumer whenever an AuctionHouse returns search results and
when the entire search has ﬁnished.
In the test setup, we mock the consumer because we want to show how
it’s notiﬁed by AuctionSearch. We represent auction houses with a simple
StubAuctionHouse that just returns a list of descriptions if it matches keywords,
or an empty list if not (real ones would communicate to auction services over
the Internet). We wrote a custom stub, instead of using a jMock allowance, to
reduce the “noise” in the failure reports; you’ll see how this matters when
we start stress-testing in the next section. We also pass an instance of
DeterministicExecutor to AuctionSearch so that we can run the tasks within
the test thread.
303
Separating Functionality and Concurrency Policy


---
**Page 304**

@RunWith(JMock.class)
public class AuctionSearchTests {
  Mockery context = new JUnit4Mockery();
  final DeterministicExecutor executor = new DeterministicExecutor();
  final StubAuctionHouse houseA = new StubAuctionHouse("houseA");
  final StubAuctionHouse houseB = new StubAuctionHouse("houseB");
  List<AuctionDescription> resultsFromA = asList(auction(houseA, "1"));
  List<AuctionDescription> resultsFromB = asList(auction(houseB, "2"));;
  final AuctionSearchConsumer consumer = context.mock(AuctionSearchConsumer.class);
  final AuctionSearch search = 
                        new AuctionSearch(executor, houses(houseA, houseB), consumer);
  @Test public void 
searchesAllAuctionHouses() throws Exception {
    final Set<String> keywords = set("sheep", "cheese");
    houseA.willReturnSearchResults(keywords, resultsFromA);
    houseB.willReturnSearchResults(keywords, resultsFromB);
    context.checking(new Expectations() {{
      final States searching = context.states("searching");
      oneOf(consumer).auctionSearchFound(resultsFromA); when(searching.isNot("done"));
      oneOf(consumer).auctionSearchFound(resultsFromB); when(searching.isNot("done"));
      oneOf(consumer).auctionSearchFinished();          then(searching.is("done"));
    }});
    search.search(keywords);
executor.runUntilIdle();
  }
}
In the test, we conﬁgure the StubAuctionHouses to return example results when
they’re queried with the given keywords. We specify our expectations that the
consumer will be notiﬁed of the two search results (in any order), and then that
the search has ﬁnished.
When we call search.search(keywords), the AuctionSearch hands a task for
each of its auction houses to the executor. By the time search() returns, the tasks
to run are queued in the executor. Finally, we call executor.runUntilIdle() to
tell the executor to run queued tasks until its queue is empty. The tasks run on
the test thread, so any assertion failures will be caught and reported by JUnit,
and we don’t have to worry about synchronizing the test thread with background
threads.
Implementing AuctionSearch
This implementation of AuctionSearch calls its executor to start a search for
each of its auction houses. It tracks how many searches are unﬁnished in its
runningSearchCount ﬁeld, so that it can notify the consumer when it’s ﬁnished.
Chapter 26
Unit Testing and Threads
304


---
**Page 305**

public class AuctionSearch {
  private final Executor executor;
  private final List<AuctionHouse> auctionHouses;
  private final AuctionSearchConsumer consumer;
private int runningSearchCount = 0;
  public AuctionSearch(Executor executor, 
                       List<AuctionHouse> auctionHouses, 
                       AuctionSearchConsumer consumer) 
  {
    this.executor = executor;
    this.auctionHouses = auctionHouses;
    this.consumer = consumer;
  }
  public void search(Set<String> keywords) {
    for (AuctionHouse auctionHouse : auctionHouses) {
      startSearching(auctionHouse, keywords);
    }
  }
  private void startSearching(final AuctionHouse auctionHouse, 
                              final Set<String> keywords) 
  {
runningSearchCount++;
    executor.execute(new Runnable() {
      public void run() {
        search(auctionHouse, keywords);
      }
    });
  }
  private void search(AuctionHouse auctionHouse, Set<String> keywords) {
    consumer.auctionSearchFound(auctionHouse.findAuctions(keywords));
runningSearchCount--;
    if (runningSearchCount == 0) {
      consumer.auctionSearchFinished();
    }
  }
}
Unfortunately, this version is unsafe because it doesn’t synchronize access to
runningSearchCount. Different threads may overwrite each other when they
decrement the ﬁeld. So far, we’ve clariﬁed the core behavior. We’ll drive out this
synchronization issue in the next test. Pulling out the Executor has given us two
advantages. First, it makes development easier as we can unit-test the basic
functionality without getting confused by threading issues. Second, the object’s
API no longer hides its concurrency policy.
Concurrency is a system-wide concern that should be controlled outside the
objects that need to run concurrent tasks. By passing an appropriate Executor
to the constructor, we’re following the “context independence” design principle.
305
Separating Functionality and Concurrency Policy


---
**Page 306**

The application can now easily adapt the object to the application’s threading
policy without changing its implementation. For example, we could introduce a
thread pool should we need to limit the number of active threads.
Unit-Testing Synchronization
Separating the functional and synchronization concerns has let us test-drive the
functional behavior of our AuctionSearch in isolation. Now it’s time to test-drive
the synchronization. We will do this by writing stress-tests that run multiple
threads through the AuctionSearch implementation to cause synchronization
errors. Without precise control over the thread scheduler, we can’t guarantee
that our tests will ﬁnd synchronization errors. The best we can do is run the same
code enough times on enough threads to give our tests a reasonable likelihood
of detecting the errors.
One approach to designing stress tests is to think about the aspects of an ob-
ject’s observable behavior that are independent of the number of threads calling
into the object. These are the object’s observable invariants with respect to con-
currency.1 By focusing on these invariants, we can tune the number of threads
in a test without having to change its assertions. This gives us a process for
writing stress tests:
•
Specify one of the object’s observable invariants with respect to concurrency;
•
Write a stress test for the invariant that exercises the object multiple times
from multiple threads;
•
Watch the test fail, and tune the stress test until it reliably fails on every
test run; and,
•
Make the test pass by adding synchronization.
We’ll demonstrate this with an example.
Safety First
In this chapter we have made the unit tests of functional behavior pass before we
covered stress testing at the unit level because that allowed us to explain each
technique on its own. In practice, however, we often write both a unit test for func-
tionality and a stress test of the synchronization before writing any code, make
sure they both fail, then make them both pass.This helps us avoid checking in code
that passes its tests but contains concurrency errors.
1. This differs from the use of invariants in “design by contract” and formal methods
of modeling concurrency. These deﬁne invariants over the object’s state.
Chapter 26
Unit Testing and Threads
306


---
**Page 307**

A Stress Test for AuctionSearch
One invariant of our AuctionSearch is that it notiﬁes the consumer just once
when the search has ﬁnished, no matter how many AuctionHouses it searches—that
is, no matter how many threads its starts.
We can use jMock to write a stress test for this invariant. We don’t always use
jMock for stress tests because expectation failures interfere with the threads of
the object under test. On the other hand, jMock reports the actual sequence
of calls to its mock objects when there is a failure, which helps diagnose defects.
It also provides convenient facilities for synchronizing between the test thread
and the threads being tested.
In AuctionSearchStressTests, we set up AuctionSearch with a thread-pool
executor that will run tasks in background threads, and a list of auction houses
stubbed to match on the given keywords. jMock is not thread-safe by default,
so we set up the Mockery with a Synchroniser, an implementation of its threading
policy that allows us to call mocked objects from different threads. To make
tuning the test easier, we deﬁne constants at the top for the “degree of stress”
we’ll apply during the run.
@RunWith(JMock.class)
public class AuctionSearchStressTests {
  private static final int NUMBER_OF_AUCTION_HOUSES = 4; 
  private static final int NUMBER_OF_SEARCHES = 8;
  private static final Set<String> KEYWORDS = setOf("sheep", "cheese");
  final Synchroniser synchroniser = new Synchroniser();
  final Mockery context = new JUnit4Mockery() {{
    setThreadingPolicy(synchroniser);
  }};
  final AuctionSearchConsumer consumer = context.mock(AuctionSearchConsumer.class);
  final States searching = context.states("searching");
  final ExecutorService executor = Executors.newCachedThreadPool();
  final AuctionSearch search = new AuctionSearch(executor, auctionHouses(), consumer); 
[…]
  private List<AuctionHouse> auctionHouses() {
    ArrayList<AuctionHouse> auctionHouses = new ArrayList<AuctionHouse>();
    for (int i = 0; i < NUMBER_OF_AUCTION_HOUSES; i++) {
      auctionHouses.add(stubbedAuctionHouse(i));
    }
    return auctionHouses;
  }
  private AuctionHouse stubbedAuctionHouse(final int id) {
    StubAuctionHouse house = new StubAuctionHouse("house" + id);
    house.willReturnSearchResults(
        KEYWORDS, asList(new AuctionDescription(house, "id" + id, "description")));
    return house;
  } 
307
Unit-Testing Synchronization


---
**Page 308**

  @Test(timeout=500) public void 
onlyOneAuctionSearchFinishedNotificationPerSearch() throws Exception {
    context.checking(new Expectations() {{ 
      ignoring (consumer).auctionSearchFound(with(anyResults()));
    }});
    for (int i = 0; i < NUMBER_OF_SEARCHES; i++) { 
      completeASearch();
    }
  }
  private void completeASearch() throws InterruptedException {
    searching.startsAs("in progress");
    context.checking(new Expectations() {{
      exactly(1).of(consumer).auctionSearchFinished(); then(searching.is("done"));
    }});
    search.search(KEYWORDS);
synchroniser.waitUntil(searching.is("done")); 
  }
  @After
  public void cleanUp() throws InterruptedException {
executor.shutdown();
executor.awaitTermination(1, SECONDS);
  }
}
In the test method onlyOneAuctionSearchFinishedNotificationPerSearch(),
we run a complete search NUMBER_OF_SEARCHES times, to increase the likelihood
of ﬁnding any race conditions. It ﬁnishes each search by asking synchroniser
to wait until it’s collected all the background threads the executor has
launched, or until it’s timed out. Synchroniser provides a method that will
safely wait until a state machine is (or is not) in a given state. The test ignores
auctionSearchFound() notiﬁcations, since here we’re only interested in making
sure that the searches ﬁnish cleanly. Finally, we shut down executor in the test
teardown.
It’s important to watch a stress test fail. It’s too easy to write a test that passes
even though the tested object has a synchronization hole. So, we “test the test”
by making it fail before we’ve synchronized the code, and checking that we get
the failure report we expected. If we don’t, then we might need to raise the
numbers of threads or iterations per thread until we can trust the test to reveal
the error.2 Then we add the synchronization to make the test pass. Here’s our
test failure:
2. Of course, the stress parameters may differ between environments, such as develop-
ment vs. build. We can’t follow that through here, except to note that it needs
addressing.
Chapter 26
Unit Testing and Threads
308


---
**Page 309**

java.lang.AssertionError: unexpected invocation: consumer.auctionSearchFinished()
expectations:
  allowed, already invoked 5 times: consumer.auctionSearchFound(ANYTHING)
  expected once, already invoked 1 time: consumer.auctionSearchFinished(); 
                                                           then searching is done
  expected once, already invoked 1 time: consumer.auctionSearchFinished(); 
                                                           then searching is done
states:
  searching is done
what happened before this:
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseA,[…]
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
  consumer.auctionSearchFinished()
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseA,[…]
  consumer.auctionSearchFinished()
  consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
This says that AuctionSearch has called auctionFinished() once too often.
Fixing the Race Condition (Twice)
We haven’t synchronized access to runningSearchCount. If we use an
AtomicInteger from the Java concurrency libraries instead of a plain int, the
threads should be able to decrement it without interfering with each other.
public class AuctionSearch { […]
private final AtomicInteger runningSearchCount = new AtomicInteger();
  public void search(Set<String> keywords) {
    for (AuctionHouse auctionHouse : auctionHouses) {
      startSearching(auctionHouse, keywords);
    }
  }
  private void startSearching(final AuctionHouse auctionHouse, 
                              final Set<String> keywords) 
  {
runningSearchCount.incrementAndGet();
    executor.execute(new Runnable() {
      public void run() { search(auctionHouse, keywords); }
    });
  }
  private void search(AuctionHouse auctionHouse, Set<String> keywords) {
    consumer.auctionSearchFound(auctionHouse.findAuctions(keywords));
    if (runningSearchCount.decrementAndGet() == 0) {
      consumer.auctionSearchFinished();
    }
  }
}
309
Unit-Testing Synchronization


---
**Page 310**

We try this and, in spite of our use of an AtomicInteger, our test still fails! We
haven’t got our synchronization right after all.
We look again at the failure and see that now the AuctionSearch is
reporting that the search has ﬁnished more than once per search. Previously,
the unsafe concurrent access to runningSearchCount resulted in fewer
auctionSearchFinshed() notiﬁcations than expected, because AuctionSearch
was losing updates to the ﬁeld. Something else must be wrong.
As an eagle-eyed reader, you’ll have noticed a race condition in the way
AuctionSearch increments and decrements runningSearchCount. It increments
the count before starting a task thread. Once the main thread has started creating
task threads, the thread scheduler can preëmpt it and start running whatever task
threads are ready—while the main thread still has search tasks left to create. If
all these started task threads complete before the scheduler resumes the main
thread, they will decrement the count to 0 and the last one will send an
auctionSearchFinshed() notiﬁcation. When the main thread ﬁnally resumes, it
will continue by starting its remaining searches, which will eventually trigger
another notiﬁcation.
This sort of error shows why we need to write stress tests, to make sure that
we see them fail, and to understand the failure messages—it’s also a good moti-
vation for us to write comprehensible failure reports. This example also highlights
the beneﬁts of splitting tests of “raw” functionality from threaded tests. With the
single-threaded version stable, we know we can concentrate on looking for race
conditions in the stress tests.
We ﬁx the code by setting runningSearchCount to the expected number of
searches before starting any threads:
public class AuctionSearch { […]
  public void search(Set<String> keywords) {
runningSearchCount.set(auctionHouses.size());
    for (AuctionHouse auctionHouse : auctionHouses) {
      startSearching(auctionHouse, keywords);
    }
  }
  private void startSearching(final AuctionHouse auctionHouse, 
                              final Set<String> keywords) 
  {
// no longer increments the count here
    executor.execute(new Runnable() {
      public void run() { search(auctionHouse, keywords); }
    });
  }
}
Chapter 26
Unit Testing and Threads
310


---
**Page 311**

Stress-Testing Passive Objects
AuctionSearch actively starts multiple threads by calling out to its executor.
Most objects that are concerned with threading, however, don’t start threads
themselves but have multiple threads “pass through” them and alter their state.
Servlets, for example, are required to support multiple threads touching the same
instance. In such cases, an object must synchronize access to any state that might
cause a race condition.
To stress-test the synchronization of a passive object, the test must start its
own threads to call the object. When all the threads have ﬁnished, the state of
the object should be the same as if those calls had happened in sequence. For
example, AtomicBigCounter below does not synchronize access to its count vari-
able. It works when called from a single thread but can lose updates when called
from multiple threads:
public class AtomicBigCounter {
  private BigInteger count = BigInteger.ZERO;
  public BigInteger count() { return count; }
  public void inc() { count = count.add(BigInteger.ONE); }
}
We can show this failure by calling inc() from multiple threads enough times
to give us a good chance of causing the race condition and losing an update.
When this happens, the ﬁnal result of count() will be less than the number of
times we’ve called inc().
We could spin up multiple threads directly in our test, but the mess of detail
for launching and synchronizing threads would get in the way of understanding
the intent. The threading concerns are a good candidate for extracting into a
subordinate object, MultiThreadedStressTester, which we use to call the counter’s
inc() method:
public class AtomicBigCounterTests { […]
  final AtomicBigCounter counter = new AtomicBigCounter();
  @Test public void
canIncrementCounterFromMultipleThreadsSimultaneously() throws InterruptedException {
    MultithreadedStressTester stressTester = new MultithreadedStressTester(25000);
    stressTester.stress(new Runnable() {
      public void run() {
        counter.inc();
      }
    });
    stressTester.shutdown();
    assertThat("final count", counter.count(), 
               equalTo(BigInteger.valueOf(stressTester.totalActionCount())));
  }
}
311
Stress-Testing Passive Objects


---
**Page 312**

The test fails, showing the race condition in AtomicBigCounter:
java.lang.AssertionError: final count
Expected: <50000>
     got: <36933>
We pass the test by making the inc() and count() methods synchronized.
Synchronizing the Test Thread with Background Threads
When writing a test for code that starts threads, the test cannot conﬁrm the code’s
behavior until it has synchronized its thread with any threads the code has
started. For example, in AuctionSearchStressTests we make the test thread wait
until all the task threads launched by AuctionSearch have been completed. Syn-
chronizing with background threads can be challenging, especially if the tested
object does not delegate to an executor to run concurrent tasks.
The easiest way to ensure that threads have ﬁnished is for the test to sleep long
enough for them all to run to completion. For example:
private void waitForSearchToFinish() throws InterruptedException {
  Thread.sleep(250);
}
This works for occasional use—a sub-second delay in a few tests won’t be
noticeable—but it doesn’t scale. As the number of tests with delays grows, the
total delay adds up and the test suite slows down so much that running it becomes
a distraction. We must be able to run all the unit tests so quickly as to not even
think about whether we should. The other problem with ﬁxed sleeps is that our
choice of delay has to apply across all the environments where the tests run. A
delay suitable for an underpowered machine will slow the tests everywhere else,
and introducing a new environment may force another round of tuning.
An alternative, as we saw in AuctionSearchStressTests, is to use jMock’s
Synchroniser. It provides support for synchronizing between test and background
threads, based on whether a state machine has entered or left a given state:
synchroniser.waitUntil(searching.is("finished"));
synchroniser.waitUntil(searching.isNot("in progress"));
These methods will block forever for a failing test, where the state machine never
meets the speciﬁed criteria, so they should be used with a timeout added to the
test declaration:
@Test(timeout=500)
This tells the test runnner to force a failure if the test overruns the timeout period.
Chapter 26
Unit Testing and Threads
312


---
**Page 313**

A test will run as fast as possible if successful (Synchroniser’s implementation
is based on Java monitors), and only wait the entire 500 ms for failures. So, most
of the time, the synchronization will not slow down the test suite.
If not using jMock, you can write a utility similar to Synchroniser to synchro-
nize between test and background threads. Alternatively, we describe other
synchronization techniques in Chapter 27.
The Limitations of Unit Stress Tests
Having a separate set of tests for our object’s synchronization behavior helps us
pinpoint where to look for defects if tests fail. It is very difﬁcult to diagnose race
conditions with a debugger, as stepping through code (or even adding print
statements) will alter the thread scheduling that’s causing the clash.3 If a change
causes a stress test to fail but the functional unit tests still pass, at least we know
that the object’s functional logic is correct and we’ve introduced a defect into its
synchronization, or vice versa.
Obviously, stress tests offer only a degree of reassurance that code is thread-safe,
not a guarantee. There may be scheduling differences between different operating
systems (or versions of an operating system) and between different processor
combinations. Further, there may be other processes on a host that affect
scheduling while the tests are running. The best we can do is to run the tests
frequently in a range of environments—locally before committing new code, and
on multiple build servers after commit. This should already be part of the devel-
opment process. We can tune the amount of work and number of threads in the
tests until they are reliable enough at detecting errors—where the meaning of
“enough” is an engineering decision for the team.
To cover our backs, we take a “belt and braces” approach.4 We run unit tests
to check that our objects correctly synchronize concurrent threads and to pin-
point synchronization failures. We run end-to-end tests to check that unit-level
synchronization policies integrate across the entire system. If the concurrency
architecture is not imposed on us by the frameworks we are using, we sometimes
use formal modeling tools, such as the LTSA tool described in [Magee06], to
prove that our concurrency model avoids certain classes of errors. Finally, we
run static analysis tools as part of our automated build process to catch further
errors. There are now some excellent practical examples, such as Findbugs,5 that
can detect synchronization errors in everyday Java code.
3. These are known as “Heisenbugs,” because trying to detect the bug alters it.
4. For American readers, this means “belt and suspenders,” but suspenders are a
signiﬁcantly different garment in British English.
5. http://findbugs.sf.net
313
The Limitations of Unit Stress Tests


---
**Page 314**

In this chapter, we’ve considered unit-level testing of concurrent code. Larger-
scale testing of concurrent behavior is much more complex—the tested code
might be running in multiple, distributed processes; the test setup might not be
able to control the creation of threads with an executor; some of the synchroniza-
tion events might not be easily detectable; and, the system might detect and
swallow errors before they can be reported to a test. We address this level of
testing in the next chapter.
Chapter 26
Unit Testing and Threads
314


