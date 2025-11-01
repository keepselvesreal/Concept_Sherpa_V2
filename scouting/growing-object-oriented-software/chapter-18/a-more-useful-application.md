Line1 # A More Useful Application (pp.205-205)
Line2 
Line3 ---
Line4 **Page 205**
Line5 
Line6 Chapter 18
Line7 Filling In the Details
Line8 In which we introduce a stop price so we don’t bid inﬁnitely, which
Line9 means we can now be losing an auction that hasn’t yet closed. We add
Line10 a new ﬁeld to the user interface and push it through to the Sniper. We
Line11 realize we should have created an Item type much earlier.
Line12 A More Useful Application
Line13 So far the functionality has been prioritized to attract potential customers by
Line14 giving them a sense of what the application will look like. We can show items
Line15 being added and some features of sniping. It’s not a very useful application be-
Line16 cause, amongst other things, there’s no upper limit for bidding on an item—it
Line17 could be very expensive to deploy.
Line18 This is a common pattern when using Agile Development techniques to work
Line19 on a new project. The team is ﬂexible enough to respond to how the needs of
Line20 the sponsors change over time: at the beginning, the emphasis might be on
Line21 proving the concept to attract enough support to continue; later, the emphasis
Line22 might be on implementing enough functionality to be ready to deploy; later still,
Line23 the emphasis might change to providing more options to support a wider range
Line24 of users.
Line25 This dynamic is very different from both a ﬁxed design approach, where the
Line26 structure of the development has to be approved before work can begin, and a
Line27 code-and-ﬁx approach, where the system might be initially successful but not
Line28 resilient enough to adapt to its changing role.
Line29 Stop When We’ve Had Enough
Line30 Our next most pressing task (especially after recent crises in the ﬁnancial markets)
Line31 is to be able to set an upper limit, the “stop price,” for our bid for an item.
Line32 Introducing a Losing State
Line33 With the introduction of a stop price, it’s possible for a Sniper to be losing before
Line34 the auction has closed. We could implement this by just marking the Sniper as
Line35 Lost when it hits its stop price, but the users want to know the ﬁnal price when
Line36 the auction has ﬁnished after they’ve dropped out, so we model this as an extra
Line37 state. Once a Sniper has been outbid at its stop price, it will never be able to win,
Line38 205
Line39 
Line40 
Line41 ---
