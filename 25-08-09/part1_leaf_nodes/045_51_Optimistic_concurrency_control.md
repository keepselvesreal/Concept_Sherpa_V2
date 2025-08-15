# 5.1 Optimistic concurrency control

**ID**: 45  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

5.1 Optimistic concurrency control
This morning, before getting to work, Theo takes Joe to the fitness room in the office and,
while running on the step machine, the two men talk about their personal lives again. Joe
talks about a fight he had last night with Kay, who thinks that he pays more attention to his
work than to his family. Theo recounts the painful conflict he had with Jane, his wife,
about house budget management. They went to see a therapist, an expert in Imago Rela-
tionship Therapy. Imago allowed them to transform their conflict into an opportunity to
grow and heal.
Joe’s ears perk up when he hears the word conflict because today’s lesson is going to be
about resolving conflicts and concurrent mutations. A different kind of conflict, though....
After a shower and a healthy breakfast, Theo and Joe get down to work.
Joe Yesterday, I showed you how to manage state with immutable data, assuming
that no mutations occur concurrently. Today, I am going to show you how to
deal with concurrency control in DOP.
Theo I’m curious to discover what kind of lock mechanisms you use in DOP to syn-
chronize concurrent mutations.
Joe In fact, we don’t use any lock mechanism!
Theo Why not?
Joe Locks hit performance, and if you’re not careful, your system could get into a
deadlock.
Theo So, how do you handle possible conflicts between concurrent mutations in
DOP?
Joe In DOP, we use a lock-free strategy called optimistic concurrency control. It’s a
strategy that allows databases like Elasticsearch to be highly scalable.
 NOTE See https://www.elastic.co/elasticsearch/ to find out more about Elastic-
search.
Theo You sound like my couples therapist and her anger-free, optimistic conflict
resolution strategy.
Joe Optimistic concurrency control and DOP fit together well. As you will see in a
moment, optimistic concurrency control is super efficient when the system
data is immutable.

## 페이지 121

5.1 Optimistic concurrency control 93
TIP Optimistic concurrency control with immutable data is super efficient.
Theo How does it work?
Joe Optimistic concurrency control occurs when we let mutations ask forgiveness
instead of permission.
TIP Optimistic concurrency control occurs when we let mutations ask forgiveness
instead of permission.
Theo What do you mean?
Joe The calculation phase does its calculation as if it were the only mutation run-
ning. The commit phase is responsible for reconciling concurrent mutations
when they don’t conflict or for aborting the mutation.
TIP The calculation phase does its calculation as if it were the only mutation running.
The commit phase is responsible for trying to reconcile concurrent mutations.
Theo That sounds quite challenging to implement.
Joe Dealing with state is never trivial. But the good news is that the code for the
reconciliation logic in the commit phase is universal.
Theo Does that mean that the same code for the commit phase can be used in any
DOP system?
Joe Definitely. The code that implements the commit phase assumes nothing
about the details of the system except that the system data is represented as an
immutable map.
TIP The implementation of the commit phase in optimistic concurrency control is
universal. It can be used in any system where the data is represented by an immutable
hash map.
Theo That’s awesome!
Joe Another cool thing is that handling concurrency doesn’t require any changes
to the code in the calculation phase. From the calculation phase perspective,
the next version of the system data is computed in isolation as if no other muta-
tions were running concurrently.
Joe stands up to illustrate what he means on the whiteboard. While Theo looks at the draw-
ing in figure 5.1, Joe summarizes the information in table 5.1.
Table 5.1 The two phases of a mutation with optimistic concurrency control
Phase Responsibility State Implementation
Calculation Compute next state in isolation Stateless Specific
Commit Reconcile and update system state Stateful Common

## 페이지 122

94 CHAPTER 5 Basic concurrency control
Calculation phase
Capturesystem state
Computenext version
Commit phase
Yes No
Concurrent mutations?
Yes No
Conflict?
Updatesystem state
Abortmutation Reconcilemutations
Updatesystem state
Figure 5.1 The logic flow
of optimistic concurrency
control
