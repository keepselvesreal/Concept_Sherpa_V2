## Development Team Culture and Process

[00:00] These developers tend to run multiple Claude sessions at once, and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time.

[00:16] Hey, I'm Alex. I lead Claude Relations here at Anthropic. Today we're gonna be and I'm joined by my colleague Cat.

[00:22] Hey, I'm Cat. I'm the product manager for Claude Code.

[00:26] Cat, I wanna kick this the insane rate of It feels every time I open it up in my terminal, there's a new product or a new feature, something for me to use. Can you walk me through of the team going from an idea to actually shipping

[00:44] Yeah, so the Claude Code team is full of very product-minded engineers and a lot of these features It's you're a developer and you really wish you had this thing, and then you build it for yourself. And the way that our process works is instead of writing a doc, it's so fast to use Claude Code to prototype a feature that most of the time people and then they ship it And if the reception is really positive, then that's a very strong signal that the external world will it too. And that's actually our bar And then of course there's always features that aren't exactly right that need some tweaking. And if we feel okay, that much, then we just go and we say okay, what else could we change about this?

[01:31] And when we say "Ants," do

[01:33] Yes, yes. That's really fascinating. I've never seen a product have as strong of "dogfooding" Do you think that's or that just naturally arise from the product itself?

[01:48] It is quite intentional, and it's also a really important reason why Claude Code works so well. Because it's so easy to prototype we do push people to but it's hard to reason about exactly how a because developers are so heterogeneous in their workflows. So oftentimes, even if you wanna do something, even if you theoretically know that you wanna build an IDE integration, there's still a range you could go about it. And often prototyping is the only way that you can really feel how the product will actually be in your workflow. So yeah, it's through the that we decide what version of

## Product Architecture and Feature Development

[02:35] I see. And there's something about the, almost the flexibility but also the constraints that allows for easy addition which I've because we have the primitives built out of slash commands and things, it's easy to add another

[02:53] Yeah, it's totally And because so many developers are familiar with the terminal, it makes new feature because for example, for which lets you add a bit of determinism around Claude Code events, because every developer and really at the end of the day, all a hook is, is a script. And so you don't need to to customize Claude Code. You write this script that and then you add it to one and now you have some determinism.

[03:35] We're really trying to meet customers or developers where they are with this tool.

## User Growth and Adoption Patterns

[03:41] Switching gears slightly, so alongside this insane rate of shipping is also the insane growth with developers everywhere. Can you walk me through to be on this rocket ship and how are we seeing various developers, whether it's at startups or individuals or at even large enterprises, use Claude?

[04:01] So one of the magical is that the onboarding is so smooth. After you do the NPM install, Claude Code just without any configuration. And this is true whether through to if you're an I think this is the Because it has access to and files that you have, you have this very clear mental model for what Claude Code is capable of.

[04:33] We do see different use between smaller companies and larger ones. We find that engineers tend to run Claude more autonomously using things "auto-accept mode," which lets Claude make edits by itself without approval of each one. We also find that these developers tend to run multiple and they've started calling So you might see sessions where people have six Claudes open on their computer at the same time. Maybe each of them are in or in a different copy of the Git repo, and they're just Whenever anyone stops they'll jump in there and then send it off and let it continue running.

[05:20] And on the other end of the spectrum for larger companies, we find that engineers really So "plan mode" is a way for developers to tell Claude Code to take a second, explore the code base, understand the architecture, and create an engineering plan before actually jumping And so we find that this is really useful for harder tasks and more complex changes.

## Unexpected Usage Patterns and Customization

[05:47] So going back to multi-Clauding just 'cause I think that's I'm sure we imagined folks wanting to do things that, but it was somewhat surprising. Is there other things oh wow, this is a usage pattern that we really did not expect that have popped up organically and we've shifted our

[06:10] Yeah, I think multi-Clauding because this is something that we thought was just a power user feature that a few people would wanna do. But in fact this is in which people use Claude. And so for example, they might have one Claude instance where they only ask questions and this one doesn't edit code. That way they can have in the same repo that does edit code and these two don't Other things that we've seen are people really to handle specialized tasks.

