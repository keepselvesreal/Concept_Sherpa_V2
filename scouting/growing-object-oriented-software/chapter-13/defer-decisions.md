Line1 # Defer Decisions (pp.136-137)
Line2 
Line3 ---
Line4 **Page 136**
Line5 
Line6 This is an example of “breaking out” that we described in “Value Types”
Line7 (page 59). It may not be obvious, but AuctionEvent is a value: it’s
Line8 immutable and there are no interesting differences between two instances
Line9 with the same contents. This refactoring separates the concerns within
Line10 AuctionMessageTranslator: the top level deals with events and listeners, and
Line11 the inner object deals with parsing strings.
Line12 Encapsulate Collections
Line13 We’ve developed a habit of packaging up common types, such as collections, in
Line14 our own classes, even though Java generics avoid the need to cast objects. We’re
Line15 trying to use the language of the problem we’re working on, rather than the language
Line16 of Java constructs. In our two versions of processMessage(), the ﬁrst has lots of
Line17 incidental noise about looking up and parsing values.The second is written in terms
Line18 of auction events, so there’s less of a conceptual gap between the domain and
Line19 the code.
Line20 Our rule of thumb is that we try to limit passing around types with generics (the
Line21 types enclosed in angle brackets). Particularly when applied to collections, we view
Line22 it as a form of duplication. It’s a hint that there’s a domain concept that should be
Line23 extracted into a type.
Line24 Defer Decisions
Line25 There’s a technique we’ve used a couple of times now, which is to introduce a
Line26 null implementation of a method (or even a type) to get us through the next step.
Line27 This helps us focus on the immediate task without getting dragged into thinking
Line28 about the next signiﬁcant chunk of functionality. The null Auction, for example,
Line29 allowed us to plug in a new relationship we’d discovered in a unit test without
Line30 getting pulled into messaging issues. That, in turn, meant we could stop and
Line31 think about the dependencies between our objects without the pressure of having
Line32 a broken compilation.
Line33 Keep the Code Compiling
Line34 We try to minimize the time when we have code that does not compile by keeping
Line35 changes incremental. When we have compilation failures, we can’t be quite sure
Line36 where the boundaries of our changes are, since the compiler can’t tell us. This, in
Line37 turn, means that we can’t check in to our source repository, which we like to do
Line38 often.The more code we have open, the more we have to keep in our heads which,
Line39 ironically, usually means we move more slowly. One of the great discoveries of
Line40 test-driven development is just how ﬁne-grained our development steps can be.
Line41 Chapter 13
Line42 The Sniper Makes a Bid
Line43 136
Line44 
Line45 
Line46 ---
Line47 
Line48 ---
Line49 **Page 137**
Line50 
Line51 Emergent Design
Line52 What we hope is becoming clear from this chapter is how we’re growing a design
Line53 from what looks like an unpromising start. We alternate, more or less, between
Line54 adding features and reﬂecting on—and cleaning up—the code that results. The
Line55 cleaning up stage is essential, since without it we would end up with an unmain-
Line56 tainable mess. We’re prepared to defer refactoring code if we’re not yet clear
Line57 what to do, conﬁdent that we will take the time when we’re ready. In the mean-
Line58 time, we keep our code as clean as possible, moving in small increments and using
Line59 techniques such as null implementation to minimize the time when it’s broken.
Line60 Figure 13.5 shows that we’re building up a layer around our core implementa-
Line61 tion that “protects” it from its external dependencies. We think this is just good
Line62 practice, but what’s interesting is that we’re getting there incrementally, by
Line63 looking for features in classes that either go together or don’t. Of course we’re
Line64 inﬂuenced by our experience of working on similar codebases, but we’re trying
Line65 hard to follow what the code is telling us instead of imposing our preconceptions.
Line66 Sometimes, when we do this, we ﬁnd that the domain takes us in the most
Line67 surprising directions.
Line68 137
Line69 Emergent Design
Line70 
Line71 
Line72 ---
