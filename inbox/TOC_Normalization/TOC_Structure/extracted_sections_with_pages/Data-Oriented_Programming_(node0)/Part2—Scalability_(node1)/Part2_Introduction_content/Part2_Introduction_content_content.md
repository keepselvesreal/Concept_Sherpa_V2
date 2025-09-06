# Part2 Introduction content

**페이지**: 165-167
**계층**: Data-Oriented Programming (node0) > Part2—Scalability (node1)
**추출 시간**: 2025-08-06 19:46:59

---


--- 페이지 165 ---

Part 2
Scalability
T
heo feels a bit uncomfortable about the meeting with Joe. He was so enthusias-
tic about DOP, and he was very good at teaching it. Every meeting with him was an
opportunity to learn new things. Theo feels lot of gratitude for the time Joe spent
with him. He doesn’t want to hurt him in any fashion. Surprisingly, Joe enters the
office with the same relaxed attitude as usual, and he is even smiling.
Joe I’m really glad that you got the deal with Nancy.
Theo Yeah. There’s lot of excitement about it here in the office, and a bit of
stress too.
Joe What kind of stress?
Theo You know.... We need to hire a team of developers, and the deadlines
are quite tight.
Joe But you told me that you won’t use DOP. I assume that you gave regular
deadlines?
Theo No, my boss Monica really wanted to close the deal. She feels that success
with this project is strategically important for Albatross, so it’s worthwhile
to accept some risk by giving what she calls an “optimistic” time estima-
tion. I told her that it was really an unrealistic time estimation, but Mon-
ica insists that if we make smart decisions and bring in more developers,
we can do it.
Joe I see. Now I understand why you told me over the phone that you were
very busy. Anyway, would you please share the reasons that made you
think DOP wouldn’t be a good fit at scale?

--- 페이지 165 끝 ---


--- 페이지 166 ---

138 PART 2 Scalability
Theo First of all, let me tell you that I feel lot of gratitude for all the teaching you
shared with me. Reimplementing the Klafim prototype with DOP was really
fun and productive due to the flexibility this paradigm offers.
Joe I’m happy that you found it valuable.
Theo But, as I told you over the phone, now we’re scaling up into a long-term project
with several developers working on a large code base. We came to the conclu-
sion that DOP will not be a good fit at scale.
Joe Could you share the reasons behind your conclusion?
Theo There are many of them. First of all, as DOP deals only with generic data struc-
tures, it’s hard to know what kind of data we have in hand, while in OOP, we
know the type of every piece of data. For the prototype, it was kind of OK. But
as the code base grows and more developers are involved in the project, it
would be too painful.
Joe I hear you. What else, my friend?
Theo Our system is going to run on a multi-threaded environment. I reviewed the
concurrency control strategy that you presented, and it’s not thread-safe.
Joe I hear you. What else, my friend?
Theo I have been doing a bit of research about implementing immutable data struc-
tures with structural sharing. I discovered that when the size of the data
structures grows, there is a significant performance hit.
Joe I hear you. What else?
Theo As our system grows, we will use a database to store the application data and
external services to enrich book information, and in what you have showed me
so far, data lives in memory.
Joe I hear you. What else, my friend?
Theo Don’t you think I have shared enough reasons to abandon DOP?
Joe I think that your concerns about DOP at scale totally make sense. However, it
doesn’t mean that you should abandon DOP.
Theo What do you mean?
Joe With the help of meditation, I learned not be attached to the objections that
flow in my mind while I’m practicing. Sometimes all that is needed to quiet our
minds is to keep breathing; sometimes, a deeper level of practice is needed.
Theo I don’t see how breathing would convince me to give DOP a second chance.
Joe Breathing might not be enough in this case, but a deeper knowledge of DOP
could be helpful. Until now, I have shared with you only the material that was
needed in order to refactor your prototype. In order to use DOP in a big proj-
ect, a few more lessons are necessary.
Theo But I don’t have time for more lessons. I need to work.
Joe Have you heard the story about the young woodcutter and the old man?
Theo No.
Joe It goes like this.

--- 페이지 166 끝 ---


--- 페이지 167 ---

PART 2 Scalability 139
The young woodcutter and the old man
A young woodcutter strained to saw down a tree. An old man who was watching near-
by asked, “What are you doing?”
“Are you blind?” the woodcutter replied. “I’m cutting down this tree.”
The old man replied, “You look exhausted! Take a break. Sharpen your saw.”
The young woodcutter explained to the old man that he had been sawing for hours
and did not have time to take a break.
The old man pushed back, “If you sharpen the saw, you would cut down the tree much
faster.”
The woodcutter said, “I don’t have time to sharpen the saw. Don’t you see, I’m too
busy!”
Theo takes a moment to meditate on the story. He wonders if he needs to take the time to
sharpen his saw and commit to a deeper level of practice.
Theo Do you really think that with DOP, it will take much less time to deliver the
project?
Joe I know so!
Theo But if we miss the deadline, I will probably get fired. I’m the one that needs to
take the risk, not you.
Joe Let’s make a deal. If you miss the deadline and get fired, I will hire you at my
company for double the salary you make at Albatross.
Theo And what if we meet the deadline?
Joe If you meet the deadline, you will probably get promoted. In that case, I will
ask you to buy a gift for my son Neriah and my daughter Aurelia.
Theo Deal! When will I get my first lesson about going deeper into DOP?
Joe Why not start right now?
Theo Let me reschedule my meetings.

--- 페이지 167 끝 ---
