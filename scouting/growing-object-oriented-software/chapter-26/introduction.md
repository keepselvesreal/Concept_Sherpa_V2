Line1 # Introduction (pp.301-302)
Line2 
Line3 ---
Line4 **Page 301**
Line5 
Line6 Chapter 26
Line7 Unit Testing and Threads
Line8 It is decreed by a merciful Nature that the human brain cannot think
Line9 of two things simultaneously.
Line10 —Sir Arthur Conan Doyle
Line11 Introduction
Line12 There’s no getting away from it: concurrency complicates matters. It is a challenge
Line13 when doing test-driven development. Unit tests cannot give you as much
Line14 conﬁdence in system quality because concurrency and synchronization are system-
Line15 wide concerns. When writing tests, you have to worry about getting the synchro-
Line16 nization right within the system and between the test and the system. Test failures
Line17 are harder to diagnose because exceptions may be swallowed by background
Line18 threads or tests may just time out with no clear explanation.
Line19 It’s hard to diagnose and correct synchronization problems in existing code,
Line20 so it’s worth thinking about the system’s concurrency architecture ahead of
Line21 time. You don’t need to design it in great detail, just decide on a broad-brush
Line22 architecture and principles by which the system will cope with concurrency.
Line23 This design is often prescribed by the frameworks or libraries that an
Line24 application uses. For example:
Line25 •
Line26 Swing dispatches user events on its own thread. If an event handler runs
Line27 for a long time, the user interface becomes unresponsive because Swing
Line28 does not process user input while the event handler is running. Event call-
Line29 backs must spawn “worker” threads to perform long-running tasks, and
Line30 those worker threads must synchronize with the event dispatch thread to
Line31 update the user interface.
Line32 •
Line33 A servlet container has a pool of threads that receive HTTP requests and
Line34 pass them to servlets for processing. Many threads can be active in the same
Line35 servlet instance at once.
Line36 •
Line37 Java EE containers manage all the threading in the application. The contain-
Line38 er guarantees that only one thread will call into a component at a time.
Line39 Components cannot start their own threads.
Line40 •
Line41 The Smack library used by the Auction Sniper application starts a daemon
Line42 thread to receive XMPP messages. It will deliver messages on a single thread,
Line43 301
Line44 
Line45 
Line46 ---
Line47 
Line48 ---
Line49 **Page 302**
Line50 
Line51 but the application must synchronize the Smack thread and the Swing thread
Line52 to avoid the GUI components being corrupted.
Line53 When you must design a system’s concurrency architecture from scratch, you
Line54 can use modeling tools to prove your design free of certain classes of synchroniza-
Line55 tion errors, such as deadlock, livelock, or starvation. Design tools that help you
Line56 model concurrency are becoming increasingly easy to use. The book Concurrency:
Line57 State Models & Java Programs [Magee06] is an introduction to concurrent pro-
Line58 gramming that stresses a combination of formal modeling and implementation
Line59 and describes how to do the formal modeling with the LTSA analysis tool.
Line60 Even with a proven design, however, we have to cross the chasm between design
Line61 and implementation. We need to ensure that our components conform to the
Line62 architectural constraints of the system. Testing can help at this point. Once we’ve
Line63 designed how the system will manage concurrency, we can test-drive the objects
Line64 that will ﬁt into that architecture. Unit tests give us conﬁdence that an object
Line65 performs its synchronization responsibilities, such as locking its state or blocking
Line66 and waking threads. Coarser-grained tests, such as system tests, give us conﬁdence
Line67 that the entire system manages concurrency correctly.
Line68 Separating Functionality and Concurrency Policy
Line69 Objects that cope with multiple threads mix functional concerns with synchro-
Line70 nization concerns, either of which can be the cause of test failures. Tests must
Line71 also synchronize with the background threads, so that they don’t make assertions
Line72 before the threads have ﬁnished working or leave threads running that might
Line73 interfere with later tests. Worse, in the presence of threads, unit tests do not
Line74 usually report failures well. Exceptions get thrown on the hidden threads, killing
Line75 them unexpectedly and breaking the behavior of the tested object. If a test times
Line76 out waiting for background threads to ﬁnish, there’s often no diagnostic other
Line77 than a basic timeout message. All this makes unit testing difﬁcult.
Line78 Searching for Auctions Concurrently
Line79 Let’s look at an example. We will extend our Auction Sniper application to let
Line80 the user search for auctions of interest. When the user enters search
Line81 keywords, the application will run the search concurrently on all auction houses
Line82 that the application can connect to. Each AuctionHouse will return a list of
Line83 AuctionDescriptions that contain information about its auctions matching the
Line84 search keywords. The application will combine the results it receives from all
Line85 AuctionHouses and display a single list of auctions to the user. The user can then
Line86 decide which of them to bid for.
Line87 The concurrent search is performed by an AuctionSearch object which passes
Line88 the search keywords to each AuctionHouse and announces the results they return
Line89 Chapter 26
Line90 Unit Testing and Threads
Line91 302
Line92 
Line93 
Line94 ---
