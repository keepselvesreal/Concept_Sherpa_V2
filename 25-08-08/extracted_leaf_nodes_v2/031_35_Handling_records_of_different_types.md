# 3.5 Handling records of different types

**메타데이터:**
- ID: 31
- 레벨: 2
- 페이지: 93-96
- 페이지 수: 4
- 부모 ID: 25
- 텍스트 길이: 7032 문자

---

cords of different types 65
3.5 Handling records of different types
We’ve seen how DOP enables us to treat records as first-class citizens that can be
manipulated in a flexible way using generic functions. But if a record is nothing more
than an aggregation of fields, how do we know what the type of the record is? DOP has
a surprising answer to this question.
Theo I have a question. If a record is nothing more than a map, how do you know
the type of the record?
Joe That’s a great question with a surprising answer.
Theo I’m curious.
Joe Most of the time, there’s no need to know the record type.
Theo What! What do you mean?
Joe I mean that what matters most are the values of the fields. For example, take a
look at the Catalog.authorNames source code. It operates on a Book record,
but the only thing that matters is the value of the authorIds field.
Doubtful, Theo looks at the source code for Catalog.authorNames. This is what Theo sees.
Listing3.25 Calculating the author names of a book
function authorNames(catalogData, book) {
var authorIds = _.get(book, "authorIds");
var names = _.map(authorIds, function(authorId) {
return _.get(catalogData, ["authorsById", authorId, "name"]);
});
return names;
}
Theo What about differentiating between various user types like Member versus
Librarian? I mean, they both have email and encryptedPassword. How do
you know if a record represents a Member or a Librarian?
Joe Simple. You check to see if the record is found in the librariansByEmail
index or in the membersByEmail index of the Catalog.
Theo Could you be more specific?
Joe Sure! Let me write what the user management data of our tiny library might
look like, assuming we have one librarian and one member. To keep things
simple, I’m encrypting passwords through naive base-64 encoding for the User-
Management record.
Listing3.26 A UserManagement record
var userManagementData = {
"librariansByEmail": {
"franck@gmail.com" : { The base-64
encoding of
"email": "franck@gmail.com",
"mypassword"
"encryptedPassword": "bXlwYXNzd29yZA=="
}
},

66 CHAPTER 3 Basic data manipulation
"membersByEmail": {
"samantha@gmail.com": {
"email": "samantha@gmail.com",
"encryptedPassword": "c2VjcmV0",
The base-64
"isBlocked": false,
encoding of
"bookLendings": [
"secret"
{
"bookItemId": "book-item-1",
"bookIsbn": "978-1779501127",
"lendingDate": "2020-04-23"
}
]
}
}
}
TIP Most of the time, there’s no need to know the record type.
Theo This morning, you told me you’d show me the code for UserManagement
.isLibrarian function this afternoon.
Joe So, here we are. It’s afternoon, and I’m going to fulfill my promise.
Joe implements isLibrarian. With a slight pause, he then issues the test for isLibrarian.
Listing3.27 Checking if a user is a librarian
function isLibrarian(userManagement, email) {
return _.has(_.get(userManagement, "librariansByEmail"), email);
}
Listing3.28 Testing isLibrarian
isLibrarian(userManagementData, "franck@gmail.com");
// → true
Theo I’m assuming that _.has is a function that checks whether a key exists in a
map. Right?
Joe Correct.
Theo OK. You simply check whether the librariansByEmail map contains the
email field.
Joe Yep.
Theo Would you use the same pattern to check whether a member is a Super mem-
ber or a VIP member?
Joe Sure. We could have SuperMembersByEmail and VIPMembersByEmail indexes.
But there’s a better way.
Theo How?
Joe When a member is a VIP member, we add a field, isVIP, with the value true to
its record. To check if a member is a VIP member, we check whether the
isVIP field is set to true in the member record. Here’s how I would code
isVIPMember.

3.5 Handling records of different types 67
Listing3.29 Checking whether a member is a VIP member
function isVIPMember(userManagement, email) {
return _.get(userManagement, ["membersByEmail", email, "isVIP"]) == true;
}
Theo I see that you access the isVIP field via its information path, ["membersBy-
Email", email, "isVIP"].
Joe Yes, I think it makes the code crystal clear.
Theo I agree. I guess we can do the same for isSuperMember and set an isSuper
field to true when a member is a Super member?
Joe Yes, just like this.
Joe assembles all the pieces in a UserManagement class. He then shows the code to Theo.
Listing3.30 The code of UserManagement module
class UserManagement {
isLibrarian(userManagement, email) {
return _.has(_.get(userManagement, "librariansByEmail"), email);
}
isVIPMember(userManagement, email) {
return _.get(userManagement,
["membersByEmail", email, "isVIP"]) == true;
}
isSuperMember(userManagement, email) {
return _.get(userManagement,
["membersByEmail", email, "isSuper"]) == true;
}
}
Theo looks at the UserManagement module code for a couple of seconds. Suddenly, an
idea comes to his mind.
Theo Why not have a type field in member record whose value would be either VIP
or Super?
Joe I assume that, according to the product requirements, a member can be both a
VIP and a Super member.
Theo Hmm...then the types field could be a collection containing VIP or Super
or both.
Joe In some situations, having a types field is helpful, but I find it simpler to have
a Boolean field for each feature that the record supports.
Theo Is there a name for fields like isVIP and isSuper?
Joe I call them feature fields.
TIP Instead of maintaining type information about a record, use a feature field (e.g.,
isVIP).

68 CHAPTER 3 Basic data manipulation
Theo Can we use feature fields to differentiate between librarians and members?
Joe You mean having an isLibrarian and an isMember field?
Theo Yes, and having a common User record type for both librarians and members.
Joe We can, but I think it’s simpler to have different record types for librarians and
members: Librarian for librarians and Member for members.
Theo Why?
Joe Because there’s a clear distinction between librarians and members in terms of
data. For example, members can have book lendings but librarians don’t.
Theo I agree. Now, we need to mention the two Member feature fields in our entity
diagram.
With that, Theo adds these fields to his diagram on the whiteboard. When he’s finished, he
shows Joe his additions (figure 3.6).
CC Library
name: String
address: String
catalog: Catalog
userManagement: Catalog
CC Catalog CC UserManagement
booksByIsbn: {Book} librariansByEmail: {Librarian}
authorsById: {Author} membersByEmail: {Member}
*
*
* CC Author CC Librarian *
CC Book id: String email: String CC Member
name: String
title : String encryptedPassword: String email: String
bookIsbns: [String]
publicationYear: Number encryptedPassword: String
isbn: String * isBlocked: Boolean
authorIds: [String] bookLendings: [BookLending]
bookItems: [BookItem] * isVIP: Boolean
isSuper: Boolean
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
Figure 3.6 A library management data model with the Member feature fields isVIP and isSuper
Joe Do you like the data model that we have designed together?
Theo I find it quite simple and clear.