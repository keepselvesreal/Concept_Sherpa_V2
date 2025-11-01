Line1 # Separating Functionality and Concurrency Policy (pp.302-306)
Line2 
Line3 ---
Line4 **Page 302**
Line5 
Line6 but the application must synchronize the Smack thread and the Swing thread
Line7 to avoid the GUI components being corrupted.
Line8 When you must design a system’s concurrency architecture from scratch, you
Line9 can use modeling tools to prove your design free of certain classes of synchroniza-
Line10 tion errors, such as deadlock, livelock, or starvation. Design tools that help you
Line11 model concurrency are becoming increasingly easy to use. The book Concurrency:
Line12 State Models & Java Programs [Magee06] is an introduction to concurrent pro-
Line13 gramming that stresses a combination of formal modeling and implementation
Line14 and describes how to do the formal modeling with the LTSA analysis tool.
Line15 Even with a proven design, however, we have to cross the chasm between design
Line16 and implementation. We need to ensure that our components conform to the
Line17 architectural constraints of the system. Testing can help at this point. Once we’ve
Line18 designed how the system will manage concurrency, we can test-drive the objects
Line19 that will ﬁt into that architecture. Unit tests give us conﬁdence that an object
Line20 performs its synchronization responsibilities, such as locking its state or blocking
Line21 and waking threads. Coarser-grained tests, such as system tests, give us conﬁdence
Line22 that the entire system manages concurrency correctly.
Line23 Separating Functionality and Concurrency Policy
Line24 Objects that cope with multiple threads mix functional concerns with synchro-
Line25 nization concerns, either of which can be the cause of test failures. Tests must
Line26 also synchronize with the background threads, so that they don’t make assertions
Line27 before the threads have ﬁnished working or leave threads running that might
Line28 interfere with later tests. Worse, in the presence of threads, unit tests do not
Line29 usually report failures well. Exceptions get thrown on the hidden threads, killing
Line30 them unexpectedly and breaking the behavior of the tested object. If a test times
Line31 out waiting for background threads to ﬁnish, there’s often no diagnostic other
Line32 than a basic timeout message. All this makes unit testing difﬁcult.
Line33 Searching for Auctions Concurrently
Line34 Let’s look at an example. We will extend our Auction Sniper application to let
Line35 the user search for auctions of interest. When the user enters search
Line36 keywords, the application will run the search concurrently on all auction houses
Line37 that the application can connect to. Each AuctionHouse will return a list of
Line38 AuctionDescriptions that contain information about its auctions matching the
Line39 search keywords. The application will combine the results it receives from all
Line40 AuctionHouses and display a single list of auctions to the user. The user can then
Line41 decide which of them to bid for.
Line42 The concurrent search is performed by an AuctionSearch object which passes
Line43 the search keywords to each AuctionHouse and announces the results they return
Line44 Chapter 26
Line45 Unit Testing and Threads
Line46 302
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 303**
Line53 
Line54 to an AuctionSearchConsumer. Our tests for the Auction Search are complicated
Line55 because an AuctionSearch will spawn multiple threads per search, one for each
Line56 AuctionHouse. If it hides those threads behind its API, we will have to implement
Line57 the searching and notiﬁcation functionality and the synchronization at the same
Line58 time. When a test fails, we will have to work out which of those concerns is at
Line59 fault. That’s why we prefer our usual practice of incrementally adding
Line60 functionality test by test.
Line61 It would be easier to test and implement the AuctionSearch if we could tackle
Line62 the functional behavior and the synchronization separately. This would allow
Line63 us to test the functional behavior within the test thread. We want to separate the
Line64 logic that splits a request into multiple tasks from the technical details of how
Line65 those tasks are executed concurrently. So we pass a “task runner” in to the
Line66 AuctionSearch, which can then delegate managing tasks to the runner instead of
Line67 starting threads itself. In our unit tests we’ll give the AuctionSearch a fake task
Line68 runner that calls tasks directly. In the real system, we’ll give it a task runner that
Line69 creates threads for tasks.
Line70 Introducing an Executor
Line71 We need an interface between the AuctionHouse and the task runner. We can use
Line72 this one from Java’s standard java.util.concurrent package:
Line73 public interface Executor {
Line74   void execute(Runnable command);
Line75 }
Line76 How should we implement Executor in our unit tests? For testing, we need to
Line77 run the tasks in the same thread as the test runner instead of creating new task
Line78 threads. We could use jMock to mock Executor and write a custom action to
Line79 capture all calls so we can run them later, but that sounds too complicated. The
Line80 easiest option is to write a class to implement Executor. We can us it to explicitly
Line81 run the tasks on the test thread after the call to the tested object has returned.
Line82 jMock includes such a class, called DeterministicExecutor. We use this
Line83 executor to write our ﬁrst unit test. It checks that AuctionSearch notiﬁes its
Line84 AuctionSearchConsumer whenever an AuctionHouse returns search results and
Line85 when the entire search has ﬁnished.
Line86 In the test setup, we mock the consumer because we want to show how
Line87 it’s notiﬁed by AuctionSearch. We represent auction houses with a simple
Line88 StubAuctionHouse that just returns a list of descriptions if it matches keywords,
Line89 or an empty list if not (real ones would communicate to auction services over
Line90 the Internet). We wrote a custom stub, instead of using a jMock allowance, to
Line91 reduce the “noise” in the failure reports; you’ll see how this matters when
Line92 we start stress-testing in the next section. We also pass an instance of
Line93 DeterministicExecutor to AuctionSearch so that we can run the tasks within
Line94 the test thread.
Line95 303
Line96 Separating Functionality and Concurrency Policy
Line97 
Line98 
Line99 ---
Line100 
Line101 ---
Line102 **Page 304**
Line103 
Line104 @RunWith(JMock.class)
Line105 public class AuctionSearchTests {
Line106   Mockery context = new JUnit4Mockery();
Line107   final DeterministicExecutor executor = new DeterministicExecutor();
Line108   final StubAuctionHouse houseA = new StubAuctionHouse("houseA");
Line109   final StubAuctionHouse houseB = new StubAuctionHouse("houseB");
Line110   List<AuctionDescription> resultsFromA = asList(auction(houseA, "1"));
Line111   List<AuctionDescription> resultsFromB = asList(auction(houseB, "2"));;
Line112   final AuctionSearchConsumer consumer = context.mock(AuctionSearchConsumer.class);
Line113   final AuctionSearch search = 
Line114                         new AuctionSearch(executor, houses(houseA, houseB), consumer);
Line115   @Test public void 
Line116 searchesAllAuctionHouses() throws Exception {
Line117     final Set<String> keywords = set("sheep", "cheese");
Line118     houseA.willReturnSearchResults(keywords, resultsFromA);
Line119     houseB.willReturnSearchResults(keywords, resultsFromB);
Line120     context.checking(new Expectations() {{
Line121       final States searching = context.states("searching");
Line122       oneOf(consumer).auctionSearchFound(resultsFromA); when(searching.isNot("done"));
Line123       oneOf(consumer).auctionSearchFound(resultsFromB); when(searching.isNot("done"));
Line124       oneOf(consumer).auctionSearchFinished();          then(searching.is("done"));
Line125     }});
Line126     search.search(keywords);
Line127 executor.runUntilIdle();
Line128   }
Line129 }
Line130 In the test, we conﬁgure the StubAuctionHouses to return example results when
Line131 they’re queried with the given keywords. We specify our expectations that the
Line132 consumer will be notiﬁed of the two search results (in any order), and then that
Line133 the search has ﬁnished.
Line134 When we call search.search(keywords), the AuctionSearch hands a task for
Line135 each of its auction houses to the executor. By the time search() returns, the tasks
Line136 to run are queued in the executor. Finally, we call executor.runUntilIdle() to
Line137 tell the executor to run queued tasks until its queue is empty. The tasks run on
Line138 the test thread, so any assertion failures will be caught and reported by JUnit,
Line139 and we don’t have to worry about synchronizing the test thread with background
Line140 threads.
Line141 Implementing AuctionSearch
Line142 This implementation of AuctionSearch calls its executor to start a search for
Line143 each of its auction houses. It tracks how many searches are unﬁnished in its
Line144 runningSearchCount ﬁeld, so that it can notify the consumer when it’s ﬁnished.
Line145 Chapter 26
Line146 Unit Testing and Threads
Line147 304
Line148 
Line149 
Line150 ---
Line151 
Line152 ---
Line153 **Page 305**
Line154 
Line155 public class AuctionSearch {
Line156   private final Executor executor;
Line157   private final List<AuctionHouse> auctionHouses;
Line158   private final AuctionSearchConsumer consumer;
Line159 private int runningSearchCount = 0;
Line160   public AuctionSearch(Executor executor, 
Line161                        List<AuctionHouse> auctionHouses, 
Line162                        AuctionSearchConsumer consumer) 
Line163   {
Line164     this.executor = executor;
Line165     this.auctionHouses = auctionHouses;
Line166     this.consumer = consumer;
Line167   }
Line168   public void search(Set<String> keywords) {
Line169     for (AuctionHouse auctionHouse : auctionHouses) {
Line170       startSearching(auctionHouse, keywords);
Line171     }
Line172   }
Line173   private void startSearching(final AuctionHouse auctionHouse, 
Line174                               final Set<String> keywords) 
Line175   {
Line176 runningSearchCount++;
Line177     executor.execute(new Runnable() {
Line178       public void run() {
Line179         search(auctionHouse, keywords);
Line180       }
Line181     });
Line182   }
Line183   private void search(AuctionHouse auctionHouse, Set<String> keywords) {
Line184     consumer.auctionSearchFound(auctionHouse.findAuctions(keywords));
Line185 runningSearchCount--;
Line186     if (runningSearchCount == 0) {
Line187       consumer.auctionSearchFinished();
Line188     }
Line189   }
Line190 }
Line191 Unfortunately, this version is unsafe because it doesn’t synchronize access to
Line192 runningSearchCount. Different threads may overwrite each other when they
Line193 decrement the ﬁeld. So far, we’ve clariﬁed the core behavior. We’ll drive out this
Line194 synchronization issue in the next test. Pulling out the Executor has given us two
Line195 advantages. First, it makes development easier as we can unit-test the basic
Line196 functionality without getting confused by threading issues. Second, the object’s
Line197 API no longer hides its concurrency policy.
Line198 Concurrency is a system-wide concern that should be controlled outside the
Line199 objects that need to run concurrent tasks. By passing an appropriate Executor
Line200 to the constructor, we’re following the “context independence” design principle.
Line201 305
Line202 Separating Functionality and Concurrency Policy
Line203 
Line204 
Line205 ---
Line206 
Line207 ---
Line208 **Page 306**
Line209 
Line210 The application can now easily adapt the object to the application’s threading
Line211 policy without changing its implementation. For example, we could introduce a
Line212 thread pool should we need to limit the number of active threads.
Line213 Unit-Testing Synchronization
Line214 Separating the functional and synchronization concerns has let us test-drive the
Line215 functional behavior of our AuctionSearch in isolation. Now it’s time to test-drive
Line216 the synchronization. We will do this by writing stress-tests that run multiple
Line217 threads through the AuctionSearch implementation to cause synchronization
Line218 errors. Without precise control over the thread scheduler, we can’t guarantee
Line219 that our tests will ﬁnd synchronization errors. The best we can do is run the same
Line220 code enough times on enough threads to give our tests a reasonable likelihood
Line221 of detecting the errors.
Line222 One approach to designing stress tests is to think about the aspects of an ob-
Line223 ject’s observable behavior that are independent of the number of threads calling
Line224 into the object. These are the object’s observable invariants with respect to con-
Line225 currency.1 By focusing on these invariants, we can tune the number of threads
Line226 in a test without having to change its assertions. This gives us a process for
Line227 writing stress tests:
Line228 •
Line229 Specify one of the object’s observable invariants with respect to concurrency;
Line230 •
Line231 Write a stress test for the invariant that exercises the object multiple times
Line232 from multiple threads;
Line233 •
Line234 Watch the test fail, and tune the stress test until it reliably fails on every
Line235 test run; and,
Line236 •
Line237 Make the test pass by adding synchronization.
Line238 We’ll demonstrate this with an example.
Line239 Safety First
Line240 In this chapter we have made the unit tests of functional behavior pass before we
Line241 covered stress testing at the unit level because that allowed us to explain each
Line242 technique on its own. In practice, however, we often write both a unit test for func-
Line243 tionality and a stress test of the synchronization before writing any code, make
Line244 sure they both fail, then make them both pass.This helps us avoid checking in code
Line245 that passes its tests but contains concurrency errors.
Line246 1. This differs from the use of invariants in “design by contract” and formal methods
Line247 of modeling concurrency. These deﬁne invariants over the object’s state.
Line248 Chapter 26
Line249 Unit Testing and Threads
Line250 306
Line251 
Line252 
Line253 ---
