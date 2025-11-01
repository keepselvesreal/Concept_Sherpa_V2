Line1 # Observations (pp.189-190)
Line2 
Line3 ---
Line4 **Page 189**
Line5 
Line6 Observations
Line7 Making Steady Progress
Line8 We’re starting to see more payback from some of our restructuring work. It was
Line9 pretty easy to convert the end-to-end test to handle multiple items, and most of
Line10 the implementation consisted of teasing apart code that was already working.
Line11 We’ve been careful to keep class responsibilities focused—except for the one
Line12 place, Main, where we’ve put all our working compromises.
Line13 We made an effort to stay honest about writing enough tests, which has forced
Line14 us to consider a couple of edge cases we might otherwise have left. We also intro-
Line15 duced a new intermediate-level “integration” test to allow us to work out the
Line16 implementation of the user interface without dragging in the rest of the system.
Line17 TDD Conﬁdential
Line18 We don’t write up everything that went into the development of our
Line19 examples—that would be boring and waste paper—but we think it’s worth a
Line20 note about what happened with this one. It took us a couple of attempts to get
Line21 this design pointing in the right direction because we were trying to allocate be-
Line22 havior to the wrong objects. What kept us honest was that for each attempt to
Line23 write tests that were focused and made sense, the setup and our assertions kept
Line24 drifting apart. Once we’d broken through our inadequacies as programmers, the
Line25 tests became much clearer.
Line26 Ship It?
Line27 So now that everything works we can get on with more features, right? Wrong.
Line28 We don’t believe that “working” is the same thing as “ﬁnished.” We’ve left quite
Line29 a design mess in Main as we sorted out our ideas, with functionality from various
Line30 slices of the application all jumbled into one, as in Figure 16.3.  Apart from the
Line31 confusion this leaves, most of this code is not really testable except through the
Line32 end-to-end tests. We can get away with that now, while the code is still small,
Line33 but it will be difﬁcult to sustain as the application grows. More importantly,
Line34 perhaps, we’re not getting any unit-test feedback about the internal quality of
Line35 the code.
Line36 We might put this code into production if we knew the code was never going
Line37 to change or there was an emergency. We know that the ﬁrst isn’t true, because
Line38 the application isn’t ﬁnished yet, and being in a hurry is not really a crisis. We
Line39 know we will be working in this code again soon, so we can either clean up now,
Line40 while it’s still fresh in our minds, or re-learn it every time we touch it. Given that
Line41 we’re trying to make an educational point here, you’ve probably guessed
Line42 what we’ll do next.
Line43 189
Line44 Observations
Line45 
Line46 
Line47 ---
Line48 
Line49 ---
Line50 **Page 190**
Line51 
Line52 This page intentionally left blank
