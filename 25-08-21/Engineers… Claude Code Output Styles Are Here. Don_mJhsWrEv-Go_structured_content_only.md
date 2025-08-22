## Cloud Code Output Styles and Agents

Line 13: [00:00] Engineers. Here we have six cloud code instances. In each instance we have six unique output styles. Default table format, YAML format, ultra concise format, text to speech summary, and most importantly, HTML format. For every agent with every style, we have one prompt.

Line 15: [00:25] Honestly, when I first saw the output styles feature drop, my first thought was, "This is useless." But I never let my initial reaction prevent me from doing the real work and understanding the feature. After a quick dev session, I learned just how useful these output styles are. Never bet on your first initial reaction without doing the work. Dan, I've explained how to add new hooks to your cloud code setup with examples and configuration steps.

Line 17: [00:57] So, you can hear our text to speech format summarize the exact work that was completed. We can see our results starting to flow in here. We're going to break down every one of these output formats. Believe it or not, this feature release marks the beginning of viable generative UI. The Claude code team is on a generational hot streak, shipping valuable features back to back to back.

Line 19: [01:23] But there are two features I'm not a fan of because they could take the tool in the complete wrong direction. We'll talk about that in this video. Right next to the output styles drop, we also have the status line feature that lets you customize your cloud code interface. And I can guarantee you, you're not using this feature to its full potential yet.

## Exploring Output Format Types

Line 23: [01:57] Default table YAML ultra concise text to speech HTML. New features are only valuable in relation to existing features. In our first cloud code instance, you can see the default response for the following prompt. We asked /quest, how can I add a new hook? If we look at this response format, you can see it's the default cloud code response format, but now we have full control over the output style of cloud code.

Line 25: [02:24] If we switch to our table output format, you can see something very different. We have clean formatted tables helping us speed up the flow of information between us and our agents. You can see this is a valuable format for organizing information. Now we get to my second favorite output format, YAML. At first, this format might seem kind of weird and kind of out of place, but the YAML output format actually has a really interesting way of organizing information in a highly structured way.

Line 27: [02:58] I found that this specific cloud code instance typically outperforms the rest. Why might that be? If I just copy all this out here, clean up the output format a little bit here. So, you can see the task here, analyze the hook system, provide guidance on adding new hooks, status complete. There's some details. The YAML format provides a highly structured informational way to get responses out of your cloud code instances.

Line 29: [03:24] So, next up, we have the ultra concise format. This format is the most similar to the default cloud code response, but it's going to be concise and just give you enough information. I've also found that the ultra concise response format reduces the number of input and output tokens that cloud code consumes. Next, the text to speech format. In the beginning, you heard after our agent completed its work, it communicated exactly what it's done.

Line 31: [03:50] I'll just run this again. Say again. Okay, so we can just hear that again. I've explained how to add new hooks to your cloud code setup with examples and configuration steps. Audio summary again for Dan about claude code hooks setup and configuration.

Line 33: [04:03] Okay, so in the system prompt it has the instructions. Whatever command you just ran, summarize it. So I asked it to run that audio summary again. It ran it and then it ran an audio summary on the audio summary. Okay, so that's fantastic.

## The HTML Format - Generative UI Revolution

Line 37: [04:18] But there is one output format that is more important than all of them. We have the HTML format. This is the most important output format of them all. Let me explain why.

Line 39: [04:35] This is the one output format to rule them all. At first, you might be thinking, Dan, this is stupid. This is super hard to read. There's no way I'm going to actually get information by reading HTML. We're talking 10 to hundreds of responses per day as we're doing real engineering work with cloud code with agent coding tools.

Line 41: [04:55] Let's slow down and really think about what's happening here. We have dynamic accurate HTML generation our agent is generating on the fly. What you're looking at here is the first useful application of generative UI. With a few tweaks to this prompt, we can create a new output style that enhances the information rate between us and our agent. Let me show you exactly what I mean.

Line 43: [05:22] Let's fire up a brand new cloud code instance /output style to update the style. And then we're going to hit genui. What you just saw was format 8. This our HTML structure. This prompt builds on top of the HTML layer. Let's fire this off and let's run that exact same prompt that we ran before. Okay. slash quest, how can I add a new hook?

