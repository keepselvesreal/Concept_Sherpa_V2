# Appendix D—Lodash reference

**메타데이터:**
- ID: 216
- 레벨: 0
- 페이지: 415-418
- 페이지 수: 4
- 부모 ID: None
- 텍스트 길이: 4592 문자

---

odash reference
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

index
A bookInfo schema 151, 155
BookInSearchResults class 52
AddBookItemController class 19 BookItem class 5, 11–12, 51
addMember mutation 84 BookItemQuery class 19
aggregateField function 216 BookItemResult class 19
allErrors options 159 bookItems member 52
association 7 BookLending class 5, 10, 12
Atom class 167 Book records 49–51, 60, 77
AtomicReference generic class 168 booksByIsbn index 46–47, 55, 77
atoms 163 boundaries of systems 143
state management with 172–174
thread-safe cache with 170–172 C
thread-safe counter with 165–170
Author class 5, 337–338 Catalog.authorNames function 115, 121
AuthorData class 347 Catalog.bookInfo function 114, 121
AuthorDataWithFullName class 347 Catalog class 5, 7, 10–11
Author entities 46–47 catalogData map 116–117
Author.myName(author, format) function Catalog entity 46–47
290 Catalog index 47
authorNameDispatch function 291 Catalog module 35, 39, 62–63
authorNames function 59, 63 Catalog record 54, 62
Author objects 7, 11 Catalog.searchBooksByTitle function 318
Author.prolificityLevel helper function 291 class inheritance 8
authorsById index 46–47, 55, 268 class members, generic access to 373–380
automatic generation of data model automatic JSON serialization of objects
diagrams 260–262 378–380
automatic generation of schema-based unit nested class members 376–378
tests 262–269 non-nested class members 373–376
code modules 31–36
B collections, reducing 97–98
CombinedBook class 231
BookAttributes class 377 commit function 88, 173
Book class 5, 7, 11, 51–52 commit phase 72, 93
Book entities 46–47 compareAndSet() method 168
bookInfo function 60, 63 complexity 13, 27, 164, 198, 341
BookInfo record 58, 60 composition 7
391