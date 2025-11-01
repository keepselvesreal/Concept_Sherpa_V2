Line1 # Deciding the Shape of the Walking Skeleton (pp.33-35)
Line2 
Line3 ---
Line4 **Page 33**
Line5 
Line6 a dummy server, not the real site. At some point before going live, we would
Line7 have had to test against Southabee’s On-Line; the earlier we can do that, the
Line8 easier it will be for us to respond to any surprises that turn up.
Line9 Whilst building the “walking skeleton,” we concentrate on the structure and
Line10 don’t worry too much about cleaning up the test to be beautifully expressive.
Line11 The walking skeleton and its supporting infrastructure are there to help us work
Line12 out how to start test-driven development. It’s only the ﬁrst step toward a complete
Line13 end-to-end acceptance-testing solution. When we write the test for the ﬁrst feature,
Line14 then we need to “write the test you want to read” (page 42) to make sure that
Line15 it’s a clear expression of the behavior of the system.
Line16 The Importance of Early End-to-End Testing
Line17 We joined a project that had been running for a couple of years but had never
Line18 tested their entire system end-to-end. There were frequent production outages
Line19 and deployments often failed. The system was large and complex, reﬂecting the
Line20 complicated business transactions it managed.The effort of building an automated,
Line21 end-to-end test suite was so large that an entire new team had to be formed to
Line22 perform the work. It took them months to build an end-to-end test environment,
Line23 and they never managed to get the entire system covered by an end-to-end
Line24 test suite.
Line25 Because the need for end-to-end testing had not inﬂuenced its design, the system
Line26 was difﬁcult to test. For example, the system’s components used internal timers
Line27 to schedule activities, some of them days or weeks into the future. This made it
Line28 very difﬁcult to write end-to-end tests: It was impractical to run the tests in real-
Line29 time but the scheduling could not be inﬂuenced from outside the system. The
Line30 developers had to redesign the system itself so that periodic activities were trig-
Line31 gered by messages sent from a remote scheduler which could be replaced in the
Line32 test environment; see “Externalize Event Sources” (page 326).This was a signiﬁ-
Line33 cant architectural change—and it was very risky because it had to be performed
Line34 without end-to-end test coverage.
Line35 Deciding the Shape of the Walking Skeleton
Line36 The development of a “walking skeleton” is the moment when we start to make
Line37 choices about the high-level structure of our application. We can’t automate the
Line38 build, deploy, and test cycle without some idea of the overall structure. We don’t
Line39 need much detail yet, just a broad-brush picture of what major system components
Line40 will be needed to support the ﬁrst planned release and how they will communicate.
Line41 Our rule of thumb is that we should be able to draw the design for the “walking
Line42 skeleton” in a few minutes on a whiteboard.
Line43 33
Line44 Deciding the Shape of the Walking Skeleton
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 34**
Line51 
Line52 Mappa Mundi
Line53 We ﬁnd that maintaining a public drawing of the structure of the system, for example
Line54 on the wall in the team’s work area as in Figure 4.1, helps the team stay oriented
Line55 when working on the code.
Line56 Figure 4.1
Line57 A broad-brush architecture diagram drawn on the
Line58 wall of a team’s work area
Line59 To design this initial structure, we have to have some understanding of the
Line60 purpose of the system, otherwise the whole exercise risks being meaningless. We
Line61 need a high-level view of the client’s requirements, both functional and non-
Line62 functional, to guide our choices. This preparatory work is part of the chartering
Line63 of the project, which we must leave as outside the scope of this book.
Line64 The point of the “walking skeleton” is to use the writing of the ﬁrst test to
Line65 draw out the context of the project, to help the team map out the landscape of
Line66 their solution—the essential decisions that they must take before they can write
Line67 any code; Figure 4.2 shows how the TDD process we drew in Figure 1.2 ﬁts into
Line68 this context.
Line69 Chapter 4
Line70 Kick-Starting the Test-Driven Cycle
Line71 34
Line72 
Line73 
Line74 ---
Line75 
Line76 ---
Line77 **Page 35**
Line78 
Line79 Figure 4.2
Line80 The context of the ﬁrst test
Line81 Please don’t confuse this with doing “Big Design Up Front” (BDUF) which
Line82 has such a bad reputation in the Agile Development community. We’re not trying
Line83 to elaborate the whole design down to classes and algorithms before we start
Line84 coding. Any ideas we have now are likely to be wrong, so we prefer to discover
Line85 those details as we grow the system. We’re making the smallest number of
Line86 decisions we can to kick-start the TDD cycle, to allow us to start learning and
Line87 improving from real feedback.
Line88 Build Sources of Feedback
Line89 We have no guarantees that the decisions we’ve taken about the design of our
Line90 application, or the assumptions on which they’re based, are right. We do the best
Line91 we can, but the only thing we can rely on is validating them as soon as possible
Line92 by building feedback into our process. The tools we build to implement the
Line93 “walking skeleton” are there to support this learning process. Of course, these
Line94 tools too will not be perfect, and we expect we will improve them incrementally
Line95 as we learn how well they support the team.
Line96 Our ideal situation is where the team releases regularly to a real production
Line97 system, as in Figure 4.3. This allows the system’s stakeholders to respond to how
Line98 well the system meets their needs, at the same time allowing us to judge its
Line99 implementation.
Line100 Figure 4.3
Line101 Requirements feedback
Line102 35
Line103 Build Sources of Feedback
Line104 
Line105 
Line106 ---
