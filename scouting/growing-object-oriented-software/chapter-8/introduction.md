Line1 # Introduction (pp.69-69)
Line2 
Line3 ---
Line4 **Page 69**
Line5 
Line6 Chapter 8
Line7 Building on Third-Party Code
Line8 Programming today is all about doing science on the parts you have
Line9 to work with.
Line10 —Gerald Jay Sussman
Line11 Introduction
Line12 We’ve shown how we pull a system’s design into existence: discovering what our
Line13 objects need and writing interfaces and further objects to meet those needs. This
Line14 process works well for new functionality. At some point, however, our design
Line15 will come up against a need that is best met by third-party code: standard APIs,
Line16 open source libraries, or vendor products. The critical point about third-party
Line17 code is that we don’t control it, so we cannot use our process to guide its design.
Line18 Instead, we must focus on the integration between our design and the
Line19 external code.
Line20 In integration, we have an abstraction to implement, discovered while we de-
Line21 veloped the rest of the feature. With the third-party API pushing back at our
Line22 design, we must ﬁnd the best balance between elegance and practical use of
Line23 someone else’s ideas. We must check that we are using the third-party API cor-
Line24 rectly, and adjust our abstraction to ﬁt if we ﬁnd that our assumptions are
Line25 incorrect.
Line26 Only Mock Types That You Own
Line27 Don’t Mock Types You Can’t Change
Line28 When we use third-party code we often do not have a deep understanding of
Line29 how it works. Even if we have the source available, we rarely have time to read
Line30 it thoroughly enough to explore all its quirks. We can read its documentation,
Line31 which is often incomplete or incorrect. The software may also have bugs that we
Line32 will need to work around. So, although we know how we want our abstraction
Line33 to behave, we don’t know if it really does so until we test it in combination with
Line34 the third-party code.
Line35 We also prefer not to change third-party code, even when we have the sources.
Line36 It’s usually too much trouble to apply private patches every time there’s a new
Line37 version. If we can’t change an API, then we can’t respond to any design feedback
Line38 we get from writing unit tests that touch it. Whatever alarm bells the unit tests
Line39 69
Line40 
Line41 
Line42 ---
