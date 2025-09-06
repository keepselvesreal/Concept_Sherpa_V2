# 1. Vibe Coding in Production

## 1.0 Introduction

Hey everyone, welcome. I'm here to talk about everyone's favorite subject, vibe coding. And somewhat controversially, how to vibe code in production responsibly. So let's talk about vibe coding and what this even is.

First of all, I'm Eric. I'm a researcher at Anthropic focused on coding agents. I was the author along with Barry Zhang of building effective agents where we outlined our best science and best practices for creating agents no matter what the application is. This is a subject that's near and dear to my heart. Last year I actually broke my hand while biking to work and was in a cast for two months and Claude wrote all of my code for those two months. And so figuring out how to make this happen effectively was really important to me and I was luckily able to figure that out well and sort of help bring that into a lot of Anthropic's other products and in our models through my research.

## 1.1 Defining Vibe Coding

### 1.1.1 Common Misconceptions

So let's first start talking about what is vibe coding. A lot of people really conflate vibe coding with just extensive use of AI to generate your code. But I think this isn't quite true. A lot of people, you know, they're using Cursor, they're using Copilot. It's a lot of AI and a lot of the code is coming from the AI rather than them writing itself. But I think when you are still in a tight feedback loop with the model like that, that isn't truly vibe coding.

### 1.1.2 Karpathy's Definition

When I say vibe coding, I think we need to go to Andre Karpathy's definition where vibe coding is where you fully give into the vibes, embrace exponentials, and forget that the code even exists. I think the key part here is forget the code even exists. And now the reason this is important is that vibe coding was when people outside of the engineering industry really started getting excited about code generation.

### 1.1.3 Impact on Non-Engineers

Copilot and Cursor were great but only for engineers but someone that didn't know how to code suddenly with vibe coding they could find themselves coding an entire app by themselves. And this was a really exciting thing and a big unlock to a lot of people.

## 1.2 Current Challenges and Limitations

### 1.2.1 Negative Consequences

Now, of course, there were a lot of downsides of this and you had people coding for the first time and really without knowing what they were doing at all. And you said, "Hey, you know, random things are happening, max out usage on my API keys, people are bypassing the subscription, creating random stuff on the DB." And so, you know, this is kind of the downside of vibe coding of what started happening.

### 1.2.2 Low-Stakes Success Stories

And the positive sides of vibe coding that you'd see were all things that were really kind of low stakes. It was people building video games, building fun side projects, things where it's okay if there was a bug. So, you know, why do we even care about vibe coding if it seems like something where the stakes are really high if you do it for a real product? And the most successful cases of it are kind of these toy examples or fun things where the stakes are very low.

## 1.3 The Exponential Growth Argument

### 1.3.1 Current Capabilities and Growth Rate

And my answer for why we should care about vibe coding is because of the exponential. The length of tasks that AI can do is doubling every seven months. Right now we're at about an hour. And that's fine. You don't need to vibe code. You can have Cursor work for you. You can have Claude Code write a feature that would take an hour. And you can review all that code and you can still be intimately involved as the AI is writing a lot of your code.

### 1.3.2 Future Scaling Challenges

But what happens next year? What happens the year after that? When the AI is powerful enough that it can be generating an entire day's worth of work for you at a time or an entire week's worth of work, there is no way that we're going to be able to keep up with that if we still need to move in lockstep. And that means that if we want to take advantage of this exponential, we are going to have to find a way to responsibly give into this and find some way to leverage this task.

### 1.3.3 The Compiler Analogy

I think my favorite analogy here is like compilers. I'm sure in the early day of compilers, a lot of developers really didn't trust them. They might use a compiler, but they'd still read the assembly that it would output to make sure it looks, you know, how they would write the assembly. But that just doesn't scale. You know, at a certain point, you start needing to work on systems that are big enough that you just have to trust the system.

## 1.4 Responsible Implementation Framework

### 1.4.1 Core Philosophy

The question though is how do you do that responsibly? And I think my challenge to the whole software industry over the next few years is how will we vibe code in production and do it safely? And my answer to that is that we will forget that the code exists but not that the product exists.

Thinking again to that compiler analogy, you know, we all still know that there's assembly under the hood, but hopefully most of us don't need to really think about what the assembly actually is. But we still are able to build good software without understanding that assembly under the hood. And I think that we will get to that same level with software.

### 1.4.2 Historical Management Precedents

And one thing I really want to emphasize is that this is not a new problem. How does a CTO manage an expert in a domain where the CTO is not themselves an expert? How does a PM review an engineering feature when they themselves can't read all the code that went into it? Or how does a CEO check the accountant's work when they themselves are not an expert in financial accounting?

