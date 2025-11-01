Line1 # Object Peer Stereotypes (pp.52-53)
Line2 
Line3 ---
Line4 **Page 52**
Line5 
Line6 Our heuristic is that we should be able to describe what an object does without
Line7 using any conjunctions (“and,” “or”). If we ﬁnd ourselves adding clauses to the
Line8 description, then the object probably should be broken up into collaborating
Line9 objects, usually one for each clause.
Line10 This principle also applies when we’re combining objects into new abstractions.
Line11 If we’re packaging up behavior implemented across several objects into a single
Line12 construct, we should be able to describe its responsibility clearly; there are some
Line13 related ideas below in the “Composite Simpler Than the Sum of Its Parts” and
Line14 “Context Independence” sections.
Line15 Object Peer Stereotypes
Line16 We have objects with single responsibilities, communicating with their peers
Line17 through messages in clean APIs, but what do they say to each other?
Line18 We categorize an object’s peers (loosely) into three types of relationship. An
Line19 object might have:
Line20 Dependencies
Line21 Services that the object requires from its peers so it can perform its responsi-
Line22 bilities. The object cannot function without these services. It should not be
Line23 possible to create the object without them. For example, a graphics package
Line24 will need something like a screen or canvas to draw on—it doesn’t make
Line25 sense without one.
Line26 Notiﬁcations
Line27 Peers that need to be kept up to date with the object’s activity. The object
Line28 will notify interested peers whenever it changes state or performs a signiﬁcant
Line29 action. Notiﬁcations are “ﬁre and forget”; the object neither knows nor cares
Line30 which peers are listening. Notiﬁcations are so useful because they decouple
Line31 objects from each other. For example, in a user interface system, a button
Line32 component promises to notify any registered listeners when it’s clicked, but
Line33 does not know what those listeners will do. Similarly, the listeners expect to
Line34 be called but know nothing of the way the user interface dispatches its events.
Line35 Adjustments
Line36 Peers that adjust the object’s behavior to the wider needs of the system. This
Line37 includes policy objects that make decisions on the object’s behalf (the Strat-
Line38 egy pattern in [Gamma94]) and component parts of the object if it’s a com-
Line39 posite. For example, a Swing JTable will ask a TableCellRenderer to draw
Line40 a cell’s value, perhaps as RGB (Red, Green, Blue) values for a color. If we
Line41 change the renderer, the table will change its presentation, now displaying
Line42 the HSB (Hue, Saturation, Brightness) values.
Line43 Chapter 6
Line44 Object-Oriented Style
Line45 52
Line46 
Line47 
Line48 ---
Line49 
Line50 ---
Line51 **Page 53**
Line52 
Line53 These stereotypes are only heuristics to help us think about the design, not
Line54 hard rules, so we don’t obsess about ﬁnding just the right classiﬁcation of an
Line55 object’s peers. What matters most is the context in which the collaborating objects
Line56 are used. For example, in one application an auditing log could be a dependency,
Line57 because auditing is a legal requirement for the business and no object should be
Line58 created without an audit trail. Elsewhere, it could be a notiﬁcation, because
Line59 auditing is a user choice and objects will function perfectly well without it.
Line60 Another way to look at it is that notiﬁcations are one-way: A notiﬁcation lis-
Line61 tener may not return a value, call back the caller, or throw an exception, since
Line62 there may be other listeners further down the chain. A dependency or adjustment,
Line63 on the other hand, may do any of these, since there’s a direct relationship.
Line64 “New or new not. There is no try.”4
Line65 We try to make sure that we always create a valid object. For dependencies, this
Line66 means that we pass them in through the constructor. They’re required, so there’s
Line67 no point in creating an instance of an object until its dependencies are available,
Line68 and using the constructor enforces this constraint in the object’s deﬁnition.
Line69 Partially creating an object and then ﬁnishing it off by setting properties is brittle
Line70 because the programmer has to remember to set all the dependencies.When the
Line71 object changes to add new dependencies, the existing client code will still compile
Line72 even though it no longer constructs a valid instance. At best this will cause a
Line73 NullPointerException, at worst it will fail misleadingly.
Line74 Notiﬁcations and adjustments can be passed to the constructor as a convenience.
Line75 Alternatively, they can be initialized to safe defaults and overwritten later (note
Line76 that there is no safe default for a dependency). Adjustments can be initialized to
Line77 common values, and notiﬁcations to a null object [Woolf98] or an empty collection.
Line78 We then add methods to allow callers to change these default values, and add or
Line79 remove listeners.
Line80 Composite Simpler Than the Sum of Its Parts
Line81 All objects in a system, except for primitive types built into the language, are
Line82 composed of other objects. When composing objects into a new type, we want
Line83 the new type to exhibit simpler behavior than all of its component parts considered
Line84 together. The composite object’s API must hide the existence of its component
Line85 parts and the interactions between them, and expose a simpler abstraction to its
Line86 peers. Think of a mechanical clock: It has two or three hands for output and one
Line87 pull-out wheel for input but packages up dozens of moving parts.
Line88 4. Attributed to Yoda.
Line89 53
Line90 Composite Simpler Than the Sum of Its Parts
Line91 
Line92 
Line93 ---
