Line1 # Start Testing with the Simplest Success Case (pp.41-42)
Line2 
Line3 ---
Line4 **Page 41**
Line5 
Line6 Start Testing with the Simplest Success Case
Line7 Where do we start when we have to write a new class or feature? It’s tempting
Line8 to start with degenerate or failure cases because they’re often easier. That’s a
Line9 common interpretation of the XP maxim to do “the simplest thing that could
Line10 possibly work” [Beck02], but simple should not be interpreted as simplistic.
Line11 Degenerate cases don’t add much to the value of the system and, more important-
Line12 ly, don’t give us enough feedback about the validity of our ideas. Incidentally,
Line13 we also ﬁnd that focusing on the failure cases at the beginning of a feature is bad
Line14 for morale—if we only work on error handling it feels like we’re not achieving
Line15 anything.
Line16 We prefer to start by testing the simplest success case. Once that’s working,
Line17 we’ll have a better idea of the real structure of the solution and can prioritize
Line18 between handling any possible failures we noticed along the way and further
Line19 success cases. Of course, a feature isn’t complete until it’s robust. This isn’t an
Line20 excuse not to bother with failure handling—but we can choose when we want
Line21 to implement ﬁrst.
Line22 We ﬁnd it useful to keep a notepad or index cards by the keyboard to jot down
Line23 failure cases, refactorings, and other technical tasks that need to be addressed.
Line24 This allows us to stay focused on the task at hand without dropping detail. The
Line25 feature is ﬁnished only when we’ve crossed off everything on the list—either
Line26 we’ve done each task or decided that we don’t need to.
Line27 Iterations in Space
Line28 We’re writing this material around the fortieth anniversary of the ﬁrst Moon landing.
Line29 The Moon program was an excellent example of an incremental approach (although
Line30 with much larger stakes than we’re used to). In 1967, they proposed a series of
Line31 seven missions, each of which would be a step on the way to a landing:
Line32 1.
Line33 Unmanned Command/Service Module (CSM) test
Line34 2.
Line35 Unmanned Lunar Module (LM) test
Line36 3.
Line37 Manned CSM in low Earth orbit
Line38 4.
Line39 Manned CSM and LM in low Earth orbit
Line40 5.
Line41 Manned CSM and LM in an elliptical Earth orbit with an apogee of 4600 mi
Line42 (7400 km)
Line43 6.
Line44 Manned CSM and LM in lunar orbit
Line45 7.
Line46 Manned lunar landing
Line47 At least in software, we can develop incrementally without building a new rocket
Line48 each time.
Line49 41
Line50 Start Testing with the Simplest Success Case
Line51 
Line52 
Line53 ---
Line54 
Line55 ---
Line56 **Page 42**
Line57 
Line58 Write the Test That You’d Want to Read
Line59 We want each test to be as clear as possible an expression of the behavior to be
Line60 performed by the system or object. While writing the test, we ignore the fact that
Line61 the test won’t run, or even compile, and just concentrate on its text; we act as
Line62 if the supporting code to let us run the test already exists.
Line63 When the test reads well, we then build up the infrastructure to support the
Line64 test. We know we’ve implemented enough of the supporting code when the test
Line65 fails in the way we’d expect, with a clear error message describing what needs
Line66 to be done. Only then do we start writing the code to make the test pass. We
Line67 look further at making tests readable in Chapter 21.
Line68 Watch the Test Fail
Line69 We always watch the test fail before writing the code to make it pass, and check
Line70 the diagnostic message. If the test fails in a way we didn’t expect, we know we’ve
Line71 misunderstood something or the code is incomplete, so we ﬁx that. When we get
Line72 the “right” failure, we check that the diagnostics are helpful. If the failure descrip-
Line73 tion isn’t clear, someone (probably us) will have to struggle when the code breaks
Line74 in a few weeks’ time. We adjust the test code and rerun the tests until the error
Line75 messages guide us to the problem with the code (Figure 5.2).
Line76 Figure 5.2
Line77 Improving the diagnostics as part of the TDD cycle
Line78 As we write the production code, we keep running the test to see our progress
Line79 and to check the error diagnostics as the system is built up behind the test. Where
Line80 necessary, we extend or modify the support code to ensure the error messages
Line81 are always clear and relevant.
Line82 There’s more than one reason for insisting on checking the error messages.
Line83 First, it checks our assumptions about the code we’re working on—sometimes
Line84 Chapter 5
Line85 Maintaining the Test-Driven Cycle
Line86 42
Line87 
Line88 
Line89 ---
