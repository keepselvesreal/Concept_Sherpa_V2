# YouTube 대본 - 문장 단위 재조직화

# 목차
---
- 생성 시간: 2025-08-19 08:11:25
- 핵심 내용: YouTube 비디오 "Retrieval Agents Actually Solved AI Coding's Biggest Problem" 대본을 문장 단위로 재조직화
- 상세 내용:
  - 메타데이터 (1-7라인): 영상 URL, 언어, 원본 추출 시간 정보
  - 문장별 시간 구간 (8-378라인): 각 문장의 시작-종료 시간과 완전한 문장 내용
- 상태: 생성됨
- 주소: youtube_transcript_EgXOaH-ZqfU_reorganized
- 참조: youtube_transcript_EgXOaH-ZqfU (원본 파일)
---

**영상 URL:** https://www.youtube.com/watch?v=EgXOaH-ZqfU
**추출 언어:** en
**원본 추출 시간:** 2025-08-18 19:50:15
**재조직화 시간:** 2025-08-19 08:11:25

---

[00:00-00:02] AI coding is constantly evolving.

[00:02-00:08] Whether you use clawed code or cursor, it doesn't matter. People are realizing that simply giving a large prompt to your AI coder is not enough anymore.

[00:08-00:15] This realization led to the introduction of context engineering a while back.

[00:15-00:24] Now, I had problems with this approach as well. Context engineering is basically the art of filling the context window of the model with only the stuff that it needs to know for a specific task.

[00:24-00:26] Sounds good in theory, right?

[00:26-00:40] But here's the issue. You never follow a set path when coding. you encounter errors. You might need to implement something new or you discover you need additional context midway through. When that happens, you're stuck. You need to constantly update your context.

[00:40-00:42] What you really need is your own knowledge base.

[00:42-00:49] And not just any knowledge base, but one through which the AI agent can get the accurate data it wants as fast as possible.

[00:49-00:57] This is where this new agent system, Archon, comes in. Let me give you a clear overview of Archon and then explain how it solves one of the biggest problems in AI coding.

[00:57-01:04] Let's start with the projects tab. I have two projects here, a test project and a task glass project.

[01:04-01:11] Each project contains two essential tabs, docs and tasks. This is your complete context management system.

[01:11-01:15] Your documentation lives here giving your AI agent full knowledge of your project.

[01:15-01:29] When I open this, you'll notice they've added templates. This means when your AI agent connects, whether it's clawed or cursor, it doesn't create random documentation. It follows these templates like architecture documentation or feature PRDS, keeping everything properly organized.

[01:29-01:35] The tasks tab works beautifully with your documentation based on your project scope, meaning what you want to build.

[01:35-01:39] The backlog automatically populates with relevant tasks.

[01:39-01:48] The AI agent manages tasks independently and maintains task memory. It never loses context and always knows which tasks need completion.

[01:48-01:57] You can create unlimited projects and manage them efficiently. In my task class project, for instance, one task sits in the backlog while 13 are actively in progress.

[01:57-02:02] Next is the MCP server which connects Archon to your AI agents.

[02:02-02:04] Setup is remarkably simple.

[02:04-02:12] They have setup commands for all agents like claude code whose command is really hard to search up. This is especially valuable for users uncomfortable with code editors or terminals.

[02:12-02:18] Now, here's the feature that makes Archon exceptional, the knowledge base.

[02:18-02:20] The knowledge base accepts any documentation you need.

[02:20-02:30] You can add links to any tools documentation. For example, I imported the entire Swift UI documentation from Apple's developer site. That's 505 pages containing over 126,000 words.

[02:30-02:40] In the add knowledge base section, you'll find categories of knowledge. You can add URLs or hosted documentation sites.

[02:40-02:49] The applications extend beyond AI coding. You can personalize documentation and create knowledge bases for anything. You can also upload PDFs for custom knowledge or internal documentation.

[02:49-02:55] What makes this different from other tools? Archon implements a complete rag system.

[02:55-03:01] When you install it, you're setting up a proper database for rag instead of simple text search. The system stores data and applies semantic search.

[03:01-03:05] The result is fast, accurate, and personalized retrieval.

[03:05-03:21] Here's a practical example. In my test projects doc section, I can add project specific sources. Say I'm building a Swift app and liquid glass UI just released. LLMs don't know about it yet. The solution is feeding Aron the Swift UI documentation.

[03:21-03:27] I added the docs to the knowledge base, set the crawl depth to two, which is optimal, and let the crawler process everything.

