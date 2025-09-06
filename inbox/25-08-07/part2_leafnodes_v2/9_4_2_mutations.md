# 9.4.2 Writing mutations with persistent data structures

9.4.2 Writing mutations with persistent data structures
Theo Shall we move forward and port the add member mutation?
Joe Sure. Porting the add member mutation from Lodash to Immutable.js only
requires you to again replace the underscore (_) with Immutable. Let’s look at
some code.
Listing9.15 Implementing member addition with persistent data structures
UserManagement.addMember = function(userManagement, member) {
var email = Immutable.get(member, "email");
var infoPath = ["membersByEmail", email];
if(Immutable.hasIn(userManagement, infoPath)) {
throw "Member already exists.";
}
var nextUserManagement = Immutable.setIn(userManagement,
infoPath,
member);
return nextUserManagement;
};
Theo So, for the tests, I’d convert the JavaScript objects to Immutable.js objects with
Immutable.fromJS(). How does this look?
Listing9.16 Testing member addition with persistent data structures
var jessie = Immutable.fromJS({
"email": "jessie@gmail.com",
"password": "my-secret"
});
var franck = Immutable.fromJS({
"email": "franck@gmail.com",
"password": "my-top-secret"
});
var userManagementStateBefore = Immutable.fromJS({
"membersByEmail": {
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
});
var expectedUserManagementStateAfter = Immutable.fromJS({
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"

## 페이지 220

192 CHAPTER 9 Persistent data structures
}
}
});
var result = UserManagement.addMember(userManagementStateBefore, jessie);
Immutable.isEqual(result, expectedUserManagementStateAfter);
// → true
Joe Great!