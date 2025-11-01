Line1 # Some Initial Choices (pp.86-88)
Line2 
Line3 ---
Line4 **Page 86**
Line5 
Line6 We’ve adopted certain naming conventions for the methods of the helper ob-
Line7 jects. If a method triggers an event to drive the test, its name will be a command,
Line8 such as startBiddingIn(). If a method asserts that something should have hap-
Line9 pened, its name will be descriptive;1 for example, showsSniperHasLostAuction()
Line10 will throw an exception if the application is not showing the auction status as
Line11 lost. JUnit will call the two stop() methods after the test has run, to clean up
Line12 the runtime environment.
Line13 In writing the test, one of the assumptions we’ve made is that a
Line14 FakeAuctionServer is tied to a given item. This matches the structure of our
Line15 intended architecture, where Southabee’s On-Line hosts multiple auctions, each
Line16 selling a single item.
Line17 One Domain at a Time
Line18 The language of this test is concerned with auctions and Snipers; there’s nothing
Line19 about messaging layers or components in the user interface—that’s all incidental
Line20 detail here. Keeping the language consistent helps us understand what’s signiﬁcant
Line21 in this test, with a nice side effect of protecting us when the implementation inevitably
Line22 changes.
Line23 Some Initial Choices
Line24 Now we have to make the test pass, which will require a lot of preparation. We
Line25 need to ﬁnd or write four components: an XMPP message broker, a stub auction
Line26 that can communicate over XMPP, a GUI testing framework, and a test har-
Line27 ness that can cope with our multithreaded, asynchronous architecture. We also
Line28 have to get the project under version control with an automated build/deploy/test
Line29 process. Compared to unit-testing a single class, there is a lot to do—but it’s es-
Line30 sential. Even at this high level, the exercise of writing tests drives the development
Line31 of the system. Working through our ﬁrst end-to-end test will force some of the
Line32 structural decisions we need to make, such as packaging and deployment.
Line33 First the package selection, we will need an XMPP message broker to let the
Line34 application talk to our stub auction house. After some investigation, we decide
Line35 on an open source implementation called Openﬁre and its associated client library
Line36 Smack. We also need a high-level test framework that can work with Swing
Line37 and Smack, both of which are multithreaded and event-driven. Luckily for us,
Line38 there are several frameworks for testing Swing applications and the way that
Line39 they deal with Swing’s multithreaded, event-driven architecture also works well
Line40 with XMPP messaging. We pick WindowLicker which is open source and supports
Line41 1. For the grammatically pedantic, the names of methods that trigger events are in the
Line42 imperative mood whereas the names of assertions are in the indicative mood.
Line43 Chapter 10
Line44 The Walking Skeleton
Line45 86
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 87**
Line52 
Line53 the asynchronous approach that we need in our tests. When assembled, the
Line54 infrastructure will look like Figure 10.2:
Line55 Figure 10.2
Line56 The end-to-end test rig
Line57 End-to-End Testing
Line58 End-to-end testing for event-based systems, such as our Sniper, has to cope with
Line59 asynchrony. The tests run in parallel with the application and do not know pre-
Line60 cisely when the application is or isn’t ready. This is unlike unit testing, where a
Line61 test drives an object directly in the same thread and so can make direct assertions
Line62 about its state and behavior.
Line63 An end-to-end test can’t peek inside the target application, so it must wait to
Line64 detect some visible effect, such as a user interface change or an entry in a log.
Line65 The usual technique is to poll for the effect and fail if it doesn’t happen within
Line66 a given time limit. There’s a further complexity in that the target application has
Line67 to stabilize after the triggering event long enough for the test to catch the result.
Line68 An asynchronous test waiting for a value that just ﬂashes on the screen will be
Line69 too unreliable for an automated build, so a common technique is to control the
Line70 application and step through the scenario. At each stage, the test waits for an
Line71 assertion to pass, then sends an event to wake the application for the next step.
Line72 See Chapter 14 for a full discussion of testing asynchronous behavior.
Line73 All this makes end-to-end testing slower and more brittle (perhaps the test
Line74 network is just busy today), so failures might need interpretation. We’ve heard
Line75 of teams where timing-related tests have to fail several times in a row before
Line76 they’re reported. This is unlike unit tests which must all pass every time.
Line77 In our case, both Swing and the messaging infrastructure are asynchronous,
Line78 so using WindowLicker (which polls for values) to drive the Sniper covers the
Line79 natural asynchrony of our end-to-end testing.
Line80 87
Line81 Some Initial Choices
Line82 
Line83 
Line84 ---
Line85 
Line86 ---
Line87 **Page 88**
Line88 
Line89 Ready to Start
Line90 You might have noticed that we skipped over one point: this ﬁrst test is not really
Line91 end-to-end. It doesn’t include the real auction service because that is not easily
Line92 available. An important part of the test-driven development skills is judging where
Line93 to set the boundaries of what to test and how to eventually cover everything. In
Line94 this case, we have to start with a fake auction service based on the documentation
Line95 from Southabee’s On-Line. The documentation might or might not be correct,
Line96 so we will record that as a known risk in the project plan and schedule time to
Line97 test against the real server as soon as we have enough functionality to complete
Line98 a meaningful transaction—even if we end up buying a hideous (but cheap) pair
Line99 of candlesticks in a real auction. The sooner we ﬁnd a discrepancy, the less code
Line100 we will have based on that misunderstanding and the more time to ﬁx it.
Line101 We’d better get on with it.
Line102 Chapter 10
Line103 The Walking Skeleton
Line104 88
