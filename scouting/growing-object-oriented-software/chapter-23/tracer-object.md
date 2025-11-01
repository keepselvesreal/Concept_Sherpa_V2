Line1 # Tracer Object (pp.270-271)
Line2 
Line3 ---
Line4 **Page 270**
Line5 
Line6 Obviously Canned Value
Line7 Sometimes, the values being checked can’t easily explain themselves. There’s not
Line8 enough information in a char or int, for example. One option is to use improb-
Line9 able values that will be obviously different from the values we would expect in
Line10 production. For an int, for example, we might use a negative value (if that doesn’t
Line11 break the code) or Integer.MAX_VALUE (if it’s wildly out of range). Similarly, the
Line12 original version of startDate in the previous example was an obviously canned
Line13 value because nothing in the system dated back to 1970.
Line14 When a team develops conventions for common values, it can ensure that they
Line15 stand out. The INVALID_ID at the end of the last chapter was three digits long;
Line16 that would be very obviously wrong if real system identiﬁers were ﬁve digits
Line17 and up.
Line18 Tracer Object
Line19 Sometimes we just want to check that an object is passed around by the code
Line20 under test and routed to the appropriate collaborator. We can create a tracer
Line21 object, a type of Obviously Canned Value, to represent this value. A tracer object
Line22 is a dummy object that has no supported behavior of its own, except to describe
Line23 its role when something fails. For example, this test:
Line24 @RunWith(JMock.class)
Line25 public class CustomerTest {
Line26   final LineItem item1 = context.mock(LineItem.class, "item1");
Line27   final LineItem item2 = context.mock(LineItem.class, "item2");
Line28   final Billing billing = context.mock(Billing.class);
Line29   @Test public void
Line30 requestsInvoiceForPurchasedItems() {
Line31     context.checking(new Expectations() {{
Line32       oneOf(billing).add(item1);
Line33       oneOf(billing).add(item2);
Line34     }});
Line35     customer.purchase(item1, item2);
Line36     customer.requestInvoice(billing);
Line37   }
Line38 }
Line39 might generate a failure report like this:
Line40 not all expectations were satisfied
Line41 expectations:
Line42   expected once, already invoked 1 time: billing.add(<item1>)
Line43   ! expected once, never invoked: billing.add(<item2>>)
Line44 what happened before this:
Line45   billing.add(<item1>)
Line46 Chapter 23
Line47 Test Diagnostics
Line48 270
Line49 
Line50 
Line51 ---
Line52 
Line53 ---
Line54 **Page 271**
Line55 
Line56 Notice that jMock can accept a name when creating a mock object that will
Line57 be used in failure reporting. In fact, where there’s more than one mock object of
Line58 the same type, jMock insists that they are named to avoid confusion (the default
Line59 is to use the class name).
Line60 Tracer objects can be a useful design tool when TDD’ing a class. We sometimes
Line61 use an empty interface to mark (and name) a domain concept and show how
Line62 it’s used in a collaboration. Later, as we grow the code, we ﬁll in the interface
Line63 with methods to describe its behavior.
Line64 Explicitly Assert That Expectations Were Satisﬁed
Line65 A test that has both expectations and assertions can produce a confusing failure.
Line66 In jMock and other mock object frameworks, the expectations are checked after
Line67 the body of the test. If, for example, a collaboration doesn’t work properly and
Line68 returns a wrong value, an assertion might fail before any expectations are checked.
Line69 This would produce a failure report that shows, say, an incorrect calculation result
Line70 rather than the missing collaboration that actually caused it.
Line71 In a few cases, then, it’s worth calling the assertIsSatisfied() method on
Line72 the Mockery before any of the test assertions to get the right failure report:
Line73 context.assertIsSatisfied();
Line74 assertThat(result, equalTo(expectedResult));
Line75 This demonstrates why it is important to “Watch the Test Fail” (page 42). If
Line76 you expect the test to fail because an expectation is not satisﬁed but a postcondi-
Line77 tion assertion fails instead, you will see that you should add an explicit call to
Line78 assert that all expectations have been satisﬁed.
Line79 Diagnostics Are a First-Class Feature
Line80 Like everyone else, we ﬁnd it easy to get carried away with the simple three-step
Line81 TDD cycle: fail, pass, refactor. We’re making good progress and we know what
Line82 the failures mean because we’ve just written the test. But nowadays, we try to
Line83 follow the four-step TDD cycle (fail, report, pass, refactor) we described in
Line84 Chapter 5, because that’s how we know we’ve understood the feature—and
Line85 whoever has to change it in a month’s time will also understand it. Figure 23.1
Line86 shows again that we need to maintain the quality of the tests, as well as the
Line87 production code.
Line88 271
Line89 Diagnostics Are a First-Class Feature
Line90 
Line91 
Line92 ---
