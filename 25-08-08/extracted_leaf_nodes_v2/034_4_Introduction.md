# 4 Introduction

**메타데이터:**
- ID: 34
- 레벨: 2
- 페이지: 99-100
- 페이지 수: 2
- 부모 ID: 33
- 텍스트 길이: 7459 문자

---

=== Page 98 ===
70 CHAPTER 3 Basic data manipulation
 The data part of a DOP system is flexible, and each piece of information is
accessible via its information path.
 There is a tradeoff between flexibility and safety in a data model.
 DOP compromises on data safety to gain flexibility and genericity.
 In DOP, the data model is flexible. We’re free to add, remove, and rename
record fields dynamically at run time.
 We manipulate data with generic functions.
 Generic functions are provided either by the language itself or by third-party
libraries like Lodash.
 JSON serialization is implemented in terms of a generic function.
 On the one hand, we’ve lost the safety of accessing record fields via members
defined at compile time. On the other hand, we’ve liberated data from the lim-
itation of classes and objects. Data is represented as data!
 The weak dependency between code and data makes it is easier to adapt to
changing requirements.
 When data is represented as data, it is straightforward to visualize system data.
 Usually, we do not need to maintain type information about a record.
 We can visualize any part of the system data.
 In statically-typed languages, we sometimes need to statically cast the field values.
 Instead of maintaining type information about a record, we use a feature field.
 There is no significant performance hit for accessing a field in a map instead of
a class member.
 In DOP, you can retrieve every piece of information via an information path and
a generic function.
 In DOP, many parts of our code base tend to be just about data manipulation
with no abstractions.
Lodash functions introduced in this chapter
Function Description
get(map, path) Gets the value of map at path
has(map, path) Checks if map has a field at path
merge(mapA, mapB) Creates a map resulting from the recursive merges between mapA and mapB
values(map) Creates an array of values of map
filter(coll, pred) Iterates over elements of coll, returning an array of all elements for which
pred returns true
map(coll, f) Creates an array of values by running each element in coll through f

=== Page 99 ===
State management
Time travel
This chapter covers
 A multi-version approach to state management
 The calculation phase of a mutation
 The commit phase of a mutation
 Keeping a history of previous state versions
So far, we have seen how DOP handles queries via generic functions that access sys-
tem data, which is represented as a hash map. In this chapter, we illustrate how
DOP deals with mutations (requests that change the system state). Instead of updat-
ing the state in place, we maintain multiple versions of the system data. At a specific
point in time, the system state refers to a specific version of the system data. This
chapter is a deep dive in the third principle of DOP.
PRINCIPLE #3 Data is immutable.
The maintenance of multiple versions of the system data requires the data to be
immutable. This is made efficient both in terms of computation and memory via a
71

=== Page 100 ===
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
4.1 Multiple versions of the system data
When Joe comes in to the office on Monday, he tells Theo that he needs to exercise before
starting to work with his mind. Theo and Joe go for a walk around the block, and the dis-
cussion turns toward version control systems. They discuss how Git keeps track of the
whole commit history and how easy and fast it is to restore the code to a previous state.
When Theo tells Joe that Git’s ability to “time travel” reminds him one of his favorite mov-
ies, Back to the Future, Joe shares that a month ago he watched the Back to the Future trilogy
with Neriah, his 14-year-old son.
Their walk complete, they arrive back at Theo’s office. Theo and Joe partake of the
espresso machine in the kitchen before they begin today’s lesson.
Joe So far, we’ve seen how we manage queries that retrieve information from the
system in DOP. Now I’m going to show you how we manage mutations. By a
mutation, I mean an operation that changes the state of the system.
 NOTE A mutation is an operation that changes the state of the system.

=== Page 101 ===
4.1 Multiple versions of the system data 73
Theo Is there a fundamental difference between queries and mutations in DOP?
After all, the whole state of the system is represented as a hash map. I could
easily write code that modifies part of the hash map, and it would be similar to
the code that retrieves information from the hash map.
Joe You could mutate the data in place, but then it would be challenging to ensure
that the code of a mutation doesn’t put the system into an invalid date. You
would also lose the ability to track previous versions of the system state.
Theo I see. So, how do you handle mutations in DOP?
Joe We adopt a multi-version state approach, similar to what a version control sys-
tem like Git does; we manage different versions of the system data. At a specific
point in time, the state of the system refers to a version of the system data. After
a mutation is executed, we move the reference forward.
Theo I’m confused. Is the system state mutable or immutable?
Joe The data is immutable, but the state reference is mutable.
TIP The data is immutable, but the state reference is mutable.
Noticing the look of confusion on Theo’s face, Joe draws a quick diagram on the white-
board. He then shows Theo figure 4.1, hoping that it will clear up Theo’s perplexity.
After mutation B After mutation C
Data V10 Data V10
MutationA MutationA
Data V11 Data V11
Mutation B Mutation B
System State Data V12 Data V12
Mutation C
System State Data V13
Figure 4.1 After mutation B is executed, the system state refers to Data V12. After
mutation C is executed, the system state refers to Data V13.
Theo Does that mean that before the code of a mutation runs, we make a copy of the
system data?
Joe No, that would be inefficient, as we would have to do a deep copy of the data.