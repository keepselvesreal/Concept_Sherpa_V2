Line1 # Start Each Feature with an Acceptance Test (pp.39-40)
Line2 
Line3 ---
Line4 **Page 39**
Line5 
Line6 Chapter 5
Line7 Maintaining the Test-Driven
Line8 Cycle
Line9 Every day you may make progress. Every step may be fruitful. Yet there
Line10 will stretch out before you an ever-lengthening, ever-ascending,
Line11 ever-improving path. You know you will never get to the end of the
Line12 journey. But this, so far from discouraging, only adds to the joy and
Line13 glory of the climb.
Line14 —Winston Churchill
Line15 Introduction
Line16 Once we’ve kick-started the TDD process, we need to keep it running smoothly.
Line17 In this chapter we’ll show how a TDD process runs once started. The rest of the
Line18 book explores in some detail how we ensure it runs smoothly—how we write
Line19 tests as we build the system, how we use tests to get early feedback on internal
Line20 and external quality issues, and how we ensure that the tests continue to support
Line21 change and do not become an obstacle to further development.
Line22 Start Each Feature with an Acceptance Test
Line23 As we described in Chapter 1, we start work on a new feature by writing failing
Line24 acceptance tests that demonstrate that the system does not yet have the feature
Line25 we’re about to write and track our progress towards completion of the
Line26 feature (Figure 5.1).
Line27 We write the acceptance test using only terminology from the application’s
Line28 domain, not from the underlying technologies (such as databases or web servers).
Line29 This helps us understand what the system should do, without tying us to any of
Line30 our initial assumptions about the implementation or complicating the test with
Line31 technological details. This also shields our acceptance test suite from changes to
Line32 the system’s technical infrastructure. For example, if a third-party organization
Line33 changes the protocol used by their services from FTP and binary ﬁles to web
Line34 services and XML, we should not have to rework the tests for the system’s
Line35 application logic.
Line36 We ﬁnd that writing such a test before coding makes us clarify what we want
Line37 to achieve. The precision of expressing requirements in a form that can be auto-
Line38 matically checked helps us uncover implicit assumptions. The failing tests keep
Line39 39
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 40**
Line46 
Line47 Figure 5.1
Line48 Each TDD cycle starts with a failing acceptance test
Line49 us focused on implementing the limited set of features they describe, improving
Line50 our chances of delivering them. More subtly, starting with tests makes us look
Line51 at the system from the users’ point of view, understanding what they need it to
Line52 do rather than speculating about features from the implementers’ point of view.
Line53 Unit tests, on the other hand, exercise objects, or small clusters of objects, in
Line54 isolation. They’re important to help us design classes and give us conﬁdence that
Line55 they work, but they don’t say anything about whether they work together with
Line56 the rest of the system. Acceptance tests both test the integration of unit-tested
Line57 objects and push the project forwards.
Line58 Separate Tests That Measure Progress from Those That
Line59 Catch Regressions
Line60 When we write acceptance tests to describe a new feature, we expect them to fail
Line61 until that feature has been implemented; new acceptance tests describe work yet
Line62 to be done. The activity of turning acceptance tests from red to green gives the
Line63 team a measure of the progress it’s making. A regular cycle of passing acceptance
Line64 tests is the engine that drives the nested project feedback loops we described in
Line65 “Feedback Is the Fundamental Tool” (page 4). Once passing, the acceptance tests
Line66 now represent completed features and should not fail again. A failure means that
Line67 there’s been a regression, that we’ve broken our existing code.
Line68 We organize our test suites to reﬂect the different roles that the tests fulﬁll.
Line69 Unit and integration tests support the development team, should run quickly,
Line70 and should always pass. Acceptance tests for completed features catch
Line71 regressions and should always pass, although they might take longer to run.
Line72 New acceptance tests represent work in progress and will not pass until a feature
Line73 is ready.
Line74 If requirements change, we must move any affected acceptance tests out of the
Line75 regression suite back into the in-progress suite, edit them to reﬂect the new
Line76 requirements, and change the system to make them pass again.
Line77 Chapter 5
Line78 Maintaining the Test-Driven Cycle
Line79 40
Line80 
Line81 
Line82 ---
