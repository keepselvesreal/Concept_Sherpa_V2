Line1 # Externalize Event Sources (pp.326-360)
Line2 
Line3 ---
Line4 **Page 326**
Line5 
Line6 brittle—they would misreport if the system changes the assumptions they’ve been
Line7 built on. One response is to add a test to conﬁrm those expectations—in this
Line8 case, perhaps a stress test to conﬁrm event processing order and alert the team
Line9 if circumstances change. That said, there should already be other tests that conﬁrm
Line10 those assumptions, so it may be enough just to associate these tests, for example
Line11 by grouping them in the same test package.
Line12 Distinguish Synchronizations and Assertions
Line13 We have one mechanism for synchronizing a test with its system and for making
Line14 assertions about that system—wait for an observable condition and time out if
Line15 it doesn’t happen. The only difference between the two activities is our interpre-
Line16 tation of what they mean. As always, we want to make our intentions explicit,
Line17 but it’s especially important here because there’s a risk that someone may look
Line18 at the test later and remove what looks like a duplicate assertion, accidentally
Line19 introducing a race condition.
Line20 We often adopt a naming scheme to distinguish between synchronizations and
Line21 assertions. For example, we might have waitUntil() and assertEventually()
Line22 methods to express the purpose of different checks that share an underlying
Line23 implementation.
Line24 Alternatively, we might reserve the term “assert” for synchronous tests and
Line25 use a different naming conventions in asynchronous tests, as we did in the Auction
Line26 Sniper example.
Line27 Externalize Event Sources
Line28 Some systems trigger their own events internally. The most common example is
Line29 using a timer to schedule activities. This might include repeated actions that run
Line30 frequently, such as bundling up emails for forwarding, or follow-up actions that
Line31 run days or even weeks in the future, such as conﬁrming a delivery date.
Line32 Hidden timers are very difﬁcult to work with because they make it hard to tell
Line33 when the system is in a stable state for a test to make its assertions. Waiting for
Line34 a repeated action to run is too slow to “succeed fast,” to say nothing of an action
Line35 scheduled a month from now. We also don’t want tests to break unpredictably
Line36 because of interference from a scheduled activity that’s just kicked in. Trying to
Line37 test a system by coinciding timers is just too brittle.
Line38 The only solution is to make the system deterministic by decoupling it from
Line39 its own scheduling. We can pull event generation out into a shared service that
Line40 is driven externally. For example, in one project we implemented the system’s
Line41 scheduler as a web service. System components scheduled activities by making
Line42 HTTP requests to the scheduler, which triggered activities by making HTTP
Line43 “postbacks.” In another project, the scheduler published notiﬁcations onto a
Line44 message bus topic that the components listened to.
Line45 Chapter 27
Line46 Testing Asynchronous Code
Line47 326
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 327**
Line54 
Line55 With this separation in place, tests can step the system through its behavior
Line56 by posing as the scheduler and generating events deterministically. Now we can
Line57 run system tests quickly and reliably. This is a nice example of a testing require-
Line58 ment leading to a better design. We’ve been forced to abstract out scheduling,
Line59 which means we won’t have multiple implementations hidden in the system.
Line60 Usually, introducing such an event infrastructure turns out to be useful for
Line61 monitoring and administration.
Line62 There’s a trade-off too, of course. Our tests are no longer exercising the entire
Line63 system. We’ve prioritized test speed and reliability over ﬁdelity. We compensate
Line64 by keeping the scheduler’s API as simple as possible and testing it rigorously
Line65 (another advantage). We would probably also write a few slow tests, running in
Line66 a separate build, that exercise the whole system together including the real
Line67 scheduler.
Line68 327
Line69 Externalize Event Sources
Line70 
Line71 
Line72 ---
Line73 
Line74 ---
Line75 **Page 328**
Line76 
Line77 This page intentionally left blank 
Line78 
Line79 
Line80 ---
Line81 
Line82 ---
Line83 **Page 329**
Line84 
Line85 Afterword
Line86 A Brief History of Mock
Line87 Objects
Line88 Tim Mackinnon
Line89 Introduction
Line90 The ideas and concepts behind mock objects didn’t materialise in a single day.
Line91 There’s a long history of experimentation, discussion, and collaboration between
Line92 many different developers who have taken the seed of an idea and grown it into
Line93 something more profound. The ﬁnal result—the topic of this book—should help
Line94 you with your software development; but the background story of “The Making
Line95 of Mock Objects” is also interesting—and a testament to the dedication of the
Line96 people involved. I hope revisiting this history will inspire you too to challenge
Line97 your thoughts on what is possible and to experiment with new practices.
Line98 Origins
Line99 The story began on a roundabout1 near Archway station in London in late 1999.
Line100 That evening, several members of a London-based software architecture group2
Line101 met to discuss topical issues in software. The discussion turned to experiences
Line102 with Agile Software Development and I mentioned the impact that writing tests
Line103 seemed to be having on our code. This was before the ﬁrst Extreme Programming
Line104 book had been published, and teams like ours were still exploring how to do
Line105 test-driven development—including what constituted a good test. In particular,
Line106 I had noticed a tendency to add “getter” methods to our objects to facilitate
Line107 testing. This felt wrong, since it could be seen as violating object-oriented princi-
Line108 ples, so I was interested in the thoughts of the other members. The conversation
Line109 was quite lively—mainly centering on the tension between pragmatism in testing
Line110 and pure object-oriented design. We also had a recent example of a colleague,
Line111 1. “Roundabout” is the UK term for a trafﬁc circle.
Line112 2. On this occasion, they were Tim Mackinnon, Peter Marks, Ivan Moore, and John
Line113 Nolan.
Line114 329
Line115 
Line116 
Line117 ---
Line118 
Line119 ---
Line120 **Page 330**
Line121 
Line122 Oli Bye, stubbing out the Java Servlet API for testing a web application without
Line123 a server.
Line124 I particularly remember from that evening a crude diagram of an onion3 and
Line125 its metaphor of the many layers of software, along with the mantra “No Getters!
Line126 Period!” The discussion revolved around how to safely peel back and test layers
Line127 of that onion without impacting its design. The solution was to focus on the
Line128 composition of software components (the group had discussed Brad Cox’s ideas
Line129 on software components many times before). It was an interesting collision of
Line130 opinions, and the emphasis on composition—now referred to as dependency
Line131 injection—gave us a technique for eliminating the getters we were “pragmatically”
Line132 adding to objects so we could write tests for them.
Line133 The following day, our small team at Connextra4 started putting the idea into
Line134 practice. We removed the getters from sections of our code and used a composi-
Line135 tional strategy by adding constructors that took the objects we wanted to test
Line136 via getters as parameters. At ﬁrst this felt cumbersome, and our two recent
Line137 graduate recruits were not convinced. I, however, had a Smalltalk background,
Line138 so to me the idea of composition and delegation felt right. Enforcing a “no getters”
Line139 rule seemed like a way to achieve a more object-oriented feeling in the Java
Line140 language we were using.
Line141 We stuck to it for several days and started to see some patterns emerging. More
Line142 of our conversations were about expecting things to happen between our
Line143 objects, and we frequently had variables with names like expectedURL and
Line144 expectedServiceName  in our injected objects. On the other hand, when our tests
Line145 failed we were tired of stepping through in a debugger to see what went wrong.
Line146 We started adding variables with names like actualURL and actualServiceName
Line147 to allow the injected test objects to throw exceptions with helpful messages.
Line148 Printing the expected and actual values side-by-side showed us immediately what
Line149 the problem was.
Line150 Over the course of several weeks we refactored these ideas into a group of
Line151 classes: ExpectationValue for single values, ExpectationList for multiple values
Line152 in a particular order, and ExpectationSet for unique values in any order. Later,
Line153 Tung Mac also added ExpectationCounter for situations where we didn’t want
Line154 to specify explicit values but just count the number of calls. It started to feel as
Line155 if something interesting was happening, but it seemed so obvious to me that there
Line156 wasn’t really much to describe. One afternoon, Peter Marks decided that we
Line157 should come up with name for what we were doing—so we could at least package
Line158 the code—and, after a few suggestions, proposed “mock.” We could use it both
Line159 as a noun and a verb, and it refactored nicely into our code, so we adopted it.
Line160 3. Initially drawn by John Nolan.
Line161 4. The team consisted of Tim Mackinnon, Tung Mac, and Matthew Cooke, with
Line162 direction from Peter Marks and John Nolan. Connextra is now part of Bet Genius.
Line163 Afterword 
Line164 A Brief History of Mock Objects
Line165 330
Line166 
Line167 
Line168 ---
Line169 
Line170 ---
Line171 **Page 331**
Line172 
Line173 Spreading the Word
Line174 Around this time, we5 also started the London Extreme Tuesday Club (XTC) to
Line175 share experiences of Extreme Programming with other teams. During one meeting,
Line176 I described our refactoring experiments and explained that I felt that it helped
Line177 our junior developers write better object-oriented code. I ﬁnished the story by
Line178 saying, “But this is such an obvious technique that I’m sure most people do it
Line179 eventually anyway.” Steve pointed out that the most obvious things aren’t always
Line180 so obvious and are usually difﬁcult to describe. He thought this could make a
Line181 great paper if we could sort the wood from the trees, so we decided to collaborate
Line182 with another XTC member (Philip Craig) and write something for the XP2000
Line183 conference. If nothing else, we wanted to go to Sardinia.
Line184 We began to pick apart the ideas and give them a consistent set of names,
Line185 studying real code examples to understand the essence of the technique. We
Line186 backported new concepts we discovered to the original Connextra codebase to
Line187 validate their effectiveness. This was an exciting time and I recall that it took
Line188 many late nights to reﬁne our ideas—although we were still struggling to come
Line189 up with an accurate “elevator pitch” for mock objects. We knew what it felt like
Line190 when using them to drive great code, but describing this experience to other
Line191 developers who weren’t part of the XTC was still challenging.
Line192 The XP2000 paper [Mackinnon00] and the initial mock objects library had a
Line193 mixed reception—for some it was revolutionary, for others it was unnecessary
Line194 overhead. In retrospect, the fact that Java didn’t have good reﬂection when we
Line195 started meant that many of the steps were manual, or augmented with code
Line196 generation tools.6 This turned people off—they couldn’t separate the idea from
Line197 the implementation.
Line198 Another Generation
Line199 The story continues when Nat Pryce took the ideas and implemented them in
Line200 Ruby. He exploited Ruby’s reﬂection to write expectations directly into the test
Line201 as blocks. Inﬂuenced by his PhD work on protocols between components, his li-
Line202 brary changed the emphasis from asserting parameter values to asserting messages
Line203 sent between objects. Nat then ported his implementation to Java, using the new
Line204 Proxy type in Java 1.3 and deﬁning expectations with “constraint” objects. When
Line205 Nat showed us this work, it immediately clicked. He donated his library to the
Line206 mock objects project and visited the Connextra ofﬁces where we worked together
Line207 to add features that the Connextra developers needed.
Line208 5. With Tim Mackinnon, Oli Bye, Paul Simmons, and Steve Freeman. Oli coined the
Line209 name XTC.
Line210 6. This later changed as Java 1.1 was released, which improved reﬂection, and as others
Line211 who had read our paper wrote more tools, such as Tammo Freese’s Easymock.
Line212 331
Line213 Another Generation
Line214 
Line215 
Line216 ---
Line217 
Line218 ---
Line219 **Page 332**
Line220 
Line221 With Nat in the ofﬁce where mock objects were being used constantly, we
Line222 were driven to use his improvements to provide more descriptive failure messages.
Line223 We had seen our developers getting bogged down when the reason for a test
Line224 failure was not obvious enough (later, we observed that this was often a hint
Line225 that an object had too many responsibilities). Now, constraints allowed us to
Line226 write tests that were more expressive and provided better failure diagnostics, as
Line227 the constraint objects could explain what went wrong.7 For example, a failure
Line228 on a stringBegins constraint could produce a message like:
Line229 Expected a string parameter beginning with "http" 
Line230   but was called with a value of "ftp.domain.com"
Line231 We released the new improved version of Nat’s library under the name Dynamock.
Line232 As we improved the library, more programmers started using it, which intro-
Line233 duced new requirements. We started adding more and more options to the API
Line234 until, eventually, it became too complicated to maintain—especially as we had
Line235 to support multiple versions of Java. Meanwhile, Steve tired of the the duplication
Line236 in the syntax required to set up expectations, so he introduced a version of a
Line237 Smalltalk cascade—multiple calls to the same object.
Line238 Then Steve noticed that in a statically typed language like Java, a cascade could
Line239 return a chain of interfaces to control when methods are made available to the
Line240 caller—in effect, we could use types to encode a workﬂow. Steve also wanted to
Line241 improve the programming experience by guiding the new generation of IDEs
Line242 to prompt with the “right” completion options. Over the course of a year, Steve
Line243 and Nat, with much input from the rest of us, pushed the idea hard to produce
Line244 jMock, an expressive API over our original Dynamock framework. This was also
Line245 ported to C# as NMock. At some point in this process, they realized that
Line246 they were actually writing a language in Java which could be used to write
Line247 expectations; they wrote this up later in an OOPLSA paper [Freeman06].
Line248 Consolidation
Line249 Through our experience in Connextra and other companies, and through giving
Line250 many presentations, we improved our understanding and communication of the
Line251 ideas of mock objects. Steve (inspired by some of the early lean software material)
Line252 coined the term “needs-driven development,” and Joe Walnes, another colleague,
Line253 drew a nice visualisation of islands of objects communicating with each other.
Line254 Joe also had the insight of using mock objects to drive the design of interfaces
Line255 between objects. At the time, we were struggling to promote the idea of using
Line256 mock objects as a design tool; many people (including some authors) saw it only
Line257 as a technique for speeding up unit tests. Joe cut through all the conceptual
Line258 barriers with his simple heuristic of “Only mock types you own.”
Line259 7. Later, Steve talked Charlie Poole into including constraints in NUnit. It took some
Line260 extra years to have matchers (the latest version of constraints) adopted by JUnit.
Line261 Afterword 
Line262 A Brief History of Mock Objects
Line263 332
Line264 
Line265 
Line266 ---
Line267 
Line268 ---
Line269 **Page 333**
Line270 
Line271 We took all these ideas and wrote a second conference paper, “Mock Roles
Line272 not Objects” [Freeman04]. Our initial description had focused too much on im-
Line273 plementation, whereas the critical idea was that the technique emphasizes the
Line274 roles that objects play for each other. When developers are using mock objects
Line275 well, I observe them drawing diagrams of what they want to test, or using CRC
Line276 cards to roleplay relationships—these then translate nicely into mock objects and
Line277 tests that drive the required code.
Line278 Since then, Nat and Steve have reworked jMock to produce jMock2, and Joe
Line279 has extracted constraints into the Hamcrest library (now adopted by JUnit).
Line280 There’s also now a wide selection of mock object libraries, in many different
Line281 languages.
Line282 The results have been worth the effort. I think we can ﬁnally say that there is
Line283 now a well-documented and polished technique that helps you write better soft-
Line284 ware. From those humble “no getters” beginnings, this book summarizes years
Line285 of experience from all of us who have collaborated, and adds Steve and Nat’s
Line286 language expertise and careful attention to detail to produce something that is
Line287 greater than the sum of its parts.
Line288 333
Line289 Consolidation
Line290 
Line291 
Line292 ---
Line293 
Line294 ---
Line295 **Page 334**
Line296 
Line297 This page intentionally left blank 
Line298 
Line299 
Line300 ---
Line301 
Line302 ---
Line303 **Page 335**
Line304 
Line305 Appendix A
Line306 jMock2 Cheat Sheet
Line307 Introduction
Line308 We use jMock2 as our mock object framework throughout this book. This
Line309 chapter summarizes its features and shows some examples of how to use them.
Line310 We’re using JUnit 4.6 (we assume you’re familiar with it); jMock also supports
Line311 JUnit3. Full documentation is available at www.jmock.org.
Line312 We’ll show the structure of a jMock unit test and describe what its features
Line313 do. Here’s a whole example:
Line314 import org.jmock.Expectations;
Line315 import org.jmock.Mockery;
Line316 import org.jmock.integration.junit4.JMock;
Line317 import org.jmock.integration.junit4.JUnit4Mockery;
Line318 @RunWith(JMock.class)
Line319 public class TurtleDriverTest {
Line320   private final Mockery context = new JUnit4Mockery();
Line321   private final Turtle turtle = context.mock(Turtle.class);
Line322   @Test public void 
Line323 goesAMinimumDistance() {
Line324     final Turtle turtle2 = context.mock(Turtle.class, "turtle2");
Line325     final TurtleDriver driver = new TurtleDriver(turtle1, turtle2); // set up
Line326     context.checking(new Expectations() {{ // expectations
Line327       ignoring (turtle2);
Line328       allowing (turtle).flashLEDs(); 
Line329       oneOf (turtle).turn(45);
Line330       oneOf (turtle).forward(with(greaterThan(20)));  
Line331       atLeast(1).of (turtle).stop();
Line332     }});
Line333     driver.goNext(45); // call the code
Line334     assertTrue("driver has moved", driver.hasMoved()); // further assertions
Line335   }
Line336 }
Line337 335
Line338 
Line339 
Line340 ---
Line341 
Line342 ---
Line343 **Page 336**
Line344 
Line345 Test Fixture Class
Line346 First, we set up the test ﬁxture class by creating its Mockery.
Line347 import org.jmock.Expectations;
Line348 import org.jmock.Mockery;
Line349 import org.jmock.integration.junit4.JMock;
Line350 import org.jmock.integration.junit4.JUnit4Mockery;
Line351 @RunWith(JMock.class)
Line352 public class TurtleDriverTest {
Line353   private final Mockery context = new JUnit4Mockery();
Line354 […]
Line355 }
Line356 For the object under test, a Mockery represents its context—the neighboring
Line357 objects it will communicate with. The test will tell the mockery to create
Line358 mock objects, to set expectations on the mock objects, and to check at the end
Line359 of the test that those expectations have been met. By convention, the mockery is
Line360 stored in an instance variable named context.
Line361 A test written with JUnit4 does not need to extend a speciﬁc base class but
Line362 must specify that it uses jMock with the @RunWith(JMock.class) attribute.1 This
Line363 tells the JUnit runner to ﬁnd a Mockery ﬁeld in the test class and to assert (at the
Line364 right time in the test lifecycle) that its expectations have been met. This requires
Line365 that there should be exactly one mockery ﬁeld in the test class. The class
Line366 JUnit4Mockery will report expectation failures as JUnit4 test failures.
Line367 Creating Mock Objects
Line368 This test uses two mock turtles, which we ask the mockery to create. The ﬁrst is
Line369 a ﬁeld in the test class:
Line370 private final Turtle turtle = context.mock(Turtle.class);
Line371 The second is local to the test, so it’s held in a variable:
Line372 final Turtle turtle2 = context.mock(Turtle.class, "turtle2");
Line373 The variable has to be ﬁnal so that the anonymous expectations block has access
Line374 to it—we’ll return to this soon. This second mock turtle has a speciﬁed name,
Line375 turtle2. Any mock can be given a name which will be used in the report if the
Line376 test fails; the default name is the type of the object. If there’s more than one mock
Line377 object of the same type, jMock enforces that only one uses the default name; the
Line378 others must be given names when declared. This is so that failure reports can
Line379 make clear which mock instance is which when describing the state of the test.
Line380 1. At the time of writing, JUnit was introducing the concept of Rule. We expect to extend
Line381 the jMock API to adopt this technique.
Line382 Appendix A
Line383 jMock2 Cheat Sheet
Line384 336
Line385 
Line386 
Line387 ---
Line388 
Line389 ---
Line390 **Page 337**
Line391 
Line392 Tests with Expectations
Line393 A test sets up its expectations in one or more expectation blocks, for example:
Line394 context.checking(new Expectations() {{ 
Line395 oneOf (turtle).turn(45);
Line396 }}); 
Line397 An expectation block can contain any number of expectations. A test can
Line398 contain multiple expectation blocks; expectations in later blocks are appended
Line399 to those in earlier blocks. Expectation blocks can be interleaved with calls to the
Line400 code under test.
Line401 What’s with the Double Braces?
Line402 The most disconcerting syntax element in jMock is its use of double braces in an
Line403 expectations block. It’s a hack, but with a purpose. If we reformat an expectations
Line404 block, we get this:
Line405 context.checking(new Expectations() {
Line406   {
Line407     oneOf (turtle).turn(45);
Line408   }
Line409 });
Line410 We’re passing to the checking() method an anonymous subclass of Expectations
Line411 (ﬁrst set of braces). Within that subclass, we have an instance initialization block
Line412 (second set of braces) that Java will call after the constructor.Within the initialization
Line413 block, we can reference the enclosing Expectations object, so oneOf() is actually
Line414 an instance method—as are all of the expectation structure clauses we describe
Line415 in the next section.
Line416 The purpose of this baroque structure is to provide a scope for building up
Line417 expectations. All the code in the expectation block is deﬁned within an anonymous
Line418 instance of Expectations, which collects the expectation components that the
Line419 code generates. The scoping to an instance allows us to make this collection im-
Line420 plicit, which requires less code. It also improves our experience in the IDE, since
Line421 code completion will be more focused, as in Figure A.1.
Line422 Referring back to the discussion in “Building Up to Higher-Level Programming”
Line423 (page 65), Expectations is an example of the Builder pattern.
Line424 337
Line425 Tests with Expectations
Line426 
Line427 
Line428 ---
Line429 
Line430 ---
Line431 **Page 338**
Line432 
Line433 Figure A.1
Line434 Narrowed scope gives better code completion
Line435 Expectations
Line436 Expectations have the following structure:
Line437 invocation-count(mock-object).method(argument-constraints);
Line438 inSequence(sequence-name);
Line439 when(state-machine.is(state-name));
Line440 will(action);
Line441 then(state-machine.is(new-state-name));
Line442 The invocation-count and mock-object are required, all the other clauses are
Line443 optional. You can give an expectation any number of inSequence, when, will,
Line444 and then clauses. Here are some common examples:
Line445 oneOf (turtle).turn(45); // The turtle must be told exactly once to turn 45 degrees.
Line446 atLeast(1).of (turtle).stop(); // The turtle must be told at least once to stop.
Line447 allowing (turtle).flashLEDs(); // The turtle may be told any number of times, 
Line448                                // including none, to flash its LEDs.
Line449 allowing (turtle).queryPen(); will(returnValue(PEN_DOWN));
Line450 // The turtle may be asked about its pen any  
Line451                                // number of times and will always return PEN_DOWN.
Line452 ignoring (turtle2); // turtle2 may be told to do anything. This test ignores it.
Line453 Invocation Count
Line454 The invocation count is required to describe how often we expect a call to be
Line455 made during the run of the test. It starts the deﬁnition of an expectation.
Line456 exactly(n).of
Line457 The invocation is expected exactly n times.
Line458 oneOf
Line459 The invocation is expected exactly once. This is a convenience shorthand for
Line460 exactly(1).of
Line461 Appendix A
Line462 jMock2 Cheat Sheet
Line463 338
Line464 
Line465 
Line466 ---
Line467 
Line468 ---
Line469 **Page 339**
Line470 
Line471 atLeast(n).of
Line472 The invocation is expected at least n times.
Line473 atMost(n).of
Line474 The invocation is expected at most n times.
Line475 between(min, max).of
Line476 The invocation is expected at least min times and at most max times.
Line477 allowing
Line478 ignoring
Line479 The invocation is allowed any number of times including none. These
Line480 clauses are equivalent to atLeast(0).of, but we use them to highlight that
Line481 the expectation is a stub—that it’s there to get the test through to the
Line482 interesting part of the behavior.
Line483 never
Line484 The invocation is not expected. This is the default behavior if no expectation
Line485 has been set. We use this clause to emphasize to the reader of a test that an
Line486 invocation should not be called.
Line487 allowing, ignoring, and never can also be applied to an object as a whole.
Line488 For example, ignoring(turtle2) says to allow all calls to turtle2. Similarly,
Line489 never(turtle2) says to fail if any calls are made to turtle2 (which is the same
Line490 as not specifying any expectations on the object). If we add method expectations,
Line491 we can be more precise, for example:
Line492 allowing(turtle2).log(with(anything()));
Line493 never(turtle2).stop(); 
Line494 will allow log messages to be sent to the turtle, but fail if it’s told to stop. In
Line495 practice, while allowing precise invocations is common, blocking individual
Line496 methods is rarely useful.
Line497 Methods
Line498 Expected methods are speciﬁed by calling the method on the mock object within
Line499 an expectation block. This deﬁnes the name of the method and what argument
Line500 values are acceptable. Values passed to the method in an expectation will be
Line501 compared for equality:
Line502 oneOf (turtle).turn(45); // matches turn() called with 45
Line503 oneOf (calculator).add(2, 2); // matches add() called with 2 and 2
Line504 Invocation matching can be made more ﬂexible by using matchers as arguments
Line505 wrapped in with() clauses:
Line506 339
Line507 Expectations
Line508 
Line509 
Line510 ---
Line511 
Line512 ---
Line513 **Page 340**
Line514 
Line515 oneOf(calculator).add(with(lessThan(15)), with(any(int.class)));
Line516 // matches add() called with a number less than 15 and any other number
Line517 Either all the arguments must be matchers or all must be values:
Line518 oneOf(calculator).add(with(lessThan(15)), 22); // this doesn't work!
Line519 Argument Matchers
Line520 The most commonly used matchers are deﬁned in the Expectations class:
Line521 equal(o)
Line522 The argument is equal to o, as deﬁned by calling o.equals() with the actual
Line523 value received during the test. This also recursively compares the contents
Line524 of arrays.
Line525 same(o)
Line526 The argument is the same object as o.
Line527 any(Class<T> type)
Line528 The argument is any value, including null. The type argument is required
Line529 to force Java to type-check the argument at compile time.
Line530 a(Class<T> type)
Line531 an(Class<T> type)
Line532 The argument is an instance of type or of one of its subtypes.
Line533 aNull(Class<T> type)
Line534 The argument is null. The type argument is to force Java to type-check the
Line535 argument at compile time.
Line536 aNonNull(Class<T> type)
Line537 The argument is not null. The type argument is to force Java to type-check
Line538 the argument at compile time.
Line539 not(m)
Line540 The argument does not match the matcher m.
Line541 anyOf(m1, m2, m3, […])
Line542 The argument matches at least one of the matchers m1, m2, m3, […].
Line543 allOf(m1, m2, m3, […])
Line544 The argument matches all of the matchers m1, m2, m3, […].
Line545 More matchers are available from static factory methods of the Hamcrest
Line546 Matchers class, which can be statically imported into the test class. For more
Line547 precision, custom matchers can be written using the Hamcrest library.
Line548 Appendix A
Line549 jMock2 Cheat Sheet
Line550 340
Line551 
Line552 
Line553 ---
Line554 
Line555 ---
Line556 **Page 341**
Line557 
Line558 Actions
Line559 An expectation can also specify an action to perform when it is matched, by
Line560 adding a will() clause after the invocation. For example, this expectation will
Line561 return PEN_DOWN when queryPen() is called:
Line562 allowing (turtle).queryPen(); will(returnValue(PEN_DOWN));
Line563 jMock provides several standard actions, and programmers can provide custom
Line564 actions by implementing the Action interface. The standard actions are:
Line565 will(returnValue(v))
Line566 Return v to the caller.
Line567 will(returnIterator(c))
Line568 Return an iterator for collection c to the caller.
Line569 will(returnIterator(v1, v2, […], vn))
Line570 Return a new iterator over elements v1 to v2 on each invocation.
Line571 will(throwException(e))
Line572 Throw exception e when called.
Line573 will(doAll(a1, a2, […], an))
Line574 Perform all the actions a1 to an on every invocation.
Line575 Sequences
Line576 The order in which expectations are speciﬁed does not have to match the order
Line577 in which their invocations are called. If invocation order is signiﬁcant, it can be
Line578 enforced in a test by adding a Sequence. A test can create more than one sequence
Line579 and an expectation can be part of more than once sequence at a time. The syntax
Line580 for creating a Sequence is:
Line581 Sequence sequence-variable = context.sequence("sequence-name"); 
Line582 To expect a sequence of invocations, create a Sequence object, write the expec-
Line583 tations in the expected order, and add an inSequence() clause to each relevant
Line584 expectation. Expectations in a sequence can have any invocation count. For
Line585 example:
Line586 context.checking(new Expectations() {{
Line587   final Sequence drawing = context.sequence("drawing");
Line588   allowing (turtle).queryColor(); will(returnValue(BLACK));
Line589   atLeast(1).of (turtle).forward(10); inSequence(drawing);
Line590   oneOf (turtle).turn(45);    inSequence(drawing);
Line591   oneOf (turtle).forward(10); inSequence(drawing);
Line592 }});
Line593 341
Line594 Expectations
Line595 
Line596 
Line597 ---
Line598 
Line599 ---
Line600 **Page 342**
Line601 
Line602 Here, the queryColor() call is not in the sequence and can take place at
Line603 any time.
Line604 States
Line605 Invocations can be constrained to occur only when a condition is true, where a
Line606 condition is deﬁned as a state machine that is in a given state. State machines can
Line607 switch between states speciﬁed by state names. A test can create multiple state
Line608 machines, and an invocation can be constrained to one or more conditions. The
Line609 syntax for creating a state machine is:
Line610 States state-machine-name =
Line611          context.states("state-machine-name").startsAs("initial-state");
Line612 The initial state is optional; if not speciﬁed, the state machine starts in an unnamed
Line613 initial state.
Line614 Add these clauses to expectations to constrain them to match invocations in
Line615 a given state, or to switch the state of a state machine after an invocation:
Line616 when(stateMachine.is("state-name"));
Line617 Constrains the last expectation to occur only when stateMachine is in the
Line618 state "state-name".
Line619 when(stateMachine.isNot("state-name"));
Line620 Constrains the last expectation to occur only when stateMachine is not in
Line621 the state "state-name".
Line622 then(stateMachine.is("state-name"));
Line623 Changes stateMachine to be in the state "state-name" when the invocation
Line624 occurs.
Line625 This example allows turtle to move only when the pen is down:
Line626 context.checking(new Expectations() {{
Line627   final States pen = context.states("pen").startsAs("up");
Line628   allowing (turtle).queryColor(); will(returnValue(BLACK));
Line629   allowing (turtle).penDown();        then(pen.is("down"));
Line630   allowing (turtle).penUp();          then(pen.is("up"));
Line631   atLeast(1).of (turtle).forward(15); when(pen.is("down"));
Line632   one (turtle).turn(90);              when(pen.is("down"));
Line633   one (turtle).forward(10);           when(pen.is("down"));
Line634 }} 
Line635 Notice that expectations with states do not deﬁne a sequence; they can be com-
Line636 bined with Sequence constraints if order is signiﬁcant. As before, the queryColor()
Line637 call is not included in the states, and so can be called at any time.
Line638 Appendix A
Line639 jMock2 Cheat Sheet
Line640 342
Line641 
Line642 
Line643 ---
Line644 
Line645 ---
Line646 **Page 343**
Line647 
Line648 Appendix B
Line649 Writing a Hamcrest Matcher
Line650 Introduction
Line651 Although Hamcrest 1.2 comes with a large library of matchers, sometimes these
Line652 do not let you specify an assertion or expectation accurately enough to convey
Line653 what you mean or to keep your tests ﬂexible. In such cases, you can easily deﬁne
Line654 a new matcher that seamlessly extends the JUnit and jMock APIs.
Line655 A matcher is an object that implements the org.hamcrest.Matcher interface:
Line656 public interface SelfDescribing {
Line657   void describeTo(Description description);
Line658 }
Line659 public interface Matcher<T> extends SelfDescribing {
Line660   boolean matches(Object item);
Line661   void describeMismatch(Object item, Description mismatchDescription);
Line662 }
Line663 A matcher does two things:
Line664 •
Line665 Reports whether a parameter value meets the constraint (the matches()
Line666 method);
Line667 •
Line668 Generates a readable description to be included in test failure messages (the
Line669 describeTo() method inherited from the SelfDescribing interface and
Line670 the describeMismatch() method).
Line671 A New Matcher Type
Line672 As an example, we will write a new matcher that tests whether a string starts
Line673 with a given preﬁx. It can be used in tests as shown below. Note that the
Line674 matcher seamlessly extends the assertion: there is no visible difference between
Line675 built-in and third-party matchers at the point of use.
Line676 @Test public void exampleTest() {
Line677 […]
Line678   assertThat(someString, startsWith("Cheese"));
Line679 }
Line680 343
Line681 
Line682 
Line683 ---
Line684 
Line685 ---
Line686 **Page 344**
Line687 
Line688 To write a new matcher, we must implement two things: a new class that im-
Line689 plements the Matcher interface and the startsWith() factory function for our
Line690 assertions to read well when we use the new matcher in our tests.
Line691 To write a matcher type, we extend one of Hamcrest’s abstract base classes,
Line692 rather than implementing the Matcher interface directly.1 For our needs, we can
Line693 extend TypeSafeMatcher<String>, which checks for nulls and type safety, casts
Line694 the matched Object to a String, and calls the template methods [Gamma94] in
Line695 our subclass.
Line696 public class StringStartsWithMatcher extends TypeSafeMatcher<String> {
Line697   private final String expectedPrefix;
Line698   public StringStartsWithMatcher(String expectedPrefix) {
Line699     this.expectedPrefix = expectedPrefix;
Line700   }
Line701   @Override
Line702   protected boolean matchesSafely(String actual) {
Line703     return actual.startsWith(expectedPrefix);
Line704   }
Line705   @Override
Line706   public void describeTo(Description matchDescription) {
Line707     matchDescription.appendText("a string starting with ")
Line708                     .appendValue(expectedPrefix);
Line709   }
Line710   @Override protected void
Line711 describeMismatchSafely(String actual, Description mismatchDescription) {
Line712     String actualPrefix = 
Line713              actual.substring(0, Math.min(actual.length(), expectedPrefix.length()));
Line714     mismatchDescription.appendText("started with ")
Line715                        .appendValue(actualPrefix);
Line716   }
Line717 }
Line718 Matcher Objects Must Be Stateless
Line719 When dispatching each invocation, jMock uses the matchers to ﬁnd an expectation
Line720 that matches the invocation’s arguments. This means that it will call the matchers
Line721 many times during the test, maybe even after the expectation has already been
Line722 matched and invoked. In fact, jMock gives no guarantees of when and how many
Line723 times it will call the matchers. This has no effect on stateless matchers, but the
Line724 behavior of stateful matchers is unpredictable.
Line725 If you want to maintain state in response to invocations, write a custom jMock
Line726 Action, not a Matcher.
Line727 1. This lets the Hamcrest team add methods to the Matcher interface without breaking
Line728 all the code that implements that interface, because they can also add a default
Line729 implementation to the base class.
Line730 Appendix B
Line731 Writing a Hamcrest Matcher
Line732 344
Line733 
Line734 
Line735 ---
Line736 
Line737 ---
Line738 **Page 345**
Line739 
Line740 The text generated by the describeTo() and describeMismatch() must follow
Line741 certain grammatical conventions to ﬁt into the error messages generated by
Line742 JUnit and jMock. Although JUnit and jMock generate different messages,
Line743 matcher descriptions that complete the sentence “expected description but it
Line744 mismatch-description” will work with both libraries. That sentence completed
Line745 with the StringStartsWithMatcher’s descriptions would be something like:
Line746 expected a string starting with "Cheese" but it started with "Bananas"
Line747 To make the new matcher ﬁt seamlessly into JUnit and jMock, we also write
Line748 a factory method that creates an instance of the StringStartsWithMatcher.
Line749 public static Matcher<String> aStringStartingWith(String prefix ) {
Line750     return new StringStartsWithMatcher(prefix);
Line751 }
Line752 The point of the factory method is to make the test code read clearly, so
Line753 consider how it will look when used in an assertion or expectation.
Line754 And that’s all there is to writing a matcher.
Line755 345
Line756 A New Matcher Type
Line757 
Line758 
Line759 ---
Line760 
Line761 ---
Line762 **Page 346**
Line763 
Line764 This page intentionally left blank 
Line765 
Line766 
Line767 ---
Line768 
Line769 ---
Line770 **Page 347**
Line771 
Line772 Bibliography
Line773  
Line774 [Abelson96] Abelson, Harold and Gerald Sussman. Structure and Interpretation of
Line775 Computer Programs. MIT Press, 1996, ISBN 978-0262011532.
Line776 [Beck99] Beck, Kent. Extreme Programming Explained: Embrace Change. Addison-
Line777 Wesley, 1999, ISBN 978-0321278654.
Line778 [Beck02] Beck, Kent. Test Driven Development: By Example. Addison-Wesley, 2002, ISBN
Line779 978-0321146530.
Line780 [Begel08] Begel, Andrew and Beth Simon. “Struggles of New College Graduates in Their
Line781 First Software Development Job.” In: SIGCSE Bulletin, 40, no. 1 (March 2008):
Line782 226–230, ACM, ISSN 0097-8418.
Line783 [Cockburn04] Cockburn, Alistair. Crystal Clear: A Human-Powered Methodology for
Line784 Small Teams. Addison-Wesley Professional, October 29, 2004, ISBN 0201699478.
Line785 [Cockburn08] Cockburn, Alistair. Hexagonal Architecture: Ports and Adapters (“Object
Line786 Structural”). June 19, 2008, http://alistair.cockburn.us/ Hexagonal+architecture.
Line787 [Cohn05] Cohn, Mike. Agile Estimating and Planning. Prentice Hall, 2005, ISBN
Line788 978-0131479418.
Line789 [Demeyer03] Demeyer, Serge, Stéphane Ducasse, and Oscar Nierstrasz. Object-Oriented
Line790 Reengineering Patterns. http://scg.unibe.ch/download/oorp/.
Line791 [Evans03] Evans, Eric. Domain-Driven Design: Tackling Complexity in the Heart of
Line792 Software. Addison-Wesley, 2003, ISBN 978-0321125217.
Line793 [Feathers04] Feathers, Michael. Working Effectively with Legacy Code. Prentice Hall,
Line794 2004, ISBN 978-0131177055.
Line795 [Fowler99] Fowler, Martin. Refactoring: Improving the Design of Existing Code.
Line796 Addison-Wesley, 1999, ISBN 978-0201485677.
Line797 [Freeman04] Freeman, Steve, Tim Mackinnon, Nat Pryce, and Joe Walnes. “Mock
Line798 Roles, Not Objects.” In: Companion to the 19th ACM SIGPLAN Conference
Line799 on Object-Oriented Programming Systems, Languages, and Applications,
Line800 OOPLSA, Vancouver, BC, October 2004, New York: ACM, ISBN 1581138334,
Line801 http://portal.acm.org/citation.cfm?doid=1028664.1028765 .
Line802 [Freeman06] Freeman, Steve and Nat Pryce. “Evolving an Embedded Domain-Speciﬁc
Line803 Language in Java.” In: Companion to the 21st ACM SIGPLAN Conference on Object-
Line804 Oriented Programming Systems, Languages, and Applications, OOPLSA, Portland,
Line805 Oregon, October 2006, New York: ACM, http://www.jmock.org/oopsla06.pdf.
Line806 [Gall03] Gall, John. The Systems Bible: The Beginner’s Guide to Systems Large and Small.
Line807 General Systemantics Pr/Liberty, 2003, ISBN 978-0961825171.
Line808 [Gamma94] Gamma, Erich, Richard Helm, Ralph Johnson, and John Vlissides. Design
Line809 Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley, 1994.
Line810 347
Line811 
Line812 
Line813 ---
Line814 
Line815 ---
Line816 **Page 348**
Line817 
Line818 [Graham93] Graham, Paul. On Lisp. Prentice Hall, 1993, ISBN 0130305529,
Line819 http://www.paulgraham.com/onlisp.html.
Line820 [Hunt99] Hunt, Andrew and David Thomas. The Pragmatic Programmer: From Journey-
Line821 man to Master. Addison-Wesley Professional, October 30, 1999, ISBN 020161622X.
Line822 [Kay98] Kay, Alan. Email Message Sent to the Squeak Mailing List. October 10, 1998,
Line823 http://lists.squeakfoundation.org/pipermail/squeak-dev/1998-October/017019.html.
Line824 [Kerievsky04] Kerievsky, Joshua. Refactoring to Patterns. Addison-Wesley, 2004, ISBN
Line825 978-0321213358.
Line826 [Kernighan76] Kernighan, Brian and P. J. Plauger. Software Tools. Addison-Wesley, 1976,
Line827 ISBN 978-0201036695.
Line828 [Lieberherr88] Lieberherr, Karl, Ian Holland, and Arthur Riel. “Object-Oriented Program-
Line829 ming: An Objective Sense of Style.” In: OOPSLA, 23, no. 11 (1988): 323–334.
Line830 [LIFT] Framework for Literate Functional Testing. https://lift.dev.java.net/.
Line831 [Mackinnon00] Mackinnon, Tim, Steve Freeman, and Philip Craig. “Endo-Testing:
Line832 Unit Testing with Mock Objects.” In: Giancarlo Succi and Michele Marchesi,
Line833 Extreme Programming Examined, Addison-Wesley, 2001, pp. 287–301, ISBN 978-
Line834 0201710403.
Line835 [Magee06] Magee, Jeff and Jeff Kramer. Concurrency: State Models & Java Programs.
Line836 Wiley, 2006, ISBN 978-0470093559.
Line837 [Martin02] Martin, Robert C. Agile Software Development, Principles, Patterns, and
Line838 Practices. Prentice Hall, 2002, ISBN 978-0135974445.
Line839 [Meszaros07] Meszaros, Gerard. xUnit Test Patterns: Refactoring Test Code. Addison-
Line840 Wesley, 2007, ISBN 978-0131495050.
Line841 [Meyer91] Meyer, Betrand. Eiffel: The Language. Prentice Hall, 1991, ISBN 978-
Line842 0132479257.
Line843 [Mugridge05] Mugridge, Rick and Ward Cunningham. Fit for Developing Software:
Line844 Framework for Integrated Tests. Prentice Hall, 2005, ISBN 978-0321269348.
Line845 [Schuh01] Schuh, Peter and Stephanie Punke. ObjectMother: Easing Test Object Creation
Line846 In XP. XP Universe, 2001.
Line847 [Schwaber01] Schwaber, Ken and Mike Beedle. Agile Software Development with Scrum.
Line848 Prentice Hall, 2001, ISBN 978-0130676344.
Line849 [Shore07] Shore, James and Shane Warden. The Art of Agile Development. O’Reilly
Line850 Media, 2007, ISBN 978-0596527679.
Line851 [Wirfs-Brock03] Wirfs-Brock, Rebecca and Alan McKean. Object Design: Roles,
Line852 Responsibilities, and Collaborations. Addison-Wesley, 2003, ISBN 0201379430.
Line853 [Woolf98] Woolf, Bobby. “Null Object.” In: Pattern Languages of Program Design 3.
Line854 Edited by Robert Martin, Dirk Riehle, and Frank Buschmann. Addison-Wesley, 1998,
Line855 http://www.cse.wustl.edu/~schmidt/PLoP-96/woolf1.ps.gz.
Line856 [Yourdon79] Yourdon, Edward and Larry Constantine. Structured Design: Fundamentals
Line857 of a Discipline of Computer Program and Systems Design. Prentice Hall, 1979, ISBN
Line858 978-0138544713.
Line859 Bibliography 
Line860 348
Line861 
Line862 
Line863 ---
Line864 
Line865 ---
Line866 **Page 349**
Line867 
Line868 A
Line869 a(), jMock, 340
Line870 AbstractTableModel class, 152
Line871 acceptance tests, 4, 7–10
Line872 failing, 6–7, 39–40, 42, 271
Line873 for changed requirements, 40
Line874 for completed features, 40
Line875 for degenerate cases, 41
Line876 for new features, 6, 39–40, 105, 225
Line877 readability of, 42
Line878 Action interface, 341, 344
Line879 ActionListener interface, 185, 187
Line880 ActiveDirectory, 232
Line881 adapters, 48, 70–71, 284, 297
Line882 addSniper(), 180
Line883 addUserRequestListenerFor(), 187
Line884 adjustments, 52–53, 238
Line885 mocking, 58
Line886 @After annotation, 23, 96
Line887 @AfterClass annotation, 223
Line888 Agile Development, 35, 47, 81, 83, 205, 329
Line889 aliasing, 50
Line890 allOf(), Hamcrest, 340
Line891 allowances, 146, 277–279
Line892 allowing(), jMock, 145–146, 181, 211, 243,
Line893 278, 278, 339
Line894 an(), jMock, 340
Line895 announce(), jMock, 187
Line896 announceClosed(), 106–107, 176
Line897 Announcer class, 187, 192
Line898 aNonNull(), jMock, 340
Line899 ant build tool, 95
Line900 aNull(), jMock, 340
Line901 any(), Hamcrest, 340
Line902 anyOf(), Hamcrest, 340
Line903 Apache Commons IO library, 221
Line904 application model, 48
Line905 ApplicationRunner class, 85, 89–92,
Line906 106–107, 140, 153, 168, 175–177, 183,
Line907 207, 254
Line908 aRowChangedEvent(), 157, 162
Line909 ArrayIndexOutOfBoundsException, 217
Line910 aSniperThatIs(), 161–162, 278
Line911 assertColumnEquals(), 157
Line912 assertEquals(), JUnit, 21–22, 276
Line913 assertEventually(), 321–323, 326
Line914 assertFalse(), JUnit, 24, 255
Line915 assertions, 22, 254–255
Line916 extending, 343–345
Line917 failing, 24, 268
Line918 messages for, 268
Line919 naming, 86
Line920 narrowness of, 255, 275–276
Line921 quantity of, 252
Line922 vs. synchronizations, 326
Line923 vs. test setup, 211
Line924 assertIsSatisﬁed(), JUnit, 271
Line925 assertNull(), JUnit, 21–22
Line926 assertRowMatchesSnapshot(), 180
Line927 assertThat(), JUnit, 24–25, 253–255, 268,
Line928 276
Line929 assertTrue(), JUnit, 21–22, 24, 255
Line930 asynchrony, 87, 180, 216, 262
Line931 testing, 315–327
Line932 atLeast(), jMock, 127, 278, 339
Line933 atMost(), jMock, 339
Line934 AtomicBigCounter class, 311–312
Line935 AtomicInteger class, 309–310
Line936 attachModelListener(), Swing, 156–157
Line937 Auction interface, 62, 126–131, 136, 155,
Line938 193, 203
Line939 Auction Sniper, 75–226
Line940 bidding, 79, 84, 105–121, 126–131, 162
Line941 for multiple items, 175
Line942 stopping, 79, 205–213
Line943 connecting, 108, 111, 179, 183
Line944 disconnecting, 219–220
Line945 displaying state of, 97–98, 128, 144–146,
Line946 152–155, 159–160, 171, 323
Line947 failing, 215–217
Line948 joining auctions, 79, 84, 91, 94, 98–100,
Line949 179–181, 184–186, 197–199
Line950 losing, 79, 84, 91, 100–102, 125, 130,
Line951 164, 205–206
Line952 portfolio of, 199
Line953 refactoring, 191–203
Line954 Index
Line955  
Line956 349
Line957 
Line958 
Line959 ---
Line960 
Line961 ---
Line962 **Page 350**
Line963 
Line964 Auction Sniper (continued)
Line965 synchronizing, 106, 301
Line966 table model for, 149–152, 156–160, 166
Line967 translating messages from auction,
Line968 112–118, 139–142, 217
Line969 updating current price, 118–121
Line970 user interface of, 79, 84, 96–97, 149–173,
Line971 183–188, 207–208, 212, 316
Line972 walking skeleton for, 79, 83–88
Line973 when an auction is closed, 84, 94
Line974 winning, 79, 139–148, 162–164
Line975 auctionClosed(), 25, 58, 116–117,
Line976 119–120, 123–125
Line977 AuctionEvent class, 134–136
Line978 AuctionEventListener interface, 19, 26, 61,
Line979 113, 117, 120, 123–124, 141, 192–193,
Line980 217–220
Line981 auctionFailed(), 217–220
Line982 AuctionHouse interface, 196, 210
Line983 AuctionLogDriver class, 221, 224
Line984 AuctionMessageTranslator class, 25–27, 61,
Line985 112–118, 134–136, 154, 192, 195,
Line986 217–219, 222, 224, 226
Line987 AuctionMessageTranslatorTest class, 141
Line988 AuctionSearchStressTests class, 307–309
Line989 AuctionSniper class, 62, 123–134, 154–155,
Line990 172–173, 192, 198–199, 208, 210–212
Line991 AuctionSniperDriver class, 91, 153, 168,
Line992 184, 207, 254
Line993 AuctionSniperEndToEndTest class, 85, 152,
Line994 183
Line995 AuctionSniperTest class, 218
Line996 B
Line997 @Before annotation, 23
Line998 between(), jMock, 339
Line999 bidsHigherAndReportsBiddingWhenNew-
Line1000 PriceArrives(), 127, 143
Line1001 “Big Design Up Front,” 35
Line1002 BlockingQueue class, 93
Line1003 breaking out technique, 59–61, 136
Line1004 budding off technique, 59, 61–62, 209
Line1005 build
Line1006 automated, 9, 36–37, 95
Line1007 features included in, 8
Line1008 from the start of a project, 31
Line1009 build(), 258–261
Line1010 Builder pattern, 66, 337
Line1011 builders. See test data builders, 254
Line1012 bundling up technique, 59–60, 62, 154
Line1013 C
Line1014 C# programming language, 225
Line1015 cannotTranslateMessage(), 222–223
Line1016 CatalogTest class, 21, 23
Line1017 Chat class, 112, 115, 129–130, 185, 192,
Line1018 219
Line1019 encapsulating, 193–195
Line1020 chatDisconnectorFor(), 220, 226
Line1021 ChatManager class, 101, 129
Line1022 ChatManagerListener interface, 92
Line1023 check(), WindowLicker, 187
Line1024 checking(), jMock, 210, 337
Line1025 classes, 14
Line1026 coherent, 12
Line1027 context-independent, 55
Line1028 encapsulating collections into, 136
Line1029 helper, 93
Line1030 hierarchy of, 16, 67
Line1031 internal features of, 237
Line1032 loosely coupled, 11–12
Line1033 mocking, 223–224, 235–237
Line1034 naming, 63, 159–160, 238, 285, 297
Line1035 tightly coupled, 12
Line1036 Clock interface, 230–232
Line1037 code
Line1038 adapting, 172
Line1039 assumptions about, 42
Line1040 cleaning up, 60, 118, 125, 131, 137, 245,
Line1041 262–264
Line1042 compiling, 136
Line1043 declarative layer of, 65
Line1044 difﬁcult to test, 44, 229
Line1045 external quality of, 10–11
Line1046 implementation layer of, 65
Line1047 internal quality of, 10–11, 60
Line1048 loosely coupled, 11–12
Line1049 maintenance of, 12, 125
Line1050 readability of, 51, 162, 173, 226, 247
Line1051 reimplementing, 60
Line1052 tightly coupled, 12
Line1053 code smells, 63, 181
Line1054 cohesion, 11–12
Line1055 collaborators, 16, 279
Line1056 collections
Line1057 encapsulating, 136
Line1058 vs. domain types, 213
Line1059 commands, 78, 278
Line1060 commit(), 279
Line1061 communication patterns, 14, 58
Line1062 communication protocols, 58, 63
Line1063 Index
Line1064 350
Line1065 
Line1066 
Line1067 ---
Line1068 
Line1069 ---
Line1070 **Page 351**
Line1071 
Line1072 ComponentDriver, 90
Line1073 “composite simpler than the sum of its
Line1074 parts,” 53–54, 60, 62
Line1075 concurrency, 301–306, 309, 313–316
Line1076 connect(), Smack, 100
Line1077 connection(), 100
Line1078 Connextra, 330–332
Line1079 constants, 255
Line1080 constructors
Line1081 bloated, 238–242
Line1082 real behavior in, 195
Line1083 container-managed transactions, 293
Line1084 containsTotalSalesFor(), 264
Line1085 context independence, 54–57, 233, 305
Line1086 CountDownLatch class, 194
Line1087 coupling, 11–12
Line1088 CRC cards, 16, 186, 333
Line1089 createChat(), Smack, 129
Line1090 Crystal Clear, 1
Line1091 currentPrice(), 118–120, 123, 141,
Line1092 162–163
Line1093 currentTimeMillis(), java.lang.System,
Line1094 230
Line1095 customer tests. See acceptance tests
Line1096 D
Line1097 DAO (Data Access Object), 297
Line1098 database tests. See persistence tests
Line1099 DatabaseCleaner class, 291–292
Line1100 databases
Line1101 cleaning up before testing, 290–292
Line1102 operations with active transactions in, 300
Line1103 data-driven tests, 24
Line1104 date manipulation, 230–233
Line1105 “debug hell,” 267
Line1106 Decorator pattern, 168, 300
Line1107 Defect exception, 165
Line1108 dependencies, 52–53, 126
Line1109 breaking in unit tests, 233
Line1110 explicit, 14
Line1111 hidden, 273
Line1112 implicit, 57, 232–233
Line1113 knowing about, 231
Line1114 loops of, 117, 129, 192
Line1115 mocking, 58
Line1116 on user interface components, 113
Line1117 quantity of, 57, 241–242, 273
Line1118 scoping, 62
Line1119 using compiler for navigating, 225
Line1120 dependency injections, 330
Line1121 deployment, 4, 9
Line1122 automated, 35–37
Line1123 from the start of a project, 31
Line1124 importance for testing, 32
Line1125 describeMismatch(), Hamcrest, 343–345
Line1126 describeTo(), Hamcrest, 343–345
Line1127 design
Line1128 changing, 172
Line1129 clarifying, 235
Line1130 feedback on, 6
Line1131 quality of, 273
Line1132 DeterministicExecutor class, 303–304
Line1133 development
Line1134 from inputs to outputs, 43, 61
Line1135 incremental, 4, 36, 73, 79, 136, 201, 303
Line1136 iterative, 4
Line1137 of user interface, 183
Line1138 working compromises during, 90, 95
Line1139 disconnect(), Smack, 111
Line1140 disconnectWhenUICloses(), 111, 179
Line1141 domain model, 15, 48, 59, 71, 290
Line1142 domain types, 213, 262, 269
Line1143 domain-speciﬁc language, embedded in Java,
Line1144 332
Line1145 “Don’t Repeat Yourself” principle, 248
Line1146 duplication, 262–264, 273, 275
Line1147 Dynamock library, 332
Line1148 E
Line1149 Eclipse development environment, 119
Line1150 encapsulation, 49–50, 55
Line1151 end-to-end tests, 8–10
Line1152 asynchronous, 87
Line1153 brittleness of, 87
Line1154 early, 32–33
Line1155 failing, 87
Line1156 for event-based systems, 87
Line1157 for existing systems, 33, 37
Line1158 on synchronization, 313
Line1159 running, 11
Line1160 simulating input and output events, 43
Line1161 slowness of, 87, 300
Line1162 EntityManager class, 279, 297, 299
Line1163 EntityManagerFactory class, 279
Line1164 EntityTransaction class, 279
Line1165 equal(), jMock, 340
Line1166 equals(), java.lang.Object, 154
Line1167 equalTo(), Hamcrest, 322
Line1168 error messages. See failure messages
Line1169 event-based systems, 86–87
Line1170 351
Line1171 Index
Line1172 
Line1173 
Line1174 ---
Line1175 
Line1176 ---
Line1177 **Page 352**
Line1178 
Line1179 events, 78
Line1180 external, 71, 326–327
Line1181 listening for, 316–317, 323–325
Line1182 processed in sequence, 325–326
Line1183 exactly(), jMock, 338
Line1184 exceptions, 22
Line1185 catching, 253–254
Line1186 on hidden threads, 302
Line1187 runtime, 165
Line1188 with helpful messages, 330
Line1189 Executor interface, 303, 305
Line1190 “Expect Unexpected Changes” principle, 45
Line1191 Expectation jMock class, 64
Line1192 ExpectationCounter jMock class, 330
Line1193 expectations, 18, 27, 64–66, 146, 254–255,
Line1194 277–279, 338
Line1195 blocks of, 337, 339
Line1196 checking after test’s body, 271
Line1197 clear descriptions of, 25
Line1198 narrowness of, 255, 277–283
Line1199 order of, 128, 282, 341–342
Line1200 quantity of, 242–244, 252
Line1201 specifying actions to perform, 341
Line1202 Expectations jMock class, 66, 337, 340
Line1203 ExpectationSet jMock class, 330
Line1204 ExpectationValue jMock class, 330
Line1205 expectFailureWithMessage(), 222
Line1206 expectSniperToFailWhenItIs(), 219, 253
Line1207 F
Line1208 failed(), 219
Line1209 failure messages, 268–269, 276
Line1210 clearness of, 42
Line1211 self-explanatory, 24–25, 343
Line1212 failures, 41
Line1213 detecting, 217–218
Line1214 diagnostics for, 267–273, 297, 302–307,
Line1215 332
Line1216 displaying, 218–219
Line1217 handling, 215–226
Line1218 messages about, 255
Line1219 recording, 221–225, 291
Line1220 writing down while developing, 41
Line1221 FakeAuctionServer class, 86, 89, 92–95,
Line1222 107–110, 120, 176, 194, 254, 276
Line1223 FeatureMatcher Hamcrest class, 162, 178
Line1224 feedback, 4, 229, 233
Line1225 from automated deployment, 35–36
Line1226 incremental, 300
Line1227 loops of, 4–5, 8, 40
Line1228 on design, 6, 299
Line1229 on failure cases, 41
Line1230 on implementations, 6
Line1231 rapid, 317
Line1232 Findbugs, 313
Line1233 ﬁxtures, 23
Line1234 functional tests. See acceptance tests
Line1235 G
Line1236 garbage collection, 23, 91, 101, 192–194
Line1237 getBody(), Smack, 222
Line1238 getColumnCount(), Swing, 158
Line1239 getValueAt(), Swing, 158
Line1240 H
Line1241 Hamcrest library, 21, 24–25, 95, 268, 274,
Line1242 296, 322, 333, 340, 343–345
Line1243 hasColumnTitles(), 169
Line1244 hasEnoughColumns(), 156–157
Line1245 hashCode(), java.lang.Object, 154
Line1246 hasProperty(), Hamcrest, 178
Line1247 hasReceivedBid(), 106–107
Line1248 hasReceivedJoinRequestFrom(), 109, 176
Line1249 hasReceivedJoinRequestFromSniper(),
Line1250 106–108
Line1251 hasShownSniperHasWon(), 323
Line1252 hasShownSniperIsBidding(), 106, 110
Line1253 hasShownSniperIsLosing(), 206–207
Line1254 hasShownSniperIsWinning(), 140, 176, 323
Line1255 hasTitle(), 169
Line1256 helper methods, 7, 51, 66, 162, 166, 210,
Line1257 226, 253, 263, 280
Line1258 naming, 51, 162
Line1259 Hibernate, 48, 289, 294
Line1260 HTTP (HyperText Transfer Protocol), 81
Line1261 I
Line1262 IDEs
Line1263 ﬁlling in missing methods on request, 119
Line1264 navigation in, 114
Line1265 IETF (Internet Engineering Task Force), 77
Line1266 ignoring(), jMock, 145, 278–279, 339
Line1267 ignoringAuction(), 219
Line1268 IllegalArgumentException, 22
Line1269 implementations
Line1270 feedback on, 6
Line1271 independent of context, 244
Line1272 null, 130, 136, 180, 218
Line1273 Index
Line1274 352
Line1275 
Line1276 
Line1277 ---
Line1278 
Line1279 ---
Line1280 **Page 353**
Line1281 
Line1282 index cards
Line1283 for technical tasks to be addressed, 41
Line1284 for to-do lists, 80–81, 103, 120–121,
Line1285 130–131, 148, 171, 182, 201,
Line1286 211–212, 225
Line1287 information hiding, 49, 55–56
Line1288 initializers, 23
Line1289 inSequence(), jMock, 338, 341
Line1290 instanses, 237–238
Line1291 integration tests, 9–10, 186–188
Line1292 and threads, 71
Line1293 difﬁcult to code, 44
Line1294 for adapters, 70
Line1295 for persistence implementations, 300
Line1296 passing, 40
Line1297 speed of, 300
Line1298 IntelliJ IDEA, 119, 250
Line1299 interface discovery, 19
Line1300 interfaces, 14, 58, 61
Line1301 callback, 71
Line1302 implementing, 63–64
Line1303 mocking, 235
Line1304 naming, 63–64, 237, 297
Line1305 narrowness of, 63
Line1306 pulling, 61, 63
Line1307 refactoring, 63–64
Line1308 relationships with, 63
Line1309 segregating, 236
Line1310 invocations
Line1311 allowed, 27, 146
Line1312 constrained, 342
Line1313 counting, 338–339
Line1314 expected, 27, 146
Line1315 number of, 27
Line1316 order of, 279–282, 341
Line1317 invokeAndWait(), Swing, 100, 180
Line1318 invokeLater(), Swing, 100
Line1319 isForSameItemAs(), 181
Line1320 isSatisﬁed(), WindowLicker, 320–321
Line1321 Item class, 209–211, 213
Line1322 iteration zero, 83, 102
Line1323 J
Line1324 Jabber. See XMPP
Line1325 Java programming language, 21
Line1326 arrays in, 177
Line1327 collections in, 179
Line1328 logging framework in, 223
Line1329 method overloading in, 261
Line1330 package loops in, 191
Line1331 synchronization errors in, 313
Line1332 syntax noise of, 253
Line1333 using compiler to navigate dependencies,
Line1334 225
Line1335 Java EE (Java Platform, Enterprise Edition),
Line1336 293–294, 301
Line1337 Java Servlet API, 330
Line1338 JAXB (Java API for XML Binding), 289
Line1339 JButton Swing component, 185
Line1340 JDBC (Java Database Connectivity), 294
Line1341 JDO (Java Data Objects), 289
Line1342 JFormattedTextField Swing component, 208
Line1343 JFrame Swing component, 96
Line1344 JFrameDriver WindowLicker class, 91
Line1345 JIDs (Jabber IDs), 77, 197
Line1346 JLabel Swing component, 150
Line1347 jMock library, 24–27, 274, 332
Line1348 allowances in, 146
Line1349 double braces in, 337
Line1350 expectations in, 25, 64–66, 146
Line1351 extensions to, 162
Line1352 generating messages in, 345
Line1353 states in, 145
Line1354 using for stress tests, 307
Line1355 verifying mock objects in, 24
Line1356 version 2, 21, 25–27, 333, 335–342
Line1357 JMS (Java Messaging Service), 292
Line1358 JMSTransactor class, 292
Line1359 joinAuction(), 100, 131–132, 142,
Line1360 180–182, 187–188, 192, 208
Line1361 JPA (Java Persistence API), 279, 289, 294
Line1362 persistence identiﬁers in, 295
Line1363 JTA (Java Transaction API), 292
Line1364 JTable Swing component, 52, 149–157, 170
Line1365 JTATransactor class, 292–293
Line1366 JTextField Swing component, 185
Line1367 JUnit library, 84, 274, 332–333
Line1368 generating messages in, 345
Line1369 new instances for each test in, 22, 117
Line1370 version 4.5, 24
Line1371 version 4.6, 21, 335
Line1372 JUnit4Mockery jMock class, 336
Line1373 L
Line1374 Law of Demeter. See “Tell, Don’t Ask”
Line1375 principle
Line1376 Lisp programming language, 66
Line1377 literals. See values
Line1378 locks, 302, 318
Line1379 log ﬁles, 221–225, 291
Line1380 cleaning up before testing, 221
Line1381 generating, 223
Line1382 353
Line1383 Index
Line1384 
Line1385 
Line1386 ---
Line1387 
Line1388 ---
Line1389 **Page 354**
Line1390 
Line1391 Logger class, 223–224, 237
Line1392 logging, 233–235
Line1393 amount of, 235
Line1394 diagnostic, 233–235
Line1395 isolated in a separate class, 226
Line1396 LoggingXMPPFailureReporter class, 223–224
Line1397 LTSA tool, 302, 313
Line1398 M
Line1399 Main class, 91, 101, 108, 117–118, 123, 126,
Line1400 132–134, 142, 168, 178–180, 183, 185,
Line1401 188–203
Line1402 matchmaker role of, 191
Line1403 main(), 91, 96
Line1404 MainWindow class, 96, 100, 113, 134, 151,
Line1405 156, 166–167, 185–187, 199, 208–209
Line1406 MainWindowTest class, 186, 209
Line1407 makeControls(), 184–185
Line1408 Mars Climate Orbiter disaster, 59
Line1409 Matcher interface, 25, 268, 343–345
Line1410 matchers, 24–25, 95, 155, 157, 276, 322,
Line1411 339–340
Line1412 combining, 24
Line1413 custom, 25, 178, 296, 340, 343–345
Line1414 reversing, 24
Line1415 stateless, 344
Line1416 Matchers Hamcrest class, 340
Line1417 matches(), Hamcrest, 343
Line1418 meetings, 4
Line1419 MessageHandler class, 217
Line1420 MessageListener interface, 93–94, 99,
Line1421 112–115, 129, 219
Line1422 messages, 13, 17
Line1423 between objects, 50, 58
Line1424 creating and checking in the same
Line1425 construct, 109
Line1426 parsing, 118–120
Line1427 See also failure messages
Line1428 methods, 13
Line1429 calling, 65
Line1430 order of, 128
Line1431 expected, 339–340
Line1432 factory, 257–258, 260–261
Line1433 getter, 329–330
Line1434 grouping together, 176
Line1435 ignoring, 279
Line1436 naming, 86, 173, 250
Line1437 overloading, 261
Line1438 side effects of, 51
Line1439 “sugar,” 65–66
Line1440 testing, 43
Line1441 See also helper methods
Line1442 MissingValueException, 218
Line1443 mock objects, 18–20, 25–27
Line1444 creating, 336
Line1445 for third-party code, 69–71, 157, 300
Line1446 history of, 329–333
Line1447 invocation order of, 279–282
Line1448 naming, 336
Line1449 to visualize protocols, 58, 61
Line1450 mockery, 20, 25
Line1451 Mockery jMock class, 26, 64, 66, 307, 336
Line1452 mocking
Line1453 adjustments, 58
Line1454 classes, 223–224, 235–237
Line1455 dependencies, 58
Line1456 interfaces, 235
Line1457 notiﬁcations, 58
Line1458 peers, 58
Line1459 returned types, 279
Line1460 third-party code, 237
Line1461 values, 237–238
Line1462 Moon program, 41
Line1463 multithreading. See threads
Line1464 N
Line1465 .Net, 22, 232
Line1466 “Never Pass Null between Objects”
Line1467 principle, 274
Line1468 never(), jMock, 339
Line1469 NMock library, 332
Line1470 not(), Hamcrest, 24, 340
Line1471 notiﬁcations, 52–53, 126, 192
Line1472 capturing, 318–320
Line1473 mocking, 58
Line1474 order of, 280
Line1475 recording, 324
Line1476 notifiesAuctionClosedWhenCloseMessage-
Line1477 Received(), 114
Line1478 notifiesAuctionFailedWhenBadMessage-
Line1479 Received(), 217
Line1480 notifiesAuctionFailedWhenEventType-
Line1481 Missing(), 218
Line1482 notifiesBidDetailsWhenCurrentPrice-
Line1483 MessageReceivedFromOtherBidder(),
Line1484 141
Line1485 notifiesBidDetailsWhenCurrentPrice-
Line1486 MessageReceivedFromSniper(), 141
Line1487 notToBeGCd ﬁeld, 101, 179, 197, 200, 203
Line1488 NullPointerException, 53, 274
Line1489 NUnit library, 22, 117, 332
Line1490 Index
Line1491 354
Line1492 
Line1493 
Line1494 ---
Line1495 
Line1496 ---
Line1497 **Page 355**
Line1498 
Line1499 O
Line1500 object mother pattern, 257–258
Line1501 object-oriented programming, 13, 329
Line1502 objects
Line1503 abstraction level of, 57
Line1504 bringing out relationships between, 236
Line1505 collaborating, 18–20, 52–53, 58, 60–62,
Line1506 186
Line1507 communicating, 13–14, 50, 58, 244–245
Line1508 composite, 53–54
Line1509 context-independent, 54–55, 233
Line1510 created by builders, 259–260
Line1511 difﬁcult to decouple, 273
Line1512 mutable, 14
Line1513 sharing references to, 50
Line1514 naming, 62, 244
Line1515 null, 22, 115, 130, 242
Line1516 observable invariants with respect to
Line1517 concurrency of, 306
Line1518 passive, 311–312
Line1519 persistent, 298–299
Line1520 simplifying, 55
Line1521 single responsibility of, 51–52
Line1522 states of, 13, 59, 145–146, 281–283, 299,
Line1523 306, 342
Line1524 subordinate, 254, 291–292, 311
Line1525 tracer, 270–271
Line1526 validity of, 53
Line1527 vs. values, 13–14, 51, 59
Line1528 web of, 13, 64–65
Line1529 oneOf(), jMock, 278, 337–338
Line1530 Openﬁre, 86, 89, 95
Line1531 ORM (Object/Relational Mapping), 289,
Line1532 297, 299
Line1533 P
Line1534 packages
Line1535 loops of, 191
Line1536 single responsibility of, 52
Line1537 pair programming, 4
Line1538 patterns, naming after, 297
Line1539 peers, 50
Line1540 mocking, 58
Line1541 types of, 52–53
Line1542 persistence tests, 289–300
Line1543 and transactions, 292–294
Line1544 cleaning up at the start, 291
Line1545 failure diagnostics in, 297
Line1546 isolating from one another, 290–292
Line1547 round-trip, 297–300
Line1548 slowness of, 300
Line1549 Poller class, 320–321
Line1550 polling for changes, 317, 320–321, 323–325
Line1551 PortfolioListener interface, 199
Line1552 ports, 48
Line1553 “ports and adapters” architecture, 48, 201,
Line1554 284, 297
Line1555 PriceSource enumeration, 141, 148
Line1556 Probe interface, 320–322
Line1557 probing a system, 315, 320–322
Line1558 processMessage(), Smack, 114–115,
Line1559 135–136, 217, 219
Line1560 production environment, 95
Line1561 programming styles, 51
Line1562 progress measuring, 4, 40
Line1563 PropertyMatcher Hamcrest class, 178
Line1564 Q
Line1565 queries, 278
Line1566 R
Line1567 receivesAMessageMatching(), 108
Line1568 redesign, 7
Line1569 refactoring, 5–7
Line1570 code difﬁcult to test, 44–45
Line1571 importance of, during TDD, 225–226
Line1572 incremental, 202
Line1573 writing down while developing, 41
Line1574 reference types, 269
Line1575 regression suites, 6, 40
Line1576 regression tests, 5
Line1577 releases, 4, 9
Line1578 planning, 81
Line1579 to a production system, 35
Line1580 removeMessageListener(), Smack, 220
Line1581 reportPrice(), 106–107, 176
Line1582 reportsInvalidMessage(), 216, 221
Line1583 reportsLostIfAuctionClosesImmediately(),
Line1584 145
Line1585 reportsLostIfAuctionClosesWhenBidding(),
Line1586 146
Line1587 repository pattern, 297
Line1588 resetLogging(), 223
Line1589 responsibilities, 16, 171, 220, 222
Line1590 quantity of, 61, 240–241, 332
Line1591 See also “single responsibility” principle
Line1592 reverting changes, 267
Line1593 rock climbing, 202
Line1594 roles, 16
Line1595 rollback(), 279
Line1596 rolling back, 267
Line1597 Ruby programming language, 331
Line1598 355
Line1599 Index
Line1600 
Line1601 
Line1602 ---
Line1603 
Line1604 ---
Line1605 **Page 356**
Line1606 
Line1607 Rule annotation, 24
Line1608 RuntimeException, 255, 277
Line1609 runUntilIdle(), 304
Line1610 @RunWith annotation, 23, 26, 336
Line1611 S
Line1612 safelyAddItemToModel(), 180, 188
Line1613 same(), jMock, 340
Line1614 sample(), WindowLicker, 320–321
Line1615 scheduled activities, 326–327
Line1616 Scrum projects, 1
Line1617 SelfDescribing interface, 343
Line1618 sendInvalidMessageContaining(), 216
Line1619 Sequence jMock class, 341–342
Line1620 sequences, 279–282, 341–342
Line1621 servlets, 301, 311
Line1622 setImposteriser(), jMock, 223
Line1623 setStatusText(), 166
Line1624 [Setup] methods, 22
Line1625 showsSniperHasFailed(), 216
Line1626 showsSniperHasWonAuction(), 140, 176
Line1627 showsSniperStatus(), 91–92
Line1628 “single responsibility” principle, 51–52, 113,
Line1629 123, 125, 220, 222
Line1630 SingleMessageListener class, 93–94,
Line1631 107–108
Line1632 singleton pattern, 50, 230
Line1633 Smack library, 86
Line1634 exceptions in, 217
Line1635 threads in, 93, 301
Line1636 Smalltalk programming language
Line1637 cascade, 258, 330, 332
Line1638 programming style compared to Java, 330
Line1639 Sniper application. See Auction Sniper
Line1640 Sniper class, 62
Line1641 sniperAdded(), 203
Line1642 sniperBidding(), 126–128, 155, 160–162
Line1643 SniperCollector class, 62, 198–199, 245
Line1644 sniperForItem(), 198
Line1645 SniperLauncher class, 62, 197–199, 210
Line1646 SniperListener interface, 124–126, 133,
Line1647 154–155, 163–164, 168
Line1648 sniperLost(), 125, 147, 164
Line1649 sniperMakesAHigherBidButLoses(), 139
Line1650 SniperPortfolio class, 199–203
Line1651 sniperReportsInvalidAuctionMessageAnd-
Line1652 StopsRespondingToEvents(), 216
Line1653 SniperSnapshot class, 159–164, 173,
Line1654 180–181, 198–199, 211, 219, 278
Line1655 SnipersTableModel class, 149, 151–152, 156,
Line1656 166, 168, 170–171, 180–182, 185,
Line1657 197–201, 207
Line1658 SniperState class, 155, 158–161, 207, 216,
Line1659 278
Line1660 sniperStateChanged(), 156–164, 278
Line1661 SniperStateDisplayer class, 133, 147, 155,
Line1662 167–168
Line1663 sniperWinning(), 143, 162–163
Line1664 sniperWinsAnAuctionByBiddingHigher(),
Line1665 139
Line1666 sniperWon(), 147, 164
Line1667 Spring, 294
Line1668 startBiddingFor(), 184
Line1669 startBiddingIn(), 177
Line1670 startBiddingWithStopPrice(), 206–207
Line1671 startSellingItem(), 92, 176
Line1672 startSniper(), 183–184
Line1673 startsWith(), Hamcrest, 343–345
Line1674 state machines, 279–282, 342
Line1675 state transition diagrams, 212
Line1676 States jMock class, 146, 198, 281–283
Line1677 static analysis tools, 313
Line1678 stop price, 80, 205–213
Line1679 stress tests, 306–313
Line1680 failing, 308–309, 313
Line1681 on event processing order, 326
Line1682 on passive objects, 311–312
Line1683 running in different environments, 313
Line1684 strings
Line1685 checking if starts with a given preﬁx,
Line1686 343–345
Line1687 comparing, 14
Line1688 vs. domain types, 213, 262, 269
Line1689 StringStartsWithMatcher Hamcrest class,
Line1690 345
Line1691 stubs, 84, 243, 277, 339
Line1692 success cases, 41
Line1693 Swing
Line1694 manipulating features in, 90
Line1695 testing, 86–87
Line1696 threads in, 123, 133, 180, 301
Line1697 SwingThreadSniperListener interface, 168,
Line1698 197, 199
Line1699 Synchroniser jMock class, 307–308,
Line1700 312–313
Line1701 synchronizations, 301–314
Line1702 errors in, 302
Line1703 testing, 302, 306–310, 313
Line1704 vs. assertions, 326
Line1705 Index
Line1706 356
Line1707 
Line1708 
Line1709 ---
Line1710 
Line1711 ---
Line1712 **Page 357**
Line1713 
Line1714 system
Line1715 application model of, 48
Line1716 changing behavior of, 48, 55
Line1717 concurrency architecture of, 301–302
Line1718 maintainability of, 47
Line1719 public drawings of, during development,
Line1720 34
Line1721 returning to initial state after a test, 323
Line1722 simplifying, 112
Line1723 system tests. See acceptance tests
Line1724 T
Line1725 tableChanged(), Swing, 157, 181
Line1726 TableModel class, 149, 168–171
Line1727 TableModelEvent class, 157, 180–181
Line1728 TableModelListener class, 156–157
Line1729 task runners, 303
Line1730 TDD (Test-Driven Development), 1, 5, 229
Line1731 cycle of, 6, 39–45, 271–272
Line1732 for existing systems, 37
Line1733 golden rule of, 6
Line1734 kick-starting, 31–37
Line1735 sustainable, 227–285
Line1736 [TearDown] methods, 22
Line1737 “Tell, Don’t Ask” principle, 17, 54, 245
Line1738 template methods, 344
Line1739 test data builders, 238, 258–259
Line1740 calling within transactions, 300
Line1741 combining, 261, 300
Line1742 creating similar objects with, 259–260
Line1743 lists of, 298–299
Line1744 removing duplication with, 262–264
Line1745 wrapping up in factory methods, 261
Line1746 test runner, 23–24
Line1747 JMock, 26
Line1748 Parameterized, 24
Line1749 “test smells,” 229, 235, 248
Line1750 beneﬁts of listening to, 244–246
Line1751 @Test annotation, 22
Line1752 TestDox convention, 249–250
Line1753 Test-Driven Development. See TDD
Line1754 tests
Line1755 against fake services, 84, 88, 93
Line1756 against real services, 32, 88, 93
Line1757 asynchronous, 315–327
Line1758 at the beginning of a project, 36, 41
Line1759 brittleness of, 229, 255, 257, 273
Line1760 cleaning up, 245, 248, 273
Line1761 decoupling from tested objects, 278
Line1762 dependencies in, 275
Line1763 explicit constraints in, 280
Line1764 failing, 267–273
Line1765 ﬂexibility of, 273–285
Line1766 ﬂickering, 317
Line1767 focused, 273, 277, 279, 279
Line1768 for late integration, 36
Line1769 hierarchy of, 9–10
Line1770 maintaining, 247, 273–274
Line1771 naming, 44, 248–250, 252, 264, 268, 326
Line1772 readability of, 247–257, 273, 280
Line1773 repeatability of, 23
Line1774 runaway, 322–323
Line1775 running, 6
Line1776 sampling, 316–317, 320–325
Line1777 self-explanatory, 274–275
Line1778 separate packages for, 114
Line1779 size of, 45, 268
Line1780 states of, 283
Line1781 synchronizing, 301–314, 317
Line1782 with background threads, 312–313
Line1783 tightly coupled, 273
Line1784 triggering detectable behavior, 325
Line1785 writing, 6
Line1786 backwards, 252
Line1787 in a standard form, 251–252
Line1788 See also acceptance tests, end-to-end tests,
Line1789 integration tests, persistence tests,
Line1790 unit tests
Line1791 textFor(), 166
Line1792 “the simplest thing that could possibly
Line1793 work,” 41
Line1794 then(), jMock, 281–282, 338, 342
Line1795 third-party code, 69–72
Line1796 abstractions over, 10
Line1797 mocking, 69–71, 157, 237, 300
Line1798 patching, 69
Line1799 testing integration with, 186–188, 289
Line1800 value types from, 71
Line1801 Thor Automagic, 12
Line1802 threads, 71, 301–315
Line1803 scheduling, 313
Line1804 three-point contact, 202
Line1805 time boxes, 4
Line1806 Timeout class, 318, 322
Line1807 timeouts, 230, 312–313, 316–318
Line1808 timestamps, 276
Line1809 toString(), java.lang.Object, 154
Line1810 tracer object, 270–271
Line1811 “train wreck” code, 17, 50–51, 65
Line1812 transaction management, 294
Line1813 transactors, 292–293
Line1814 translate(), 217
Line1815 357
Line1816 Index
Line1817 
Line1818 
Line1819 ---
Line1820 
Line1821 ---
Line1822 **Page 358**
Line1823 
Line1824 translatorFor(), 220, 226, 253
Line1825 TypeSafeMatcher<String> Hamcrest class,
Line1826 344
Line1827 U
Line1828 unit tests, 4, 9
Line1829 against static global objects, 234
Line1830 and threads, 301–314
Line1831 at the beginning of a project, 43
Line1832 breaking dependencies in, 233
Line1833 brittleness of, 245
Line1834 difﬁcult to code, 44
Line1835 failing, 8
Line1836 isolating from each other, 22, 117
Line1837 length of, 245–246
Line1838 limiting scope of, 57
Line1839 naming, 114, 141
Line1840 on behavior, not methods, 43
Line1841 on collaborating objects, 18–20
Line1842 on synchronization, 302, 306–310, 313
Line1843 passing, 40
Line1844 readability of, 245–246
Line1845 simplifying, 62
Line1846 speed of, 300, 312
Line1847 structure of, 335–342
Line1848 writing, 11
Line1849 Unix, 66
Line1850 User Experience community, 81, 212
Line1851 user interface
Line1852 conﬁguring through, 242
Line1853 dependencies on, 113
Line1854 handling user requests, 186
Line1855 support logging in, 233
Line1856 working on parallel to development, 183,
Line1857 212
Line1858 UserRequestListener interface, 186–188,
Line1859 208–209, 213
Line1860 V
Line1861 value types, 59–60, 141
Line1862 from third-party code, 71
Line1863 helper, 59
Line1864 naming, 173
Line1865 placeholder, 59, 209
Line1866 public ﬁnal ﬁelds in, 154
Line1867 vs. values, 59
Line1868 with generics, 136
Line1869 valueIn(), 166–167
Line1870 ValueMatcherProbe WindowLicker class, 187
Line1871 values, 255–256
Line1872 comparing, 22
Line1873 expected, 127
Line1874 immutable, 50, 59
Line1875 mocking, 237–238
Line1876 mutable, 50
Line1877 obviously canned, 270
Line1878 self-describing, 269, 285
Line1879 side effects of, 51
Line1880 vs. objects, 13–14, 51, 59
Line1881 variables, 255–256
Line1882 global, 50
Line1883 naming, 209, 330
Line1884 W
Line1885 waitForAnotherAuctionEvent(), 216
Line1886 waitUntil(), 326
Line1887 walking skeleton, 32–37
Line1888 for Auction Sniper, 79, 83–88
Line1889 when(), jMock, 281–282, 338, 342
Line1890 whenAuctionClosed(), 164–165
Line1891 will(), jMock, 338, 341
Line1892 WindowAdapter class, 134
Line1893 WindowLicker library, 24, 86–87, 186–187,
Line1894 254, 316
Line1895 controlling Swing components in, 90–91
Line1896 error messages in, 96
Line1897 with(), jMock, 339–340
Line1898 overloaded, 261
Line1899 X
Line1900 XmlMarshaller class, 284–285
Line1901 XmlMarshallerTest class, 284
Line1902 XMPP (eXtensible Messaging and Presence
Line1903 Protocol), 76–77, 105, 203
Line1904 messages in, 301
Line1905 reliability of, 81
Line1906 security of, 81
Line1907 XMPP message brokers, 84, 86, 95
Line1908 XMPPAuction class, 62, 131–132, 192–197,
Line1909 203, 224
Line1910 XMPPAuctionException, 224
Line1911 XMPPAuctionHouse class, 62, 196–197, 203,
Line1912 224
Line1913 XMPPConnection class, 195–197
Line1914 XMPPException, 130
Line1915 XMPPFailureReporter class, 222–223, 226
Line1916 XP (Extreme Programming), 1, 41, 331
Line1917 XStream, 289
Line1918 XTC (London Extreme Tuesday Club), 331
Line1919 Index
Line1920 358
Line1921 
Line1922 
Line1923 ---
Line1924 
Line1925 ---
Line1926 **Page 359**
Line1927 
Line1928 InformIT is a brand of Pearson and the online presence 
Line1929 for the world’s leading technology publishers. It’s your source 
Line1930 for reliable and qualified content and knowledge, providing 
Line1931 access to the top brands, authors, and contributors from 
Line1932 the tech community.
Line1933 informIT.com
Line1934 THE TRUSTED TECHNOLOGY LEARNING SOURCE
Line1935 LearnIT at InformIT
Line1936 Looking for a book, eBook, or training video on a new technology? Seeking 
Line1937 timely and relevant information and tutorials? Looking for expert opinions, 
Line1938 advice, and tips?  InformIT has the solution.
Line1939 •
Line1940 Learn about new releases and special promotions by 
Line1941 subscribing to a wide variety of newsletters. 
Line1942 Visit informit.com/newsletters.
Line1943 •   Access FREE podcasts from experts at informit.com/podcasts.
Line1944 •   Read the latest author articles and sample chapters at 
Line1945 informit.com/articles.
Line1946 •
Line1947 Access thousands of books and videos in the Safari Books 
Line1948 Online digital library at safari.informit.com.
Line1949 • Get tips from expert blogs at informit.com/blogs.
Line1950 Visit informit.com/learn to discover all the ways you can access the 
Line1951 hottest technology content.
Line1952 informIT.com THE TRUSTED TECHNOLOGY LEARNING SOURCE
Line1953 Are You Part of the IT Crowd?
Line1954 Connect with Pearson authors and editors via RSS feeds, Facebook, 
Line1955 Twitter, YouTube, and more! Visit informit.com/socialconnect.
Line1956 
Line1957 
Line1958 ---
Line1959 
Line1960 ---
Line1961 **Page 360**
Line1962 
Line1963 Your purchase of Growing Object-Oriented Software, Guided by Tests includes access 
Line1964 to a free online edition for 45 days through the Safari Books Online subscription service. 
Line1965 Nearly every Addison-Wesley Professional book is available online through Safari Books 
Line1966 Online, along with more than 5,000 other technical books and videos from publishers 
Line1967 such as Cisco Press, Exam Cram, IBM Press, O’Reilly, Prentice Hall, Que, and Sams. 
Line1968 SAFARI BOOKS ONLINE allows you to search for a speciﬁ c answer, cut and paste 
Line1969 code, download chapters, and stay current with emerging technologies. 
Line1970 Activate your FREE Online Edition at 
Line1971 www.informit.com/safarifree
Line1972 STEP 1:  Enter the coupon code: CYMIQVH.
Line1973 STEP 2:  New Safari users, complete the brief registration form. 
Line1974 Safari subscribers, just log in.
Line1975 If you have difﬁ culty registering on Safari or accessing the online edition, 
Line1976 please e-mail customer-service@safaribooksonline.com
Line1977 FREE Online 
Line1978 Edition
