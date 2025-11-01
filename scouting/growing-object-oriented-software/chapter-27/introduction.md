Line1 # Introduction (pp.315-316)
Line2 
Line3 ---
Line4 **Page 315**
Line5 
Line6 Chapter 27
Line7 Testing Asynchronous Code
Line8 I can spell banana but I never know when to stop.
Line9 —Johnny Mercer (songwriter)
Line10 Introduction
Line11 Some tests must cope with asynchronous behavior—whether they’re end-to-end
Line12 tests probing a system from the outside or, as we’ve just seen, unit tests exercising
Line13 multithreaded code. These tests trigger some activity within the system to run
Line14 concurrently with the test’s thread. The critical difference from “normal” tests,
Line15 where there is no concurrency, is that control returns to the test before the tested
Line16 activity is complete—returning from the call to the target code does not mean
Line17 that it’s ready to be checked.
Line18 For example, this test assumes that a Set has ﬁnished adding an element when
Line19 the add() method returns. Asserting that set has a size of one veriﬁes that it did
Line20 not store duplicate elements.
Line21 @Test public void storesUniqueElements() {
Line22   Set set = new HashSet<String>();
Line23   set.add("bananana");
Line24   set.add("bananana");
Line25   assertThat(set.size(), equalTo(1));
Line26 }
Line27 By contrast, this system test is asynchronous. The holdingOfStock() method
Line28 synchronously downloads a stock report by HTTP, but the send() method sends
Line29 an asynchronous message to a server that updates its records of stocks held.
Line30 @Test public void buyAndSellOfSameStockOnSameDayCancelsOutOurHolding() {
Line31   Date tradeDate = new Date();
Line32   send(aTradeEvent().ofType(BUY).onDate(tradeDate).forStock("A").withQuantity(10));
Line33   send(aTradeEvent().ofType(SELL).onDate(tradeDate).forStock("A").withQuantity(10));
Line34   assertThat(holdingOfStock("A", tradeDate), equalTo(0));
Line35 }
Line36 The transmission and processing of a trade message happens concurrently with
Line37 the test, so the server might not have received or processed the messages yet
Line38 315
Line39 
Line40 
Line41 ---
Line42 
Line43 ---
Line44 **Page 316**
Line45 
Line46 when the test makes its assertion. The value of the stock holding that the assertion
Line47 checks will depend on timings: how long the messages take to reach the server,
Line48 how long the server takes to update its database, and how long the test takes to
Line49 run. The test might ﬁre the assertion after both messages have been processed
Line50 (passing correctly), after one message (failing incorrectly), or before either
Line51 message (passing, but testing nothing at all).
Line52 As you can see from this small example, with an asynchronous test we have
Line53 to be careful about its coordination with the system it’s testing. Otherwise, it can
Line54 become unreliable, failing intermittently when the system is working or, worse,
Line55 passing when the system is broken.
Line56 Current testing frameworks provide little support for dealing with asynchrony.
Line57 They mostly assume that the tests run in a single thread of control, leaving the
Line58 programmer to build the scaffolding needed to test concurrent behavior. In this
Line59 chapter we describe some practices for writing reliable, responsive tests for
Line60 asynchronous code.
Line61 Sampling or Listening
Line62 The fundamental difﬁculty with testing asynchronous code is that a test triggers
Line63 activity that runs concurrently with the test and therefore cannot immediately
Line64 check the outcome of the activity. The test will not block until the activity has
Line65 ﬁnished. If the activity fails, it will not throw an exception back into the test, so
Line66 the test cannot recognize if the activity is still running or has failed. The test
Line67 therefore has to wait for the activity to complete successfully and fail if this
Line68 doesn’t happen within a given timeout period.
Line69 Wait for Success
Line70 An asynchronous test must wait for success and use timeouts to detect failure.
Line71 This implies that every tested activity must have an observable effect: a test
Line72 must affect the system so that its observable state becomes different. This sounds
Line73 obvious but it drives how we think about writing asynchronous tests. If an activ-
Line74 ity has no observable effect, there is nothing the test can wait for, and therefore
Line75 no way for the test to synchronize with the system it is testing.
Line76 There are two ways a test can observe the system: by sampling its observable
Line77 state or by listening for events that it sends out. Of these, sampling is often the
Line78 only option because many systems don’t send any monitoring events. It’s quite
Line79 common for a test to include both techniques to interact with different “ends”
Line80 of its system. For example, the Auction Sniper end-to-end tests sample the user
Line81 interface for display changes, through the WindowLicker framework, but listen
Line82 for chat events in the fake auction server.
Line83 Chapter 27
Line84 Testing Asynchronous Code
Line85 316
Line86 
Line87 
Line88 ---
