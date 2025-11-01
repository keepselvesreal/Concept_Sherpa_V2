# Chapter 9: Commissioning an Auction Sniper (pp.75-82)

---
**Page 75**

Chapter 9
Commissioning an Auction
Sniper
To Begin at the Beginning
In which we are commissioned to build an application that automati-
cally bids in auctions. We sketch out how it should work and what
the major components should be. We put together a rough plan for the
incremental steps in which we will grow the application.
We’re a development team for Markup and Gouge, a company that buys antiques
on the professional market to sell to clients “with the best possible taste.” Markup
and Gouge has been following the industry and now does a lot of its buying on-
line, largely from Southabee’s, a venerable auction house that is keen to grow
online. The trouble is that our buyers are spending a lot of their time manually
checking the state of an auction to decide whether or not to bid, and even missed
a couple of attractive items because they could not respond quickly enough.
After intense discussion, the management decides to commission an Auction
Sniper, an application that watches online auctions and automatically bids
slightly higher whenever the price changes, until it reaches a stop-price or the
auction closes. The buyers are keen to have this new application and some of
them agree to help us clarify what to build.
We start by talking through their ideas with the buyers’ group and ﬁnd that,
to avoid confusion, we need to agree on some basic terms:
•
Item is something that can be identiﬁed and bought.
•
Bidder is a person or organization that is interested in buying an item.
•
Bid is a statement that a bidder will pay a given price for an item.
•
Current price is the current highest bid for the item.
•
Stop price is the most a bidder is prepared to pay for an item.
•
Auction is a process for managing bids for an item.
•
Auction house is an institution that hosts auctions.
75


---
**Page 76**

The discussions generate a long list of requirements, such as being able to bid
for related groups of items. There’s no way anyone could deliver everything
within a useful time, so we talk through the options and the buyers reluctantly
agree that they’d rather get a basic application working ﬁrst. Once that’s in place,
we can make it more powerful.
It turns out that in the online system there’s an auction for every item, so we
decide to use an item’s identiﬁer to refer to its auction. In practice, it also turns
out that the Sniper application doesn’t have to concern itself with managing any
items we’ve bought, since other systems will handle payment and delivery.
We decide to build the Auction Sniper as a Java Swing application. It will run
on a desktop and allow the user to bid for multiple items at a time. It will show
the identiﬁer, stop price, and the current auction price and status for each item
it’s sniping. Buyers will be able to add new items for sniping through the user
interface, and the display values will change in response to events arriving from
the auction house. The buyers are still working with our usability people, but
we’ve agreed a rough version that looks like Figure 9.1.
Figure 9.1
A ﬁrst user interface
This is obviously incomplete and not pretty, but it’s close enough to get us
started.
While these discussions are taking place, we also talk to the technicians at
Southabee’s who support their online services. They send us a document that
Chapter 9
Commissioning an Auction Sniper
76


---
**Page 77**

describes their protocol for bidding in auctions, which uses XMPP (Jabber) for
its underlying communication layer. Figure 9.2 shows how it handles multiple
bidders sending bids over XMPP to the auction house, our Sniper being one of
them. As the auction progresses, Southabee’s will send events to all the connected
bidders to tell them when anyone’s bid has raised the current price and when the
auction closes.
Figure 9.2
Southabee’s online auction system
XMPP: the eXtensible Messaging and Presence Protocol
XMPP is a protocol for streaming XML elements across the network. It was origi-
nally designed for, and named after, the Jabber instant messaging system and
was renamed to XMPP when submitted to the IETF for approval as an Internet
standard. Because it is a generic framework for exchanging XML elements across
the network, it can be used for a wide variety of applications that need to exchange
structured data in close to real time.
XMPP has a decentralized, client/server architecture. There is no central server,
in contrast with other chat services such as AOL Instant Messenger or MSN
Messenger. Anyone may run an XMPP server that hosts users and lets them
communicate among themselves and with users hosted by other XMPP servers
on the network.
A user can log in to an XMPP server simultaneously from multiple devices or
clients, known in XMPP terminology as resources. A user assigns each resource
a priority. Unless addressed to a speciﬁc resource, messages sent to the user are
delivered to this user’s highest priority resource that is currently logged in.
Every user on the network has a unique Jabber ID (usually abbreviated as JID)
that is rather like an e-mail address. A JID contains a username and a DNS address
of the server where that user resides, separated by an at sign (@, for example,
username@example.com), and can optionally be sufﬁxed with a resource name after
a forward slash (for example, username@example.com/office).
77
To Begin at the Beginning


---
**Page 78**

Communicating with an Auction
The Auction Protocol
The protocol for messages between a bidder and an auction house is simple.
Bidders send commands, which can be:
Join
A bidder joins an auction. The sender of the XMPP message identiﬁes the
bidder, and the name of the chat session identiﬁes the item.
Bid
A bidder sends a bidding price to the auction.
Auctions send events, which can be:
Price
An auction reports the currently accepted price. This event also includes the
minimum increment that the next bid must be raised by, and the name of
bidder who bid this price. The auction will send this event to a bidder when
it joins and to all bidders whenever a new bid has been accepted.
Close
An auction announces that it has closed. The winner of the last price event
has won the auction.
Figure 9.3
A bidder’s behavior represented as a state machine
Chapter 9
Commissioning an Auction Sniper
78


