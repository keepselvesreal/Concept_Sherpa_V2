# 2.1 The two parts of a DOP system

**ID**: 19  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

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

28 CHAPTER 2 Separation between code and data
he designed and built, and about his struggles to adapt to changing requirements, Joe is
not surprised.
Joe tells Theo that the systems that he and his team have built in Clojure over the last 7
years are less complex and more flexible than the systems he used to build in Java. Accord-
ing to Joe, the systems they build now tend to be much simpler because they follow the
principles of DOP.
Theo I’ve never heard of data-oriented programming. Is it a new concept?
Joe Yes and no. Most of the foundational ideas of data-oriented programming, or
DOP as we like to call it, are well known to programmers as best practices. The
novelty of DOP, however, is that it combines best practices into a cohesive
whole.
Theo That’s a bit abstract for me. Can you give me an example?
Joe Sure! Take, for instance, the first insight of DOP. It’s about the relations between
code and data.
Theo You mean the encapsulation of data in objects?
Joe Actually, DOP is against data encapsulation.
Theo Why is that? I thought data encapsulation was a positive programming paradigm.
Joe Data encapsulation has both merits and drawbacks. Think about the way you
designed the Library Management System. According to DOP, the main cause
of complexity and inflexibility in systems is that code and data are mixed
together in objects.
TIP DOP is against data encapsulation.
Theo It sounds similar to what I’ve heard about functional programming. So, if I
want to adopt DOP, do I need to get rid of object-oriented programming and
learn functional programming?
Joe No, DOP principles are language-agnostic. They can be applied in both object-
oriented and functional programming languages.
Theo That’s a relief! I was afraid that you were going to teach me about monads,
algebraic data types, and higher order functions.
Joe No, none of that is required in DOP.
TIP DOP principles are language-agnostic.
Theo What does the separation between code and data look like in DOP then?
Joe Data is represented by data entities that only hold members. Code is aggre-
gated into modules where all functions are stateless.
Theo What do you mean by stateless functions?
Joe Instead of having the state encapsulated in the object, the data entity is passed
as an argument.
Theo I don’t get that.
Joe Here, let’s make it visual.

## 페이지 57

