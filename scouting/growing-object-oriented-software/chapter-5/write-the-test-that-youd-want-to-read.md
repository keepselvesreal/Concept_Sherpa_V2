Line1 # Write the Test That You'd Want to Read (pp.42-42)
Line2 
Line3 ---
Line4 **Page 42**
Line5 
Line6 Write the Test That You’d Want to Read
Line7 We want each test to be as clear as possible an expression of the behavior to be
Line8 performed by the system or object. While writing the test, we ignore the fact that
Line9 the test won’t run, or even compile, and just concentrate on its text; we act as
Line10 if the supporting code to let us run the test already exists.
Line11 When the test reads well, we then build up the infrastructure to support the
Line12 test. We know we’ve implemented enough of the supporting code when the test
Line13 fails in the way we’d expect, with a clear error message describing what needs
Line14 to be done. Only then do we start writing the code to make the test pass. We
Line15 look further at making tests readable in Chapter 21.
Line16 Watch the Test Fail
Line17 We always watch the test fail before writing the code to make it pass, and check
Line18 the diagnostic message. If the test fails in a way we didn’t expect, we know we’ve
Line19 misunderstood something or the code is incomplete, so we ﬁx that. When we get
Line20 the “right” failure, we check that the diagnostics are helpful. If the failure descrip-
Line21 tion isn’t clear, someone (probably us) will have to struggle when the code breaks
Line22 in a few weeks’ time. We adjust the test code and rerun the tests until the error
Line23 messages guide us to the problem with the code (Figure 5.2).
Line24 Figure 5.2
Line25 Improving the diagnostics as part of the TDD cycle
Line26 As we write the production code, we keep running the test to see our progress
Line27 and to check the error diagnostics as the system is built up behind the test. Where
Line28 necessary, we extend or modify the support code to ensure the error messages
Line29 are always clear and relevant.
Line30 There’s more than one reason for insisting on checking the error messages.
Line31 First, it checks our assumptions about the code we’re working on—sometimes
Line32 Chapter 5
Line33 Maintaining the Test-Driven Cycle
Line34 42
Line35 
Line36 
Line37 ---
