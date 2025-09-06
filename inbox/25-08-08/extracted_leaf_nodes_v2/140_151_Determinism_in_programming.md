# 15.1 Determinism in programming

**메타데이터:**
- ID: 140
- 레벨: 2
- 페이지: 340-341
- 페이지 수: 2
- 부모 ID: 138
- 텍스트 길이: 6483 문자

---

in programming
After a few months, Theo calls Dave to tell him that he’s leaving Albatross. After Dave
recovers from this first surprise, he’s given another, more pleasant one. Theo informs Dave
that after consulting with the management team, they have decided that Dave will be in
charge of DOP at Albatross. In addition to the farewell at the office next week, Theo invites
Dave for a last one-on-one work session at the Exploratorium Museum of Science.
During their visit, Dave particularly enjoys the Cells to Self exhibit in the Living Systems
gallery; meanwhile, Theo is having fun with the Colored Shadows exhibit in the Reflec-
tions gallery. After the visit, Theo and Dave settle in the back row of the museum’s audito-
rium and open their laptops.
Dave Why did you want our last meeting to happen here at the Museum of Science?
Theo Remember when Joe told us that someday we’d be able to innovate in DOP?
Dave Yes.
Theo Well, that day may have come. I think I have discovered an interesting connec-
tion between DOP and science, and it has implications in the way we debug a
program.
Dave I’m curious.
Theo Do you believe in determinism?
Dave You mean that everything that happens in the universe is predestined and that
free will is an illusion?
Theo No, I don’t want to get into a philosophy. This is more of a scientific question.
Do you think that the same causes always produce the same effects?
Dave I think so. Otherwise, each time I use an elevator, I’d be scared to death that
the laws of physics have changed, and the elevator might go down instead of
up, or even crash!
Theo What about determinism in programming?
Dave How would you define causes and effects in programming?
Theo Let’s say, for the sake of simplicity, that in the context of programming, causes
are function arguments and effects are return values.
Dave What about side effects?
Theo Let’s leave them aside for now.
Dave What about the program state? I mean, a function could return a different
value for the same arguments if the program state changes.
Theo That’s why we should avoid state as much as possible.
Dave But you can’t avoid state in real-life applications!
Theo Right, but we can minimize the number of modules that deal with state. In fact,
that’s exactly what DOP has encouraged us to do: only the SystemState mod-
ule deals with state, and all other modules deal with immutable data.
Dave Then, I think that in modules that deal with immutable data, determinism as
you defined it holds. For the same arguments, a function will always return the
same value.
TIP In modules that deal with immutable data, function behavior is deterministic—the
same arguments always lead to the same return values.

15.1 Determinism in programming 313
Theo Perfect. Let’s give a name to the values of the function arguments that a function
is called with: the function run-time context or, in short, the function context.
Dave I think I see what you mean. In general, the function context should involve
both the function arguments and the program state. But in DOP, because we
deal with immutable data, a function context is made only of the values of the
function arguments.
TIP In DOP, the function context is made of the values of the function arguments.
Theo Exactly! Now, let’s talk about reproducibility. Let’s say that you want to capture
a function context and reproduce it in another environment.
Dave Could you be a bit more concrete about reproducing a function context in
another environment?
Theo Take, for example, a web service endpoint. You trigger the endpoint with some
parameters. Inside the program, down the stack, a function foo is called. Now,
you want to capture the context in which foo is called in order to reproduce
later the same behavior of foo.
Dave We deal with immutable data. So, if we call foo again with the same arguments,
it will behave the same.
Theo The problem is how do you know the values of the function arguments?
Remember that we didn’t trigger foo directly. We triggered the endpoint.
Dave That’s not a problem. You use a debugger and set a breakpoint inside the code of
foo, and you inspect the arguments when the program stops at the breakpoint.
Theo Let’s say foo receives three arguments: a number, a string, and a huge nested map.
How do you capture the arguments and replay foo with the same arguments?
Dave I am not sure what you mean exactly by replaying foo?
Theo I mean executing foo in the REPL.
 NOTE The REPL (Read Eval Print Loop), sometimes called language shell, is a pro-
gramming environment that takes pieces of code, executes them, and displays the
result. See table 15.1 for a list of REPLs for different programming languages.
Table 15.1 REPLs per programming language
JavaScript (Browser) Browser console
Node.js Node CLI
Java JShell
C# C# REPL
Python Python interpreter
Ruby Interactive Ruby
Dave Does the REPL have to be part of the process that I’m debugging?
Theo It doesn’t have to be. Think of the REPL as a scientific lab, where developers
perform experiments. Let’s say you’re using a separate process for the REPL.

314 CHAPTER 15 Debugging
Dave OK. For the number and the string, I can simply copy their values to the clip-
board, paste them to the REPL, and execute foo in the REPL with the same
arguments.
Theo That’s the easy part. What about the nested map?
Dave I don’t know. I don’t think I can copy a nested map from a debugger to the
clipboard!
Theo In fact, JavaScript debuggers can. For instance, in Chrome, there is a Copy
option that appears when you right-click on data that is displayed in the browser
console.
Dave I never noticed it.
Theo Even without that, you could serialize the nested map to a JSON string, copy
the string to the clipboard, and then paste the JSON string to the REPL.
Finally, you could deserialize the string into a hash map and call foo with it.
Dave Nice trick!
Theo I don’t think of it as a trick, but rather as a fundamental aspect of DOP: data is
represented with generic data structures.
Dave I see. It’s easy to serialize a generic data structure.
TIP In order to copy and paste a generic data structure, we serialize and deserialize it.
Theo You just discovered the two conditions for reproducibility in programming.
Dave The first one is that data should be immutable.
Theo Right, and the second one?
Dave It should be easy to serialize and deserialize any data.
TIP The two conditions for reproducibility in programming are immutability and
ease of (de)serialization.