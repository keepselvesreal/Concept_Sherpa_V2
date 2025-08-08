# 3.1 Designing a data model

**메타데이터:**
- ID: 27
- 레벨: 2
- 페이지: 72-75
- 페이지 수: 4
- 부모 ID: 25
- 텍스트 길이: 7443 문자

---

data model
During lunch at Simple, Theo and Joe don’t talk about programming. Instead, they start
getting to know each other on a personal level. Theo discovers that Joe is married to Kay,
who has just opened her creative therapy practice after many years of studying various
fields related to well-being. Neriah, their 14-year-old son, is passionate about drones, whereas
Aurelia, their 12-year-old daughter, plays the transverse flute.
Joe tells Theo that he’s been practicing meditation for 10 years. Meditation, he says, has
taught him how to break away from being continually lost in a “storm thought” (especially
negative thoughts, which can be the source of great suffering) to achieve a more direct
relationship with reality. The more he learns to experience reality as it is, the calmer his
mind. When he first started to practice meditation, it was sometimes difficult and even
weird, but by persevering, he has increased his feeling of well-being with each passing year.
When they’re back at the office, Joe tells Theo that his next step in their DOP journey
will be about data models. This includes data representation.
Joe When we design the data part of our system, we’re free to do it in isolation.
Theo What do you mean by isolation?
Joe I mean that you don’t have to bother with code, only data.
Theo Oh, right. I remember you telling me how that makes a DOP system simpler
than OOP. Separation of concerns is a design principle I’m used to in OOP.
Joe Indeed.
Theo And, when we think about data, the only relations we have to think about are
association and composition.
Joe Correct.
Theo Will the data model design be significantly different than the data model I’m
used to designing as an OOP developer?
Joe Not so much.
Theo OK. Let me see if I can draw a DOP-style data entity diagram.
Theo takes a look at the data mind map that he drew earlier in the morning. He then
draws the diagram in figure 3.1.
He refines the details of the fields of each data entity and the kind of relations between
entities. Figure 3.2 shows the result of this redefined data entity diagram.

3.1 Designing a data model 45
Books
Authors
Catalog
Book items
Library data Book lendings
Users
User management Members
Librarians Figure 3.1 A data mind map of
the Library Management System
CC Library
name: String
address: String
CC Catalog CC UserManagement
* * *
CC Book CC Librarian CC Member
email: String email: String
title : String
password: String password: String
publicationYear: Number
*
ISBN: String
publisher: String
* *
CC Author CC BookLending
name: String lendingDate: String
CC BookItem
* libld: String
purchaseDate: String
Figure 3.2 A data model of the Library Management System

46 CHAPTER 3 Basic data manipulation
Joe The next step is to be more explicit about the relations between entities.
Theo What do you mean?
Joe For example, in your entity diagram, Book and Author are connected by a
many-to-many association relation. How is this relation going to be repre-
sented in your program?
Theo In the Book entity, there will be a collection of author IDs, and in the Author
entity, there will be a collection of book IDs.
Joe Sounds good. And what will the book ID be?
Theo The book ISBN.
 NOTE The International Standard Book Number (ISBN) is a numeric commercial
book identifier that is intended to be unique.
Joe And where will you hold the index that enables you to retrieve a Book from its
ISBN?
Theo In the Catalog because the catalog holds a bookByISBN index.
Joe What about author ID?
Theo Author ID is the author name in lowercase and with dashes instead of white
spaces (assuming that we don’t have two authors with the same name).
Joe And I guess that you also hold the author index in the Catalog?
Theo Exactly!
Joe Excellent. You’ve been 100% explicit about the relation between Book and
Author. I’ll ask you to do the same with the other relations of the system.
It’s quite easy for Theo to do, as he has done that so many times as an OOP developer. Fig-
ure 3.3 provides the detailed entity diagram of Theo’s system.
 NOTE By positional collection, we mean a collection where the elements are in order
(like a list or an array). By index, we mean a collection where the elements are accessi-
ble via a key (like a hash map or a dictionary).
The Catalog entity contains two indexes:
 booksByIsbn—The keys are book ISBNs, and the values are Book entities. Its type is
noted as {Book}.
 authorsById—The keys are author IDs, and the values are Author entities. Its type
is noted as {Author}.
Inside a Book entity, we have authors, which is a positional collection of author IDs of type
[String]. Inside an Author entity, we have books, which is a collection of book IDs of
type [String].
 NOTE For the notation for collections and index types, a positional collection of
Strings is noted as [String]. An index of Books is noted as {Book}. In the context of
a data model, the index keys are always strings.

3.1 Designing a data model 47
CC Library
name: String
address: String
catalog: Catalog
userManagement: UserManagement
CC Catalog CC UserManagement
booksByIsbn: {Book} librariansByEmail: {Librarian}
authorsById: {Author} membersByEmail: {Member}
*
*
* CC Author CC Librarian
CC Book i n d a : m S e tr : i n S g tring email: String CC Me * mber
title : String encryptedPassword: String
bookIsbns: [String] email: String
publicationYear: Number
encryptedPassword: String
isbn: String *
isBlocked: Boolean
authorIds: [String]
bookLendings: [BookLending]
bookItems: [BookItem] *
CC BookLending
lendingDate: String
bookItemId: String *
CC BookItem
bookIsbn: String
id: String
libId: String
*
purchaseDate: String
isLent: Boolean
Figure 3.3 Library management relation model. Dashed lines (e.g., between Book and Author) denote
indirect relations, [String] denotes a positional collection of strings, and {Book} denotes an index of
Books.
There is a dashed line between Book and Author, which means that the relation between
Book and Author is indirect. To access the collection of Author entities from a Book entity,
we’ll use the authorById index defined in the Catalog entity.
Joe I like your data entity diagram.
Theo Thank you.
Joe Can you tell me what the three kinds of data aggregations are in your diagram
(and, in fact, in any data entity diagram)?
Theo Let’s see...we have positional collections like authors in Book. We have
indexes like booksByIsbn in Catalog. I can’t find the third one.
Joe The third kind of data aggregation is what we’ve called, until now, an “entity”
(like Library, Catalog, Book, etc.), and the common term for entity in com-
puter science is record.

48 CHAPTER 3 Basic data manipulation
 NOTE A record is a data structure that groups together related data items. It’s a col-
lection of fields, possibly of different data types.
Theo Is it correct to say that a data entity diagram consists only of records, positional
collections, and indexes?
Joe That’s correct. Can you make a similar statement about the relations between
entities?
Theo The relations in a data entity diagram are either composition (solid line with a
full diamond) or association (dashed line with an empty diamond). Both types
of relations can be either one-to-one, one-to-many, or many-to-many.
Joe Excellent!
TIP A data entity diagram consists of records whose values are either primitives, posi-
tional collections, or indexes. The relation between records is either composition or
association.