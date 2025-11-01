Line1 # Building Up to Higher-Level Programming (pp.65-67)
Line2 
Line3 ---
Line4 **Page 65**
Line5 
Line6 assembly of components to build, in effect, a subsystem to plug into the rest of
Line7 the application. Such designs are also easy to extend—just write a new plug-
Line8 compatible component and add it in; you’ll see us write several new Hamcrest
Line9 matchers in Part III.
Line10 For example, to have jMock check that a method example.doSomething() is
Line11 called exactly once with an argument of type String, we set up our test context
Line12 like this:
Line13 InvocationExpectation expectation = new InvocationExpectation();
Line14 expectation.setParametersMatcher(
Line15   new AllParametersMatcher(Arrays.asList(new IsInstanceOf(String.class)));
Line16 expectation.setCardinality(new Cardinality(1, 1));
Line17 expectation.setMethodMatcher(new MethodNameMatcher("doSomething"));
Line18 expectation.setObjectMatcher(new IsSame<Example>(example));
Line19 context.addExpectation(expectation);
Line20 Building Up to Higher-Level Programming
Line21 You have probably spotted a difﬁculty with the code fragment above: it doesn’t
Line22 explain very well what the expectation is testing. Conceptually, assembling a
Line23 web of objects is straightforward. Unfortunately, the mainstream languages we
Line24 usually work with bury the information we care about (objects and their relation-
Line25 ships) in a morass of keywords, setters, punctuation, and the like. Just assigning
Line26 and linking objects, as in this example, doesn’t help us understand the behavior
Line27 of the system we’re assembling—it doesn’t express our intent.2
Line28 Our response is to organize the code into two layers: an implementation layer
Line29 which is the graph of objects, its behavior is the combined result of how its objects
Line30 respond to events; and, a declarative layer which builds up the objects in the
Line31 implementation layer, using small “sugar” methods and syntax to describe
Line32 the purpose of each fragment. The declarative layer describes what the code will
Line33 do, while the implementation layer describes how the code does it. The declarative
Line34 layer is, in effect, a small domain-speciﬁc language embedded (in this case)
Line35 in Java.3
Line36 The different purposes of the two layers mean that we use a different coding
Line37 style for each. For the implementation layer we stick to the conventional object-
Line38 oriented style guidelines we described in the previous chapter. We’re more ﬂexible
Line39 for the declarative layer—we might even use “train wreck” chaining of method
Line40 calls or static methods to help get the point across.
Line41 A good example is jMock itself. We can rewrite the example from the previous
Line42 section as:
Line43 2. Nor does the common alternative of moving the object construction into a separate
Line44 XML ﬁle.
Line45 3. This became clear to us when working on jMock. We wrote up our experiences in
Line46 [Freeman06].
Line47 65
Line48 Building Up to Higher-Level Programming
Line49 
Line50 
Line51 ---
Line52 
Line53 ---
Line54 **Page 66**
Line55 
Line56 context.checking(new Expectations() {{
Line57     oneOf(example).doSomething(with(any(String.class)));
Line58 }});
Line59 The Expectations object is a Builder [Gamma94] that constructs expectations.
Line60 It deﬁnes “sugar” methods that construct the assembly of expectations and
Line61 matchers and load it into the Mockery, as shown in Figure 7.2.
Line62 Figure 7.2
Line63 A syntax-layer constructs the interpreter
Line64 Most of the time, such a declarative layer emerges from continual “merciless”
Line65 refactoring. We start by writing code that directly composes objects and keep
Line66 factoring out duplication. We also add helper methods to push the syntax noise
Line67 out of the main body of the code and to add explanation. Taking care to notice
Line68 when an area of code is not clear, we add or move structure until it is; this is
Line69 very easy to do in a modern refactoring IDE. Eventually, we ﬁnd we have our
Line70 two-layer structure. Occasionally, we start from the declarative code we’d like
Line71 to have and work down to ﬁll in its implementation, as we do with the ﬁrst
Line72 end-to-end test in Chapter 10.
Line73 Our purpose, in the end, is to achieve more with less code. We aspire to raise
Line74 ourselves from programming in terms of control ﬂow and data manipulation, to
Line75 composing programs from smaller programs—where objects form the smallest
Line76 unit of behavior. None of this is new—it’s the same concept as programming
Line77 Unix by composing utilities with pipes [Kernighan76],4 or building up layers of
Line78 language in Lisp [Graham93]—but we still don’t see it in the ﬁeld as often as we
Line79 would like.
Line80 4. Kernighan and Plauger attribute the idea of pipes to Douglas McIlroy, who wrote a
Line81 memo in 1964 suggesting the metaphor of data passing through a segmented garden
Line82 hose. It’s currently available at http://plan9.bell-labs.com/who/dmr/mdmpipe.pdf.
Line83 Chapter 7
Line84 Achieving Object-Oriented Design
Line85 66
Line86 
Line87 
Line88 ---
Line89 
Line90 ---
Line91 **Page 67**
Line92 
Line93 And What about Classes?
Line94 One last point. Unusually for a book on object-oriented software, we haven’t
Line95 said much about classes and inheritance. It should be obvious by now that we’ve
Line96 been pushing the application domain into the gaps between the objects, the
Line97 communication protocols. We emphasize interfaces more than classes because
Line98 that’s what other objects see: an object’s type is deﬁned by the roles it plays.
Line99 We view classes for objects as an “implementation detail”—a way of imple-
Line100 menting types, not the types themselves. We discover object class hierarchies by
Line101 factoring out common behavior, but prefer to refactor to delegation if possible
Line102 since we ﬁnd that it makes our code more ﬂexible and easier to understand.5
Line103 Value types, on the other hand, are less likely to use delegation since they don’t
Line104 have peers.
Line105 There’s plenty of good advice on how to work with classes in, for example,
Line106 [Fowler99], [Kerievsky04], and [Evans03].
Line107 5. The design forces, of course, are different in languages that support multiple
Line108 inheritance well, such as Eiffel [Meyer91].
Line109 67
Line110 And What about Classes?
Line111 
Line112 
Line113 ---
