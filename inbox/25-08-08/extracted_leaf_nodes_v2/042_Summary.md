# Summary

**메타데이터:**
- ID: 42
- 레벨: 2
- 페이지: 117-118
- 페이지 수: 2
- 부모 ID: 33
- 텍스트 길이: 2512 문자

---

I see that implementing System.undoLastMutation is simply a matter of hav-
ing systemData refer the same value as previousSystemData.
Joe As I told you, if we need to allow multiple undos, the code would be a bit more
complicated, but you get the idea.
Theo I think so. Although Back to the Future belongs to the realm of science fiction, in
DOP, time travel is real.
Summary
 DOP principle #3 states that data is immutable.
 A mutation is an operation that changes the state of the system.
 In a multi-version approach to state management, mutations are split into cal-
culation and commit phases.
 All data manipulation must be done via immutable functions. It is forbidden to
use the native hash map setter.
 Structural sharing allows us to create new versions of data efficiently (in terms of
memory and computation), where data that is common between the two ver-
sions is shared instead of being copied.
 Structural sharing creates a new version of the data by recursively sharing the
parts that don’t need to change.
 A mutation is split in two phases: calculation and commit.
 A function is said to be immutable when, instead of mutating the data, it creates
a new version of the data without changing the data it receives.
 During the calculation phase, data is manipulated with immutable functions that
use structural sharing.
 The calculation phase is stateless.
 During the commit phase, we update the system state.
 The responsibility of the commit phase is to move the system state forward to
the version of the state returned by the calculation phase.
 The data is immutable, but the state reference is mutable.
 The commit phase is stateful.
 We validate the system data as a whole. Data validation is decoupled from data
manipulation.
 The fact that the code for the commit phase is common to all the mutations
allows us to validate the system state in a central place before we update the
state.
 Keeping the history of the versions of the system data is memory efficient due to
structural sharing.
 Restoring the system to one of its previous states is straightforward due to the
clear separation between the calculation phase and the commit phase.

90 CHAPTER 4 State management
 In order to use Lodash immutable functions, we use the Lodash FP module
(https://github.com/lodash/lodash/wiki/FP-Guide).
Lodash functions introduced in this chapter
Function Description
set(map, path, value) Creates a map with the same fields as map with the addition of a
<path, value> field