Line 45: [05:45] And what you're going to see here is nothing short of extraordinary. With output styles, with cloud code, our agent can build UI on the fly. Now, I'll create a comprehensive HTML guide explaining how to add a new hook to cloud code. On every response, our agent is going to generate UI and respond to us in this rich way. Okay, check this out.

Line 47: [06:12] How to add a new cloud code hook. Okay, let's see exactly what happened there. It wrote to a temporary file. It opened it at the end of the response and it generated an HTML guide for us. This is generative UI. This is not a gimmick.

Line 49: [06:30] This is yet another powerful agent decoding tool, a powerful agent decoding pattern you now have in your toolbox. Okay. With every request, we can now have our agent generate UI for us. This is generative UI. And you can see here we got a great breakdown on exactly how to add this. It's got consistent simple themes and styles. This is insane, right?

Line 51: [06:54] And then we have project structure, right? It's really breaking down how we can add a cloud code hook. We even have some next steps. We have files referenced. Here we have UI that was generated on the fly for us. This is HTML. It's the language of UI and of course sonnet opus they can generate this for us with no problem.

Line 53: [07:15] Okay, it does take a little more time to generate the response but you can see how powerful this can be. Okay, this is not a gimmick, right? Let's run some more of these. Output style genui output style genui. Here we're going to generate a typescript interface. Here we're going to do some research with firecrawl. We want to see the top five hacker news posts. break down the sentiment.

Line 55: [07:36] I'm going to update the model here. Switch to opus and this is going to be in that YAML format. Create a pyantic class for cloud code hook output structure blah blah blah. All right, so we're going to run that. Now we have multiple agents running on our behalf getting work done for us.

Line 57: [07:52] All right, so check this out. Here's our hacker news sentiment analysis. We can quickly validate this. The future of large files in git is git. If we just search this, you can see there's that 453 points. That looks right. This is quite fascinating. Okay, there's a new paradigm to operate in. You can see the points on the side there. We are getting the top five posts on hacker news right now of this date. We have a temp file getting generated for us on the fly.

Line 59: [08:16] Here's another one. We have that typescript interface get generated. Here's a summary of the work done. Task completed. It created this new types file for us based on the JSON structure in this file. Clean simple write up, right? Detailing exactly what was done. Preconfigured variables. You can see here's the interface hierarchy just giving us a breakdown of what this looks like.

Line 61: [08:36] We can of course open up this codebase. Just search for types, there it is. If we look MCP JSON sample, this exact type right here. And it looks like it's typed it out nicely for us here based on the other MCP servers it has in its system prompt.

Line 63: [08:53] And here's our last request here wrapping up CC generate cloud code hook models. So based on all the output types from our hooks, look at this incredible UI, right? Every time it runs, it's generating UI for us. You can imagine pushing this further, adding a layer on top of this where we can interact back and forth. You can imagine a layer where cloud code itself, the terminal interface, is actually presenting us with generated terminal user interfaces and letting us interact with that.

Line 65: [09:26] Right? There are really no limits to this capability, right? We have truly the first useful application of generative UI, right? Us interacting with our agents, our agents giving us specific responses. You can see here it's breaking down all the hooks. This is all based on our output style system prompt. Okay, this feature is ultra ultra powerful.

Line 67: [09:47] I'm almost like embarrassed to say that I thought this was not useful, right? that this is ultra powerful and I think that probably even the cloud code engineers haven't really realized this capability right or where this could go they have now because they're watching this video what's up anthropic engineers cloud code engineers thank you you guys are doing incredible work here but this is really extraordinary right this is the power of the primitive that is cloud code this is the power of stacking up the right feature set putting together the right tools and most importantly understanding the fundamentals of AI coding and what's actually happening under the hood of the agent, right?

Line 69: [10:27] All this does is it updates the prompt, right? The output style, they say it here, right? I'm really happy that they're being really clear about the fundamental unit that this is updating. The output styles update the system prompt. Okay, as viewers of the channel know, there are only three key elements of every agentic system. Context, model, prompt. If you master these, if you understand these, you can move from tool to tool to tool to idea to idea to idea at light speed because everything is built on this. This is a principle of AI coding. Okay? Principle of the generative AI age.

## Status Lines and Multi-Agent Management

Line 73: [14:19] As you can see here, I have a pretty bare minimum status line. A lot of the status lines you've probably seen so far are like vibe coding. It's the lowest hanging fruit. When you combine hooks and a simple state management system, your status lines can become tremendously more valuable. Let me show you exactly what I mean.

