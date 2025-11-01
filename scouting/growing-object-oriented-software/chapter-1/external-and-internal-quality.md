Line1 # External and Internal Quality (pp.10-12)
Line2 
Line3 ---
Line4 **Page 10**
Line5 
Line6 There’s been a lot of discussion in the TDD world over the terminology for
Line7 what we’re calling acceptance tests: “functional tests,” “customer tests,” “system
Line8 tests.” Worse, our deﬁnitions are often not the same as those used by professional
Line9 software testers. The important thing is to be clear about our intentions. We use
Line10 “acceptance tests” to help us, with the domain experts, understand and agree on
Line11 what we are going to build next. We also use them to make sure that we haven’t
Line12 broken any existing features as we continue developing.
Line13 Our preferred implementation of the “role” of acceptance testing is to write
Line14 end-to-end tests which, as we just noted, should be as end-to-end as possible;
Line15 our bias often leads us to use these terms interchangeably although, in some
Line16 cases, acceptance tests might not be end-to-end.
Line17 We use the term integration tests to refer to the tests that check how some of
Line18 our code works with code from outside the team that we can’t change. It might
Line19 be a public framework, such as a persistence mapper, or a library from another
Line20 team within our organization. The distinction is that integration tests make sure
Line21 that any abstractions we build over third-party code work as we expect. In a
Line22 small system, such as the one we develop in Part III, acceptance tests might be
Line23 enough. In most professional development, however, we’ll want integration tests
Line24 to help tease out conﬁguration issues with the external packages, and to give
Line25 quicker feedback than the (inevitably) slower acceptance tests.
Line26 We won’t write much more about techniques for acceptance and integration
Line27 testing, since both depend on the technologies involved and even the culture of
Line28 the organization. You’ll see some examples in Part III which we hope give a sense
Line29 of the motivation for acceptance tests and show how they ﬁt in the development
Line30 cycle. Unit testing techniques, however, are speciﬁc to a style of programming,
Line31 and so are common across all systems that take that approach—in our case, are
Line32 object-oriented.
Line33 External and Internal Quality
Line34 There’s another way of looking at what the tests can tell us about a system. We
Line35 can make a distinction between external and internal quality: External quality
Line36 is how well the system meets the needs of its customers and users (is it functional,
Line37 reliable, available, responsive, etc.), and internal quality is how well it meets the
Line38 needs of its developers and administrators (is it easy to understand, easy to change,
Line39 etc.). Everyone can understand the point of external quality; it’s usually part of
Line40 the contract to build. The case for internal quality is equally important but is
Line41 often harder to make. Internal quality is what lets us cope with continual and
Line42 unanticipated change which, as we saw at the beginning of this chapter, is a fact
Line43 of working with software. The point of maintaining internal quality is to allow
Line44 us to modify the system’s behavior safely and predictably, because it minimizes
Line45 the risk that a change will force major rework.
Line46 Chapter 1
Line47 What Is the Point of Test-Driven Development?
Line48 10
Line49 
Line50 
Line51 ---
Line52 
Line53 ---
Line54 **Page 11**
Line55 
Line56 Running end-to-end tests tells us about the external quality of our system, and
Line57 writing them tells us something about how well we (the whole team) understand
Line58 the domain, but end-to-end tests don’t tell us how well we’ve written the code.
Line59 Writing unit tests gives us a lot of feedback about the quality of our code, and
Line60 running them tells us that we haven’t broken any classes—but, again, unit tests
Line61 don’t give us enough conﬁdence that the system as a whole works. Integration
Line62 tests fall somewhere in the middle, as in Figure 1.3.
Line63 Figure 1.3
Line64 Feedback from tests
Line65 Thorough unit testing helps us improve the internal quality because, to be
Line66 tested, a unit has to be structured to run outside the system in a test ﬁxture. A
Line67 unit test for an object needs to create the object, provide its dependencies, interact
Line68 with it, and check that it behaved as expected. So, for a class to be easy to unit-
Line69 test, the class must have explicit dependencies that can easily be substituted and
Line70 clear responsibilities that can easily be invoked and veriﬁed. In software engineer-
Line71 ing terms, that means that the code must be loosely coupled and highly
Line72 cohesive—in other words, well-designed.
Line73 When we’ve got this wrong—when a class, for example, is tightly coupled to
Line74 distant parts of the system, has implicit dependencies, or has too many or unclear
Line75 responsibilities—we ﬁnd unit tests difﬁcult to write or understand, so writing a
Line76 test ﬁrst gives us valuable, immediate feedback about our design. Like everyone,
Line77 we’re tempted not to write tests when our code makes it difﬁcult, but we try to
Line78 resist. We use such difﬁculties as an opportunity to investigate why the test is
Line79 hard to write and refactor the code to improve its structure. We call this “listening
Line80 to the tests,” and we’ll work through some common patterns in Chapter 20.
Line81 11
Line82 External and Internal Quality
Line83 
Line84 
Line85 ---
Line86 
Line87 ---
Line88 **Page 12**
Line89 
Line90 Coupling and Cohesion
Line91 Coupling and cohesion are metrics that (roughly) describe how easy it will be to
Line92 change the behavior of some code.They were described by Larry Constantine in
Line93 [Yourdon79].
Line94 Elements are coupled if a change in one forces a change in the other. For example,
Line95 if two classes inherit from a common parent, then a change in one class might
Line96 require a change in the other. Think of a combo audio system: It’s tightly coupled
Line97 because if we want to change from analog to digital radio, we must rebuild the
Line98 whole system. If we assemble a system from separates, it would have low coupling
Line99 and we could just swap out the receiver. “Loosely” coupled features (i.e., those
Line100 with low coupling) are easier to maintain.
Line101 An element’s cohesion is a measure of whether its responsibilities form a mean-
Line102 ingful unit. For example, a class that parses both dates and URLs is not coherent,
Line103 because they’re unrelated concepts.Think of a machine that washes both clothes
Line104 and dishes—it’s unlikely to do both well.2 At the other extreme, a class that parses
Line105 only the punctuation in a URL is unlikely to be coherent, because it doesn’t repre-
Line106 sent a whole concept. To get anything done, the programmer will have to ﬁnd
Line107 other parsers for protocol, host, resource, and so on. Features with “high”
Line108 coherence are easier to maintain.
Line109 2. Actually, there was a combined clothes and dishwasher.The “Thor Automagic” was
Line110 manufactured in the 1940s, but the idea hasn’t survived.
Line111 Chapter 1
Line112 What Is the Point of Test-Driven Development?
Line113 12
