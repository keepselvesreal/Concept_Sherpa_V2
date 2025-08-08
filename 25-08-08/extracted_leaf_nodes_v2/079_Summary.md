# Summary

**메타데이터:**
- ID: 79
- 레벨: 2
- 페이지: 202-202
- 페이지 수: 1
- 부모 ID: 73
- 텍스트 길이: 1098 문자

---

ng concurrency with atoms is much simpler than managing concur-
rency with locks because we don’t have to deal with the risk of deadlocks.
 Cloning data to avoid read locks doesn’t scale.
 When data is immutable, reads are always safe.
 Atoms provide a way to manage concurrency without locks.
 With atoms, deadlocks never happen.
 Using atoms for a thread-safe counter is trivial because the state of the counter
is represented with a primitive type (an integer).
 We can manage composite data in a thread-safe way with atoms.
 We make the highly scalable state management approach from part 1 thread-
safe by keeping the whole system state inside an atom.
 It’s quite common to represent an in-memory cache as a string map.
 When data is immutable, it is safe (and fast) to compare by reference.
 In theory, atoms could create starvation in a system with thousands of threads
that do nothing besides swapping an atom.
 In practice, once an atom is swapped, the threads do some real work (e.g.,
database access) to provide an opportunity for other threads to swap the atom
successfully.