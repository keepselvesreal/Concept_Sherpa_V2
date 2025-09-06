# 속성
process_status:

# 추출


# 내용
## Testing Scenarios and Results

And of course, we're going to scale this up. Let's go ahead and throw a harder, more agentic problem at these models. I'll run that hop. Hop is higher order prompt. We'll break that down in just a second. And then we have this prompt that we're passing into this prompt. Basic read test. Let's fire this off.

We're running a multi-model evaluation system inside of Claude Code. So, we prompt a higher order prompt. We pass in a lower order prompt. We then have our primary agent kick off a slew of respective models running against the nano agent MCP server with a few very specific tools.

You can think of this server as like a micro Gemini CLI, a micro codec, a micro Claude code server that our agents can run against in a fair playing field. You can see our agents are starting to respond here and then they return the results and of course they report back to the primary agent and then our primary agent reports back to us.

So this is the multi-model evaluation workflow. Higher order prompt, lower order prompt. We have models that call our nano agent MCP server and the whole point here is to create a true even playing field. You and I need to evaluate agentic behavior against these models and understand the tradeoffs they all have: performance, speed, cost. All of these mattered.

You can see our results coming in here. Let's go ahead and dive in to this codebase, the nano agent codebase, and understand exactly how this is formatted so that we can benchmark brand new fresh state-of-the-art models like GPT5 against the new Opus 4.1. And ultra excitingly, these brand new GPT open-source models, OpenAI absolutely cooked on these models. Again, these are running right on my machine right now.

# 구성
