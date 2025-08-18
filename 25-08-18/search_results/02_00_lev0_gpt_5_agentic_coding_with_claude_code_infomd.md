# 속성
---
source_type: None
structure_type: None
document_language: None
similarity_score: 0.3776
search_dimension: content

# 추출
---
## 핵심 내용
이 글은 GPT-5, Opus 4.1, 그리고 로컬에서 실행되는 오픈소스 모델들을 에이전트 코딩 작업에서 성능, 속도, 비용 측면으로 비교 평가한 실험에 관한 내용입니다. Claude Code를 사용하여 멀티 모델 평가 시스템을 구축하고, 각 모델이 파일 읽기와 같은 에이전트 작업을 수행할 때의 실제 성능을 측정했습니다. 핵심 결론은 단순한 프롬프트 성능보다는 도구 체인을 통한 에이전트 작업 능력이 중요하며, 작업에 따라 성능-비용-속도의 적절한 트레이드오프를 선택하는 것이 핵심이라는 것입니다.

## 상세 핵심 내용
이 연구는 최신 AI 모델들의 **에이전트 코딩 능력**을 실제 환경에서 평가한 혁신적인 실험입니다. GPT-5, Opus 4.1, Sonnet, Haiku와 함께 M4 Max MacBook Pro에서 직접 실행되는 20억 및 1200억 파라미터 GPT 오픈소스 모델들을 동일한 조건에서 비교했습니다.

**평가 방법론**의 핵심은 Claude Code 기반의 **멀티 모델 평가 시스템**입니다. 각 모델이 "nano agent MCP 서버"라는 표준화된 도구 세트에 접근하여 공정한 경쟁 환경을 조성했습니다. 이는 마치 "마이크로 Gemini CLI"나 "마이크로 Claude Code 서버"처럼 작동하여 모든 모델이 동등한 조건에서 에이전트 작업을 수행할 수 있게 합니다.

**실험 구조**는 높은 차원의 프롬프트(HOP: Higher Order Prompt)와 낮은 차원의 프롬프트(LOP: Lower Order Prompt)를 활용한 프롬프트 오케스트레이션 기법을 사용했습니다. 실제 테스트는 "미국의 수도는?" 같은 기본 질문부터 "README 파일의 첫 10줄과 마지막 10줄을 읽어라"와 같은 도구 사용이 필요한 에이전트 작업까지 단계적으로 진행되었습니다.

**놀라운 결과**는 Claude 3 Haiku가 일부 작업에서 더 비싼 모델들을 능가했다는 점입니다. 이는 단순한 벤치마크 점수가 아닌 **실제 에이전트 성능**이 중요함을 보여줍니다. 특히 Opus 4.1은 뛰어난 성능을 보였지만 극도로 높은 비용이 문제였고, GPT-5는 의외로 많은 토큰을 소모하며 비효율적인 모습을 보였습니다.

**핵심 교훈**은 모델 선택이 작업별 **성능-비용-속도 트레이드오프**를 기반으로 이루어져야 한다는 것입니다. 모든 작업에 최고 성능 모델이 필요한 것이 아니며, 상황에 따라 저렴한 모델이나 로컬 모델이 더 적합할 수 있습니다.

## 주요 화제
- 멀티모델 에이전트 성능 비교 평가: GPT-5, Opus 4.1, Sonnet, Haiku 등 다양한 AI 모델들을 동일한 조건에서 성능, 속도, 비용 측면에서 비교 분석
- Claude Code 기반 에이전트 아키텍처: 에이전트 체인을 통해 다중 도구를 연결하여 실제 엔지니어링 작업을 수행하는 시스템 구조 설명
- 나노 에이전트 MCP 서버 구현: 공정한 모델 비교를 위한 마이크로 서비스 형태의 에이전트 평가 플랫폼 개발
- 온디바이스 로컬 LLM 성능 검증: M4 Max MacBook Pro에서 GPT OSS 20억/120억 파라미터 모델의 실시간 에이전트 작업 수행 능력 테스트
- 프롬프트 오케스트레이션 기법: 상위 프롬프트(HOP)와 하위 프롬프트(LOP)를 조합한 계층적 프롬프트 엔지니어링 방법론
- LLM-as-a-Judge 평가 시스템: Claude Code Opus 4.1을 심사위원으로 활용한 S~F 등급 기반 모델 성능 자동 평가 체계
- 에이전틱 코딩의 미래 전망: 개별 모델 성능보다 도구 체인 연결을 통한 실제 작업 완수 능력이 중요해지는 패러다임 변화
- 성능-비용-속도 트레이드오프 전략: 작업 유형과 상황에 따른 최적 모델 선택을 위한 의사결정 프레임워크

