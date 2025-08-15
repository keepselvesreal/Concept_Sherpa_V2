# 4.2 Structural sharing

**ID**: 36  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

4.2 Structural sharing
As mentioned in the previous section, structural sharing enables the efficient cre-
ation of new versions of immutable data. In DOP, we use structural sharing in the
calculation phase of a mutation to compute the next state of the system based on
the current state of the system. Inside the calculation phase, we don’t have to deal
with state management; that is delayed to the commit phase. As a consequence, the
code involved in the calculation phase of a mutation is stateless and is as simple as
the code of a query.
Theo I’m really intrigued by this more efficient way to create new versions of data.
How does it work?
Joe Let’s take a simple example from our library system. Imagine that you want to
modify the value of a field in a book in the catalog; for instance, the publica-
tion year of Watchmen. Can you tell me the information path for Watchmen’s
publication year?
Theo takes a quick look at the catalog data in figure 4.2. Then he answers Joe’s question.

## 페이지 103

4.2 Structural sharing 75
catalog
booksByIsbn authorsById
978-1779501127 alan-moore
title isbn name
Watchmen 978-1779501127 Alan Moore
authorIds publicationYear bookIsbns
1987
1 0 0
bookItems
dave-gibbons alan-moore 978-1779501127
1 0 dave-gibbons
id id name
book-item-2 book-item-1 Dave Gibbons
libId libId bookIsbns
la-central-lib nyc-cental-lib
0
isLent isLent
978-1779501127
false true
Figure 4.2 Visualization of the catalog data. The nodes in the information path to Watchmen’s publication
year are marked with a dotted border.
Theo The information path for Watchmen’s publication year is ["catalog", "books-
ByIsbn", "978-1779501127", "publicationYear"].
Joe Now, let me show how you to use the immutable function _.set that Lodash
also provides.
Theo Wait! What do you mean by an immutable function? When I looked at the
Lodash documentation for _.set on their website, it said that it mutates the
object.
Joe You’re right, but the default Lodash functions are not immutable. In order to
use an immutable version of the functions, we need to use the Lodash FP mod-
ule as explained in the Lodash FP guide.
 NOTE See https://lodash.com/docs/4.17.15#set to view Lodash’s documentation
for _.set, and see https://github.com/lodash/lodash/wiki/FP-Guide to view the
Lodash FP guide.
Theo Do the immutable functions have the same signature as the mutable functions?
Joe By default, the order of the arguments in immutable functions is shuffled.
The Lodash FP guide explains how to resolve this. With this piece of code,

## 페이지 104

76 CHAPTER 4 State management
the signature of the immutable functions is exactly the same as the mutable
functions.
Listing4.1 Configuring Lodash so immutable and mutable functions have same signature
_ = fp.convert({
"cap": false,
"curry": false,
"fixed": false,
"immutable": true,
"rearg": false
});
TIP In order to use Lodash immutable functions, we use Lodash’s FP module, and
we configure it so that the signature of the immutable functions is the same as in the
Lodash documentation web site.
Theo So basically, I can still rely on Lodash documentation when using immutable
versions of the functions.
Joe Except for the piece in the documentation that says the function mutates the
object.
Theo Of course!
Joe Now I’ll show you how to write code that creates a version of the library data
with the immutable function _.set.
Joe’s fingers fly across Theo’s keyboard. Theo then looks at Joe’s code, which creates a ver-
sion of the library data where the Watchmen publication year is set to 1986.
Listing4.2 Using _.set as an immutable function
var nextLibraryData = _.set(libraryData,
["catalog", "booksByIsbn",
"978-1779501127", "publicationYear"],
1986);
 NOTE A function is said to be immutable when, instead of mutating the data, it cre-
ates a new version of the data without changing the data it receives.
Theo You told me earlier that structural sharing allowed immutable functions to be
efficient in terms of memory and computation. Can you tell me what makes
them efficient?
Joe With pleasure, but before that, you have to answer a series of questions. Are
you ready?
Theo Yes, sure...
Joe What part of the library data is impacted by updating the Watchmen publication
year: the UserManagement or the Catalog?

## 페이지 105

4.2 Structural sharing 77
Theo Only the Catalog.
Joe What part of the Catalog?
Theo Only the booksByIsbn index.
Joe What part of the booksByIsbn index?
Theo Only the Book record that holds the information about Watchmen.
Joe What part of the Book record?
Theo Only the publicationYear field.
Joe Perfect! Now, suppose that the current version of the library data looks like
this.
Joe goes to the whiteboard and draws a diagram. Figure 4.3 shows the result.
Library
Catalog UserManagement
authorsByld booksBylsbn ...
... watchmen
title:Watchmen publicationYear:1987 authorlds
...
Figure 4.3 High-level visualization of the current version of Library
Theo So far, so good...
Joe Next, let me show you what an immutable function does when you use it to cre-
ate a new version of Library, where the publication year of Watchmen is set to
1986 instead of 1987.
Joe updates his diagram on the whiteboard. It now looks like figure 4.4.

## 페이지 106

78 CHAPTER 4 State management
«Next»
Library
Library
«Next»
Catalog UserManagement
Catalog
«Next»
booksByIsbn ... authorsById
booksByIsbn
«Next»
watchmen ...
watchmen
«Next»
publicationYear:1987 title:Watchmen authorlds
publicationYear:1986
...
Figure 4.4 Structural sharing provides an efficient way to create a new version of the data.
Next Library is recursively made of nodes that use the parts of Library that are
common between the two.
Theo Could you explain?
Joe The immutable function creates a fresh Library hash map, which recursively
uses the parts of the current Library that are common between the two ver-
sions instead of deeply copying them.
Theo It’s a bit abstract for me.
Joe The next version of Library uses the same UserManagement hash map as the
old one. The Catalog inside the next Library uses the same authorsById as
the current Catalog. The Watchmen Book record inside the next Catalog uses
all the fields of the current Book except for the publicationYear field.
Theo So, in fact, most parts of the data are shared between the two versions. Right?
Joe Exactly! That’s why this technique is called structural sharing.
TIP Structural sharing provides an efficient way (both in terms of memory and com-
putation) to create a new version of the data by recursively sharing the parts that don’t
need to change.
Theo That’s very cool!
Joe Indeed. Now let’s look at how to write a mutation for adding a member using
immutable functions.

## 페이지 107

4.2 Structural sharing 79
Once again, Joe goes to the whiteboard. Figure 4.5 shows the diagram that Joe draws to
illustrate how structural sharing looks when we add a member.
«Next»
Library
Library
«Next»
UserManagement Catalog
userManagement
«Next»
members librarians ...
members
Figure 4.5 Adding a member
with structural sharing. Most of
the data is shared between the
... member0 member1
two versions.
Theo Awesome! The Catalog and the librarians hash maps don’t have to be copied!
Joe Now, in terms of code, we have to write a Library.addMember function that
delegates to UserManagement.addMember.
Theo I guess it’s going to be similar to the code we wrote earlier to implement the
search books query, where Library.searchBooksByTitleJSON delegates to
Catalog.searchBooksByTitle.
Joe Similar in the sense that all the functions are static, and they receive the data
they manipulate as an argument. But there are two differences. First, a muta-
tion could fail, for instance, if the member to be added already exists. Second,
the code for Library.addMember is a bit more elaborate than the code for
Library.searchBooksByTitleJSON because we have to create a new version
of Library that refers to the new version of UserManagement. Here, let me
show you an example.
Listing4.3 The code for the mutation that adds a member
UserManagement.addMember = function(userManagement, member) {
var email = _.get(member, "email");
var infoPath = ["membersByEmail", email];
if(_.has(userManagement, infoPath)) {
Checks if a member with
throw "Member already exists.";
the same email address
}
already exists
var nextUserManagement = _.set(
userManagement,
Creates a new version of
infoPath,
userManagement that
member);
includes the member
return nextUserManagement;
};

## 페이지 108

80 CHAPTER 4 State management
Library.addMember = function(library, member) {
var currentUserManagement = _.get(library, "userManagement");
var nextUserManagement = UserManagement.addMember(
currentUserManagement,
member);
var nextLibrary = _.set(library,
"userManagement",
nextUserManagement);
Creates a new version of
return nextLibrary;
library that contains the new
};
version of userManagement
Theo To me, it’s a bit weird that immutable functions return an updated version of
the data instead of changing it in place.
Joe It was also weird for me when I first encountered immutable data in Clojure
seven years ago.
Theo How long did it take you to get used to it?
Joe A couple of weeks.
