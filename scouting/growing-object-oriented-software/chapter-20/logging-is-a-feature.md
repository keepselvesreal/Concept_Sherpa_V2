Line1 # Logging Is a Feature (pp.233-235)
Line2 
Line3 ---
Line4 **Page 233**
Line5 
Line6 One goal of object orientation as a technique for structuring code is to make
Line7 the boundaries of an object clearly visible. An object should only deal with values
Line8 and instances that are either local—created and managed within its scope—or
Line9 passed in explicitly, as we emphasized in “Context Independence” (page 54).
Line10 In the example above, the act of making date checking testable forced us to
Line11 make the Receiver’s requirements more explicit and to think more clearly about
Line12 the domain.
Line13 Use the Same Techniques to Break Dependencies in Unit Tests
Line14 as in Production Code
Line15 There are several frameworks available that use techniques such as manipulating
Line16 class loaders or bytecodes to allow unit tests to break dependencies without
Line17 changing the target code. As a rule, these are advanced techniques that most
Line18 developers would not use when writing production code. Sometimes these tools
Line19 really are necessary, but developers should be aware that they come with a
Line20 hidden cost.
Line21 Unit-testing tools that let the programmer sidestep poor dependency management
Line22 in the design waste a valuable source of feedback.When the developers eventually
Line23 do need to address these design weaknesses to add some urgent feature, they
Line24 will ﬁnd it harder to do. The poor structure will have inﬂuenced other parts of the
Line25 system that rely on it, and any understanding of the original intent will have
Line26 evaporated. As with dirty pots and pans, it’s easier to get the grease off before it’s
Line27 been baked in.
Line28 Logging Is a Feature
Line29 We have a more contentious example of working with objects that are hard to
Line30 replace: logging. Take a look at these two lines of code:
Line31 log.error("Lost touch with Reality after " + timeout + "seconds");
Line32 log.trace("Distance traveled in the wilderness: " + distance);
Line33 These are two separate features that happen to share an implementation. Let
Line34 us explain.
Line35 •
Line36 Support logging (errors and info) is part of the user interface of the appli-
Line37 cation. These messages are intended to be tracked by support staff, as well
Line38 as perhaps system administrators and operators, to diagnose a failure or
Line39 monitor the progress of the running system.
Line40 •
Line41 Diagnostic logging (debug and trace) is infrastructure for programmers.
Line42 These messages should not be turned on in production because they’re in-
Line43 tended to help the programmers understand what’s going on inside the
Line44 system they’re developing.
Line45 233
Line46 Logging Is a Feature
Line47 
Line48 
Line49 ---
Line50 
Line51 ---
Line52 **Page 234**
Line53 
Line54 Given this distinction, we should consider using different techniques for these
Line55 two type of logging. Support logging should be test-driven from somebody’s re-
Line56 quirements, such as auditing or failure recovery. The tests will make sure we’ve
Line57 thought about what each message is for and made sure it works. The tests will
Line58 also protect us from breaking any tools and scripts that other people write to
Line59 analyze these log messages. Diagnostic logging, on the other hand, is driven by
Line60 the programmers’ need for ﬁne-grained tracking of what’s happening in the sys-
Line61 tem. It’s scaffolding—so it probably doesn’t need to be test-driven and the mes-
Line62 sages might not need to be as consistent as those for support logs. After all, didn’t
Line63 we just agree that these messages are not to be used in production?
Line64 Notiﬁcation Rather Than Logging
Line65 To get back to the point of the chapter, writing unit tests against static global
Line66 objects, including loggers, is clumsy. We have to either read from the ﬁle system
Line67 or manage an extra appender object for testing; we have to remember to clean
Line68 up afterwards so that tests don’t interfere with each other and set the right level
Line69 on the right logger. The noise in the test reminds us that our code is working at
Line70 two levels: our domain and the logging infrastructure. Here’s a common example
Line71 of code with logging:
Line72 Location location = tracker.getCurrentLocation();
Line73 for (Filter filter : filters) {
Line74   filter.selectFor(location);
Line75 if (logger.isInfoEnabled()) {
Line76     logger.info("Filter " + filter.getName() + ", " + filter.getDate()
Line77                  + " selected for " + location.getName() 
Line78                  + ", is current: " + tracker.isCurrent(location));
Line79   }
Line80 }
Line81 Notice the shift in vocabulary and style between the functional part of the
Line82 loop and the (emphasized) logging part. The code is doing two things at
Line83 once—something to do with locations and rendering support information—which
Line84 breaks the single responsibility principle. Maybe we could do this instead:
Line85 Location location = tracker.getCurrentLocation();
Line86 for (Filter filter : filters) {
Line87   filter.selectFor(location);
Line88 support.notifyFiltering(tracker, location, filter);}
Line89 where the support object might be implemented by a logger, a message bus,
Line90 pop-up windows, or whatever’s appropriate; this detail is not relevant to the
Line91 code at this level.
Line92 This code is also easier to test, as you saw in Chapter 19. We, not the logging
Line93 framework, own the support object, so we can pass in a mock implementation
Line94 at our convenience and keep it local to the test case. The other simpliﬁcation is
Line95 that now we’re testing for objects, rather than formatted contents of a string. Of
Line96 Chapter 20
Line97 Listening to the Tests
Line98 234
Line99 
Line100 
Line101 ---
Line102 
Line103 ---
Line104 **Page 235**
Line105 
Line106 course, we will still need to write an implementation of support and some focused
Line107 integration tests to go with it.
Line108 But That’s Crazy Talk…
Line109 The idea of encapsulating support reporting sounds like over-design, but it’s
Line110 worth thinking about for a moment. It means we’re writing code in terms of our
Line111 intent (helping the support people) rather than implementation (logging), so it’s
Line112 more expressive. All the support reporting is handled in a few known places, so
Line113 it’s easier to be consistent about how things are reported and to encourage reuse.
Line114 It can also help us structure and control our reporting in terms of the application
Line115 domain, rather than in terms of Java packages. Finally, the act of writing a test
Line116 for each report helps us avoid the “I don’t know what to do with this exception,
Line117 so I’ll log it and carry on” syndrome, which leads to log bloat and production
Line118 failures because we haven’t handled obscure error conditions.
Line119 One objection we’ve heard is, “I can’t pass in a logger for testing because I’ve
Line120 got logging all over my domain objects. I’d have to pass one around everywhere.”
Line121 We think this is a test smell that is telling us that we haven’t clariﬁed our design
Line122 enough. Perhaps some of our support logging should really be diagnostic logging,
Line123 or we’re logging more than we need because of something that we wrote when
Line124 we hadn’t yet understood the behavior. Most likely, there’s still too much dupli-
Line125 cation in our domain code and we haven’t yet found the “choke points” where
Line126 most of the production logging should go.
Line127 So what about diagnostic logging? Is it disposable scaffolding that should be
Line128 taken down once the job is done, or essential infrastructure that should be tested
Line129 and maintained? That depends on the system, but once we’ve made the distinction
Line130 we have more freedom to think about using different techniques for support and
Line131 diagnostic logging. We might even decide that in-line code is the wrong technique
Line132 for diagnostic logging because it interferes with the readability of the production
Line133 code that matters. Perhaps we could weave in some aspects instead (since that’s
Line134 the canonical example of their use); perhaps not—but at least we’ve now
Line135 clariﬁed the choice.
Line136 One ﬁnal data point. One of us once worked on a system where so much
Line137 content was written to the logs that they had to be deleted after a week to ﬁt on
Line138 the disks. This made maintenance very difﬁcult as the relevant logs were usually
Line139 gone by the time a bug was assigned to be ﬁxed. If they’d logged nothing at all,
Line140 the system would have run faster with no loss of useful information.
Line141 Mocking Concrete Classes
Line142 One approach to interaction testing is to mock concrete classes rather than inter-
Line143 faces. The technique is to inherit from the class you want to mock and override
Line144 the methods that will be called within the test, either manually or with any of
Line145 235
Line146 Mocking Concrete Classes
Line147 
Line148 
Line149 ---
