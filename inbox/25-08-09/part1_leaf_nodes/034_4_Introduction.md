# 4 Introduction

**ID**: 34  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

72 CHAPTER 4 State management
technique called structural sharing, where parts of the data that are common between
two versions are shared instead of being copied. In DOP, a mutation is split into two
distinct phases:
 In the calculation phase, we compute the next version of the system data.
 In the commit phase, we move the system state forward so that it refers to the
version of the system data computed by the calculation phase.
This distinction between calculation and commit phases allows us to reduce the part
of our system that is stateful to its bare minimum. Only the code of the commit phase
is stateful, while the code in the calculation phase of a mutation is stateless and is
made of generic functions similar to the code of a query. The implementation of the
commit phase is common to all mutations. As a consequence, inside the commit
phase, we have the ability to ensure that the state always refers to a valid version of the
system data.
Another benefit of this state management approach is that we can keep track of
the history of previous versions of the system data. Restoring the system to a previous
state (if needed) becomes straightforward. Table 4.1 shows the two phases.
Table 4.1 The two phases of a mutation
Phase Responsibility State Implementation
Calculation Computes the next version of system data Stateless Specific
Commit Moves the system state forward Stateful Common
In this chapter, we assume that no mutations occur concurrently in our system. In the
next chapter, we will deal with concurrency control.
