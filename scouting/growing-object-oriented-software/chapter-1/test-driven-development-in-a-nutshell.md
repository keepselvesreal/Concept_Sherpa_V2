Line1 # Test-Driven Development in a Nutshell (pp.6-7)
Line2 
Line3 ---
Line4 **Page 6**
Line5 
Line6 Test-Driven Development in a Nutshell
Line7 The cycle at the heart of TDD is: write a test; write some code to get it working;
Line8 refactor the code to be as simple an implementation of the tested features as
Line9 possible. Repeat.
Line10 Figure 1.1
Line11 The fundamental TDD cycle
Line12 As we develop the system, we use TDD to give us feedback on the quality of
Line13 both its implementation (“Does it work?”) and design (“Is it well structured?”).
Line14 Developing test-ﬁrst, we ﬁnd we beneﬁt twice from the effort. Writing tests:
Line15 •
Line16 makes us clarify the acceptance criteria for the next piece of work—we
Line17 have to ask ourselves how we can tell when we’re done (design);
Line18 •
Line19 encourages us to write loosely coupled components, so they can easily be
Line20 tested in isolation and, at higher levels, combined together (design);
Line21 •
Line22 adds an executable description of what the code does (design); and,
Line23 •
Line24 adds to a complete regression suite (implementation);
Line25 whereas running tests:
Line26 •
Line27 detects errors while the context is fresh in our mind (implementation); and,
Line28 •
Line29 lets us know when we’ve done enough, discouraging “gold plating” and
Line30 unnecessary features (design).
Line31 This feedback cycle can be summed up by the Golden Rule of TDD:
Line32 The Golden Rule of Test-Driven Development
Line33 Never write new functionality without a failing test.
Line34 Chapter 1
Line35 What Is the Point of Test-Driven Development?
Line36 6
Line37 
Line38 
Line39 ---
Line40 
Line41 ---
Line42 **Page 7**
Line43 
Line44 Refactoring.Think Local, Act Local
Line45 Refactoring means changing the internal structure of an existing body of code
Line46 without changing its behavior.The point is to improve the code so that it’s a better
Line47 representation of the features it implements, making it more maintainable.
Line48 Refactoring is a disciplined technique where the programmer applies a series of
Line49 transformations (or “refactorings”) that do not change the code’s behavior. Each
Line50 refactoring is small enough to be easy to understand and “safe”; for example, a
Line51 programmer might pull a block of code into a helper method to make the original
Line52 method shorter and easier to understand. The programmer makes sure that the
Line53 system is still working after each refactoring step, minimizing the risk of getting
Line54 stranded by a change; in test-driven code, we can do that by running the tests.
Line55 Refactoring is a “microtechnique” that is driven by ﬁnding small-scale im-
Line56 provements. Our experience is that, applied rigorously and consistently, its many
Line57 small steps can lead to signiﬁcant structural improvements. Refactoring is not the
Line58 same activity as redesign, where the programmers take a conscious decision to
Line59 change a large-scale structure. That said, having taken a redesign decision, a
Line60 team can use refactoring techniques to get to the new design incrementally
Line61 and safely.
Line62 You’ll see quite a lot of refactoring in our example in Part III. The standard text on
Line63 the concept is Fowler’s [Fowler99].
Line64 The Bigger Picture
Line65 It is tempting to start the TDD process by writing unit tests for classes in the
Line66 application. This is better than having no tests at all and can catch those basic
Line67 programming errors that we all know but ﬁnd so hard to avoid: fencepost errors,
Line68 incorrect boolean expressions, and the like. But a project with only unit tests is
Line69 missing out on critical beneﬁts of the TDD process. We’ve seen projects with
Line70 high-quality, well unit-tested code that turned out not to be called from anywhere,
Line71 or that could not be integrated with the rest of the system and had to be rewritten.
Line72 How do we know where to start writing code? More importantly, how do we
Line73 know when to stop writing code? The golden rule tells us what we need to do:
Line74 Write a failing test.
Line75 When we’re implementing a feature, we start by writing an acceptance test,
Line76 which exercises the functionality we want to build. While it’s failing, an acceptance
Line77 test demonstrates that the system does not yet implement that feature; when it
Line78 passes, we’re done. When working on a feature, we use its acceptance test to
Line79 guide us as to whether we actually need the code we’re about to write—we only
Line80 write code that’s directly relevant. Underneath the acceptance test, we follow the
Line81 unit level test/implement/refactor cycle to develop the feature; the whole cycle
Line82 looks like Figure 1.2.
Line83 7
Line84 The Bigger Picture
Line85 
Line86 
Line87 ---
