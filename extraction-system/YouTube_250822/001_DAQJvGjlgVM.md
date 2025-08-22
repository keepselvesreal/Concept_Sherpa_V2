# Building and prototyping with Claude Code

**Extracted Time:** 2025-08-22 15:43:39

---

[00:00] - These developers tend to like to run
[00:01] multiple Claude sessions at once,
[00:04] and they've started calling
this multi-Clauding.
[00:07] So you might see sessions
[00:08] where people have like six Claudes open
[00:10] on their computer at the same time.
[00:16] - Hey, I'm Alex.
[00:17] I lead Claude Relations here at Anthropic.
[00:19] Today we're gonna be
talking about Claude Code,
[00:21] and I'm joined by my colleague Cat.
[00:22] - Hey, I'm Cat.
[00:24] I'm the product manager for Claude Code.
[00:26] - Cat, I wanna kick this
off just talking about
[00:27] the insane rate of
shipping in Claude Code.
[00:30] It feels like literally every time
[00:31] I open it up in my terminal,
[00:33] there's a new product or a new feature,
[00:35] something for me to use.
[00:37] Can you walk me through
what the process looks like
[00:39] of the team going from an idea
[00:41] to actually shipping
something to end users?
[00:44] - Yeah, so the Claude Code team is full
[00:45] of very product-minded engineers
[00:47] and a lot of these features
are just built bottom-up.
[00:50] It's like you're a developer
[00:52] and you really wish you had this thing,
[00:54] and then you build it for yourself.
[00:56] And the way that our process works
[00:57] is instead of writing a doc,
[00:59] it's so fast to use Claude Code
[01:01] to prototype a feature
[01:03] that most of the time people
just prototype the feature
[01:06] and then they ship it
internally to "Ants".
[01:08] And if the reception is really positive,
[01:10] then that's a very strong signal
[01:12] that the external world will like it too.
[01:13] And that's actually our bar
for shipping it externally.
[01:17] And then of course there's always features
[01:19] that like aren't exactly right
[01:21] that need some tweaking.
[01:22] And if we feel like, okay,
"Ants" aren't really using it
[01:25] that much, then we just go
back to the drawing board
[01:28] and we say like, okay,
[01:29] what else could we change about this?
[01:31] - And when we say "Ants," do
we mean Anthropic employees?
[01:33] - Yes, yes.
- Yeah.
[01:34] That's really fascinating.
[01:36] I've never seen a product have as strong
[01:39] of like a "dogfooding"
loop as Claude Code.
[01:41] Do you think that's
something we purposely did
[01:44] or that just kind of naturally arise
[01:46] from the product itself?
[01:48] - It is quite intentional,
[01:49] and it's also a really important reason
[01:52] why Claude Code works so well.
[01:55] Because it's so easy to prototype
features on Claude Code,
[01:59] we do push people to
prototype as much as possible,
[02:03] but it's hard to reason about
[02:05] like exactly how a
developer will use a tool
[02:09] because developers are so heterogeneous
[02:11] in their workflows.
[02:12] So oftentimes, even if
you theoretically know
[02:15] you wanna do something,
[02:16] like even if you theoretically know
[02:18] that you wanna build an IDE integration,
[02:20] there's still a range
of like potential ways
[02:23] you could go about it.
[02:24] And often prototyping is the only way
[02:25] that you can really feel how the product
[02:28] will actually be in your workflow.
[02:30] So yeah, it's through the
process of "dogfooding"
[02:32] that we decide what version of
a feature we decide to ship.
[02:35] - I see.
[02:36] And there's something about the,
[02:38] almost like the flexibility
[02:39] but also the constraints
of the terminal too
[02:41] that allows for easy addition
of like new features,
[02:45] which I've kind of
noticed where it's like,
[02:47] because we have the primitives built out
[02:49] of like slash commands and things,
[02:50] it's easy to add another
one on top of that.
[02:53] - Yeah, it's totally
designed to be customizable.
[02:56] And because so many developers
[02:58] are familiar with the terminal,
[03:00] it makes like new feature
onboarding super straightforward,
[03:06] because for example, for
a feature like hooks,
[03:10] which lets you add a bit of determinism
[03:12] around Claude Code events,
[03:14] because every developer
knows how to write a script,
[03:19] and really at the end of the day,
[03:21] all a hook is, is a script.
[03:23] And so you don't need to
learn a new technology
[03:25] to customize Claude Code.
[03:27] You write this script that
you already know how to do
[03:30] and then you add it to one
of the Claude Code events
[03:33] and now you have some determinism.
[03:35] - We're really trying to meet customers
[03:37] or developers where they are
[03:39] with this tool.
- Definitely.
[03:41] - Switching gears slightly,
[03:43] so alongside this insane rate of shipping
[03:45] is also the insane growth
rate of Claude Code
[03:48] with developers everywhere.
[03:51] Can you walk me through
what that's been like
[03:53] to kind of be on this rocket ship
[03:54] and how are we seeing various developers,
[03:57] whether it's at startups or individuals
[03:59] or at even large enterprises, use Claude?
[04:01] - So one of the magical
things about Claude Code
[04:03] is that the onboarding is so smooth.
[04:07] After you do the NPM install,
[04:09] Claude Code kind of just
like works out of the box
[04:12] without any configuration.
[04:13] And this is true whether
you are an indie developer
[04:17] through to if you're an
engineer at a Fortune 500.
[04:21] I think this is the
magic behind Claude Code.
[04:23] Because it has access to
all of the local tools
[04:27] and files that you have,
[04:28] you have this like very clear mental model
[04:31] for what Claude Code is capable of.
[04:33] We do see different use
case patterns though
[04:36] between smaller companies and larger ones.
[04:39] We find that engineers
at smaller companies
[04:41] tend to run Claude more autonomously
[04:43] using things like "auto-accept mode,"
[04:46] which lets Claude make edits by itself
[04:48] without approval of each one.
[04:50] We also find that these developers
[04:52] tend to like to run multiple
Claude sessions at once,
[04:55] and they've started calling
this multi-Clauding.
[04:58] So you might see sessions
[05:00] where people have like six Claudes open
[05:02] on their computer at the same time.
[05:04] Maybe each of them are in
a different Git workspace
[05:07] or in a different copy of the Git repo,
[05:09] and they're just like
managing each of them.
[05:13] Whenever anyone stops
and asks for feedback,
[05:16] they'll jump in there and then send it off
[05:18] and let it continue running.
[05:20] And on the other end of the spectrum
[05:22] for larger companies,
[05:23] we find that engineers really
like to use "plan mode."
[05:26] So "plan mode" is a way for developers
[05:29] to tell Claude Code to take a second,
[05:32] explore the code base,
[05:34] understand the architecture,
[05:35] and create an engineering plan
[05:38] before actually jumping
into the code itself.
[05:40] And so we find that this is really useful
[05:43] for harder tasks and more complex changes.
[05:47] - So going back to multi-Clauding
[05:48] just 'cause I think that's
a fascinating concept.
[05:52] I'm sure we kind of imagined folks
[05:54] wanting to do things like that,
[05:56] but it was like somewhat surprising.
[05:59] Is there other things
in that domain of like,
[06:02] oh wow, this is a usage pattern
[06:04] that we really did not expect
[06:06] that have kind of popped up organically
[06:07] and we've shifted our
roadmap around a little bit?
[06:10] - Yeah, I think multi-Clauding
is the biggest one
[06:13] because this is something that we thought
[06:14] was just a power user feature
[06:17] that like a few people would wanna do.
[06:19] But in fact this is
actually a really common way
[06:21] in which people use Claude.
[06:23] And so for example,
[06:25] they might have one Claude instance
[06:26] where they only ask questions
[06:29] and this one doesn't edit code.
[06:31] That way they can have
another Claude instance
[06:32] in the same repo that does edit code
[06:35] and these two don't
interfere with each other.
[06:37] Other things that we've seen
[06:38] are people really like
to customize Claude Code
[06:41] to handle specialized tasks.
[06:44] So we've seen people build
like SRE agents on Claude Code,
[06:49] security agents, incident response agents.
[06:53] And what that made us realize
[06:55] is that integrations are so important
[06:57] for making sure Claude Code works well.
[06:59] And so we've been encouraging people
[07:00] to spend more time to
tell Claude Code about,
[07:04] hey, these are the CLI
tools we commonly use
[07:07] or to set up remote MCP servers
[07:09] to get access to logs and
ticket management software.
[07:12] - When these engineers are
customizing Claude Code,
[07:14] does that mean they're creating sub-agents
[07:17] or are they creating markdown files
[07:20] like CLAUDE.md files?
[07:22] How exactly are they creating these
[07:23] different types of agents?
[07:25] - Yeah, I think the most common ways
[07:27] that we've seen people customize
[07:28] is by investing a lot
into the CLAUDE.md file.
[07:32] So the CLAUDE.md file is
our concept of memory.
[07:35] And so it's the best place for you
[07:37] to tell Claude Code about
what your team's goals are,
[07:41] how the code is architected,
[07:43] any gotchas in the code base,
[07:47] any best practices.
[07:48] And investing in CLAUDE.md
[07:51] we've heard dramatically improves
[07:53] the quality of the output.
[07:55] The other way that people
customize Claude Code
[07:57] is by adding custom slash commands.
[08:00] So if there's a prompt
that you're always typing,
[08:03] you can add that into
the custom slash commands
[08:05] and you could also check these in
[08:07] so that you share them
with the rest of your team.
[08:09] And then you can also add custom hooks.
[08:12] So if for example,
[08:14] you want Claude Code to run lints
[08:17] before it makes a commit,
[08:19] this is something that's great for a hook.
[08:21] If you want Claude Code to
send you a Slack notification
[08:24] every time it's done working,
[08:25] this is actually the original inspiration
[08:27] for making hooks.
[08:29] And so these are all customizations
[08:31] that people are building today.
[08:32] - Tell me more about,
[08:34] what is the Claude Code SDK?
[08:35] - The Claude Code SDK is a great way
[08:37] to build general agents.
[08:38] The Claude Code SDK gives you access
[08:42] to all of the core building
blocks of an agent,
[08:44] including you can bring
your own system prompt,
[08:47] you can bring your own custom tools,
[08:49] and what you get from the
SDK is a core agentic loop
[08:54] where we handle the user turns
[08:57] and we handle executing
the tool calls for you.
[09:00] You get to use our
existing permission system
[09:02] so that you don't need to
build one from scratch.
[09:05] And we also handle interacting
with the underlying API.
[09:08] So we make sure that we have backoff
[09:11] if there's any API errors.
[09:13] We very aggressively prompt cache
[09:16] to make sure that your
requests are token-efficient.
[09:19] If you are prototyping
building an agent from scratch,
[09:22] if you use the Claude Code SDK,
[09:24] you can get up and running with something
[09:26] pretty powerful within
like 30 minutes or so.
[09:29] We've been seeing people build
really cool things with it.
[09:33] We open-sourced our Claude
Code on GitHub integration,
[09:36] which is completely built on the SDK,
[09:39] and we've seen people build
security agents on it,
[09:42] SRE agents, incident response agents.
[09:46] And these are just
within the coding domain.
[09:48] Outside of coding, we've seen people
[09:49] prototype legal agents, compliance agents.
[09:53] This is very much intended
to be a general SDK
[09:56] for all your agent needs.
[09:57] - The SDK is pretty amazing to me.
[09:59] I feel like we've lived in
the single request API world
[10:04] for so long.
[10:05] And now we're moving to like
a next level abstraction
[10:08] almost where we're gonna handle
[10:10] all the nitty-gritty of
the things you mentioned.
[10:13] Where is the SDK headed?
[10:15] What's next there?
[10:17] - We're really excited about the SDK
[10:19] as the next way to unlock
another generation of agents.
[10:24] We're investing very heavily
[10:26] in making sure the SDK is best-in-class
[10:28] for building agents.
[10:30] So all of the nice features
[10:32] that you have in Claude Code
[10:33] will be available out
of the box in the SDK,
[10:36] and you can pick and choose
which ones you wanna keep.
[10:39] So for example, if you want your agent
[10:41] to be able to have a to-do list, great.
[10:43] You have the to-do list
tool out of the box.
[10:46] If you don't want that,
[10:47] it's really easy to just delete that tool.
[10:50] If your agent needs to
edit files, for example,
[10:53] to update its memory, you
get that out of the box.
[10:55] And if you decide, okay,
mine won't edit files
[11:00] or it'll edit files in a different way,
[11:03] you can just bring your
own implementation.
[11:05] - Okay, so it's extremely customizable,
[11:08] basically general purpose in the sense
[11:09] that you could swap out the system prompt
[11:11] or the tools for your own implementations.
[11:13] And they just nicely slot in
[11:15] to whatever thing you're building for,
[11:16] whether it's in an entirely
different domain than code.
[11:19] Right?
- Yeah, totally.
[11:20] I'm really excited to see what
people hack on top of this.
[11:22] I think like especially for people
[11:25] who are just trying to prototype an agent,
[11:28] this is like, I think
by far the fastest way
[11:30] to get started.
[11:31] Like we really spent almost a year
[11:35] perfecting this harness,
[11:36] and this is the same harness
that Claude Code runs on.
[11:39] And so if you want to just jump
[11:41] right into the specific
integrations that your agent needs
[11:46] and you wanna jump right into like
[11:48] just working on the system prompt
[11:50] to share context about the
problems faced with the agent,
[11:54] and you don't wanna deal
with the agent loop,
[11:57] this is like the best way to circumvent
[12:00] all the general purpose harness
[12:02] and just add your like
special sauce to it.
[12:05] - Hmm, all right.
[12:07] Well, you heard it here.
[12:08] You gotta go build on the SDK.
[12:09] Before we wrap up here,
[12:10] I'm really curious to hear your own tips
[12:12] for how you use Claude Code,
[12:14] and what are some best practices
[12:16] we can share with developers?
[12:17] - When you work with Claude
Code or any agentic tool,
[12:22] I think the most important thing
[12:24] is to clearly communicate what
your goals are to the tool.
[12:28] I think a lot of people
think that prompting
[12:31] is this like magical
thing, but it really isn't.
[12:35] It's very much about, okay,
[12:37] did I clearly articulate
what my purpose is?
[12:41] Like what my purpose with this task is,
[12:44] how I'm evaluating the output of the task,
[12:47] any constraints in the design system.
[12:51] And I think usually
[12:53] when you can clearly
communicate these things,
[12:56] Claude Code will either be able to do them
[12:58] or just tell you that
like, "Okay, this thing,
[13:01] like I'm not able to do because A, B, C
[13:03] and do you wanna try
like D, E, F instead?"
[13:06] - So it's all about the communication
[13:07] just as if you're working
with another engineer.
[13:10] - Yeah, totally.
[13:11] And another thing is if you notice
[13:14] that Claude Code did something weird,
[13:16] you could actually just ask
it why it wanted to do that.
[13:20] And it might tell you something like,
[13:21] oh, okay, there was something
in CLAUDE.md that said this,
[13:24] or I read something in this file
[13:26] that like gave me this like impression.
[13:28] And then that way you can actually use
[13:30] like talking to Claude as a way to debug.
[13:33] It doesn't always work,
[13:35] but I think it's definitely worth trying.
[13:37] And it's like a common
technique that we use.
[13:39] - You use Claude Code
to debug Claude Code.
[13:42] I love it.
- Yeah, yeah.
[13:43] Like the same way that
when working with a human,
[13:45] if they say something
that you didn't expect,
[13:47] you might feel like, "Oh, interesting.
[13:48] Like, what gave you that impression?
[13:50] Or why did you think this?"
[13:52] And I think you can do
the same with agents too.
[13:54] - That's fascinating.
[13:55] Well, Cat, this has been great.
[13:56] Really, we appreciate the time.
[13:57] Thank you.
- Thanks for having me.