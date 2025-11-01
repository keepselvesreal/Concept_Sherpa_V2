Line1 # Introduction (pp.39-39)
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
