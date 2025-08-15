# 6.2.1 The tree of function calls

**ID**: 56  
**Level**: 3  
**추출 시간**: 2025-08-09 10:09:52 KST

---

6.2.1 The tree of function calls
The waiter brings Theo his café au lait and Joe his tight espresso. They continue their dis-
cussion while enjoying their coffees.
Joe Before writing a unit test for a code flow, I find it useful to visualize the tree of
function calls of the code flow.
Theo What do you mean by a tree of function calls?
Joe Here, I’ll draw the tree of function calls for the Library.searchBooksBy-
TitleJSON code flow.
Joe puts down his espresso and takes a napkin from the dispenser. He carefully places it
flat on the table and starts to draw. When he is done, he shows the illustration to Theo (see
figure 6.1).

## 페이지 142

114 CHAPTER 6 Unit tests
Library.searchBooksByTitleJSON
_.get JSON.stringify Catalog.searchBooksByTitle
_.get _.map _.filter Catalog.bookInfo
_.get Catalog.authorNames
_.get _.map
Figure 6.1 The tree of function calls for the search query code flow
Theo Nice! Can you teach me how to draw a tree of function calls like that?
Joe Sure. The root of the tree is the name of the function for which you draw the
tree, in our case, Library.searchBooksByTitleJSON. The children of a
node in the tree are the names of the functions called by the function. For exam-
ple, if you look again at the code for Library.searchBooksByTitleJSON (list-
ing 6.4), you’ll see that it calls Catalog.searchBooksByTitle, _.get, and
JSON.stringify.
Theo How long would I continue to recursively expand the tree?
Joe You continue until you reach a function that doesn’t belong to the code base
of your application. Those nodes are the leaves of our tree; for example, the
functions from Lodash: _.get, _.map, and so forth.
Theo What if the code of a function doesn’t call any other functions?
Joe A function that doesn’t call any other function would be a leaf in the tree.
Theo What about functions that are called inside anonymous functions like Catalog
.bookInfo?
Joe Catalog.bookInfo appears in the code of Catalog.searchBooksByTitle.
Therefore, it is considered to be a child node of Catalog.searchBooksBy-
Title. The fact that it is nested inside an anonymous function is not relevant
in the context of the tree of function calls.
 NOTE A tree of function calls for a function f is a tree where the root is f, and the
children of a node g in the tree are the functions called by g. The leaves of the tree are
functions that are not part of the code base of the application. These are functions
that don’t call any other functions.
Theo It’s very cool to visualize my code as a tree, but I don’t see how it relates to
unittests.

## 페이지 143

6.2 Unit tests for data manipulation code 115
Joe The tree of function calls guides us about the quality and the quantity of test
cases we should write.
Theo How?
Joe You’ll see in a moment.
