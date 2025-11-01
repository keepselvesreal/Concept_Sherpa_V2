Line1 # Distinguish Synchronizations and Assertions (pp.326-326)
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
