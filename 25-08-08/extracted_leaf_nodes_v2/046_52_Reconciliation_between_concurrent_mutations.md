# 5.2 Reconciliation between concurrent mutations

**메타데이터:**
- ID: 46
- 레벨: 2
- 페이지: 122-124
- 페이지 수: 3
- 부모 ID: 43
- 텍스트 길이: 4673 문자

---

on between concurrent mutations
Theo Could you give me some examples of conflicting concurrent mutations?
Joe Sure. One example would be two members trying to borrow the same book
copy. Another example might be when two librarians update the publication
year of the same book.
Theo You mentioned that the code for the reconciliation logic in the commit phase
is universal. What do you mean exactly by reconciliation logic?
Joe It’s quite similar to what could happen in Git when you merge a branch back
into the main branch.
Theo I love it when the main branch stays the same.
Joe Yes, it’s nice when the merge has no conflicts and can be done automatically.
Do you remember how Git handles the merge in that case?
Theo Git does a fast-forward; it updates the main branch to be the same as the merge
branch.
Joe Right! And what happens when you discover that, meanwhile, another devel-
oper has committed their code to the main branch?
Theo Then Git does a three-way merge, trying to combine all the changes from the
two merge branches with the main branch.
Joe Does it always go smoothly?
Theo Usually, yes, but it’s possible that two developers have modified the same line
in the same file. I then have to manually resolve the conflict. I hate when that
happens!
TIP In a production system, multiple mutations run concurrently. Before updating
the state, we need to reconcile the conflicts between possible concurrent mutations.

5.2 Reconciliation between concurrent mutations 95
Joe In DOP, the reconciliation algorithm in the commit phase is quite similar to a
merge in Git, except instead of a manual conflict resolution, we abort the
mutation. There are three possibilities to reconcile between possible concur-
rent mutations: fast-forward, three-way merge, or abort.
Joe goes to the whiteboard again. He draws the two diagrams shown in figures 5.2 and 5.3.
Yes No
State has stayed the same
Yes No
Concurrent mutations compatible?
Fast forward
3-way Merge Abort
Figure 5.2 The
reconciliation flow
The version during
the Commit phase
current
previous
next
The base version
for the Calculation
The version Figure 5.3 When the commit phase
phase
returned by the starts, there are three versions of the
Calculation phase system state.
Theo Could you explain in more detail?
Joe When the commit phase of a mutation starts, we have three versions of the sys-
tem state: previous, which is the version on which the calculation phase based
its computation; current, which is the current version during the commit
phase; and next, which is the version returned by the calculation phase.
Theo Why would current be different than previous?
Joe It happens when other mutations have run concurrently with our mutation.
Theo I see.
Joe If we are in a situation where the current state is the same as the previous state,
it means that no mutations run concurrently. Therefore, as in Git, we can
safely fast-forward and update the state of the system with the next version.
Theo What if the state has not stayed the same?
Joe Then it means that mutations have run concurrently. We have to check for
conflicts in a way similar to the three-way merge used by Git. The difference is
that instead of comparing lines, we compare fields of the system hash map.
Theo Could you explain that?

96 CHAPTER 5 Basic concurrency control
Joe We calculate the diff between previous and next and between previous and
current. If the two diffs have no fields in common, then there is no conflict
between the mutations that have run concurrently. We can safely apply the
changes from previous to next into current.
Joe makes his explanation visual with another diagram on the whiteboard. He then shows
figure 5.4 to Theo.
diffPreviousCurrent diffPreviousNext
current
previous merged
diffPreviousNext
next
Figure 5.4 In a three-way merge, we calculate the diff between previous and
next, and we apply it to current.
Theo What if there is a conflict?
Joe Then we abort the mutation.
Theo Aborting a user request seems unacceptable.
Joe In fact, in a user-facing system, conflicting concurrent mutations are fairly rare.
That’s why it’s OK to abort and let the user run the mutation again. Here, let
me draft a table to show you the differences between Git and DOP (table 5.2).
Table 5.2 The analogy between Git and data-oriented programming
Data-oriented programming Git
Concurrent mutations Different branches
A version of the system data A commit
State A reference
Calculation phase Branching
Validation Precommit hook
Reconciliation Merge
Fast-forward Fast-forward
Three-way merge Three-way merge
Abort Manual conflict resolution
Hash map Tree (folder)
Leaf node Blob (file)
Data field Line of code