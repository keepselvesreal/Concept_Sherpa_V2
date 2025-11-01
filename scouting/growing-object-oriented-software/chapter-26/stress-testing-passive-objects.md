Line1 # Stress-Testing Passive Objects (pp.311-312)
Line2 
Line3 ---
Line4 **Page 311**
Line5 
Line6 Stress-Testing Passive Objects
Line7 AuctionSearch actively starts multiple threads by calling out to its executor.
Line8 Most objects that are concerned with threading, however, don’t start threads
Line9 themselves but have multiple threads “pass through” them and alter their state.
Line10 Servlets, for example, are required to support multiple threads touching the same
Line11 instance. In such cases, an object must synchronize access to any state that might
Line12 cause a race condition.
Line13 To stress-test the synchronization of a passive object, the test must start its
Line14 own threads to call the object. When all the threads have ﬁnished, the state of
Line15 the object should be the same as if those calls had happened in sequence. For
Line16 example, AtomicBigCounter below does not synchronize access to its count vari-
Line17 able. It works when called from a single thread but can lose updates when called
Line18 from multiple threads:
Line19 public class AtomicBigCounter {
Line20   private BigInteger count = BigInteger.ZERO;
Line21   public BigInteger count() { return count; }
Line22   public void inc() { count = count.add(BigInteger.ONE); }
Line23 }
Line24 We can show this failure by calling inc() from multiple threads enough times
Line25 to give us a good chance of causing the race condition and losing an update.
Line26 When this happens, the ﬁnal result of count() will be less than the number of
Line27 times we’ve called inc().
Line28 We could spin up multiple threads directly in our test, but the mess of detail
Line29 for launching and synchronizing threads would get in the way of understanding
Line30 the intent. The threading concerns are a good candidate for extracting into a
Line31 subordinate object, MultiThreadedStressTester, which we use to call the counter’s
Line32 inc() method:
Line33 public class AtomicBigCounterTests { […]
Line34   final AtomicBigCounter counter = new AtomicBigCounter();
Line35   @Test public void
Line36 canIncrementCounterFromMultipleThreadsSimultaneously() throws InterruptedException {
Line37     MultithreadedStressTester stressTester = new MultithreadedStressTester(25000);
Line38     stressTester.stress(new Runnable() {
Line39       public void run() {
Line40         counter.inc();
Line41       }
Line42     });
Line43     stressTester.shutdown();
Line44     assertThat("final count", counter.count(), 
Line45                equalTo(BigInteger.valueOf(stressTester.totalActionCount())));
Line46   }
Line47 }
Line48 311
Line49 Stress-Testing Passive Objects
Line50 
Line51 
Line52 ---
Line53 
Line54 ---
Line55 **Page 312**
Line56 
Line57 The test fails, showing the race condition in AtomicBigCounter:
Line58 java.lang.AssertionError: final count
Line59 Expected: <50000>
Line60      got: <36933>
Line61 We pass the test by making the inc() and count() methods synchronized.
Line62 Synchronizing the Test Thread with Background Threads
Line63 When writing a test for code that starts threads, the test cannot conﬁrm the code’s
Line64 behavior until it has synchronized its thread with any threads the code has
Line65 started. For example, in AuctionSearchStressTests we make the test thread wait
Line66 until all the task threads launched by AuctionSearch have been completed. Syn-
Line67 chronizing with background threads can be challenging, especially if the tested
Line68 object does not delegate to an executor to run concurrent tasks.
Line69 The easiest way to ensure that threads have ﬁnished is for the test to sleep long
Line70 enough for them all to run to completion. For example:
Line71 private void waitForSearchToFinish() throws InterruptedException {
Line72   Thread.sleep(250);
Line73 }
Line74 This works for occasional use—a sub-second delay in a few tests won’t be
Line75 noticeable—but it doesn’t scale. As the number of tests with delays grows, the
Line76 total delay adds up and the test suite slows down so much that running it becomes
Line77 a distraction. We must be able to run all the unit tests so quickly as to not even
Line78 think about whether we should. The other problem with ﬁxed sleeps is that our
Line79 choice of delay has to apply across all the environments where the tests run. A
Line80 delay suitable for an underpowered machine will slow the tests everywhere else,
Line81 and introducing a new environment may force another round of tuning.
Line82 An alternative, as we saw in AuctionSearchStressTests, is to use jMock’s
Line83 Synchroniser. It provides support for synchronizing between test and background
Line84 threads, based on whether a state machine has entered or left a given state:
Line85 synchroniser.waitUntil(searching.is("finished"));
Line86 synchroniser.waitUntil(searching.isNot("in progress"));
Line87 These methods will block forever for a failing test, where the state machine never
Line88 meets the speciﬁed criteria, so they should be used with a timeout added to the
Line89 test declaration:
Line90 @Test(timeout=500)
Line91 This tells the test runnner to force a failure if the test overruns the timeout period.
Line92 Chapter 26
Line93 Unit Testing and Threads
Line94 312
Line95 
Line96 
Line97 ---
