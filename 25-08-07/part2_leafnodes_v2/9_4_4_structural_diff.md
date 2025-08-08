# 9.4.4 Structural diff

9.4.4 Structural diff
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