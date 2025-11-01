Line1 # Identify Relationships with Interfaces (pp.63-63)
Line2 
Line3 ---
Line4 **Page 63**
Line5 
Line6 Identify Relationships with Interfaces
Line7 We use Java interfaces more liberally than some other developers. This reﬂects
Line8 our emphasis on the relationships between objects, as deﬁned by their communi-
Line9 cation protocols. We use interfaces to name the roles that objects can play and
Line10 to describe the messages they’ll accept.
Line11 We also prefer interfaces to be as narrow as possible, even though that means
Line12 we need more of them. The fewer methods there are on an interface, the more
Line13 obvious is its role in the calling object. We don’t have to worry which other
Line14 methods are relevant to a particular call and which were included for convenience.
Line15 Narrow interfaces are also easier to write adapters and decorators for; there’s
Line16 less to implement, so it’s easier to write objects that compose together well.
Line17 “Pulling” interfaces into existence, as we described in “Budding Off,” helps
Line18 us keep them as narrow as possible. Driving an interface from its client avoids
Line19 leaking excess information about its implementers, which minimizes any implicit
Line20 coupling between objects and so keeps the code malleable.
Line21 Impl Classes Are Meaningless
Line22 Sometimes we see code with classes named by adding “Impl” to the single interface
Line23 they implement. This is better than leaving the class name unchanged and
Line24 preﬁxing an “I” to the interface, but not by much. A name like BookingImpl is dupli-
Line25 cation; it says exactly the same as implements Booking, which is a “code smell.”
Line26 We would not be happy with such obvious duplication elsewhere in our code,
Line27 so we ought to refactor it away.
Line28 It might just be a naming problem. There’s always something speciﬁc about an
Line29 implementation that can be included in the class name: it might use a bounded
Line30 collection, communicate over HTTP, use a database for persistence, and so on.
Line31 A bridging class is even easier to name, since it will belong in one domain but
Line32 implement interfaces in another.
Line33 If there really isn’t a good implementation name, it might mean that the interface
Line34 is poorly named or designed. Perhaps it’s unfocused because it has too many re-
Line35 sponsibilities; or it’s named after its implementation rather than its role in the client;
Line36 or it’s a value, not an object—this discrepancy sometimes turns up when writing
Line37 unit tests, see “Don’t Mock Values” (page 237).
Line38 Refactor Interfaces Too
Line39 Once we have interfaces for protocols, we can start to pay attention to similarities
Line40 and differences. In a reasonably large codebase, we often start to ﬁnd interfaces
Line41 that look similar. This means we should look at whether they represent a single
Line42 concept and should be merged. Extracting common roles makes the design more
Line43 63
Line44 Refactor Interfaces Too
Line45 
Line46 
Line47 ---
