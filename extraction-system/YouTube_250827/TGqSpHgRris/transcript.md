# AI Writes Better Code With Test Driven Development

**Extracted Time:** 2025-08-27 16:44:25

---

[00:00] Everybody wants production ready AI
[00:02] code, but the brutal truth is AI code
[00:04] breaks in production more often than
[00:06] not. And in this video, I'm going to
[00:08] solve that problem for you because I'm
[00:09] going to teach you how you can make your
[00:11] AI agent test its own code using
[00:14] testdriven development. This means that
[00:16] AI will first write the tests to
[00:19] actually know whether its implementation
[00:20] is correct or not, thereby being a self-
[00:23] testing AI agent. And to prove that this
[00:25] works, I'm going to be implementing this
[00:27] strategy on a codebase that uses both
[00:29] Python as well as Java. So that no
[00:31] matter what programming language you
[00:33] use, you know how to use the strategy
[00:35] properly like a senior engineer. So
[00:37] let's get started. Welcome to our test
[00:39] application of today, an auction site
[00:42] that's implemented in both Python as
[00:43] well as Java. And this front end
[00:45] interacts with both of these backends at
[00:47] once. And these backends actually
[00:49] communicate over the same database. So,
[00:51] for example, I can actually create a
[00:53] sample auction on the Python site here.
[00:55] And then let's go ahead and bid on this
[00:57] Raspberry Pi cluster kit with Python
[00:59] Pete. I'm going to bid $250 like so. And
[01:03] then you can indeed see that now I am
[01:04] the highest bidder. And if I switch to
[01:06] Java side of things, I can actually
[01:08] enter a bid here as well. I can, for
[01:10] example, say that I want to bid 270
[01:12] bucks with Java Jane. So, I'm going to
[01:14] go ahead and place a bid. And you can
[01:16] actually see now that my bid must be at
[01:17] least $275
[01:19] because this actually has a current
[01:21] price and then a minimum increment. So,
[01:23] okay, we'll go ahead and actually bid
[01:25] 275 bucks then. And there we go. We can
[01:29] even for example close the current
[01:30] auction
[01:32] and then go ahead and create a new
[01:34] sample auction in the Java side as well
[01:36] just to show you that these backends are
[01:38] interoperable. They both have the same
[01:40] endpoints. Now, we are going to be
[01:42] implementing a new feature on this
[01:43] auctioning website, namely the ability
[01:46] to set the price at which an item can be
[01:48] immediately purchased. You see this a
[01:50] lot on platforms like eBay, right? Where
[01:51] you're able to just bid a specific
[01:53] amount and then the item is guaranteed
[01:55] to be yours. So, let's go ahead and see
[01:57] how we're going to implement that in
[01:59] both of these backends using testdriven
[02:01] development. First, we have to explore
[02:03] the codebase. So, let's go ahead and
[02:04] jump right into Visual Studio Code. In
[02:06] here, you can actually see that we have
[02:08] a couple of folders. You can see here
[02:10] how we have a Java backend, a Python
[02:12] backend, and this simple web interface,
[02:14] which is just an HTML file. And to build
[02:17] this new feature, I actually have
[02:19] prepared a prompt. And this prompt will
[02:21] actually be included in the description
[02:22] down below. No need to worry about that
[02:24] for now. And this prompt actually
[02:26] describes how Claw Code should implement
[02:29] a new feature using test-driven
[02:31] development. So, let's actually go ahead
[02:33] and check out what we're going to be
[02:34] building. We're going to be building a
[02:36] buy it now feature for the auctioning
[02:38] system. Now the thing is there's a lot
[02:40] of requirements here about adding an
[02:42] optional field, setting a certain buyout
[02:45] price that must be higher than the
[02:47] starting price etc. But the process of
[02:50] building this feature doesn't start with
[02:52] actually creating the code for the
[02:53] feature itself. No, actually test-driven
[02:56] development is a form of development
[02:58] where you first write the tests for your
[03:00] feature which will obviously fail
[03:02] because the code has not been
[03:03] implemented yet. And then from that
[03:05] point forward, your AI agent will
[03:07] implement the actual code. And the
[03:09] beautiful part is after it has
[03:11] implemented the code, it can run all of
[03:13] the tests again. And if they all pass,
[03:16] then you know that your code is actually
[03:18] genuinely functional. And of course, you
[03:20] can have a bit of a human in the loop
[03:22] element here as well, where you can, for
[03:23] example, first check the unit tests
[03:26] before you let the AI agent actually
[03:28] write the code to make sure that the
[03:30] tests already match your expectation. So
[03:32] in this case, what's actually going to
[03:34] happen is we're going to be implementing
[03:35] eight test cases. For example, creating
[03:38] an auction with a valid buyout price,
[03:40] but we also want to test some edge
[03:42] cases, right? That's how you're going to
[03:43] get production ready code. For example,
[03:46] we want to make sure that auctions can
[03:49] still be created without a buyout price
[03:51] to make sure that we have backwards
[03:52] compatibility with how the system worked
[03:54] before. So that's really how this prompt
[03:57] works on the high level. But in order to
[03:59] do test-driven development, you do
[04:01] actually need an existing test suite. In
[04:03] this case, if we open for example the
[04:04] Python backend folder, you will see how
[04:07] we actually have a test auction service
[04:09] Python file and this file contains our
[04:12] current unit tests. Similarly on the
[04:15] Java side of things, if we go into
[04:16] source, you can actually see we have a
[04:18] test folder here as well. And you can
[04:19] see how we actually have various tests,
[04:21] for example, for the auction service.
[04:23] And this is basically the test suite
[04:25] that Claude code is going to be
[04:27] extending with test-driven development
[04:29] before it actually implements the new
[04:31] bidding feature. In any case, enough
[04:33] talking. Let's get coding. So, what I'm
[04:35] going to do is I'm actually going to go
[04:37] ahead and open two new windows because I
[04:40] want to implement this feature on both
[04:42] the Java back end as well as the Python
[04:44] back end. But I'm not going to make
[04:45] Cloud Code do both backends at once.
[04:47] That's just asking for problems. I want
[04:49] Cloud Code to be able to focus on one
[04:51] programming language at a time. All
[04:52] right. So, I set up two terminal
[04:54] windows, one for the Python backend and
[04:56] then one for the Java backend. And all
[04:58] I'm going to do now is actually just
[04:59] start up two clawed code windows. And
[05:01] I'm going to say proceed for this one. I
[05:03] do trust my own back end, of course. And
[05:06] then what I'm going to do is I'm
[05:08] actually just going to paste this
[05:09] test-driven development feature prompt
[05:11] because it already includes all of the
[05:13] directives that Claude Code needs to get
[05:15] started on writing the actual test
[05:17] first. So, we're going to paste the
[05:18] exact same prompt into both of these
[05:21] Cloud Code sessions. And in a way, we're
[05:23] actually going to be parallelizing this
[05:25] effort, right? Because we're going to
[05:26] have two agents working on both of the
[05:29] actual backends at the same time. Now,
[05:32] you can actually see here that it's
[05:34] going to be starting to implement this
[05:36] feature by using strict testdriven
[05:38] development methodology. And while it's
[05:40] coming up with the first test, I just
[05:41] wanted to let you know that watching
[05:42] this video until the very end is very
[05:44] important because there's so much
[05:46] content out there nowadays that tries to
[05:48] make you believe that AI coding will 100
[05:50] extra productivity and that AI code can
[05:52] just oneshot the most complex
[05:54] applications out there. But this is not
[05:56] true. AI coding has been a great
[05:58] productivity booster for me as an actual
[06:00] senior engineer, but it has its limits.
[06:02] But by using real software methodologies
[06:04] like test-driven development, you can
[06:07] actually write productionready AI code.
[06:09] You just have to follow tutorials like
[06:11] this one and really understand how to
[06:13] write proper AI code first. There are a
[06:15] lot of distracting methodologies out
[06:17] there that people try to teach you like
[06:19] the BMAT method. And I'm not saying that
[06:21] these methods are bad. It's just that it
[06:23] doesn't compensate for lack of skills.
[06:25] If you for example don't know how to
[06:27] code, then you are going to get stuck
[06:29] with AI coding no matter what method
[06:31] you're using because it's going to make
[06:32] a mistake now and then and then if you
[06:34] don't know any Python or Java then how
[06:36] are you going to fix this application?
[06:38] That's right, you will not be able to
[06:40] and that's where you get stuck. So
[06:42] actually understanding how to code
[06:43] properly is super important and that's
[06:46] what you're learning today because
[06:47] test-driven development has been a
[06:48] tested framework that has been used in
[06:50] software development for many years now.
[06:52] Okay, enough theoretical talk. Let's
[06:54] actually see what cloud code is up to
[06:56] right now. And you can actually see that
[06:58] it's understood the codebase structure
[07:00] and of course it's explored different
[07:02] files for the Java side of things
[07:04] compared to the Python files. The Python
[07:07] files are a lot flatter. There's a lot
[07:08] more included in one single file whereas
[07:10] the Java files are a little bit more
[07:12] split apart. It's an interesting
[07:13] difference between writing Java and
[07:15] Python code. Right. And now you can see
[07:18] that the first failing test has been
[07:19] written. I'm going to give this terminal
[07:21] a little bit more room so you can see
[07:22] what's going on. I'm going to go ahead
[07:23] and allow it to make these edits. And
[07:26] then if we check out our git work tree,
[07:28] you can see that finally we have our
[07:29] first test here. This is a new test that
[07:32] will actually fail because if you look
[07:34] here, you can actually see that set
[07:36] buyout price is not even a valid method
[07:38] because it's not been implemented yet.
[07:40] That's a good thing. That's how we're
[07:41] actually approaching this test-driven
[07:43] development properly. So now what you
[07:45] can see is that claw code is going to
[07:47] run all tests to confirm that these new
[07:50] tests do fail. So here you go. It's
[07:52] written a bunch of new failing tests and
[07:54] now it's actually going to go ahead and
[07:55] run all of the tests. And I think I can
[07:58] actually show you if I do controlr here
[08:00] that a lot of these tests are failing.
[08:02] That's exactly what we want. So we can
[08:04] go ahead and toggle back and you can
[08:06] indeed see that in this case that's a
[08:08] great thing. Cloud code is aware that
[08:09] it's supposed to be failing. And now
[08:11] it's actually going to be implementing
[08:12] the minimum code to make the tests pass.
[08:15] And this is a super important element as
[08:17] well. A lot of the times AI code is
[08:19] super verbose and it will write way more
[08:21] code than it needs to. In this case,
[08:23] cloud code will write the minimum amount
[08:25] of code that it needs to in order to
[08:27] make the tests pass. And now on the left
[08:29] side here, you can see that it's
[08:30] starting to actually finish up those
[08:32] tests on the Python file as well. So
[08:34] that's great. I'm going to go ahead and
[08:36] approve all of that there too. And you
[08:38] can see here how the approach is the
[08:40] exact same. It doesn't matter whether
[08:42] you're using a strict language like Java
[08:44] or a more loosely typed language like
[08:45] Python. You can use this method
[08:47] regardless of the programming language.
[08:49] And indeed here you can see that the
[08:51] Python tests are failing as well which
[08:52] is actually expected. Now I'm going to
[08:54] go ahead and give cloud code the time
[08:56] that it needs to actually write the
[08:57] implementation code. And then we'll have
[08:59] a look at whether the tests will pass.
[09:02] So on the bottom right you can see after
[09:03] a while cloud code has finished the
[09:05] implementation and now when running all
[09:07] of the tests you can see that all the
[09:09] tests are actually passing which is
[09:11] perfect. And now you can actually see
[09:13] here on the left in our change log that
[09:15] we actually have modifications in the
[09:17] actual root application. So for example,
[09:19] we now have a new big decimal buyout
[09:21] price. And then if we go into the
[09:22] auction service, you can actually see
[09:24] that if the buyout price is included, we
[09:27] do a couple of validations which all
[09:29] have to do with making sure that these
[09:31] tests that it was creating earlier can
[09:34] actually pass. For example, there are
[09:36] tests here like fail when buyout price
[09:38] is less than or equal to starting price,
[09:41] which is a great test case, right?
[09:43] Because we want to make sure that the
[09:44] buyer price has to be more than the
[09:46] starting price. It doesn't make sense
[09:47] for the auction system otherwise. So,
[09:49] you can see here how it actually works
[09:51] very well. Now, let's go ahead and see
[09:53] how far ahead it is with the Python
[09:55] implementation. And you can see that
[09:57] it's running all the tests, but there
[09:58] are some issues here. It seems like
[10:00] decimal places is not valid for
[10:02] Padantics decimal field. Now, it's
[10:04] interesting that it actually oneshot all
[10:06] the Java unit tests, but it's having
[10:08] some trouble with Python. And that has
[10:10] to do with the fact that Java is a much
[10:12] more strictly typed language, which is
[10:14] also something that is really beneficial
[10:16] for an AI coding mechanism. Because if
[10:18] you look here on the bottom right, you
[10:19] can actually compile the code as well
[10:21] with a language like Java, which gives
[10:23] you a lot of guarantees on the I guess
[10:26] baseline quality of the code. Just
[10:27] because code is compiling doesn't mean
[10:29] that the code is perfect but it's
[10:30] definitely a step forward and you know
[10:32] that the code is at least meeting some
[10:34] kind of minimum requirement there right
[10:36] so of course if we try and run clean
[10:38] compile it will actually work because
[10:40] claude code was able to oneshot the Java
[10:43] implementation here whereas here on the
[10:46] Python side of things finally it did
[10:48] actually manage to implement the test
[10:50] suite correctly but it's actually a
[10:52] relatively simple feature and you can
[10:53] see here already how the behavior drifts
[10:55] between these two different programming
[10:57] languages. And that's another great
[10:59] learning point for you from this video.
[11:00] You should pick the language that you're
[11:02] the most comfortable with, but it can be
[11:04] beneficial to learn a more strict typed
[11:07] language like Java or C. You can also
[11:10] implement types in a programming
[11:11] language like Python, but it's still not
[11:13] really the same as a language that can
[11:15] compile in a real way like a Java
[11:18] application. Anyway, I digress. We now
[11:21] have code that runs on the back end of
[11:23] both the Java application and the Python
[11:25] one, which is great. But I'm sure that
[11:27] you want to see some proof of this, some
[11:29] actual proof in the web application
[11:31] instead of it just being in the back
[11:32] ends. So let's go ahead and implement a
[11:34] change in our HTML page so we can
[11:37] actually interact with this new feature.
[11:39] What I'm going to be doing is I'm going
[11:41] to go to my files here and then I'm
[11:43] going to go ahead and drag in index.html
[11:45] HTML and I'm going to do that inside of
[11:47] the Java chat session that I have
[11:49] because the Java implementation is
[11:51] strictly typed. So I trust this a little
[11:53] bit more compared to the Python
[11:54] implementation since I have the luxury
[11:56] to choose anyway. And I'm going to say
[11:58] the following. This is our web page to
[12:01] interact with the back end. In fact, we
[12:06] interact with both a Java and Python
[12:10] back end with the same
[12:13] implementation.
[12:15] Given your latest Java edition, rework
[12:20] the HTML/JavaScript
[12:24] to include the ability to handle the
[12:28] buyout
[12:29] price. The sample auctions that the
[12:34] front end calls should include a buyout
[12:38] price and this price should of course be
[12:42] displayed in the front end. Here we go.
[12:46] This is what I want to do now. I wanted
[12:48] to rework that HTML file. So while cloud
[12:50] code is working on this implementation,
[12:52] I just wanted to let you know that these
[12:54] kinds of real AI coding strategies is
[12:56] what I focus on in my AI native engineer
[12:58] community. And in this community, you
[13:00] can learn how to accelerate yourself
[13:01] with AI regardless of whether you are
[13:03] working on your career or a business. So
[13:06] you can check out the community in the
[13:07] link in the description below.
[13:08] Otherwise, I'll see you in just a second
[13:10] and we'll check out how this has been
[13:12] implemented in our front end. So it
[13:14] seems like it's done with the front end
[13:15] implementation. It wants to test the
[13:17] front end itself, but I'm just going to
[13:18] go ahead and exit out of the session
[13:20] because we're going to do that manually,
[13:21] right? So in our application, I can now
[13:24] go ahead and create a new sample
[13:25] auction. And then you will see that we
[13:27] actually have a buyout price set of
[13:29] $150. So I can actually just create an
[13:31] initial bid of 55 bucks which will work
[13:34] just fine. And then now I can actually
[13:35] create a buyout price bid of 155 bucks.
[13:39] So I'm going to go ahead and place a bit
[13:40] here. And then actually something seems
[13:42] to go wrong. So what seems to happen
[13:44] here is that I place a bid and the
[13:46] auction is closed off. But the thing is
[13:48] my front end doesn't really know that
[13:50] that is a possibility. my front end
[13:52] continuously tries to fetch the latest
[13:54] auction and it doesn't really have a way
[13:56] of knowing that the auction was actually
[13:58] closed off because our front end doesn't
[14:00] actually have any logic for when a
[14:02] buyout price is reached. And this
[14:04] actually shows you why test-driven
[14:06] development is so important. We did not
[14:08] do test-driven development for our front
[14:10] end. So our front end does sort of work
[14:13] now, but it's already running into
[14:14] issues. And that is the reality of AI
[14:16] coding without a proper framework like
[14:18] test-driven development. So what I have
[14:20] to do now is now I have to go back into
[14:23] claude and actually just communicate
[14:24] that this issue exists and then let's
[14:27] see if we can fix it. So I can for
[14:28] example say here the front end does not
[14:32] know how to deal with a bid that's
[14:36] placed that actually buys out the item
[14:41] because the front end continuously
[14:44] refreshes the auction.
[14:47] I actually get an ID error. And you can
[14:50] see here that now I have to go back to
[14:52] Claude and try to fix the error. If I
[14:54] had actually done test-driven
[14:55] development for my front end from the
[14:57] very beginning, I probably could have
[14:59] oneshot that implementation as well.
[15:01] This shows you the reality of AI coding.
[15:03] Other content would probably not show
[15:05] you this and just act like everything is
[15:06] working. But this is the truth that you
[15:08] see here on this channel. You have to
[15:10] use the right coding methodology to
[15:12] actually get success out of AI coding.
[15:14] Looks like we're done. Let's go back
[15:16] into our front end. Give it a full
[15:17] refresh just to make sure. We're going
[15:19] to go ahead and create a new sample
[15:20] auction. And then I'm just going to go
[15:21] ahead and buy that out straight away
[15:23] with 500 bucks. Going to go ahead and
[15:25] place a bid. And there you go. Now we
[15:27] can actually see that the front end is
[15:29] able to deal with the new buying out
[15:31] logic. And this just shows you how
[15:33] powerful using the right methodologies
[15:35] can be for AI coding. So I hope that
[15:37] from this video you've learned that
[15:39] using the right methodology to do AI
[15:41] coding can give you so many amazing real
[15:43] results. If you want to escape the trap
[15:45] of vibe coding and actually get
[15:48] productive with AI as an engineer, you
[15:50] should definitely check out my AI native
[15:51] engineering community in the link in the
[15:53] description below. And I hope to see you
[15:55] there.