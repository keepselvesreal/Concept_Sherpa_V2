# On-Device Model Performance

### Local Model Capabilities

You can imagine that we can just continue doing this along every other model we want to run. So you can see here, here's GPT5 mini. But we can easily just swap this out. You can see here there's nano, here's mini, here's five. And then we repeat the same thing for the correct OpenAI local models, which are absolutely mind-blowing.

We have 20 billion and 120 billion running right on my M4 Max MacBook Pro. This is a 128 GB unified memory machine. This thing is absolutely cracked. These models run on the device and they are doing agent decoding work as you'll see in these results.

### Detailed Test Results

Let's go ahead and hop back to the results. Pretty excited to share this with you here. But you can see how these prompts are set up - these are our agents and our lower order prompts just detail the exact benchmark that we want run. So on our dummy test the prompt is "what's the capital of the United States, respond in JSON format structure" so we can get all the auxiliary metadata coming out of the nano agent MCP server.

We have another interesting result here. We have the raw outputs. Here's all of our agents that executed - we had nine nano agents firing off. And then we have the respective responses. You can see here we're looking for first 10 lines and last 10 lines in the specific prompt format.

### File Operations Test

We can take a look at the result. Let me just quickly show you exactly what that prompt looked like. So this is a lower order prompt basic read. So if we look at this, we have instructions and then we have variables. And the prompt here is the most important. So we're saying read the readme file. Provide exactly the first 10 lines and the last 10 lines of the file.

So this is an agentic task. This is a little more advanced. We're just stepping up the difficulty scale just a little bit from just asking a simple question. We just want it in this exact response format. So we're testing for instruction following. We're testing for tool use. In a second here, I'll show you the exact tools that our nano agent MCP server can call.

Then we fire off all of our agents and we have an expected output. So, we're just sticking to great prompt patterns. We're writing extraordinarily clearly to our agent, both our primary agent and our sub agents, and we're being really clear about the flow of communication between our agents. We need to make sure that we're orchestrating the communication extraordinarily well.

## Future Implications and Conclusions

So, that's what we're doing here. But the key here is: here's the agentic prompt that's running. Read the readme. Give me the first 10 lines and the last 10 lines. So this is what we're evaluating our models against. So now we can say for this fundamental agent decoding task, how did our models perform?

### Performance Analysis

And we are evaluating on performance. So did it do the job? Speed and cost. Obviously if the model can't do the job, it doesn't matter if it's fast or how much it costs or how cheap it is.

So, you can see kind of some rough grades here. If you look at the overall breakdown of this task, we have some rough grades. It's not all roses when you really flatten the playing field.

Take a look at Opus for instance. We all know that Opus costs, but we don't really realize how much this model costs. It's extraordinarily expensive. And you can see here, for some reason, GPT5 had to churn and turn and churn its output tokens to figure out how to get this response properly. Terrible cost there. I'm actually surprised this chewed up that many tokens. I've seen this run much better, but I have seen some weirdness with GPT5 through the API.

### Breakthrough Week Assessment

This has been a breakthrough week. It's very clear to me that there is more compute than ever to tap into. I'm able to understand and move and work through these innovations because I understand the industry at a fundamental level.

Everything we do is based off just one concept. The big three: context, model, and prompt. Everything is based off these. If you understand these, you can build evals, you can build benchmarks, you can build agents because they're all just scaffolded on top of these.

### Key Insights

So, we have more compute than ever. It's not about the prompt anymore. It's not about the individual model anymore. It's about what the model can do in long chains of tool calls. The true value proposition of models is being exposed. It's real work end to end.

And the thing to keep an eye on is: do you know how to trade off performance, cost, and speed when the time is right? Because I can guarantee you, you don't always need Opus 4. You might be able to settle with GPT5, which is much cheaper, by the way, than Opus 4. Or you might be able to go further. You can just use five mini. Maybe you need to scale to Sonnet four for that task. Fine.

But maybe you can build your own specialized small agent. You can build off from the nano agent codebase that is going to be available to you. Link in the description. I'm going to clean this up and make sure it's available for you so that you can understand agentic coding at a fundamental level.

### Future Outlook

But maybe you can go even further beyond and use a small on-device model. These are only going to get better. So you want to have the infrastructure in place and the tooling in place to understand the capabilities so when it's ready you can hop on it.

I can tell you right now I'm going to be investing more into these models across the board so I know what tasks can be accomplished by what model so I can make the right tradeoff. Engineering is all about tradeoffs: performance, speed, cost. At different times of the day, based on the task you're working on, different things matter.

So super long one. Thanks for sticking with me here. Stay focused and keep building.