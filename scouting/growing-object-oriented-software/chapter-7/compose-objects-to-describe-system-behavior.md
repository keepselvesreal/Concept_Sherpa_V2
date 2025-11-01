Line1 # Compose Objects to Describe System Behavior (pp.64-65)
Line2 
Line3 ---
Line4 **Page 64**
Line5 
Line6 malleable because more components will be “plug-compatible,” so we can work
Line7 at a higher level of abstraction. For the developer, there’s a secondary advantage
Line8 that there will be fewer concepts that cost time to understand.
Line9 Alternatively, if similar interfaces turn out to represent different concepts, we
Line10 can make a point of making them distinct, so that the compiler can ensure that
Line11 we only combine objects correctly. A decision to separate similar-looking inter-
Line12 faces is a good time to reconsider their naming. It’s likely that there’s a more
Line13 appropriate name for at least one of them.
Line14 Finally, another time to consider refactoring interfaces is when we start imple-
Line15 menting them. For example, if we ﬁnd that the structure of an implementing class
Line16 is unclear, perhaps it has too many responsibilities which might be a hint that
Line17 the interface is unfocused too and should be split up.
Line18 Compose Objects to Describe System Behavior
Line19 TDD at the unit level guides us to decompose our system into value types and
Line20 loosely coupled computational objects. The tests give us a good understanding
Line21 of how each object behaves and how it can be combined with others. We then
Line22 use lower-level objects as the building blocks of more capable objects; this is the
Line23 web of objects we described in Chapter 2.
Line24 In jMock, for example, we assemble a description of the expected calls for a
Line25 test in a context object called a Mockery. During a test run, the Mockery will pass
Line26 calls made to any of its mocked objects to its Expectations, each of which will
Line27 attempt to match the call. If an Expectation matches, that part of the test suc-
Line28 ceeds. If none matches, then each Expectation reports its disagreement and the
Line29 test fails. At runtime, the assembled objects look like Figure 7.1:
Line30 Figure 7.1
Line31 jMock Expectations are assembled from many objects
Line32 The advantage of this approach is that we end up with a ﬂexible application
Line33 structure built from relatively little code. It’s particularly suitable where the code
Line34 has to support many related scenarios. For each scenario, we provide a different
Line35 Chapter 7
Line36 Achieving Object-Oriented Design
Line37 64
Line38 
Line39 
Line40 ---
Line41 
Line42 ---
Line43 **Page 65**
Line44 
Line45 assembly of components to build, in effect, a subsystem to plug into the rest of
Line46 the application. Such designs are also easy to extend—just write a new plug-
Line47 compatible component and add it in; you’ll see us write several new Hamcrest
Line48 matchers in Part III.
Line49 For example, to have jMock check that a method example.doSomething() is
Line50 called exactly once with an argument of type String, we set up our test context
Line51 like this:
Line52 InvocationExpectation expectation = new InvocationExpectation();
Line53 expectation.setParametersMatcher(
Line54   new AllParametersMatcher(Arrays.asList(new IsInstanceOf(String.class)));
Line55 expectation.setCardinality(new Cardinality(1, 1));
Line56 expectation.setMethodMatcher(new MethodNameMatcher("doSomething"));
Line57 expectation.setObjectMatcher(new IsSame<Example>(example));
Line58 context.addExpectation(expectation);
Line59 Building Up to Higher-Level Programming
Line60 You have probably spotted a difﬁculty with the code fragment above: it doesn’t
Line61 explain very well what the expectation is testing. Conceptually, assembling a
Line62 web of objects is straightforward. Unfortunately, the mainstream languages we
Line63 usually work with bury the information we care about (objects and their relation-
Line64 ships) in a morass of keywords, setters, punctuation, and the like. Just assigning
Line65 and linking objects, as in this example, doesn’t help us understand the behavior
Line66 of the system we’re assembling—it doesn’t express our intent.2
Line67 Our response is to organize the code into two layers: an implementation layer
Line68 which is the graph of objects, its behavior is the combined result of how its objects
Line69 respond to events; and, a declarative layer which builds up the objects in the
Line70 implementation layer, using small “sugar” methods and syntax to describe
Line71 the purpose of each fragment. The declarative layer describes what the code will
Line72 do, while the implementation layer describes how the code does it. The declarative
Line73 layer is, in effect, a small domain-speciﬁc language embedded (in this case)
Line74 in Java.3
Line75 The different purposes of the two layers mean that we use a different coding
Line76 style for each. For the implementation layer we stick to the conventional object-
Line77 oriented style guidelines we described in the previous chapter. We’re more ﬂexible
Line78 for the declarative layer—we might even use “train wreck” chaining of method
Line79 calls or static methods to help get the point across.
Line80 A good example is jMock itself. We can rewrite the example from the previous
Line81 section as:
Line82 2. Nor does the common alternative of moving the object construction into a separate
Line83 XML ﬁle.
Line84 3. This became clear to us when working on jMock. We wrote up our experiences in
Line85 [Freeman06].
Line86 65
Line87 Building Up to Higher-Level Programming
Line88 
Line89 
Line90 ---