[03:27-03:36] The crawler works programmatically. It follows every link on the site, navigates through menus, enters each page, and extracts all information systematically.

[03:36-03:41] This is a comprehensive system combining context engineering, rag, web scraping, and task management in one platform.

[03:41-03:49] When our community creates something this powerful, others build on it to create even more innovative tools. That's the beauty of this community.

[03:49-03:54] Now, a quick break to tell you about today's sponsor, logs.so.

[03:54-04:03] Ever launch a feature and have no clue if anyone touched it? Or find out about a payment failure only when a customer tweets at you? Logs.so SO shows every sign up, click, payment, and error in one live feed.

[04:03-04:11] No dashboards, no dev console, just a simple timeline anyone on the team can read. You don't have to wire up fancy tools or write code.

[04:11-04:19] Paste one line into your site or drop the snippet into whatever builder you're using and watch events roll in.

[04:19-04:26] The first 1,000 events every month are free forever. That's enough to track a side project or prove value before you even pay a scent.

[04:26-04:31] Ready to see what really happens in your product? Hit the link below and start tracking with logs.so.

[04:31-04:39] So, this is the GitHub repository of Archon. And the first thing you're going to do is come here and copy the link. Then you'll go back into your terminal.

[04:39-04:45] You're going to clone the GitHub repository and add it inside your chosen directory.

[04:45-04:51] You can see that for me, it already exists and I already have it up and running successfully. When I ran it, you can see it completed successfully.

[04:51-04:59] After the GitHub repository is installed, you're going to run this specific command that's shown right here in the GitHub repository. This command will create your env file where you need to put some important variables that I'll show you in just a moment.

[05:05-05:13] Now, since Archon is a proper knowledge hub, it needs a proper database to perform rag and all the AI searching capabilities that it provides.

[05:13-05:18] For this, the author has chosen to use Superbase as the main database. And setting it up is really simple.

[05:18-05:25] First, make sure you have a project created in Superbase. As you can see, I created a project called Archon.

[05:25-05:31] The great thing is you don't need to pay for this. The free version of Superbase is absolutely enough for what we need.

[05:31-05:41] Next, you need to create your database tables inside Superbase. But don't worry about having to do that manually. They've provided an automatically configured setup that makes this incredibly easy.

[05:41-05:52] All you have to do is open the current repository inside Cursor so you can easily access all the files. Just use this command. It'll open the Archon repository directly inside Cursor.

[05:52-06:02] Once you're inside cursor, navigate to the migration folder. There you'll see a complete setup.SQL file with everything configured. Simply copy the whole thing and go back into Superbase.

[06:02-06:17] In the Superbase sidebar, you'll find the SQL editor. You can see that I've already pasted mine, but basically you paste the SQL code there and run it. Once it finishes executing, you'll see the message success and no rules returned. That confirmation means the database has been set up correctly.

[06:17-06:31] Now once you're done with that setup, you need to grab two important credentials. Head into the settings section of Superbase and first go to the data API section. Here you'll get your project URL. Copy that.

[06:31-06:36] Then navigate to API keys. Reveal the service role API key and copy that as well.

[06:36-06:51] Go back to yourv file. Remember the env is a copy of the env.ample file which you created earlier using the cp command. Here you'll paste your superbase URL that you just copied and then paste your service ro key in the appropriate field.

[06:51-07:00] Once you've done that, you'll run the docker compose up command. The first time you run this command, it will take some time as it needs to fetch and build all the docker containers.

[07:00-07:12] For this to work, you do need to have docker running. So make sure docker is turned on and running in the background on your system whether you're on Windows or Mac before executing this command.

[07:12-07:21] Docker will go ahead and start all the containers and you'll see a progress bar showing the setup progress. Once it finishes, you'll see that four containers have been started. Archon agents, Archon server, Archon MCP, and the front end.

[07:21-07:35] Finally, if you go to the Archon UI, which is now running, you'll find it at localhost 3737. Just enter that address in your browser and it will automatically take you through the first step, the onboarding step that gets everything configured for your use.

[07:35-07:44] After you've set everything up and your services are running, when you open the front-end link in your browser, you're going to be greeted with this onboarding flow.

[07:44-07:50] The first thing you'll need is an additional API key. You can go ahead and choose between Google Gemini or OpenAI for this.

[07:50-08:03] In their documentation, they've specifically listed Google Gemini and its free models as a good alternative. They mention that the free rate limited models are completely sufficient for this use case and you won't exceed the limits during normal operation.

[08:03-08:07] I'm just going to go ahead with Open AI. The reason you need to provide another API key is for the rag implementation.

