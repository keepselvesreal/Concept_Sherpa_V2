Line1 # Where Do Objects Come From? (pp.60-63)
Line2 
Line3 ---
Line4 **Page 60**
Line5 
Line6 type, which might eventually allow us to hide its ﬁelds behind a clean
Line7 interface, satisfying the “composite simpler than the sum of its parts” rule.
Line8 We ﬁnd that the discovery of value types is usually motivated by trying to
Line9 follow our design principles, rather than by responding to code stresses when
Line10 writing tests.
Line11 Where Do Objects Come From?
Line12 The categories for discovering object types are similar (which is why we shoe-
Line13 horned them into these names), except that the design guidance we get from
Line14 writing unit tests tends to be more important. As we wrote in “External and
Line15 Internal Quality” (page 10), we use the effort of unit testing to maintain the
Line16 code’s internal quality. There are more examples of the inﬂuence of testing on
Line17 design in Chapter 20.
Line18 Breaking Out: Splitting a Large Object into a Group of
Line19 Collaborating Objects
Line20 When starting a new area of code, we might temporarily suspend our design
Line21 judgment and just write code without attempting to impose much structure. This
Line22 allows us to gain some experience in the area and test our understanding of any
Line23 external APIs we’re developing against. After a short while, we’ll ﬁnd our code
Line24 becoming too complex to understand and will want to clean it up. We can start
Line25 pulling out cohesive units of functionality into smaller collaborating objects,
Line26 which we can then unit-test independently. Splitting out a new object also forces
Line27 us to look at the dependencies of the code we’re pulling out.
Line28 We have two concerns about deferring cleanup. The ﬁrst is how long we should
Line29 wait before doing something. Under time pressure, it’s tempting to leave the un-
Line30 structured code as is and move on to the next thing (“after all, it works and it’s
Line31 just one class…”). We’ve seen too much code where the intention wasn’t clear
Line32 and the cost of cleanup kicked in when the team could least afford it. The second
Line33 concern is that occasionally it’s better to treat this code as a spike—once we
Line34 know what to do, just roll it back and reimplement cleanly. Code isn’t sacred
Line35 just because it exists, and the second time won’t take as long.
Line36 The Tests Say…
Line37 Break up an object if it becomes too large to test easily, or if its test failures become
Line38 difﬁcult to interpret. Then unit-test the new parts separately.
Line39 Chapter 7
Line40 Achieving Object-Oriented Design
Line41 60
Line42 
Line43 
Line44 ---
Line45 
Line46 ---
Line47 **Page 61**
Line48 
Line49 Looking Ahead…
Line50 In Chapter 12, when extracting an AuctionMessageTranslator, we avoid including
Line51 its interaction with MainWindow because that would give it too many responsibilities.
Line52 Looking at the behavior of the new class, we identify a missing dependency,
Line53 AuctionEventListener, which we deﬁne while writing the unit tests.We repackage
Line54 the existing code in Main to provide an implementation for the new interface.
Line55 AuctionMessageTranslator satisﬁes both our design heuristics: it introduces a
Line56 separation of concerns by splitting message translation from auction display, and
Line57 it abstracts message-handling code into a new domain-speciﬁc concept.
Line58 Budding Off: Deﬁning a New Service That an Object Needs and
Line59 Adding a New Object to Provide It
Line60 When the code is more stable and has some degree of structure, we often discover
Line61 new types by “pulling” them into existence. We might be adding behavior to an
Line62 object and ﬁnd that, following our design principles, some new feature doesn’t
Line63 belong inside it.
Line64 Our response is to create an interface to deﬁne the service that the object needs
Line65 from the object’s point of view. We write tests for the new behavior as if the
Line66 service already exists, using mock objects to help describe the relationship between
Line67 the target object and its new collaborator; this is how we introduced the
Line68 AuctionEventListener we mentioned in the previous section.
Line69 The development cycle goes like this. When implementing an object, we discover
Line70 that it needs a service to be provided by another object. We give the new service
Line71 a name and mock it out in the client object’s unit tests, to clarify the relationship
Line72 between the two. Then we write an object to provide that service and, in doing
Line73 so, discover what services that object needs. We follow this chain (or perhaps a
Line74 directed graph) of collaborator relationships until we connect up to existing ob-
Line75 jects, either our own or from a third-party API. This is how we implement
Line76 “Develop from the Inputs to the Outputs” (page 43).
Line77 We think of this as “on-demand” design: we “pull” interfaces and their imple-
Line78 mentations into existence from the needs of the client, rather than “pushing” out
Line79 the features that we think a class should provide.
Line80 The Tests Say…
Line81 When writing a test, we ask ourselves, “If this worked, who would know?” If the
Line82 right answer to that question is not in the target object, it’s probably time to introduce
Line83 a new collaborator.
Line84 61
Line85 Where Do Objects Come From?
Line86 
Line87 
Line88 ---
Line89 
Line90 ---
Line91 **Page 62**
Line92 
Line93 Looking Ahead…
Line94 In Chapter 13, we introduce an Auction interface. The concept of making a bid
Line95 would have been an additional responsibility for AuctionSniper, so we introduce
Line96 a new service for bidding—just an interface without any implementation.We write a
Line97 new test to show the relationship between AuctionSniper and Auction. Then we
Line98 write a concrete implementation of Auction—initially as an anonymous class in
Line99 Main, later as XMPPAuction.
Line100 Bundling Up: Hiding Related Objects into a Containing Object
Line101 This is the application of the “composite simpler than the sum of its parts” rule
Line102 (page 53). When we have a cluster of related objects that work together, we can
Line103 package them up in a containing object. The new object hides the complexity in
Line104 an abstraction that allows us to program at a higher level.
Line105 The process of making an implicit concept concrete has some other nice effects.
Line106 First, we have to give it a name which helps us understand the domain a little
Line107 better. Second, we can scope dependencies more clearly, since we can see the
Line108 boundaries of the concept. Third, we can be more precise with our unit testing.
Line109 We can test the new composite object directly, and use a mock implementation
Line110 to simplify the tests for code from which it was extracted (since, of course, we
Line111 added an interface for the role the new object plays).
Line112 The Tests Say…
Line113 When the test for an object becomes too complicated to set up—when there are
Line114 too many moving parts to get the code into the relevant state—consider bundling
Line115 up some of the collaborating objects. There’s an example in “Bloated Constructor”
Line116 (page 238).
Line117 Looking Ahead…
Line118 In Chapter 17, we introduce XMPPAuctionHouse to package up everything to do with
Line119 the messaging infrastructure, and SniperLauncher for constructing and attaching a
Line120 Sniper. Once extracted, the references to Swing behavior in SniperLauncher
Line121 stand out as inappropriate, so we introduce SniperCollector to decouple the
Line122 domains.
Line123 Chapter 7
Line124 Achieving Object-Oriented Design
Line125 62
Line126 
Line127 
Line128 ---
Line129 
Line130 ---
Line131 **Page 63**
Line132 
Line133 Identify Relationships with Interfaces
Line134 We use Java interfaces more liberally than some other developers. This reﬂects
Line135 our emphasis on the relationships between objects, as deﬁned by their communi-
Line136 cation protocols. We use interfaces to name the roles that objects can play and
Line137 to describe the messages they’ll accept.
Line138 We also prefer interfaces to be as narrow as possible, even though that means
Line139 we need more of them. The fewer methods there are on an interface, the more
Line140 obvious is its role in the calling object. We don’t have to worry which other
Line141 methods are relevant to a particular call and which were included for convenience.
Line142 Narrow interfaces are also easier to write adapters and decorators for; there’s
Line143 less to implement, so it’s easier to write objects that compose together well.
Line144 “Pulling” interfaces into existence, as we described in “Budding Off,” helps
Line145 us keep them as narrow as possible. Driving an interface from its client avoids
Line146 leaking excess information about its implementers, which minimizes any implicit
Line147 coupling between objects and so keeps the code malleable.
Line148 Impl Classes Are Meaningless
Line149 Sometimes we see code with classes named by adding “Impl” to the single interface
Line150 they implement. This is better than leaving the class name unchanged and
Line151 preﬁxing an “I” to the interface, but not by much. A name like BookingImpl is dupli-
Line152 cation; it says exactly the same as implements Booking, which is a “code smell.”
Line153 We would not be happy with such obvious duplication elsewhere in our code,
Line154 so we ought to refactor it away.
Line155 It might just be a naming problem. There’s always something speciﬁc about an
Line156 implementation that can be included in the class name: it might use a bounded
Line157 collection, communicate over HTTP, use a database for persistence, and so on.
Line158 A bridging class is even easier to name, since it will belong in one domain but
Line159 implement interfaces in another.
Line160 If there really isn’t a good implementation name, it might mean that the interface
Line161 is poorly named or designed. Perhaps it’s unfocused because it has too many re-
Line162 sponsibilities; or it’s named after its implementation rather than its role in the client;
Line163 or it’s a value, not an object—this discrepancy sometimes turns up when writing
Line164 unit tests, see “Don’t Mock Values” (page 237).
Line165 Refactor Interfaces Too
Line166 Once we have interfaces for protocols, we can start to pay attention to similarities
Line167 and differences. In a reasonably large codebase, we often start to ﬁnd interfaces
Line168 that look similar. This means we should look at whether they represent a single
Line169 concept and should be merged. Extracting common roles makes the design more
Line170 63
Line171 Refactor Interfaces Too
Line172 
Line173 
Line174 ---
