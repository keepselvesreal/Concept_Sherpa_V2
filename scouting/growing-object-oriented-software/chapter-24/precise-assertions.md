Line1 # Precise Assertions (pp.275-277)
Line2 
Line3 ---
Line4 **Page 275**
Line5 
Line6 public interface CustomerBase {
Line7 Maybe<Customer> findCustomerWithEmailAddress(String emailAddress);
Line8 }
Line9 public abstract class Maybe<T> implements Iterable<T> {
Line10   abstract boolean hasResult();
Line11   public static Maybe<T> just(T oneValue) { …
Line12   public static Maybe<T> nothing() { …
Line13 }
Line14 We still, however, have the tests that stub CustomerBase to return null, to
Line15 represent missing customers. The compiler cannot warn us of the mismatch be-
Line16 cause null is a valid value of type Maybe<Customer> too, so the best we can do
Line17 is to watch all these tests fail and change each one to the new design.
Line18 If, instead, we’d given the tests their own representation of “no customer
Line19 found” as a single well-named constant instead of the literal null, we could have
Line20 avoided this drudgery. We would have changed one line:
Line21 public static final Customer NO_CUSTOMER_FOUND = null;
Line22 to
Line23 public static final Maybe<Customer> NO_CUSTOMER_FOUND = Maybe.nothing();
Line24 without changing the tests themselves.
Line25 Tests should be written in terms of the information passed between objects,
Line26 not of how that information is represented. Doing so will both make the tests
Line27 more self-explanatory and shield them from changes in implementation controlled
Line28 elsewhere in the system. Signiﬁcant values, like NO_CUSTOMER_FOUND, should be
Line29 deﬁned in one place as a constant. There’s another example in Chapter 12 when
Line30 we introduce UNUSED_CHAT. For more complex structures, we can hide the details
Line31 of the representation in test data builders (Chapter 22).
Line32 Precise Assertions
Line33 In a test, focus the assertions on just what’s relevant to the scenario being tested.
Line34 Avoid asserting values that aren’t driven by the test inputs, and avoid reasserting
Line35 behavior that is covered in other tests.
Line36 We ﬁnd that these heuristics guide us towards writing tests where each method
Line37 exercises a unique aspect of the target code’s behavior. This makes the tests more
Line38 robust because they’re not dependent on unrelated results, and there’s less
Line39 duplication.
Line40 Most test assertions are simple checks for equality; for example, we assert the
Line41 number of rows in a table model in “Extending the Table Model” (page 180).
Line42 Testing for equality doesn’t scale well as the value being returned becomes more
Line43 275
Line44 Precise Assertions
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 276**
Line51 
Line52 complex. Different test scenarios may make the tested code return results that
Line53 differ only in speciﬁc attributes, so comparing the entire result each time is
Line54 misleading and introduces an implicit dependency on the behavior of the whole
Line55 tested object.
Line56 There are a couple of ways in which a result can be more complex. First, it
Line57 can be deﬁned as a structured value type. This is straightforward since we can
Line58 just reference directly any attributes we want to assert. For example, if we take
Line59 the ﬁnancial instrument from “Use Structure to Explain” (page 253), we might
Line60 need to assert only its strike price:
Line61 assertEquals("strike price", 92, instrument.getStrikePrice());
Line62 without comparing the whole instrument.
Line63 We can use Hamcrest matchers to make the assertions more expressive and
Line64 more ﬁnely tuned. For example, if we want to assert that a transaction identiﬁer
Line65 is larger than its predecessor, we can write:
Line66 assertThat(instrument.getTransactionId(), largerThan(PREVIOUS_TRANSACTION_ID));
Line67 This tells the programmer that the only thing we really care about is that the new
Line68 identiﬁer is larger than the previous one—its actual value is not important in this
Line69 test. The assertion also generates a helpful message when it fails.
Line70 The second source of complexity is implicit, but very common. We often have
Line71 to make assertions about a text string. Sometimes we know exactly what the text
Line72 should be, for example when we have the FakeAuctionServer look for speciﬁc
Line73 messages in “Extending the Fake Auction” (page 107). Sometimes, however,
Line74 all we need to check is that certain values are included in the text.
Line75 A frequent example is when generating a failure message. We don’t want all
Line76 our unit tests to be locked to its current formatting, so that they fail when we
Line77 add whitespace, and we don’t want to have to do anything clever to cope with
Line78 timestamps. We just want to know that the critical information is included, so
Line79 we write:
Line80 assertThat(failureMessage,
Line81            allOf(containsString("strikePrice=92"), 
Line82                  containsString("id=FGD.430"), 
Line83                  containsString("is expired"))); 
Line84 which asserts that all these strings occur somewhere in failureMessage. That’s
Line85 enough reassurance for us, and we can write other tests to check that a message
Line86 is formatted correctly if we think it’s signiﬁcant.
Line87 One interesting effect of trying to write precise assertions against text strings
Line88 is that the effort often suggests that we’re missing an intermediate structure
Line89 object—in this case perhaps an InstrumentFailure. Most of the code would be
Line90 written in terms of an InstrumentFailure, a structured value that carries all the
Line91 relevant ﬁelds. The failure would be converted to a string only at the last possible
Line92 moment, and that string conversion can be tested in isolation.
Line93 Chapter 24
Line94 Test Flexibility
Line95 276
Line96 
Line97 
Line98 ---
Line99 
Line100 ---
Line101 **Page 277**
Line102 
Line103 Precise Expectations
Line104 We can extend the concept of being precise about assertions to being precise
Line105 about expectations. Each mock object test should specify just the relevant details
Line106 of the interactions between the object under test and its neighbors. The combined
Line107 unit tests for an object describe its protocol for communicating with the rest of
Line108 the system.
Line109 We’ve built a lot of support into jMock for specifying this communication
Line110 between objects as precisely as it should be. The API is designed to produce tests
Line111 that clearly express how objects relate to each other and that are ﬂexible because
Line112 they’re not too restrictive. This may require a little more test code than some
Line113 of the alternatives, but we ﬁnd that the extra rigor keeps the tests clear.
Line114 Precise Parameter Matching
Line115 We want to be as precise about the values passed in to a method as we are about
Line116 the value it returns. For example, in “Assertions and Expectations” (page 254)
Line117 we showed an expectation where one of the accepted arguments was any type
Line118 of RuntimeException; the speciﬁc class doesn’t matter. Similarly, in “Extracting
Line119 the SnipersTableModel” (page 197), we have this expectation:
Line120 oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId)));
Line121 The method sniperForItem() returns a Matcher that checks only the item identiﬁer
Line122 when given an AuctionSniper. This test doesn’t care about anything else in the
Line123 sniper’s state, such as its current bid or last price, so we don’t make it more
Line124 brittle by checking those values.
Line125 The same precision can be applied to expecting input strings. If, for example,
Line126 we have an auditTrail object to accept the failure message we described
Line127 above, we can write a precise expectation for that auditing:
Line128 oneOf(auditTrail).recordFailure(with(allOf(containsString("strikePrice=92"),
Line129                                            containsString("id=FGD.430"), 
Line130                                            containsString("is expired")))); 
Line131 Allowances and Expectations
Line132 We introduced the concept of allowances in “The Sniper Acquires Some State”
Line133 (page 144). jMock insists that all expectations are met during a test, but al-
Line134 lowances may be matched or not. The point of the distinction is to highlight
Line135 what matters in a particular test. Expectations describe the interactions that are
Line136 essential to the protocol we’re testing: if we send this message to the object, we
Line137 expect to see it send this other message to this neighbor.
Line138 Allowances support the interaction we’re testing. We often use them as stubs
Line139 to feed values into the object, to get the object into the right state for the behavior
Line140 we want to test. We also use them to ignore other interactions that aren’t relevant
Line141 277
Line142 Precise Expectations
Line143 
Line144 
Line145 ---
