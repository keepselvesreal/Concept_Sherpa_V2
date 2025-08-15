# Part 3 Introduction

**Level:** 1
**페이지 범위:** 273 - 275
**총 페이지 수:** 3
**ID:** 113

---

=== 페이지 273 ===
Part 3
Maintainability
A
fter a month, the Klafim project enters what Alabatross calls the mainte-
nance phase. Small new features need to be added on a weekly basis. Bugs need to be
fixed; nothing dramatic....
Monica, Theo’s boss, decides to allocate Dave to the maintenance of the Klafim
project. It makes sense. Over the last few months, Dave has demonstrated a great atti-
tude of curiosity and interest, and he has solid programming skills. Theo sets up a
meeting with Joe and Dave, hoping that Joe will be willing to teach DOP to Dave so
that he can continue to advance the good work he’s already done on Klafim. Theo
and Dave place a conference call to Joe.
Theo Hi, Joe. Will you have time over the next few weeks to teach Dave the
principles of DOP?
Joe Yes, but I prefer not to.
Dave Why? Is it because I don’t have enough experience in software develop-
ment? I can guarantee you that I’m a fast learner.
Joe It has nothing to do with your experience, Dave.
Theo Why not then?
Joe Theo, I think that you could be a great mentor for Dave.
Theo But, I don’t even know all the parts of DOP!
Dave Come on! No false modesty between us, my friend.
Joe Knowledge is never complete. As the great Socrates used to say, “The more
I know, the more I realize I know nothing.” I’m confident you will be able
to learn the missing parts by yourself and maybe even invent some.
Theo How will I be able to invent missing parts?

=== 페이지 274 ===
246 PART 3 Maintainability
Joe You see, DOP is such a simple paradigm that it’s fertile material for innovation.
Part of the material I taught you I learned from others, and part of it was an
invention of mine. If you keep practicing DOP, I’m quite sure you, too, will
come up with some inventions of your own.
Theo What do you say Dave? Are you willing to learn DOP from me?
Dave Definitely!
Theo Joe, will you be continue to be available if we need your help from time to time?
Joe Of course!

=== 페이지 275 ===
Advanced data
validation
A self-made gift
This chapter covers
 Validating function arguments
 Validating function return values
 Data validation beyond static types
 Automatic generation of data model diagrams
 Automatic generation of schema-based unit tests
As the size of a code base grows in a project that follows DOP principles, it becomes
harder to manipulate functions that receive and return only generic data. It is hard
to figure out the expected shape of the function arguments, and when we pass
invalid data, we don’t get meaningful errors.
Until now, we have illustrated how to validate data at system boundaries. In this
chapter, we will illustrate how to validate data when it flows inside the system by
defining data schemas for function arguments and their return values. This allows
us to make explicit the expected shape of function arguments, and it eases develop-
ment. We gain some additional benefits from this endeavor, such as automatic gen-
eration of data model diagrams and schema-based unit tests.
247
