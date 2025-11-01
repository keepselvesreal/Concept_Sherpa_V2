Line1 # Testing End-to-End (pp.8-9)
Line2 
Line3 ---
Line4 **Page 8**
Line5 
Line6 Figure 1.2
Line7 Inner and outer feedback loops in TDD
Line8 The outer test loop is a measure of demonstrable progress, and the growing
Line9 suite of tests protects us against regression failures when we change the system.
Line10 Acceptance tests often take a while to make pass, certainly more than one check-in
Line11 episode, so we usually distinguish between acceptance tests we’re working on
Line12 (which are not yet included in the build) and acceptance tests for the features
Line13 that have been ﬁnished (which are included in the build and must always pass).
Line14 The inner loop supports the developers. The unit tests help us maintain the
Line15 quality of the code and should pass soon after they’ve been written. Failing unit
Line16 tests should never be committed to the source repository.
Line17 Testing End-to-End
Line18 Wherever possible, an acceptance test should exercise the system end-to-end
Line19 without directly calling its internal code. An end-to-end test interacts with the
Line20 system only from the outside: through its user interface, by sending messages as
Line21 if from third-party systems, by invoking its web services, by parsing reports, and
Line22 so on. As we discuss in Chapter 10, the whole behavior of the system includes
Line23 its interaction with its external environment. This is often the riskiest and most
Line24 difﬁcult aspect; we ignore it at our peril. We try to avoid acceptance tests that
Line25 just exercise the internal objects of the system, unless we really need the speed-up
Line26 and already have a stable set of end-to-end tests to provide cover.
Line27 The Importance of End-to-End Testing: A Horror Story
Line28 Nat was once brought onto a project that had been using TDD since its inception.
Line29 The team had been writing acceptance tests to capture requirements and show
Line30 progress to their customer representatives. They had been writing unit tests for
Line31 the classes of the system, and the internals were clean and easy to change.They
Line32 had been making great progress, and the customer representatives had signed
Line33 off all the implemented features on the basis of the passing acceptance tests.
Line34 Chapter 1
Line35 What Is the Point of Test-Driven Development?
Line36 8
Line37 
Line38 
Line39 ---
Line40 
Line41 ---
Line42 **Page 9**
Line43 
Line44 But the acceptance tests did not run end-to-end—they instantiated the system’s
Line45 internal objects and directly invoked their methods. The application actually did
Line46 nothing at all. Its entry point contained only a single comment:
Line47 // TODO implement this
Line48 Additional feedback loops, such as regular show-and-tell sessions, should have
Line49 been in place and would have caught this problem.
Line50 For us, “end-to-end” means more than just interacting with the system from
Line51 the outside—that might be better called “edge-to-edge” testing. We prefer to
Line52 have the end-to-end tests exercise both the system and the process by which it’s
Line53 built and deployed. An automated build, usually triggered by someone checking
Line54 code into the source repository, will: check out the latest version; compile and
Line55 unit-test the code; integrate and package the system; perform a production-like
Line56 deployment into a realistic environment; and, ﬁnally, exercise the system through
Line57 its external access points. This sounds like a lot of effort (it is), but has to be
Line58 done anyway repeatedly during the software’s lifetime. Many of the steps might
Line59 be ﬁddly and error-prone, so the end-to-end build cycle is an ideal candidate for
Line60 automation. You’ll see in Chapter 10 how early in a project we get this working.
Line61 A system is deployable when the acceptance tests all pass, because they should
Line62 give us enough conﬁdence that everything works. There’s still, however, a ﬁnal
Line63 step of deploying to production. In many organizations, especially large or
Line64 heavily regulated ones, building a deployable system is only the start of a release
Line65 process. The rest, before the new features are ﬁnally available to the end users,
Line66 might involve different kinds of testing, handing over to operations and data
Line67 groups, and coordinating with other teams’ releases. There may also be additional,
Line68 nontechnical costs involved with a release, such as training, marketing, or an
Line69 impact on service agreements for downtime. The result is a more difﬁcult release
Line70 cycle than we would like, so we have to understand our whole technical and
Line71 organizational environment.
Line72 Levels of Testing
Line73 We build a hierarchy of tests that correspond to some of the nested feedback
Line74 loops we described above:
Line75 Acceptance:  Does the whole system work?
Line76 Integration:  Does our code work against code we can't change?
Line77 Unit:  Do our objects do the right thing, are they convenient to work with?
Line78 9
Line79 Levels of Testing
Line80 
Line81 
Line82 ---
