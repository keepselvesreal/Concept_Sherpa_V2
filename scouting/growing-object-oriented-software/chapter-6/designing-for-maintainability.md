Line1 # Designing for Maintainability (pp.47-50)
Line2 
Line3 ---
Line4 **Page 47**
Line5 
Line6 Chapter 6
Line7 Object-Oriented Style
Line8 Always design a thing by considering it in its next larger
Line9 context—a chair in a room, a room in a house, a house in an
Line10 environment, an environment in a city plan.
Line11 —Eliel Saarinen
Line12 Introduction
Line13 So far in Part II, we’ve talked about how to get started with the development
Line14 process and how to keep going. Now we want to take a more detailed look at
Line15 our design goals and our use of TDD, and in particular mock objects, to guide
Line16 the structure of our code.
Line17 We value code that is easy to maintain over code that is easy to write.1 Imple-
Line18 menting a feature in the most direct way can damage the maintainability of the
Line19 system, for example by making the code difﬁcult to understand or by introducing
Line20 hidden dependencies between components. Balancing immediate and longer-term
Line21 concerns is often tricky, but we’ve seen too many teams that can no longer deliver
Line22 because their system is too brittle.
Line23 In this chapter, we want to show something of what we’re trying to achieve
Line24 when we design software, and how that looks in an object-oriented language;
Line25 this is the “opinionated” part of our approach to software. In the next chapter,
Line26 we’ll look at the mechanics of how to guide code in this direction with TDD.
Line27 Designing for Maintainability
Line28 Following the process we described in Chapter 5, we grow our systems a slice of
Line29 functionality at a time. As the code scales up, the only way we can continue to
Line30 understand and maintain it is by structuring the functionality into objects, objects
Line31 into packages,2 packages into programs, and programs into systems. We use two
Line32 principal heuristics to guide this structuring:
Line33 1. As the Agile Manifesto might have put it.
Line34 2. We’re being vague about the meaning of “package” here since we want it to include
Line35 concepts such as modules, libraries, and namespaces, which tend to be confounded
Line36 in the Java world—but you know what we mean.
Line37 47
Line38 
Line39 
Line40 ---
Line41 
Line42 ---
Line43 **Page 48**
Line44 
Line45 Separation of concerns
Line46 When we have to change the behavior of a system, we want to change as
Line47 little code as possible. If all the relevant changes are in one area of code, we
Line48 don’t have to hunt around the system to get the job done. Because we cannot
Line49 predict when we will have to change any particular part of the system, we
Line50 gather together code that will change for the same reason. For example, code
Line51 to unpack messages from an Internet standard protocol will not change for
Line52 the same reasons as business code that interprets those messages, so we
Line53 partition the two concepts into different packages.
Line54 Higher levels of abstraction
Line55 The only way for humans to deal with complexity is to avoid it, by working
Line56 at higher levels of abstraction. We can get more done if we program by
Line57 combining components of useful functionality rather than manipulating
Line58 variables and control ﬂow; that’s why most people order food from a menu
Line59 in terms of dishes, rather than detail the recipes used to create them.
Line60 Applied consistently, these two forces will push the structure of an appli-
Line61 cation towards something like Cockburn’s “ports and adapters” architecture
Line62 [Cockburn08], in which the code for the business domain is isolated from its
Line63 dependencies on technical infrastructure, such as databases and user interfaces.
Line64 We don’t want technical concepts to leak into the application model, so we write
Line65 interfaces to describe its relationships with the outside world in its terminology
Line66 (Cockburn’s ports). Then we write bridges between the application core and each
Line67 technical domain (Cockburn’s adapters). This is related to what Eric Evans calls
Line68 an “anticorruption layer” [Evans03].
Line69 The bridges implement the interfaces deﬁned by the application model and
Line70 map between application-level and technical-level objects (Figure 6.1). For exam-
Line71 ple, a bridge might map an order book object to SQL statements so that orders
Line72 are persisted in a database. To do so, it might query values from the application
Line73 object or use an object-relational tool like Hibernate3 to pull values out of objects
Line74 using Java reﬂection. We’ll show an example of refactoring to this architecture
Line75 in Chapter 17.
Line76 The next question is how to ﬁnd the facets in the behavior where the interfaces
Line77 should be, so that we can divide up the code cleanly. We have some second-level
Line78 heuristics to help us think about that.
Line79 3. http://www.hibernate.org
Line80 Chapter 6
Line81 Object-Oriented Style
Line82 48
Line83 
Line84 
Line85 ---
Line86 
Line87 ---
Line88 **Page 49**
Line89 
Line90 Figure 6.1
Line91 An application’s core domain model is mapped onto
Line92 technical infrastructure
Line93 Encapsulation and Information Hiding
Line94 We want to be careful with the distinction between “encapsulation” and “information
Line95 hiding.” The terms are often used interchangeably but actually refer to two separate,
Line96 and largely orthogonal, qualities:
Line97 Encapsulation
Line98 Ensures that the behavior of an object can only be affected through its API.
Line99 It lets us control how much a change to one object will impact other parts of
Line100 the system by ensuring that there are no unexpected dependencies between
Line101 unrelated components.
Line102 Information hiding
Line103 Conceals how an object implements its functionality behind the abstraction
Line104 of its API. It lets us work with higher abstractions by ignoring lower-level details
Line105 that are unrelated to the task at hand.
Line106 We’re most aware of encapsulation when we haven’t got it. When working with
Line107 badly encapsulated code, we spend too much time tracing what the potential
Line108 effects of a change might be, looking at where objects are created, what common
Line109 data they hold, and where their contents are referenced. The topic has inspired
Line110 two books that we know of, [Feathers04] and [Demeyer03].
Line111 49
Line112 Designing for Maintainability
Line113 
Line114 
Line115 ---
Line116 
Line117 ---
Line118 **Page 50**
Line119 
Line120 Many object-oriented languages support encapsulation by providing control over
Line121 the visibility of an object’s features to other objects, but that’s not enough. Objects
Line122 can break encapsulation by sharing references to mutable objects, an effect known
Line123 as aliasing. Aliasing is essential for conventional object- oriented systems (other-
Line124 wise no two objects would be able to communicate), but accidental aliasing can
Line125 couple unrelated parts of a system so it behaves mysteriously and is inﬂexible to
Line126 change.
Line127 We follow standard practices to maintain encapsulation when coding: deﬁne
Line128 immutable value types, avoid global variables and singletons, copy collections
Line129 and mutable values when passing them between objects, and so on. We have
Line130 more about information hiding later in this chapter.
Line131 Internals vs. Peers
Line132 As we organize our system, we must decide what is inside and outside each object,
Line133 so that the object provides a coherent abstraction with a clear API. Much of the
Line134 point of an object, as we discussed above, is to encapsulate access to its internals
Line135 through its API and to hide these details from the rest of the system. An object
Line136 communicates with other objects in the system by sending and receiving messages,
Line137 as in Figure 6.2; the objects it communicates with directly are its peers.
Line138 Figure 6.2
Line139 Objects communicate by sending and receiving messages
Line140 This decision matters because it affects how easy an object is to use, and so
Line141 contributes to the internal quality of the system. If we expose too much of an
Line142 object’s internals through its API, its clients will end up doing some of its work.
Line143 We’ll have distributed behavior across too many objects (they’ll be coupled to-
Line144 gether), increasing the cost of maintenance because any changes will now ripple
Line145 across the code. This is the effect of the “train wreck” example on page 17:
Line146 Chapter 6
Line147 Object-Oriented Style
Line148 50
Line149 
Line150 
Line151 ---
