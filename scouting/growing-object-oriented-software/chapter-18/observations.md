Line1 # Observations (pp.212-214)
Line2 
Line3 ---
Line4 **Page 212**
Line5 
Line6 Figure 18.3
Line7 The Sniper stops bidding at the stop price
Line8 Observations
Line9 User Interfaces, Incrementally
Line10 It looks like we’re making signiﬁcant changes again to the user interface at a late
Line11 stage in our development. Shouldn’t we have seen this coming? This is an active
Line12 topic for discussion in the Agile User Experience community and, as always, the
Line13 answer is “it depends, but you have more ﬂexibility than you might think.”
Line14 In truth, for a simple application like this it would make sense to work out the
Line15 user interface in more detail at the start, to make sure it’s usable and coherent.
Line16 That said, we also wanted to make a point that we can respond to changing
Line17 needs, especially if we structure our tests and code so that they’re ﬂexible, not a
Line18 dead weight. We all know that requirements will change, especially once we put
Line19 our application into production, so we should be able to respond.
Line20 Other Modeling Techniques Still Work
Line21 Some presentations of TDD appear to suggest that it supersedes all previous
Line22 software design techniques. We think TDD works best when it’s based on skill
Line23 and judgment acquired from as wide an experience as possible—which includes
Line24 taking advantage of older techniques and formats (we hope we’re not being too
Line25 controversial here).
Line26 State transition diagrams are one example of taking another view. We regularly
Line27 come across teams that have never quite ﬁgured out what the valid states and
Line28 transitions are for key concepts in their domain, and applying this simple
Line29 Chapter 18
Line30 Filling In the Details
Line31 212
Line32 
Line33 
Line34 ---
Line35 
Line36 ---
Line37 **Page 213**
Line38 
Line39 formalism often means we can clean up a lucky-dip of snippets of behavior
Line40 scattered across the code. What’s nice about state transitions diagrams is that
Line41 they map directly onto tests, so we can show that we’ve covered all the
Line42 possibilities.
Line43 The trick is to understand and use other modeling techniques for support and
Line44 guidance, not as an end in themselves—which is how they got a bad name in the
Line45 ﬁrst place. When we’re doing TDD and we’re uncertain what to do, sometimes
Line46 stepping back and opening a pack of index cards, or sketching out the interactions,
Line47 can help us regain direction.
Line48 Domain Types Are Better Than Strings
Line49 The string is a stark data structure and everywhere it is passed there
Line50 is much duplication of process. It is a perfect vehicle for hiding
Line51 information.
Line52 —Alan Perlis
Line53 Looking back, we wish we’d created the Item type earlier, probably when we
Line54 extracted UserRequestListener, instead of just using a String to represent the
Line55 thing a Sniper bids for. Had we done so, we could have added the stop price to
Line56 the existing Item class, and it would have been delivered, by deﬁnition, to where
Line57 it was needed.
Line58 We might also have noticed sooner that we do not want to index our table on
Line59 item identiﬁer but on an Item, which would open up the possibility of trying
Line60 multiple policies in a single auction. We’re not saying that we should have de-
Line61 signed more speculatively for a need that hasn’t been proved. Rather, when we
Line62 take the trouble to express the domain clearly, we often ﬁnd that we have more
Line63 options.
Line64 It’s often better to deﬁne domain types to wrap not only Strings but other
Line65 built-in types too, including collections. All we have to do is remember to apply
Line66 our own advice. As you see, sometimes we forget.
Line67 213
Line68 Observations
Line69 
Line70 
Line71 ---
Line72 
Line73 ---
Line74 **Page 214**
Line75 
Line76 This page intentionally left blank
