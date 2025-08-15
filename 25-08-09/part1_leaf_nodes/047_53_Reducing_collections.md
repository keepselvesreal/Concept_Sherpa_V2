# 5.3 Reducing collections

**ID**: 47  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

5.3 Reducing collections 97
Theo Great! That helps, but in cases where two mutations update the same field of
the same entity, I think it’s fair enough to let the user know that the request
can’t be processed.
TIP In a user-facing system, conflicting concurrent mutations are fairly rare.
5.3 Reducing collections
Joe Are you ready to challenge your mind with the implementation of the diff
algorithm?
Theo Let’s take a short coffee break before, if you don’t mind. Then, I’ll be ready to
tackle anything.
After enjoying large mug of hot coffee and a few butter cookies, Theo and Joe are back to
work. Their discussion on the diff algorithm continues.
Joe In the implementation of the diff algorithm, we’re going to reduce collections.
Theo I heard about reducing collections in a talk about FP, but I don’t remember
the details. Could you remind me how this works?
Joe Imagine you want to calculate the sum of the elements in a collection of num-
bers. With Lodash’s _.reduce, it would look like this.
Listing5.1 Summing numbers with _.reduce
_.reduce([1, 2, 3], function(res, elem) {
return res + elem;
}, 0);
// → 6
Theo I don’t understand.
Joe goes to the whiteboard and writes the description of _.reduce. Theo waits patiently
until Joe puts the pen down before looking at the description.
Description of _.reduce
_.reduce receives three arguments:
 coll—A collection of elements
 f—A function that receives two arguments
 initVal—A value
Logic flow:
1 Initialize currentRes with initVal.
2 For each element x of coll, update currentRes with f(currentRes, x).
3 Return currentRes.

## 페이지 126

98 CHAPTER 5 Basic concurrency control
Theo Would you mind if I manually expand the logic flow of that code you just wrote
for _.reduce?
Joe I think it’s a great idea!
Theo In our case, initVal is 0. It means that the first call to f will be f(0, 1). Then,
we’ll have f(f(0, 1), 2) and, finally, f(f(f(0, 1), 2), 3).
Joe I like your manual expansion, Theo! Let’s make it visual.
Now Theo goes to the whiteboard and draws a diagram. Figure 5.5 shows what that looks like.
f
f a
2
f a
1
a 0 initVal Figure 5.5 Visualization
of _.reduce
Theo It’s much clearer now. I think that by implementing my custom version of
_.reduce, it will make things 100% clear.
It takes Theo much less time than he expected to implement reduce(). In no time at all,
he shows Joe the code.
Listing5.2 Custom implementation of _.reduce
function reduce(coll, f, initVal) {
var currentRes = initVal;
for (var i = 0; i < coll.length; i++) {
We could use
currentRes = f(currentRes, coll[i])
forEach instead
}
of a for loop.
return currentRes;
}
After checking that Theo’s code works as expected (see listing 5.3), Joe is proud of Theo.
He seems to be catching on better than he anticipated.
Listing5.3 Testing the custom implementation of reduce()
reduce([1, 2, 3], function(res, elem) {
return res + elem;
}, 0);
// → 6
Joe Well done!

## 페이지 127