Line 75: [14:36] So I'm going to get rid of some instances here. Let's clear out and just focus on a single instance. Here we have a simple minimal status line. Model current working directory get branch plus the changes on committed or cloud code version. This is simple mostly static information. Let's update our status line to use a new format. I'll open up cursor go to my settings here. We'll search for status line.

Line 77: [15:01] If we open up our folder structure here, I have a dedicated status lines directory with four versions giving us different status line outputs. Let's update to v2 and let's see exactly what this looks like. I'll close claude reopen and check this out. Now we have model and no recent prompt. So you can see exactly where this is going, right? I'll say hi. We now have our most recent prompt in the status line.

Line 79: [15:25] So who cares what why is this important? Right? Isn't this kind of stupid? If you follow this channel, you probably are running more than one cloud code instance at any time, right? Just like AI coding is not enough. One agent is not enough. As soon as you start using powerful agent coding tools like cloud code, especially cloud code, there are only two directions to go. Better agents or more agents.

Line 81: [15:50] All right, output formats helps us with better agents. Status lines helps us with more agents. Okay, this is really really simple to portray here, right? Open up a new terminal window. Fire up cloud code. Let's go YOLO mode in Opus. Let's update our output style just for fun. We'll use text to speech summary.

Line 83: [16:12] This is a great format when you have multiple agents and you're working in parallel doing a lot of work, long running tasks. You can put on text to speech and when your agent finishes, it'll respond back to you. So, this is great for more and better agents. Here's the kicker. This says hi. I can say who's investing the most in AI data centers between and Google, right? Just any prompt, right? I'm just firing off whatever.

Line 85: [16:36] And you can see here we have a brand new last executed prompt. Now, on its own, not very useful, right? But when you're switching instances all the time, tell me about this codebase, this becomes very useful. Okay, so we have one instance here, we have another instance here. Right? If you're really pushing this tool, you've likely opened up multiple and I'm talking three, five, ten instances of this tool and you're prompting all the time.

Line 87: [17:05] Here's another prompt. Okay? And so it becomes very very helpful to have this last prompt status line to remind you what is going on. Right? So now I can just quickly look at this cloud code instance. I can read the status line and I can know okay yes that's what I was prompting. That's what I was working on in this specific instance.

Line 89: [17:23] Okay. And so when you combine just a little bit of state with cloud code hooks with the status line you get a really really powerful capability here that builds on your agent coding tool. So you can see here our web starts firing off and when I look at this I can just immediately look at the status line right we have emojis based on if we're asking a question if we're creating new code right let's go ahead and do that here in a new instance right so claude create a compressed read me based on read me like this right we have the create keyword here right an information dense keyword and now our recent prompt there we go we have that light bulb right because it's creating or updating something new.

Line 91: [18:10] Okay. And so, we're using the tools. I've analyzed your Claude code hooks mastery codebase. It's an advanced toolkit for extending Claude code with hooks, sub agents, and custom behaviors. Wonderful. So, we got that text to speech response. Again, this is useful for interacting with multiple agents. This kind of replaces our stop hook text to speech response that we had that we've been using in previous videos.

Line 93: [18:34] Now with the output styles, we can have our agent run a tool every time it finishes. In this case, the tool happens to be 11 Labs text to speech. I hope you're really paying attention to what you can do with this tool, right? Output styles in combination with the status lines. What does this do? What's the fundamental change that's happening here? We are increasing the information rate between ourselves and our agents, right?

Line 95: [19:00] And when you push this further with something like created a compressed readme that cuts 650 lines down to 150 while keeping all essential information. Wonderful. And so when you push this even further, what do we get? Right. We get generative UI. Okay. Right. This is where this is all going. I hope you guys can kind of see a larger picture here of how far you can push this tool.

## Advanced Status Line Features

Line 99: [20:24] Now, I have these four windows open, right? I'm doing a lot of work in parallel. I can cycle through these and know exactly what was going on, right? So, literally nothing was happening here. Just demoed prompt. But here, who's investing the most? Okay, now we can follow up on that. What else we have? Right. Create a compressed readme. Okay, fantastic. We also got that text to speech summary 650 down to this. Open that file. Of course, we're going to get that I've opened the compressed readme file for you to review text to speech response. Fantastic stuff.

