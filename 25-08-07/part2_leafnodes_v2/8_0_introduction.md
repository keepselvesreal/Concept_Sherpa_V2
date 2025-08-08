# 8.0 Introduction (사용자 추가)

Advanced
concurrency control
No more deadlocks!
This chapter covers
 Atoms as an alternative to locks
 Managing a thread-safe counter and a thread-safe
in-memory cache with atoms
 Managing the whole system state in a thread-safe
way with atoms
The traditional way to manage concurrency in a multi-threaded environment
involves lock mechanisms like mutexes. Lock mechanisms tend to increase the com-
plexity of the system because it’s not trivial to make sure the system is free of dead-
locks. In DOP, we leverage the fact that data is immutable, and we use a lock-free
mechanism, called an atom, to manage concurrency. Atoms are simpler to manage
than locks because they are lock-free. As a consequence, the usual complexity of
locks that are required to avoid deadlocks don’t apply to atoms.
 NOTE This chapter is mostly relevant to multi-threaded environments like Java,
C#, Python, and Ruby. It is less relevant to single-threaded environments like Java-
Script. The JavaScript code snippets in this chapter are written as though JavaScript
were multi-threaded.
163