[06:44] So we've seen people build security agents, incident response agents. And what that made us realize is that integrations are so important for making sure Claude Code works well. And so we've been encouraging people to spend more time to hey, these are the CLI or to set up remote MCP servers to get access to logs and

[07:12] When these engineers are does that mean they're creating sub-agents or are they creating markdown files CLAUDE.md files? How exactly are they creating these different types of agents?

[07:25] Yeah, I think the most common ways that we've seen people customize is by investing a lot So the CLAUDE.md file is And so it's the best place for you to tell Claude Code about how the code is architected, any gotchas in the code base, any best practices. And investing in CLAUDE.md we've heard dramatically improves the quality of the output.

[07:55] The other way that people is by adding custom slash commands. So if there's a prompt you can add that into and you could also check these in so that you share them And then you can also add custom hooks. So if for example, you want Claude Code to run lints before it makes a commit, this is something that's great for a hook. If you want Claude Code to every time it's done working, this is actually the original inspiration for making hooks. And so these are all customizations that people are building today.

## Claude Code SDK and Agent Development

[08:32] Tell me more about, what is the Claude Code SDK?

[08:35] The Claude Code SDK is a great way to build general agents. The Claude Code SDK gives you access to all of the core building including you can bring you can bring your own custom tools, and what you get from the where we handle the user turns and we handle executing You get to use our so that you don't need to And we also handle interacting So we make sure that we have backoff if there's any API errors. We very aggressively prompt cache to make sure that your If you are prototyping if you use the Claude Code SDK, you can get up and running with something pretty powerful within

[09:29] We've been seeing people build We open-sourced our Claude which is completely built on the SDK, and we've seen people build SRE agents, incident response agents. And these are just Outside of coding, we've seen people prototype legal agents, compliance agents. This is very much intended for all your agent needs.

[09:57] The SDK is pretty amazing to me. I feel we've lived in for so long. And now we're moving to almost where we're gonna handle all the nitty-gritty of Where is the SDK headed? What's next there?

[10:17] We're really excited about the SDK as the next way to unlock We're investing very heavily in making sure the SDK is best-in-class for building agents. So all of the nice features that you have in Claude Code will be available out and you can pick and choose So for example, if you want your agent to be able to have a to-do list, great. You have the to-do list If you don't want that, it's really easy to just delete that tool. If your agent needs to to update its memory, you And if you decide, okay, or it'll edit files in a different way, you can just bring your

[11:05] Okay, so it's extremely customizable, basically general purpose in the sense that you could swap out the system prompt or the tools for your own implementations. And they just nicely slot in to whatever thing you're building for, whether it's in an entirely Right?

[11:20] I'm really excited to see what I think especially for people who are just trying to prototype an agent, this is I think to get started. We really spent almost a year perfecting this harness, and this is the same harness And so if you want to just jump right into the specific and you wanna jump right into just working on the system prompt to share context about the and you don't wanna deal this is the best way to circumvent all the general purpose harness and just add your

## Best Practices and Communication Tips

[12:05] Hmm, all right. Well, you heard it here. You gotta go build on the SDK. Before we wrap up here, I'm really curious to hear your own tips for how you use Claude Code, and what are some best practices we can share with developers?

[12:17] When you work with Claude I think the most important thing is to clearly communicate what I think a lot of people is this magical It's very much about, okay, did I clearly articulate what my purpose with this task is, how I'm evaluating the output of the task, any constraints in the design system. And I think usually when you can clearly Claude Code will either be able to do them or just tell you that I'm not able to do because A, B, C and do you wanna try

[13:06] So it's all about the communication just as if you're working

[13:10] Yeah, totally. And another thing is if you notice that Claude Code did something weird, you could actually just ask And it might tell you something oh, okay, there was something or I read something in this file that gave me this impression. And then that way you can actually use talking to Claude as a way to debug. It doesn't always work, but I think it's definitely worth trying. And it's a common

[13:39] You use Claude Code I love it. The same way that if they say something you might feel, "Oh, interesting. what gave you that impression? Or why did you think this?" And I think you can do

[13:54] That's fascinating. Well, Cat, this has been great. Really, we appreciate the time. Thank you.