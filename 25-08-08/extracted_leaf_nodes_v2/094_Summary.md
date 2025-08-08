# Summary

**메타데이터:**
- ID: 94
- 레벨: 2
- 페이지: 223-224
- 페이지 수: 2
- 부모 ID: 80
- 텍스트 길이: 2789 문자

---

[
4
],
"y": {
"z": 2
}
}));
Joe What do you think of all this, my friend?
Theo I think that using persistent data collections with a library like Immutable.js is
much easier than understanding the internals of persistent data structures. But
I’m also glad that I know how it works under the hood.
After accompanying Joe to the office door, Theo meets Dave. Dave had been peering
through the window in Theo’s office, looking at the whiteboard, anxious to catch a glimpse
of today’s topic on DOP.
Dave What did Joe teach you today?
Theo He took me to the university and taught me the foundations of persistent data
structures for dealing with immutability at scale.
Dave What’s wrong with the structural sharing that I implemented a couple of
months ago?
Theo When the number of elements in the collection is big enough, naive structural
sharing has performance issues.
Dave I see. Could you tell me more about that?
Theo I’d love to, but my brain isn’t functioning properly after this interesting but
exhausting day. We’ll do it soon, promise.
Dave No worries. Have a nice evening, Theo.
Theo You too, Dave.
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

196 CHAPTER 9 Persistent data structures
 Persistent data structures represent data internally in such a way that structural
sharing scales well, both in terms of memory and computation.
 When data is immutable, it is safe to share it.
 Internally, persistence uses a branching factor of 32.
 In practice, manipulation of persistent data structures is efficient even for col-
lections with 10 billion entries!
 Due to modern architecture considerations, the performance of updating a
persistent list is dominated much more by the depth of the tree than by the
number of nodes at each level of the tree.
 Persistent lists can be manipulated in near constant time.
 In most languages, third-party libraries provide an implementation of persistent
data structures.
 Paguro collections implement the read-only parts of Java collection interfaces.
 Paguro collections can be passed to any methods that expect to receive a Java
collection without mutating them.