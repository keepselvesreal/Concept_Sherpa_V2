# 2.4 DOP systems are easy to understand

**메타데이터:**
- ID: 22
- 레벨: 2
- 페이지: 64-65
- 페이지 수: 2
- 부모 ID: 17
- 텍스트 길이: 4804 문자

---

are easy to understand
Theo takes a look at the two diagrams that represent the high-level design of his system:
 The data entities in the data mind map in figure 2.8
 The code modules in the module diagram in figure 2.9
A bit perplexed, Theo asks Joe:
Theo I’m not sure that this system is better than a traditional OOP system where
objects encapsulate data.
Joe The main benefit of a DOP system over a traditional OOP system is that it’s eas-
ier to understand.
Theo What makes it easier to understand?
Joe The fact that the system is split cleanly into code modules and data entities.
Theo How does that help?
Joe When you try to understand the data entities of the system, you don’t have to
think about the details of the code that manipulates the data entities.
Theo So, when I look at the data mind map of my Library Management System, I can
understand it on its own?
Joe Exactly, and similarly, when you try to understand the code modules of the sys-
tem, you don’t have to think about the details of the data entities manipulated
by the code. There is a clear separation of concerns between the code and the
data.
Theo looks again at the data mind map in figure 2.8. He has kind of an Aha! moment:
Data lives on its own!
 NOTE A DOP system is easier to understand because the system is split into two
parts: data entities and code modules.

2.4 DOP systems are easy to understand 37
Books
Authors
Catalog
Book items
Library data Book lendings
Users
User management Members
Figure 2.8 A data mind map of the
Librarians
Library Management System
Now, Theo looks at the module diagram in figure 2.9. He feels a bit confused and asks Joe
for clarification:
 On one hand, the module diagram looks similar to the class diagrams from classic
OOP, boxes for classes and arrows for relations between classes.
 On the other hand, the code module diagram looks much simpler than the class
diagrams from classic OOP, but he cannot explain why.
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
Figure 2.9 The modules of the Library Management System with the function arguments
Theo The module diagram seems much simpler than the class diagrams I am used to
in OOP. I feel it, but I can’t put it into words.
Joe The reason is that module diagrams have constraints.

38 CHAPTER 2 Separation between code and data
Theo What kind of constraints?
Joe Constraints on the functions we saw before. All the functions are static (or
stateless), but there’s also constraints on the relations between the modules.
TIP All the functions in a DOP module are stateless.
Theo In what way are the relations between modules constrained?
Joe There is a single kind of relation between DOP modules—the usage relation. A
module uses code from another module. There’s no association, no composi-
tion, and no inheritance between modules. That’s what makes a DOP module
diagram easy to understand.
Theo I understand why there is no association and no composition between DOP
modules. After all, association and composition are data relations. But why no
inheritance relation? Does that mean that DOP is against polymorphism?
Joe That’s a great question! The quick answer is that in DOP, we achieve polymor-
phism with a different mechanism than class inheritance. We will talk about it
some day.
 NOTE For a discussion of polymorphism in DOP, see chapter 13.
Theo Now, you’ve piqued my curiosity. I thought inheritance was the only way to
achieve polymorphism.
Theo looks again at the module diagram in figure 2.9. Now he not only feels that this dia-
gram is simpler than traditional OOP class diagrams, he understands why it’s simpler: all
the functions are static, and all the relations between modules are of type usage. Table 2.1
summarizes Theo’s perception.
TIP The only kind of relation between DOP modules is the usage relation.
Table 2.1 What makes each part of a DOP system easy to understand
System part Constraint on entities Constraints on relations
Data entities Members only (no code) Association and composition
Code modules Stateless functions (no members) Usage (no inheritance)
TIP Each part of a DOP system is easy to understand because it provides constraints.