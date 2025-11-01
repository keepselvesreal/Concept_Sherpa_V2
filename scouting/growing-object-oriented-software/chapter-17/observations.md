Line1 # Observations (pp.201-204)
Line2 
Line3 ---
Line4 **Page 201**
Line5 
Line6 Now that we’ve cleaned up, we can cross the next item off our list: Figure 17.4.
Line7 Figure 17.4
Line8 Adding items through the user interface
Line9 Observations
Line10 Incremental Architecture
Line11 This restructuring of Main is a key moment in the development of the application.
Line12 As Figure 17.5 shows, we now have a structure that matches the “ports and
Line13 adapters” architecture we described in “Designing for Maintainability” (page 47).
Line14 There is core domain code (for example, AuctionSniper) which depends on
Line15 bridging code (for example, SnipersTableModel) that drives or responds to
Line16 technical code (for example, JTable). We’ve kept the domain code free of any
Line17 reference to the external infrastructure. The contents of our auctionsniper
Line18 package deﬁne a model of our auction sniping business, using a self-contained
Line19 language. The exception is Main, which is our entry point and binds the domain
Line20 model and infrastructure together.
Line21 What’s important for the purposes of this example, is that we arrived at this
Line22 design incrementally, by adding features and repeatedly following heuristics.
Line23 Although we rely on our experience to guide our decisions, we reached this
Line24 solution almost automatically by just following the code and taking care to keep
Line25 it clean.
Line26 201
Line27 Observations
Line28 
Line29 
Line30 ---
Line31 
Line32 ---
Line33 **Page 202**
Line34 
Line35 Figure 17.5
Line36 The application now has a “ports and adapters”
Line37 architecture
Line38 Three-Point Contact
Line39 We wrote this refactoring up in detail because we wanted to make some points
Line40 along the way and to show that we can do signiﬁcant refactorings incrementally.
Line41 When we’re not sure what to do next or how to get there from here, one way of
Line42 coping is to scale down the individual changes we make, as Kent Beck showed
Line43 in [Beck02]. By repeatedly ﬁxing local problems in the code, we ﬁnd we can ex-
Line44 plore the design safely, never straying more than a few minutes from working
Line45 code. Usually this is enough to lead us towards a better design, and we can always
Line46 backtrack and take another path if it doesn’t work out.
Line47 One way to think of this is the rock climbing rule of “three-point contact.”
Line48 Trained climbers only move one limb at a time (a hand or a foot), to minimize
Line49 the risk of falling off. Each move is minimal and safe, but combining enough of
Line50 them will get you to the top of the route.
Line51 In “elapsed time,” this refactoring didn’t take much longer than the time you
Line52 spent reading it, which we think is a good return for the clearer separation of
Line53 concerns. With experience, we’ve learned to recognize fault lines in code so we
Line54 can often take a more direct route.
Line55 Chapter 17
Line56 Teasing Apart Main
Line57 202
Line58 
Line59 
Line60 ---
Line61 
Line62 ---
Line63 **Page 203**
Line64 
Line65 Dynamic as Well as Static Design
Line66 We did encounter one small bump whilst working on the code for this chapter.
Line67 Steve was extracting the SniperPortfolio and got stuck trying to ensure that the
Line68 sniperAdded() method was called within the Swing thread. Eventually he remem-
Line69 bered that the event is triggered by a button click anyway, so he was already
Line70 covered.
Line71 What we learn from this (apart from the need for pairing while writing book
Line72 examples) is that we should consider more than one view when refactoring code.
Line73 Refactoring is, after all, a design activity, which means we still need all the skills
Line74 we were taught—except that now we need them all the time rather than periodi-
Line75 cally. Refactoring is so focused on static structure (classes and interfaces) that
Line76 it’s easy to lose sight of an application’s dynamic structure (instances and threads).
Line77 Sometimes we just need to step back and draw out, say, an interaction diagram
Line78 like Figure 17.6:
Line79 Figure 17.6
Line80 An Interaction Diagram
Line81 An Alternative Fix to notToBeGCd
Line82 Our chosen ﬁx relies on the SniperPortfolio holding onto the reference. That’s
Line83 likely to be the case in practice, but if it ever changes we will get transient failures
Line84 that are hard to track down. We’re relying on a side effect of the application to
Line85 ﬁx an issue in the XMPP code.
Line86 An alternative would be to say that it’s a Smack problem, so our XMPP layer
Line87 should deal with it. We could make the XMPPAuctionHouse hang on to the
Line88 XMPPAuctions it creates, in which case we’d to have to add a lifecycle listener of
Line89 some sort to tell us when we’re ﬁnished with an Auction and can release it. There
Line90 is no obvious choice here; we just have to look at the circumstances and exercise
Line91 some judgment.
Line92 203
Line93 Observations
Line94 
Line95 
Line96 ---
Line97 
Line98 ---
Line99 **Page 204**
Line100 
Line101 This page intentionally left blank
