--- 페이지 54 ---
26
Separation between
code and data
A whole new world
The first insight of DOP is that we can decrease the complexity of our systems by
separating code from data. Indeed, when code is separated from data, our systems
are made of two main pieces that can be thought about separately: data entities and
code modules. This chapter is a deep dive in the first principle of DOP (summa-
rized in figure 2.1).
This chapter covers
The benefits of separating code from data
Designing a system where code and data are 
separate
Implementing a system that respects the 
separation between code and data
PRINCIPLE #1
Separate code from data such that the code resides in functions,
whose behavior doesn’t depend on data that is somehow encapsulated in the func-
tion’s context.

--- 페이지 55 ---
27
