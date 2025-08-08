# 4.6 Ensuring system state integrity

**메타데이터:**
- ID: 40
- 레벨: 2
- 페이지: 113-113
- 페이지 수: 1
- 부모 ID: 33
- 텍스트 길이: 3081 문자

---

tem state integrity 85
var next = Library.addMember(previous, member);
SystemState.commit(previous, next);
SystemState is covered
}
in listing 4.8.
}
Theo What does SystemState look like?
Joe I had a feeling you were going to ask that. Here’s the code for the System-
State class, which is a stateful class!
Listing4.8 The SystemState class
class SystemState {
systemState;
get() {
return this.systemState;
}
commit(previous, next) {
this.systemState = next;
}
}
Theo I don’t get the point of SystemState. It’s a simple class with a getter and a
commit function, right?
Joe In a moment, we are going to enrich the code of the SystemState.commit
method so that it provides data validation and history tracking. For now, the
important thing to notice is that the code of the calculation phase is stateless
and is decoupled from the code of the commit phase, which is stateful.
TIP The calculation phase is stateless. The commit phase is stateful.
4.6 Ensuring system state integrity
Theo Something still bothers me about the way functions manipulate immutable
data in the calculation phase. How do we preserve data integrity?
Joe What do you mean?
Theo In OOP, data is manipulated only by methods that belong to the same class as
the data. It prevents other classes from corrupting the inner state of the class.
Joe Could you give me an example of an invalid state of the library?
Theo For example, imagine that the code of a mutation adds a book item to the
book lendings of a member without marking the book item as lent in the cata-
log. Then the system data would be corrupted.
Joe In DOP, we have the privilege of ensuring data integrity at the level of the
whole system instead of scattering the validation among many classes.
Theo How does that work?
Joe The fact that the code for the commit phase is common to all the mutations
allows us to validate the system data in a central place. At the beginning of the
commit phase, there is a step that checks whether the version of the system

86 CHAPTER 4 State management
state to be committed is valid. If the data is invalid, the commit is rejected.
Here let me show you.
Listing4.9 Data validation inside the commit phase
SystemState.commit = function(previous, next) {
if(!SystemValidity.validate(previous, next)) { // not implemented for now
throw "The system data to be committed is not valid!";
};
this.systemData = next;
};
Theo It sounds similar to a commit hook in Git.
Joe I like your analogy!
Theo Why are you passing the previous state in previous and the next state in next
to SystemValidity.validate?
Joe Because it allows SystemValidity.validate to optimize the validation in
terms of computation. For example, we could validate just the data that has
changed.
TIP In DOP, we validate the system data as a whole. Data validation is decoupled
from data manipulation.
Theo What does the code of SystemValidity.validate look like?
Joe Someday, I will show you how to define a data schema and to validate that a
piece of data conforms to a schema.
 NOTE See chapters 7 and 12 to see how Joe defines this data schema.