## 부차 화제
- 프롬프트 오케스트레이션 기법(Higher Order Prompt/Lower Order Prompt): 상위 수준 프롬프트와 하위 수준 프롬프트를 조합하여 재사용 가능한 프롬프트 구조를 만드는 컨텍스트 엔지니어링 기법을 설명

- 평가 등급 시스템(S-F Grading): S등급(최고)부터 F등급(최악)까지의 단순한 등급 체계를 사용하여 모델 성능을 객관적으로 측정하는 방법을 제시

- 나노 에이전트 MCP 서버: 공정한 경쟁 환경을 위해 모든 모델이 동일한 도구와 컨텍스트에 접근할 수 있도록 하는 마이크로 서비스 형태의 평가 인프라를 소개

- 온디바이스 로컬 모델 성능: M4 Max MacBook Pro에서 20억/1200억 파라미터 GPT 오픈소스 모델을 직접 실행하며 로컬 AI 모델의 실용적 성능을 검증

- 에이전트 통신 오케스트레이션: 기본 에이전트, 서브 에이전트, 나노 에이전트 간의 명확한 커뮤니케이션 플로우 설계를 통한 멀티 에이전트 시스템 구축 방법론을 다룸

- 파일 작업 테스트 시나리오: README 파일의 첫 10줄과 마지막 10줄을 정확히 추출하는 에이전트 작업을 통해 도구 사용 능력과 명령 수행 정확도를 평가

- 성능-속도-비용 트레이드오프 분석: 실제 업무에서 상황에 따라 Opus 4, GPT-5, Sonnet 등 다른 모델을 선택해야 하는 엔지니어링 의사결정의 중요성을 강조

- 컨텍스트-모델-프롬프트 삼위일체: 모든 AI 시스템 구축의 기반이 되는 세 가지 핵심 개념을 중심으로 한 에이전트 아키텍처 설계 철학을 제시

# 내용
---
# GPT-5 Agentic Coding with Claude Code

## Introduction and Overview

It's incredible what you can do with a single prompt. We're running GPT5 Mini Nano right next to Opus, Opus 41, Sonnet, Haiku, and the new GPT OSS 20 billion and 120 billion that are running directly on my M4 Max MacBook Pro. 

You can hear the agents are completing their work. Agent complete in parallel - we have natural language responses coming back to us and at the end here we're going to get a concrete comparison of how these models performed across the most important three dimensions: performance, speed, and cost.

We have a brand new agentic model lineup that we need to break down in this video. We're going to look at a concrete way of how we can flatten the playing field to really understand how these models perform side by side. All of our cloud code sub agents running in their own respective nano agents have finished their work. All set and ready for the next step.

We have concrete responses and concrete grades for every single model. So we are using Claude code running Opus 4.1 in the LLM as a judge pattern to determine what models are giving us the best results. And you can see something really awesome here. Total cost on GPT OSS: $0.

### Core Questions

In this video we dive into fundamental agent coding and attempt to answer these questions:
- Can GPT5 compete with Opus 4.1? 
- Has useful on-device local LLM performance been achieved?
- What's the best way to organize all the compute available to you?

If these questions interest you, stick around and let's see how our agents perform on fundamental agentic coding tasks.

### Beyond Benchmark Regurgitation

As you've seen already, every single tech YouTuber, content creator, they've turned the camera on, recorded the screen, and literally just spat back out the benchmarks of all these brand new models back out to you. Just regurgitated exactly what the post tells you itself.

If you've been with the channel for any amount of time, you know that we don't do that here. We dive deeper. We actually use this technology and we develop a deep understanding so that we can choose and select the best tool for the job at hand.

## Model Evaluation Framework

There is one trend that matters above all. Right now, it doesn't matter if we're talking about GPT5, whatever Anthropic has cooking next, the cursor CLI or any other model that's getting put out right now, open source, closed source, there is one thing everyone is focused on. If you've been paying any attention, you know exactly what it is. It is the agent architecture.

### Why Agents Matter

