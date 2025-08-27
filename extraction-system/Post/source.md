---
created: 2025-08-27T16:28:10 (UTC +09:00)
tags: []
source: https://medium.com/vibe-coding/how-i-turn-claude-into-a-systems-engineering-genius-with-one-prompt-d342af0f517c
author: Alex Dunlop
---

# How I Turn Claude Into a Systems Engineering Genius With One Prompt | Vibe Coding

> ## Excerpt
> Learn modular architecture principles that scale. Turn tangled React code into replaceable components using AI prompts from a legendary C programmer.

---
Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*UlwN36mKsWn1Hj1G-ihWSw.png)

Image I created using Midjourney then edited with Figma

## **How a legendary systems engineer’s lecture became my most powerful AI prompt**

[

![Alex Dunlop](https://miro.medium.com/v2/resize:fill:48:48/1*mWvQckMd9GIigTpeHXsv5A.png)



](https://medium.com/@alexjamesdunlop?source=post_page---byline--d342af0f517c---------------------------------------)

Last month I found something that changed how I architect software projects. A lecture from a C engineer named Eskil Steenberg, changed the way I think about systems.

I took this lecture and turned it into three AI prompts that now guide me through every refactor or new project I do.

[Not a Medium member? Keep reading for free by clicking here.](https://medium.com/@alexjamesdunlop/how-i-turn-claude-into-a-systems-engineering-genius-with-one-prompt-d342af0f517c?sk=94dbed9acf55dba92fc296042f5d86fe)

Instead of focusing on preventing AI from creating complex code, I can now break everything up into perfect “black boxes” that any developer _(or AI developer)_ can understand and replace.

## The Problem That Led Me Here

Recently, [Mentis](https://medium.com/vibe-coding/why-im-open-sourcing-the-component-every-chat-app-needs-09ea6fe44f9b) _(my open-source project)_ has had complex bugs which led me to hit a massive wall. Massive shout out to [Abdelrahman](https://github.com/abdelrahmanrafaat) for helping to test and report these issues.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1050/1*xI-IRckpmO2sQvnVUgvqNg.png)

Complex issues were caused by weird DOM interactions with React

A lot of the problems stem from DOM manipulation with React, these kinds of bugs make me question my life and sometimes why I started the project in the first place.

The codebase started to grow into a mess where fixing one issue broke another. My tests couldn’t catch everything because the DOM would render differently than how React intended.

## The Discovery That Changed My Software Approach

While taking a break from fixing issues, I came across Eskil Steenberg’s lecture “Architecting LARGE Software Projects”. This guy builds everything from 3D engines to networked games, all in C.

These are my favourite of his core principles:

-   **Constant developer velocity** — _regardless of project size._
-   **One module, one person** — _one person should be able to do everything (given enough time)_.
-   **Everything should be replaceable** — _if you can’t understand it, you can rewrite it easily._
-   **Black box interfaces** — _modules communicate through clean APIs._
-   **Writing 5 lines today** — _rather than editing 1 line later (context switching affects velocity)._

He also suggested making modules that can be reused in different projects which I really like.

In the lecture, he gives an example of how to build a system built for a fighter jet. This helped me realise how much simpler my task is, but my approach needed to change.

> “It’s faster to write five lines of code today than to write one line today and then have to edit it in the future.” — Eskil Steenberg

I would highly recommend watching the video:

## Converting The Theory Of The Lecture

After taking in Eskil’s amazing lecture, it took me a while to really understand _(I even rewatched it a couple of times)_.

The main thing I struggled with was Eskil’s lecture was built for C, a low level language and I’m building for React.

That’s when I had an amazing idea, I took the complete transcript of the lecture and built prompts from it.

I built three prompts that I use:

1.  **Claude Code Prompt** — _For hands on development._
2.  **Claude Prompt** — _For planning and designing._
3.  **Cursor Prompt** — _Debugging and mainly testing strategies._

These prompts are built for any language and any framework. Teaching AI to think on a much larger scale.

## The Lightbulb Context Moment

The prompts were working great, but they had a big issue. They worked better for new projects only. That’s when I remembered another technique I have been using.

The big problem with AI refactoring is you need certainty. With certainty, you need control over what’s changing.

The architecture prompts provide excellent plans for breaking refactors into bite sized chunks. My workflow has become:

-   Focus on a single folder.
-   Pass the context and prompt to Claude.
-   Come up with a strategic plan.
-   Execute that plan using either Claude Code or Cursor.

## My Real Results

I passed my entire Mentis context into Claude with the new architecture prompt and asked for some help.

_The response blew me away._

I needed to interface directly with the DOM instead of relying on React’s unpredictable behaviour.

This new black box DOM interface implementation would allow me to completely reuse the code for different frameworks with minimal overhead.

Something I never thought would be possible and something directly the prompt came up with directly.

## Why This Matters With AI Development

Following Eskil’s principle: “**Everything should be replaceable”** — _if you can’t understand it, you can rewrite it easily._

We can transform some of AI’s biggest weaknesses into a new superpower by structuring our systems as modular, replaceable components.

Now when AI generates code we don’t understand, we can easily replace that module. This allows AI to build something fast while giving us the freedom to refactor or completely rewrite modules when needed.

Everything becomes manageable bite sized chunks.

_Use the power of AI with the power of large systems._

## These Prompts Change Everything

I’ve packaged everything into a GitHub repo with all three prompts and the original video transcript.

View the [prompts here](https://github.com/Alexanderdunlop/ai-architecture-prompts).

## At The End Of The Day

Eskil’s insights are great, focusing on reducing cognitive load (context switching included) and not depending on a single person.

In the new AI era, this is more important than ever, if AI creates something complex or buggy you are able to replace just that module without breaking anything else.

I have spent weeks testing this approach before sharing it. The results for me personally make it a no brainer. Something appeared that I would have never thought of by myself.

_I’m not affiliated with Anthropic, Eskil Steenberg, or any of the tools mentioned. All opinions and experiences shared are based on my own developer experiences and thoughts._

### Resources:

-   [Eskil’s great youtube video](https://www.youtube.com/watch?v=sSpULGNHyoI).
-   [Mentis](https://github.com/alexanderdunlop/mentis).
-   [Prompts & Transcript repo](https://github.com/Alexanderdunlop/ai-architecture-prompts).

### Related Posts:
