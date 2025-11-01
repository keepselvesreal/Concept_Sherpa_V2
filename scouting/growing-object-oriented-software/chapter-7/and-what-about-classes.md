Line1 # And What about Classes? (pp.67-68)
Line2 
Line3 ---
Line4 **Page 67**
Line5 
Line6 And What about Classes?
Line7 One last point. Unusually for a book on object-oriented software, we haven’t
Line8 said much about classes and inheritance. It should be obvious by now that we’ve
Line9 been pushing the application domain into the gaps between the objects, the
Line10 communication protocols. We emphasize interfaces more than classes because
Line11 that’s what other objects see: an object’s type is deﬁned by the roles it plays.
Line12 We view classes for objects as an “implementation detail”—a way of imple-
Line13 menting types, not the types themselves. We discover object class hierarchies by
Line14 factoring out common behavior, but prefer to refactor to delegation if possible
Line15 since we ﬁnd that it makes our code more ﬂexible and easier to understand.5
Line16 Value types, on the other hand, are less likely to use delegation since they don’t
Line17 have peers.
Line18 There’s plenty of good advice on how to work with classes in, for example,
Line19 [Fowler99], [Kerievsky04], and [Evans03].
Line20 5. The design forces, of course, are different in languages that support multiple
Line21 inheritance well, such as Eiffel [Meyer91].
Line22 67
Line23 And What about Classes?
Line24 
Line25 
Line26 ---
Line27 
Line28 ---
Line29 **Page 68**
Line30 
Line31 This page intentionally left blank
