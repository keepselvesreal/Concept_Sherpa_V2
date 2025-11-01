Line1 # Separate Tests That Measure Progress from Those That Catch Regressions (pp.40-41)
Line2 
Line3 ---
Line4 **Page 40**
Line5 
Line6 Figure 5.1
Line7 Each TDD cycle starts with a failing acceptance test
Line8 us focused on implementing the limited set of features they describe, improving
Line9 our chances of delivering them. More subtly, starting with tests makes us look
Line10 at the system from the users’ point of view, understanding what they need it to
Line11 do rather than speculating about features from the implementers’ point of view.
Line12 Unit tests, on the other hand, exercise objects, or small clusters of objects, in
Line13 isolation. They’re important to help us design classes and give us conﬁdence that
Line14 they work, but they don’t say anything about whether they work together with
Line15 the rest of the system. Acceptance tests both test the integration of unit-tested
Line16 objects and push the project forwards.
Line17 Separate Tests That Measure Progress from Those That
Line18 Catch Regressions
Line19 When we write acceptance tests to describe a new feature, we expect them to fail
Line20 until that feature has been implemented; new acceptance tests describe work yet
Line21 to be done. The activity of turning acceptance tests from red to green gives the
Line22 team a measure of the progress it’s making. A regular cycle of passing acceptance
Line23 tests is the engine that drives the nested project feedback loops we described in
Line24 “Feedback Is the Fundamental Tool” (page 4). Once passing, the acceptance tests
Line25 now represent completed features and should not fail again. A failure means that
Line26 there’s been a regression, that we’ve broken our existing code.
Line27 We organize our test suites to reﬂect the different roles that the tests fulﬁll.
Line28 Unit and integration tests support the development team, should run quickly,
Line29 and should always pass. Acceptance tests for completed features catch
Line30 regressions and should always pass, although they might take longer to run.
Line31 New acceptance tests represent work in progress and will not pass until a feature
Line32 is ready.
Line33 If requirements change, we must move any affected acceptance tests out of the
Line34 regression suite back into the in-progress suite, edit them to reﬂect the new
Line35 requirements, and change the system to make them pass again.
Line36 Chapter 5
Line37 Maintaining the Test-Driven Cycle
Line38 40
Line39 
Line40 
Line41 ---
Line42 
Line43 ---
Line44 **Page 41**
Line45 
Line46 Start Testing with the Simplest Success Case
Line47 Where do we start when we have to write a new class or feature? It’s tempting
Line48 to start with degenerate or failure cases because they’re often easier. That’s a
Line49 common interpretation of the XP maxim to do “the simplest thing that could
Line50 possibly work” [Beck02], but simple should not be interpreted as simplistic.
Line51 Degenerate cases don’t add much to the value of the system and, more important-
Line52 ly, don’t give us enough feedback about the validity of our ideas. Incidentally,
Line53 we also ﬁnd that focusing on the failure cases at the beginning of a feature is bad
Line54 for morale—if we only work on error handling it feels like we’re not achieving
Line55 anything.
Line56 We prefer to start by testing the simplest success case. Once that’s working,
Line57 we’ll have a better idea of the real structure of the solution and can prioritize
Line58 between handling any possible failures we noticed along the way and further
Line59 success cases. Of course, a feature isn’t complete until it’s robust. This isn’t an
Line60 excuse not to bother with failure handling—but we can choose when we want
Line61 to implement ﬁrst.
Line62 We ﬁnd it useful to keep a notepad or index cards by the keyboard to jot down
Line63 failure cases, refactorings, and other technical tasks that need to be addressed.
Line64 This allows us to stay focused on the task at hand without dropping detail. The
Line65 feature is ﬁnished only when we’ve crossed off everything on the list—either
Line66 we’ve done each task or decided that we don’t need to.
Line67 Iterations in Space
Line68 We’re writing this material around the fortieth anniversary of the ﬁrst Moon landing.
Line69 The Moon program was an excellent example of an incremental approach (although
Line70 with much larger stakes than we’re used to). In 1967, they proposed a series of
Line71 seven missions, each of which would be a step on the way to a landing:
Line72 1.
Line73 Unmanned Command/Service Module (CSM) test
Line74 2.
Line75 Unmanned Lunar Module (LM) test
Line76 3.
Line77 Manned CSM in low Earth orbit
Line78 4.
Line79 Manned CSM and LM in low Earth orbit
Line80 5.
Line81 Manned CSM and LM in an elliptical Earth orbit with an apogee of 4600 mi
Line82 (7400 km)
Line83 6.
Line84 Manned CSM and LM in lunar orbit
Line85 7.
Line86 Manned lunar landing
Line87 At least in software, we can develop incrementally without building a new rocket
Line88 each time.
Line89 41
Line90 Start Testing with the Simplest Success Case
Line91 
Line92 
Line93 ---
