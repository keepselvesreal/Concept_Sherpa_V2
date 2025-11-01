Line1 # Introduction (pp.31-32)
Line2 
Line3 ---
Line4 **Page 31**
Line5 
Line6 Chapter 4
Line7 Kick-Starting the Test-Driven
Line8 Cycle
Line9 We should be taught not to wait for inspiration to start a thing. Action
Line10 always generates inspiration. Inspiration seldom generates action.
Line11 —Frank Tibolt
Line12 Introduction
Line13 The TDD process we described in Chapter 1 assumes that we can grow the system
Line14 by just slotting the tests for new features into an existing infrastructure. But what
Line15 about the very ﬁrst feature, before we have this infrastructure? As an acceptance
Line16 test, it must run end-to-end to give us the feedback we need about the system’s
Line17 external interfaces, which means we must have implemented a whole automated
Line18 build, deploy, and test cycle. This is a lot of work to do before we can even see
Line19 our ﬁrst test fail.
Line20 Deploying and testing right from the start of a project forces the team to un-
Line21 derstand how their system ﬁts into the world. It ﬂushes out the “unknown
Line22 unknown” technical and organizational risks so they can be addressed while
Line23 there’s still time. Attempting to deploy also helps the team understand who they
Line24 need to liaise with, such as system administrators or external vendors, and start
Line25 to build those relationships.
Line26 Starting with “build, deploy, and test” on a nonexistent system sounds odd,
Line27 but we think it’s essential. The risks of leaving it to later are just too high. We
Line28 have seen projects canceled after months of development because they could not
Line29 reliably deploy their system. We have seen systems discarded because new features
Line30 required months of manual regression testing and even then the error rates were
Line31 too high. As always, we view feedback as a fundamental tool, and we want to
Line32 know as early as possible whether we’re moving in the right direction. Then,
Line33 once we have our ﬁrst test in place, subsequent tests will be much quicker to write.
Line34 31
Line35 
Line36 
Line37 ---
Line38 
Line39 ---
Line40 **Page 32**
Line41 
Line42 First, Test a Walking Skeleton
Line43 The quandary in writing and passing the ﬁrst acceptance test is that it’s hard to
Line44 build both the tooling and the feature it’s testing at the same time. Changes in
Line45 one disrupt any progress made with the other, and tracking down failures is
Line46 tricky when the architecture, the tests, and the production code are all moving.
Line47 One of the symptoms of an unstable development environment is that there’s no
Line48 obvious ﬁrst place to look when something fails.
Line49 We can cut through this “ﬁrst-feature paradox” by splitting it into two smaller
Line50 problems. First, work out how to build, deploy, and test a “walking skeleton,”
Line51 then use that infrastructure to write the acceptance tests for the ﬁrst meaningful
Line52 feature. After that, everything will be in place for test-driven development of the
Line53 rest of the system.
Line54 A “walking skeleton” is an implementation of the thinnest possible slice of
Line55 real functionality that we can automatically build, deploy, and test end-to-end
Line56 [Cockburn04]. It should include just enough of the automation, the major com-
Line57 ponents, and communication mechanisms to allow us to start working on the
Line58 ﬁrst feature. We keep the skeleton’s application functionality so simple that it’s
Line59 obvious and uninteresting, leaving us free to concentrate on the infrastructure.
Line60 For example, for a database-backed web application, a skeleton would show a
Line61 ﬂat web page with ﬁelds from the database. In Chapter 10, we’ll show an example
Line62 that displays a single value in the user interface and sends just a handshake
Line63 message to the server.
Line64 It’s also important to realize that the “end” in “end-to-end” refers to the pro-
Line65 cess, as well as the system. We want our test to start from scratch, build a deploy-
Line66 able system, deploy it into a production-like environment, and then run the tests
Line67 through the deployed system. Including the deployment step in the testing process
Line68 is critical for two reasons. First, this is the sort of error-prone activity that should
Line69 not be done by hand, so we want our scripts to have been thoroughly exercised
Line70 by the time we have to deploy for real. One lesson that we’ve learned repeatedly
Line71 is that nothing forces us to understand a process better than trying to automate
Line72 it. Second, this is often the moment where the development team bumps into the
Line73 rest of the organization and has to learn how it operates. If it’s going to take six
Line74 weeks and four signatures to set up a database, we want to know now, not
Line75 two weeks before delivery.
Line76 In practice, of course, real end-to-end testing may be so hard to achieve that
Line77 we have to start with infrastructure that implements our current understanding
Line78 of what the real system will do and what its environment is. We keep in mind,
Line79 however, that this is a stop-gap, a temporary patch until we can ﬁnish the job,
Line80 and that unknown risks remain until our tests really run end-to-end. One of the
Line81 weaknesses of our Auction Sniper example (Part III) is that the tests run against
Line82 Chapter 4
Line83 Kick-Starting the Test-Driven Cycle
Line84 32
Line85 
Line86 
Line87 ---
