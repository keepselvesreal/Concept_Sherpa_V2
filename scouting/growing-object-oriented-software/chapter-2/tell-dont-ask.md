Line1 # Tell, Don't Ask (pp.17-17)
Line2 
Line3 ---
Line4 **Page 17**
Line5 
Line6 Tell, Don’t Ask
Line7 We have objects sending each other messages, so what do they say? Our experi-
Line8 ence is that the calling object should describe what it wants in terms of the role
Line9 that its neighbor plays, and let the called object decide how to make that happen.
Line10 This is commonly known as the “Tell, Don’t Ask” style or, more formally, the
Line11 Law of Demeter. Objects make their decisions based only on the information
Line12 they hold internally or that which came with the triggering message; they avoid
Line13 navigating to other objects to make things happen. Followed consistently, this
Line14 style produces more ﬂexible code because it’s easy to swap objects that play the
Line15 same role. The caller sees nothing of their internal structure or the structure of
Line16 the rest of the system behind the role interface.
Line17 When we don’t follow the style, we can end up with what’s known as “train
Line18 wreck” code, where a series of getters is chained together like the carriages in a
Line19 train. Here’s one case we found on the Internet:
Line20 ((EditSaveCustomizer) master.getModelisable()
Line21   .getDockablePanel()
Line22     .getCustomizer())
Line23       .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
Line24 After some head scratching, we realized what this fragment was meant to say:
Line25 master.allowSavingOfCustomisations();
Line26 This wraps all that implementation detail up behind a single call. The client of
Line27 master no longer needs to know anything about the types in the chain. We’ve
Line28 reduced the risk that a design change might cause ripples in remote parts of the
Line29 codebase.
Line30 As well as hiding information, there’s a more subtle beneﬁt from “Tell, Don’t
Line31 Ask.” It forces us to make explicit and so name the interactions between objects,
Line32 rather than leaving them implicit in the chain of getters. The shorter version
Line33 above is much clearer about what it’s for, not just how it happens to be
Line34 implemented.
Line35 But Sometimes Ask
Line36 Of course we don’t “tell” everything;1 we “ask” when getting information from
Line37 values and collections, or when using a factory to create new objects. Occasion-
Line38 ally, we also ask objects about their state when searching or ﬁltering, but we still
Line39 want to maintain expressiveness and avoid “train wrecks.”
Line40 For example (to continue with the metaphor), if we naively wanted to spread
Line41 reserved seats out across the whole of a train, we might start with something like:
Line42 1. Although that’s an interesting exercise to try, to stretch your technique.
Line43 17
Line44 But Sometimes Ask
Line45 
Line46 
Line47 ---
