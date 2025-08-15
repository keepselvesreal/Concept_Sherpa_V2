# 14 Advanced data manipulation

**Level:** 1
**페이지 범위:** 323 - 338
**총 페이지 수:** 16
**ID:** 131

---

=== 페이지 323 ===
Advanced data
manipulation
Whatever is well-conceived
is clearly said
This chapter covers
 Manipulating nested data
 Writing clear and concise code for business
logic
 Separating business logic and generic data
manipulation
 Building custom data manipulation tools
 Using the best tool for the job
When our business logic involves advanced data processing, the generic data manip-
ulation functions provided by the language run time and by third-party libraries
might not be sufficient. Instead of mixing the details of data manipulation with
business logic, we can write our own generic data manipulation functions and imple-
ment our custom business logic using them. Separating business logic from the inter-
nal details of data manipulation makes the business logic code concise and easy to
read for other developers.
295

=== 페이지 324 ===
296 CHAPTER 14 Advanced data manipulation
14.1 Updating a value in a map with eloquence
Dave is more and more autonomous on the Klafim project. He can implement most fea-
tures on his own, typically turning to Theo only for code reviews. Dave’s code quality stan-
dards are quite high. Even when his code is functionally solid, he tends to be unsatisfied
with its readability. Today, he asks for Theo’s help in improving the readability of the code
that fixes a bug Theo introduced a long time ago.
Dave I think I have a found a bug in the code that returns book information from
the Open Library API.
Theo What bug?
Dave Sometimes, the API returns duplicate author names, and we pass the dupli-
cates through to the client.
Theo It doesn’t sound like a complicated bug to fix.
Dave Right, I fixed it, but I’m not satisfied with the readability of the code I wrote.
Theo Being critical of our own code is an important quality for a developer to prog-
ress. What is it exactly that you don’t like?
Dave Take a look at this code.
Listing14.1 Removing duplicates in a straightforward but tedious way
function removeAuthorDuplicates(book) {
var authors = _.get(book, "authors");
var uniqAuthors = _.uniq(authors);
return _.set(book,"authors", uniqAuthors);
}
Dave I’m using _.get to retrieve the array with the author names, then _.uniq to
create a duplicate-free version of the array, and finally, _.set to create a new
version of the book with no duplicate author names.
Theo The code is tedious because the next value of authorNames needs to be based
on its current value.
Dave But it’s a common use case! Isn’t there a simpler way to write this kind of code?
Theo Your astonishment definitely honors you as a developer, Dave. I agree with you
that there must be a simpler way. Let me phone Joe and see if he’s available for
a conference call.
Joe How’s it going, Theo?
Theo Great! Are you back from your tech conference?
Joe I just landed. I’m on my way home now in a taxi.
Theo How was your talk about DOP?
Joe Pretty good. At the beginning people were a bit suspicious, but when I told
them the story of Albatross and Klafim, it was quite convincing.
Theo Yeah, adults are like children in that way; they love stories.
Joe What about you? Did you manage to achieve polymorphism with multimethods?
Theo Yes! Dave even managed to implement a feature in Klafim with multimethods.
Joe Cool!

