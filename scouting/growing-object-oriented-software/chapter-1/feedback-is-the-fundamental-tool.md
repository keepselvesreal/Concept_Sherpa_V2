Line1 # Feedback Is the Fundamental Tool (pp.4-5)
Line2 
Line3 ---
Line4 **Page 4**
Line5 
Line6 Feedback Is the Fundamental Tool
Line7 We think that the best approach a team can take is to use empirical feedback to
Line8 learn about the system and its use, and then apply that learning back to the system.
Line9 A team needs repeated cycles of activity. In each cycle it adds new features and
Line10 gets feedback about the quantity and quality of the work already done. The team
Line11 members split the work into time boxes, within which they analyze, design,
Line12 implement, and deploy as many features as they can.
Line13 Deploying completed work to some kind of environment at each cycle is critical.
Line14 Every time a team deploys, its members have an opportunity to check their as-
Line15 sumptions against reality. They can measure how much progress they’re really
Line16 making, detect and correct any errors, and adapt the current plan in response to
Line17 what they’ve learned. Without deployment, the feedback is not complete.
Line18 In our work, we apply feedback cycles at every level of development, organizing
Line19 projects as a system of nested loops ranging from seconds to months, such as:
Line20 pair programming, unit tests, acceptance tests, daily meetings, iterations, releases,
Line21 and so on. Each loop exposes the team’s output to empirical feedback so that
Line22 the team can discover and correct any errors or misconceptions. The nested
Line23 feedback loops reinforce each other; if a discrepancy slips through an inner loop,
Line24 there is a good chance an outer loop will catch it.
Line25 Each feedback loop addresses different aspects of the system and development
Line26 process. The inner loops are more focused on the technical detail: what a unit of
Line27 code does, whether it integrates with the rest of the system. The outer loops are
Line28 more focused on the organization and the team: whether the application serves
Line29 its users’ needs, whether the team is as effective as it could be.
Line30 The sooner we can get feedback about any aspect of the project, the better.
Line31 Many teams in large organizations can release every few weeks. Some teams re-
Line32 lease every few days, or even hours, which gives them an order of magnitude
Line33 increase in opportunities to receive and respond to feedback from real users.
Line34 Incremental and Iterative Development
Line35 In a project organized as a set of nested feedback loops, development is
Line36 incremental and iterative.
Line37 Incremental development builds a system feature by feature, instead of building
Line38 all the layers and components and integrating them at the end. Each feature is
Line39 implemented as an end-to-end “slice” through all the relevant parts of the system.
Line40 The system is always integrated and ready for deployment.
Line41 Iterative development progressively reﬁnes the implementation of features in
Line42 response to feedback until they are good enough.
Line43 Chapter 1
Line44 What Is the Point of Test-Driven Development?
Line45 4
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 5**
Line52 
Line53 Practices That Support Change
Line54 We’ve found that we need two technical foundations if we want to grow a system
Line55 reliably and to cope with the unanticipated changes that always happen. First,
Line56 we need constant testing to catch regression errors, so we can add new features
Line57 without breaking existing ones. For systems of any interesting size, frequent
Line58 manual testing is just impractical, so we must automate testing as much as we
Line59 can to reduce the costs of building, deploying, and modifying versions of the
Line60 system.
Line61 Second, we need to keep the code as simple as possible, so it’s easier to under-
Line62 stand and modify. Developers spend far more time reading code than writing it,
Line63 so that’s what we should optimize for.1 Simplicity takes effort, so we constantly
Line64 refactor [Fowler99] our code as we work with it—to improve and simplify its
Line65 design, to remove duplication, and to ensure that it clearly expresses what it does.
Line66 The test suites in the feedback loops protect us against our own mistakes as we
Line67 improve (and therefore change) the code.
Line68 The catch is that few developers enjoy testing their code. In many development
Line69 groups, writing automated tests is seen as not “real” work compared to adding
Line70 features, and boring as well. Most people do not do as well as they should at
Line71 work they ﬁnd uninspiring.
Line72 Test-Driven Development (TDD) turns this situation on its head. We write
Line73 our tests before we write the code. Instead of just using testing to verify our work
Line74 after it’s done, TDD turns testing into a design activity. We use the tests to clarify
Line75 our ideas about what we want the code to do. As Kent Beck described it to us,
Line76 “I was ﬁnally able to separate logical from physical design. I’d always been told
Line77 to do that but no one ever explained how.” We ﬁnd that the effort of writing a
Line78 test ﬁrst also gives us rapid feedback about the quality of our design ideas—that
Line79 making code accessible for testing often drives it towards being cleaner and more
Line80 modular.
Line81 If we write tests all the way through the development process, we can build
Line82 up a safety net of automated regression tests that give us the conﬁdence to make
Line83 changes.
Line84 “… you have nothing to lose but your bugs”
Line85 We cannot emphasize strongly enough how liberating it is to work on test-driven
Line86 code that has thorough test coverage.We ﬁnd that we can concentrate on the task
Line87 in hand, conﬁdent that we’re doing the right work and that it’s actually quite hard
Line88 to break the system—as long as we follow the practices.
Line89 1. Begel and Simon [Begel08] showed that new graduates at Microsoft spend most of
Line90 their ﬁrst year just reading code.
Line91 5
Line92 Practices That Support Change
Line93 
Line94 
Line95 ---
