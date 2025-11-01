Line1 # Build Sources of Feedback (pp.35-36)
Line2 
Line3 ---
Line4 **Page 35**
Line5 
Line6 Figure 4.2
Line7 The context of the ﬁrst test
Line8 Please don’t confuse this with doing “Big Design Up Front” (BDUF) which
Line9 has such a bad reputation in the Agile Development community. We’re not trying
Line10 to elaborate the whole design down to classes and algorithms before we start
Line11 coding. Any ideas we have now are likely to be wrong, so we prefer to discover
Line12 those details as we grow the system. We’re making the smallest number of
Line13 decisions we can to kick-start the TDD cycle, to allow us to start learning and
Line14 improving from real feedback.
Line15 Build Sources of Feedback
Line16 We have no guarantees that the decisions we’ve taken about the design of our
Line17 application, or the assumptions on which they’re based, are right. We do the best
Line18 we can, but the only thing we can rely on is validating them as soon as possible
Line19 by building feedback into our process. The tools we build to implement the
Line20 “walking skeleton” are there to support this learning process. Of course, these
Line21 tools too will not be perfect, and we expect we will improve them incrementally
Line22 as we learn how well they support the team.
Line23 Our ideal situation is where the team releases regularly to a real production
Line24 system, as in Figure 4.3. This allows the system’s stakeholders to respond to how
Line25 well the system meets their needs, at the same time allowing us to judge its
Line26 implementation.
Line27 Figure 4.3
Line28 Requirements feedback
Line29 35
Line30 Build Sources of Feedback
Line31 
Line32 
Line33 ---
Line34 
Line35 ---
Line36 **Page 36**
Line37 
Line38 We use the automation of building and testing to give us feedback on qualities
Line39 of the system, such as how easily we can cut a version and deploy, how well the
Line40 design works, and how good the code is. The automated deployment helps us
Line41 release frequently to real users, which gives us feedback on how well we have
Line42 understood the domain and whether seeing the system in practice has changed
Line43 our customer’s priorities.
Line44 The great beneﬁt is that we will be able to make changes in response to what-
Line45 ever we learn, because writing everything test-ﬁrst means that we will have a
Line46 thorough set of regression tests. No tests are perfect, of course, but in practice
Line47 we’ve found that a substantial test suite allows us to make major changes safely.
Line48 Expose Uncertainty Early
Line49 All this effort means that teams are frequently surprised by the time it takes to
Line50 get a “walking skeleton” working, considering that it does hardly anything.
Line51 That’s because this ﬁrst step involves establishing a lot of infrastructure and
Line52 asking (and answering) many awkward questions. The time to implement the
Line53 ﬁrst few features will be unpredictable as the team discovers more about its re-
Line54 quirements and target environment. For a new team, this will be compounded
Line55 by the social stresses of learning how to work together.
Line56 Fred Tingey, a colleague, once observed that incremental development can be
Line57 disconcerting for teams and management who aren’t used to it because it front-
Line58 loads the stress in a project. Projects with late integration start calmly but gener-
Line59 ally turn difﬁcult towards the end as the team tries to pull the system together
Line60 for the ﬁrst time. Late integration is unpredictable because the team has to
Line61 assemble a great many moving parts with limited time and budget to ﬁx any
Line62 failures. The result is that experienced stakeholders react badly to the instability
Line63 at the start of an incremental project because they expect that the end of the
Line64 project will be much worse.
Line65 Our experience is that a well-run incremental development runs in the opposite
Line66 direction. It starts unsettled but then, after a few features have been implemented
Line67 and the project automation has been built up, settles in to a routine. As a project
Line68 approaches delivery, the end-game should be a steady production of functionality,
Line69 perhaps with a burst of activity before the ﬁrst release. All the mundane but
Line70 brittle tasks, such as deployment and upgrades, will have been automated so that
Line71 they “just work.” The contrast looks rather like Figure 4.4.
Line72 This aspect of test-driven development, like others, may appear counter-
Line73 intuitive, but we’ve always found it worth taking enough time to structure and
Line74 automate the basics of the system—or at least a ﬁrst cut. Of course, we don’t
Line75 want to spend the whole project setting up a perfect “walking skeleton,” so we
Line76 limit ourselves to whiteboard-level decisions and reserve the right to change our
Line77 mind when we have to. But the most important thing is to have a sense of direction
Line78 and a concrete implementation to test our assumptions.
Line79 Chapter 4
Line80 Kick-Starting the Test-Driven Cycle
Line81 36
Line82 
Line83 
Line84 ---
