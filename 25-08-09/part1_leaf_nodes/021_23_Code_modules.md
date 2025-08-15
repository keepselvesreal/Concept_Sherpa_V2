# 2.3 Code modules

**ID**: 21  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

2.3 Code modules 31
The most precise way to visualize the data entities of a DOP system is to draw a data
entity diagram with different arrows for association and composition. We will come
back to data entity diagrams later.
TIP Discover the data entities of your system and then sort them into high-level
groups, either as a nested list or as a mind map.
We will dive deeper into the design and representation of data entities in the next
chapter. For now, let’s simplify things and say that the data of our library system is
made of two high-level groups: user management and catalog.
2.3 Code modules
The second step of the design process in DOP is to define the code modules. Let’s lis-
ten in on Joe and Theo again.
Joe Now that you have identified the data entities of your system and have
arranged them into high-level groups, it’s time to think about the code part of
your system.
Theo What do you mean by the code part?
Joe One way to think about that is to identity the functionality of your system.
Theo looks again at Nancy’s requirements. This time he highlights the verb phrases that
represent functionality.
Highlighting terms in the requirements that correspond to functionality
 There are two kinds of users: library members and librarians.
 Users log in to the system via email and password.
 Members can borrow books.
 Members and librarians can search books by title or by author.
 Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
 Librarians can list the books currently lent to a member.
 There could be several copies of a book.
In addition, it’s obvious to Theo that members can also return a book. Moreover, there
should be a way to detect whether a user is a librarian or not. He adds those to the require-
ments and then lists the functionality of the system.
The functionality of the library system
 Search for a book.
 Add a book item.
 Block a member.

## 페이지 60

32 CHAPTER 2 Separation between code and data
(continued)
 Unblock a member.
 Log a user into the system.
 List the books currently lent to a member.
 Borrow a book.
 Return a book.
 Check whether a user is a librarian.
Joe Excellent! Now, tell me what functionality needs to be exposed to the outside
world?
Theo What do you mean by exposed to the outside world?
Joe Imagine that the Library Management System exposes an API over HTTP.
What functionality would be exposed by the HTTP endpoints?
Theo Well, all system functionality would be exposed except checking to see if a user
is a librarian.
Joe OK. Now give each exposed function a short name and gather them together
in a module box called Library.
That takes Theo less than a minute. Figure 2.4 shows the module that contains the
exposed functions of the library devised by Theo.
C Library
searchBook()
addBookItem()
blockMember()
unblockMember()
getBookLendings() Figure 2.4 The Library module
checkoutBook() contains the exposed functions of the
returnBook() Library Management System.
TIP The first step in designing the code part of a DOP system is to aggregate the
exposed functions into a single module.
Joe Beautiful! You just created your first code module.
Theo To me it looks like a class. What’s the difference between a module and a class?
Joe A module is an aggregation of functions. In OOP, a module is represented
bya class, but in other programming languages, it might be a package or a
namespace.
Theo I see.
Joe The important thing about DOP code modules is that they contain only state-
less functions.
Theo You mean like static methods in Java?
Joe Yes, and the classes of these static methods should not have any data members.

## 페이지 61

2.3 Code modules 33
Theo So, how do the functions know what piece of information they operate on?
Joe Easy. We pass that as the first argument to the function.
Theo OK. Can you give me an example?
Joe, biting his nails, takes a look at the list of functions of the Library module in figure 2.4.
He spots a likely candidate.
Joe Let’s take, for example, getBookLendings. In classic OOP, what would its
arguments be?
Theo A librarian ID and a member ID.
Joe So, in traditional OOP, getBookLendings would be a method of a Library
class that receives two arguments: librarianId and memberId.
Theo Yep.
Joe Now comes the subtle part. In DOP, getBookLendings is part of the Library
module, and it receives the LibraryData as an argument.
Theo Could you show me what you mean?
Joe Sure.
Joe goes over to Theo’s keyboard and starts typing. He enters an example of what a class
method looks like in OOP:
class Library {
catalog
userManagement
getBookLendings(userId, memberId) {
// accesses library state via this.catalog and this.userManagement
}
}
Theo Right! The method accesses the state of the object (in our case, the library
data) via this.
Joe Would you say that the object’s state is an argument of the object’s methods?
Theo I’d say that the object’s state is an implicit argument to the object’s methods.
TIP In traditional OOP, the state of the object is an implicit argument to the meth-
ods of the object.
Joe Well, in DOP, we pass data as an explicit argument. The signature of getBook-
Lendings would look like this.
Listing2.1 The signature of getBookLendings
class Library {
static getBookLendings(libraryData, userId, memberId) {
}
}

