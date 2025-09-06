# Summary

**메타데이터:**
- ID: 101
- 레벨: 2
- 페이지: 246-247
- 페이지 수: 2
- 부모 ID: 95
- 텍스트 길이: 2543 문자

---

our applications, we represent data fetched from the database, no matter
if it is relational or nonrelational, as a generic data structure.
 In the case of a relational database, data is represented as a list of maps.
 Representing data from the database as data reduces system complexity because
we don’t need design patterns or complex class hierarchies to do it.
 We are free to manipulate data from the database with generic functions, such as
returning a list made of the values of some data fields, creating a version of a
map omitting a data field, or grouping maps in a list according to the value of a
data field.
 We use generic functions for data manipulation with great flexibility, using the
fact that inside a hash map, we access the value of a field via its name, repre-
sented as a string.
 When we package our data manipulation logic into custom functions that receive
field names as arguments, we are able to use those functions on different data
entities.
 The best way to manipulate data is to represent data as data.
 We represent data from the database with generic data collections, and we
manipulate it with generic functions.
 Accessing data from a NoSQL database is done in a similar way to the approach
presented in this chapter for accessing data from a relational database.
 With late binding, we care about data types as late as possible.
 Flexibility is increased as many parts of the system are free to manipulate data
without dealing with concrete types.
 Accessing a field in a hash map is more flexible than accessing a member in an
object instantiated from a class.

Summary 219
 In DOP, field names are just strings. It allows us to write generic functions to
manipulate list of maps representing data fetched from the database.
 In DOP, fields are first-class citizens.
 We can implement renaming keys in a list of maps or aggregating rows returned
by a database query via generic functions.
 JDBC stands for Java database connectivity.
 Converting a JDBC result set into a list of maps is quite straightforward.
Lodash functions introduced in this chapter
Function Description
at(map, [paths]) Creates an array of values corresponding to paths of map
omit(map, [paths]) Creates a map composed of the fields of map not in paths
nth(arr, n) Gets the element at index n in arr
groupBy(coll, f) Creates a map composed of keys generated from the results of running
each element of coll through f. The corresponding value for each key
is an array of elements responsible for generating the key.