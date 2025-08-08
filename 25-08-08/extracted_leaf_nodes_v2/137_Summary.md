# Summary

**메타데이터:**
- ID: 137
- 레벨: 2
- 페이지: 338-338
- 페이지 수: 1
- 부모 ID: 131
- 텍스트 길이: 1622 문자

---

in a clear separation between the code that deals with business logic and
the implementation of the data manipulation.
 Separating business logic from data manipulation makes our code not only con-
cise, but also easy to read because it conveys the intent in a clear manner.
 We design and implement custom data manipulation functions in a four-step
process:
a Discover the function signature by using it before it is implemented.
b Write a unit test for the function.
c Formulate the behavior of the function in plain English.
d Implement the function.
 The best way to find the signature of a custom data manipulation function is to
think about the most convenient way to use it.
 Before implementing a custom data manipulation function, formulate in plain
English exactly what the function does.
 Pick the least generic utility function that solves your problem.
 Don’t use _.reduce or any other low-level data manipulation function inside
code that deals with business logic. Instead, write a utility function—with a proper
name—that hides _.reduce.
 Before implementing a complicated function, write a unit test for it.
Lodash functions introduced in this chapter
Function Description
flatten(arr) Flattens arr a single level deep
sum(arr) Computes the sum of the values in arr
uniq(arr) Creates an array of unique values from arr
every(coll, pred) Checks if pred returns true for all elements of coll
forEach(coll, f) Iterates over elements of coll and invokes f for each element
sortBy(coll, f) Creates an array of elements, sorted in ascending order, by the results of
running each element in coll through f