## 페이지 62

34 CHAPTER 2 Separation between code and data
Joe The state of the library is stored in libraryData, and libraryData is passed
to the getBookLendings static method as an explicit argument.
Theo Is that a general rule?
Joe Absolutely! The same rule applies to the other functions of the Library mod-
ule and to other modules as well. All of the modules are stateless—they receive
the library data that they manipulate as an argument.
TIP In DOP, functions of a code module are stateless. They receive the data that they
manipulate as an explicit argument, which is usually the first argument.
 NOTE A module is an aggregation of functions. In DOP, the module functions are
stateless.
Theo It reminds me of Python and the way the self argument appears in method
signatures. Here, let me show you an example.
Listing2.2 A Python object as an explicit argument in method signatures
class Library:
catalog = {}
userManagement = {}
def getBookLendings(self, userId, memberId):
# accesses library state via self.catalog and self.userManagement
Joe Indeed, but the difference I’m talking about is much deeper than a syntax
change. It’s about the fact that data lives outside the modules.
Theo I got that. As you said, module functions are stateless.
Joe Exactly! Would you like to try and apply this principle across the whole
Library module?
Theo Sure.
Theo refines the design of the Library module by including the details about the func-
tions’ arguments. He presents the diagram in figure 2.5 to Joe.
C Library
searchBook(libraryData, searchQuery)
addBookItem(libraryData, bookItemInfo)
blockMember(libraryData, memberId)
unblockMember(libraryData, memberId)
login(libraryData, loginInfo)
getBookLendings(libraryData, userId)
checkoutBook(libraryData, userId, bookItemId) Figure 2.5 The Library module
returnBook(libraryData, userId, bookItemId)
with the functions’ arguments
Joe Perfect. Now, we’re ready to tackle the high-level design of our system.
Theo What’s a high-level design in DOP?

## 페이지 63

2.3 Code modules 35
Joe A high-level design in DOP is the definition of modules and the interaction
between them.
Theo I see. Are there any guidelines to help me define the modules?
Joe Definitely. The high-level modules of the system correspond to the high-level
data entities.
Theo You mean the data entities that appear in the data mind map?
Joe Exactly!
Theo looks again at the data mind map (figure 2.6). He focuses on the high-level data enti-
ties library, catalog, and user management. This means that in the system, besides the
Library module, we have two high-level modules:
 The Catalog module deals with catalog data.
 The UserManagement module deals with user management data.
Catalog
Library data Figure 2.6 A mind map of the high-
level data entities of the Library
User management
Management System
Theo then draws the high-level design of the Library Management System with the Catalog
and UserManagement modules. Figure 2.7 shows the addition of these modules, where:
 Functions of Catalog receive catalogData as their first argument.
 Functions of UserManagement receive userManagementData as their first argument.
C Library
searchBook(libraryData, searchQuery)
addBookItem(libraryData, bookItemInfo)
blockMember(libraryData, memberId)
unblockMember(libraryData, memberId)
login(libraryData, loginInfo)
getBookLendings(libraryData, userId)
checkoutBook(libraryData, userId, bookItemId)
returnBook(libraryData, userId, bookItemId)
C Catalog
C UserManagement
searchBook(catalogData, searchQuery)
blockMember(userManagementData, memberId)
addBookItem(catalogData, bookItemInfo)
unblockMember(userManagementData, memberId)
checkoutBook(catalogData, bookItemId)
login(userManagementData, loginInfo)
returnBook(catalogData, bookItemId)
isLibrarian(userManagementData, userId)
getBookLendings(catalogData, userId)
Figure 2.7 The modules of the Library Management System with their functions’ arguments

## 페이지 64

36 CHAPTER 2 Separation between code and data
It’s not 100% clear for Theo at this point how the data entities get passed between mod-
ules. For the moment, he thinks of libraryData as a class with two members:
 catalog holds the catalog data.
 userManagement holds the user management data.
Theo also sees that the functions of Library share a common pattern. (Later on in this
chapter, we’ll see the code for some functions of the Library module.)
 They receive libraryData as an argument.
 They pass libraryData.catalog to the functions of Catalog.
 They pass libraryData.userManagement to the functions of UserManagement.
TIP The high-level modules of a DOP system correspond to the high-level data enti-
ties.
