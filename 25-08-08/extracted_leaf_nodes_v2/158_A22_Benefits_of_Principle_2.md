# A.2.2 Benefits of Principle #2

**메타데이터:**
- ID: 158
- 레벨: 2
- 페이지: 374-374
- 페이지 수: 1
- 부모 ID: 155
- 텍스트 길이: 3326 문자

---

f Principle #2
Using generic data structures to represent data has multiple benefits. We cover these
benefits in greater detail in the following sections:
 The ability to use generic functions that are not limited to our specific use case
 A flexible data model
USING FUNCTIONS THAT ARE NOT LIMITED TO A SPECIFIC USE CASE
Using generic data structures to represent data makes it possible to manipulate data
with a rich set of functions that are available on those data structures natively in our
programming language. Additionally, third-party libraries also provide more of these
functions. For instance, JavaScript natively provides some basic functions on maps and
arrays, and third-party libraries like Lodash (https://lodash.com/) extend the func-
tionality with even more functions. There is a famous quote by Alan Perlis that sum-
marizes this benefit:
It is better to have 100 functions operate on one data structure than to have 10 functions
operate on 10 data structures.
—Alan Perlis (“Epigrams on Programming,” 1982)
When an author is represented as a map, the author can be serialized into JSON
using JSON.stringify(), which is part of JavaScript. The following listing provides
an example.
ListingA.15 [#serialize-klipse-js],reftext="A.1"
var data = createAuthorData("Isaac", "Asimov", 500);
JSON.stringify(data);
// → "{\"firstName\":\"Isaac\",\"lastName\":\"Asimov\",\"books\":500}"
Serializing author data without the number of books can be accomplished via Lodash’s
_.pick() function. The following listing uses _.pick() to create an object with a sub-
set of keys.

A.2 Principle #2: Represent data with generic data structures 347
ListingA.16 Manipulating data with generic functions
var data = createAuthorData("Isaac", "Asimov", 500);
var dataWithoutBooks = _.pick(data, ["firstName", "lastName"]);
JSON.stringify(dataWithoutBooks);
// → "{\"firstName\":\"Isaac\",\"lastName\":\"Asimov\"}"
TIP When adhering to Principle #2, a rich set of functionality is available for data
manipulation.
FLEXIBLE DATA MODEL
When using generic data structures, the data model is flexible, and data is not forced
into a specific shape. Data can be created with no predefined shape, and its shape can
be modified at will.
In classic OOP, when not adhering to Principle #2, each piece of data is instanti-
ated via a class and must follow a rigid shape. When a slightly different data shape is
needed, a new class must be defined. Take, for example, AuthorData, a class that rep-
resents an author entity made of three fields: firstName, lastName, and books. Sup-
pose that you want to add a field called fullName with the full name of the author. If
we fail to adhere to Principle #2, a new class, AuthorDataWithFullName, must be
defined. However, when using generic data structures, fields can be added to (or
removed from) a map on the fly as the following listing shows.
ListingA.17 Adding a field on the fly
var data = createAuthorData("Isaac", "Asimov", 500);
data.fullName = "Isaac Asimov";
TIP Working with a flexible data model is particularly useful in applications where
the shape of the data tends to be dynamic (e.g., web apps and web services).
Part 1 of the book explores in detail the benefits of a flexible data model in real-world
applications. Next, let’s explore the cost for adhering to Principle #2.