Line1 # The Limitations of Unit Stress Tests (pp.313-314)
Line2 
Line3 ---
Line4 **Page 313**
Line5 
Line6 A test will run as fast as possible if successful (Synchroniser’s implementation
Line7 is based on Java monitors), and only wait the entire 500 ms for failures. So, most
Line8 of the time, the synchronization will not slow down the test suite.
Line9 If not using jMock, you can write a utility similar to Synchroniser to synchro-
Line10 nize between test and background threads. Alternatively, we describe other
Line11 synchronization techniques in Chapter 27.
Line12 The Limitations of Unit Stress Tests
Line13 Having a separate set of tests for our object’s synchronization behavior helps us
Line14 pinpoint where to look for defects if tests fail. It is very difﬁcult to diagnose race
Line15 conditions with a debugger, as stepping through code (or even adding print
Line16 statements) will alter the thread scheduling that’s causing the clash.3 If a change
Line17 causes a stress test to fail but the functional unit tests still pass, at least we know
Line18 that the object’s functional logic is correct and we’ve introduced a defect into its
Line19 synchronization, or vice versa.
Line20 Obviously, stress tests offer only a degree of reassurance that code is thread-safe,
Line21 not a guarantee. There may be scheduling differences between different operating
Line22 systems (or versions of an operating system) and between different processor
Line23 combinations. Further, there may be other processes on a host that affect
Line24 scheduling while the tests are running. The best we can do is to run the tests
Line25 frequently in a range of environments—locally before committing new code, and
Line26 on multiple build servers after commit. This should already be part of the devel-
Line27 opment process. We can tune the amount of work and number of threads in the
Line28 tests until they are reliable enough at detecting errors—where the meaning of
Line29 “enough” is an engineering decision for the team.
Line30 To cover our backs, we take a “belt and braces” approach.4 We run unit tests
Line31 to check that our objects correctly synchronize concurrent threads and to pin-
Line32 point synchronization failures. We run end-to-end tests to check that unit-level
Line33 synchronization policies integrate across the entire system. If the concurrency
Line34 architecture is not imposed on us by the frameworks we are using, we sometimes
Line35 use formal modeling tools, such as the LTSA tool described in [Magee06], to
Line36 prove that our concurrency model avoids certain classes of errors. Finally, we
Line37 run static analysis tools as part of our automated build process to catch further
Line38 errors. There are now some excellent practical examples, such as Findbugs,5 that
Line39 can detect synchronization errors in everyday Java code.
Line40 3. These are known as “Heisenbugs,” because trying to detect the bug alters it.
Line41 4. For American readers, this means “belt and suspenders,” but suspenders are a
Line42 signiﬁcantly different garment in British English.
Line43 5. http://findbugs.sf.net
Line44 313
Line45 The Limitations of Unit Stress Tests
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 314**
Line52 
Line53 In this chapter, we’ve considered unit-level testing of concurrent code. Larger-
Line54 scale testing of concurrent behavior is much more complex—the tested code
Line55 might be running in multiple, distributed processes; the test setup might not be
Line56 able to control the creation of threads with an executor; some of the synchroniza-
Line57 tion events might not be easily detectable; and, the system might detect and
Line58 swallow errors before they can be reported to a test. We address this level of
Line59 testing in the next chapter.
Line60 Chapter 26
Line61 Unit Testing and Threads
Line62 314
