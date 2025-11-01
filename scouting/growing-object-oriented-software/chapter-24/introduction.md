Line1 # Introduction (pp.273-274)
Line2 
Line3 ---
Line4 **Page 273**
Line5 
Line6 Chapter 24
Line7 Test Flexibility
Line8 Living plants are flexible and tender;
Line9 the dead are brittle and dry.
Line10 […]
Line11 The rigid and stiff will be broken.
Line12 The soft and yielding will overcome.
Line13 —Lao Tzu (c.604—531 B.C.)
Line14 Introduction
Line15 As the system and its associated test suite grows, maintaining the tests can become
Line16 a burden if they have not been written carefully. We’ve described how we can
Line17 reduce the ongoing cost of tests by making them easy to read and generating
Line18 helpful diagnostics on failure. We also want to make sure that each test fails
Line19 only when its relevant code is broken. Otherwise, we end up with brittle
Line20 tests that slow down development and inhibit refactoring. Common causes of test
Line21 brittleness include:
Line22 •
Line23 The tests are too tightly coupled to unrelated parts of the system or unrelated
Line24 behavior of the object(s) they’re testing;
Line25 •
Line26 The tests overspecify the expected behavior of the target code, constraining
Line27 it more than necessary; and,
Line28 •
Line29 There is duplication when multiple tests exercise the same production code
Line30 behavior.
Line31 Test brittleness is not just an attribute of how the tests are written; it’s also
Line32 related to the design of the system. If an object is difﬁcult to decouple from its
Line33 environment because it has many dependencies or its dependencies are hidden,
Line34 its tests will fail when distant parts of the system change. It will be hard to judge
Line35 the knock-on effects of altering the code. So, we can use test brittleness as a
Line36 valuable source of feedback about design quality.
Line37 There’s a virtuous relationship with test readability and resilience. A test that
Line38 is focused, has clean set-up, and has minimal duplication is easier to name and is
Line39 more obvious about its purpose. This chapter expands on some of the techniques
Line40 we discussed in Chapter 21. Actually, the whole chapter can be collapsed into a
Line41 single rule:
Line42 273
Line43 
Line44 
Line45 ---
Line46 
Line47 ---
Line48 **Page 274**
Line49 
Line50 Specify Precisely What Should Happen and No More
Line51 JUnit, Hamcrest, and jMock allow us to specify just what we want from the
Line52 target code (there are equivalents in other languages). The more precise we are,
Line53 the more the code can ﬂex in other unrelated dimensions without breaking tests
Line54 misleadingly. Our experience is that the other beneﬁt of keeping tests ﬂexible is
Line55 that they’re easier for us to understand because they are clearer about what they’re
Line56 testing—about what is and is not important in the tested code.
Line57 Test for Information, Not Representation
Line58 A test might need to pass a value to trigger the behavior it’s supposed to exercise
Line59 in its target object. The value could either be passed in as a parameter to a method
Line60 on the object, or returned as a result from a query the object makes on one of
Line61 its neighbors stubbed by the test. If the test is structured in terms of how the
Line62 value is represented by other parts of the system, then it has a dependency on
Line63 those parts and will break when they change.
Line64 For example, imagine we have a system that uses a CustomerBase to store and
Line65 ﬁnd information about our customers. One of its features is to look up a Customer
Line66 given an email address; it returns null if there’s no customer with the given
Line67 address.
Line68 public interface CustomerBase {
Line69 // Returns null if no customer found
Line70   Customer findCustomerWithEmailAddress(String emailAddress);
Line71 […]
Line72 }
Line73 When we test the parts of the code that search for customers by email address,
Line74 we stub CustomerBase as a collaborating object. In some of those tests, no
Line75 customer will be found so we return null:
Line76 allowing(customerBase).findCustomerWithEmailAddress(theAddress);
Line77                                         will(returnValue(null));
Line78 There are two problems with this use of null in a test. First, we have to remember
Line79 what null means here, and when it’s appropriate; the test is not self-explanatory.
Line80 The second concern is the cost of maintenance.
Line81 Some time later, we experience a NullPointerException in production and
Line82 track the source of the null reference down to the CustomerBase. We realize we’ve
Line83 broken one of our design rules: “Never Pass Null between Objects.” Ashamed,
Line84 we change the CustomerBase’s search methods to return a Maybe type, which im-
Line85 plements an iterable collection of at most one result.
Line86 Chapter 24
Line87 Test Flexibility
Line88 274
Line89 
Line90 
Line91 ---
