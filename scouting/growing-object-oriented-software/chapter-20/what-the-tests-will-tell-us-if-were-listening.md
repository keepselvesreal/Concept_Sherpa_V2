Line1 # What the Tests Will Tell Us (If We're Listening) (pp.244-246)
Line2 
Line3 ---
Line4 **Page 244**
Line5 
Line6 Special Bonus Prize
Line7 We always have problems coming up with good examples. There’s actually a
Line8 better improvement to this code, which is to notice that we’ve pulled out a chain
Line9 of objects to get to the case object, exposing dependencies that aren’t relevant
Line10 here. Instead, we should have told the nearest object to do the work for us,
Line11 like this:
Line12 public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
Line13   if (firstParty.isReady()) {
Line14 organization.adjudicateBetween(firstParty, thirdParty, issue);
Line15   } else {
Line16     thirdParty.adjourn();
Line17   }
Line18 }
Line19 or, possibly,
Line20 public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
Line21   if (firstParty.isReady()) {
Line22     thirdParty.startAdjudication(organization, firstParty, issue);
Line23   } else{
Line24     thirdParty.adjourn();
Line25   }
Line26 }
Line27 which looks more balanced. If you spotted this, we award you a Moment of
Line28 Smugness™ to be exercised at your convenience.
Line29 What the Tests Will Tell Us (If We’re Listening)
Line30 We’ve found these beneﬁts from learning to listen to test smells:
Line31 Keep knowledge local
Line32 Some of the test smells we’ve identiﬁed, such as needing “magic” to create
Line33 mocks, are to do with knowledge leaking between components. If we can
Line34 keep knowledge local to an object (either internal or passed in), then its im-
Line35 plementation is independent of its context; we can safely move it wherever
Line36 we like. Do this consistently and your application, built out of pluggable
Line37 components, will be easy to change.
Line38 If it’s explicit, we can name it
Line39 One reason why we don’t like mocking concrete classes is that we like to
Line40 have names for the relationships between objects as well the objects them-
Line41 selves. As the legends say, if we have something’s true name, we can control
Line42 it. If we can see it, we have a better chance of ﬁnding its other uses and so
Line43 reducing duplication.
Line44 Chapter 20
Line45 Listening to the Tests
Line46 244
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 245**
Line53 
Line54 More names mean more domain information
Line55 We ﬁnd that when we emphasize how objects communicate, rather than
Line56 what they are, we end up with types and roles deﬁned more in terms of the
Line57 domain than of the implementation. This might be because we have a greater
Line58 number of smaller abstractions, which gets us further away from the under-
Line59 lying language. Somehow we seem to get more domain vocabulary into
Line60 the code.
Line61 Pass behavior rather than data
Line62 We ﬁnd that by applying “Tell, Don’t Ask” consistently, we end up with a
Line63 coding style where we tend to pass behavior (in the form of callbacks) into
Line64 the system instead of pulling values up through the stack. For example, in
Line65 Chapter 17, we introduced a SniperCollector that responds when told about
Line66 a new Sniper. Passing this listener into the Sniper creation code gives us
Line67 better information hiding than if we’d exposed a collection to be added
Line68 to. More precise interfaces give us better information-hiding and clearer
Line69 abstractions.
Line70 We care about keeping the tests and code clean as we go, because it helps to
Line71 ensure that we understand our domain and reduces the risk of being unable
Line72 to cope when a new requirement triggers changes to the design. It’s much easier to
Line73 keep a codebase clean than to recover from a mess. Once a codebase starts
Line74 to “rot,” the developers will be under pressure to botch the code to get the next
Line75 job done. It doesn’t take many such episodes to dissipate a team’s good intentions.
Line76 We once had a posting to the jMock user list that included this comment:
Line77 I was involved in a project recently where jMock was used quite heavily. Looking
Line78 back, here’s what I found:
Line79 1.
Line80 The unit tests were at times unreadable (no idea what they were doing).
Line81 2.
Line82 Some tests classes would reach 500 lines in addition to inheriting an abstract
Line83 class which also would have up to 500 lines.
Line84 3.
Line85 Refactoring would lead to massive changes in test code.
Line86 A unit test shouldn’t be 1000 lines long! It should focus on at most a few
Line87 classes and should not need to create a large ﬁxture or perform lots of preparation
Line88 just to get the objects into a state where the target feature can be exercised. Such
Line89 tests are hard to understand—there’s just so much to remember when reading
Line90 them. And, of course, they’re brittle, all the objects in play are too tightly coupled
Line91 and too difﬁcult to set to the state the test requires.
Line92 Test-driven development can be unforgiving. Poor quality tests can slow devel-
Line93 opment to a crawl, and poor internal quality of the system being tested will result
Line94 in poor quality tests. By being alert to the internal quality feedback we get from
Line95 245
Line96 What the Tests Will Tell Us (If We’re Listening)
Line97 
Line98 
Line99 ---
Line100 
Line101 ---
Line102 **Page 246**
Line103 
Line104 writing tests, we can nip this problem in the bud, long before our unit tests ap-
Line105 proach 1000 lines of code, and end up with tests we can live with. Conversely,
Line106 making an effort to write tests that are readable and ﬂexible gives us more feed-
Line107 back about the internal quality of the code we are testing. We end up with tests
Line108 that help, rather than hinder, continued development.
Line109 Chapter 20
Line110 Listening to the Tests
Line111 246
