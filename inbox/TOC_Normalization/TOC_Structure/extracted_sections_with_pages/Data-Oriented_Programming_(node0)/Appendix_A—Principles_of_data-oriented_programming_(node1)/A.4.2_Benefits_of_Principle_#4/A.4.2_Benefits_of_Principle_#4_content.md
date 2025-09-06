# A.4.2 Benefits of Principle #4

**페이지**: 359-360
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:34

---


--- 페이지 359 ---

Summary 331
Dave Really?
Theo Yes. I’ll be traveling around the world for a couple of months.
Dave And after that, will you go back to work in programming?
Theo I’m not sure.
Dave Do you have other projects in mind?
Theo I’m thinking of writing a book.
Dave A book?
Theo Yes. DOP has been a meaningful journey for me. I have learned some interest-
ing lessons about reducing complexity in programming, and I would like to
share my story with the community of developers.
Dave Well, if you are as good of a storyteller as you are as a teacher, I am sure your
book will be a success.
Theo Thank you, Dave!
Monica, Dave, Nancy, Joe, and all the other Albatross employees raise their glasses to
Theo’s health and exclaim together, “Cheers! Here’s to a successful book.”
Summary
 We reproduce a scenario by capturing the context in which a function is called
and replaying it either in the REPL or in a unit test. In this chapter, we call it
context capturing.
 In DOP, a function context is made only of data.
 There are various locations to capture a function context—the clipboard, the
console, a file.
 We are able to capture a function’s context because data is represented with a
generic data structure and, therefore, it is easily serializable.
 Replaying a scenario in the REPL provides a short feedback loop that allows us
to be effective when we want to fix our code.
 When we execute a function with a captured context, the behavior of the func-
tion is guaranteed to be the same as long as it only manipulates immutable data
as specified by DOP.
 In modules that deal with immutable data, function behavior is deterministic—
the same arguments always lead to the same return values.
 The function context is made of the values of the function arguments.
 The REPL (Read Eval Print Loop), sometimes called language shell, is a pro-
gramming environment that takes pieces of code, executes them, and displays
the result.
 In order to copy and paste a generic data structure, we serialize and deserialize it.

--- 페이지 359 끝 ---


--- 페이지 360 ---

332 CHAPTER 15 Debugging
 Reproducibility allows us to reproduce a scenario in a pristine environment.
 The two conditions for reproducibility in programming are immutability and
ease of (de)serialization.
Lodash functions introduced in this chapter
Function Description
find(coll, pred) Iterates over elements of coll, returning the first element for which pred
returns true

--- 페이지 360 끝 ---
