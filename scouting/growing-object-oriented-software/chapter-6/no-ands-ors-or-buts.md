Line1 # No And's, Or's, or But's (pp.51-52)
Line2 
Line3 ---
Line4 **Page 51**
Line5 
Line6 ((EditSaveCustomizer) master.getModelisable()
Line7   .getDockablePanel()
Line8     .getCustomizer())
Line9       .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
Line10 Every getter in this example exposes a structural detail. If we wanted to change,
Line11 say, the way customizations on the master are enabled, we’d have to change all
Line12 the intermediate relationships.
Line13 Different Levels of Language
Line14 As you’ll see in Part III, we often write helper methods to make code more readable.
Line15 We’re not afraid of adding very small methods if they clarify the meaning of the
Line16 feature they represent. We name these methods to make the calling code read
Line17 as naturally as possible; we don’t have to conform to external conventions since
Line18 these methods are only there to support other code. For example, in Chapter 15
Line19 we have a line in a test that reads:
Line20 allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING)));
Line21 We’ll explain what this means at the time. What’s relevant here is that
Line22 aSniperThatIs() is a local method that constructs a value to be passed to the
Line23 with() method, and that its name is intended to describe its intent in this context.
Line24 In effect, we’re constructing a very small embedded language that deﬁnes, in this
Line25 case, a part of a test.
Line26 As well as distinguishing between value and object types (page 13), we ﬁnd that
Line27 we tend towards different programming styles at different levels in the code.
Line28 Loosely speaking, we use the message-passing style we’ve just described between
Line29 objects, but we tend to use a more functional style within an object, building up
Line30 behavior from methods and values that have no side effects.
Line31 Features without side effects mean that we can assemble our code from smaller
Line32 components, minimizing the amount of risky shared state. Writing large-scale
Line33 functional programs is a topic for a different book, but we ﬁnd that a little
Line34 immutability within the implementation of a class leads to much safer code and
Line35 that, if we do a good job, the code reads well too.
Line36 So how do we choose the right features for an object?
Line37 No And’s, Or’s, or But’s
Line38 Every object should have a single, clearly deﬁned responsibility; this is the “single
Line39 responsibility” principle [Martin02]. When we’re adding behavior to a system,
Line40 this principle helps us decide whether to extend an existing object or create a
Line41 new service for an object to call.
Line42 51
Line43 No And’s, Or’s, or But’s
Line44 
Line45 
Line46 ---
Line47 
Line48 ---
Line49 **Page 52**
Line50 
Line51 Our heuristic is that we should be able to describe what an object does without
Line52 using any conjunctions (“and,” “or”). If we ﬁnd ourselves adding clauses to the
Line53 description, then the object probably should be broken up into collaborating
Line54 objects, usually one for each clause.
Line55 This principle also applies when we’re combining objects into new abstractions.
Line56 If we’re packaging up behavior implemented across several objects into a single
Line57 construct, we should be able to describe its responsibility clearly; there are some
Line58 related ideas below in the “Composite Simpler Than the Sum of Its Parts” and
Line59 “Context Independence” sections.
Line60 Object Peer Stereotypes
Line61 We have objects with single responsibilities, communicating with their peers
Line62 through messages in clean APIs, but what do they say to each other?
Line63 We categorize an object’s peers (loosely) into three types of relationship. An
Line64 object might have:
Line65 Dependencies
Line66 Services that the object requires from its peers so it can perform its responsi-
Line67 bilities. The object cannot function without these services. It should not be
Line68 possible to create the object without them. For example, a graphics package
Line69 will need something like a screen or canvas to draw on—it doesn’t make
Line70 sense without one.
Line71 Notiﬁcations
Line72 Peers that need to be kept up to date with the object’s activity. The object
Line73 will notify interested peers whenever it changes state or performs a signiﬁcant
Line74 action. Notiﬁcations are “ﬁre and forget”; the object neither knows nor cares
Line75 which peers are listening. Notiﬁcations are so useful because they decouple
Line76 objects from each other. For example, in a user interface system, a button
Line77 component promises to notify any registered listeners when it’s clicked, but
Line78 does not know what those listeners will do. Similarly, the listeners expect to
Line79 be called but know nothing of the way the user interface dispatches its events.
Line80 Adjustments
Line81 Peers that adjust the object’s behavior to the wider needs of the system. This
Line82 includes policy objects that make decisions on the object’s behalf (the Strat-
Line83 egy pattern in [Gamma94]) and component parts of the object if it’s a com-
Line84 posite. For example, a Swing JTable will ask a TableCellRenderer to draw
Line85 a cell’s value, perhaps as RGB (Red, Green, Blue) values for a color. If we
Line86 change the renderer, the table will change its presentation, now displaying
Line87 the HSB (Hue, Saturation, Brightness) values.
Line88 Chapter 6
Line89 Object-Oriented Style
Line90 52
Line91 
Line92 
Line93 ---