And these are all problems that have existed for hundreds or thousands of years and we have solutions to them. A CTO can still write acceptance tests for an expert that works for them even if they don't understand the implementation under the hood. They can see that these acceptance tests pass and that the work is high quality. A product manager can use the product that their engineering team built and make sure that it works the way they expected even if they're not writing the code. And a CEO can spot check key facts that they do understand and slices of the data so that they can build confidence in the overall financial model even though they themselves might not be an expert in how the entire thing flows.

### 1.4.3 Adapting to New Management Paradigms

And so thinking about these examples, managing implementations that you yourself don't understand is actually a problem as old as civilization. And every manager in the world is actually already dealing with this. Just we as software engineers are not used to this. We are used to being purely individual contributors where we understand the full depth down to the stack. But that's something that in order to become most productive, we are going to need to let go of in the way that every manager in order to be most productive is going to need to let go of some details.

### 1.4.4 Abstraction Layers and Verification

And just like us as software engineers, you know, we let go of some of the details of like understanding the assembly itself that's happening under the hood. And the way that you do this while still being safe and being responsible is to find an abstraction layer that you can verify even without knowing the implementation underneath it.

## 1.5 Technical Debt Considerations

### 1.5.1 The Technical Debt Problem

Now I have one caveat to that today which is tech debt. So right now there is not a good way to measure or validate tech debt without reading the code yourself. Most other systems in life you know like the accountant example, the PM, you know, you have ways to verify the things you care about without knowing the implementation. Tech debt I think is one of those rare things where there really isn't a good way to validate it other than being an expert in the implementation itself.

### 1.5.2 Leaf Node Strategy

So that is the one thing that right now we do not have a good way to validate. However, that doesn't mean that we can't do this at all. It just means we need to be very smart and targeted where we can take advantage of coding. My answer to this is to focus on leaf nodes in our codebase. And what I mean by that is parts of the code and parts of our system that nothing depends on them. They are kind of the end feature. They're the end bells and whistles rather than things that are the branch or trunks beneath them like here in white.

Here the orange dots are all these leaf nodes where honestly if you have a system like this it's kind of okay if there is tech debt in these leaf nodes because nothing else depends on them. They're unlikely to change. They're unlikely to have further things built on them versus the things that are in white here, the trunks and the underlying branches of your system. That is the core architecture that we as engineers still need to deeply understand because that's what's going to change. That's what other things are going to be built on and it's very important that we protect those and make sure that they stay extensible and understandable and flexible.

### 1.5.3 Future Model Improvements

Now the one thing I will say here is that the models are getting better all the time and so we might get to a world where this gets further and further down where we trust the models more and more to write code that is extensible and doesn't have tech debt. Using the Claude 4 models over the last week or two within Anthropic has been a really exciting thing and I've given them much more trust than I did with 3.7. So I think that this is going to change and more and more of the stack we will be able to work with in this way.

## 1.6 Success Strategies for Vibe Coding

### 1.6.1 Acting as Claude's Product Manager

So let's talk about how to succeed at vibe coding. And my main advice here is ask not what Claude can do for you but what you can do for Claude. I think when you're vibe coding you are basically acting as a product manager for Claude. So you need to think like a product manager. What guidance or context would a new employee on your team need to succeed at this task?

I think a lot of times we're too used to doing a very quick back and forth chat with AI of make this feature, fix this bug, but a human if it was their first day on the job and you just said, "Hey, implement this feature," there's no way you'd expect them to actually succeed at that. You need to give them a tour of the codebase. You need to tell them what are the actual requirements and specifications and constraints that they need to understand.

### 1.6.2 Preparation and Context Building

And I think that as we vibe code, that becomes our responsibility to feed that information into Claude to make sure that it has all of that same context and is set up to succeed. When I'm working on features with Claude, I often spend 15 or 20 minutes collecting guidance into a single prompt and then let Claude cook after that.

And that 15 or 20 minutes isn't just me writing the prompt by hand. This is often a separate conversation where I'm talking back and forth with Claude. It's exploring the codebase. It's looking for files. We're building a plan together that captures the essence of what I want, what files are going to need to be changed, what patterns in the codebase should it follow.

And once I have that artifact, that all of that information, then I give it to Claude, either in a new context or say, "Hey, let's go execute this plan." And I've typically seen once I put that effort into collecting all that information, Claude has a very, very high success rate of being able to complete something in a very good way.

### 1.6.3 Limitations and Prerequisites