[08:07-08:22] To make rag work, the system needs to convert the words in your documents into numbers based on their meaning. This conversion process is what makes the search so fast and accurate and it requires a model to create these meaningful numerical representations.

[08:22-08:30] Let me take you through the actual process that needs to be done. First, you create a new project like I did. After creating the project, I went into Claude Code and asked it to search for all the projects.

[08:30-08:45] It fetched my project and returned the ID along with the description. In that description, I had defined that it should only use local storage, follow a specific architecture, and be built with Swift UI.

[08:45-08:59] Next, I told it that I wanted to build the app and provided some requirements. For example, I specified that it must use liquid glass and that I just wanted two pages in the app for now. Think of this step as writing a PRD and you can discuss this with claude code and finalize this.

[08:59-09:06] You just need to focus on the features you want. Archon can just then create the docs using the templates that I showed you.

[09:06-09:16] Think of your coding agent as the tool that's only there to execute tasks while Archon is the context box where all your knowledge and instructions live.

[09:16-09:27] Going back to the process, once the documentation was ready and it had the Swift UI knowledge base in it, it needed to create tasks. I told it to break the work into two cycles of tasks for simplicity. It went ahead and started generating tasks.

[09:27-09:36] If you check the tasks tab, you'll see that there are tasks placed in the backlog and the ones that done are awaiting review. Then I told it that the iOS app I made in Xcode was already set up and it just needed to begin development using the manage tasks tool.

[09:36-09:45] Archon's MCP began executing the tasks. Now you might wonder how it knows when to use the documentation.

[09:45-09:58] Before as you know the big issue was that giving some context for a single task and many times that context wouldn't turn out to be enough. With Archon, this problem is completely solved.

[09:58-10:07] The coding agent is integrated with Archon so that whenever it feels even the slightest uncertainty, it automatically fetches the required documentation.

[10:07-10:22] Before creating tasks or PRDs, it already uses rag to gather context. But throughout the entire process, it keeps fetching more documentation if needed. This way, it never relies on an inaccurate web search or the limited context for the task.

[10:22-10:31] And how is this behavior built in? Well, Archon provides a rules file. This file essentially tells the agent how to function with the Archon MCP connector.

[10:31-10:41] You can get this file directly from the settings. Copy the rules and apply them to any agent. There is one specifically for clawed code but the universal one can also be used with any.

[10:41-10:49] You also have the rag settings available. You can choose the model, tweak various options or even use a cheaper alternative with Google's free tier API key.

[10:49-10:58] So moving on, I completed the first cycle and then I ran into a small error in the app which is normal with Swift. It created the error as another task and fixed it as well.

[10:58-11:05] I also gave it some additional instructions and it added those as tasks as well. For example, here it needed to implement the glass morphism effect during the second cycle in the Polish phase.

[11:05-11:17] Now here since it wasn't certain, it performed its rag query to search for results. It didn't find much in that so pulled the code examples and found some helpful implementation in that.

[11:17-11:28] So again it automatically knows when it needs to perform a rag search whenever it's uncertain about something or doesn't have the information. After that it went ahead coded everything and completed the tasks.

[11:28-11:46] Now in a way this is similar to what you've already seen in other framework systems with task management like for example the BMAD method. In my opinion, the BMAD method offers a better flow for coding using the agile method and there is a set path. But until that happens in this tool, it's not really that beginnerfriendly and you might need to experiment to find the perfect flow with this.

[11:46-11:56] But the amazing thing Archon gives you is its knowledge base and that's what I'm encouraging you to take advantage of.

[11:56-12:03] I'm sure that looking at this, people will definitely start building more tools on top of it and that's why I'm really excited about it.

[12:03-12:10] Moving into Xcode in the simulator, you'll see that I had also requested a widget. The code for the widget was completed, but I had to manually add it into the app.

[12:10-12:22] It can't be done automatically with a command. So, I still had to do a bit of manual work, which is why the widget isn't showing here. Other than that, the basic app that I wanted to make was ready and I could use it.

[12:22-12:32] Another thing I want you to know is that Archon is currently in its beta version. This is the beta release and soon enough they're going to be launching the final version. It's already scheduled, so keep an eye out for that.

[12:32-12:40] If there are any major improvements in the workflow or how it's used, I'll definitely make another video to keep you updated. That brings us to the end of this video.

[12:40-12:47] If you'd like to support the channel and help us keep making videos like this, you can do so by using the super thanks button below.

[12:47-12:49] As always, thank you for watching and I'll see you in the next one.