Line 101: [20:53] Let's go ahead and close out our instances here. Let's focus. That was just two status lines, right? Let's go to status line V3 and then I'll leave V4 for you to experiment with. Here, let's fire up Claude once again. We'll run an opus with permissions. You can see here a very similar format until we start prompting. So, the new flow here for me is set my output format. Let's go ahead and set a YAML structured format here.

Line 103: [21:17] And I'll say at we'll search for that new compress readme. What does this codebase do? Read only this file. So, we're just going to get a quick understanding and you're going to see something really incredible here. Our status line updated here. We have a name for our agent. Kind of a similar format, right? Opus is a little bit better at formatting YAML. We have a great YAML based response format. Again, there's something about this response format that improves this agent's performance. Definitely play around with this.

Line 105: [21:47] Right? We said, what does this do? Read only this file. Task completed. Overview. Core functionality. Right. Eight life cycles for controlling cloud code. Yep. Sub agents. Okay. Meta agent. Very good. We covered that in the previous video. Custom features. Status line. Output formats. Very good. Technical stack. Love that. Astral UV. That's right. Shout out Astral. Use cases. Key innovations. Great stuff. Right.

Line 107: [22:12] And our status line has the last prompt and an agent name. Another tool to scale your agents. And another example to showcase how you can use state that's getting updated throughout your session to guide your agent and to help you interact with your agents faster and better. Right? More agents, better agents. First you make your agents better, then you add more agents. Okay?

Line 109: [22:35] Now read read me update your understanding. Okay? Something like that. And in this status line V3, we now have trailing prompts, right? So, historic trailing prompts. Here's the most up-to-date. And here's the second to last prompt that we ran. Okay. So, really powerful stuff here. I think you get the idea. As we're interacting with agents more and more as engineers, the key idea, the key value proposition is in increasing the information rate between you and your agent, right? Between you and the work that you're trying to do.

## Concerns About Plan Mode and Background Commands

Line 113: [23:25] There are a couple features I want to talk about that I think might be pushing cloud code in the wrong direction my opinions but I want to share this with you. I want to get your thoughts on these as well. slash model opus plan mode. When you submit a prompt, Cloud Code is going to plan with Opus and then build with Sonnet.

Line 115: [23:44] If you've been with the channel for a while, this feature might make you think of ADER, the original AI coding tool. ADER was one of the first AI coding tools to really leverage language models. This is traditional AI coding. It's not agent coding. There are no tool calls happening in ADR. That PR, that patch just hasn't gotten out. Ader was one of the first tools to build out a architect mode. We can see this great blog put back out in 2024.

Line 117: [24:12] This was innovative because they used a prompt chain, right? Two prompts with two models. Ader separated thinking and building. Okay, this was really big. We had already talked about prompt chaining on the channel around this time. Why do I have an issue with this? Right? Why is plan, build, architect, builder something that I have beef with? The power of cloud code lies in its flexibility, control, and simplicity.

Line 119: [24:36] As the creator Boris said, cloud code is a primitive. It's an engineering primitive. This feature feels like a slight overreach to me along with the bash background commands. To me, it feels like the beginning of loss of directional focus. They should let the engineer decide on the models, how they're used, the planning, the building, and things like background task management, right? Bash controls.

Line 121: [25:03] I can simplify everything I'm trying to say here a little further and just say, don't tell me how to use the models. Don't tell me how to manage my bash commands in my background processes. Okay, this is something I always watch out for with every tool, right? Especially the leading tool. I have a guiding question that kind of helps me determine if a new feature is valuable or if it should even exist.

Line 123: [25:26] Right? In the generative AI age, we always have to keep track of the context model and prompt every step of the way. The leading question here is, do I know exactly what the context, model, and prompt are at every step of the process in whatever tool I'm using? Okay. Any feature that obscures this or inserts an opinion about how you or I should manage the big three, it throws up a huge yellow, orange, red flag to me.

Line 125: [25:52] Now, to be clear, both of these features are useful, right? Opus plan mode where you have opus plan and sonnet build quite useful feature I'm not saying it's not a valuable feature you can build a great feature that is directionally incorrect for your product for your mission for your stated engineering philosophy okay so maybe this is just me let me know what you think about this do you think that opus plan mode and background commands are a slight overreach from cloud code right from the team in cloud code is this the right set of features that they should be building out I think this is the first sign of things going a little bit off course, but maybe I'm overanalyzing, being too detailed oriented.

