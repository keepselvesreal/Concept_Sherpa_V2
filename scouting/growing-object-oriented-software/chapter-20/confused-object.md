Line1 # Confused Object (pp.240-241)
Line2 
Line3 ---
Line4 **Page 240**
Line5 
Line6 messageProcessor = 
Line7   new MessageProcessor(new XmlMessageUnpacker(), 
Line8                        auditor, counterpartyFinder, 
Line9                        locationFinder, domesticNotifier,
Line10                        importedNotifier);
Line11 to this:
Line12 messageProcessor = 
Line13   new MessageProcessor(new XmlMessageUnpacker(counterpartyFinder),
Line14                        auditor,
Line15 new MessageDispatcher(
Line16                          locationFinder, 
Line17                          domesticNotifier, importedNotifier));
Line18 Later we can reduce the syntax noise by extracting out the creation of the
Line19 MessageDispatcher.
Line20 Confused Object
Line21 Another diagnosis for a “bloated constructor” might be that the object itself is
Line22 too large because it has too many responsibilities. For example,
Line23 public class Handset {
Line24   public Handset(Network network, Camera camera, Display display, 
Line25                 DataNetwork dataNetwork, AddressBook addressBook,
Line26                 Storage storage, Tuner tuner, …)
Line27   {
Line28 // set the fields here
Line29   }
Line30   public void placeCallTo(DirectoryNumber number) { 
Line31     network.openVoiceCallTo(number);
Line32   }
Line33   public void takePicture() { 
Line34     Frame frame = storage.allocateNewFrame();
Line35     camera.takePictureInto(frame);
Line36     display.showPicture(frame);
Line37   }
Line38   public void showWebPage(URL url) {
Line39     display.renderHtml(dataNetwork.retrievePage(url));
Line40   }
Line41   public void showAddress(SearchTerm searchTerm) {
Line42     display.showAddress(addressBook.findAddress(searchTerm));
Line43   } 
Line44   public void playRadio(Frequency frequency) {
Line45     tuner.tuneTo(frequency);
Line46     tuner.play();
Line47   }
Line48 // and so on
Line49 }
Line50 Like our mobile phones, this class has several unrelated responsibilities which
Line51 force it to pull in many dependencies. And, like our phones, the class is confusing
Line52 to use because unrelated features interfere with each other. We’re prepared to
Line53 Chapter 20
Line54 Listening to the Tests
Line55 240
Line56 
Line57 
Line58 ---
Line59 
Line60 ---
Line61 **Page 241**
Line62 
Line63 put up with these compromises in a handset because we don’t have enough
Line64 pockets for all the devices it includes, but that doesn’t apply to code. This class
Line65 should be broken up; Michael Feathers describes some techniques for doing so
Line66 in Chapter 20 of [Feathers04].
Line67 An associated smell for this kind of class is that its test suite will look confused
Line68 too. The tests for its various features will have no relationship with each other,
Line69 so we’ll be able to make major changes in one area without touching others. If
Line70 we can break up the test class into slices that don’t share anything, it might be
Line71 best to go ahead and slice up the object too.
Line72 Too Many Dependencies
Line73 A third diagnosis for a bloated constructor might be that not all of the arguments
Line74 are dependencies, one of the peer stereotypes we deﬁned in “Object Peer
Line75 Stereotypes” (page 52). As discussed in that section, we insist on dependencies
Line76 being passed in to the constructor, but notiﬁcations and adjustments can be set
Line77 to defaults and reconﬁgured later. When a constructor is too large, and we don’t
Line78 believe there’s an implicit new type amongst the arguments, we can use more
Line79 default values and only overwrite them for particular test cases.
Line80 Here’s an example—it’s not quite bad enough to need ﬁxing, but it’ll do to
Line81 make the point. The application is a racing game; players can try out different
Line82 conﬁgurations of car and driving style to see which one wins.1 A RacingCar
Line83 represents a competitor within a race:
Line84 public class RacingCar {
Line85   private final Track track;
Line86   private Tyres tyres;
Line87   private Suspension suspension;
Line88   private Wing frontWing;
Line89   private Wing backWing;
Line90   private double fuelLoad;
Line91   private CarListener listener;
Line92   private DrivingStrategy driver;
Line93   public RacingCar(Track track, DrivingStrategy driver, Tyres tyres, 
Line94                   Suspension suspension, Wing frontWing, Wing backWing, 
Line95                   double fuelLoad, CarListener listener)
Line96   {
Line97     this.track = track;
Line98     this.driver = driver;
Line99     this.tyres = tyres;
Line100     this.suspension = suspension;
Line101     this.frontWing = frontWing;
Line102     this.backWing = backWing;
Line103     this.fuelLoad = fuelLoad;
Line104     this.listener = listener;
Line105   }
Line106 }
Line107 1. Nat once worked in a job that involved following the Formula One circuit.
Line108 241
Line109 Too Many Dependencies
Line110 
Line111 
Line112 ---