And the other thing I'll say here is that you need to be able to ask the right questions. And despite the title of my talk, I don't think that vibe coding in production is for everybody. I don't think that people that are fully non-technical should go and try to build a business fully from scratch. I think that is dangerous because they're not able to ask the right questions. They're not able to be an effective product manager for Claude when they do that and so they're not going to succeed.

## 1.7 Case Study: 22,000-Line Production Change

### 1.7.1 Project Overview

We recently merged a 22,000-line change to our production reinforcement learning codebase that was written heavily by Claude. So how on earth did we do this responsibly? And yes, this is the actual screenshot of the diff from GitHub for the PR.

### 1.7.2 Human Work and Planning

The first thing is we asked what we could do for Claude. This wasn't just a single prompt that we then merged. There was still days of human work that went into this of coming up with the requirements, guiding Claude and figuring out what the system should be. And we really embraced our roles as the product manager for Claude in this feature.

### 1.7.3 Strategic Code Placement

The change was largely concentrated in leaf nodes in our codebase where we knew it was okay for there to be some tech debt because we didn't expect these parts of the codebase to need to change in the near future. And the parts of it that we did think were important that would need to be extensible, we did heavy human review of those parts.

### 1.7.4 Verification Strategy

And lastly, we carefully designed stress tests for stability. And we designed the whole system so that it would have very easily human verifiable inputs and outputs. And what that let us do these last two pieces is it let us create these sort of verifiable checkpoints so that we could make sure that this was correct even without understanding or reading the full underlying implementation.

Our biggest concern was stability and we were able to measure that even without reading the code by creating these stress tests and running them for long durations. And we were able to verify correctness based on the input and outputs of the system that we designed it to have.

### 1.7.5 Results and Impact

So basically we designed this system to be understandable and verifiable even without us reading all the code. And so ultimately by combining those things we were able to become just as confident in this change as any other change that we made to our codebase but deliver it in a tiny fraction of the time and effort that it would have taken to write this entire thing by hand and review every line of it.

And I think one of the really exciting things about this is not just that this saved us a week's worth of human time, but knowing that we could do this, it made us think differently about our engineering, about what we could do. And now suddenly when something costs one day of time instead of two weeks, you realize that you can go and make much bigger features and much bigger changes. The marginal cost of software is lower and it lets you consume and build more software.

So I think that was the really exciting thing about this is not just saving the time but now kind of feeling like oh things that are going to take two weeks let's just do them. It's only going to take a day. And that's kind of the exciting thing here.

## 1.8 Conclusion and Key Principles

### 1.8.1 Core Guidelines

So to leave you with the closing thoughts about how to vibe code in production responsibly. Be Claude's PM. Ask not what Claude can do for you, but what you can do for Claude. Focus your vibe coding on the leaf nodes, not the core architecture and underlying systems so that if there is tech debt, it's contained and it's not in important areas. Think about verifiability and how you can know whether this change is correct without needing to go read the code yourself. And finally, remember the exponential. It's okay today if you don't vibe code, but in a year or two, it's going to be a huge disadvantage if you yourself are demanding that you read every single line of code or write every single line of code. You're going to not be able to take advantage of the newest wave of models that are able to produce very large chunks of work for you. And you are going to become the bottleneck if we don't get good at this.

### 1.8.2 Industry Challenge

So overall that is vibe coding in production responsibly. And I think this is going to become one of the biggest challenges for the software engineering industry over the next few years. Thank you. And I have plenty of time for questions.

## 1.9 Q&A Session

### 1.9.1 Learning and Skill Development

**Question**: In the past we spent a lot of time dealing with syntax problems or libraries or connections amongst components of the code and that was how we learn by coding like that. But how do we learn now? How do we become better coders? How do we know more to become better product managers of the agent AI?

**Eric**: Yeah, so I think this is a really interesting question and I think there are reasons to be very worried about this and also reasons to be very optimistic about this. I think the reason to be worried like you mentioned is that we are not going to be there in the struggle, in the grind.

I think that is actually okay. I've met some of my professors in college would say like "ah man like coders today aren't as good because they never had to write their assembly by hand. They don't really feel the pain of how to make something run really fast."

I think the positive side of this is that I have found that I'm able to learn about things so much more quickly by using these AI tools. A lot of times when I am coding with Claude I'll be reviewing the code and I'll say "hey Claude I've never seen this library before. Tell me about it. What is it? Why did you choose it over another?" And having that always there pair programmer.

I think what's going to change is that people that are lazy are not going to learn. They're just going to glide by. But if you take the time and you want to learn, there's all these amazing resources and Claude will help you understand what it vibe coded for you.