=== 페이지 325 ===
14.1 Updating a value in a map with eloquence 297
Theo Do you have time to help Dave with a question about programming?
Joe Sure.
Dave Hi Joe. How are you doing?
Joe Hello Dave. Not bad. What kind of help do you need?
Dave I’m wondering if there’s a simpler way to remove duplicates inside an array
value in a map. Using _.get, _.uniq, and _.set looks quite tedious.
Joe You should build your own data manipulation tools.
Dave What do you mean?
Joe You should write a generic update function that updates a value in a map,
applying a calculation based on its current value.1
Dave What would the arguments of update be in your opinion?
Joe Put the cart before the horse.
Dave What?!
Joe Rewrite your business logic as if update were already implemented, and you’ll
discover what the arguments of update should be.
Dave I see what you mean: the horse is the implementation of update, and the cart is
the usage of update.
Joe Exactly. But remember, it’s better if you keep your update function generic.
Dave How?
Joe By not limiting it to your specific use case.
Dave I see. The implementation of update should not deal with removing duplicate
elements. Instead, it should receive the updating function—in my case,
_.uniq—as an argument.
Joe Exactly! Uh, sorry Dave, I gotta go, I just got home. Good luck!
Dave Take care, Joe, and thanks!
Dave ends the conference call. Looking at Theo, he reiterates the conversation with Joe.
Dave Joe advised me to write my own update function. For that purpose, he told me
to start by rewriting removeAuthorDuplicates as if update were already
implemented. That will allow us to make sure we get the signature of update
right.
Theo Sounds like a plan.
Dave Joe called it “putting the cart before the horse.”
Theo Joe and his funny analogies...
TIP The best way to find the signature of a custom data manipulation function is to
think about the most convenient way to use it.
Dave Anyway, the way I’d like to use update inside removeAuthorDuplicates is
like this.
1 Lodash provides an implementation of update, but for the sake of teaching, we are writing our own imple-
mentation.

=== 페이지 326 ===
298 CHAPTER 14 Advanced data manipulation
Listing14.2 The code that removes duplicates in an elegant way
function removeAuthorDuplicates(book) {
return update(book, "authors", _.uniq);
}
Theo Looks good to me!
Dave Wow! Now the code with update is much more elegant than the code with
_.get and _.set!
Theo Before you implement update, I suggest that you write down in plain English
exactly what the function does.
Dave It’s quite easy: update receives a map called map, a path called path, and a
function called fun. It returns a new version of map, where path is associated
with fun(currentValue), and currentValue is the value associated with
path in map.
Thinking out loud, Dave simultaneously draws a diagram like that in figure 14.1. Theo is
becoming more and more impressed with his young protegé as he studies the figure.
{
"position" : "manager", "income"
"income" : 100000
} map fun path
update
{
"position" : "manager",
"income" : fun(100000)
res Figure 14.1 The
}
behavior of update
TIP Before implementing a custom data manipulation function, formulate in plain
English exactly what the function does.
Theo With such a clear definition, it’s going to be a piece of cake to implement
update!
After a few minutes, Dave comes up with the code. It doesn’t take long because the plain-
English diagram helps him to organize the code.
Listing14.3 A generic update function
function update(map, path, fun) {
var currentValue = _.get(map, path);
var nextValue = fun(currentValue);
return _.set(map, path, nextValue);
}

=== 페이지 327 ===
14.2 Manipulating nested data 299
Theo Why don’t you see if it works with a simple case such as incrementing a number
in a map?
Dave Good idea! I’ll try multiplying a value in a map by 2 with update. How’s this
look?
Listing14.4 Multiplying a value in a map by 2
var m = {
"position": "manager",
"income": 100000
};
update(m, "income", function(x) {
return x * 2;
});
// → {"position": "manager", "income": 200000}
Theo Great! It seems to work.
14.2 Manipulating nested data
The next Monday, during Theo and Dave’s weekly sync meeting, they discuss the upcom-
ing features for Klafim. Theo fondly remembers another Monday where they met at Dave’s
family home in the country. Coming back to the present moment, Theo begins.
Theo Recently, Nancy has been asking for more and more administrative features.
Dave Like what?
Theo I’ll give you a few examples.... Let me find the email I got from Nancy yesterday.
Dave OK.
Theo Here it is. There are three feature requests for now: listing all the book author
IDs, calculating the book lending ratio, and grouping books by a physical library.
Dave What feature should I tackle first?
Theo It doesn’t matter, but you should deliver the three of these before the end of
the week. Good luck, and don’t hesitate to call me if you need help.
On Tuesday, Dave asks for Theo’s help. Dave is not pleased with how his code looks.
Dave I started to work on the three admin features, but I don’t like the code I wrote.
Let me show you the code for retrieving the list of author IDs from the list of
books returned from the database.
Theo Can you remind me what an element in a book list returned from the database
looks like?
Dave Each book is a map with an authorIds array field.
Theo OK, so it sounds like a map over the books should do it.
Dave This is what I did, but it doesn’t work as expected. Here’s my code for listing
the book author IDs.

