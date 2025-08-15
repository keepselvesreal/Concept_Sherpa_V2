# 6.4 Unit tests for mutations

**ID**: 60  
**Level**: 2  
**추출 시간**: 2025-08-09 10:09:52 KST

---

6.4 Unit tests for mutations
Joe Before writing unit tests for the add member mutation, let’s draw the tree of
function calls for System.addMember.
Theo I can do that.
Theo takes a look at the code for the functions involved in the add member mutation. He
notices the code is spread over three classes: System, Library, and UserManagement.
Listing6.21 The functions involved in the add member mutation
System.addMember = function(systemState, member) {
var previous = systemState.get();
var next = Library.addMember(previous, member);
systemState.commit(previous, next);
};
Library.addMember = function(library, member) {
var currentUserManagement = _.get(library, "userManagement");
var nextUserManagement = UserManagement.addMember(
currentUserManagement, member);
var nextLibrary = _.set(library, "userManagement", nextUserManagement);
return nextLibrary;
};
UserManagement.addMember = function(userManagement, member) {
var email = _.get(member, "email");
var infoPath = ["membersByEmail", email];
if(_.has(userManagement, infoPath)) {
throw "Member already exists.";
}
var nextUserManagement = _.set(userManagement,
infoPath,
member);
return nextUserManagement;
};
Theo grabs another napkin. Drawing the tree of function calls for System.addMember is
now quite easy (see figure 6.5).
System.addMember
SystemState.get SystemState.commit Library.addMember
_.get _.set UserManagement.addMember
_.has _.set
Figure 6.5 The tree of function calls for System.addMember

## 페이지 155

6.4 Unit tests for mutations 127
Joe Excellent! So which functions of the tree should be unit tested for the add
member mutation?
Theo I think the functions we need to test are System.addMember, SystemState
.get, SystemState.commit, Library.addMember, and UserManagement
.addMember. That right?
Joe You’re totally right. Let’s defer writing unit tests for functions that belong to
SystemState until later. Those are generic functions that should be tested
outside the context of a specific mutation. Let’s assume for now that we’ve
already written unit tests for the SystemState class. We’re left with three func-
tions: System.addMember, Library.addMember, and UserManagement.add-
Member.
Theo In what order should we write the unit tests, bottom up or top down?
Joe Let’s start where the real meat is—in UserManagement.addMember. The two
other functions are just wrappers.
Theo OK.
Joe Writing a unit test for the main function of a mutation requires more effort
than writing the test for a query. The reason is that a query returns a response
based on the system data, whereas a mutation computes a new state of the system
based on the current state of the system and some arguments (see figure 6.6).
SystemData Argument Argument SystemData
Mutation Query
NextSystemData ResponseData
Figure 6.6 The output of a mutation is more complex than
the output of a query.
TIP Writing a unit test for the main function of a mutation requires more effort than
for a query.
Theo It means that in the test cases of UserManagement.addMember, both the input
and the expected output are maps that describe the state of the system.
Joe Exactly. Let’s start with the simplest case, where the initial state of the system
is empty.
Theo You mean that userManagementData passed to UserManagement.addMember
is an empty map?
Joe Yes.
Once again, Theo places his hands over his laptop keyboard, thinks for a moment, and
begins typing. He reminds himself that the code needs to add a member to an empty user

## 페이지 156

