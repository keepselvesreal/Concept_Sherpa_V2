## Real Development Process and Results

After you've set everything up and your services are running, when you open the front-end link in your browser, you're going to be greeted with this onboarding flow. The first thing you'll need is an additional API key. You can go ahead and choose between Google Gemini or OpenAI for this.

The reason you need to provide another API key is for the RAG implementation. To make RAG work, the system needs to convert the words in your documents into numbers based on their meaning. This conversion process is what makes the search so fast and accurate and it requires a model to create these meaningful numerical representations.

First, you create a new project like I did. After creating the project, I went into Claude Code and asked it to search for all the projects. It fetched my project and returned the ID along with the description. In that description, I had defined that it should only use local storage, follow a specific architecture, and be built with Swift UI.

Next, I told it that I wanted to build the app and provided some requirements. For example, I specified that it must use Liquid Glass and that I just wanted two pages in the app for now. Think of this step as writing a PRD and you can discuss this with Claude Code and finalize this.

Think of your coding agent as the tool that's only there to execute tasks while Archon is the context box where all your knowledge and instructions live. Going back to the process, once the documentation was ready and it had the Swift UI knowledge base in it, it needed to create tasks.

Now you might wonder how it knows when to use the documentation. Before as you know the big issue was that giving some context for a single task and many times that context wouldn't turn out to be enough. With Archon, this problem is completely solved. The coding agent is integrated with Archon so that whenever it feels even the slightest uncertainty, it automatically fetches the required documentation.