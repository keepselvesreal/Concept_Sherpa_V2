Line1 # Too Many Dependencies (pp.241-242)
Line2 
Line3 ---
Line4 **Page 241**
Line5 
Line6 put up with these compromises in a handset because we don’t have enough
Line7 pockets for all the devices it includes, but that doesn’t apply to code. This class
Line8 should be broken up; Michael Feathers describes some techniques for doing so
Line9 in Chapter 20 of [Feathers04].
Line10 An associated smell for this kind of class is that its test suite will look confused
Line11 too. The tests for its various features will have no relationship with each other,
Line12 so we’ll be able to make major changes in one area without touching others. If
Line13 we can break up the test class into slices that don’t share anything, it might be
Line14 best to go ahead and slice up the object too.
Line15 Too Many Dependencies
Line16 A third diagnosis for a bloated constructor might be that not all of the arguments
Line17 are dependencies, one of the peer stereotypes we deﬁned in “Object Peer
Line18 Stereotypes” (page 52). As discussed in that section, we insist on dependencies
Line19 being passed in to the constructor, but notiﬁcations and adjustments can be set
Line20 to defaults and reconﬁgured later. When a constructor is too large, and we don’t
Line21 believe there’s an implicit new type amongst the arguments, we can use more
Line22 default values and only overwrite them for particular test cases.
Line23 Here’s an example—it’s not quite bad enough to need ﬁxing, but it’ll do to
Line24 make the point. The application is a racing game; players can try out different
Line25 conﬁgurations of car and driving style to see which one wins.1 A RacingCar
Line26 represents a competitor within a race:
Line27 public class RacingCar {
Line28   private final Track track;
Line29   private Tyres tyres;
Line30   private Suspension suspension;
Line31   private Wing frontWing;
Line32   private Wing backWing;
Line33   private double fuelLoad;
Line34   private CarListener listener;
Line35   private DrivingStrategy driver;
Line36   public RacingCar(Track track, DrivingStrategy driver, Tyres tyres, 
Line37                   Suspension suspension, Wing frontWing, Wing backWing, 
Line38                   double fuelLoad, CarListener listener)
Line39   {
Line40     this.track = track;
Line41     this.driver = driver;
Line42     this.tyres = tyres;
Line43     this.suspension = suspension;
Line44     this.frontWing = frontWing;
Line45     this.backWing = backWing;
Line46     this.fuelLoad = fuelLoad;
Line47     this.listener = listener;
Line48   }
Line49 }
Line50 1. Nat once worked in a job that involved following the Formula One circuit.
Line51 241
Line52 Too Many Dependencies
Line53 
Line54 
Line55 ---
Line56 
Line57 ---
Line58 **Page 242**
Line59 
Line60 It turns out that track is the only dependency of a RacingCar; the hint is that
Line61 it’s the only ﬁeld that’s ﬁnal. The listener is a notiﬁcation, and everything else
Line62 is an adjustment; all of these can be modiﬁed by the user before or during the
Line63 race. Here’s a reworked constructor:
Line64 public class RacingCar {
Line65   private final Track track;
Line66   private DrivingStrategy driver = DriverTypes.borderlineAggressiveDriving();
Line67   private Tyres tyres = TyreTypes.mediumSlicks();
Line68   private Suspension suspension = SuspensionTypes.mediumStiffness();
Line69   private Wing frontWing = WingTypes.mediumDownforce();
Line70   private Wing backWing = WingTypes.mediumDownforce();
Line71   private double fuelLoad = 0.5;
Line72   private CarListener listener = CarListener.NONE;
Line73   public RacingCar(Track track) {
Line74     this.track = track;
Line75   }
Line76   public void setSuspension(Suspension suspension) { […]
Line77   public void setTyres(Tyres tyres) { […]
Line78   public void setEngine(Engine engine) { […]
Line79   public void setListener(CarListener listener) { […]
Line80 }
Line81 Now we’ve initialized these peers to common defaults; the user can conﬁgure
Line82 them later through the user interface, and we can conﬁgure them in our unit tests.
Line83 We’ve initialized the listener to a null object, again this can be changed later
Line84 by the object’s environment.
Line85 Too Many Expectations
Line86 When a test has too many expectations, it’s hard to see what’s important and
Line87 what’s really under test. For example, here’s a test:
Line88 @Test public void 
Line89 decidesCasesWhenFirstPartyIsReady() {
Line90   context.checking(new Expectations(){{
Line91     one(firstPart).isReady(); will(returnValue(true));
Line92     one(organizer).getAdjudicator(); will(returnValue(adjudicator));
Line93     one(adjudicator).findCase(firstParty, issue); will(returnValue(case));
Line94     one(thirdParty).proceedWith(case);
Line95   }});
Line96   claimsProcessor.adjudicateIfReady(thirdParty, issue);
Line97 }
Line98 that might be implemented like this:
Line99 Chapter 20
Line100 Listening to the Tests
Line101 242
Line102 
Line103 
Line104 ---
