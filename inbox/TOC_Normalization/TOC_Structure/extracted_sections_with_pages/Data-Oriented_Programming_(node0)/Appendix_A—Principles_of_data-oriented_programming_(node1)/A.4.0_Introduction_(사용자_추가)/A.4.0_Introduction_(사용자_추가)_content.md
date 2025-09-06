# A.4.0 Introduction (사용자 추가)

**페이지**: 358-359
**계층**: Data-Oriented Programming (node0) > Appendix A—Principles of data-oriented programming (node1)
**추출 시간**: 2025-08-06 19:47:33

---


--- 페이지 358 ---

330 CHAPTER 15 Debugging
Dave Are there databases like that for real?
Theo Yes. For instance, the Datomic immutable database is used by some digital
banks.
 NOTE See https://www.datomic.com for more information on the Datomic transac-
tional database.
Dave But most databases don’t provide such a guarantee!
Theo Right, but in practice, when we’re debugging an issue in our local environ-
ment, data usually doesn’t change.
Dave What do you mean?
Theo Take, for instance, Klafim’s database. In theory, between the time you trigger
the search endpoint and the time you replay the search code from the REPL
with the same context, a book might have been borrowed, and its availability
state in the database has changed. This leads to a difference response to the
search query.
Dave Exactly.
Theo But in practice, you are the only one that interacts with the system in your local
environment. Therefore, it should not happen.
Dave I see. Because we are at the Museum of Science, would you allow me an anal-
ogy with science?
Theo Of course!
Dave In a sense, external data sources are like hidden variables in quantum physics.
In theory, they can alter the result of an experiment for no obvious reason. But
in practice, our physical world looks stable at the macro level.
With today’s discussion at an end, Theo searches his bag to find a parcel wrapped with gift
wrap from the museum’s souvenir shop, which he hands to Dave with a smile. Dave opens
the gift to find a T-shirt. On one side there is an Albert Einstein avatar and his famous
quote: “God does not play dice with the universe”; on the other side, an avatar of Alan Kay
and his quote: “The last thing you want to do is to mess with internal state.”
Dave thanks Theo for his gift. Theo can feel a touch of emotion at the back of his
throat. He’s really enjoyed playing the role of mentor with Dave, a rather skilled student.
Farewell
A week after the meeting with Dave at the museum, Theo invites Joe and Nancy for his
farewell party at Albatross. This is the first time that Joe meets Nancy, and Theo takes the
opportunity to tell Nancy that if the Klafim project met its deadlines, it was thanks to Joe.
Everyone is curious about the name of the company Theo is going to work for, but no one
dares to ask him. Finally, it’s Dave who gets up the courage to ask.
Dave May I ask you what company are you going to work for?
Theo I’m going to take a break.

--- 페이지 358 끝 ---


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
