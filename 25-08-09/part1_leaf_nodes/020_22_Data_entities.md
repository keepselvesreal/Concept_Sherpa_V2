# 2.2 Data entities

**ID**: 20  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

2.2 Data entities 29
Joe steps up to a whiteboard and quickly draws a diagram to illustrate his comment. Fig-
ure 2.2 shows Joe’s drawing.
Code modules Stateless functions
Separate code from data
Data entities Only members
Figure 2.2 The separation between code and data
Theo It’s still not clear.
Joe It will become clearer when I show you how it looks in the context of your
Library Management System.
Theo OK. Shall we start with code or with data?
Joe Well, it’s data-oriented programming, so let’s start with data.
2.2 Data entities
In DOP, we start the design process by discovering the data entities of our system.
Here’s what Joe and Theo have to say about data entities.
Joe What are the data entities of your system?
Theo What do you mean by data entities?
Joe I mean the parts of your system that hold information.
 NOTE Data entities are the parts of your system that hold information.
Theo Well, it’s a Library Management System, so we have books and members.
Joe Of course, but there are more. One way to discover the data entities of a system
is to look for nouns and noun phrases in the requirements of the system.
Theo looks at Nancy’s requirement napkin. He highlights the nouns and noun phrases
that seem to represent data entities.
Highlighting terms in the requirements that correspond to data entities
 There are two kinds of users: library members and librarians.
 Users log in to the system via email and password.
 Members can borrow books.
 Members and librarians can search books by title or by author.
 Librarians can block and unblock members (e.g., when they are late in return-
ing a book).
 Librarians can list the books currently lent to a member.
 There could be several copies of a book.

## 페이지 58

30 CHAPTER 2 Separation between code and data
Joe Excellent. Can you see a natural way to group these entities?
Theo Not sure, but it seems to me that users, members, and librarians form one
group, whereas books, authors, and book copies form another group.
Joe Sounds good to me. What would you call each group?
Theo Probably user management for the first group and catalog for the second
group.
The data entities of the system organized in a nested list
 The catalog data
– Data about books
– Data about authors
– Data about book items
– Data about book lendings
 The user management data
– Data about users
– Data about members
– Data about librarians
Theo I’m not sure about the relations between books and authors. Should it be asso-
ciation or composition?
Joe Don’t worry too much about the details for the moment. We’ll refine our data
entity design later. For now, let’s visualize the two groups in a mind map.
Theo and Joe confer for a bit. Figure 2.3 shows the mind map they come up with.
Books
Authors
Catalog
Book items
Library data Book lendings
Users
User management Members
Librarians Figure 2.3 The data entities of the
system organized in a mind map

## 페이지 59

