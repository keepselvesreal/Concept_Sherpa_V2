Line1 # Emergent Design (pp.137-138)
Line2 
Line3 ---
Line4 **Page 137**
Line5 
Line6 Emergent Design
Line7 What we hope is becoming clear from this chapter is how we’re growing a design
Line8 from what looks like an unpromising start. We alternate, more or less, between
Line9 adding features and reﬂecting on—and cleaning up—the code that results. The
Line10 cleaning up stage is essential, since without it we would end up with an unmain-
Line11 tainable mess. We’re prepared to defer refactoring code if we’re not yet clear
Line12 what to do, conﬁdent that we will take the time when we’re ready. In the mean-
Line13 time, we keep our code as clean as possible, moving in small increments and using
Line14 techniques such as null implementation to minimize the time when it’s broken.
Line15 Figure 13.5 shows that we’re building up a layer around our core implementa-
Line16 tion that “protects” it from its external dependencies. We think this is just good
Line17 practice, but what’s interesting is that we’re getting there incrementally, by
Line18 looking for features in classes that either go together or don’t. Of course we’re
Line19 inﬂuenced by our experience of working on similar codebases, but we’re trying
Line20 hard to follow what the code is telling us instead of imposing our preconceptions.
Line21 Sometimes, when we do this, we ﬁnd that the domain takes us in the most
Line22 surprising directions.
Line23 137
Line24 Emergent Design
Line25 
Line26 
Line27 ---
Line28 
Line29 ---
Line30 **Page 138**
Line31 
Line32 This page intentionally left blank
