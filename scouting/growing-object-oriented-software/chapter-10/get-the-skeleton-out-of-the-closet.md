Line1 # Get the Skeleton out of the Closet (pp.83-84)
Line2 
Line3 ---
Line4 **Page 83**
Line5 
Line6 Chapter 10
Line7 The Walking Skeleton
Line8 In which we set up our development environment and write our ﬁrst
Line9 end-to-end test. We make some infrastructure choices that allow us to
Line10 get started, and construct a build. We’re surprised, yet again, at how
Line11 much effort this takes.
Line12 Get the Skeleton out of the Closet
Line13 So now we’ve got an idea of what to build, can we get on with it and write our
Line14 ﬁrst unit test?
Line15 Not yet.
Line16 Our ﬁrst task is to create the “walking skeleton” we described in “First, Test
Line17 a Walking Skeleton” (page 32). Again, the point of the walking skeleton is to
Line18 help us understand the requirements well enough to propose and validate a broad-
Line19 brush system structure. We can always change our minds later, when we learn
Line20 more, but it’s important to start with something that maps out the landscape of
Line21 our solution. Also, it’s very important to be able to assess the approach we’ve
Line22 chosen and to test our decisions so we can make changes with conﬁdence later.
Line23 For most projects, developing the walking skeleton takes a surprising amount
Line24 of effort. First, because deciding what to do will ﬂush out all sorts of questions
Line25 about the application and its place in the world. Second, because the automation
Line26 of building, packaging, and deploying into a production-like environment (once
Line27 we know what that means) will ﬂush out all sorts of technical and organizational
Line28 questions.
Line29 Iteration Zero
Line30 In most Agile projects, there’s a ﬁrst stage where the team is doing initial analysis,
Line31 setting up its physical and technical environments, and otherwise getting started.
Line32 The team isn’t adding much visible functionality since almost all the work is infra-
Line33 structure, so it might not make sense to count this as a conventional iteration for
Line34 scheduling purposes. A common practice is to call this step iteration zero: “iteration”
Line35 because the team still needs to time-box its activities and “zero” because it’s before
Line36 functional development starts in iteration one. One important task for iteration zero
Line37 is to use the walking skeleton to test-drive the initial architecture.
Line38 Of course, we start our walking skeleton by writing a test.
Line39 83
Line40 
Line41 
Line42 ---
Line43 
Line44 ---
Line45 **Page 84**
Line46 
Line47 Our Very First Test
Line48 The walking skeleton must cover all the components of our Auction Sniper system:
Line49 the user interface, the sniping component, and the communication with an auction
Line50 server. The thinnest slice we can imagine testing, the ﬁrst item on our to-do list,
Line51 is that the Auction Sniper can join an auction and then wait for it to close. This
Line52 slice is so minimal that we’re not even concerned with sending a bid; we just
Line53 want to know that the two sides can communicate and that we can test the system
Line54 from outside (through the client’s GUI and by injecting events as if from the ex-
Line55 ternal auction server). Once that’s working, we have a solid base on which to
Line56 build the rest of the features that the clients want.
Line57 We like to start by writing a test as if its implementation already exists, and
Line58 then ﬁlling in whatever is needed to make it work—what Abelson and Sussman
Line59 call “programming by wishful thinking” [Abelson96]. Working backwards from
Line60 the test helps us focus on what we want the system to do, instead of getting
Line61 caught up in the complexity of how we will make it work. So, ﬁrst we code up
Line62 a test to describe our intentions as clearly as we can, given the expressive limits
Line63 of a programming language. Then we build the infrastructure to support the way
Line64 we want to test the system, instead of writing the tests to ﬁt in with an existing
Line65 infrastructure. This usually takes a large part of our initial effort because there
Line66 is so much to get ready. With this infrastructure in place, we can implement the
Line67 feature and make the test pass.
Line68 An outline of the test we want is:
Line69 1.
Line70 When an auction is selling an item,
Line71 2.
Line72 And an Auction Sniper has started to bid in that auction,
Line73 3.
Line74 Then the auction will receive a Join request from the Auction Sniper.
Line75 4.
Line76 When an auction announces that it is Closed,
Line77 5.
Line78 Then the Auction Sniper will show that it lost the auction.
Line79 This describes one transition in the state machine (see Figure 10.1).
Line80 We need to translate this into something executable. We use JUnit as our test
Line81 framework since it’s familiar and widely supported. We also need mechanisms
Line82 to control the application and the auction that the application is talking to.
Line83 Southabee’s On-Line test services are not freely available. We have to book
Line84 ahead and pay for each test session, which is not practical if we want to run tests
Line85 all the time. We’ll need a fake auction service that we can control from our
Line86 tests to behave like the real thing—or at least like we think the real thing behaves
Line87 until we get a chance to test against it for real. This fake auction, or stub, will
Line88 be as simple as we can make it. It will connect to an XMPP message broker,
Line89 receive commands from the Sniper to be checked by the test, and allow the test
Line90 to send back events. We’re not trying to reimplement all of Southabee’s On-Line,
Line91 just enough of it to support test scenarios.
Line92 Chapter 10
Line93 The Walking Skeleton
Line94 84
Line95 
Line96 
Line97 ---
