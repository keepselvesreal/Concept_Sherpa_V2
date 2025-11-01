Line1 # Context Independence (pp.54-55)
Line2 
Line3 ---
Line4 **Page 54**
Line5 
Line6 In software, a user interface component for editing money values might have
Line7 two subcomponents: one for the amount and one for the currency. For the
Line8 component to be useful, its API should manage both values together, otherwise
Line9 the client code could just control it subcomponents directly.
Line10 moneyEditor.getAmountField().setText(String.valueOf(money.amount());
Line11 moneyEditor.getCurrencyField().setText(money.currencyCode());
Line12 The “Tell, Don’t Ask” convention can start to hide an object’s structure from
Line13 its clients but is not a strong enough rule by itself. For example, we could replace
Line14 the getters in the ﬁrst version with setters:
Line15 moneyEditor.setAmountField(money.amount());
Line16 moneyEditor.setCurrencyField(money.currencyCode());
Line17 This still exposes the internal structure of the component, which its client still
Line18 has to manage explicitly.
Line19 We can make the API much simpler by hiding within the component everything
Line20 about the way money values are displayed and edited, which in turn simpliﬁes
Line21 the client code:
Line22 moneyEditor.setValue(money);
Line23 This suggests a rule of thumb:
Line24 Composite Simpler Than the Sum of Its Parts
Line25 The API of a composite object should not be more complicated than that of any of
Line26 its components.
Line27 Composite objects can, of course, be used as components in larger-scale, more
Line28 sophisticated composite objects. As we grow the code, the “composite simpler
Line29 than the sum of its parts” rule contributes to raising the level of abstraction.
Line30 Context Independence
Line31 While the “composite simpler than the sum of its parts” rule helps us decide
Line32 whether an object hides enough information, the “context independence” rule
Line33 helps us decide whether an object hides too much or hides the wrong information.
Line34 A system is easier to change if its objects are context-independent; that is, if
Line35 each object has no built-in knowledge about the system in which it executes. This
Line36 allows us to take units of behavior (objects) and apply them in new situations.
Line37 To be context-independent, whatever an object needs to know about the larger
Line38 environment it’s running in must be passed in. Those relationships might be
Line39 Chapter 6
Line40 Object-Oriented Style
Line41 54
Line42 
Line43 
Line44 ---
Line45 
Line46 ---
Line47 **Page 55**
Line48 
Line49 “permanent” (passed in on construction) or “transient” (passed in to the method
Line50 that needs them).
Line51 In this “paternalistic” approach, each object is told just enough to do its job
Line52 and wrapped up in an abstraction that matches its vocabulary. Eventually, the
Line53 chain of objects reaches a process boundary, which is where the system will ﬁnd
Line54 external details such as host names, ports, and user interface events.
Line55 One Domain Vocabulary
Line56 A class that uses terms from multiple domains might be violating context
Line57 independence, unless it’s part of a bridging layer.
Line58 The effect of the “context independence” rule on a system of objects is to make
Line59 their relationships explicit, deﬁned separately from the objects themselves. First,
Line60 this simpliﬁes the objects, since they don’t need to manage their own relationships.
Line61 Second, this simpliﬁes managing the relationships, since objects at the same
Line62 scale are often created and composed together in the same places, usually in
Line63 mapping-layer factory objects.
Line64 Context independence guides us towards coherent objects that can be applied
Line65 in different contexts, and towards systems that we can change by reconﬁguring
Line66 how their objects are composed.
Line67 Hiding the Right Information
Line68 Encapsulation is almost always a good thing to do, but sometimes information
Line69 can be hidden in the wrong place. This makes the code difﬁcult to understand,
Line70 to integrate, or to build behavior from by composing objects. The best defense
Line71 is to be clear about the difference between the two concepts when discussing a
Line72 design. For example, we might say:
Line73 •
Line74 “Encapsulate the data structure for the cache in the CachingAuctionLoader
Line75 class.”
Line76 •
Line77 “Encapsulate the name of the application’s log ﬁle in the PricingPolicy
Line78 class.”
Line79 These sound reasonable until we recast them in terms of information hiding:
Line80 •
Line81 “Hide the data structure used for the cache in the CachingAuctionLoader
Line82 class.”
Line83 •
Line84 “Hide the name of the application’s log ﬁle in the PricingPolicy class.”
Line85 55
Line86 Hiding the Right Information
Line87 
Line88 
Line89 ---