=== 페이지 328 ===
300 CHAPTER 14 Advanced data manipulation
Listing14.5 Retrieving the author IDs in books as an array of arrays
function authorIdsInBooks(books) {
return _.map(books, "authorIds");
}
Theo What’s the problem?
Dave The problem is that it returns an array of arrays of author IDs instead of an
array of author IDs. For instance, when I run authorIdsInBooks on a catalog
with two books, I get this result.
Listing14.6 The author IDs in an array of arrays
[
["sean-covey", "stephen-covey"],
["alan-moore", "dave-gibbons"]
]
Theo That’s not a big problem. You can flatten an array of arrays with _.flatten,
and you should get the result you expect.
Dave Nice! This is exactly what I need! Give me a moment to fix the code of
authorIdsInBooks. . . here you go.
Listing14.7 Retrieving the author IDs in books as an array of strings
function authorIdsInBooks(books) {
return _.flatten(_.map(books, "authorIds"));
}
Theo Don’t you think that mapping and then flattening deserves a function of its own?
Dave Maybe. It’s quite easy to implement a flatMap function.2 How about this?
Listing14.8 The implementation of flatMap
function flatMap(coll, f) {
return _.flatten(_.map(coll,f));
}
Theo Nice!
Dave I don’t know.... It’s kind of weird to have such a small function.
Theo I don’t think that code size is what matters here.
Dave What do you mean?
Theo See what happens when you rewrite authorIdsInBooks using flatMap.
Dave OK, here’s how I’d use flatMap to list the author IDs.
2 Lodash provides an implementation of flatMap, but for the sake of teaching, we are writing our own
implementation.

=== 페이지 329 ===
14.3 Using the best tool for the job 301
Listing14.9 Retrieving the author IDs as an array of strings using flatMap
function authorIdsInBooks(books) {
return flatMap(books, "authorIds");
}
Theo What implementation do you prefer, the one with flatten and map (in listing
14.7) or the one with flatMap (in listing 14.9)?
Dave I don’t know. To me, they look quite similar.
Theo Right, but which implementation is more readable?
Dave Well, assuming I know what flatMap does, I would say the implementation
with flatMap. Because it’s more concise, it is a bit more readable.
Theo Again, it’s not about the size of the code. It’s about the clarity of intent and the
power of naming things.
Dave I don’t get that.
Theo Let me give you an example from our day-to-day language.
Dave OK.
Theo Could you pass me that thing on your desk that’s used for writing?
It takes Dave a few seconds to get that Theo has asked him to pass the pen on the desk.
After he passes Theo the pen, he asks:
Dave Why didn’t you simply ask for the pen?
Theo I wanted you to experience how it feels when we use descriptions instead of
names to convey our intent.
Dave Oh, I see. You mean that once we use a name for the operation that maps and
flattens, the code becomes clearer.
Theo Exactly.
Dave Let’s move on to the second admin feature: calculating the book lending ratio.
Theo Before that, I think we deserve a short period for rest and refreshments, where
we drink a beverage made by percolation from roasted and ground seeds.
Dave A coffee break!
14.3 Using the best tool for the job
After the coffee break, Dave shows Theo his implementation of the book lending ratio cal-
culation. This time, he seems to like the code he wrote.
Dave I’m quite proud of the code I wrote to calculate the book lending ratio.
Theo Show me the money!
Dave My function receives a list of books from the database like this.
Listing14.10 A list of two books with bookItems
[
{
"isbn": "978-1779501127",

=== 페이지 330 ===
302 CHAPTER 14 Advanced data manipulation
"title": "Watchmen",
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
}
]
},
{
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"bookItems": [
{
"id": "book-item-123",
"libId": "hudson-park-lib",
"isLent": true
},
{
"id": "book-item-17",
"libId": "nyc-central-lib",
"isLent": false
}
]
}
]
Theo Quite a nested piece of data!
Dave Yeah, but now that I’m using flatMap, calculating the lending ratio is quite
easy. I’m going over all the book items with forEach and incrementing either
the lent or the notLent counter. At the end, I return the ratio between lent
and (lent + notLent). Here’s how I do that.
Listing14.11 Calculating the book lending ratio using forEach
function lendingRatio(books) {
var bookItems = flatMap(books, "bookItems");
var lent = 0;
var notLent = 0;
_.forEach(bookItems, function(item) {
if(_.get(item, "isLent")) {
lent = lent + 1;
} else {
notLent = notLent + 1;
}
});
return lent/(lent + notLent);
}
Theo Would you allow me to tell you frankly what I think of your code?
Dave If you are asking this question, it means that you don’t like it. Right?
Theo It’s nothing against you; I don’t like any piece of code with forEach.

