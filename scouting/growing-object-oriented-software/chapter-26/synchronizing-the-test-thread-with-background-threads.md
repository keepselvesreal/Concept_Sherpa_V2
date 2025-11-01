Line1 # Synchronizing the Test Thread with Background Threads (pp.312-313)
Line2 
Line3 ---
Line4 **Page 312**
Line5 
Line6 The test fails, showing the race condition in AtomicBigCounter:
Line7 java.lang.AssertionError: final count
Line8 Expected: <50000>
Line9      got: <36933>
Line10 We pass the test by making the inc() and count() methods synchronized.
Line11 Synchronizing the Test Thread with Background Threads
Line12 When writing a test for code that starts threads, the test cannot conﬁrm the code’s
Line13 behavior until it has synchronized its thread with any threads the code has
Line14 started. For example, in AuctionSearchStressTests we make the test thread wait
Line15 until all the task threads launched by AuctionSearch have been completed. Syn-
Line16 chronizing with background threads can be challenging, especially if the tested
Line17 object does not delegate to an executor to run concurrent tasks.
Line18 The easiest way to ensure that threads have ﬁnished is for the test to sleep long
Line19 enough for them all to run to completion. For example:
Line20 private void waitForSearchToFinish() throws InterruptedException {
Line21   Thread.sleep(250);
Line22 }
Line23 This works for occasional use—a sub-second delay in a few tests won’t be
Line24 noticeable—but it doesn’t scale. As the number of tests with delays grows, the
Line25 total delay adds up and the test suite slows down so much that running it becomes
Line26 a distraction. We must be able to run all the unit tests so quickly as to not even
Line27 think about whether we should. The other problem with ﬁxed sleeps is that our
Line28 choice of delay has to apply across all the environments where the tests run. A
Line29 delay suitable for an underpowered machine will slow the tests everywhere else,
Line30 and introducing a new environment may force another round of tuning.
Line31 An alternative, as we saw in AuctionSearchStressTests, is to use jMock’s
Line32 Synchroniser. It provides support for synchronizing between test and background
Line33 threads, based on whether a state machine has entered or left a given state:
Line34 synchroniser.waitUntil(searching.is("finished"));
Line35 synchroniser.waitUntil(searching.isNot("in progress"));
Line36 These methods will block forever for a failing test, where the state machine never
Line37 meets the speciﬁed criteria, so they should be used with a timeout added to the
Line38 test declaration:
Line39 @Test(timeout=500)
Line40 This tells the test runnner to force a failure if the test overruns the timeout period.
Line41 Chapter 26
Line42 Unit Testing and Threads
Line43 312
Line44 
Line45 
Line46 ---
Line47 
Line48 ---
Line49 **Page 313**
Line50 
Line51 A test will run as fast as possible if successful (Synchroniser’s implementation
Line52 is based on Java monitors), and only wait the entire 500 ms for failures. So, most
Line53 of the time, the synchronization will not slow down the test suite.
Line54 If not using jMock, you can write a utility similar to Synchroniser to synchro-
Line55 nize between test and background threads. Alternatively, we describe other
Line56 synchronization techniques in Chapter 27.
Line57 The Limitations of Unit Stress Tests
Line58 Having a separate set of tests for our object’s synchronization behavior helps us
Line59 pinpoint where to look for defects if tests fail. It is very difﬁcult to diagnose race
Line60 conditions with a debugger, as stepping through code (or even adding print
Line61 statements) will alter the thread scheduling that’s causing the clash.3 If a change
Line62 causes a stress test to fail but the functional unit tests still pass, at least we know
Line63 that the object’s functional logic is correct and we’ve introduced a defect into its
Line64 synchronization, or vice versa.
Line65 Obviously, stress tests offer only a degree of reassurance that code is thread-safe,
Line66 not a guarantee. There may be scheduling differences between different operating
Line67 systems (or versions of an operating system) and between different processor
Line68 combinations. Further, there may be other processes on a host that affect
Line69 scheduling while the tests are running. The best we can do is to run the tests
Line70 frequently in a range of environments—locally before committing new code, and
Line71 on multiple build servers after commit. This should already be part of the devel-
Line72 opment process. We can tune the amount of work and number of threads in the
Line73 tests until they are reliable enough at detecting errors—where the meaning of
Line74 “enough” is an engineering decision for the team.
Line75 To cover our backs, we take a “belt and braces” approach.4 We run unit tests
Line76 to check that our objects correctly synchronize concurrent threads and to pin-
Line77 point synchronization failures. We run end-to-end tests to check that unit-level
Line78 synchronization policies integrate across the entire system. If the concurrency
Line79 architecture is not imposed on us by the frameworks we are using, we sometimes
Line80 use formal modeling tools, such as the LTSA tool described in [Magee06], to
Line81 prove that our concurrency model avoids certain classes of errors. Finally, we
Line82 run static analysis tools as part of our automated build process to catch further
Line83 errors. There are now some excellent practical examples, such as Findbugs,5 that
Line84 can detect synchronization errors in everyday Java code.
Line85 3. These are known as “Heisenbugs,” because trying to detect the bug alters it.
Line86 4. For American readers, this means “belt and suspenders,” but suspenders are a
Line87 signiﬁcantly different garment in British English.
Line88 5. http://findbugs.sf.net
Line89 313
Line90 The Limitations of Unit Stress Tests
Line91 
Line92 
Line93 ---
