# 2.5 DOP systems are flexible

**메타데이터:**
- ID: 23
- 레벨: 2
- 페이지: 66-69
- 페이지 수: 4
- 부모 ID: 17
- 텍스트 길이: 6542 문자

---

are flexible
Theo I see how a sharp separation between code and data makes DOP systems easier
to understand than classic OOP systems. But what about adapting to changes
in requirements?
Joe Another benefit of DOP systems is that it is easy to extend them and to adapt to
changing requirements.

2.5 DOP systems are flexible 39
Theo I remember that, when Nancy asked me to add Super members and VIP mem-
bers to the system, it was hard to adapt my OOP system. I had to introduce a
few base classes, and the class hierarchy became really complex.
Joe I know exactly what you mean. I’ve experienced the same kind of struggle so
many times. Describe the changes in the requirements for Super members and
VIP members, and I’m quite sure that you’ll see how easy it would be to extend
your DOP system.
The requirements for Super members and VIP members
 Super members are members that are allowed to list the book lendings to
other members.
 VIP members are members that are allowed to add book items to the library.
Theo opens his IDE and starts to code the getBookLendings function of the Library
module (see listing 2.3), first without addressing the requirements for Super members.
Theo remembers what Joe told him about module functions in DOP:
 Functions are stateless.
 Functions receive the data they manipulate as their first argument.
In terms of functionality, getBookLendings has two parts:
 Checks that the user is a librarian.
 Retrieves the book lendings from the catalog.
Basically, the code of getBookLendings has two parts as well:
 Calls the isLibrarian function from the UserManagement module and passes it
the UserManagementData.
 Calls the getBookLendings function from the Catalog module and passes it the
CatalogData.
Listing2.3 Getting the book lendings of a member
class Library {
static getBookLendings(libraryData, userId, memberId) {
if(UserManagement.isLibrarian(libraryData.userManagement, userId)) {
return Catalog.getBookLendings(libraryData.catalog, memberId);
} else {
throw "Not allowed to get book lendings";
There are other
}
ways to manage
}
errors.
}
class UserManagement {
static isLibrarian(userManagementData, userId) {
// will be implemented later
In chapter 3, we will see how
}
to manage permissions with
}
generic data collections.

40 CHAPTER 2 Separation between code and data
class Catalog {
static getBookLendings(catalogData, memberId) {
// will be implemented later
In chapter 3, we will see how
}
to query data with generic
}
data collections.
It’s Theo’s first piece of DOP code and passing around all those data objects—library-
Data, libraryData.userManagement, and libraryData.catalog—feels a bit awkward.
But he did it! Joe looks at Theo’s code and seems satisfied.
Joe Now, how would you adapt your code to Super members?
Theo I would add a function isSuperMember to the UserManagement module and
call it from Library.getBookLendings.
Joe Exactly! It’s as simple as that.
Theo types the code on his laptop so that he can show it to Joe. Here’s how Theo adapts
his code for Super members.
Listing2.4 Allowing Super members to get the book lendings of a member
class Library {
static getBookLendings(libraryData, userId, memberId) {
if(Usermanagement.isLibrarian(libraryData.userManagement, userId) ||
Usermanagement.isSuperMember(libraryData.userManagement, userId)) {
return Catalog.getBookLendings(libraryData.catalog, memberId);
} else {
throw "Not allowed to get book lendings";
There are other
}
ways to manage
}
errors.
}
class UserManagement {
static isLibrarian(userManagementData, userId) {
// will be implemented later
In chapter 3, we will see how
}
to manage permissions with
static isSuperMember(userManagementData, userId) {
generic data collections.
// will be implemented later
}
}
class Catalog {
static getBookLendings(catalogData, memberId) {
// will be implemented later
In chapter 3, we will see how
}
to query data with generic
}
data collections.
Now, the awkward feeling caused by passing around all those data objects is dominated by
a feeling of relief. Adapting to this change in requirements takes only a few lines of code
and requires no changes in the system design. Once again, Joe seems satisfied.
TIP DOP systems are flexible. Quite often they adapt to changing requirements with-
out changing the system design.

2.5 DOP systems are flexible 41
Theo starts coding addBookItem. He looks at the signature of Library.addBookItem,
and the meaning of the third argument bookItemInfo isn’t clear to him. He asks Joe for
clarification.
Listing2.5 The signature of Library.addBookItem
class Library {
static addBookItem(libraryData, userId, bookItemInfo) {
}
}
Theo What is bookItemInfo?
Joe Let’s call it the book item information. Imagine we have a way to represent this
information in a data entity named bookItemInfo.
Theo You mean an object?
Joe For now, it’s OK to think about bookItemInfo as an object. Later on, I will
show you how to we represent data in DOP.
Besides this subtlety about how the book item information is represented by book-
ItemInfo, the code for Library.addBookItem in listing 2.6 is quite similar to the code
Theo wrote for Library.getBookLendings in listing 2.4. Once again, Theo is amazed by
the fact that adding support for VIP members requires no design change.
Listing2.6 Allowing VIP members to add a book item to the library
class Library {
static addBookItem(libraryData, userId, bookItemInfo) {
if(UserManagement.isLibrarian(libraryData.userManagement, userId) ||
UserManagement.isVIPMember(libraryData.userManagement, userId)) {
return Catalog.addBookItem(libraryData.catalog, bookItemInfo);
} else {
throw "Not allowed to add a book item";
There are other
}
ways to manage
}
errors.
}
class UserManagement {
static isLibrarian(userManagementData, userId) {
// will be implemented later
In chapter 3, we will see how
}
to manage permissions with
static isVIPMember(userManagementData, userId) {
generic data collections.
// will be implemented later
}
}
class Catalog {
static addBookItem(catalogData, memberId) {
// will be implemented later
In chapter 4, we will see how
}
to manage state of the system
}
with immutable data.

42 CHAPTER 2 Separation between code and data
Theo It takes a big mindset shift to learn how to separate code from data!
Joe What was the most challenging thing to accept?
Theo The fact that data is not encapsulated in objects.
Joe It was the same for me when I switched from OOP to DOP.
Now it’s time to eat! Theo takes Joe for lunch at Simple, a nice, small restaurant near the
office.