# Appendix D—Lodash reference

**Level:** 0
**페이지 범위:** 415 - 418
**총 페이지 수:** 4
**ID:** 216

---

=== 페이지 415 ===
appendix D
Lodash reference
Throughout the book, we have used Lodash (https://lodash.com/) to illustrate
how to manipulate data with generic functions. But there is nothing unique about
Lodash. The exact same approach could be implemented via other data manipula-
tion libraries or custom code.
Moreover, we used Lodash FP (https://github.com/lodash/lodash/wiki/FP-
Guide) to manipulate data without mutating it. By default, the order of the argu-
ments in immutable functions is shuffled. The code in listing D.1 is needed when
configuring Lodash in order to ensure the signature of the immutable functions is
exactly the same as the mutable functions.
ListingD.1 Configuring immutable functions
_ = fp.convert({
"cap": false,
"curry": false,
"fixed": false,
"immutable": true,
"rearg": false
});
This short appendix lists the 28 Lodash functions used in the book to help you, in
case you are looking at a code snippet in the book that uses a Lodash function that
you want to understand. The functions are split in to three categories:
 Functions on maps in table D.1
 Functions on arrays in table D.2
 Function on collections (both arrays and maps) in table D.3
387

=== 페이지 416 ===
388 APPENDIX D Lodash reference
Each table has three columns:
 Function shows the function with its signature.
 Description provides a brief description of the function.
 Chapter is the chapter number where the function appears for the first time.
Table D.1 Lodash functions on maps
Function Description Chapter
at(map, [paths]) Creates an array of values corresponding to paths 10
of map
get(map, path) Gets the value at path of map 3
has(map, path) Checks if map has a field at path 3
merge(mapA, mapB) Creates a map resulting from the recursive merges 3
between mapA and mapB
omit(map, [paths]) Creates a map composed of the fields of map not in 10
paths
set(map, path, value) Creates a map with the same fields as map with the 4
addition of a field <path, value>
values(map) Creates an array of values of map 3
Table D.2 Lodash functions on arrays
Function Description Chapter
concat(arrA, arrB) Creates an new array that concatenates arrA and 5
arrB
flatten(arr) Flattens arr a single level deep 14
intersection(arrA, Creates an array of unique values both in arrA and 5
arrB) arrB
nth(arr, n) Gets the element at index n in arr 10
sum(arr) Computes the sum of the values in arr 14
union(arrA, arrB) Creates an array of unique values from arrA and 5
arrB
uniq(arr) Creates an array of unique values from arr 14

=== 페이지 417 ===
APPENDIX D Lodash reference 389
Table D.3 Lodash functions on collections (both arrays and maps)
Function Description Chapter
every(coll, pred) Checks if pred returns true for all elements of coll 14
filter(coll, pred) Iterates over elements of coll, returning an array of all 3
elements for which pred returns true
find(coll, pred) Iterates over elements of coll, returning the first ele- 15
ment for which pred returns true
forEach(coll, f) Iterates over elements of coll and invokes f for each 14
element
groupBy(coll, f) Creates a map composed of keys generated from the 10
results of running each element of coll through f. The
corresponding value for each key is an array of elements
responsible for generating the key.
isEmpty(coll) Checks if coll is empty 5
keyBy(coll, f) Creates a map composed of keys generated from the 11
results of running each element of coll through f. The
corresponding value for each key is the last element
responsible for generating the key.
map(coll, f) Creates an array of values by running each element in 3
coll through f
reduce(coll, f, Reduces coll to a value which is the accumulated result 5
initVal) of running each element in coll through f, where each
successive invocation is supplied the return value of the
previous
size(coll) Gets the size of coll 13
sortBy(coll, f) Creates an array of elements, sorted in ascending order by 14
the results of running each element in coll through f
isEqual(collA, collB) Performs a deep comparison between collA and 6
collB
isArray(coll) Checks if coll is an array 5
isObject(coll) Checks if coll is a collection 5
