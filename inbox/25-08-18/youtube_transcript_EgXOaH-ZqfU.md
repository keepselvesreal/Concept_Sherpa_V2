# YouTube 대본

**영상 URL:** https://www.youtube.com/watch?v=EgXOaH-ZqfU
**추출 언어:** en
**추출 시간:** 2025-08-18 19:50:15

---

[00:00] AI coding is constantly evolving.
[00:02] Whether you use clawed code or cursor,
[00:04] it doesn't matter. People are realizing
[00:06] that simply giving a large prompt to
[00:08] your AI coder is not enough anymore.
[00:10] This realization led to the introduction
[00:12] of context engineering a while back.
[00:14] Now, I had problems with this approach
[00:16] as well. Context engineering is
[00:18] basically the art of filling the context
[00:20] window of the model with only the stuff
[00:22] that it needs to know for a specific
[00:24] task. Sounds good in theory, right? But
[00:26] here's the issue. You never follow a set
[00:28] path when coding. you encounter errors.
[00:30] You might need to implement something
[00:32] new or you discover you need additional
[00:34] context midway through. When that
[00:36] happens, you're stuck. You need to
[00:38] constantly update your context. What you
[00:40] really need is your own knowledge base.
[00:42] And not just any knowledge base, but one
[00:44] through which the AI agent can get the
[00:47] accurate data it wants as fast as
[00:49] possible. This is where this new agent
[00:51] system, Archon, comes in. Let me give
[00:53] you a clear overview of Archon and then
[00:55] explain how it solves one of the biggest
[00:57] problems in AI coding. Let's start with
[00:59] the projects tab. I have two projects
[01:01] here, a test project and a task glass
[01:04] project. Each project contains two
[01:06] essential tabs, docs and tasks. This is
[01:08] your complete context management system.
[01:11] Your documentation lives here giving
[01:12] your AI agent full knowledge of your
[01:15] project. When I open this, you'll notice
[01:17] they've added templates. This means when
[01:19] your AI agent connects, whether it's
[01:21] clawed or cursor, it doesn't create
[01:23] random documentation. It follows these
[01:25] templates like architecture
[01:26] documentation or feature PRDS, keeping
[01:29] everything properly organized. The tasks
[01:31] tab works beautifully with your
[01:33] documentation based on your project
[01:35] scope, meaning what you want to build.
[01:37] The backlog automatically populates with
[01:39] relevant tasks. The AI agent manages
[01:42] tasks independently and maintains task
[01:44] memory. It never loses context and
[01:46] always knows which tasks need
[01:48] completion. You can create unlimited
[01:50] projects and manage them efficiently. In
[01:52] my task class project, for instance, one
[01:54] task sits in the backlog while 13 are
[01:57] actively in progress. Next is the MCP
[01:59] server which connects Archon to your AI
[02:02] agents. Setup is remarkably simple. They
[02:04] have setup commands for all agents like
[02:06] claude code whose command is really hard
[02:08] to search up. This is especially
[02:10] valuable for users uncomfortable with
[02:12] code editors or terminals. Now, here's
[02:14] the feature that makes Archon
[02:16] exceptional, the knowledge base. The
[02:18] knowledge base accepts any documentation
[02:20] you need. You can add links to any tools
[02:22] documentation. For example, I imported
[02:25] the entire Swift UI documentation from
[02:27] Apple's developer site. That's 505 pages
[02:30] containing over 126,000 words. In the
[02:33] add knowledge base section, you'll find
[02:35] categories of knowledge. You can add
[02:37] URLs or hosted documentation sites. The
[02:40] applications extend beyond AI coding.
[02:42] You can personalize documentation and
[02:45] create knowledge bases for anything. You
[02:47] can also upload PDFs for custom
[02:49] knowledge or internal documentation.
[02:51] What makes this different from other
[02:53] tools? Archon implements a complete rag
[02:55] system. When you install it, you're
[02:57] setting up a proper database for rag
[02:59] instead of simple text search. The
[03:01] system stores data and applies semantic
[03:03] search. The result is fast, accurate,
[03:05] and personalized retrieval. Here's a
[03:07] practical example. In my test projects
[03:09] doc section, I can add project specific
[03:12] sources. Say I'm building a Swift app
[03:14] and liquid glass UI just released. LLMs
[03:17] don't know about it yet. The solution is
[03:18] feeding Aron the Swift UI documentation.
[03:21] I added the docs to the knowledge base,
[03:23] set the crawl depth to two, which is
[03:25] optimal, and let the crawler process
[03:27] everything. The crawler works
[03:28] programmatically. It follows every link
[03:30] on the site, navigates through menus,
[03:32] enters each page, and extracts all
[03:34] information systematically. This is a
[03:36] comprehensive system combining context
[03:39] engineering, rag, web scraping, and task
[03:41] management in one platform. When our
[03:43] community creates something this
[03:45] powerful, others build on it to create
[03:47] even more innovative tools. That's the
[03:49] beauty of this community. Now, a quick
[03:52] break to tell you about today's sponsor,
[03:54] logs.so. Ever launch a feature and have
[03:56] no clue if anyone touched it? Or find
[03:58] out about a payment failure only when a
[04:00] customer tweets at you? Logs.so SO shows
[04:03] every sign up, click, payment, and error
[04:05] in one live feed. No dashboards, no dev
[04:08] console, just a simple timeline anyone
[04:10] on the team can read. You don't have to
[04:11] wire up fancy tools or write code. Paste
[04:14] one line into your site or drop the
[04:16] snippet into whatever builder you're
[04:17] using and watch events roll in. The
[04:19] first 1,000 events every month are free
[04:22] forever. That's enough to track a side
[04:24] project or prove value before you even
[04:26] pay a scent. Ready to see what really
[04:27] happens in your product? Hit the link
[04:29] below and start tracking with logs.so.
[04:31] So, this is the GitHub repository of
[04:34] Archon. And the first thing you're going
[04:35] to do is come here and copy the link.
[04:37] Then you'll go back into your terminal.
[04:39] You're going to clone the GitHub
[04:41] repository and add it inside your chosen
[04:43] directory. You can see that for me, it
[04:45] already exists and I already have it up
[04:47] and running successfully. When I ran it,
[04:49] you can see it completed successfully.
[04:51] After the GitHub repository is
[04:53] installed, you're going to run this
[04:55] specific command that's shown right here
[04:56] in the GitHub repository. This command
[04:59] will create your env file where you need
[05:01] to put some important variables that
[05:03] I'll show you in just a moment. Now,
[05:05] since Archon is a proper knowledge hub,
[05:07] it needs a proper database to perform
[05:09] rag and all the AI searching
[05:11] capabilities that it provides. For this,
[05:13] the author has chosen to use Superbase
[05:16] as the main database. And setting it up
[05:18] is really simple. First, make sure you
[05:20] have a project created in Superbase. As
[05:22] you can see, I created a project called
[05:25] Archon. The great thing is you don't
[05:27] need to pay for this. The free version
[05:28] of Superbase is absolutely enough for
[05:31] what we need. Next, you need to create
[05:33] your database tables inside Superbase.
[05:35] But don't worry about having to do that
[05:37] manually. They've provided an
[05:39] automatically configured setup that
[05:41] makes this incredibly easy. All you have
[05:43] to do is open the current repository
[05:45] inside Cursor so you can easily access
[05:48] all the files. Just use this command.
[05:50] It'll open the Archon repository
[05:52] directly inside Cursor. Once you're
[05:54] inside cursor, navigate to the migration
[05:56] folder. There you'll see a complete
[05:58] setup.SQL file with everything
[06:00] configured. Simply copy the whole thing
[06:02] and go back into Superbase. In the
[06:04] Superbase sidebar, you'll find the SQL
[06:06] editor. You can see that I've already
[06:08] pasted mine, but basically you paste the
[06:11] SQL code there and run it. Once it
[06:13] finishes executing, you'll see the
[06:14] message success and no rules returned.
[06:17] That confirmation means the database has
[06:19] been set up correctly. Now once you're
[06:21] done with that setup, you need to grab
[06:23] two important credentials. Head into the
[06:25] settings section of Superbase and first
[06:27] go to the data API section. Here you'll
[06:29] get your project URL. Copy that. Then
[06:31] navigate to API keys. Reveal the service
[06:34] role API key and copy that as well. Go
[06:36] back to yourv file. Remember the env is
[06:39] a copy of the env.ample file which you
[06:42] created earlier using the cp command.
[06:45] Here you'll paste your superbase URL
[06:47] that you just copied and then paste your
[06:49] service ro key in the appropriate field.
[06:51] Once you've done that, you'll run the
[06:52] docker compose up command. The first
[06:54] time you run this command, it will take
[06:56] some time as it needs to fetch and build
[06:58] all the docker containers. For this to
[07:00] work, you do need to have docker
[07:02] running. So make sure docker is turned
[07:04] on and running in the background on your
[07:06] system whether you're on Windows or Mac
[07:08] before executing this command. Docker
[07:10] will go ahead and start all the
[07:12] containers and you'll see a progress bar
[07:14] showing the setup progress. Once it
[07:15] finishes, you'll see that four
[07:17] containers have been started. Archon
[07:19] agents, Archon server, Archon MCP, and
[07:21] the front end. Finally, if you go to the
[07:23] Archon UI, which is now running, you'll
[07:26] find it at localhost 3737. Just enter
[07:29] that address in your browser and it will
[07:31] automatically take you through the first
[07:33] step, the onboarding step that gets
[07:35] everything configured for your use.
[07:37] After you've set everything up and your
[07:39] services are running, when you open the
[07:40] front-end link in your browser, you're
[07:42] going to be greeted with this onboarding
[07:44] flow. The first thing you'll need is an
[07:46] additional API key. You can go ahead and
[07:48] choose between Google Gemini or OpenAI
[07:50] for this. In their documentation,
[07:52] they've specifically listed Google
[07:54] Gemini and its free models as a good
[07:56] alternative. They mention that the free
[07:58] rate limited models are completely
[07:59] sufficient for this use case and you
[08:01] won't exceed the limits during normal
[08:03] operation. I'm just going to go ahead
[08:04] with Open AI. The reason you need to
[08:07] provide another API key is for the rag
[08:09] implementation. To make rag work, the
[08:11] system needs to convert the words in
[08:13] your documents into numbers based on
[08:15] their meaning. This conversion process
[08:17] is what makes the search so fast and
[08:19] accurate and it requires a model to
[08:21] create these meaningful numerical
[08:22] representations. Let me take you through
[08:25] the actual process that needs to be
[08:26] done. First, you create a new project
[08:28] like I did. After creating the project,
[08:30] I went into Claude Code and asked it to
[08:33] search for all the projects. It fetched
[08:35] my project and returned the ID along
[08:37] with the description. In that
[08:38] description, I had defined that it
[08:40] should only use local storage, follow a
[08:43] specific architecture, and be built with
[08:45] Swift UI. Next, I told it that I wanted
[08:47] to build the app and provided some
[08:49] requirements. For example, I specified
[08:51] that it must use liquid glass and that I
[08:54] just wanted two pages in the app for
[08:55] now. Think of this step as writing a PRD
[08:58] and you can discuss this with claude
[08:59] code and finalize this. You just need to
[09:02] focus on the features you want. Archon
[09:04] can just then create the docs using the
[09:06] templates that I showed you. Think of
[09:08] your coding agent as the tool that's
[09:10] only there to execute tasks while Archon
[09:12] is the context box where all your
[09:14] knowledge and instructions live. Going
[09:16] back to the process, once the
[09:17] documentation was ready and it had the
[09:19] Swift UI knowledge base in it, it needed
[09:21] to create tasks. I told it to break the
[09:24] work into two cycles of tasks for
[09:26] simplicity. It went ahead and started
[09:27] generating tasks. If you check the tasks
[09:30] tab, you'll see that there are tasks
[09:32] placed in the backlog and the ones that
[09:34] done are awaiting review. Then I told it
[09:36] that the iOS app I made in Xcode was
[09:38] already set up and it just needed to
[09:40] begin development using the manage tasks
[09:42] tool. Archon's MCP began executing the
[09:45] tasks. Now you might wonder how it knows
[09:47] when to use the documentation. Before as
[09:50] you know the big issue was that giving
[09:52] some context for a single task and many
[09:54] times that context wouldn't turn out to
[09:56] be enough. With Archon, this problem is
[09:58] completely solved. The coding agent is
[10:00] integrated with Archon so that whenever
[10:02] it feels even the slightest uncertainty,
[10:05] it automatically fetches the required
[10:07] documentation. Before creating tasks or
[10:09] PRDs, it already uses rag to gather
[10:12] context. But throughout the entire
[10:14] process, it keeps fetching more
[10:15] documentation if needed. This way, it
[10:18] never relies on an inaccurate web search
[10:20] or the limited context for the task. And
[10:22] how is this behavior built in? Well,
[10:24] Archon provides a rules file. This file
[10:27] essentially tells the agent how to
[10:28] function with the Archon MCP connector.
[10:31] You can get this file directly from the
[10:32] settings. Copy the rules and apply them
[10:35] to any agent. There is one specifically
[10:37] for clawed code but the universal one
[10:39] can also be used with any. You also have
[10:41] the rag settings available. You can
[10:43] choose the model, tweak various options
[10:45] or even use a cheaper alternative with
[10:47] Google's free tier API key. So moving
[10:49] on, I completed the first cycle and then
[10:52] I ran into a small error in the app
[10:54] which is normal with Swift. It created
[10:56] the error as another task and fixed it
[10:58] as well. I also gave it some additional
[11:00] instructions and it added those as tasks
[11:03] as well. For example, here it needed to
[11:05] implement the glass morphism effect
[11:07] during the second cycle in the Polish
[11:09] phase. Now here since it wasn't certain,
[11:11] it performed its rag query to search for
[11:13] results. It didn't find much in that so
[11:15] pulled the code examples and found some
[11:17] helpful implementation in that. So again
[11:20] it automatically knows when it needs to
[11:22] perform a rag search whenever it's
[11:24] uncertain about something or doesn't
[11:25] have the information. After that it went
[11:28] ahead coded everything and completed the
[11:30] tasks. Now in a way this is similar to
[11:32] what you've already seen in other
[11:34] framework systems with task management
[11:36] like for example the BMAD method. In my
[11:38] opinion, the BMAD method offers a better
[11:40] flow for coding using the agile method
[11:42] and there is a set path. But until that
[11:44] happens in this tool, it's not really
[11:46] that beginnerfriendly and you might need
[11:48] to experiment to find the perfect flow
[11:50] with this. But the amazing thing Archon
[11:52] gives you is its knowledge base and
[11:54] that's what I'm encouraging you to take
[11:56] advantage of. I'm sure that looking at
[11:57] this, people will definitely start
[11:59] building more tools on top of it and
[12:01] that's why I'm really excited about it.
[12:03] Moving into Xcode in the simulator,
[12:05] you'll see that I had also requested a
[12:07] widget. The code for the widget was
[12:08] completed, but I had to manually add it
[12:10] into the app. It can't be done
[12:12] automatically with a command. So, I
[12:14] still had to do a bit of manual work,
[12:16] which is why the widget isn't showing
[12:18] here. Other than that, the basic app
[12:20] that I wanted to make was ready and I
[12:22] could use it. Another thing I want you
[12:23] to know is that Archon is currently in
[12:25] its beta version. This is the beta
[12:27] release and soon enough they're going to
[12:29] be launching the final version. It's
[12:30] already scheduled, so keep an eye out
[12:32] for that. If there are any major
[12:34] improvements in the workflow or how it's
[12:36] used, I'll definitely make another video
[12:38] to keep you updated. That brings us to
[12:40] the end of this video. If you'd like to
[12:42] support the channel and help us keep
[12:43] making videos like this, you can do so
[12:45] by using the super thanks button below.
[12:47] As always, thank you for watching and
[12:49] I'll see you in the next one.