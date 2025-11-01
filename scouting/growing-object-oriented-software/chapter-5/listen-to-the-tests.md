Line1 # Listen to the Tests (pp.44-45)
Line2 
Line3 ---
Line4 **Page 44**
Line5 
Line6 The Importance of Describing Behavior, Not API Features
Line7 Nat used to run a company that produced online advertising and branded content
Line8 for clients sponsoring sports teams. One of his clients sponsored a Formula One
Line9 racing team. Nat wrote a fun little game that simulated Formula One race strategies
Line10 for the client to put on the team’s website. It took him two weeks to write, from
Line11 initial idea to ﬁnal deliverable, and once he handed it over to the client he forgot
Line12 all about it.
Line13 It turned out, however, that the throw-away game was by far the most popular
Line14 content on the team’s website. For the next F1 season, the client wanted to capi-
Line15 talize on its success. They wanted the game to model the track of each Grand
Line16 Prix, to accommodate the latest F1 rules, to have a better model of car physics,
Line17 to simulate dynamic weather, overtaking, spin-outs, and more.
Line18 Nat had written the original version test-ﬁrst, so he expected it to be easy to
Line19 change. However, going back to the code, he found the tests very hard to under-
Line20 stand. He had written a test for each method of each object but couldn’t understand
Line21 from those tests how each object was meant to behave—what the responsibilities
Line22 of the object were and how the different methods of the object worked together.
Line23 It helps to choose test names that describe how the object behaves in the
Line24 scenario being tested. We look at this in more detail in “Test Names Describe
Line25 Features” (page 248).
Line26 Listen to the Tests
Line27 When writing unit and integration tests, we stay alert for areas of the code that
Line28 are difﬁcult to test. When we ﬁnd a feature that’s difﬁcult to test, we don’t just
Line29 ask ourselves how to test it, but also why is it difﬁcult to test.
Line30 Our experience is that, when code is difﬁcult to test, the most likely cause is
Line31 that our design needs improving. The same structure that makes the code difﬁcult
Line32 to test now will make it difﬁcult to change in the future. By the time that future
Line33 comes around, a change will be more difﬁcult still because we’ll have forgotten
Line34 what we were thinking when we wrote the code. For a successful system, it might
Line35 even be a completely different team that will have to live with the consequences
Line36 of our decisions.
Line37 Our response is to regard the process of writing tests as a valuable early
Line38 warning of potential maintenance problems and to use those hints to ﬁx a problem
Line39 while it’s still fresh. As Figure 5.3 shows, if we’re ﬁnding it hard to write the next
Line40 failing test, we look again at the design of the production code and often refactor
Line41 it before moving on.
Line42 Chapter 5
Line43 Maintaining the Test-Driven Cycle
Line44 44
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 45**
Line51 
Line52 Figure 5.3
Line53 Difﬁculties writing tests may suggest a need to ﬁx
Line54 production code
Line55 This is an example of how our maxim—“Expect Unexpected Changes”—guides
Line56 development. If we keep up the quality of the system by refactoring when we see
Line57 a weakness in the design, we will be able to make it respond to whatever changes
Line58 turn up. The alternative is the usual “software rot” where the code decays until
Line59 the team just cannot respond to the needs of its customers. We’ll return to this
Line60 topic in Chapter 20.
Line61 Tuning the Cycle
Line62 There’s a balance between exhaustively testing execution paths and testing inte-
Line63 gration. If we test at too large a grain, the combinatorial explosion of trying all
Line64 the possible paths through the code will bring development to a halt. Worse,
Line65 some of those paths, such as throwing obscure exceptions, will be impractical to
Line66 test from that level. On the other hand, if we test at too ﬁne a grain—just at the
Line67 class level, for example—the testing will be easier but we’ll miss problems that
Line68 arise from objects not working together.
Line69 How much unit testing should we do, using mock objects to break external
Line70 dependencies, and how much integration testing? We don’t think there’s a single
Line71 answer to this question. It depends too much on the context of the team and its
Line72 environment. The best we can get from the testing part of TDD (which is a lot)
Line73 is the conﬁdence that we can change the code without breaking it: Fear kills
Line74 progress. The trick is to make sure that the conﬁdence is justiﬁed.
Line75 So, we regularly reﬂect on how well TDD is working for us, identify any
Line76 weaknesses, and adapt our testing strategy. Fiddly bits of logic might need more
Line77 unit testing (or, alternatively, simpliﬁcation); unhandled exceptions might need
Line78 more integration-level testing; and, unexpected system failures will need more
Line79 investigation and, possibly, more testing throughout.
Line80 45
Line81 Tuning the Cycle
Line82 
Line83 
Line84 ---
