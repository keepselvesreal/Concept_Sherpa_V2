Line1 # Value Types (pp.59-60)
Line2 
Line3 ---
Line4 **Page 59**
Line5 
Line6 Value Types
Line7 Before we go further, we want to revisit the distinction we described in “Values
Line8 and Objects” (page 13): values are immutable, so they’re simpler and have no
Line9 meaningful identity; objects have state, so they have identity and relationships
Line10 with each other.
Line11 The more code we write, the more we’re convinced that we should deﬁne
Line12 types to represent value concepts in the domain, even if they don’t do much. It
Line13 helps to create a consistent domain model that is more self-explanatory. If we
Line14 create, for example, an Item type in a system, instead of just using String, we can
Line15 ﬁnd all the code that’s relevant for a change without having to chase through the
Line16 method calls. Speciﬁc types also reduce the risk of confusion—as the Mars Climate
Line17 Orbiter disaster showed, feet and metres may both be represented as numbers
Line18 but they’re different things.1 Finally, once we have a type to represent a concept,
Line19 it usually turns out to be a good place to hang behavior, guiding us towards using
Line20 a more object-oriented approach instead of scattering related behavior across
Line21 the code.
Line22 We use three basic techniques for introducing value types, which we’ve called
Line23 (in a ﬁt of alliteration): breaking out, budding off, and bundling up.
Line24 Breaking out
Line25 When we ﬁnd that the code in an object is becoming complex, that’s often
Line26 a sign that it’s implementing multiple concerns and that we can break out
Line27 coherent units of behavior into helper types. There’s an example in “Tidying
Line28 Up the Translator” (page 135) where we break a class that handles incoming
Line29 messages into two parts: one to parse the message string, and one to interpret
Line30 the result of the parsing.
Line31 Budding off
Line32 When we want to mark a new domain concept in the code, we often introduce
Line33 a placeholder type that wraps a single ﬁeld, or maybe has no ﬁelds at all. As
Line34 the code grows, we ﬁll in more detail in the new type by adding ﬁelds and
Line35 methods. With each type that we add, we’re raising the level of abstraction
Line36 of the code.
Line37 Bundling up
Line38 When we notice that a group of values are always used together, we take
Line39 that as a suggestion that there’s a missing construct. A ﬁrst step might be to
Line40 create a new type with ﬁxed public ﬁelds—just giving the group a name
Line41 highlights the missing concept. Later we can migrate behavior to the new
Line42 1. In 1999, NASA’s Mars Climate Orbiter burned up in the planet’s atmosphere because,
Line43 amongst other problems, the navigation software confused metric with imperial units.
Line44 There’s a brief description at http://news.bbc.co.uk/1/hi/sci/tech/514763.stm.
Line45 59
Line46 Value Types
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 60**
Line53 
Line54 type, which might eventually allow us to hide its ﬁelds behind a clean
Line55 interface, satisfying the “composite simpler than the sum of its parts” rule.
Line56 We ﬁnd that the discovery of value types is usually motivated by trying to
Line57 follow our design principles, rather than by responding to code stresses when
Line58 writing tests.
Line59 Where Do Objects Come From?
Line60 The categories for discovering object types are similar (which is why we shoe-
Line61 horned them into these names), except that the design guidance we get from
Line62 writing unit tests tends to be more important. As we wrote in “External and
Line63 Internal Quality” (page 10), we use the effort of unit testing to maintain the
Line64 code’s internal quality. There are more examples of the inﬂuence of testing on
Line65 design in Chapter 20.
Line66 Breaking Out: Splitting a Large Object into a Group of
Line67 Collaborating Objects
Line68 When starting a new area of code, we might temporarily suspend our design
Line69 judgment and just write code without attempting to impose much structure. This
Line70 allows us to gain some experience in the area and test our understanding of any
Line71 external APIs we’re developing against. After a short while, we’ll ﬁnd our code
Line72 becoming too complex to understand and will want to clean it up. We can start
Line73 pulling out cohesive units of functionality into smaller collaborating objects,
Line74 which we can then unit-test independently. Splitting out a new object also forces
Line75 us to look at the dependencies of the code we’re pulling out.
Line76 We have two concerns about deferring cleanup. The ﬁrst is how long we should
Line77 wait before doing something. Under time pressure, it’s tempting to leave the un-
Line78 structured code as is and move on to the next thing (“after all, it works and it’s
Line79 just one class…”). We’ve seen too much code where the intention wasn’t clear
Line80 and the cost of cleanup kicked in when the team could least afford it. The second
Line81 concern is that occasionally it’s better to treat this code as a spike—once we
Line82 know what to do, just roll it back and reimplement cleanly. Code isn’t sacred
Line83 just because it exists, and the second time won’t take as long.
Line84 The Tests Say…
Line85 Break up an object if it becomes too large to test easily, or if its test failures become
Line86 difﬁcult to interpret. Then unit-test the new parts separately.
Line87 Chapter 7
Line88 Achieving Object-Oriented Design
Line89 60
Line90 
Line91 
Line92 ---