Line 127: [26:34] Let me know in the comments if you like this direction from cloud code separate from the individual features themselves. Again, I'm not saying background bash commands and opus plan aren't valuable features.

## How Output Styles Work and Final Thoughts

Line 131: [26:52] So with that aside, you can see here that output styles and the status line increase the information rate between you and your agent. So let's quickly understand how this works. These are very simple features which I absolutely love. The cloud code team is keeping it simple. If we open up claude, open up output styles, you can see we have all of these output styles detailed here. We have a bullet points format that I just completely glossed over, right? We have our HTML structure. We have our markdown. And of course, we have the gen UI.

Line 133: [27:24] This codebase is going to be available to you. Link in the description. By the way, if you made it to this point in the video and you tune in every single week and you're still not subscribed for some reason, what are you doing? Right? All of this work, all the ideas we talk about every single week and you can't press one button to show your appreciation, come on. Subscribe. Join the journey. Don't be weird about it. Okay?

Line 135: [27:45] You're in good company. I'm here delivering value for free for you every single week. So, hop on the train. Things are only going to continue to accelerate. So, that's GUI. Check this out. Again, link in the description. You can see how this works and you can tweak it to make it your own. You can see we have that key workflow step for these agentic workflows where we want our agent to take actions back to back to back.

Line 137: [28:06] This is a great place to get a high level breakdown of what the prompt does exactly. So, that's that HTML structure TTS. It's all there. If we close that, we can focus on our status lines. And I've created a dedicated folder for this. Output styles is a anthropic specific directory. Status lines is something that I created just for organizational purposes.

Line 139: [28:21] Just like the data directory here, we'll talk about in a second. You can see in the status line directory, the only thing you need to focus on is main, right? We read in the line. We generate whatever status line you want using whatever data you want, but most importantly, we're just printing it. That's it. That's how status lines work.

Line 141: [28:39] And to run this specific status line, as you saw, all you need to do is add this to your do.cloud settings file. You can see here we have that status line V3. And if we open up V3, you can see something really cool in combination with our cloud code hook. If we look for user prompt, right, and we open up these files side by side, we are managing session data.

Line 143: [29:05] So every cloud code prompt makes a contribution to our agent specific data. Right? So we have this new.cloud. If we open up data, you can see here I have a bunch of sessions. And if we open up one of the sessions, you can see here we have information about that particular session that we can update, write to and read from. Okay.

Line 145: [29:24] So as you would expect, session ID, agent name, prompts. This is how we're populating our agent name and our prompt history, right? And we can keep prompting. Fantastic. Looks great. Just a random prompt just to showcase that, we're tracking the three most recent prompts with this status line, right? And this is all because we have a simple state management system. Again, just JSON objects, super readable, very understandable.

Line 147: [29:49] And that's that, right? In the user prompt submit hook. Right here we have that cloud code hook. We are combining these two features to get more value out of them. Prompts append. If we don't have an agent name, we're doing something really awesome. If you remember from our GPT5 nano agents video, we were running GPT 4-o-mini 20 billion. Here we're doing that exact same thing. If we open up ollama py, we're having a powerful on-device model right on my MacBook. Generate unique names for our agent.

Line 149: [30:17] This is a super simple, great use case for these agents. You can see here, generate agent name. This file is going to be here for you to check out. It's super simple. We're generating a one-word name, right? This is prompt engineering 101. That's it. The agent has 5 seconds to generate this or it falls back. And this is how we update state for our status lines.

Line 151: [30:42] What you're seeing here, right, all these features that you've seen here in this video, these are essential ideas of what you can do with output styles. You can take this further and combine, merge, and add conditional branches directly in your output style system prompt to direct which output type your agent uses based on the prompt at hand. Okay, so if you want to take this even further, that's a great direction.

Line 153: [31:05] And this is what makes Cloud Code so great. It's a new primitive of engineering. It's the engineers agent that's increasingly customizable and so far so good, very unopinionated. This is key. It's not a dedicated solution. This is what we as engineers need to solve any problem we face. And this is why again I feel like the plan mode and the bash command is starting to look like a slight overreach of this principle of being an unopinionated simple engineering primitive.

Line 155: [31:37] Tell me what you think about that. Drop a comment down below. This codebase is available to you. Link in the description. No matter what, stay focused and keep building.