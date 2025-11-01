Line1 # Making Steady Progress (pp.148-148)
Line2 
Line3 ---
Line4 **Page 148**
Line5 
Line6 Having previously made a fuss about PriceSource, are we being inconsistent
Line7 here by using a boolean for isWinning? Our excuse is that we did try an enum
Line8 for the Sniper state, but it just looked too complicated. The ﬁeld is private to
Line9 AuctionSniper, which is small enough so it’s easy to change later and the code
Line10 reads well.
Line11 The unit and end-to-end tests all pass now, so we can cross off another item
Line12 from the to-do list in Figure 14.3.
Line13 Figure 14.3
Line14 The Sniper wins
Line15 There are more tests we could write—for example, to describe the transitions
Line16 from bidding to winning and back again, but we’ll leave those as an exercise for
Line17 you, Dear Reader. Instead, we’ll move on to the next signiﬁcant change in
Line18 functionality.
Line19 Making Steady Progress
Line20 As always, we made steady progress by adding little slices of functionality. First
Line21 we made the Sniper show when it’s winning, then when it has won. We used
Line22 empty implementations to get us through the compiler when we weren’t ready
Line23 to ﬁll in the code, and we stayed focused on the immediate task.
Line24 One of the pleasant surprises is that, now the code is growing a little, we’re
Line25 starting to see some of our earlier effort pay off as new features just ﬁt into the
Line26 existing structure. The next tasks we have to implement will shake this up.
Line27 Chapter 14
Line28 The Sniper Wins the Auction
Line29 148
