Line1 # Sampling or Listening (pp.316-318)
Line2 
Line3 ---
Line4 **Page 316**
Line5 
Line6 when the test makes its assertion. The value of the stock holding that the assertion
Line7 checks will depend on timings: how long the messages take to reach the server,
Line8 how long the server takes to update its database, and how long the test takes to
Line9 run. The test might ﬁre the assertion after both messages have been processed
Line10 (passing correctly), after one message (failing incorrectly), or before either
Line11 message (passing, but testing nothing at all).
Line12 As you can see from this small example, with an asynchronous test we have
Line13 to be careful about its coordination with the system it’s testing. Otherwise, it can
Line14 become unreliable, failing intermittently when the system is working or, worse,
Line15 passing when the system is broken.
Line16 Current testing frameworks provide little support for dealing with asynchrony.
Line17 They mostly assume that the tests run in a single thread of control, leaving the
Line18 programmer to build the scaffolding needed to test concurrent behavior. In this
Line19 chapter we describe some practices for writing reliable, responsive tests for
Line20 asynchronous code.
Line21 Sampling or Listening
Line22 The fundamental difﬁculty with testing asynchronous code is that a test triggers
Line23 activity that runs concurrently with the test and therefore cannot immediately
Line24 check the outcome of the activity. The test will not block until the activity has
Line25 ﬁnished. If the activity fails, it will not throw an exception back into the test, so
Line26 the test cannot recognize if the activity is still running or has failed. The test
Line27 therefore has to wait for the activity to complete successfully and fail if this
Line28 doesn’t happen within a given timeout period.
Line29 Wait for Success
Line30 An asynchronous test must wait for success and use timeouts to detect failure.
Line31 This implies that every tested activity must have an observable effect: a test
Line32 must affect the system so that its observable state becomes different. This sounds
Line33 obvious but it drives how we think about writing asynchronous tests. If an activ-
Line34 ity has no observable effect, there is nothing the test can wait for, and therefore
Line35 no way for the test to synchronize with the system it is testing.
Line36 There are two ways a test can observe the system: by sampling its observable
Line37 state or by listening for events that it sends out. Of these, sampling is often the
Line38 only option because many systems don’t send any monitoring events. It’s quite
Line39 common for a test to include both techniques to interact with different “ends”
Line40 of its system. For example, the Auction Sniper end-to-end tests sample the user
Line41 interface for display changes, through the WindowLicker framework, but listen
Line42 for chat events in the fake auction server.
Line43 Chapter 27
Line44 Testing Asynchronous Code
Line45 316
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 317**
Line52 
Line53 Beware of Flickering Tests
Line54 A test can fail intermittently if its timeout is too close to the time the tested behavior
Line55 normally takes to run, or if it doesn’t synchronize correctly with the system. On a
Line56 small system, an occasional ﬂickering test might not cause problems—the test will
Line57 most likely pass during the next build—but it’s risky. As the test suite grows, it be-
Line58 comes increasingly difﬁcult to get a test run in which none of the ﬂickering tests fail.
Line59 Flickering tests can mask real defects. If the system itself occasionally fails, the
Line60 tests that accurately detect those failures will seem to be ﬂickering. If the suite
Line61 contains unreliable tests, intermittent failures detected by reliable tests can easily
Line62 be ignored. We need to make sure we understand what the real problem is before
Line63 we ignore ﬂickering tests.
Line64 Allowing ﬂickering tests is bad for the team. It breaks the culture of quality where
Line65 things should “just work,” and even a few ﬂickering tests can make a team stop
Line66 paying attention to broken builds. It also breaks the habit of feedback. We should
Line67 be paying attention to why the tests are ﬂickering and whether that means we
Line68 should improve the design of both the tests and code. Of course, there might be
Line69 times when we have to compromise and decide to live with a ﬂickering test for the
Line70 moment, but this should be done reluctantly and include a plan for when it will
Line71 be ﬁxed.
Line72 As we saw in the last chapter, synchronizing by simply making each test wait
Line73 for a ﬁxed time is not practical. The test suite for a system of any size will take
Line74 too long to run. We know we’ll have to wait for failing tests to time out, but
Line75 succeeding tests should be able to ﬁnish as soon as there’s a response from
Line76 the code.
Line77 Succeed Fast
Line78 Make asynchronous tests detect success as quickly as possible so that they provide
Line79 rapid feedback.
Line80 Of the two observation strategies we outlined in the previous section, listening
Line81 for events is the quickest. The test thread can block, waiting for an event from
Line82 the system. It will wake up and check the result as soon as it receives an event.
Line83 The alternative—sampling—means repeatedly polling the target system for a
Line84 state change, with a short delay between polls. The frequency of this polling has
Line85 to be tuned to the system under test, to balance the need for a fast response
Line86 against the load it imposes on the target system. In the worst case, fast polling
Line87 might slow the system enough to make the tests unreliable.
Line88 317
Line89 Sampling or Listening
Line90 
Line91 
Line92 ---
Line93 
Line94 ---
Line95 **Page 318**
Line96 
Line97 Put the Timeout Values in One Place
Line98 Both observation strategies use a timeout to detect that the system has failed.
Line99 Again, there’s a balance to be struck between a timeout that’s too short, which will
Line100 make the tests unreliable, and one that’s too long, which will make failing tests too
Line101 slow. This balance can be different in different environments, and will change as
Line102 the system grows over time.
Line103 When the timeout duration is deﬁned in one place, it’s easy to ﬁnd and change.
Line104 The team can adjust its value to ﬁnd the right balance between speed and reliability
Line105 as the system develops.
Line106 Two Implementations
Line107 Scattering ad hoc sleeps and timeouts throughout the tests makes them difﬁcult
Line108 to understand, because it leaves too much implementation detail in the tests
Line109 themselves. Synchronization and assertion is just the sort of behavior that’s
Line110 suitable for factoring out into subordinate objects because it usually turns into
Line111 a bad case of duplication if we don’t. It’s also just the sort of tricky code that we
Line112 want to get right once and not have to change again.
Line113 In this section, we’ll show an example implementation of each observation
Line114 strategy.
Line115 Capturing Notiﬁcations
Line116 An event-based assertion waits for an event by blocking on a monitor until it
Line117 gets notiﬁed or times out. When the monitor is notiﬁed, the test thread wakes
Line118 up and continues if it ﬁnds that the expected event has arrived, or blocks again.
Line119 If the test times out, then it raises a failure.
Line120 NotificationTrace is an example of how to record and test notiﬁcations sent
Line121 by the system. The setup of the test will arrange for the tested code to call
Line122 append() when the event happens, for example by plugging in an event listener
Line123 that will call the method when triggered. In the body of the test, the test thread
Line124 calls containsNotification() to wait for the expected notiﬁcation or fail if it
Line125 times out. For example:
Line126 trace.containsNotification(startsWith("WANTED"));
Line127 will wait for a notiﬁcation string that starts with WANTED.
Line128 Within NotificationTrace, incoming notiﬁcations are stored in a list trace,
Line129 which is protected by a lock traceLock. The class is generic, so we don’t specify
Line130 the type of these notiﬁcations, except to say that the matchers we pass into
Line131 containsNotification() must be compatible with that type. The implementation
Line132 uses Timeout and NotificationStream classes that we’ll describe later.
Line133 Chapter 27
Line134 Testing Asynchronous Code
Line135 318
Line136 
Line137 
Line138 ---
