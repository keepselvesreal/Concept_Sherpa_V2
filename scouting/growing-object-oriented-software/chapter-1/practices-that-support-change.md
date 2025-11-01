Line1 # Practices That Support Change (pp.5-6)
Line2 
Line3 ---
Line4 **Page 5**
Line5 
Line6 Practices That Support Change
Line7 We’ve found that we need two technical foundations if we want to grow a system
Line8 reliably and to cope with the unanticipated changes that always happen. First,
Line9 we need constant testing to catch regression errors, so we can add new features
Line10 without breaking existing ones. For systems of any interesting size, frequent
Line11 manual testing is just impractical, so we must automate testing as much as we
Line12 can to reduce the costs of building, deploying, and modifying versions of the
Line13 system.
Line14 Second, we need to keep the code as simple as possible, so it’s easier to under-
Line15 stand and modify. Developers spend far more time reading code than writing it,
Line16 so that’s what we should optimize for.1 Simplicity takes effort, so we constantly
Line17 refactor [Fowler99] our code as we work with it—to improve and simplify its
Line18 design, to remove duplication, and to ensure that it clearly expresses what it does.
Line19 The test suites in the feedback loops protect us against our own mistakes as we
Line20 improve (and therefore change) the code.
Line21 The catch is that few developers enjoy testing their code. In many development
Line22 groups, writing automated tests is seen as not “real” work compared to adding
Line23 features, and boring as well. Most people do not do as well as they should at
Line24 work they ﬁnd uninspiring.
Line25 Test-Driven Development (TDD) turns this situation on its head. We write
Line26 our tests before we write the code. Instead of just using testing to verify our work
Line27 after it’s done, TDD turns testing into a design activity. We use the tests to clarify
Line28 our ideas about what we want the code to do. As Kent Beck described it to us,
Line29 “I was ﬁnally able to separate logical from physical design. I’d always been told
Line30 to do that but no one ever explained how.” We ﬁnd that the effort of writing a
Line31 test ﬁrst also gives us rapid feedback about the quality of our design ideas—that
Line32 making code accessible for testing often drives it towards being cleaner and more
Line33 modular.
Line34 If we write tests all the way through the development process, we can build
Line35 up a safety net of automated regression tests that give us the conﬁdence to make
Line36 changes.
Line37 “… you have nothing to lose but your bugs”
Line38 We cannot emphasize strongly enough how liberating it is to work on test-driven
Line39 code that has thorough test coverage.We ﬁnd that we can concentrate on the task
Line40 in hand, conﬁdent that we’re doing the right work and that it’s actually quite hard
Line41 to break the system—as long as we follow the practices.
Line42 1. Begel and Simon [Begel08] showed that new graduates at Microsoft spend most of
Line43 their ﬁrst year just reading code.
Line44 5
Line45 Practices That Support Change
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 6**
Line52 
Line53 Test-Driven Development in a Nutshell
Line54 The cycle at the heart of TDD is: write a test; write some code to get it working;
Line55 refactor the code to be as simple an implementation of the tested features as
Line56 possible. Repeat.
Line57 Figure 1.1
Line58 The fundamental TDD cycle
Line59 As we develop the system, we use TDD to give us feedback on the quality of
Line60 both its implementation (“Does it work?”) and design (“Is it well structured?”).
Line61 Developing test-ﬁrst, we ﬁnd we beneﬁt twice from the effort. Writing tests:
Line62 •
Line63 makes us clarify the acceptance criteria for the next piece of work—we
Line64 have to ask ourselves how we can tell when we’re done (design);
Line65 •
Line66 encourages us to write loosely coupled components, so they can easily be
Line67 tested in isolation and, at higher levels, combined together (design);
Line68 •
Line69 adds an executable description of what the code does (design); and,
Line70 •
Line71 adds to a complete regression suite (implementation);
Line72 whereas running tests:
Line73 •
Line74 detects errors while the context is fresh in our mind (implementation); and,
Line75 •
Line76 lets us know when we’ve done enough, discouraging “gold plating” and
Line77 unnecessary features (design).
Line78 This feedback cycle can be summed up by the Golden Rule of TDD:
Line79 The Golden Rule of Test-Driven Development
Line80 Never write new functionality without a failing test.
Line81 Chapter 1
Line82 What Is the Point of Test-Driven Development?
Line83 6
Line84 
Line85 
Line86 ---
