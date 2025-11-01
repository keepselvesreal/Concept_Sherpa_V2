Line1 # Composite Simpler Than the Sum of Its Parts (pp.53-54)
Line2 
Line3 ---
Line4 **Page 53**
Line5 
Line6 These stereotypes are only heuristics to help us think about the design, not
Line7 hard rules, so we don’t obsess about ﬁnding just the right classiﬁcation of an
Line8 object’s peers. What matters most is the context in which the collaborating objects
Line9 are used. For example, in one application an auditing log could be a dependency,
Line10 because auditing is a legal requirement for the business and no object should be
Line11 created without an audit trail. Elsewhere, it could be a notiﬁcation, because
Line12 auditing is a user choice and objects will function perfectly well without it.
Line13 Another way to look at it is that notiﬁcations are one-way: A notiﬁcation lis-
Line14 tener may not return a value, call back the caller, or throw an exception, since
Line15 there may be other listeners further down the chain. A dependency or adjustment,
Line16 on the other hand, may do any of these, since there’s a direct relationship.
Line17 “New or new not. There is no try.”4
Line18 We try to make sure that we always create a valid object. For dependencies, this
Line19 means that we pass them in through the constructor. They’re required, so there’s
Line20 no point in creating an instance of an object until its dependencies are available,
Line21 and using the constructor enforces this constraint in the object’s deﬁnition.
Line22 Partially creating an object and then ﬁnishing it off by setting properties is brittle
Line23 because the programmer has to remember to set all the dependencies.When the
Line24 object changes to add new dependencies, the existing client code will still compile
Line25 even though it no longer constructs a valid instance. At best this will cause a
Line26 NullPointerException, at worst it will fail misleadingly.
Line27 Notiﬁcations and adjustments can be passed to the constructor as a convenience.
Line28 Alternatively, they can be initialized to safe defaults and overwritten later (note
Line29 that there is no safe default for a dependency). Adjustments can be initialized to
Line30 common values, and notiﬁcations to a null object [Woolf98] or an empty collection.
Line31 We then add methods to allow callers to change these default values, and add or
Line32 remove listeners.
Line33 Composite Simpler Than the Sum of Its Parts
Line34 All objects in a system, except for primitive types built into the language, are
Line35 composed of other objects. When composing objects into a new type, we want
Line36 the new type to exhibit simpler behavior than all of its component parts considered
Line37 together. The composite object’s API must hide the existence of its component
Line38 parts and the interactions between them, and expose a simpler abstraction to its
Line39 peers. Think of a mechanical clock: It has two or three hands for output and one
Line40 pull-out wheel for input but packages up dozens of moving parts.
Line41 4. Attributed to Yoda.
Line42 53
Line43 Composite Simpler Than the Sum of Its Parts
Line44 
Line45 
Line46 ---
Line47 
Line48 ---
Line49 **Page 54**
Line50 
Line51 In software, a user interface component for editing money values might have
Line52 two subcomponents: one for the amount and one for the currency. For the
Line53 component to be useful, its API should manage both values together, otherwise
Line54 the client code could just control it subcomponents directly.
Line55 moneyEditor.getAmountField().setText(String.valueOf(money.amount());
Line56 moneyEditor.getCurrencyField().setText(money.currencyCode());
Line57 The “Tell, Don’t Ask” convention can start to hide an object’s structure from
Line58 its clients but is not a strong enough rule by itself. For example, we could replace
Line59 the getters in the ﬁrst version with setters:
Line60 moneyEditor.setAmountField(money.amount());
Line61 moneyEditor.setCurrencyField(money.currencyCode());
Line62 This still exposes the internal structure of the component, which its client still
Line63 has to manage explicitly.
Line64 We can make the API much simpler by hiding within the component everything
Line65 about the way money values are displayed and edited, which in turn simpliﬁes
Line66 the client code:
Line67 moneyEditor.setValue(money);
Line68 This suggests a rule of thumb:
Line69 Composite Simpler Than the Sum of Its Parts
Line70 The API of a composite object should not be more complicated than that of any of
Line71 its components.
Line72 Composite objects can, of course, be used as components in larger-scale, more
Line73 sophisticated composite objects. As we grow the code, the “composite simpler
Line74 than the sum of its parts” rule contributes to raising the level of abstraction.
Line75 Context Independence
Line76 While the “composite simpler than the sum of its parts” rule helps us decide
Line77 whether an object hides enough information, the “context independence” rule
Line78 helps us decide whether an object hides too much or hides the wrong information.
Line79 A system is easier to change if its objects are context-independent; that is, if
Line80 each object has no built-in knowledge about the system in which it executes. This
Line81 allows us to take units of behavior (objects) and apply them in new situations.
Line82 To be context-independent, whatever an object needs to know about the larger
Line83 environment it’s running in must be passed in. Those relationships might be
Line84 Chapter 6
Line85 Object-Oriented Style
Line86 54
Line87 
Line88 
Line89 ---
