# Chapter 10 Summary

Summary
 It’s possible to manually ensure that our data isn’t mutated, but it’s cumbersome.
 At scale, naive structural sharing causes a performance hit, both in terms of
memory and computation.
 Naive structural sharing doesn’t prevent data structures from being accidentally
mutated.
 Immutable collections are not the same as persistent data structures.
 Immutable collections don’t provide an efficient way to create new versions of
the collections.
 Persistent data structures protect data from mutation.
 Persistent data structures provide an efficient way to create new versions of the
collections.
 Persistent data structures always preserve the previous version of themselves when
they are modified.

## 페이지 224