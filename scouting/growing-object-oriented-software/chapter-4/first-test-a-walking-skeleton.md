Line1 # First, Test a Walking Skeleton (pp.32-33)
Line2 
Line3 ---
Line4 **Page 32**
Line5 
Line6 First, Test a Walking Skeleton
Line7 The quandary in writing and passing the ﬁrst acceptance test is that it’s hard to
Line8 build both the tooling and the feature it’s testing at the same time. Changes in
Line9 one disrupt any progress made with the other, and tracking down failures is
Line10 tricky when the architecture, the tests, and the production code are all moving.
Line11 One of the symptoms of an unstable development environment is that there’s no
Line12 obvious ﬁrst place to look when something fails.
Line13 We can cut through this “ﬁrst-feature paradox” by splitting it into two smaller
Line14 problems. First, work out how to build, deploy, and test a “walking skeleton,”
Line15 then use that infrastructure to write the acceptance tests for the ﬁrst meaningful
Line16 feature. After that, everything will be in place for test-driven development of the
Line17 rest of the system.
Line18 A “walking skeleton” is an implementation of the thinnest possible slice of
Line19 real functionality that we can automatically build, deploy, and test end-to-end
Line20 [Cockburn04]. It should include just enough of the automation, the major com-
Line21 ponents, and communication mechanisms to allow us to start working on the
Line22 ﬁrst feature. We keep the skeleton’s application functionality so simple that it’s
Line23 obvious and uninteresting, leaving us free to concentrate on the infrastructure.
Line24 For example, for a database-backed web application, a skeleton would show a
Line25 ﬂat web page with ﬁelds from the database. In Chapter 10, we’ll show an example
Line26 that displays a single value in the user interface and sends just a handshake
Line27 message to the server.
Line28 It’s also important to realize that the “end” in “end-to-end” refers to the pro-
Line29 cess, as well as the system. We want our test to start from scratch, build a deploy-
Line30 able system, deploy it into a production-like environment, and then run the tests
Line31 through the deployed system. Including the deployment step in the testing process
Line32 is critical for two reasons. First, this is the sort of error-prone activity that should
Line33 not be done by hand, so we want our scripts to have been thoroughly exercised
Line34 by the time we have to deploy for real. One lesson that we’ve learned repeatedly
Line35 is that nothing forces us to understand a process better than trying to automate
Line36 it. Second, this is often the moment where the development team bumps into the
Line37 rest of the organization and has to learn how it operates. If it’s going to take six
Line38 weeks and four signatures to set up a database, we want to know now, not
Line39 two weeks before delivery.
Line40 In practice, of course, real end-to-end testing may be so hard to achieve that
Line41 we have to start with infrastructure that implements our current understanding
Line42 of what the real system will do and what its environment is. We keep in mind,
Line43 however, that this is a stop-gap, a temporary patch until we can ﬁnish the job,
Line44 and that unknown risks remain until our tests really run end-to-end. One of the
Line45 weaknesses of our Auction Sniper example (Part III) is that the tests run against
Line46 Chapter 4
Line47 Kick-Starting the Test-Driven Cycle
Line48 32
Line49 
Line50 
Line51 ---
Line52 
Line53 ---
Line54 **Page 33**
Line55 
Line56 a dummy server, not the real site. At some point before going live, we would
Line57 have had to test against Southabee’s On-Line; the earlier we can do that, the
Line58 easier it will be for us to respond to any surprises that turn up.
Line59 Whilst building the “walking skeleton,” we concentrate on the structure and
Line60 don’t worry too much about cleaning up the test to be beautifully expressive.
Line61 The walking skeleton and its supporting infrastructure are there to help us work
Line62 out how to start test-driven development. It’s only the ﬁrst step toward a complete
Line63 end-to-end acceptance-testing solution. When we write the test for the ﬁrst feature,
Line64 then we need to “write the test you want to read” (page 42) to make sure that
Line65 it’s a clear expression of the behavior of the system.
Line66 The Importance of Early End-to-End Testing
Line67 We joined a project that had been running for a couple of years but had never
Line68 tested their entire system end-to-end. There were frequent production outages
Line69 and deployments often failed. The system was large and complex, reﬂecting the
Line70 complicated business transactions it managed.The effort of building an automated,
Line71 end-to-end test suite was so large that an entire new team had to be formed to
Line72 perform the work. It took them months to build an end-to-end test environment,
Line73 and they never managed to get the entire system covered by an end-to-end
Line74 test suite.
Line75 Because the need for end-to-end testing had not inﬂuenced its design, the system
Line76 was difﬁcult to test. For example, the system’s components used internal timers
Line77 to schedule activities, some of them days or weeks into the future. This made it
Line78 very difﬁcult to write end-to-end tests: It was impractical to run the tests in real-
Line79 time but the scheduling could not be inﬂuenced from outside the system. The
Line80 developers had to redesign the system itself so that periodic activities were trig-
Line81 gered by messages sent from a remote scheduler which could be replaced in the
Line82 test environment; see “Externalize Event Sources” (page 326).This was a signiﬁ-
Line83 cant architectural change—and it was very risky because it had to be performed
Line84 without end-to-end test coverage.
Line85 Deciding the Shape of the Walking Skeleton
Line86 The development of a “walking skeleton” is the moment when we start to make
Line87 choices about the high-level structure of our application. We can’t automate the
Line88 build, deploy, and test cycle without some idea of the overall structure. We don’t
Line89 need much detail yet, just a broad-brush picture of what major system components
Line90 will be needed to support the ﬁrst planned release and how they will communicate.
Line91 Our rule of thumb is that we should be able to draw the design for the “walking
Line92 skeleton” in a few minutes on a whiteboard.
Line93 33
Line94 Deciding the Shape of the Walking Skeleton
Line95 
Line96 
Line97 ---
