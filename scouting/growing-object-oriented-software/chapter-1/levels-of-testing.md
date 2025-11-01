Line1 # Levels of Testing (pp.9-10)
Line2 
Line3 ---
Line4 **Page 9**
Line5 
Line6 But the acceptance tests did not run end-to-end—they instantiated the system’s
Line7 internal objects and directly invoked their methods. The application actually did
Line8 nothing at all. Its entry point contained only a single comment:
Line9 // TODO implement this
Line10 Additional feedback loops, such as regular show-and-tell sessions, should have
Line11 been in place and would have caught this problem.
Line12 For us, “end-to-end” means more than just interacting with the system from
Line13 the outside—that might be better called “edge-to-edge” testing. We prefer to
Line14 have the end-to-end tests exercise both the system and the process by which it’s
Line15 built and deployed. An automated build, usually triggered by someone checking
Line16 code into the source repository, will: check out the latest version; compile and
Line17 unit-test the code; integrate and package the system; perform a production-like
Line18 deployment into a realistic environment; and, ﬁnally, exercise the system through
Line19 its external access points. This sounds like a lot of effort (it is), but has to be
Line20 done anyway repeatedly during the software’s lifetime. Many of the steps might
Line21 be ﬁddly and error-prone, so the end-to-end build cycle is an ideal candidate for
Line22 automation. You’ll see in Chapter 10 how early in a project we get this working.
Line23 A system is deployable when the acceptance tests all pass, because they should
Line24 give us enough conﬁdence that everything works. There’s still, however, a ﬁnal
Line25 step of deploying to production. In many organizations, especially large or
Line26 heavily regulated ones, building a deployable system is only the start of a release
Line27 process. The rest, before the new features are ﬁnally available to the end users,
Line28 might involve different kinds of testing, handing over to operations and data
Line29 groups, and coordinating with other teams’ releases. There may also be additional,
Line30 nontechnical costs involved with a release, such as training, marketing, or an
Line31 impact on service agreements for downtime. The result is a more difﬁcult release
Line32 cycle than we would like, so we have to understand our whole technical and
Line33 organizational environment.
Line34 Levels of Testing
Line35 We build a hierarchy of tests that correspond to some of the nested feedback
Line36 loops we described above:
Line37 Acceptance:  Does the whole system work?
Line38 Integration:  Does our code work against code we can't change?
Line39 Unit:  Do our objects do the right thing, are they convenient to work with?
Line40 9
Line41 Levels of Testing
Line42 
Line43 
Line44 ---
Line45 
Line46 ---
Line47 **Page 10**
Line48 
Line49 There’s been a lot of discussion in the TDD world over the terminology for
Line50 what we’re calling acceptance tests: “functional tests,” “customer tests,” “system
Line51 tests.” Worse, our deﬁnitions are often not the same as those used by professional
Line52 software testers. The important thing is to be clear about our intentions. We use
Line53 “acceptance tests” to help us, with the domain experts, understand and agree on
Line54 what we are going to build next. We also use them to make sure that we haven’t
Line55 broken any existing features as we continue developing.
Line56 Our preferred implementation of the “role” of acceptance testing is to write
Line57 end-to-end tests which, as we just noted, should be as end-to-end as possible;
Line58 our bias often leads us to use these terms interchangeably although, in some
Line59 cases, acceptance tests might not be end-to-end.
Line60 We use the term integration tests to refer to the tests that check how some of
Line61 our code works with code from outside the team that we can’t change. It might
Line62 be a public framework, such as a persistence mapper, or a library from another
Line63 team within our organization. The distinction is that integration tests make sure
Line64 that any abstractions we build over third-party code work as we expect. In a
Line65 small system, such as the one we develop in Part III, acceptance tests might be
Line66 enough. In most professional development, however, we’ll want integration tests
Line67 to help tease out conﬁguration issues with the external packages, and to give
Line68 quicker feedback than the (inevitably) slower acceptance tests.
Line69 We won’t write much more about techniques for acceptance and integration
Line70 testing, since both depend on the technologies involved and even the culture of
Line71 the organization. You’ll see some examples in Part III which we hope give a sense
Line72 of the motivation for acceptance tests and show how they ﬁt in the development
Line73 cycle. Unit testing techniques, however, are speciﬁc to a style of programming,
Line74 and so are common across all systems that take that approach—in our case, are
Line75 object-oriented.
Line76 External and Internal Quality
Line77 There’s another way of looking at what the tests can tell us about a system. We
Line78 can make a distinction between external and internal quality: External quality
Line79 is how well the system meets the needs of its customers and users (is it functional,
Line80 reliable, available, responsive, etc.), and internal quality is how well it meets the
Line81 needs of its developers and administrators (is it easy to understand, easy to change,
Line82 etc.). Everyone can understand the point of external quality; it’s usually part of
Line83 the contract to build. The case for internal quality is equally important but is
Line84 often harder to make. Internal quality is what lets us cope with continual and
Line85 unanticipated change which, as we saw at the beginning of this chapter, is a fact
Line86 of working with software. The point of maintaining internal quality is to allow
Line87 us to modify the system’s behavior safely and predictably, because it minimizes
Line88 the risk that a change will force major rework.
Line89 Chapter 1
Line90 What Is the Point of Test-Driven Development?
Line91 10
Line92 
Line93 
Line94 ---
