# Summary

**메타데이터:**
- ID: 50
- 레벨: 2
- 페이지: 136-137
- 페이지 수: 2
- 부모 ID: 43
- 텍스트 길이: 2683 문자

---

stic concurrency control allows mutations to ask forgiveness instead of
permission.
 Optimistic concurrency control is lock-free.
 Managing concurrent mutations of our system state with optimistic concurrency
control allows our system to support a high throughput of reads and writes.
 Optimistic concurrency control with immutable data is super efficient.
 Before updating the state, we need to reconcile the conflicts between possible con-
current mutations.
 We reconcile between concurrent mutations in a way that is similar to how Git han-
dles a merge between two branches: either a fast-forward or a three-way merge.
 The changes required to let our system manage concurrency are only in the
commit phase.
 The calculation phase does its calculation as if it were the only mutation running.
 The commit phase is responsible for trying to reconcile concurrent mutations.
 The reconciliation algorithm is universal in the sense that it can be used in any sys-
tem where the system data is represented as an immutable hash map.
 The implementation of the reconciliation algorithm is efficient, as it leverages
the fact that subsequent versions of the system state are created via structural
sharing.
 In a user-facing system, conflicting concurrent mutations are fairly rare.
 When we cannot safely reconcile between concurrent mutations, we abort the
mutation and ask the user to try again.

Summary 109
 Calculating the structural diff between two versions of the state is efficient because
two hash maps created via structural sharing from the same hash map have most
of their nodes in common.
 When data is immutable, it is safe to compare by reference, which is fast. When
the references are the same, it means that the data is the same.
 There are three kinds of structural differences between two nested hash maps:
replacement, addition, and deletion.
 Our structural diff algorithm supports replacements and additions but not
deletions.
Lodash functions introduced in this chapter
Function Description
concat(arrA, arrB) Creates an new array, concatenating arrA and arrB
intersection(arrA, arrB) Creates an array of unique values both in arrA and arrB
union(arrA, arrB) Creates an array of unique values from arrA and arrB
find(coll, pred) Iterates over elements of coll, returning the first element for
which pred returns true
isEmpty(coll) Checks if coll is empty
reduce(coll, f, initVal) Reduces coll to a value that is the accumulated result of running
each element in coll through f, where each successive invoca-
tion is supplied the return value of the previous
isArray(coll) Checks if coll is an array
isObject(coll) Checks if coll is a collection