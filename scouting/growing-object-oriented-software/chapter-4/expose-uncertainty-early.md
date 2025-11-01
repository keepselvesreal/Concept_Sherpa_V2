Line1 # Expose Uncertainty Early (pp.36-38)
Line2 
Line3 ---
Line4 **Page 36**
Line5 
Line6 We use the automation of building and testing to give us feedback on qualities
Line7 of the system, such as how easily we can cut a version and deploy, how well the
Line8 design works, and how good the code is. The automated deployment helps us
Line9 release frequently to real users, which gives us feedback on how well we have
Line10 understood the domain and whether seeing the system in practice has changed
Line11 our customer’s priorities.
Line12 The great beneﬁt is that we will be able to make changes in response to what-
Line13 ever we learn, because writing everything test-ﬁrst means that we will have a
Line14 thorough set of regression tests. No tests are perfect, of course, but in practice
Line15 we’ve found that a substantial test suite allows us to make major changes safely.
Line16 Expose Uncertainty Early
Line17 All this effort means that teams are frequently surprised by the time it takes to
Line18 get a “walking skeleton” working, considering that it does hardly anything.
Line19 That’s because this ﬁrst step involves establishing a lot of infrastructure and
Line20 asking (and answering) many awkward questions. The time to implement the
Line21 ﬁrst few features will be unpredictable as the team discovers more about its re-
Line22 quirements and target environment. For a new team, this will be compounded
Line23 by the social stresses of learning how to work together.
Line24 Fred Tingey, a colleague, once observed that incremental development can be
Line25 disconcerting for teams and management who aren’t used to it because it front-
Line26 loads the stress in a project. Projects with late integration start calmly but gener-
Line27 ally turn difﬁcult towards the end as the team tries to pull the system together
Line28 for the ﬁrst time. Late integration is unpredictable because the team has to
Line29 assemble a great many moving parts with limited time and budget to ﬁx any
Line30 failures. The result is that experienced stakeholders react badly to the instability
Line31 at the start of an incremental project because they expect that the end of the
Line32 project will be much worse.
Line33 Our experience is that a well-run incremental development runs in the opposite
Line34 direction. It starts unsettled but then, after a few features have been implemented
Line35 and the project automation has been built up, settles in to a routine. As a project
Line36 approaches delivery, the end-game should be a steady production of functionality,
Line37 perhaps with a burst of activity before the ﬁrst release. All the mundane but
Line38 brittle tasks, such as deployment and upgrades, will have been automated so that
Line39 they “just work.” The contrast looks rather like Figure 4.4.
Line40 This aspect of test-driven development, like others, may appear counter-
Line41 intuitive, but we’ve always found it worth taking enough time to structure and
Line42 automate the basics of the system—or at least a ﬁrst cut. Of course, we don’t
Line43 want to spend the whole project setting up a perfect “walking skeleton,” so we
Line44 limit ourselves to whiteboard-level decisions and reserve the right to change our
Line45 mind when we have to. But the most important thing is to have a sense of direction
Line46 and a concrete implementation to test our assumptions.
Line47 Chapter 4
Line48 Kick-Starting the Test-Driven Cycle
Line49 36
Line50 
Line51 
Line52 ---
Line53 
Line54 ---
Line55 **Page 37**
Line56 
Line57 Figure 4.4
Line58 Visible uncertainty in test-ﬁrst and test-later projects
Line59 A “walking skeleton” will ﬂush out issues early in the project when there’s
Line60 still time, budget, and goodwill to address them.
Line61 Brownﬁeld Development
Line62 We don’t always have the luxury of building a new system from the ground up.
Line63 Many of our projects have started with an existing system that must be extended,
Line64 adapted, or replaced. In such cases, we can’t start by building a “walking skeleton”;
Line65 we have to work with what already exists, no matter how hostile its structure.
Line66 That said, the process of kick-starting TDD of an existing system is not fundamen-
Line67 tally different from applying it to a new system—although it may be orders of
Line68 magnitude more difﬁcult because of the technical baggage the system already
Line69 carries. Michael Feathers has written a whole book on the topic, [Feathers04].
Line70 It is risky to start reworking a system when there are no tests to detect regressions.
Line71 The safest way to start the TDD process is to automate the build and deploy pro-
Line72 cess, and then add end-to-end tests that cover the areas of the code we need to
Line73 change. With that protection, we can start to address internal quality issues with
Line74 more conﬁdence, refactoring the code and introducing unit tests as we add func-
Line75 tionality.
Line76 The easiest way to start building an end-to-end test infrastructure is with the sim-
Line77 plest path through the system that we can ﬁnd. Like a “walking skeleton,” this lets
Line78 us build up some supporting infrastructure before we tackle the harder problems
Line79 of testing more complicated functionality.
Line80 37
Line81 Expose Uncertainty Early
Line82 
Line83 
Line84 ---
Line85 
Line86 ---
Line87 **Page 38**
Line88 
Line89 This page intentionally left blank
