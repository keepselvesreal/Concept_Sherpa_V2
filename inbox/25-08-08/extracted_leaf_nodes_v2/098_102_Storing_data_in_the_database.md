# 10.2 Storing data in the database

**메타데이터:**
- ID: 98
- 레벨: 2
- 페이지: 232-234
- 페이지 수: 3
- 부모 ID: 95
- 텍스트 길이: 4068 문자

---

a in the database
In the previous section, we saw how to retrieve data from the database as a list of maps.
Next, we’ll see how to store data in the database when data is represented with a map.
Theo I guess that storing data in the database is quite similar to fetching data from
the database.
Joe It’s similar in the sense that we deal only with generic data collections. Can you
write a parameterized SQL query that inserts a row with user info using only
email and encrypted_password, please?
Theo OK.

10.2 Storing data in the database 205
Theo takes a moment to think about the code and writes a few lines of SQL as Joe
requested. He shows it to Joe.
Listing10.7 SQL statement to add a member
INSERT
INTO members
(email, encrypted_password)
VALUES ($1, $2)
Joe Great! And here’s how to integrate your SQL query in our application code.
Listing10.8 Adding a member from inside the application
var addMemberQuery =
"INSERT INTO members (email, password) VALUES ($1, $2)";
dbClient.query(addMemberQuery,
Passes the two parameters to
[_.get(member, "email"),
the SQL query as an array
_.get(member, "encryptedPassword")]);
Theo Your code is very clear, but something still bothers me.
Joe What is that?
Theo I find it cumbersome that you use _.get(user, "email") instead of user
.email, like I would if the data were represented with a class.
Joe In JavaScript, you are allowed to use the dot notation user.email instead of
_.get(user, "email").
Theo Then why don’t you use the dot notation?
Joe Because I wanted to show you how you can apply DOP principles even in lan-
guages like Java, where the dot notation is not available for hash maps.
 NOTE In this book, we avoid using the JavaScript dot notation to access a field in a
hash map in order to illustrate how to apply DOP in languages that don’t support dot
notation on hash maps.
Theo That’s exactly my point. I find it cumbersome in a language like Java to use
_.get(user, "email") instead of user.email like I would if the data were
represented with a class.
Joe On one hand, it’s cumbersome. On the other hand, representing data with a
hash map instead of a static class allows you to access fields in a flexible way.
Theo I know—you’ve told me so many times! But I can’t get used to it.
Joe Let me give you another example of the benefits of the flexible access to data
fields in the context of adding a member to the database. You said that writing
[_.get(member, "email"), _.get(member, "encryptedPassword")] was
less convenient than writing [member.email, member.encryptedPassword].
Right?
Theo Absolutely!
Joe Let me show you how to write the same code in a more succinct way, using a
function from Lodash called _.at.

206 CHAPTER 10 Database operations
Theo What does this _.at function do?
Joe It receives a map m, a list keyList, and returns a list made of the values in m
associated with the keys in keyList.
Theo How about an example?
Joe Sure. We create a list made of the fields email and encryptedPassword of a
member.
Joe types for a bit. He shows this code to Theo.
Listing10.9 Creating a list made of some values in a map with _.at
var member = {
"email": "samantha@gmail.com",
"encryptedPassword": "c2VjcmV0",
"isBlocked": false
};
_.at(member,
["email", "encryptedPassword"]);
// ? ["samantha@gmail.com", "c2VjcmV0"]
Theo Do the values in the results appear in the same order as the keys in keyList?
Joe Yes!
Theo That’s cool.
TIP Accessing a field in a hash map is more flexible than accessing a member in an
object instantiated from a class.
Joe And here’s the code for adding a member using _.at.
Listing10.10 Using _.at to return multiple values from a map
class CatalogDB {
static addMember(member) {
var addMemberQuery = `INSERT
INTO members
(email, encrypted_password)
VALUES ($1, $2)`;
dbClient.query(addMemberQuery,
_.at(member, ["email",
"encryptedPassword"]));
}
}
Theo I can see how the _.at function becomes really beneficial when we need to
pass a bigger number of field values.
Joe I’ll be showing you more examples that use the flexible data access that we
have in DOP.