The other thing I will say is that for learning some of these higher level things about what makes a project go well, what is a feature that gets you product market fit versus flops, we're going to be able to take so many more shots on goal. I feel like especially system engineers or architects, it takes oftentimes like two years to make a big change in a codebase and really come to terms with was that a good architecture decision or not. And if we can collapse that time down to 6 months, I think engineers that are investing in their own time and trying to learn, they're going to be able to learn from four times as many lessons in the same amount of calendar time as long as they're putting in the effort to trying.

### 1.9.2 Planning and Information Balance

**Question**: Going back to your pre-planning process, what's the balance between giving it too much information and too little? Are you giving it a full product requirement document? Is there kind of a standardized template that you put together before you actually move into vibe coding?

**Eric**: Yeah. I think it depends a lot on what you care about. I would say that for things where I don't really care how it does it, I won't talk at all about the implementation details. I'll just say these are my requirements like this is what I want at the end. There's other times where I know the codebase well and I will go into much more depth of like, hey, these are the classes you should use to implement this logic. Look at this example of a similar feature.

I'd say it all comes down to what you care about at the end of the day. I would say though that our models do best when you don't over constrain them. So, you know, if I wouldn't put too much effort into creating a very rigorous format or anything. I would just think about it as like a junior engineer what you would give them in order to succeed.

### 1.9.3 Security Considerations

**Question**: How did you balance effectiveness and cybersecurity? Like there were reports a couple months back of the top 10 vibe coded apps being super vulnerable and a lot of important information was released. Well, not released but proven to be releasable and the person who did it wasn't even like a pro hacker and stuff and so like there's that. How did you balance being able to keep things secure even at a leaf node level and then also being effective because something can be effective but not secure?

**Eric**: Yeah, that's a great question and I think that all comes down to this first point here of being Claude's PM and understanding enough about the context to basically know what is dangerous, know what's safe, and know where you should be careful. And I think yeah, the things that get a lot of press about vibe coding are people that have no business coding at all doing these. And that's fine. That's great for games. That's great for creativity and like having people be able to create. But I think for production systems, you need to know enough about what questions to ask to guide Claude in the right direction. And for our internal case of this example, it was something that's fully offline. And so we knew there weren't any like we were very confident that there was no security problems that could happen into this. In our case it's run in something that's fully offline.

So this is more about people that have no business vibe coding in production for an important system. I will say that.

### 1.9.4 Democratization and Safety

**Question**: But if we look at the numbers right, less than 0.5% of the world's population are software developers and software is an amazing way to scale ideas. So how do you think the products need to change to make it easier for people to vibe code and build software while also avoiding some of the things that we run into with people leaking API keys and things like that?

**Eric**: That's a really great question and I would be super excited to see more products and frameworks emerge that are kind of like provably correct. And maybe what I mean by that is I'm sure people could build some backend systems that the important auth parts, the payment parts are built for you and all you have to do is fill in the UI layer. And you know, you can vibe code that and it basically gives you some nice fill-in-the-blank sandboxes where to put your code.

I feel like there's tons of things like that that could exist. And maybe like the simplest example is like Claude artifacts where Claude can help you write code that gets hosted right there in Claude AI to display. And of course that is safe because it is very limited. There is no auth, there is no payments. It's front end only. But maybe that's a good product idea that someone should do here is build some way to make a provably correct hosting system that can have a backend that you know is safe no matter what shenanigans happens on the front end.

But yeah, I hope people build good tools that are complements to vibe coding.

### 1.9.5 Test-Driven Development

**Question**: For test driven development, do you have any tips because I often see that Claude just spits out the entire implementation and then writes test cases. Sometimes they don't, they fail and then I'm trying to prompt it to write the test cases first but I also don't want to verify them by myself because I haven't seen implementation yet so do you have an iterative approach that you've ever tried for test driven development?

**Eric**: Yeah yeah I definitely, test driven development is very useful in vibe coding as long as you can understand what the test cases are even without that it helps Claude be a little bit more self consistent even if you yourself don't look at the tests.

But a lot of times, I'd say it's easy for Claude to go down a rabbit hole of writing tests that are too implementation specific. When I'm trying to do this, a lot of times I will encourage, I will give Claude examples of like, hey, just write three end-to-end tests and, you know, do the happy path, an error case, and this other error case. And I'm very prescriptive about that. I want the test to be general and end to end. And I think that helps make sure it's something that I can understand and it's something that Claude can do without getting too in the weeds.

I'll also say a lot of times when I'm vibe coding the only part of the code or at least the first part of the code that I'll read is the tests to make sure that if I agree with the tests and the tests pass then I feel pretty good about the code. That works best if you can encourage Claude to write very minimalist end-to-end tests.