=== 페이지 331 ===
14.3 Using the best tool for the job 303
Dave What’s wrong with forEach?
Theo It’s too generic!
Dave I thought that genericity was a positive thing in programming.
Theo It is when we build a utility function, but when we use a utility function, we
should use the least generic function that solves our problem.
Dave Why?
Theo Because we ought to choose the right tool for the job, like in the real life.
Dave What do you mean?
Theo Let me give you an example. Yesterday, I had to clean my drone from the
inside. Do you think that I used a screwdriver or a Swiss army knife to unscrew
the drone cover?
Dave A screwdriver, of course! It’s much more convenient to manipulate.
Theo Right. Also, imagine that someone looks at me using a screwdriver. It’s quite
clear to them that I am turning a screw. It conveys my intent clearly.
Dave Are you saying that forEach is like the Swiss army knife of data manipulation?
Theo That’s a good way to put it.
TIP Pick the least generic utility function that solves your problem.
Dave What function should I use then, to iterate over the book item collection?
Theo You could use _.reduce.
Dave I thought reduce was about returning data from a collection. Here, I don’t
need to return data; I need to update two variables, lent and notLent.
Theo You could represent those two values in a map with two keys.
Dave Can you show me how to rewrite my lendingRatio function using reduce?
Theo Sure. The initial value passed to reduce is the map, {"lent": 0, "notLent": 0},
and inside each iteration, we update one of the two keys, like this.
Listing14.12 Calculating the book lending ratio using reduce
function lendingRatio(books) {
var bookItems = flatMap(books, "bookItems");
var stats = _.reduce(bookItems, function(res, item) {
if(_.get(item, "isLent")) {
res.lent = res.lent + 1;
} else {
res.notLent = res.notLent + 1;
}
return res;
}, {notLent: 0, lent:0});
return stats.lent/(stats.lent + stats.notLent);
}
Dave Instead of updating the variables lent and notLent, now we are updating lent
and notLent map fields. What’s the difference?

