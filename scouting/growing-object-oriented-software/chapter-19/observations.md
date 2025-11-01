Line1 # Observations (pp.225-228)
Line2 
Line3 ---
Line4 **Page 225**
Line5 
Line6 The end-to-end test passes completely and we can cross another item off our
Line7 list: Figure 19.2.
Line8 Figure 19.2
Line9 The Sniper reports failed messages from an auction
Line10 Observations
Line11 “Inverse Salami” Development
Line12 We hope that by now you’re getting a sense of the rhythm of incrementally
Line13 growing software, adding functionality in thin but coherent slices. For each new
Line14 feature, write some tests that show what it should do, work through each of
Line15 those tests changing just enough code to make it pass, restructure the code as
Line16 needed either to open up space for new functionality or to reveal new
Line17 concepts—then ship it. We discuss how this ﬁts into the larger development picture
Line18 in Chapter 5. In static languages, such as Java and C#, we can often use the
Line19 compiler to help us navigate the chain of implementation dependencies: change
Line20 the code to accept the new triggering event, see what breaks, ﬁx that breakage,
Line21 see what that change breaks in turn, and repeat the process until the
Line22 functionality works.
Line23 The skill is in learning how to divide requirements up into incremental slices,
Line24 always having something working, always adding just one more feature. The
Line25 process should feel relentless—it just keeps moving. To make this work, we have
Line26 to understand how to change the code incrementally and, critically, keep the
Line27 code well structured so that we can take it wherever we need to go (and we
Line28 don’t know where that is yet). This is why the refactoring part of a test-driven
Line29 225
Line30 Observations
Line31 
Line32 
Line33 ---
Line34 
Line35 ---
Line36 **Page 226**
Line37 
Line38 development cycle is so critical—we always get into trouble when we don’t keep
Line39 up that side of the bargain.
Line40 Small Methods to Express Intent
Line41 We have a habit of writing helper methods to wrap up small amounts of code—for
Line42 two reasons. First, this reduces the amount of syntactic noise in the calling code
Line43 that languages like Java force upon us. For example, when we disconnect
Line44 the Sniper, the translatorFor() method means we don’t have to type
Line45 "AuctionMessageTranslator" twice in the same line. Second, this gives a mean-
Line46 ingful name to a structure that would not otherwise be obvious. For example,
Line47 chatDisconnectorFor() describes what its anonymous class does and is less
Line48 intrusive than deﬁning a named inner class.
Line49 Our aim is to do what we can to make each level of code as readable and self-
Line50 explanatory as possible, repeating the process all the way down until we actually
Line51 have to use a Java construct.
Line52 Logging Is Also a Feature
Line53 We deﬁned XMPPFailureReporter to package up failure reporting for the
Line54 AuctionMessageTranslator. Many teams would regard this as overdesign and
Line55 just write the log message in place. We think this would weaken the design by
Line56 mixing levels (message translation and logging) in the same code.
Line57 We’ve seen many systems where logging has been added ad hoc by developers
Line58 wherever they ﬁnd a need. However, production logging is an external interface
Line59 that should be driven by the requirements of those who will depend on it, not
Line60 by the structure of the current implementation. We ﬁnd that when we take the
Line61 trouble to describe runtime reporting in the caller’s terms, as we did with
Line62 the XMPPFailureReporter, we end up with more useful logs. We also ﬁnd that
Line63 we end up with the logging infrastructure clearly isolated, rather than scattered
Line64 throughout the code, which makes it easier to work with.
Line65 This topic is such a bugbear (for Steve at least) that we devote a whole section
Line66 to it in Chapter 20.
Line67 Chapter 19
Line68 Handling Failure
Line69 226
