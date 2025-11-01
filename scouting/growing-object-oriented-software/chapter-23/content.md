# Chapter 23: Test Diagnostics (pp.267-272)

---
**Page 267**

Chapter 23
Test Diagnostics
Mistakes are the portals of discovery.
—James Joyce
Design to Fail
The point of a test is not to pass but to fail. We want the production code to
pass its tests, but we also want the tests to detect and report any errors that
do exist. A “failing” test has actually succeeded at the job it was designed to do.
Even unexpected test failures, in an area unrelated to where we are working, can
be valuable because they reveal implicit relationships in the code that we hadn’t
noticed.
One situation we want to avoid, however, is when we can’t diagnose a test
failure that has happened. The last thing we should have to do is crack open the
debugger and step through the tested code to ﬁnd the point of disagreement. At
a minimum, it suggests that our tests don’t yet express our requirements clearly
enough. In the worst case, we can ﬁnd ourselves in “debug hell,” with deadlines
to meet but no idea of how long a ﬁx will take. At this point, the temptation will
be high to just delete the test—and lose our safety net.
Stay Close to Home
Synchronize frequently with the source code repository—up to every few minutes—
so that if a test fails unexpectedly it won’t cost much to revert your recent changes
and try another approach.
The other implication of this tip is not to be too inhibited about dropping code and
trying again. Sometimes it’s quicker to roll back and restart with a clear head than
to keep digging.
We’ve learned the hard way to make tests fail informatively. If a failing test
clearly explains what has failed and why, we can quickly diagnose and correct
the code. Then, we can get on with the next task.
Chapter 21 addressed the static readability of tests. This chapter describes
some practices that we ﬁnd helpful to make sure the tests give us the information
we need at runtime.
267


---
**Page 268**

Small, Focused, Well-Named Tests
The easiest way to improve diagnostics is to keep each test small and focused
and give tests readable names, as described in Chapter 21. If a test is small, its
name should tell us most of what we need to know about what has gone wrong.
Explanatory Assertion Messages
JUnit’s assertion methods all have a version in which the ﬁrst parameter is a
message to display when the assertion fails. From what we’ve seen, this feature
is not used as often as it should be to make assertion failures more helpful.
For example, when this test fails:
Customer customer  = order.getCustomer();
assertEquals("573242", customer.getAccountId());
assertEquals(16301, customer.getOutstandingBalance());
the report does not make it obvious which of the assertions has failed:
ComparisonFailure: expected:<[16301]> but was:<[16103]>
The message is describing the symptom (the balance is 16103) rather than the
cause (the outstanding balance calculation is wrong).
If we add a message to identify the value being asserted:
assertEquals("account id", "573242", customer.getAccountId());
assertEquals("outstanding balance", 16301, customer.getOustandingBalance());
we can immediately see what the point is:
ComparisonFailure: outstanding balance expected:<[16301]> but was:<[16103]>
Highlight Detail with Matchers
Developers can provide another level of diagnostic detail by using assertThat()
with Hamcrest matchers. The Matcher API includes support for describing the
value that mismatched, to help with understanding exactly what is different. For
example, the instrument strike price assertion on page 252 generates this failure
report:
Expected: a collection containing instrument at price a value greater than <81>
     but: price was <50>, price was <72>, price was <31>
which shows exactly which values are relevant.
Chapter 23
Test Diagnostics
268


---
**Page 269**

Self-Describing Value
An alternative to adding detail to the assertion is to build the detail into values
in the assertion. We can take this in the same spirit as the idea that comments
are a hint that the code needs to be improved: if we have to add detail to an
assertion, maybe that’s a hint that we could make the failure more obvious.
In the customer example above, we could improve the failure message by setting
the account identiﬁer in the test Customer to the self-describing value "a customer
account id":
ComparisonFailure: expected:<[a customer account id]> but was:<[id not set]>
Now we don’t need to add an explanatory message, because the value itself
explains its role.
We might be able to do more when we’re working with reference types. For
example, in a test that has this setup:
Date startDate = new Date(1000);
Date endDate = new Date(2000);
the failure message reports that a payment date is wrong but doesn’t describe
where the wrong value might have come from:
java.lang.AssertionError: payment date
Expected: <Thu Jan 01 01:00:01 GMT 1970>
     got: <Thu Jan 01 01:00:02 GMT 1970>
