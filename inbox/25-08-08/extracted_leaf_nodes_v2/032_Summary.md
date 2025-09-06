# Summary

**메타데이터:**
- ID: 32
- 레벨: 2
- 페이지: 97-98
- 페이지 수: 2
- 부모 ID: 25
- 텍스트 길이: 4358 문자

---

That’s the main goal of DOP.
Theo Also, I’m pleasantly surprised how easy it is to adapt to changing requirements,
both in terms of code and the data model.
Joe I suppose you’re also happy to get rid of complex class hierarchy diagrams.
Theo Absolutely! Also, I think I’ve found an interesting connection between DOP
and meditation.
Joe Really?
Theo When we were eating at Simple, you told me that meditation helped you expe-
rience reality as it is without the filter of your thoughts.
Joe Right.
Theo From what you taught me today, I understand that in DOP, we are encouraged
to treat data as data without the filter of our classes.
Joe Clever! I never noticed that connection between those two disciplines that are
so important for me. I guess you’d like to continue your journey in the realm
of DOP.
Theo Definitely. Let’s meet again tomorrow.
Joe Unfortunately, tomorrow I’m taking my family to the beach to celebrate the
twelfth birthday of my eldest daughter, Aurelia.
Theo Happy birthday, Aurelia!
Joe We could meet again next Monday, if that’s OK with you.
Theo With pleasure!
Summary
 DOP principle #2 is to represent data entities with generic data structures.
 We refer to maps that have strings as keys as string maps.
 Representing data as data means representing records with string maps.
 By positional collection, we mean a collection where the elements are in order
(like a list or an array).
 A positional collection of Strings is noted as [String].
 By index, we mean a collection where the elements are accessible via a key (like
a hash map or a dictionary).
 An index of Books is noted as {Book}.
 In the context of a data model, the index keys are always strings.
 A record is a data structure that groups together related data items. It’s a collec-
tion of fields, possibly of different data types.
 A homogeneous map is a map where all the values are of the same type.
 A heterogeneous map is a map where the values are of different types.
 In DOP, we represent a record as a heterogeneous string map.
 A data entity diagram consists of records whose values are either primitives, posi-
tional collections, or indexes.
 The relation between records in a data entity diagram is either composition or
association.

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