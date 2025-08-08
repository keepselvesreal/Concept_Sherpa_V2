# Part 3 Introduction

**메타데이터:**
- ID: 113
- 레벨: 1
- 페이지: 273-275
- 페이지 수: 3
- 부모 ID: 112
- 텍스트 길이: 7657 문자

---

=== Page 272 ===
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

=== Page 273 ===
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

=== Page 274 ===
246 PART 3 Maintainability
Joe You see, DOP is such a simple paradigm that it’s fertile material for innovation.
Part of the material I taught you I learned from others, and part of it was an
invention of mine. If you keep practicing DOP, I’m quite sure you, too, will
come up with some inventions of your own.
Theo What do you say Dave? Are you willing to learn DOP from me?
Dave Definitely!
Theo Joe, will you be continue to be available if we need your help from time to time?
Joe Of course!

=== Page 275 ===
Advanced data
validation
A self-made gift
This chapter covers
 Validating function arguments
 Validating function return values
 Data validation beyond static types
 Automatic generation of data model diagrams
 Automatic generation of schema-based unit tests
As the size of a code base grows in a project that follows DOP principles, it becomes
harder to manipulate functions that receive and return only generic data. It is hard
to figure out the expected shape of the function arguments, and when we pass
invalid data, we don’t get meaningful errors.
Until now, we have illustrated how to validate data at system boundaries. In this
chapter, we will illustrate how to validate data when it flows inside the system by
defining data schemas for function arguments and their return values. This allows
us to make explicit the expected shape of function arguments, and it eases develop-
ment. We gain some additional benefits from this endeavor, such as automatic gen-
eration of data model diagrams and schema-based unit tests.
247

=== Page 276 ===
248 CHAPTER 12 Advanced data validation
12.1 Function arguments validation
Dave’s first task is to implement a couple of new HTTP endpoints to download the catalog
as a CSV file, search books by author, and rate the books. Once he is done with the tasks,
Dave calls Theo for a code review.
 NOTE The involvement of Dave in the Klafim project is explained in the opener for
part 3. Please take a moment to read the opener if you missed it.
Theo Was it difficult to get your head around the DOP code?
Dave Not so much. I read your notes of the meetings with Joe, and I must admit, the
code is quite simple to grasp.
Theo Cool!
Dave But there is something that I can’t get used to.
Theo What’s that?
Dave I’m struggling with the fact that all the functions receive and return generic
data. In OOP, I know the expected shape of the arguments for each and every
function.
Theo Did you validate data at system boundaries, like I have done?
Dave Absolutely. I defined a data schema for every additional user request, database
query, and external service response.
Theo Nice!
Dave Indeed, when the system runs in production, it works well. When data is valid,
the data flows through the system, and when data is invalid, we are able to dis-
play a meaningful error message to the user.
Theo What’s the problem then?
Dave The problem is that during development, it’s hard to figure out the expected
shape of the function arguments. And when I pass invalid data by mistake, I
don’t get clear error messages.
Theo I see. I remember that when Joe showed me how to validate data at system
boundaries, I raised this concern about the development phase. Joe told me
then that we validate data as it flows inside the system exactly like we validate data
at system boundaries: we separate between data schema and data representation.
Dave Are we going to use JSON Schema also?
Theo Yes.
Dave Cool.... I like JSON Schema.
Theo The main purpose of data validation at system boundaries is to prevent invalid
data from getting into the system, whereas the main purpose of data validation
inside the system is to make it easier to develop the system. Here, let me draw a
table on the whiteboard for you to visualize this (table 12.1).
Table 12.1 Two kinds of data validation
Kind of data validation Purpose Environment
Boundaries Guardian Production
Inside Ease of development Dev