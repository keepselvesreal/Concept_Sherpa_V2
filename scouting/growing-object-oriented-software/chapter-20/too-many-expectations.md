Line1 # Too Many Expectations (pp.242-244)
Line2 
Line3 ---
Line4 **Page 242**
Line5 
Line6 It turns out that track is the only dependency of a RacingCar; the hint is that
Line7 it’s the only ﬁeld that’s ﬁnal. The listener is a notiﬁcation, and everything else
Line8 is an adjustment; all of these can be modiﬁed by the user before or during the
Line9 race. Here’s a reworked constructor:
Line10 public class RacingCar {
Line11   private final Track track;
Line12   private DrivingStrategy driver = DriverTypes.borderlineAggressiveDriving();
Line13   private Tyres tyres = TyreTypes.mediumSlicks();
Line14   private Suspension suspension = SuspensionTypes.mediumStiffness();
Line15   private Wing frontWing = WingTypes.mediumDownforce();
Line16   private Wing backWing = WingTypes.mediumDownforce();
Line17   private double fuelLoad = 0.5;
Line18   private CarListener listener = CarListener.NONE;
Line19   public RacingCar(Track track) {
Line20     this.track = track;
Line21   }
Line22   public void setSuspension(Suspension suspension) { […]
Line23   public void setTyres(Tyres tyres) { […]
Line24   public void setEngine(Engine engine) { […]
Line25   public void setListener(CarListener listener) { […]
Line26 }
Line27 Now we’ve initialized these peers to common defaults; the user can conﬁgure
Line28 them later through the user interface, and we can conﬁgure them in our unit tests.
Line29 We’ve initialized the listener to a null object, again this can be changed later
Line30 by the object’s environment.
Line31 Too Many Expectations
Line32 When a test has too many expectations, it’s hard to see what’s important and
Line33 what’s really under test. For example, here’s a test:
Line34 @Test public void 
Line35 decidesCasesWhenFirstPartyIsReady() {
Line36   context.checking(new Expectations(){{
Line37     one(firstPart).isReady(); will(returnValue(true));
Line38     one(organizer).getAdjudicator(); will(returnValue(adjudicator));
Line39     one(adjudicator).findCase(firstParty, issue); will(returnValue(case));
Line40     one(thirdParty).proceedWith(case);
Line41   }});
Line42   claimsProcessor.adjudicateIfReady(thirdParty, issue);
Line43 }
Line44 that might be implemented like this:
Line45 Chapter 20
Line46 Listening to the Tests
Line47 242
Line48 
Line49 
Line50 ---
Line51 
Line52 ---
Line53 **Page 243**
Line54 
Line55 public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
Line56   if (firstParty.isReady()) {
Line57     Adjudicator adjudicator = organization.getAdjudicator();
Line58     Case case = adjudicator.findCase(firstParty, issue);
Line59     thirdParty.proceedWith(case);
Line60   } else{
Line61     thirdParty.adjourn();
Line62   }
Line63 }
Line64 What makes the test hard to read is that everything is an expectation, so every-
Line65 thing looks equally important. We can’t tell what’s signiﬁcant and what’s just
Line66 there to get through the test.
Line67 In fact, if we look at all the methods we call, there are only two that
Line68 have any side effects outside this class: thirdParty.proceedWith() and
Line69 thirdParty.adjourn(); it would be an error to call these more than once. All the
Line70 other methods are queries; we can call organization.getAdjudicator() repeat-
Line71 edly without breaking any behavior. adjudicator.findCase() might go either
Line72 way, but it happens to be a lookup so it has no side effects.
Line73 We can make our intentions clearer by distinguishing between stubs, simulations
Line74 of real behavior that help us get the test to pass, and expectations, assertions we
Line75 want to make about how an object interacts with its neighbors. There’s a longer
Line76 discussion of this distinction in “Allowances and Expectations” (page 277).
Line77 Reworking the test, we get:
Line78 @Test public void decidesCasesWhenFirstPartyIsReady() {
Line79   context.checking(new Expectations(){{
Line80 allowing(firstPart).isReady(); will(returnValue(true));
Line81 allowing(organizer).getAdjudicator(); will(returnValue(adjudicator));
Line82 allowing(adjudicator).findCase(firstParty, issue); will(returnValue(case));
Line83     one(thirdParty).proceedWith(case);
Line84   }});
Line85   claimsProcessor.adjudicateIfReady(thirdParty, issue);
Line86 }
Line87 which is more explicit about how we expect the object to change the world
Line88 around it.
Line89 Write Few Expectations
Line90 A colleague, Romilly Cocking, when he ﬁrst started working with us, was surprised
Line91 by how few expectations we usually write in a unit test. Just like “everyone” has
Line92 now learned to avoid too many assertions in a test, we try to avoid too many
Line93 expectations. If we have more than a few, then either we’re trying to test too large
Line94 a unit, or we’re locking down too many of the object’s interactions.
Line95 243
Line96 Too Many Expectations
Line97 
Line98 
Line99 ---
Line100 
Line101 ---
Line102 **Page 244**
Line103 
Line104 Special Bonus Prize
Line105 We always have problems coming up with good examples. There’s actually a
Line106 better improvement to this code, which is to notice that we’ve pulled out a chain
Line107 of objects to get to the case object, exposing dependencies that aren’t relevant
Line108 here. Instead, we should have told the nearest object to do the work for us,
Line109 like this:
Line110 public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
Line111   if (firstParty.isReady()) {
Line112 organization.adjudicateBetween(firstParty, thirdParty, issue);
Line113   } else {
Line114     thirdParty.adjourn();
Line115   }
Line116 }
Line117 or, possibly,
Line118 public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
Line119   if (firstParty.isReady()) {
Line120     thirdParty.startAdjudication(organization, firstParty, issue);
Line121   } else{
Line122     thirdParty.adjourn();
Line123   }
Line124 }
Line125 which looks more balanced. If you spotted this, we award you a Moment of
Line126 Smugness™ to be exercised at your convenience.
Line127 What the Tests Will Tell Us (If We’re Listening)
Line128 We’ve found these beneﬁts from learning to listen to test smells:
Line129 Keep knowledge local
Line130 Some of the test smells we’ve identiﬁed, such as needing “magic” to create
Line131 mocks, are to do with knowledge leaking between components. If we can
Line132 keep knowledge local to an object (either internal or passed in), then its im-
Line133 plementation is independent of its context; we can safely move it wherever
Line134 we like. Do this consistently and your application, built out of pluggable
Line135 components, will be easy to change.
Line136 If it’s explicit, we can name it
Line137 One reason why we don’t like mocking concrete classes is that we like to
Line138 have names for the relationships between objects as well the objects them-
Line139 selves. As the legends say, if we have something’s true name, we can control
Line140 it. If we can see it, we have a better chance of ﬁnding its other uses and so
Line141 reducing duplication.
Line142 Chapter 20
Line143 Listening to the Tests
Line144 244
Line145 
Line146 
Line147 ---
