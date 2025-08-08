# Part3 Introduction content

**페이지**: 271-273
**계층**: Data-Oriented Programming (node0) > Part3—Maintainability (node1) > Part3 Introduction (사용자 추가) (node2)
**추출 시간**: 2025-08-06 19:47:16

---


--- 페이지 271 ---

11.6 Search result enrichment in action 243
if(!ajv.validate(searchBooksRequestSchema, request)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid request:" + errors;
}
var title = _.get(request, "title");
var fields = _.get(request, "fields");
var dbBookInfos = CatalogDataSource.matchingBooks(title);
var isbns = _.map(dbBookInfos, "isbn");
var openLibBookInfos =
OpenLibraryDataSource.multipleBookInfo(isbns, fields);
var response = joinArrays(dbBookInfos, openLibBookInfos);
if(!ajv.validate(searchBooksResponseSchema, request)) {
var errors = ajv.errorsText(ajv.errors);
throw "Invalid response:" + errors;
}
return response;
}
}
class Library {
static searchBooksByTitle(payloadBody) {
var payloadData = JSON.parse(payloadBody);
var results = Catalog.searchBooksByTitle(payloadData);
return JSON.stringify(results);
}
}
TIP Classes are much less complex when we use them as a means to aggregate state-
less functions that operate on similar domain entities.
Joe interrupts Theo’s meditation moment. After looking over the code in the previous list-
ings, he congratulates Theo.
Joe Excellent job, my friend! By the way, after reading The Power of Habit, I quit
chewing my nails.
Theo Wow! That’s terrific! Maybe I should read that book to overcome my habit of
drinking too much coffee.
Joe Thanks, and good luck with the coffee habit.
Theo I was supposed to call Nancy later today with an ETA for the Open Library
Book milestone. I wonder what her reaction will be when I tell her the feature
is ready.
Joe Maybe you should tell her it’ll be ready in a week, which would give you time to
begin work on the next milestone.

--- 페이지 271 끝 ---


--- 페이지 272 ---

244 CHAPTER 11 Web services
Delivering on time
Joe was right! Theo recalls Joe’s story about the young woodcutter and the old man. Theo
was able to learn DOP and deliver the project on time! He’s pleased that he took the time
“to sharpen his saw and commit to a deeper level of practice.”
 NOTE If you are unable to recall the story or if you missed it, check out the opener
to part 2.
The Klafim project is a success. Nancy is pleased. Theo’s boss is satisfied. Theo got pro-
moted. What more can a person ask for?
Theo remembers his deal with Joe. As he strolls through the stores of the Westfield San
Francisco Center to look for a gift for each of Joe’s children, Neriah and Aurelia, he is
filled with a sense of purpose and great pleasure. He buys a DJI Mavic Air 2 drone for Ner-
iah, and the latest Apple Airpod Pros for Aurelia. He also takes this opportunity to buy a
necklace and a pair of earrings for his wife, Jane. It’s a way for him to thank her for having
endured his long days at work since the beginning of the Klafim project.
 NOTE The story continues in the opener of part 3.
Summary
 We build the insides of our systems like we build the outsides.
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

--- 페이지 272 끝 ---


--- 페이지 273 ---

Part 3
Maintainability
A
fter a month, the Klafim project enters what Alabatross calls the mainte-
nance phase. Small new features need to be added on a weekly basis. Bugs need to be
fixed; nothing dramatic....
Monica, Theo’s boss, decides to allocate Dave to the maintenance of the Klafim
project. It makes sense. Over the last few months, Dave has demonstrated a great atti-
tude of curiosity and interest, and he has solid programming skills. Theo sets up a
meeting with Joe and Dave, hoping that Joe will be willing to teach DOP to Dave so
that he can continue to advance the good work he’s already done on Klafim. Theo
and Dave place a conference call to Joe.
Theo Hi, Joe. Will you have time over the next few weeks to teach Dave the
principles of DOP?
Joe Yes, but I prefer not to.
Dave Why? Is it because I don’t have enough experience in software develop-
ment? I can guarantee you that I’m a fast learner.
Joe It has nothing to do with your experience, Dave.
Theo Why not then?
Joe Theo, I think that you could be a great mentor for Dave.
Theo But, I don’t even know all the parts of DOP!
Dave Come on! No false modesty between us, my friend.
Joe Knowledge is never complete. As the great Socrates used to say, “The more
I know, the more I realize I know nothing.” I’m confident you will be able
to learn the missing parts by yourself and maybe even invent some.
Theo How will I be able to invent missing parts?

--- 페이지 273 끝 ---
