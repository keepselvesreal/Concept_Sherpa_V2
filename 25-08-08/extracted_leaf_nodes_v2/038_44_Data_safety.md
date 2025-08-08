# 4.4 Data safety

**메타데이터:**
- ID: 38
- 레벨: 2
- 페이지: 110-110
- 페이지 수: 1
- 부모 ID: 33
- 텍스트 길이: 1965 문자

---

Joe is about to start the day’s lesson. Theo asks him a question about yesterday’s material
instead.
Theo Something isn’t clear to me regarding this structural sharing stuff. What hap-
pens if we write code that modifies the data part that’s shared between the two
versions of the data? Does the change affect both versions?
Joe Could you please write a code snippet that illustrates your question?
Theo starts typing on his laptop. He comes up with this code to illustrate modifying a piece
of data shared between two versions.
Listing4.5 Modifying data that’s shared between two versions
var books = {
"978-1779501127": {
"isbn": "978-1779501127",
"title": "Watchmen",
"publicationYear": 1987,
"authorIds": ["alan-moore",
"dave-gibbons"]
}
};
var nextBooks = _.set(books, ["978-1779501127", "publicationYear"], 1986)
console.log("Before:", nextBooks["978-1779501127"]["authorIds"][1]);
books["978-1779501127"]["authorIds"][1] = "dave-chester-gibbons";
console.log("After:", nextBooks["978-1779501127"]["authorIds"][1]);
// → Before: dave-gibbons
// → After: dave-chester-gibbons
Theo My question is, what is the value of isBlocked in updatedMember?
Joe The answer is that mutating data via the native hash map setter is forbidden.
All the data manipulation must be done via immutable functions.
 NOTE All data manipulation must be done with immutable functions. It is forbid-
den to use the native hash map setter.
Theo When you say “forbidden,” you mean that it’s up to the developer to make sure
it doesn’t happen. Right?
Joe Exactly.
Theo Is there a way to protect our system from a developer’s mistake?
Joe Yes, there is a way to ensure the immutability of the data at the level of the data
structure. It’s called persistent data structures.
Theo Are persistent data structures also efficient in terms of memory and computation?
Joe Actually, the way data is organized inside persistent data structures make them
even more efficient than immutable functions.