=== 페이지 332 ===
304 CHAPTER 14 Advanced data manipulation
Theo Dealing with map fields instead of variables allows us to get rid of reduce in
our business logic code.
Dave How could you iterate over a collection without forEach and without reduce?
Theo I can’t avoid the iteration over a collection, but I can hide reduce behind a
utility function. Take a look at the way reduce is used inside the code of
lendingRatio. What is the meaning of the reduce call?
Dave looks at the code in listing 14.12. He thinks for a long moment before he answers.
Dave I think it’s counting the number of times isLent is true and false.
Theo Right. Now, let’s use Joe’s advice about building our own data manipulation
tool.
Dave How exactly?
Theo I suggest that you write a countByBoolField utility function that counts the
number of times a field is true and false.
Dave OK, but before implementing this function, let me first rewrite the code of
lendingRatio, assuming this function already exists.
Theo You are definitely a fast learner, Dave!
Dave Thanks! I think that by using countByBoolField, the code for calculating the
lending ratio using a custom utility function would be something like this.
Listing14.13 Calculating the book lending ratio
function lendingRatio(books) {
var bookItems = flatMap(books, "bookItems");
var stats = countByBoolField(bookItems, "isLent", "lent", "notLent");
return stats.lent/(stats.lent + stats.notLent);
}
TIP Don’t use _.reduce or any other low-level data manipulation function inside
code that deals with business logic. Instead, write a utility function—with a proper
name—that hides _.reduce.
Theo Perfect. Don’t you think that this code is clearer than the code using _.reduce?
Dave I do! The code is both more concise and the intent is clearer. Let me see if I
can implement countByBoolField now.
Theo I suggest that you write a unit test first.
Dave Good idea.
Dave types for a bit. When he’s satisfied, he shows Theo the result.
Listing14.14 A unit test for countByBoolField
var input = [
{"a": true},
{"a": false},
{"a": true},

=== 페이지 333 ===
14.4 Unwinding at ease 305
{"a": true}
];
var expectedRes = {
"aTrue": 3,
"aFalse": 1
};
_.isEqual(countByBoolField(input, "a", "aTrue", "aFalse"), expectedRes);
Theo Looks good to me. Now, for the implementation of countByBoolField, I
think you are going to need our update function.
Dave I think you’re right. On each iteration, I need to increment the value of either
aTrue or aFalse using update and a function that increments a number by 1.
After a few minutes of trial and error, Dave comes up with the piece of code that uses
reduce, update, and inc. He shows Theo the code for countByBoolField.
Listing14.15 The implementation of countByBoolField
function inc (n) {
return n + 1;
}
function countByBoolField(coll, field, keyTrue, keyFalse) {
return _.reduce(coll, function(res, item) {
if (_.get(item, field)) {
return update(res, keyTrue, inc);
}
return update(res, keyFalse, inc);
}, {[keyTrue]: 0,
Creates a map with
[keyFalse]: 0});
keyTrue and keyFalse
}
associated to 0
Theo Well done! Shall we move on and review the third admin feature?
Dave The third feature is more complicated. I would like to use the teachings from
the first two features for the implementation of the third feature.
Theo OK. Call me when you’re ready for the code review.
14.4 Unwinding at ease
Dave really struggled with the implementation of the last admin feature, grouping books
by a physical library. After a couple of hours of frustration, Dave calls Theo for a rescue.
Dave I really had a hard time implementing the grouping by library feature.
Theo I only have a couple of minutes before my next meeting, but I can try to help
you. What’s the exact definition of grouping by library?
Dave Let me show you the unit test I wrote.

=== 페이지 334 ===
306 CHAPTER 14 Advanced data manipulation
Listing14.16 Unit test for grouping books by a library
var books = [
{
"isbn": "978-1779501127",
"title": "Watchmen",
"bookItems": [
{
"id": "book-item-1",
"libId": "nyc-central-lib",
"isLent": true
}
]
},
{
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
"bookItems": [
{
"id": "book-item-123",
"libId": "hudson-park-lib",
"isLent": true
},
{
"id": "book-item-17",
"libId": "nyc-central-lib",
"isLent": false
}
]
}
];
var expectedRes =
{
"hudson-park-lib": [
{
"bookItems": {
"id": "book-item-123",
"isLent": true,
"libId": "hudson-park-lib",
},
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
},
],
"nyc-central-lib": [
{
"bookItems": {
"id": "book-item-1",
"isLent": true,
"libId": "nyc-central-lib",
},
"isbn": "978-1779501127",
"title": "Watchmen",
},

=== 페이지 335 ===
14.4 Unwinding at ease 307
{
"bookItems": {
"id": "book-item-17",
"isLent": false,
"libId": "nyc-central-lib",
},
"isbn": "978-1982137274",
"title": "7 Habits of Highly Effective People",
},
],
};
_.isEqual(booksByRack(books) , expectedRes);
Theo Cool.... Writing unit tests before implementing complicated functions was
also helpful for me when I refactored Klafim from OOP to DOP.
Dave Writing unit tests for functions that receive and return data is much more fun
than writing unit tests for the methods of stateful objects.
TIP Before implementing a complicated function, write a unit test for it.
Theo What was difficult about the implementation of booksByLib?
Dave I started with a complicated implementation involving merge and reduce
before I remembered that you advised me to hide reduce behind a generic
function. But I couldn’t figure out what kind of generic function I needed.
Theo Indeed, it’s not easy to implement.
Dave I’m glad to hear that. I thought I was doing something wrong.
Theo The challenge here is that you need to work with book items, but the book title
and ISBN are not present in the book item map.
Dave Exactly!
Theo It reminds me a query I had to write a year ago on MongoDB, where data was
laid out in a similar way.
Dave And what did your query look like?
Theo I used MongoDB’s $unwind operator. Given a map m with a field <arr,
myArray>, it returns an array where each element is a map corresponding to m
without arr and with item associated to an element of myArray.
Dave That’s a bit abstract for me. Could you give me an example?
Theo moves to the whiteboard. He draws a diagram like the one in figure 14.2.
Theo In my case, I was dealing with an online store, where a customer cart was repre-
sented as a map with a customer-id field and an items array field. Each ele-
ment in the array represented an item in the cart. I wrote a query with unwind
that retrieved the cart items with the customer-id field.
Dave Amazing! That’s exactly what we need. Let’s write our own unwind function!