### 1.9.6 Understanding Exponential Growth

**Question**: Thank you for the very fascinating talk. I also appreciate that you've done what a lot of people haven't done and tried to interpret one of the more peculiar lines in Karpathy's original post, embrace exponentials. So, I wonder if I could pin you down a little more and say, how would I know if I've embraced the exponentials? Like, what precisely means following that advice? And to maybe put it down a little more in what I think it intends to mean, it sort of maybe alludes to this, the models will get better. Do you think there's some legitimacy in saying just the fact that the models will get better doesn't mean they'll get better at every conceivable dimension we might be imagining we hope they'll be in.

**Eric**: Yeah. So how do I embrace exponentials? Yeah, absolutely. So the I think you got close with the quote of keep assuming the models are going to get better, but it's a step beyond that. The idea of the exponential is not just that they're going to keep getting better, but they're going to get better faster than we can possibly imagine.

And that's kind of like when you can see the shape of the dots here. It's not just that it's getting steadily better, it's that it's getting better and then it goes wild. I think the other funny quote I heard from this this was in Dario and Mike Krieger's talk is machines of loving grace is not science fiction. It's a product roadmap. Even though it sounds like something that's very far out like when you are on an exponential things get wild very fast and faster than you expect.

And I think, you know, if you talk to someone that was doing computers in the 90s, it's like, okay, great. We have a couple kilobytes of RAM. We have a couple more kilobytes of RAM. But if you fast forward to where we are now, it's like we have terabytes. And it's not just that it got twice as good, it's that things got millions of times better. And that's what happens with exponentials over a course of 20 years.

So, we shouldn't think about 20 years from now as what happens if these models are twice as good. We should think about what happens if these models are a million times smarter and faster than they are today, which is wild. We can't even think about what that means. In the same way that someone working on computers in the 90s, I don't think they could think about what would happen to society if a computer was a million times faster than what they were working with. But that's what happened.

And so that's what we mean by the exponential is it's going to go bonkers.

### 1.9.7 Workflow and Tool Management

**Question**: I got a couple questions. When it comes to vibe coding I have two different workflows. I have one where I'm in my terminal and then I have one when I'm in VS Code or Cursor. Which workflow do you use and if you're using Claude Code in the terminal how often do you compact? Because what I find is my functions will get a new name as the longer I vibe code or things kind of go off the rails the longer I go and if I compact it still happens if I create a document to kind of guide it I still have to get it back on track.

**Eric**: Yeah. Great question. I do both. I often code with Claude Code open in my terminal and VS Code. And I'd say that Claude Code is doing most of the editing and I'm reviewing the code as I go in VS Code, which is not true vibe coding in the sense here. Or maybe I'm reviewing just the tests from it.

I like to compact or just start a new session whenever I get Claude to a good stopping point where it feels like, okay, as a human programmer, when would I stop and take a break and maybe go get lunch and then come back. If I feel like I'm at that stage, that's a good time to compact. So maybe I'll start off with having Claude find all the relevant files and make a plan and then I'll say okay write all this into a document and then I'll compact and that gets rid of 100k tokens that it took to create that plan and find all these files and boils it down to a few thousand tokens.

### 1.9.8 Multi-Tool Integration and Codebase Exploration

**Question**: Have you used other tools along with Claude Code to increase your speed a little bit more like running multiple Claude Codes together using git work trees and then merging few things or stack PRs or something like that. Is that something that you personally follow or would advise to? Second question is how do you structurally and in a very nice engineering way approach a part of the codebase that you're not very familiar with but you want to ship a PR in it really fast and you want to do it in a really nice way and not vibe code it. So yeah what are your ways of using Claude Code to help do both these things?

**Eric**: Yep. Yeah. So, I definitely use Claude Code as well as Cursor. And I'd say typically I'll start things with Claude Code and then I'll use Cursor to fix things up. Or if I have very specific changes, if I know exactly the change that I want to do to this file, I'll just do it myself with Cursor and target the exact lines that I know need to change.

The second part of your question was how to get spun up on a new part of the codebase. Before I start trying to write the feature I use Claude Code to help me explore the codebase. So I might say like tell me where in this codebase auth happens or where in this codebase something happens. Tell me similar features to this and have it tell me the file names. Have it tell me the classes that I should look at. And then use that to try to build up a mental picture to make sure that I can do this and not vibe code. Make sure I can still get a good sense of what's happening. And then I go work on the feature with Claude.

Thank you so much. I'll be around and can answer other questions.