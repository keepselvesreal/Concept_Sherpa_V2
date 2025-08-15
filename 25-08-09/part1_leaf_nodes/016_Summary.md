# Summary

**ID**: 16  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

Summary
 Complexity in the context of this book means hard to understand.
 We use the terms code and behavior interchangeably.
 DOP stands for data-oriented programming.
 OOP stands for object-oriented programming.
 FP stands for functional programming.
 In a composition relation, when one object dies, the other one also dies.
 A composition relation is represented by a plain diamond at one edge and an
optional star at the other edge.
 In an association relation, each object has an independent life cycle.
 A many-to-many association relation is represented by an empty diamond and a
star at both edges.
 Dashed arrows indicate a usage relation; for instance, when a class uses a method
of another class.
 Plain arrows with empty triangles represent class inheritance, where the arrow
points towards the superclass.
 The design presented in this chapter doesn’t pretend to be the smartest OOP
design. Experienced OOP developers would probably use a couple of design
patterns and suggest a much better diagram.

## 페이지 53

Summary 25
 Traditional OOP systems tend to increase system complexity, in the sense that
OOP systems are hard to understand.
 In traditional OOP, code and data are mixed together in classes: data as mem-
bers and code as methods.
 In traditional OOP, data is mutable.
 The root cause of the increase in complexity is related to the mixing of code
and data together into objects.
 When code and data are mixed, classes tend to be involved in many relations.
 When objects are mutable, extra thinking is required in order to understand
how the code behaves.
 When objects are mutable, explicit synchronization mechanisms are required
on multi-threaded environments.
 When data is locked in objects, data serialization is not trivial.
 When code is locked in classes, class hierarchies tend to be complex.
 A system where every class is split into two independent parts, code and data, is
simpler than a system where code and data are mixed.
 A system made of multiple simple independent parts is less complex than a sys-
tem made of a single complex part.
 When data is mutable, code is unpredictable.
 A strategic use of design patterns can help mitigate complexity in traditional
OOP to some degree.
 Data immutability brings serenity to DOP developers’ minds.
 Most OOP programming languages alleviate slightly the difficulty involved the
conversion from and to JSON. It either involves reflection, which is definitely a
complex thing, or code verbosity.
 In traditional OOP, data serialization is difficult.
 In traditional OOP, data is locked in classes as members.
 In traditional OOP, code is locked into classes.
 DOP reduces complexity by rethinking data.
 DOP is compatible both with OOP and FP.

## 페이지 54

Separation between
code and data
A whole new world
This chapter covers
 The benefits of separating code from data
 Designing a system where code and data are
separate
 Implementing a system that respects the
separation between code and data
The first insight of DOP is that we can decrease the complexity of our systems by
separating code from data. Indeed, when code is separated from data, our systems
are made of two main pieces that can be thought about separately: data entities and
code modules. This chapter is a deep dive in the first principle of DOP (summa-
rized in figure 2.1).
PRINCIPLE #1 Separate code from data such that the code resides in functions,
whose behavior doesn’t depend on data that is somehow encapsulated in the func-
tion’s context.
26

## 페이지 55

2.1 The two parts of a DOP system 27
Stateless (static)
Functions
Data asfirst argument
Code modules
Usage
Relations
No inheritance
Separate code from data
Only members
Data entities No code
Association
Relations
Composition
Figure 2.1 DOP principle #1 summarized: Separate code from data.
In this chapter, we’ll illustrate the separation between code and data in the context of
Klafim’s Library Management System that we introduced in chapter 1. We’ll also unveil
the benefits that this separation brings to the system:
 The system is simple. It is easy to understand.
 The system is flexible and extensible. Quite often, it requires no design changes to
adapt to changing requirements.
This chapter focuses on the design of the code in a system where code and data are
separate. In the next chapter, we’ll focus on the design of the data. As we progress in
the book, we’ll discover other benefits of separating code from data.
2.1 The two parts of a DOP system
While Theo is driving home after delivering the prototype, he asks himself whether the
Klafim project was a success or not. Sure, he was able to satisfy the customer, but it was
more luck than brains. He wouldn’t have made it on time if Nancy had decided to keep
the Super members feature. Why was it so complicated to add tiny features to the system?
Why was the system he built so complex? He thought there should be a way to build more
flexible systems!
The next morning, Theo asks on Hacker News and on Reddit for ways to reduce system
complexity and build flexible systems. Some folks mention using different programming
languages, while others talk about advanced design patterns. Finally, Theo’s attention gets
captured by a comment from a user named Joe. He mentions data-oriented programming and
claims that its main goal is to reduce system complexity. Theo has never heard this term
before. Out of curiosity, he decides to contact Joe by email. What a coincidence! Joe lives
in San Francisco too. Theo invites him to a meeting in his office.
Joe is a 40-year-old developer. He was a Java developer for nearly a decade before adopt-
ing Clojure around 7 years ago. When Theo tells Joe about the Library Management System

## 페이지 56