=== 페이지 336 ===
308 CHAPTER 14 Advanced data manipulation
{
"customer-id" : "joe",
// Other fields
"items" : [
{
"item" : "phone",
"quantity" : 1
},
{
"item" : "pencil",
"quantity" : 10 "items"
}
] map path
}
unwind
{ {
"customer-id" : "joe", "customer-id" : "joe",
// Other fields // Other fields
"items" : { res "items" : {
"item" : "phone", "item" : "pencil",
"quantity" : 1 "quantity" : 10
} }
} }
Figure 14.2 The behavior of unwind
Theo I’d be happy to pair program with you on this cool stuff, but I’m already run-
ning late for another meeting.
Dave I’m glad I’m not a manager!
When Theo leaves for his meeting, Dave goes to the kitchen and prepares himself a long
espresso as a reward for all that he’s accomplished today. He thoroughly enjoys it as he
works on the implementation of unwind.
As Joe advised, Dave starts by writing the code for booksByLib as if unwind were already
implemented. He needs to go over each book and unwind its book items using flatMap
and unwind. He then groups the book items by their libId using _.groupBy. Satisfied
with the resulting code, he finishes his espresso.
Listing14.17 Grouping books by a library using unwind
function booksByRack(books) {
var bookItems = flatMap(books, function(book) {
return unwind(book, "bookItems");
});
return _.groupBy(bookItems, "bookItems.libId")
}
Dave cannot believe that such a complicated function could be implemented so clearly
and compactly. Dave says to himself that the complexity must reside in the implementation
of unwind—but he soon finds out that he’s wrong; it is not going to be as complicated as
he thought! He starts by writing a unit test for unwind, similar to Theo’s MongoDB cus-
tomer cart scenario.

=== 페이지 337 ===
14.4 Unwinding at ease 309
Listing14.18 A unit test for unwind
var customer = {
"customer-id": "joe",
"items": [
{
"item": "phone",
"quantity": 1
},
{
"item": "pencil",
"quantity": 10
}
]
};
var expectedRes = [
{
"customer-id": "joe",
"items": {
"item": "phone",
"quantity": 1
}
},
{
"customer-id": "joe",
"items": {
"item": "pencil",
"quantity": 10
}
}
]
_.isEqual(unwind(customer, "items"), expectedRes)
The implementation of unwind is definitely not as complicated as Dave thought. It retrieves
the array arr associated with f in m and creates, for each element of arr, a version of m,
where f is associated with elem. Dave is happy to remember that data being immutable,
there is no need to clone m.
Listing14.19 The implementation of unwind
function unwind(map, field) {
var arr = _.get(map, field);
return _.map(arr, function(elem) {
return _.set(map, field, elem);
});
}
After a few moments of contemplating his beautiful code, Dave sends Theo a message with
a link to the pull request that implements grouping books by a library with unwind. After
that he leaves the office to go home, by bike, tired but satisfied.

=== 페이지 338 ===
310 CHAPTER 14 Advanced data manipulation
Summary
 Maintain a clear separation between the code that deals with business logic and
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
