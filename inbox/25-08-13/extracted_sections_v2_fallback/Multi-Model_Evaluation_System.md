# Multi-Model Evaluation System

Looking at the document structure, I can see that "Multi-Model Evaluation System" appears to be a subsection header within the "Testing Scenarios and Results" section, and "Prompt Orchestration Technique" is the next subsection at the same level.

Here is the text between these two section headers:

We're running a multi-model evaluation system inside of Claude Code. So, we prompt a higher order prompt. We pass in a lower order prompt. We then have our primary agent kick off a slew of respective models running against the nano agent MCP server with a few very specific tools.

You can think of this server as like a micro Gemini CLI, a micro codec, a micro Claude code server that our agents can run against in a fair playing field. You can see our agents are starting to respond here and then they return the results and of course they report back to the primary agent and then our primary agent reports back to us.