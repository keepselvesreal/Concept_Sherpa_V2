Line1 # Follow the Messages (pp.14-17)
Line2 
Line3 ---
Line4 **Page 14**
Line5 
Line6 Figure 2.1
Line7 A web of objects
Line8 object-oriented languages that most of us use, the confusion is that both concepts
Line9 are implemented by the same language construct: classes.
Line10 Values are immutable instances that model ﬁxed quantities. They have no in-
Line11 dividual identity, so two value instances are effectively the same if they have the
Line12 same state. This means that it makes no sense to compare the identity of two
Line13 values; doing so can cause some subtle bugs—think of the different ways of
Line14 comparing two copies of new Integer(999). That’s why we’re taught to use
Line15 string1.equals(string2) in Java rather than string1 == string2.
Line16 Objects, on the other hand, use mutable state to model their behavior over
Line17 time. Two objects of the same type have separate identities even if they have ex-
Line18 actly the same state now, because their states can diverge if they receive different
Line19 messages in the future.
Line20 In practice, this means that we split our system into two “worlds”: values,
Line21 which are treated functionally, and objects, which implement the stateful behavior
Line22 of the system. In Part III, you’ll see how our coding style varies depending on
Line23 which world we’re working in.
Line24 In this book, we will use the term object to refer only to instances with identity,
Line25 state, and processing—not values. There doesn’t appear to be another accepted
Line26 term that isn’t overloaded with other meanings (such as entity and process).
Line27 Follow the Messages
Line28 We can beneﬁt from this high-level, declarative approach only if our objects are
Line29 designed to be easily pluggable. In practice, this means that they follow common
Line30 communication patterns and that the dependencies between them are made ex-
Line31 plicit. A communication pattern is a set of rules that govern how a group of ob-
Line32 jects talk to each other: the roles they play, what messages they can send and
Line33 when, and so on. In languages like Java, we identify object roles with (abstract)
Line34 interfaces, rather than (concrete) classes—although interfaces don’t deﬁne
Line35 everything we need to say.
Line36 Chapter 2
Line37 Test-Driven Development with Objects
Line38 14
Line39 
Line40 
Line41 ---
Line42 
Line43 ---
Line44 **Page 15**
Line45 
Line46 In our view, the domain model is in these communication patterns, because
Line47 they are what gives meaning to the universe of possible relationships between
Line48 the objects. Thinking of a system in terms of its dynamic, communication structure
Line49 is a signiﬁcant mental shift from the static classiﬁcation that most of us learn
Line50 when being introduced to objects. The domain model isn’t even obviously visible
Line51 because the communication patterns are not explicitly represented in the program-
Line52 ming languages we get to work with. We hope to show, in this book, how tests
Line53 and mock objects help us see the communication between our objects more
Line54 clearly.
Line55 Here’s a small example of how focusing on the communication between objects
Line56 guides design.
Line57 In a video game, the objects in play might include: actors, such as the player
Line58 and the enemies; scenery, which the player ﬂies over; obstacles, which the
Line59 player can crash into; and effects, such as explosions and smoke. There are also
Line60 scripts spawning objects behind the scenes as the game progresses.
Line61 This is a good classiﬁcation of the game objects from the players’ point of view
Line62 because it supports the decisions they need to make when playing the game—when
Line63 interacting with the game from outside. This is not, however, a useful classiﬁcation
Line64 for the implementers of the game. The game engine has to display objects that
Line65 are visible, tell objects that are animated about the passing of time, detect colli-
Line66 sions between objects that are physical, and delegate decisions about what to do
Line67 when physical objects collide to collision resolvers.
Line68 Figure 2.2
Line69 Roles and objects in a video game
Line70 As you can see in Figure 2.2, the two views, one from the game engine and
Line71 one from the implementation of the in-play objects, are not the same. An Obstacle,
Line72 for example, is Visible and Physical, while a Script is a Collision Resolver and
Line73 Animated but not Visible. The objects in the game play different roles depending
Line74 15
Line75 Follow the Messages
Line76 
Line77 
Line78 ---
Line79 
Line80 ---
Line81 **Page 16**
Line82 
Line83 on what the engine needs from them at the time. This mismatch between static
Line84 classiﬁcation and dynamic communication means that we’re unlikely to come
Line85 up with a tidy class hierarchy for the game objects that will also suit the needs
Line86 of the engine.
Line87 At best, a class hierarchy represents one dimension of an application, providing
Line88 a mechanism for sharing implementation details between objects; for example,
Line89 we might have a base class to implement the common features of frame-based
Line90 animation. At worst, we’ve seen too many codebases (including our own) that
Line91 suffer complexity and duplication from using one mechanism to represent multiple
Line92 concepts.
Line93 Roles, Responsibilities, Collaborators
Line94 We try to think about objects in terms of roles, responsibilities, and collaborators,
Line95 as best described by Wirfs-Brock and McKean in [Wirfs-Brock03]. An object is an
Line96 implementation of one or more roles; a role is a set of related responsibilities;
Line97 and a responsibility is an obligation to perform a task or know information. A
Line98 collaboration is an interaction of objects or roles (or both).
Line99 Sometimes we step away from the keyboard and use an informal design technique
Line100 that Wirfs-Brock and McKean describe, called CRC cards (Candidates, Responsi-
Line101 bilities, Collaborators). The idea is to use low-tech index cards to explore the po-
Line102 tential object structure of an application, or a part of it. These index cards allow
Line103 us to experiment with structure without getting stuck in detail or becoming too
Line104 attached to an early solution.
Line105 Figure 2.3
Line106 CRC card for a video game
Line107 Chapter 2
Line108 Test-Driven Development with Objects
Line109 16
Line110 
Line111 
Line112 ---
Line113 
Line114 ---
Line115 **Page 17**
Line116 
Line117 Tell, Don’t Ask
Line118 We have objects sending each other messages, so what do they say? Our experi-
Line119 ence is that the calling object should describe what it wants in terms of the role
Line120 that its neighbor plays, and let the called object decide how to make that happen.
Line121 This is commonly known as the “Tell, Don’t Ask” style or, more formally, the
Line122 Law of Demeter. Objects make their decisions based only on the information
Line123 they hold internally or that which came with the triggering message; they avoid
Line124 navigating to other objects to make things happen. Followed consistently, this
Line125 style produces more ﬂexible code because it’s easy to swap objects that play the
Line126 same role. The caller sees nothing of their internal structure or the structure of
Line127 the rest of the system behind the role interface.
Line128 When we don’t follow the style, we can end up with what’s known as “train
Line129 wreck” code, where a series of getters is chained together like the carriages in a
Line130 train. Here’s one case we found on the Internet:
Line131 ((EditSaveCustomizer) master.getModelisable()
Line132   .getDockablePanel()
Line133     .getCustomizer())
Line134       .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
Line135 After some head scratching, we realized what this fragment was meant to say:
Line136 master.allowSavingOfCustomisations();
Line137 This wraps all that implementation detail up behind a single call. The client of
Line138 master no longer needs to know anything about the types in the chain. We’ve
Line139 reduced the risk that a design change might cause ripples in remote parts of the
Line140 codebase.
Line141 As well as hiding information, there’s a more subtle beneﬁt from “Tell, Don’t
Line142 Ask.” It forces us to make explicit and so name the interactions between objects,
Line143 rather than leaving them implicit in the chain of getters. The shorter version
Line144 above is much clearer about what it’s for, not just how it happens to be
Line145 implemented.
Line146 But Sometimes Ask
Line147 Of course we don’t “tell” everything;1 we “ask” when getting information from
Line148 values and collections, or when using a factory to create new objects. Occasion-
Line149 ally, we also ask objects about their state when searching or ﬁltering, but we still
Line150 want to maintain expressiveness and avoid “train wrecks.”
Line151 For example (to continue with the metaphor), if we naively wanted to spread
Line152 reserved seats out across the whole of a train, we might start with something like:
Line153 1. Although that’s an interesting exercise to try, to stretch your technique.
Line154 17
Line155 But Sometimes Ask
Line156 
Line157 
Line158 ---
