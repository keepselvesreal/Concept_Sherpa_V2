Line1 # Obviously Canned Value (pp.270-270)
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
