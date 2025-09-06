# Delivering on time

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