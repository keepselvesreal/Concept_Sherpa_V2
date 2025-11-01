Line1 # Tuning the Cycle (pp.45-46)
Line2 
Line3 ---
Line4 **Page 45**
Line5 
Line6 Figure 5.3
Line7 Difﬁculties writing tests may suggest a need to ﬁx
Line8 production code
Line9 This is an example of how our maxim—“Expect Unexpected Changes”—guides
Line10 development. If we keep up the quality of the system by refactoring when we see
Line11 a weakness in the design, we will be able to make it respond to whatever changes
Line12 turn up. The alternative is the usual “software rot” where the code decays until
Line13 the team just cannot respond to the needs of its customers. We’ll return to this
Line14 topic in Chapter 20.
Line15 Tuning the Cycle
Line16 There’s a balance between exhaustively testing execution paths and testing inte-
Line17 gration. If we test at too large a grain, the combinatorial explosion of trying all
Line18 the possible paths through the code will bring development to a halt. Worse,
Line19 some of those paths, such as throwing obscure exceptions, will be impractical to
Line20 test from that level. On the other hand, if we test at too ﬁne a grain—just at the
Line21 class level, for example—the testing will be easier but we’ll miss problems that
Line22 arise from objects not working together.
Line23 How much unit testing should we do, using mock objects to break external
Line24 dependencies, and how much integration testing? We don’t think there’s a single
Line25 answer to this question. It depends too much on the context of the team and its
Line26 environment. The best we can get from the testing part of TDD (which is a lot)
Line27 is the conﬁdence that we can change the code without breaking it: Fear kills
Line28 progress. The trick is to make sure that the conﬁdence is justiﬁed.
Line29 So, we regularly reﬂect on how well TDD is working for us, identify any
Line30 weaknesses, and adapt our testing strategy. Fiddly bits of logic might need more
Line31 unit testing (or, alternatively, simpliﬁcation); unhandled exceptions might need
Line32 more integration-level testing; and, unexpected system failures will need more
Line33 investigation and, possibly, more testing throughout.
Line34 45
Line35 Tuning the Cycle
Line36 
Line37 
Line38 ---
Line39 
Line40 ---
Line41 **Page 46**
Line42 
Line43 This page intentionally left blank
