# 5 Introduction

**ID**: 44  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

92 CHAPTER 5 Basic concurrency control
In DOP, because only the code of the commit phase is stateful, that allows us to use
an optimistic concurrency control strategy that doesn’t involve any locking mechanism. As
a consequence, the throughput of reads and writes is high. The modifications to the
code are not trivial, as we have to implement an algorithm that reconciles concurrent
mutations. But the modifications impact only the commit phase. The code for the cal-
culation phase stays the same as in the previous chapter.
 NOTE This chapter requires more of an effort to grasp. The flow of the reconcilia-
tion algorithm is definitely not trivial, and the implementation involves a nontrivial
recursion.
