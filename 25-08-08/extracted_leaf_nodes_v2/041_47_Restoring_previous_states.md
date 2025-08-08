# 4.7 Restoring previous states

**메타데이터:**
- ID: 41
- 레벨: 2
- 페이지: 114-116
- 페이지 수: 3
- 부모 ID: 33
- 텍스트 길이: 4080 문자

---

evious states
Another advantage of the multi-version state approach with immutable data that is
manipulated via structural sharing is that we can keep track of the history of all the
versions of the data without exploding the memory of our program. It allows us, for
instance, to restore the system back to an earlier state easily.
Theo You told me earlier that it was easy to restore the system to a previous state.
Could you show me how?
Joe Happily, but before that, I’d like to make sure you understand why keeping
track of all the versions of the data is efficient in terms of memory.
Theo I think it’s related to the fact that immutable functions use structural sharing,
and most of the data between subsequent versions of the state is shared.
TIP Structural sharing allows us to keep many versions of the system state without
exploding memory use.
Joe Perfect! Now, I’ll show you how simple it is to undo a mutation. In order to
implement an undo mechanism, our SystemState class needs to have two

4.7 Restoring previous states 87
references to the system data: systemData references the current state of the
system, and previousSystemData references the previous state of the system.
Theo That makes sense.
Joe In the commit phase, we update both previousSystemData and systemData.
Theo What does it take to implement an undo mechanism?
Joe The undo is achieved by having systemData reference the same version of the
system data as previousSystemData.
Theo Could you walk me through an example?
Joe To make things simple, I am going to give a number to each version of the sys-
tem state. It starts at V0, and each time a mutation is committed, the version is
incremented: V1, V2, V3, and so forth.
Theo OK.
Joe Let’s say that currently our system state is at V12 (see figure 4.8). In the
SystemState object, systemData refers to V12, and previousSystemData
refers to V11.
previousSystemData
MutationA Mutation B
Data V10 Data V11 Data V12
systemData
Figure 4.8 When the system state is at V12, systemData refers to V12, and
previousSystemData refers to V11.
Theo So far, so good...
Joe Now, when a mutation is committed (for instance, adding a member), both
references move forward: systemData refers to V13, and previousSystem-
Data refers to V12.
Joe erases the whiteboard to make room for another diagram (figure 4.9). When he’s
through with his drawing, he shows it to Theo.
previousSystemData
MutationA Mutation B Mutation C
Data V10 Data V11 Data V12 Data V13
systemData
Figure 4.9 When a mutation is committed, systemData refers to V13, and
previousSystemData refers to V12.

88 CHAPTER 4 State management
Theo I suppose that when we undo the mutation, both references move backward.
Joe In theory, yes, but in practice, it’s necessary to maintain a stack of all the state
references. For now, to simplify things, we’ll maintain only a reference to the
previous version. As a consequence, when we undo the mutation, both refer-
ences refer to V12. Let me draw another diagram on the whiteboard that shows
this state (see figure 4.10).
previousSystemData
MutationA Mutation B Mutation C
Data V10 Data V11 Data V12 Data V13
systemData
Figure 4.10 When a mutation is undone, both systemData and previousSystemData refer
to V12.
Theo Could you show me how to implement this undo mechanism?
Joe Actually, it takes only a couple of changes to the SystemState class. Pay atten-
tion to the changes in the commit function. Inside systemDataBeforeUpdate,
we keep a reference to the current state of the system. If the validation and
the conflict resolution succeed, we update both previousSystemData and
systemData.
Listing4.10 The SystemState class with undo capability
class SystemState {
systemData;
previousSystemData;
get() {
return this.systemData;
}
commit(previous, next) {
var systemDataBeforeUpdate = this.systemData;
if(!Consistency.validate(previous, next)) {
throw "The system data to be committed is not valid!";
}
this.systemData = next;
this.previousSystemData = systemDataBeforeUpdate;
}
undoLastMutation() {
this.systemData = this.previousSystemData;
}
}