---
**Page 79**

We spend some time working through the documentation and talking to
Southabee’s On-Line support people, and ﬁgure out a state machine that shows
the transitions a Sniper can make. Essentially, a Sniper joins an auction, then
there are some rounds of bidding, until the auction closes, at which point the
Sniper will have won or lost; see Figure 9.3. We’ve left out the stop price for now
to keep things simple; it’ll turn up in Chapter 18.
The XMPP Messages
Southabee’s On-Line has also sent us details of the formats they use within the
XMPP messages. They’re pretty simple, since they only involve a few names and
values, and are serialized in a single line with key/value pairs. Each line starts
with a version number for the protocol itself. The messages look like this:
SOLVersion: 1.1; Command: JOIN; 
SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;
SOLVersion: 1.1; Command: BID; Price: 199;
SOLVersion: 1.1; Event: CLOSE;
Southabee’s On-Line uses login names to identify items for sale, so to bid
for an item with identiﬁer 12793, a client would start a chat with the “user”
auction-12793 at the Southabee’s server. The server can tell who is bidding from
the identity of the caller, assuming the accounts have been set up beforehand.
Getting There Safely
Even a small application like this is too large to write in one go, so we need to
ﬁgure out, roughly, the steps we might take to get there. A critical technique with
incremental development is learning how to slice up the functionality so that it
can be built a little at a time. Each slice should be signiﬁcant and concrete enough
that the team can tell when it’s done, and small enough to be focused on one
concept and achievable quickly. Dividing our work into small, coherent chunks
also helps us manage the development risk. We get regular, concrete feedback
on the progress we’re making, so we can adjust our plan as the team discovers
more about the domain and the technologies.
Our immediate task is to ﬁgure out a series of incremental development steps
for the Sniper application. The ﬁrst is absolutely the smallest feature we can build,
the “walking skeleton” we described in “First, Test a Walking Skeleton”
(page 32). Here, the skeleton will cut a minimum path through Swing, XMPP,
and our application; it’s just enough to show that we can plug these components
together. Each subsequent step adds a single element of complexity to the existing
application, building on the work that’s done before. After some discussion, we
come up with this sequence of features to build:
79
Getting There Safely


---
**Page 80**

Single item: join, lose without bidding
This is our starting case where we put together the core infrastructure; it is
the subject of Chapter 10.
Single item: join, bid, and lose
Add bidding to the basic connectivity.
Single item: join, bid, and win
Distinguish who sent the winning bid.
Show price details
Start to fill out the user interface.
Multiple items
Support bidding for multiple items in the same application.
Add items through the user interface
Implement input via the user interface.
Stop bidding at the stop price
More intelligence in the Sniper algorithm.
Within the list, the buyers have prioritized the user interface over the stop
price, partly because they want to make sure they’ll feel comfortable with the
application and partly because there won’t be an easy way to add multiple items,
each with its own stop price, without a user interface.
Once this is stable, we can work on more complicated scenarios, such as
retrying if a bid failed or using different strategies for bidding. For now,
implementing just these features should keep us busy.
Figure 9.4
The initial plan
Chapter 9
Commissioning an Auction Sniper
80


---
**Page 81**

We don’t know if this is exactly the order of steps we’ll take, but we believe
we need all of this, and we can adjust as we go along. To keep ourselves
focused, we’ve written the plan on an index card, as in Figure 9.4.
This Isn’t Real
By now you may be raising objections about all the practicalities we’ve skipped
over. We saw them too. We’ve taken shortcuts with the process and design to
give you a feel of how a real project works while remaining within the limits of
a book. In particular:
•
This isn’t a realistic architecture: XMPP is neither reliable nor secure, and
so is unsuitable for transactions. Ensuring any of those qualities is outside
our scope. That said, the fundamental techniques that we describe still apply
whatever the underlying architecture may be. (In our defense, we see that
major systems have been built on a protocol as inappropriate as HTTP, so
perhaps we’re not as unrealistic as we fear.)
•
This isn’t Agile Planning: We rushed through the planning of the project
to produce a single to-do list. In a real project, we’d likely have a view of
the whole deliverable (a release plan) before jumping in. There are good
descriptions of how to do agile planning in other books, such as [Shore07]
and [Cohn05].
•
This isn’t realistic usability design: Good user experience design investigates
what the end user is really trying to achieve and uses that to create a con-
sistent experience. The User Experience community has been engaging with
the Agile Development community for some time on how to do this itera-
tively. This project is simple enough that we can draft a vision of what we
want to achieve and work towards it.
81
This Isn’t Real


---
**Page 82**

This page intentionally left blank 


