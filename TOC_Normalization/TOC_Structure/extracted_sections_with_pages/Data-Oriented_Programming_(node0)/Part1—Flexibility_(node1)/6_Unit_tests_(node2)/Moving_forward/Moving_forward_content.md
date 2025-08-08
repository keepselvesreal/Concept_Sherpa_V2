# Moving forward

**페이지**: 158-159
**계층**: Data-Oriented Programming (node0) > Part1—Flexibility (node1) > 6 Unit tests (node2)
**추출 시간**: 2025-08-06 19:46:58

---


--- 페이지 158 ---

130 CHAPTER 6 Unit tests
var expectedException = "Member already exists.";
var exceptionInMutation;
try {
UserManagement.addMember(userManagementStateBefore, jessie);
} catch (e) {
exceptionInMutation = e;
}
_.isEqual(exceptionInMutation, expectedException);
Theo Now, I think I’m ready to move forward and write unit tests for Library.add-
Member and System.addMember.
Joe I agree with you. Please start with Library.addMember.
Theo Library.addMember is quite similar to UserManagement.addMember. So I
guess I’ll write similar test cases.
Joe In fact, that won’t be required. As I told you when we wrote unit tests for a
query, when you write a unit test for a function, you can assume that the func-
tions down the tree work as expected.
Theo Right. So I’ll just write the test case for existing members.
Joe Go for it!
Theo starts with a copy-and-paste of the code from the UserManagement.addMember test
case with the existing members in listing 6.23. After a few modifications, the unit test for
Library.addMember is ready.
Listing6.25 Unit test for Library.addMember
var jessie = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var franck = {
"email": "franck@gmail.com",
"password": "my-top-secret"
};
var libraryStateBefore = {
"userManagement": {
"membersByEmail": {
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
}
};
var expectedLibraryStateAfter = {
"userManagement": {
"membersByEmail": {

--- 페이지 158 끝 ---


--- 페이지 159 ---

6.4 Unit tests for mutations 131
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
}
};
var result = Library.addMember(libraryStateBefore, jessie);
_.isEqual(result, expectedLibraryStateAfter);
Joe Beautiful! Now, we’re ready for the last piece. Write a unit test for System
.addMember. Before you start, could you please describe the input and the out-
put of System.addMember?
Theo takes another look at the code for System.addMember and hesitates; he’s a bit con-
fused. The function doesn’t seem to return anything!
Listing6.26 The code of System.addMember
System.addMember = function(systemState, member) {
var previous = systemState.get();
var next = Library.addMember(previous, member);
systemState.commit(previous, next);
};
Theo The input of System.addMember is a system state instance and a member. But,
I’m not sure what the output of System.addMember is.
Joe In fact, System.addMember doesn’t have any output. It belongs to this stateful
part of our code that doesn’t deal with data manipulation. Although DOP
allows us to reduce the size of the stateful part of our code, it still exists. Here is
how I visualize it.
Joe calls the waiter to see if he can get more napkins. With that problem resolved, he draws
the diagram in figure 6.7.
SystemData Member
Mutation Change system state
Figure 6.7 System.addMember
doesn’t return data—it changes the
Nothing system state!

--- 페이지 159 끝 ---
