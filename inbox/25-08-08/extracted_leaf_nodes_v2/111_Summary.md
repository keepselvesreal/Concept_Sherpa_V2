# Summary

**메타데이터:**
- ID: 111
- 레벨: 2
- 페이지: 272-272
- 페이지 수: 1
- 부모 ID: 102
- 텍스트 길이: 1149 문자

---

ld the insides of our systems like we build the outsides.
 Components inside a program communicate via data that is represented as
immutable data collections in the same way as components communicate via
data over the wire.
 In DOP, the inner components of a program are loosely coupled.
 Many parts of business logic can be implemented through generic data manipu-
lation functions. We use generic functions to
– Implement each step of the data flow inside a web service.
– Parse a request from a client.
– Apply business logic to the request.
– Fetch data from external sources (e.g., database and other web services).
– Apply business logic to the responses from external sources.
– Serialize response to the client.
 Classes are much less complex when we use them as a means to aggregate
together stateless functions that operate on similar domain entities.
Lodash functions introduced in this chapter
Function Description
keyBy(coll, f) Creates a map composed of keys generated from the results of running each ele-
ment of coll through f; the corresponding value for each key is the last element
responsible for generating the key.

Part 3