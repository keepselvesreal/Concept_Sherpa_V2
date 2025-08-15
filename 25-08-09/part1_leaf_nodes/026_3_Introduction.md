# 3 Introduction

**ID**: 26  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

44 CHAPTER 3 Basic data manipulation
We increase system flexibility when we represent records as string maps and not as
objects instantiated from classes. This liberates data from the rigidity of a class-based sys-
tem. Data becomes a first-class citizen powered by generic functions to add, remove, or
rename fields.
 NOTE We refer to maps that have strings as keys as string maps.
The dependency between the code that manipulates data and the data is a weak
dependency. The code only needs to know the keys of specific fields in the record it
wants to manipulate. The code doesn’t even need to know about all the keys in the
record, only the ones relevant to it. In this chapter, we’ll deal only with data query.
We’ll discuss managing changes in system state in the next chapter.