128 CHAPTER 6 Unit tests
management map and to check that the resulting map is as expected. When he’s finished,
he shows his code to Joe.
Listing6.22 Test case for Catalog.addMember without members
var member = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var userManagementStateBefore = {};
var expectedUserManagementStateAfter = {
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
}
}
};
var result = UserManagement.addMember(userManagementStateBefore, member);
_.isEqual(result, expectedUserManagementStateAfter);
Joe Very nice! Keep going and write a test case when the initial state is not empty.
Theo knows this requires a few more lines of code but nothing complicated. When he fin-
ishes, he once again shows the code to Joe.
Listing6.23 Test case for Catalog.addMember with existing members
var jessie = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var franck = {
"email": "franck@gmail.com",
"password": "my-top-secret"
};
var userManagementStateBefore = {
"membersByEmail": {
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
};
var expectedUserManagementStateAfter = {
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",

## 페이지 157

6.4 Unit tests for mutations 129
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
}
}
};
var result = UserManagement.addMember(userManagementStateBefore, jessie);
_.isEqual(result, expectedUserManagementStateAfter);
Joe Awesome! Can you think of other test cases for UserManagement.addMember?
Theo No.
Joe What about cases where the mutation fails?
Theo Right! I always forget to think about negative test cases. I assume that relates to
the fact that I’m an optimistic person.
TIP Don’t forget to include negative test cases in your unit tests.
Joe Me too. The more I meditate, the more I’m able to focus on the positive side of
life. Anyway, how would you write a test case where the mutation fails?
Theo I would pass to UserManagement.addMember a member that already exists in
userManagementStateBefore.
Joe And how would you check that the code behaves as expected in case of a failure?
Theo Let me see. When a member already exists, UserManagement.addMember
throws an exception. Therefore, what I need to do in my test case is to wrap the
code in a try/catch block.
Joe Sounds good to me.
Once again, it doesn’t require too much of an effort for Theo to create a new test case.
When he’s finished, he eagerly turns his laptop to Joe.
Listing6.24 Test case for UserManagement.addMember if it’s expected to fail
var jessie = {
"email": "jessie@gmail.com",
"password": "my-secret"
};
var userManagementStateBefore = {
"membersByEmail": {
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
}
}
};

## 페이지 158

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

## 페이지 159

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

## 페이지 160

132 CHAPTER 6 Unit tests
Theo Then how do we validate that the code works as expected?
Joe We’ll retrieve the system state after the code is executed and compare it to the
expected value of the state.
Theo OK. I’ll try to write the unit test.
Joe Writing unit tests for stateful code is more complicated than for data manipula-
tion code. It requires the calm of the office.
Theo Then let’s go back to the office. Waiter! Check, please.
Theo picks up the tab, and he and Joe take the cable car back to Albatross. When they’re
back at the office, Theo starts coding the unit test for Library.addMember.
Theo Can we use _.isEqual with system state?
Joe Definitely. The system state is a map like any other map.
TIP The system state is a map. Therefore, in the context of a test case, we can com-
pare the system state after a mutation is executed to the expected system state using
_.isEqual
Theo copies and pastes the code for Library.addMember (listing 6.21), which initializes
the data for the test. Then, he passes a SystemState object that is initialized with
libraryStateBefore to System.addMember. Finally, to complete the test, he compares
the system state after the mutation is executed with the expected value of the state.
class SystemState {
systemState;
get() {
return this.systemState;
}
commit(previous, next) {
this.systemState = next;
}
}
window.SystemState = SystemState;
Listing6.27 Unit test for System.addMember
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

## 페이지 161

6.4 Unit tests for mutations 133
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
"jessie@gmail.com": {
"email": "jessie@gmail.com",
"password": "my-secret"
},
"franck@gmail.com": {
"email": "franck@gmail.com",
"password": "my-top-secret"
Creates an empty
}
SystemState object
}
(see chapter 4)
}
};
Initializes the system
state with the library
data before the
var systemState = new SystemState();
mutation
systemState.commit(null, libraryStateBefore);
System.addMember(systemState, jessie);
Executes the
mutation on the
_.isEqual(systemState.get(),
SystemState object
expectedLibraryStateAfter);
Validates the state after the
mutation is executed
Joe Wow, I’m impressed; you did it! Congratulations!
Theo Thank you. I’m so glad that in DOP most of our code deals with data manipu-
lation. It’s definitely more pleasant to write unit tests for stateless code that
only deals with data manipulation.
Joe Now that you know the basics of DOP, would you like to refactor the code of
your Klafim prototype according to DOP principles?
Theo Definitely. Nancy told me yesterday that Klafim is getting nice market traction.
I’m supposed to have a meeting with her in a week or so about the next steps.
Hopefully, she’ll be willing to work with Albatross for the long term.
Joe Exciting! Do you know what might influence Nancy’s decision?
Theo Our cost estimate, certainly, but I know she’s in touch with other software com-
panies. If we come up with a competitive proposal, I think we’ll get the deal.
Joe I’m quite sure that after refactoring to DOP, features will take much less time
to implement. That means you should be able to quote Nancy a lower total cost
than the competition, right?
Theo I’ll keep my fingers crossed!

## 페이지 162

134 CHAPTER 6 Unit tests
