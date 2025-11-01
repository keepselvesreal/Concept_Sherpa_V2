Line1 # Hiding the Right Information (pp.55-56)
Line2 
Line3 ---
Line4 **Page 55**
Line5 
Line6 “permanent” (passed in on construction) or “transient” (passed in to the method
Line7 that needs them).
Line8 In this “paternalistic” approach, each object is told just enough to do its job
Line9 and wrapped up in an abstraction that matches its vocabulary. Eventually, the
Line10 chain of objects reaches a process boundary, which is where the system will ﬁnd
Line11 external details such as host names, ports, and user interface events.
Line12 One Domain Vocabulary
Line13 A class that uses terms from multiple domains might be violating context
Line14 independence, unless it’s part of a bridging layer.
Line15 The effect of the “context independence” rule on a system of objects is to make
Line16 their relationships explicit, deﬁned separately from the objects themselves. First,
Line17 this simpliﬁes the objects, since they don’t need to manage their own relationships.
Line18 Second, this simpliﬁes managing the relationships, since objects at the same
Line19 scale are often created and composed together in the same places, usually in
Line20 mapping-layer factory objects.
Line21 Context independence guides us towards coherent objects that can be applied
Line22 in different contexts, and towards systems that we can change by reconﬁguring
Line23 how their objects are composed.
Line24 Hiding the Right Information
Line25 Encapsulation is almost always a good thing to do, but sometimes information
Line26 can be hidden in the wrong place. This makes the code difﬁcult to understand,
Line27 to integrate, or to build behavior from by composing objects. The best defense
Line28 is to be clear about the difference between the two concepts when discussing a
Line29 design. For example, we might say:
Line30 •
Line31 “Encapsulate the data structure for the cache in the CachingAuctionLoader
Line32 class.”
Line33 •
Line34 “Encapsulate the name of the application’s log ﬁle in the PricingPolicy
Line35 class.”
Line36 These sound reasonable until we recast them in terms of information hiding:
Line37 •
Line38 “Hide the data structure used for the cache in the CachingAuctionLoader
Line39 class.”
Line40 •
Line41 “Hide the name of the application’s log ﬁle in the PricingPolicy class.”
Line42 55
Line43 Hiding the Right Information
Line44 
Line45 
Line46 ---
Line47 
Line48 ---
Line49 **Page 56**
Line50 
Line51 Context independence tells us that we have no business hiding details of the
Line52 log ﬁle in the PricingPolicy class—they’re concepts from different levels in
Line53 the “Russian doll” structure of nested domains. If the log ﬁle name is necessary,
Line54 it should be packaged up and passed in from a level that understands external
Line55 conﬁguration.
Line56 An Opinionated View
Line57 We’ve taken the time to describe what we think of as “good” object-oriented
Line58 design because it underlies our approach to development and we ﬁnd that it helps
Line59 us write code that we can easily grow and adapt to meet the changing needs of
Line60 its users. Now we want to show how our approach to test-driven development
Line61 supports these principles.
Line62 Chapter 6
Line63 Object-Oriented Style
Line64 56
