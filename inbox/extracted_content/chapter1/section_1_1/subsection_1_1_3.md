# 1.1.3 Explaining each piece of the class diagram

1.1.3 Explaining each piece of the class diagram
Dave Thanks for the UML refresher! Now I think I can remember what the different
arrows mean.
Theo My pleasure. Want to see how it all fits together?
Dave What class should we look at first?
Theo I think we should start with Library.
THE LIBRARY CLASS
The Library is the root class of the library system. Figure 1.6 shows the system structure.
CC Library
name : String
address : String
*
C Member
C Catalog
Bool isBlocked()
List<Book> search(searchCriteria, queryStr) Bool block()
BookItem addBookItem(librarian: Librarian, Bool unblock()
bookItem: BookItem) Bool returnBook(bookLending: BookLending)
BookLending checkout(bookItem: BookItem)
*
CC Librarian
Bool blockMember(member: Member)
Bool unblockMember(member: Member)
BookItem addBookItem(bookItem: BookItem)
List<BookLending> getBookLendingsOfMember
(member: Member)
Figure 1.6 The Library class

=== PAGE 38 ===
10 CHAPTER 1 Complexity of object-orientedprogramming
In terms of code (behavior), a Library object does nothing on its own. It delegates
everything to the objects it owns. In terms of data, a Library object owns
 Multiple Member objects
 Multiple Librarian objects
 A single Catalog object
 NOTE In this book, we use the terms code and behavior interchangeably.
LIBRARIAN, MEMBER, AND USER CLASSES
Librarian and Member both derive from User. Figure 1.7 shows this relation.
C Member C Librarian
isBlocked() : Bool blockMember(member: Member) : Bool
block() : Bool unblockMember(member: Member) : Bool
unblock() : Bool addBookItem(bookItem: BookItem) : BookItem
returnBook(bookLending : BookLending) : Bool : Member) :
checkout(bookItem: BookItem) : BookLending
CC User
id : String
email : String
password : String
login() : Bool
Figure 1.7 Librarian and Member derive from User.
The User class represents a user of the library:
 In terms of data members, it sticks to the bare minimum: it has an id, email,
and password (with no security and encryption for now).
 In terms of code, it can log in via login.
The Member class represents a member of the library:
 It inherits from User.
 In terms of data members, it has nothing more than User.
 In terms of code, it can
– Check out a book via checkout.
– Return a book via returnBook.
– Block itself via block.
– Unblock itself via unblock.
– Answer if it is blocked via isBlocked.
 It owns multiple BookLending objects.
 It uses BookItem in order to implement checkout.

=== PAGE 39 ===
1.1 OOP design: Classic or classical? 11
The Librarian class represents a librarian:
 It derives from User.
 In terms of data members, it has nothing more than User.
 In terms of code, it can
– Block and unblock a Member.
– List the member’s book lendings via getBookLendings.
– Add book items to the library via addBookItem.
 It uses Member to implement blockMember, unblockMember, and getBook-
Lendings.
 It uses BookItem to implement checkout.
 It uses BookLending to implement getBookLendings.
THE CATALOG CLASS
The Catalog class is responsible for the management of the books. Figure 1.8 shows
the relation among the Catalog, Librarian, and Book classes. In terms of code, a
Catalog object can
 Search books via search.
 Add book items to the library via addBookItem.
C Catalog
List<Book> search(searchCriteria, queryStr)
BookItem addBookItem(librarian: Librarian, bookItem: BookItem)
C Librarian *
C Book
Bool blockMember(member: Member)
Bool unblockMember(member: Member) id : String
BookItem addBookItem(bookItem: BookItem) title : String
List<BookLending> getBookLendingsOfMember (member: Member)
Figure 1.8 The Catalog class
A Catalog object uses Librarian in order to implement addBookItem. In terms of
data, a Catalog owns multiple Book objects.
THE BOOK CLASS
Figure 1.9 presents the Book class. In terms of data, a Book object
 Should have as its bare minimum an id and a title.
 Is associated with multiple Author objects (a book might have multiple authors).
 Owns multiple BookItem objects, one for each copy of the book.

=== PAGE 40 ===
12 CHAPTER 1 Complexity of object-orientedprogramming
C Book
id : String
*
title : String
* *
C BookItem C Author
id : String id : String
Iibld: String fullName: String
BookLending checkout(member: Member)
C BookLending
id : String
lendingDate : date
dueDate : date
Bool isLate()
Bool returnBook() Figure 1.9 The Book class
THE BOOKITEM CLASS
The BookItem class represents a book copy, and a book could have many copies. In
terms of data, a BookItem object
 Should have as its bare minimum data for members: an id and a libId (for its
physical library ID).
 Owns multiple BookLending objects, one for each time the book is lent.
In terms of code, a BookItem object can be checked out via checkout.