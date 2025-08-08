# 9.4.4 Structural diff

Theo So far, we have ported pieces of code that dealt with simple data manipula-
tions. I’m curious to see how it goes with complex data manipulations such as
the code that computes the structural diff between two maps.
 NOTE Chapter 5 introduces structural diff.
Joe That also works smoothly, but we need to port another eight functions.
Listing9.19 Porting Lodash functions involved in structural diff computation
Immutable.reduce = function(coll, reducer, initialReduction) {
return coll.reduce(reducer, initialReduction);
};
Immutable.isEmpty = function(coll) {
return coll.isEmpty();
};
Immutable.keys = function(coll) {
return coll.keySeq();
};
Immutable.isObject = function(coll) {
return Immutable.Map.isMap(coll);
};
Immutable.isArray = Immutable.isIndexed;
Immutable.union = function() {
return Immutable.Set.union(arguments);
};
Theo Everything looks trivial with one exception: the use of arguments in Immutable
.union.
Joe In JavaScript, arguments is an implicit array-like object that contains the values
of the function arguments.
Theo I see. It’s one of those pieces of JavaScript magic!
Joe Yep. We need to use arguments because Lodash and Immutable.js differ slightly
in the signature of the union function. Immutable.Set.union receives an array
of lists, whereas a Lodash _.union receives several arrays.
Theo Makes sense. Let me give it a try.
Blowing on his fingers like a seasoned safecracker, first one hand and then the next, Theo
begins typing. Once again, Theo is surprised to discover that after replacing the _ with
Immutable in listing 9.20, the tests pass with the code in listing 9.21.
Listing9.20 Implementing structural diff with persistent data structures
function diffObjects(data1, data2) {
var emptyObject = Immutable.isArray(data1) ?
Immutable.fromJS([]) :

## 페이지 222

194 CHAPTER 9 Persistent data structures
Immutable.fromJS({});
if(data1 == data2) {
return emptyObject;
}
var keys = Immutable.union(Immutable.keys(data1), Immutable.keys(data2));
return Immutable.reduce(keys,
function (acc, k) {
var res = diff(Immutable.get(data1, k),
Immutable.get(data2, k));
if((Immutable.isObject(res) && Immutable.isEmpty(res)) ||
(res == "data-diff:no-diff")) {
return acc;
}
return Immutable.set(acc, k, res);
},
emptyObject);
}
function diff(data1, data2) {
if(Immutable.isObject(data1) && Immutable.isObject(data2)) {
return diffObjects(data1, data2);
}
if(data1 !== data2) {
return data2;
}
return "data-diff:no-diff";
}
Listing9.21 Testing structural diff with persistent data structures
var data1 = Immutable.fromJS({
g: {
c: 3
},
x: 2,
y: {
z: 1
},
w: [5]
});
var data2 = Immutable.fromJS({
g: {
c:3
},
x: 2,
y: {
z: 2
},
w: [4]
});
Immutable.isEqual(diff(data1, data2),
Immutable.fromJS({

## 페이지 223

Summary 195
"w": [
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

## 페이지 224

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

## 페이지 225

Database operations
A cloud is a cloud
This chapter covers
 Fetching data from the database
 Storing data in the database
 Manipulating data fetched from the database
Traditionally in OOP, we use design patterns and complex layers of objects to struc-
ture access to the database. In DOP, we prefer to represent data fetched from the
database with generic data collections, namely, lists of maps, where fields in the
maps correspond to database column values. As we’ll see throughout the chapter,
the fact that fields inside a map are accessible dynamically via their names allows us
to use the same generic code for different data entities.
TIP The best way to manipulate data is to represent data as data.
In this chapter, we’ll illustrate the application of data-oriented principles when
accessing data from a relational database. Basic knowledge of relational database
and SQL query syntax (like SELECT, AS, WHERE, and INNER JOIN) is assumed. This
approach can be easily adapted to NoSQL databases.
197

## 페이지 226

198 CHAPTER