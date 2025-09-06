# 14.4 Unwinding at ease

**메타데이터:**
- ID: 136
- 레벨: 2
- 페이지: 333-337
- 페이지 수: 5
- 부모 ID: 131
- 텍스트 길이: 7439 문자

---

t ease 305
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

310 CHAPTER 14 Advanced data manipulation