What we really want to know is the meaning of these dates. If we force the
display string:
Date startDate = namedDate(1000, "startDate");
Date endDate = namedDate(2000, "endDate");
Date namedDate(long timeValue, final String name) {
    return new Date(timeValue) { public String toString() { return name; } };
}
we get a message that describes the role that each date plays:
java.lang.AssertionError: payment date
Expected: <startDate>
     got: <endDate>
which makes it clear that we’ve assigned the wrong ﬁeld to the payment date.1
1. This is yet another motivation for deﬁning more domain types to hide the basic types
in the language. As we discussed in “Domain Types Are Better Than Strings”
(page 213), it gives us somewhere to hang useful behavior like this.
269
Self-Describing Value


---
**Page 270**

Obviously Canned Value
Sometimes, the values being checked can’t easily explain themselves. There’s not
enough information in a char or int, for example. One option is to use improb-
able values that will be obviously different from the values we would expect in
production. For an int, for example, we might use a negative value (if that doesn’t
break the code) or Integer.MAX_VALUE (if it’s wildly out of range). Similarly, the
original version of startDate in the previous example was an obviously canned
value because nothing in the system dated back to 1970.
When a team develops conventions for common values, it can ensure that they
stand out. The INVALID_ID at the end of the last chapter was three digits long;
that would be very obviously wrong if real system identiﬁers were ﬁve digits
and up.
Tracer Object
Sometimes we just want to check that an object is passed around by the code
under test and routed to the appropriate collaborator. We can create a tracer
object, a type of Obviously Canned Value, to represent this value. A tracer object
is a dummy object that has no supported behavior of its own, except to describe
its role when something fails. For example, this test:
@RunWith(JMock.class)
public class CustomerTest {
  final LineItem item1 = context.mock(LineItem.class, "item1");
  final LineItem item2 = context.mock(LineItem.class, "item2");
  final Billing billing = context.mock(Billing.class);
  @Test public void
requestsInvoiceForPurchasedItems() {
    context.checking(new Expectations() {{
      oneOf(billing).add(item1);
      oneOf(billing).add(item2);
    }});
    customer.purchase(item1, item2);
    customer.requestInvoice(billing);
  }
}
might generate a failure report like this:
not all expectations were satisfied
expectations:
  expected once, already invoked 1 time: billing.add(<item1>)
  ! expected once, never invoked: billing.add(<item2>>)
what happened before this:
  billing.add(<item1>)
Chapter 23
Test Diagnostics
270


---
**Page 271**

Notice that jMock can accept a name when creating a mock object that will
be used in failure reporting. In fact, where there’s more than one mock object of
the same type, jMock insists that they are named to avoid confusion (the default
is to use the class name).
Tracer objects can be a useful design tool when TDD’ing a class. We sometimes
use an empty interface to mark (and name) a domain concept and show how
it’s used in a collaboration. Later, as we grow the code, we ﬁll in the interface
with methods to describe its behavior.
Explicitly Assert That Expectations Were Satisﬁed
A test that has both expectations and assertions can produce a confusing failure.
In jMock and other mock object frameworks, the expectations are checked after
the body of the test. If, for example, a collaboration doesn’t work properly and
returns a wrong value, an assertion might fail before any expectations are checked.
This would produce a failure report that shows, say, an incorrect calculation result
rather than the missing collaboration that actually caused it.
In a few cases, then, it’s worth calling the assertIsSatisfied() method on
the Mockery before any of the test assertions to get the right failure report:
context.assertIsSatisfied();
assertThat(result, equalTo(expectedResult));
This demonstrates why it is important to “Watch the Test Fail” (page 42). If
you expect the test to fail because an expectation is not satisﬁed but a postcondi-
tion assertion fails instead, you will see that you should add an explicit call to
assert that all expectations have been satisﬁed.
Diagnostics Are a First-Class Feature
Like everyone else, we ﬁnd it easy to get carried away with the simple three-step
TDD cycle: fail, pass, refactor. We’re making good progress and we know what
the failures mean because we’ve just written the test. But nowadays, we try to
follow the four-step TDD cycle (fail, report, pass, refactor) we described in
Chapter 5, because that’s how we know we’ve understood the feature—and
whoever has to change it in a month’s time will also understand it. Figure 23.1
shows again that we need to maintain the quality of the tests, as well as the
production code.
271
Diagnostics Are a First-Class Feature


---
**Page 272**

Figure 23.1
Improve the diagnostics as part of the TDD cycle
Chapter 23
Test Diagnostics
272


