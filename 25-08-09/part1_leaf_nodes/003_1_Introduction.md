# 1 Introduction

**ID**: 3  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

Complexity of object-
oriented programming
A capricious entrepreneur
This chapter covers
 The tendency of OOP to increase system
complexity
 What makes OOP systems hard to understand
 The cost of mixing code and data together into
objects
In this chapter, we’ll explore why object-oriented programming (OOP) systems tend to
be complex. This complexity is not related to the syntax or the semantics of a specific
OOP language. It is something that is inherent to OOP’s fundamental insight—
programs should be composed from objects, which consist of some state, together
with methods for accessing and manipulating that state.
Over the years, OOP ecosystems have alleviated this complexity by adding new
features to the language (e.g., anonymous classes and anonymous functions) and
by developing frameworks that hide some of this complexity, providing a simpler
interface for developers (e.g., Spring and Jackson in Java). Internally, the frame-
works rely on the advanced features of the language such as reflection and custom
annotations.
3

## 페이지 32

4 CHAPTER 1 Complexity of object-orientedprogramming
This chapter is not meant to be read as a critical analysis of OOP. Its purpose is to
raise your awareness of the tendency towards OOP’s increased complexity as a pro-
gramming paradigm. Hopefully, it will motivate you to discover a different program-
ming paradigm, where system complexity tends to be reduced. This paradigm is
known as data-oriented programming (DOP).
