Line1 # Introduction (pp.47-47)
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
