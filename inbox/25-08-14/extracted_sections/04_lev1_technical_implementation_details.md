## Technical Implementation Details

Let's open up this codebase and understand the setup. As usual, we have our primary agentic directories. We have our plans. We have our application specific nano agent here. We have our app docs, AI docs, and most importantly, our commands and our agents.

So, if we open up commands, you can see we have this directory perf. So inside of Perf you can see we have a hop - a higher order prompt - and we have lops - lower order prompts.

So this is a powerful prompt orchestration or prompt engineering or context engineering, whatever you want to call it. This is a powerful prompt orchestration technique you can use to reuse prompts and pass in prompts as a lower level. We've covered this on the channel.

But you can see here we have a simple grading system. S through F where S is the best and F is the worst. We have a classic prompt format. We can collapse everything to quickly understand it. Use the nano agent MCP server, execute and then report the results in the response format. And so you can see the response format is a simple grading scheme.

We are using Claude code Opus 4.1 as an LLM as a judge to manage all this for us. And then inside the evaluation details, we're just passing in the lops, the lower order prompts - the prompts that contain the detail that we want to swap in and out as we evaluate different agentic behavior.

If we open up the terminal again, we can see how we're doing here. Looks like we are waiting on GPT OSS 20 billion and everyone else has completed. Not a ton of surprises there. On device does take some time to run. There we go. We just got that completed and now Claude code is going to formulate these results into a concrete response for us. It's going to do the evaluation.

So you can see those tokens streaming in there. Hopefully I still have enough Opus for a great evaluation here. Let's see how that goes. But so we have a higher order prompt here and then here's our eval one that we ran. This is our dummy test.