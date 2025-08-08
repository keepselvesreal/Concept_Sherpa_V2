# 4.1 Multiple versions of the system data

**메타데이터:**
- ID: 35
- 레벨: 2
- 페이지: 100-101
- 페이지 수: 2
- 부모 ID: 33
- 텍스트 길이: 4040 문자

---

rsions of the system data
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

74 CHAPTER 4 State management
Theo How does it work then?
Joe It works by using a technique called structural sharing, where most of the data
between subsequent versions of the state is shared instead of being copied.
This technique efficiently creates new versions of the system data, both in
terms of memory and computation.
Theo I’m intrigued.
TIP With structural sharing, it’s efficient (in terms of memory and computation) to
create new versions of data.
Joe I’ll explain in detail how structural sharing works in a moment.
Theo takes another look at the diagram in figure 4.1, which illustrates how the system state
refers to a version of the system data. Suddenly, a question emerges.
Theo Are the previous versions of the system data kept?
Joe In a simple application, previous versions are automatically removed by the
garbage collector. But, in some cases, we maintain historical references to pre-
vious versions of the data.
Theo What kind of cases?
Joe For example, if we want to support time travel in our system, as in Git, we can
move the system back to a previous version of the state easily.
Theo Now I understand what you mean by data is immutable, but the state reference
is mutable!