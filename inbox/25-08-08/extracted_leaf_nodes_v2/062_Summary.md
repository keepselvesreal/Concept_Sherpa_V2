# Summary

**메타데이터:**
- ID: 62
- 레벨: 2
- 페이지: 162-164
- 페이지 수: 3
- 부모 ID: 51
- 텍스트 길이: 2475 문자

---

f the code in a data-oriented system deals with data manipulation.
 It’s straightforward to write unit tests for code that deals with data manipulation.
 Test cases follow the same simple general pattern:
a Generate data input
b Generate expected data output
c Compare the output of the function with the expected data output
 In order to compare the output of a function with the expected data output, we
need to recursively compare the two pieces of data.
 The recursive comparison of two pieces of data is implemented via a generic
function.
 When a function returns a JSON string, we parse the string back to data so that
we deal with data comparison instead of string comparison.
 A tree of function calls for a function f is a tree where the root is f, and the chil-
dren of a node g in the tree are the functions called by g.
 The leaves of the tree are functions that are not part of the code base of the
application and are functions that don’t call any other functions.
 The tree of function calls visualization guides us regarding the quality and
quantity of the test cases in a unit test.

Summary 135
 Functions that appear in a lower level in the tree of function calls tend to involve
less complex data than functions that appear in a higher level in the tree.
 Functions that appear in a lower level in the tree of function calls usually need
to be covered with more test cases than functions that appear in a higher level
in the tree.
 Unit tests for mutations focus on the calculation phase of the mutation.
 The validity of the data depends on the context.
 The smaller the data, the easier it is to manipulate.
 We compare the output and the expected output of our functions with a generic
function that recursively compares two pieces of data (e.g., _.isEqual).
 When we write a unit test for a function, we assume that the functions called by
this function are covered by the unit tests and work as expected. This signifi-
cantly reduces the quantity of test cases in our unit tests.
 We avoid using string comparison in unit tests for functions that deal with data.
 Writing a unit test for the main function of a mutation requires more effort
than for a query.
 Remember to include negative test cases in your unit tests.
 The system state is a map. Therefore, in the context of a test case, we can com-
pare the system state after a mutation is executed to the expected system state
using a generic function like _.isEqual.

Part 2