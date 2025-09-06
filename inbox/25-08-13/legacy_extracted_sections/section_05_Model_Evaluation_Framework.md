# Model Evaluation Framework

<!-- 추출 정보
노드 ID: 5
제목: Model Evaluation Framework
추출 길이: 1,723자
추출 시간: 2025-08-13 17:34:03
-->

## Model Evaluation Framework

There is one trend that matters above all. Right now, it doesn't matter if we're talking about GPT5, whatever Anthropic has cooking next, the cursor CLI or any other model that's getting put out right now, open source, closed source, there is one thing everyone is focused on. If you've been paying any attention, you know exactly what it is. It is the agent architecture.

### Why Agents Matter

Why does everyone care so much about agents? First, let's understand how you and I, engineers with our boots on the ground, can have a better, deeper understanding of these models' agentic performance. It's not about a single prompt call anymore. It's about how well your agent chains together multiple tools to accomplish real engineering results on your behalf.

### Initial Surprising Results

What just happened with this prompt? You can see here we have rankings. Surprisingly, we have Claude 3 Haiku outperforming all of our other models. If you look at this, it looks backward. We would expect these models to be on top and these other models to be on the bottom. What's going on?

We're evaluating all of our models against each other in a fair playing field where we care about performance, speed, and cost as a collective. These agents are operating in a nano agent, a new MCP server to create a fair playing field where every one of these models is scaffolded with the same context and prompt. Two of the big three. And then we get to see how they truly perform.

If we put these models inside Claude Code, I can guarantee you Opus and Sonnet will outperform. But you can see here for this extremely simple task, "what's the capital?" we can see very different results out of the box.
