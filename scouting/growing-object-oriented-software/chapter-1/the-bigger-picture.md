Line1 # The Bigger Picture (pp.7-8)
Line2 
Line3 ---
Line4 **Page 7**
Line5 
Line6 Refactoring.Think Local, Act Local
Line7 Refactoring means changing the internal structure of an existing body of code
Line8 without changing its behavior.The point is to improve the code so that it’s a better
Line9 representation of the features it implements, making it more maintainable.
Line10 Refactoring is a disciplined technique where the programmer applies a series of
Line11 transformations (or “refactorings”) that do not change the code’s behavior. Each
Line12 refactoring is small enough to be easy to understand and “safe”; for example, a
Line13 programmer might pull a block of code into a helper method to make the original
Line14 method shorter and easier to understand. The programmer makes sure that the
Line15 system is still working after each refactoring step, minimizing the risk of getting
Line16 stranded by a change; in test-driven code, we can do that by running the tests.
Line17 Refactoring is a “microtechnique” that is driven by ﬁnding small-scale im-
Line18 provements. Our experience is that, applied rigorously and consistently, its many
Line19 small steps can lead to signiﬁcant structural improvements. Refactoring is not the
Line20 same activity as redesign, where the programmers take a conscious decision to
Line21 change a large-scale structure. That said, having taken a redesign decision, a
Line22 team can use refactoring techniques to get to the new design incrementally
Line23 and safely.
Line24 You’ll see quite a lot of refactoring in our example in Part III. The standard text on
Line25 the concept is Fowler’s [Fowler99].
Line26 The Bigger Picture
Line27 It is tempting to start the TDD process by writing unit tests for classes in the
Line28 application. This is better than having no tests at all and can catch those basic
Line29 programming errors that we all know but ﬁnd so hard to avoid: fencepost errors,
Line30 incorrect boolean expressions, and the like. But a project with only unit tests is
Line31 missing out on critical beneﬁts of the TDD process. We’ve seen projects with
Line32 high-quality, well unit-tested code that turned out not to be called from anywhere,
Line33 or that could not be integrated with the rest of the system and had to be rewritten.
Line34 How do we know where to start writing code? More importantly, how do we
Line35 know when to stop writing code? The golden rule tells us what we need to do:
Line36 Write a failing test.
Line37 When we’re implementing a feature, we start by writing an acceptance test,
Line38 which exercises the functionality we want to build. While it’s failing, an acceptance
Line39 test demonstrates that the system does not yet implement that feature; when it
Line40 passes, we’re done. When working on a feature, we use its acceptance test to
Line41 guide us as to whether we actually need the code we’re about to write—we only
Line42 write code that’s directly relevant. Underneath the acceptance test, we follow the
Line43 unit level test/implement/refactor cycle to develop the feature; the whole cycle
Line44 looks like Figure 1.2.
Line45 7
Line46 The Bigger Picture
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 8**
Line53 
Line54 Figure 1.2
Line55 Inner and outer feedback loops in TDD
Line56 The outer test loop is a measure of demonstrable progress, and the growing
Line57 suite of tests protects us against regression failures when we change the system.
Line58 Acceptance tests often take a while to make pass, certainly more than one check-in
Line59 episode, so we usually distinguish between acceptance tests we’re working on
Line60 (which are not yet included in the build) and acceptance tests for the features
Line61 that have been ﬁnished (which are included in the build and must always pass).
Line62 The inner loop supports the developers. The unit tests help us maintain the
Line63 quality of the code and should pass soon after they’ve been written. Failing unit
Line64 tests should never be committed to the source repository.
Line65 Testing End-to-End
Line66 Wherever possible, an acceptance test should exercise the system end-to-end
Line67 without directly calling its internal code. An end-to-end test interacts with the
Line68 system only from the outside: through its user interface, by sending messages as
Line69 if from third-party systems, by invoking its web services, by parsing reports, and
Line70 so on. As we discuss in Chapter 10, the whole behavior of the system includes
Line71 its interaction with its external environment. This is often the riskiest and most
Line72 difﬁcult aspect; we ignore it at our peril. We try to avoid acceptance tests that
Line73 just exercise the internal objects of the system, unless we really need the speed-up
Line74 and already have a stable set of end-to-end tests to provide cover.
Line75 The Importance of End-to-End Testing: A Horror Story
Line76 Nat was once brought onto a project that had been using TDD since its inception.
Line77 The team had been writing acceptance tests to capture requirements and show
Line78 progress to their customer representatives. They had been writing unit tests for
Line79 the classes of the system, and the internals were clean and easy to change.They
Line80 had been making great progress, and the customer representatives had signed
Line81 off all the implemented features on the basis of the passing acceptance tests.
Line82 Chapter 1
Line83 What Is the Point of Test-Driven Development?
Line84 8
Line85 
Line86 
Line87 ---