Why does everyone care so much about agents? First, let's understand how you and I, engineers with our boots on the ground, can have a better, deeper understanding of these models' agentic performance. It's not about a single prompt call anymore. It's about how well your agent chains together multiple tools to accomplish real engineering results on your behalf.

### Initial Surprising Results

What just happened with this prompt? You can see here we have rankings. Surprisingly, we have Claude 3 Haiku outperforming all of our other models. If you look at this, it looks backward. We would expect these models to be on top and these other models to be on the bottom. What's going on?

We're evaluating all of our models against each other in a fair playing field where we care about performance, speed, and cost as a collective. These agents are operating in a nano agent, a new MCP server to create a fair playing field where every one of these models is scaffolded with the same context and prompt. Two of the big three. And then we get to see how they truly perform.

If we put these models inside Claude Code, I can guarantee you Opus and Sonnet will outperform. But you can see here for this extremely simple task, "what's the capital?" we can see very different results out of the box.

## Testing Scenarios and Results

And of course, we're going to scale this up. Let's go ahead and throw a harder, more agentic problem at these models. I'll run that hop. Hop is higher order prompt. We'll break that down in just a second. And then we have this prompt that we're passing into this prompt. Basic read test. Let's fire this off.

### Multi-Model Evaluation System

We're running a multi-model evaluation system inside of Claude Code. So, we prompt a higher order prompt. We pass in a lower order prompt. We then have our primary agent kick off a slew of respective models running against the nano agent MCP server with a few very specific tools.

You can think of this server as like a micro Gemini CLI, a micro codec, a micro Claude code server that our agents can run against in a fair playing field. You can see our agents are starting to respond here and then they return the results and of course they report back to the primary agent and then our primary agent reports back to us.

### Prompt Orchestration Technique

So this is the multi-model evaluation workflow. Higher order prompt, lower order prompt. We have models that call our nano agent MCP server and the whole point here is to create a true even playing field. You and I need to evaluate agentic behavior against these models and understand the tradeoffs they all have: performance, speed, cost. All of these mattered.

You can see our results coming in here. Let's go ahead and dive in to this codebase, the nano agent codebase, and understand exactly how this is formatted so that we can benchmark brand new fresh state-of-the-art models like GPT5 against the new Opus 4.1. And ultra excitingly, these brand new GPT open-source models, OpenAI absolutely cooked on these models. Again, these are running right on my machine right now.

## Technical Implementation Details

Let's open up this codebase and understand the setup. As usual, we have our primary agentic directories. We have our plans. We have our application specific nano agent here. We have our app docs, AI docs, and most importantly, our commands and our agents.

### Command Structure

So, if we open up commands, you can see we have this directory perf. So inside of Perf you can see we have a hop - a higher order prompt - and we have lops - lower order prompts.

So this is a powerful prompt orchestration or prompt engineering or context engineering, whatever you want to call it. This is a powerful prompt orchestration technique you can use to reuse prompts and pass in prompts as a lower level. We've covered this on the channel.

### Grading System

But you can see here we have a simple grading system. S through F where S is the best and F is the worst. We have a classic prompt format. We can collapse everything to quickly understand it. Use the nano agent MCP server, execute and then report the results in the response format. And so you can see the response format is a simple grading scheme.

We are using Claude code Opus 4.1 as an LLM as a judge to manage all this for us. And then inside the evaluation details, we're just passing in the lops, the lower order prompts - the prompts that contain the detail that we want to swap in and out as we evaluate different agentic behavior.

### Real-Time Results Processing

If we open up the terminal again, we can see how we're doing here. Looks like we are waiting on GPT OSS 20 billion and everyone else has completed. Not a ton of surprises there. On device does take some time to run. There we go. We just got that completed and now Claude code is going to formulate these results into a concrete response for us. It's going to do the evaluation.

So you can see those tokens streaming in there. Hopefully I still have enough Opus for a great evaluation here. Let's see how that goes. But so we have a higher order prompt here and then here's our eval one that we ran. This is our dummy test.

## On-Device Model Performance

So you can see the structure here. We're firing off Claude code sub agents and we're having our sub agents then fire off our nano agent server. So if we open up GPT5 nano, so this is a Claude code sub agent and all it does is it takes whatever prompt was passed in. It has access to a single tool - our MCP nano prompt nano agent tool - and then we just pass in whatever our parent gives us, whatever the primary agent gives us. So simple enough.

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

# 구성
---

