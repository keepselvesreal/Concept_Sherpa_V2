Line1 # Self-Describing Value (pp.269-270)
Line2 
Line3 ---
Line4 **Page 269**
Line5 
Line6 Self-Describing Value
Line7 An alternative to adding detail to the assertion is to build the detail into values
Line8 in the assertion. We can take this in the same spirit as the idea that comments
Line9 are a hint that the code needs to be improved: if we have to add detail to an
Line10 assertion, maybe that’s a hint that we could make the failure more obvious.
Line11 In the customer example above, we could improve the failure message by setting
Line12 the account identiﬁer in the test Customer to the self-describing value "a customer
Line13 account id":
Line14 ComparisonFailure: expected:<[a customer account id]> but was:<[id not set]>
Line15 Now we don’t need to add an explanatory message, because the value itself
Line16 explains its role.
Line17 We might be able to do more when we’re working with reference types. For
Line18 example, in a test that has this setup:
Line19 Date startDate = new Date(1000);
Line20 Date endDate = new Date(2000);
Line21 the failure message reports that a payment date is wrong but doesn’t describe
Line22 where the wrong value might have come from:
Line23 java.lang.AssertionError: payment date
Line24 Expected: <Thu Jan 01 01:00:01 GMT 1970>
Line25      got: <Thu Jan 01 01:00:02 GMT 1970>
Line26 What we really want to know is the meaning of these dates. If we force the
Line27 display string:
Line28 Date startDate = namedDate(1000, "startDate");
Line29 Date endDate = namedDate(2000, "endDate");
Line30 Date namedDate(long timeValue, final String name) {
Line31     return new Date(timeValue) { public String toString() { return name; } };
Line32 }
Line33 we get a message that describes the role that each date plays:
Line34 java.lang.AssertionError: payment date
Line35 Expected: <startDate>
Line36      got: <endDate>
Line37 which makes it clear that we’ve assigned the wrong ﬁeld to the payment date.1
Line38 1. This is yet another motivation for deﬁning more domain types to hide the basic types
Line39 in the language. As we discussed in “Domain Types Are Better Than Strings”
Line40 (page 213), it gives us somewhere to hang useful behavior like this.
Line41 269
Line42 Self-Describing Value
Line43 
Line44 
Line45 ---
Line46 
Line47 ---
Line48 **Page 270**
Line49 
Line50 Obviously Canned Value
Line51 Sometimes, the values being checked can’t easily explain themselves. There’s not
Line52 enough information in a char or int, for example. One option is to use improb-
Line53 able values that will be obviously different from the values we would expect in
Line54 production. For an int, for example, we might use a negative value (if that doesn’t
Line55 break the code) or Integer.MAX_VALUE (if it’s wildly out of range). Similarly, the
Line56 original version of startDate in the previous example was an obviously canned
Line57 value because nothing in the system dated back to 1970.
Line58 When a team develops conventions for common values, it can ensure that they
Line59 stand out. The INVALID_ID at the end of the last chapter was three digits long;
Line60 that would be very obviously wrong if real system identiﬁers were ﬁve digits
Line61 and up.
Line62 Tracer Object
Line63 Sometimes we just want to check that an object is passed around by the code
Line64 under test and routed to the appropriate collaborator. We can create a tracer
Line65 object, a type of Obviously Canned Value, to represent this value. A tracer object
Line66 is a dummy object that has no supported behavior of its own, except to describe
Line67 its role when something fails. For example, this test:
Line68 @RunWith(JMock.class)
Line69 public class CustomerTest {
Line70   final LineItem item1 = context.mock(LineItem.class, "item1");
Line71   final LineItem item2 = context.mock(LineItem.class, "item2");
Line72   final Billing billing = context.mock(Billing.class);
Line73   @Test public void
Line74 requestsInvoiceForPurchasedItems() {
Line75     context.checking(new Expectations() {{
Line76       oneOf(billing).add(item1);
Line77       oneOf(billing).add(item2);
Line78     }});
Line79     customer.purchase(item1, item2);
Line80     customer.requestInvoice(billing);
Line81   }
Line82 }
Line83 might generate a failure report like this:
Line84 not all expectations were satisfied
Line85 expectations:
Line86   expected once, already invoked 1 time: billing.add(<item1>)
Line87   ! expected once, never invoked: billing.add(<item2>>)
Line88 what happened before this:
Line89   billing.add(<item1>)
Line90 Chapter 23
Line91 Test Diagnostics
Line92 270
Line93 
Line94 
Line95 ---
