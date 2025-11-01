Line1 # Getting There Safely (pp.79-81)
Line2 
Line3 ---
Line4 **Page 79**
Line5 
Line6 We spend some time working through the documentation and talking to
Line7 Southabee’s On-Line support people, and ﬁgure out a state machine that shows
Line8 the transitions a Sniper can make. Essentially, a Sniper joins an auction, then
Line9 there are some rounds of bidding, until the auction closes, at which point the
Line10 Sniper will have won or lost; see Figure 9.3. We’ve left out the stop price for now
Line11 to keep things simple; it’ll turn up in Chapter 18.
Line12 The XMPP Messages
Line13 Southabee’s On-Line has also sent us details of the formats they use within the
Line14 XMPP messages. They’re pretty simple, since they only involve a few names and
Line15 values, and are serialized in a single line with key/value pairs. Each line starts
Line16 with a version number for the protocol itself. The messages look like this:
Line17 SOLVersion: 1.1; Command: JOIN; 
Line18 SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
Line19 SOLVersion: 1.1; Command: BID; Price: 199;
Line20 SOLVersion: 1.1; Event: CLOSE;
Line21 Southabee’s On-Line uses login names to identify items for sale, so to bid
Line22 for an item with identiﬁer 12793, a client would start a chat with the “user”
Line23 auction-12793 at the Southabee’s server. The server can tell who is bidding from
Line24 the identity of the caller, assuming the accounts have been set up beforehand.
Line25 Getting There Safely
Line26 Even a small application like this is too large to write in one go, so we need to
Line27 ﬁgure out, roughly, the steps we might take to get there. A critical technique with
Line28 incremental development is learning how to slice up the functionality so that it
Line29 can be built a little at a time. Each slice should be signiﬁcant and concrete enough
Line30 that the team can tell when it’s done, and small enough to be focused on one
Line31 concept and achievable quickly. Dividing our work into small, coherent chunks
Line32 also helps us manage the development risk. We get regular, concrete feedback
Line33 on the progress we’re making, so we can adjust our plan as the team discovers
Line34 more about the domain and the technologies.
Line35 Our immediate task is to ﬁgure out a series of incremental development steps
Line36 for the Sniper application. The ﬁrst is absolutely the smallest feature we can build,
Line37 the “walking skeleton” we described in “First, Test a Walking Skeleton”
Line38 (page 32). Here, the skeleton will cut a minimum path through Swing, XMPP,
Line39 and our application; it’s just enough to show that we can plug these components
Line40 together. Each subsequent step adds a single element of complexity to the existing
Line41 application, building on the work that’s done before. After some discussion, we
Line42 come up with this sequence of features to build:
Line43 79
Line44 Getting There Safely
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 80**
Line51 
Line52 Single item: join, lose without bidding
Line53 This is our starting case where we put together the core infrastructure; it is
Line54 the subject of Chapter 10.
Line55 Single item: join, bid, and lose
Line56 Add bidding to the basic connectivity.
Line57 Single item: join, bid, and win
Line58 Distinguish who sent the winning bid.
Line59 Show price details
Line60 Start to fill out the user interface.
Line61 Multiple items
Line62 Support bidding for multiple items in the same application.
Line63 Add items through the user interface
Line64 Implement input via the user interface.
Line65 Stop bidding at the stop price
Line66 More intelligence in the Sniper algorithm.
Line67 Within the list, the buyers have prioritized the user interface over the stop
Line68 price, partly because they want to make sure they’ll feel comfortable with the
Line69 application and partly because there won’t be an easy way to add multiple items,
Line70 each with its own stop price, without a user interface.
Line71 Once this is stable, we can work on more complicated scenarios, such as
Line72 retrying if a bid failed or using different strategies for bidding. For now,
Line73 implementing just these features should keep us busy.
Line74 Figure 9.4
Line75 The initial plan
Line76 Chapter 9
Line77 Commissioning an Auction Sniper
Line78 80
Line79 
Line80 
Line81 ---
Line82 
Line83 ---
Line84 **Page 81**
Line85 
Line86 We don’t know if this is exactly the order of steps we’ll take, but we believe
Line87 we need all of this, and we can adjust as we go along. To keep ourselves
Line88 focused, we’ve written the plan on an index card, as in Figure 9.4.
Line89 This Isn’t Real
Line90 By now you may be raising objections about all the practicalities we’ve skipped
Line91 over. We saw them too. We’ve taken shortcuts with the process and design to
Line92 give you a feel of how a real project works while remaining within the limits of
Line93 a book. In particular:
Line94 •
Line95 This isn’t a realistic architecture: XMPP is neither reliable nor secure, and
Line96 so is unsuitable for transactions. Ensuring any of those qualities is outside
Line97 our scope. That said, the fundamental techniques that we describe still apply
Line98 whatever the underlying architecture may be. (In our defense, we see that
Line99 major systems have been built on a protocol as inappropriate as HTTP, so
Line100 perhaps we’re not as unrealistic as we fear.)
Line101 •
Line102 This isn’t Agile Planning: We rushed through the planning of the project
Line103 to produce a single to-do list. In a real project, we’d likely have a view of
Line104 the whole deliverable (a release plan) before jumping in. There are good
Line105 descriptions of how to do agile planning in other books, such as [Shore07]
Line106 and [Cohn05].
Line107 •
Line108 This isn’t realistic usability design: Good user experience design investigates
Line109 what the end user is really trying to achieve and uses that to create a con-
Line110 sistent experience. The User Experience community has been engaging with
Line111 the Agile Development community for some time on how to do this itera-
Line112 tively. This project is simple enough that we can draft a vision of what we
Line113 want to achieve and work towards it.
Line114 81
Line115 This Isn’t Real
Line116 
Line117 
Line118 ---
