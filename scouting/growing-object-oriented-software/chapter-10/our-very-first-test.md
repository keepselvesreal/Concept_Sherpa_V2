Line1 # Our Very First Test (pp.84-86)
Line2 
Line3 ---
Line4 **Page 84**
Line5 
Line6 Our Very First Test
Line7 The walking skeleton must cover all the components of our Auction Sniper system:
Line8 the user interface, the sniping component, and the communication with an auction
Line9 server. The thinnest slice we can imagine testing, the ﬁrst item on our to-do list,
Line10 is that the Auction Sniper can join an auction and then wait for it to close. This
Line11 slice is so minimal that we’re not even concerned with sending a bid; we just
Line12 want to know that the two sides can communicate and that we can test the system
Line13 from outside (through the client’s GUI and by injecting events as if from the ex-
Line14 ternal auction server). Once that’s working, we have a solid base on which to
Line15 build the rest of the features that the clients want.
Line16 We like to start by writing a test as if its implementation already exists, and
Line17 then ﬁlling in whatever is needed to make it work—what Abelson and Sussman
Line18 call “programming by wishful thinking” [Abelson96]. Working backwards from
Line19 the test helps us focus on what we want the system to do, instead of getting
Line20 caught up in the complexity of how we will make it work. So, ﬁrst we code up
Line21 a test to describe our intentions as clearly as we can, given the expressive limits
Line22 of a programming language. Then we build the infrastructure to support the way
Line23 we want to test the system, instead of writing the tests to ﬁt in with an existing
Line24 infrastructure. This usually takes a large part of our initial effort because there
Line25 is so much to get ready. With this infrastructure in place, we can implement the
Line26 feature and make the test pass.
Line27 An outline of the test we want is:
Line28 1.
Line29 When an auction is selling an item,
Line30 2.
Line31 And an Auction Sniper has started to bid in that auction,
Line32 3.
Line33 Then the auction will receive a Join request from the Auction Sniper.
Line34 4.
Line35 When an auction announces that it is Closed,
Line36 5.
Line37 Then the Auction Sniper will show that it lost the auction.
Line38 This describes one transition in the state machine (see Figure 10.1).
Line39 We need to translate this into something executable. We use JUnit as our test
Line40 framework since it’s familiar and widely supported. We also need mechanisms
Line41 to control the application and the auction that the application is talking to.
Line42 Southabee’s On-Line test services are not freely available. We have to book
Line43 ahead and pay for each test session, which is not practical if we want to run tests
Line44 all the time. We’ll need a fake auction service that we can control from our
Line45 tests to behave like the real thing—or at least like we think the real thing behaves
Line46 until we get a chance to test against it for real. This fake auction, or stub, will
Line47 be as simple as we can make it. It will connect to an XMPP message broker,
Line48 receive commands from the Sniper to be checked by the test, and allow the test
Line49 to send back events. We’re not trying to reimplement all of Southabee’s On-Line,
Line50 just enough of it to support test scenarios.
Line51 Chapter 10
Line52 The Walking Skeleton
Line53 84
Line54 
Line55 
Line56 ---
Line57 
Line58 ---
Line59 **Page 85**
Line60 
Line61 Figure 10.1
Line62 A Sniper joins, then loses
Line63 Controlling the Sniper application is more complicated. We want our skeleton
Line64 test to exercise our application as close to end-to-end as possible, to show that
Line65 the main() method initializes the application correctly and that the components
Line66 really work together. This means that we should start by working through the
Line67 publicly visible features of the application (in this case, its user interface) instead
Line68 of directly invoking its domain objects. We also want our test to be clear about
Line69 what is being checked, written in terms of the relationship between a Sniper and
Line70 its auction, so we’ll hide all the messy code for manipulating Swing in an
Line71 ApplicationRunner class. We’ll start by writing the test as if all the code it needs
Line72 exists and will ﬁll in the implementations afterwards.
Line73 public class AuctionSniperEndToEndTest {
Line74   private final FakeAuctionServer auction = new FakeAuctionServer("item-54321");
Line75   private final ApplicationRunner application = new ApplicationRunner();
Line76   @Test public void sniperJoinsAuctionUntilAuctionCloses() throws Exception {
Line77     auction.startSellingItem();                 // Step 1
Line78     application.startBiddingIn(auction);        // Step 2
Line79     auction.hasReceivedJoinRequestFromSniper(); // Step 3
Line80     auction.announceClosed();                   // Step 4
Line81     application.showsSniperHasLostAuction();    // Step 5
Line82   }
Line83 // Additional cleanup
Line84   @After public void stopAuction() {
Line85     auction.stop();
Line86   }
Line87   @After public void stopApplication() {
Line88     application.stop();
Line89   }
Line90 }
Line91 85
Line92 Our Very First Test
Line93 
Line94 
Line95 ---
Line96 
Line97 ---
Line98 **Page 86**
Line99 
Line100 We’ve adopted certain naming conventions for the methods of the helper ob-
Line101 jects. If a method triggers an event to drive the test, its name will be a command,
Line102 such as startBiddingIn(). If a method asserts that something should have hap-
Line103 pened, its name will be descriptive;1 for example, showsSniperHasLostAuction()
Line104 will throw an exception if the application is not showing the auction status as
Line105 lost. JUnit will call the two stop() methods after the test has run, to clean up
Line106 the runtime environment.
Line107 In writing the test, one of the assumptions we’ve made is that a
Line108 FakeAuctionServer is tied to a given item. This matches the structure of our
Line109 intended architecture, where Southabee’s On-Line hosts multiple auctions, each
Line110 selling a single item.
Line111 One Domain at a Time
Line112 The language of this test is concerned with auctions and Snipers; there’s nothing
Line113 about messaging layers or components in the user interface—that’s all incidental
Line114 detail here. Keeping the language consistent helps us understand what’s signiﬁcant
Line115 in this test, with a nice side effect of protecting us when the implementation inevitably
Line116 changes.
Line117 Some Initial Choices
Line118 Now we have to make the test pass, which will require a lot of preparation. We
Line119 need to ﬁnd or write four components: an XMPP message broker, a stub auction
Line120 that can communicate over XMPP, a GUI testing framework, and a test har-
Line121 ness that can cope with our multithreaded, asynchronous architecture. We also
Line122 have to get the project under version control with an automated build/deploy/test
Line123 process. Compared to unit-testing a single class, there is a lot to do—but it’s es-
Line124 sential. Even at this high level, the exercise of writing tests drives the development
Line125 of the system. Working through our ﬁrst end-to-end test will force some of the
Line126 structural decisions we need to make, such as packaging and deployment.
Line127 First the package selection, we will need an XMPP message broker to let the
Line128 application talk to our stub auction house. After some investigation, we decide
Line129 on an open source implementation called Openﬁre and its associated client library
Line130 Smack. We also need a high-level test framework that can work with Swing
Line131 and Smack, both of which are multithreaded and event-driven. Luckily for us,
Line132 there are several frameworks for testing Swing applications and the way that
Line133 they deal with Swing’s multithreaded, event-driven architecture also works well
Line134 with XMPP messaging. We pick WindowLicker which is open source and supports
Line135 1. For the grammatically pedantic, the names of methods that trigger events are in the
Line136 imperative mood whereas the names of assertions are in the indicative mood.
Line137 Chapter 10
Line138 The Walking Skeleton
Line139 86
Line140 
Line141 
Line142 ---
