Line1 # To Begin at the Beginning (pp.75-78)
Line2 
Line3 ---
Line4 **Page 75**
Line5 
Line6 Chapter 9
Line7 Commissioning an Auction
Line8 Sniper
Line9 To Begin at the Beginning
Line10 In which we are commissioned to build an application that automati-
Line11 cally bids in auctions. We sketch out how it should work and what
Line12 the major components should be. We put together a rough plan for the
Line13 incremental steps in which we will grow the application.
Line14 We’re a development team for Markup and Gouge, a company that buys antiques
Line15 on the professional market to sell to clients “with the best possible taste.” Markup
Line16 and Gouge has been following the industry and now does a lot of its buying on-
Line17 line, largely from Southabee’s, a venerable auction house that is keen to grow
Line18 online. The trouble is that our buyers are spending a lot of their time manually
Line19 checking the state of an auction to decide whether or not to bid, and even missed
Line20 a couple of attractive items because they could not respond quickly enough.
Line21 After intense discussion, the management decides to commission an Auction
Line22 Sniper, an application that watches online auctions and automatically bids
Line23 slightly higher whenever the price changes, until it reaches a stop-price or the
Line24 auction closes. The buyers are keen to have this new application and some of
Line25 them agree to help us clarify what to build.
Line26 We start by talking through their ideas with the buyers’ group and ﬁnd that,
Line27 to avoid confusion, we need to agree on some basic terms:
Line28 •
Line29 Item is something that can be identiﬁed and bought.
Line30 •
Line31 Bidder is a person or organization that is interested in buying an item.
Line32 •
Line33 Bid is a statement that a bidder will pay a given price for an item.
Line34 •
Line35 Current price is the current highest bid for the item.
Line36 •
Line37 Stop price is the most a bidder is prepared to pay for an item.
Line38 •
Line39 Auction is a process for managing bids for an item.
Line40 •
Line41 Auction house is an institution that hosts auctions.
Line42 75
Line43 
Line44 
Line45 ---
Line46 
Line47 ---
Line48 **Page 76**
Line49 
Line50 The discussions generate a long list of requirements, such as being able to bid
Line51 for related groups of items. There’s no way anyone could deliver everything
Line52 within a useful time, so we talk through the options and the buyers reluctantly
Line53 agree that they’d rather get a basic application working ﬁrst. Once that’s in place,
Line54 we can make it more powerful.
Line55 It turns out that in the online system there’s an auction for every item, so we
Line56 decide to use an item’s identiﬁer to refer to its auction. In practice, it also turns
Line57 out that the Sniper application doesn’t have to concern itself with managing any
Line58 items we’ve bought, since other systems will handle payment and delivery.
Line59 We decide to build the Auction Sniper as a Java Swing application. It will run
Line60 on a desktop and allow the user to bid for multiple items at a time. It will show
Line61 the identiﬁer, stop price, and the current auction price and status for each item
Line62 it’s sniping. Buyers will be able to add new items for sniping through the user
Line63 interface, and the display values will change in response to events arriving from
Line64 the auction house. The buyers are still working with our usability people, but
Line65 we’ve agreed a rough version that looks like Figure 9.1.
Line66 Figure 9.1
Line67 A ﬁrst user interface
Line68 This is obviously incomplete and not pretty, but it’s close enough to get us
Line69 started.
Line70 While these discussions are taking place, we also talk to the technicians at
Line71 Southabee’s who support their online services. They send us a document that
Line72 Chapter 9
Line73 Commissioning an Auction Sniper
Line74 76
Line75 
Line76 
Line77 ---
Line78 
Line79 ---
Line80 **Page 77**
Line81 
Line82 describes their protocol for bidding in auctions, which uses XMPP (Jabber) for
Line83 its underlying communication layer. Figure 9.2 shows how it handles multiple
Line84 bidders sending bids over XMPP to the auction house, our Sniper being one of
Line85 them. As the auction progresses, Southabee’s will send events to all the connected
Line86 bidders to tell them when anyone’s bid has raised the current price and when the
Line87 auction closes.
Line88 Figure 9.2
Line89 Southabee’s online auction system
Line90 XMPP: the eXtensible Messaging and Presence Protocol
Line91 XMPP is a protocol for streaming XML elements across the network. It was origi-
Line92 nally designed for, and named after, the Jabber instant messaging system and
Line93 was renamed to XMPP when submitted to the IETF for approval as an Internet
Line94 standard. Because it is a generic framework for exchanging XML elements across
Line95 the network, it can be used for a wide variety of applications that need to exchange
Line96 structured data in close to real time.
Line97 XMPP has a decentralized, client/server architecture. There is no central server,
Line98 in contrast with other chat services such as AOL Instant Messenger or MSN
Line99 Messenger. Anyone may run an XMPP server that hosts users and lets them
Line100 communicate among themselves and with users hosted by other XMPP servers
Line101 on the network.
Line102 A user can log in to an XMPP server simultaneously from multiple devices or
Line103 clients, known in XMPP terminology as resources. A user assigns each resource
Line104 a priority. Unless addressed to a speciﬁc resource, messages sent to the user are
Line105 delivered to this user’s highest priority resource that is currently logged in.
Line106 Every user on the network has a unique Jabber ID (usually abbreviated as JID)
Line107 that is rather like an e-mail address. A JID contains a username and a DNS address
Line108 of the server where that user resides, separated by an at sign (@, for example,
Line109 username@example.com), and can optionally be sufﬁxed with a resource name after
Line110 a forward slash (for example, username@example.com/office).
Line111 77
Line112 To Begin at the Beginning
Line113 
Line114 
Line115 ---
Line116 
Line117 ---
Line118 **Page 78**
Line119 
Line120 Communicating with an Auction
Line121 The Auction Protocol
Line122 The protocol for messages between a bidder and an auction house is simple.
Line123 Bidders send commands, which can be:
Line124 Join
Line125 A bidder joins an auction. The sender of the XMPP message identiﬁes the
Line126 bidder, and the name of the chat session identiﬁes the item.
Line127 Bid
Line128 A bidder sends a bidding price to the auction.
Line129 Auctions send events, which can be:
Line130 Price
Line131 An auction reports the currently accepted price. This event also includes the
Line132 minimum increment that the next bid must be raised by, and the name of
Line133 bidder who bid this price. The auction will send this event to a bidder when
Line134 it joins and to all bidders whenever a new bid has been accepted.
Line135 Close
Line136 An auction announces that it has closed. The winner of the last price event
Line137 has won the auction.
Line138 Figure 9.3
Line139 A bidder’s behavior represented as a state machine
Line140 Chapter 9
Line141 Commissioning an Auction Sniper
Line142 78
Line143 
Line144 
Line145 ---
