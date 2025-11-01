Line1 # Observations (pp.171-174)
Line2 
Line3 ---
Line4 **Page 171**
Line5 
Line6 The acceptance test passes, and we can see the result in Figure 15.5.
Line7 Figure 15.5
Line8 Sniper with column headers
Line9 Enough for Now
Line10 There’s more we should do, such as set up borders and text alignment, to tune
Line11 the user interface. We might do that by associating CellRenderers with each
Line12 Column value, or perhaps by introducing a TableColumnModel. We’ll leave those
Line13 as an exercise for the reader, since they don’t add any more insight into our
Line14 development process.
Line15 In the meantime, we can cross off one more task from our to-do list:
Line16 Figure 15.6.
Line17 Figure 15.6
Line18 The Sniper shows price information
Line19 Observations
Line20 Single Responsibilities
Line21 SnipersTableModel has one responsibility: to represent the state of our bidding
Line22 in the user interface. It follows the heuristic we described in “No And’s, Or’s, or
Line23 171
Line24 Observations
Line25 
Line26 
Line27 ---
Line28 
Line29 ---
Line30 **Page 172**
Line31 
Line32 But’s” (page 51). We’ve seen too much user interface code that is brittle because
Line33 it has business logic mixed in. In this case, we could also have made the model
Line34 responsible for deciding whether to bid (“because that would be simpler”), but
Line35 that would make it harder to respond when either the user interface or the bidding
Line36 policy change. It would be harder to even ﬁnd the bidding policy, which is why
Line37 we isolated it in AuctionSniper.
Line38 Keyhole Surgery for Software
Line39 In this chapter we repeatedly used the practice of adding little slices of behavior
Line40 all the way through the system: replace a label with a table, get that working;
Line41 show the Sniper bidding, get that working; add the other values, get that
Line42 working. In all of these cases, we’ve ﬁgured out where we want to get to (always
Line43 allowing that we might discover a better alternative along the way), but we want
Line44 to avoid ripping the application apart to get there. Once we start a major rework,
Line45 we can’t stop until it’s ﬁnished, we can’t check in without branching, and merging
Line46 with rest of the team is harder. There’s a reason that surgeons prefer keyhole
Line47 surgery to opening up a patient—it’s less invasive and cheaper.
Line48 Programmer Hyper-Sensitivity
Line49 We have a well-developed sense of the value of our own time. We keep an eye
Line50 out for activities that don’t seem to be making the best of our (doubtless signiﬁ-
Line51 cant) talents, such as boiler-plate copying and adapting code: if we had the right
Line52 abstraction, we wouldn’t have to bother. Sometimes this just has to be done, es-
Line53 pecially when working with existing code—but there are fewer excuses when it’s
Line54 our own. Deciding when to change the design requires a good sense for trade-
Line55 offs, which implies both sensitivity and technical maturity: “I’m about to repeat
Line56 this code with minor variations, that seems dull and wasteful” as against “This
Line57 may not be the right time to rework this, I don’t understand it yet.”
Line58 We don’t have a simple, reproducible technique here; it requires skill and ex-
Line59 perience. Developers should have a habit of reﬂecting on their activity, on the
Line60 best way to invest their time for the rest of a coding session. This might mean
Line61 carrying on exactly as before, but at least they’ll have thought about it.
Line62 Celebrate Changing Your Mind
Line63 When the facts change, I change my mind. What do you do, sir?
Line64 —John Maynard Keynes
Line65 During this chapter, we renamed several features in the code. In many develop-
Line66 ment cultures, this is viewed as a sign of weakness, as an inability to do a proper
Line67 job. Instead, we think this is an essential part of our development process. Just
Line68 Chapter 15
Line69 Towards a Real User Interface
Line70 172
Line71 
Line72 
Line73 ---
Line74 
Line75 ---
Line76 **Page 173**
Line77 
Line78 as we learn more about what the structure should be by using the code we’ve
Line79 written, we learn more about the names we’ve chosen when we work with them.
Line80 We see how the type and method names ﬁt together and whether the concepts
Line81 are clear, which stimulates the discovery of new ideas. If the name of a feature
Line82 isn’t right, the only smart thing to do is change it and avoid countless hours of
Line83 confusion for all who will read the code later.
Line84 This Isn’t the Only Solution
Line85 Examples in books, such as this one, tend to read as if there was an inevitability
Line86 about the solution. That’s partly because we put effort into making the narrative
Line87 ﬂow, but it’s also because presenting one solution tends to drive others out of
Line88 the reader’s consciousness. There are other variations we could have considered,
Line89 some of which might even resurface as the example develops.
Line90 For example, we could argue that AuctionSniper doesn’t need to know whether
Line91 it’s won or lost the auction—just whether it should bid or not. At present, the
Line92 only part of the application that cares about winning is the user interface, and
Line93 it would certainly simplify the AuctionSniper and SniperSnapshot if we moved
Line94 that decision away from them. We won’t do that now, because we don’t yet
Line95 know if it’s the right choice, but we ﬁnd that kicking around design options
Line96 sometimes leads to much better solutions.
Line97 173
Line98 Observations
Line99 
Line100 
Line101 ---
Line102 
Line103 ---
Line104 **Page 174**
Line105 
Line106 This page intentionally left blank
