Line1 # Test for Information, Not Representation (pp.274-275)
Line2 
Line3 ---
Line4 **Page 274**
Line5 
Line6 Specify Precisely What Should Happen and No More
Line7 JUnit, Hamcrest, and jMock allow us to specify just what we want from the
Line8 target code (there are equivalents in other languages). The more precise we are,
Line9 the more the code can ﬂex in other unrelated dimensions without breaking tests
Line10 misleadingly. Our experience is that the other beneﬁt of keeping tests ﬂexible is
Line11 that they’re easier for us to understand because they are clearer about what they’re
Line12 testing—about what is and is not important in the tested code.
Line13 Test for Information, Not Representation
Line14 A test might need to pass a value to trigger the behavior it’s supposed to exercise
Line15 in its target object. The value could either be passed in as a parameter to a method
Line16 on the object, or returned as a result from a query the object makes on one of
Line17 its neighbors stubbed by the test. If the test is structured in terms of how the
Line18 value is represented by other parts of the system, then it has a dependency on
Line19 those parts and will break when they change.
Line20 For example, imagine we have a system that uses a CustomerBase to store and
Line21 ﬁnd information about our customers. One of its features is to look up a Customer
Line22 given an email address; it returns null if there’s no customer with the given
Line23 address.
Line24 public interface CustomerBase {
Line25 // Returns null if no customer found
Line26   Customer findCustomerWithEmailAddress(String emailAddress);
Line27 […]
Line28 }
Line29 When we test the parts of the code that search for customers by email address,
Line30 we stub CustomerBase as a collaborating object. In some of those tests, no
Line31 customer will be found so we return null:
Line32 allowing(customerBase).findCustomerWithEmailAddress(theAddress);
Line33                                         will(returnValue(null));
Line34 There are two problems with this use of null in a test. First, we have to remember
Line35 what null means here, and when it’s appropriate; the test is not self-explanatory.
Line36 The second concern is the cost of maintenance.
Line37 Some time later, we experience a NullPointerException in production and
Line38 track the source of the null reference down to the CustomerBase. We realize we’ve
Line39 broken one of our design rules: “Never Pass Null between Objects.” Ashamed,
Line40 we change the CustomerBase’s search methods to return a Maybe type, which im-
Line41 plements an iterable collection of at most one result.
Line42 Chapter 24
Line43 Test Flexibility
Line44 274
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 275**
Line51 
Line52 public interface CustomerBase {
Line53 Maybe<Customer> findCustomerWithEmailAddress(String emailAddress);
Line54 }
Line55 public abstract class Maybe<T> implements Iterable<T> {
Line56   abstract boolean hasResult();
Line57   public static Maybe<T> just(T oneValue) { …
Line58   public static Maybe<T> nothing() { …
Line59 }
Line60 We still, however, have the tests that stub CustomerBase to return null, to
Line61 represent missing customers. The compiler cannot warn us of the mismatch be-
Line62 cause null is a valid value of type Maybe<Customer> too, so the best we can do
Line63 is to watch all these tests fail and change each one to the new design.
Line64 If, instead, we’d given the tests their own representation of “no customer
Line65 found” as a single well-named constant instead of the literal null, we could have
Line66 avoided this drudgery. We would have changed one line:
Line67 public static final Customer NO_CUSTOMER_FOUND = null;
Line68 to
Line69 public static final Maybe<Customer> NO_CUSTOMER_FOUND = Maybe.nothing();
Line70 without changing the tests themselves.
Line71 Tests should be written in terms of the information passed between objects,
Line72 not of how that information is represented. Doing so will both make the tests
Line73 more self-explanatory and shield them from changes in implementation controlled
Line74 elsewhere in the system. Signiﬁcant values, like NO_CUSTOMER_FOUND, should be
Line75 deﬁned in one place as a constant. There’s another example in Chapter 12 when
Line76 we introduce UNUSED_CHAT. For more complex structures, we can hide the details
Line77 of the representation in test data builders (Chapter 22).
Line78 Precise Assertions
Line79 In a test, focus the assertions on just what’s relevant to the scenario being tested.
Line80 Avoid asserting values that aren’t driven by the test inputs, and avoid reasserting
Line81 behavior that is covered in other tests.
Line82 We ﬁnd that these heuristics guide us towards writing tests where each method
Line83 exercises a unique aspect of the target code’s behavior. This makes the tests more
Line84 robust because they’re not dependent on unrelated results, and there’s less
Line85 duplication.
Line86 Most test assertions are simple checks for equality; for example, we assert the
Line87 number of rows in a table model in “Extending the Table Model” (page 180).
Line88 Testing for equality doesn’t scale well as the value being returned becomes more
Line89 275
Line90 Precise Assertions
Line91 
Line92 
Line93 ---
