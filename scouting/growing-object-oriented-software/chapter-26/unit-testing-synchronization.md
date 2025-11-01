Line1 # Unit-Testing Synchronization (pp.306-311)
Line2 
Line3 ---
Line4 **Page 306**
Line5 
Line6 The application can now easily adapt the object to the application’s threading
Line7 policy without changing its implementation. For example, we could introduce a
Line8 thread pool should we need to limit the number of active threads.
Line9 Unit-Testing Synchronization
Line10 Separating the functional and synchronization concerns has let us test-drive the
Line11 functional behavior of our AuctionSearch in isolation. Now it’s time to test-drive
Line12 the synchronization. We will do this by writing stress-tests that run multiple
Line13 threads through the AuctionSearch implementation to cause synchronization
Line14 errors. Without precise control over the thread scheduler, we can’t guarantee
Line15 that our tests will ﬁnd synchronization errors. The best we can do is run the same
Line16 code enough times on enough threads to give our tests a reasonable likelihood
Line17 of detecting the errors.
Line18 One approach to designing stress tests is to think about the aspects of an ob-
Line19 ject’s observable behavior that are independent of the number of threads calling
Line20 into the object. These are the object’s observable invariants with respect to con-
Line21 currency.1 By focusing on these invariants, we can tune the number of threads
Line22 in a test without having to change its assertions. This gives us a process for
Line23 writing stress tests:
Line24 •
Line25 Specify one of the object’s observable invariants with respect to concurrency;
Line26 •
Line27 Write a stress test for the invariant that exercises the object multiple times
Line28 from multiple threads;
Line29 •
Line30 Watch the test fail, and tune the stress test until it reliably fails on every
Line31 test run; and,
Line32 •
Line33 Make the test pass by adding synchronization.
Line34 We’ll demonstrate this with an example.
Line35 Safety First
Line36 In this chapter we have made the unit tests of functional behavior pass before we
Line37 covered stress testing at the unit level because that allowed us to explain each
Line38 technique on its own. In practice, however, we often write both a unit test for func-
Line39 tionality and a stress test of the synchronization before writing any code, make
Line40 sure they both fail, then make them both pass.This helps us avoid checking in code
Line41 that passes its tests but contains concurrency errors.
Line42 1. This differs from the use of invariants in “design by contract” and formal methods
Line43 of modeling concurrency. These deﬁne invariants over the object’s state.
Line44 Chapter 26
Line45 Unit Testing and Threads
Line46 306
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 307**
Line53 
Line54 A Stress Test for AuctionSearch
Line55 One invariant of our AuctionSearch is that it notiﬁes the consumer just once
Line56 when the search has ﬁnished, no matter how many AuctionHouses it searches—that
Line57 is, no matter how many threads its starts.
Line58 We can use jMock to write a stress test for this invariant. We don’t always use
Line59 jMock for stress tests because expectation failures interfere with the threads of
Line60 the object under test. On the other hand, jMock reports the actual sequence
Line61 of calls to its mock objects when there is a failure, which helps diagnose defects.
Line62 It also provides convenient facilities for synchronizing between the test thread
Line63 and the threads being tested.
Line64 In AuctionSearchStressTests, we set up AuctionSearch with a thread-pool
Line65 executor that will run tasks in background threads, and a list of auction houses
Line66 stubbed to match on the given keywords. jMock is not thread-safe by default,
Line67 so we set up the Mockery with a Synchroniser, an implementation of its threading
Line68 policy that allows us to call mocked objects from different threads. To make
Line69 tuning the test easier, we deﬁne constants at the top for the “degree of stress”
Line70 we’ll apply during the run.
Line71 @RunWith(JMock.class)
Line72 public class AuctionSearchStressTests {
Line73   private static final int NUMBER_OF_AUCTION_HOUSES = 4; 
Line74   private static final int NUMBER_OF_SEARCHES = 8;
Line75   private static final Set<String> KEYWORDS = setOf("sheep", "cheese");
Line76   final Synchroniser synchroniser = new Synchroniser();
Line77   final Mockery context = new JUnit4Mockery() {{
Line78     setThreadingPolicy(synchroniser);
Line79   }};
Line80   final AuctionSearchConsumer consumer = context.mock(AuctionSearchConsumer.class);
Line81   final States searching = context.states("searching");
Line82   final ExecutorService executor = Executors.newCachedThreadPool();
Line83   final AuctionSearch search = new AuctionSearch(executor, auctionHouses(), consumer); 
Line84 […]
Line85   private List<AuctionHouse> auctionHouses() {
Line86     ArrayList<AuctionHouse> auctionHouses = new ArrayList<AuctionHouse>();
Line87     for (int i = 0; i < NUMBER_OF_AUCTION_HOUSES; i++) {
Line88       auctionHouses.add(stubbedAuctionHouse(i));
Line89     }
Line90     return auctionHouses;
Line91   }
Line92   private AuctionHouse stubbedAuctionHouse(final int id) {
Line93     StubAuctionHouse house = new StubAuctionHouse("house" + id);
Line94     house.willReturnSearchResults(
Line95         KEYWORDS, asList(new AuctionDescription(house, "id" + id, "description")));
Line96     return house;
Line97   } 
Line98 307
Line99 Unit-Testing Synchronization
Line100 
Line101 
Line102 ---
Line103 
Line104 ---
Line105 **Page 308**
Line106 
Line107 @Test(timeout=500) public void 
Line108 onlyOneAuctionSearchFinishedNotificationPerSearch() throws Exception {
Line109     context.checking(new Expectations() {{ 
Line110       ignoring (consumer).auctionSearchFound(with(anyResults()));
Line111     }});
Line112     for (int i = 0; i < NUMBER_OF_SEARCHES; i++) { 
Line113       completeASearch();
Line114     }
Line115   }
Line116   private void completeASearch() throws InterruptedException {
Line117     searching.startsAs("in progress");
Line118     context.checking(new Expectations() {{
Line119       exactly(1).of(consumer).auctionSearchFinished(); then(searching.is("done"));
Line120     }});
Line121     search.search(KEYWORDS);
Line122 synchroniser.waitUntil(searching.is("done")); 
Line123   }
Line124   @After
Line125   public void cleanUp() throws InterruptedException {
Line126 executor.shutdown();
Line127 executor.awaitTermination(1, SECONDS);
Line128   }
Line129 }
Line130 In the test method onlyOneAuctionSearchFinishedNotificationPerSearch(),
Line131 we run a complete search NUMBER_OF_SEARCHES times, to increase the likelihood
Line132 of ﬁnding any race conditions. It ﬁnishes each search by asking synchroniser
Line133 to wait until it’s collected all the background threads the executor has
Line134 launched, or until it’s timed out. Synchroniser provides a method that will
Line135 safely wait until a state machine is (or is not) in a given state. The test ignores
Line136 auctionSearchFound() notiﬁcations, since here we’re only interested in making
Line137 sure that the searches ﬁnish cleanly. Finally, we shut down executor in the test
Line138 teardown.
Line139 It’s important to watch a stress test fail. It’s too easy to write a test that passes
Line140 even though the tested object has a synchronization hole. So, we “test the test”
Line141 by making it fail before we’ve synchronized the code, and checking that we get
Line142 the failure report we expected. If we don’t, then we might need to raise the
Line143 numbers of threads or iterations per thread until we can trust the test to reveal
Line144 the error.2 Then we add the synchronization to make the test pass. Here’s our
Line145 test failure:
Line146 2. Of course, the stress parameters may differ between environments, such as develop-
Line147 ment vs. build. We can’t follow that through here, except to note that it needs
Line148 addressing.
Line149 Chapter 26
Line150 Unit Testing and Threads
Line151 308
Line152 
Line153 
Line154 ---
Line155 
Line156 ---
Line157 **Page 309**
Line158 
Line159 java.lang.AssertionError: unexpected invocation: consumer.auctionSearchFinished()
Line160 expectations:
Line161   allowed, already invoked 5 times: consumer.auctionSearchFound(ANYTHING)
Line162   expected once, already invoked 1 time: consumer.auctionSearchFinished(); 
Line163                                                            then searching is done
Line164   expected once, already invoked 1 time: consumer.auctionSearchFinished(); 
Line165                                                            then searching is done
Line166 states:
Line167   searching is done
Line168 what happened before this:
Line169   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseA,[…]
Line170   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
Line171   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
Line172   consumer.auctionSearchFinished()
Line173   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseA,[…]
Line174   consumer.auctionSearchFinished()
Line175   consumer.auctionSearchFound(<[AuctionDescription[auctionHouse=houseB,[…]
Line176 This says that AuctionSearch has called auctionFinished() once too often.
Line177 Fixing the Race Condition (Twice)
Line178 We haven’t synchronized access to runningSearchCount. If we use an
Line179 AtomicInteger from the Java concurrency libraries instead of a plain int, the
Line180 threads should be able to decrement it without interfering with each other.
Line181 public class AuctionSearch { […]
Line182 private final AtomicInteger runningSearchCount = new AtomicInteger();
Line183   public void search(Set<String> keywords) {
Line184     for (AuctionHouse auctionHouse : auctionHouses) {
Line185       startSearching(auctionHouse, keywords);
Line186     }
Line187   }
Line188   private void startSearching(final AuctionHouse auctionHouse, 
Line189                               final Set<String> keywords) 
Line190   {
Line191 runningSearchCount.incrementAndGet();
Line192     executor.execute(new Runnable() {
Line193       public void run() { search(auctionHouse, keywords); }
Line194     });
Line195   }
Line196   private void search(AuctionHouse auctionHouse, Set<String> keywords) {
Line197     consumer.auctionSearchFound(auctionHouse.findAuctions(keywords));
Line198     if (runningSearchCount.decrementAndGet() == 0) {
Line199       consumer.auctionSearchFinished();
Line200     }
Line201   }
Line202 }
Line203 309
Line204 Unit-Testing Synchronization
Line205 
Line206 
Line207 ---
Line208 
Line209 ---
Line210 **Page 310**
Line211 
Line212 We try this and, in spite of our use of an AtomicInteger, our test still fails! We
Line213 haven’t got our synchronization right after all.
Line214 We look again at the failure and see that now the AuctionSearch is
Line215 reporting that the search has ﬁnished more than once per search. Previously,
Line216 the unsafe concurrent access to runningSearchCount resulted in fewer
Line217 auctionSearchFinshed() notiﬁcations than expected, because AuctionSearch
Line218 was losing updates to the ﬁeld. Something else must be wrong.
Line219 As an eagle-eyed reader, you’ll have noticed a race condition in the way
Line220 AuctionSearch increments and decrements runningSearchCount. It increments
Line221 the count before starting a task thread. Once the main thread has started creating
Line222 task threads, the thread scheduler can preëmpt it and start running whatever task
Line223 threads are ready—while the main thread still has search tasks left to create. If
Line224 all these started task threads complete before the scheduler resumes the main
Line225 thread, they will decrement the count to 0 and the last one will send an
Line226 auctionSearchFinshed() notiﬁcation. When the main thread ﬁnally resumes, it
Line227 will continue by starting its remaining searches, which will eventually trigger
Line228 another notiﬁcation.
Line229 This sort of error shows why we need to write stress tests, to make sure that
Line230 we see them fail, and to understand the failure messages—it’s also a good moti-
Line231 vation for us to write comprehensible failure reports. This example also highlights
Line232 the beneﬁts of splitting tests of “raw” functionality from threaded tests. With the
Line233 single-threaded version stable, we know we can concentrate on looking for race
Line234 conditions in the stress tests.
Line235 We ﬁx the code by setting runningSearchCount to the expected number of
Line236 searches before starting any threads:
Line237 public class AuctionSearch { […]
Line238   public void search(Set<String> keywords) {
Line239 runningSearchCount.set(auctionHouses.size());
Line240     for (AuctionHouse auctionHouse : auctionHouses) {
Line241       startSearching(auctionHouse, keywords);
Line242     }
Line243   }
Line244   private void startSearching(final AuctionHouse auctionHouse, 
Line245                               final Set<String> keywords) 
Line246   {
Line247 // no longer increments the count here
Line248     executor.execute(new Runnable() {
Line249       public void run() { search(auctionHouse, keywords); }
Line250     });
Line251   }
Line252 }
Line253 Chapter 26
Line254 Unit Testing and Threads
Line255 310
Line256 
Line257 
Line258 ---
Line259 
Line260 ---
Line261 **Page 311**
Line262 
Line263 Stress-Testing Passive Objects
Line264 AuctionSearch actively starts multiple threads by calling out to its executor.
Line265 Most objects that are concerned with threading, however, don’t start threads
Line266 themselves but have multiple threads “pass through” them and alter their state.
Line267 Servlets, for example, are required to support multiple threads touching the same
Line268 instance. In such cases, an object must synchronize access to any state that might
Line269 cause a race condition.
Line270 To stress-test the synchronization of a passive object, the test must start its
Line271 own threads to call the object. When all the threads have ﬁnished, the state of
Line272 the object should be the same as if those calls had happened in sequence. For
Line273 example, AtomicBigCounter below does not synchronize access to its count vari-
Line274 able. It works when called from a single thread but can lose updates when called
Line275 from multiple threads:
Line276 public class AtomicBigCounter {
Line277   private BigInteger count = BigInteger.ZERO;
Line278   public BigInteger count() { return count; }
Line279   public void inc() { count = count.add(BigInteger.ONE); }
Line280 }
Line281 We can show this failure by calling inc() from multiple threads enough times
Line282 to give us a good chance of causing the race condition and losing an update.
Line283 When this happens, the ﬁnal result of count() will be less than the number of
Line284 times we’ve called inc().
Line285 We could spin up multiple threads directly in our test, but the mess of detail
Line286 for launching and synchronizing threads would get in the way of understanding
Line287 the intent. The threading concerns are a good candidate for extracting into a
Line288 subordinate object, MultiThreadedStressTester, which we use to call the counter’s
Line289 inc() method:
Line290 public class AtomicBigCounterTests { […]
Line291   final AtomicBigCounter counter = new AtomicBigCounter();
Line292   @Test public void
Line293 canIncrementCounterFromMultipleThreadsSimultaneously() throws InterruptedException {
Line294     MultithreadedStressTester stressTester = new MultithreadedStressTester(25000);
Line295     stressTester.stress(new Runnable() {
Line296       public void run() {
Line297         counter.inc();
Line298       }
Line299     });
Line300     stressTester.shutdown();
Line301     assertThat("final count", counter.count(), 
Line302                equalTo(BigInteger.valueOf(stressTester.totalActionCount())));
Line303   }
Line304 }
Line305 311
Line306 Stress-Testing Passive Objects
Line307 
Line308 
Line309 ---
