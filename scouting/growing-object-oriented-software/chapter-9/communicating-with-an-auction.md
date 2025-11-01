Line1 # Communicating with an Auction (pp.78-79)
Line2 
Line3 ---
Line4 **Page 78**
Line5 
Line6 Communicating with an Auction
Line7 The Auction Protocol
Line8 The protocol for messages between a bidder and an auction house is simple.
Line9 Bidders send commands, which can be:
Line10 Join
Line11 A bidder joins an auction. The sender of the XMPP message identiﬁes the
Line12 bidder, and the name of the chat session identiﬁes the item.
Line13 Bid
Line14 A bidder sends a bidding price to the auction.
Line15 Auctions send events, which can be:
Line16 Price
Line17 An auction reports the currently accepted price. This event also includes the
Line18 minimum increment that the next bid must be raised by, and the name of
Line19 bidder who bid this price. The auction will send this event to a bidder when
Line20 it joins and to all bidders whenever a new bid has been accepted.
Line21 Close
Line22 An auction announces that it has closed. The winner of the last price event
Line23 has won the auction.
Line24 Figure 9.3
Line25 A bidder’s behavior represented as a state machine
Line26 Chapter 9
Line27 Commissioning an Auction Sniper
Line28 78
Line29 
Line30 
Line31 ---
Line32 
Line33 ---
Line34 **Page 79**
Line35 
Line36 We spend some time working through the documentation and talking to
Line37 Southabee’s On-Line support people, and ﬁgure out a state machine that shows
Line38 the transitions a Sniper can make. Essentially, a Sniper joins an auction, then
Line39 there are some rounds of bidding, until the auction closes, at which point the
Line40 Sniper will have won or lost; see Figure 9.3. We’ve left out the stop price for now
Line41 to keep things simple; it’ll turn up in Chapter 18.
Line42 The XMPP Messages
Line43 Southabee’s On-Line has also sent us details of the formats they use within the
Line44 XMPP messages. They’re pretty simple, since they only involve a few names and
Line45 values, and are serialized in a single line with key/value pairs. Each line starts
Line46 with a version number for the protocol itself. The messages look like this:
Line47 SOLVersion: 1.1; Command: JOIN; 
Line48 SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
Line49 SOLVersion: 1.1; Command: BID; Price: 199;
Line50 SOLVersion: 1.1; Event: CLOSE;
Line51 Southabee’s On-Line uses login names to identify items for sale, so to bid
Line52 for an item with identiﬁer 12793, a client would start a chat with the “user”
Line53 auction-12793 at the Southabee’s server. The server can tell who is bidding from
Line54 the identity of the caller, assuming the accounts have been set up beforehand.
Line55 Getting There Safely
Line56 Even a small application like this is too large to write in one go, so we need to
Line57 ﬁgure out, roughly, the steps we might take to get there. A critical technique with
Line58 incremental development is learning how to slice up the functionality so that it
Line59 can be built a little at a time. Each slice should be signiﬁcant and concrete enough
Line60 that the team can tell when it’s done, and small enough to be focused on one
Line61 concept and achievable quickly. Dividing our work into small, coherent chunks
Line62 also helps us manage the development risk. We get regular, concrete feedback
Line63 on the progress we’re making, so we can adjust our plan as the team discovers
Line64 more about the domain and the technologies.
Line65 Our immediate task is to ﬁgure out a series of incremental development steps
Line66 for the Sniper application. The ﬁrst is absolutely the smallest feature we can build,
Line67 the “walking skeleton” we described in “First, Test a Walking Skeleton”
Line68 (page 32). Here, the skeleton will cut a minimum path through Swing, XMPP,
Line69 and our application; it’s just enough to show that we can plug these components
Line70 together. Each subsequent step adds a single element of complexity to the existing
Line71 application, building on the work that’s done before. After some discussion, we
Line72 come up with this sequence of features to build:
Line73 79
Line74 Getting There Safely
Line75 
Line76 
Line77 ---
