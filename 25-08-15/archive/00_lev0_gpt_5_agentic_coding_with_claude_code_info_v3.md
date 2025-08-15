# 속성
process_status: true

# 추출
---
## 핵심 내용
이 내용은 GPT-5, Claude Opus 4.1, 온디바이스 모델 등 최신 AI 모델들을 실제 에이전트 코딩 작업에서 성능, 속도, 비용 측면으로 공정하게 비교 평가하는 프레임워크를 다룹니다. 단순한 벤치마크가 아닌 실제 도구 사용과 다단계 작업 수행 능력을 통해 모델의 진정한 에이전트 역량을 측정하며, 상황에 따라 적절한 모델을 선택하는 것이 중요하다는 점을 강조합니다. 특히 M4 Max MacBook에서 직접 실행되는 온디바이스 모델들의 가능성과 함께 비용 효율적인 모델 선택의 중요성을 제시합니다.

## 상세 핵심 내용
이 문서는 AI 모델 평가의 패러다임 전환을 보여줍니다. 기존 벤치마크 점수 나열에서 벗어나 실제 에이전트 작업 수행 능력을 측정하는 혁신적 접근법을 제시합니다.

**공정한 평가 프레임워크**
모든 모델이 동일한 nano agent MCP 서버를 통해 작업을 수행하여 진정한 공정성을 확보합니다. GPT-5, Claude Opus 4.1, Sonnet, Haiku, 그리고 M4 Max MacBook에서 직접 실행되는 20억/1200억 파라미터 온디바이스 모델들이 같은 조건에서 경쟁합니다.

**에이전트 중심 평가**
단순한 질문-응답이 아닌 도구 연계 사용 능력을 측정합니다. "README 파일에서 첫 10줄과 마지막 10줄 추출" 같은 실제 개발 작업을 통해 모델의 에이전트 역량을 평가하며, 파일 읽기, 형식 준수, 정확한 출력 생성까지 종합적으로 검증합니다.

**3차원 성능 지표**
성능(작업 완수 여부), 속도(응답 시간), 비용(토큰 사용량)을 종합 평가합니다. 놀랍게도 Claude Haiku가 다른 고성능 모델들을 제치고 상위권에 랭크되었으며, 이는 비용 효율성이 반영된 결과입니다.

**온디바이스 모델의 돌파구**
128GB 통합 메모리를 가진 M4 Max에서 실행되는 대형 모델들이 실용적 성능을 보여주며, 클라우드 의존성 없이 로컬에서 에이전트 작업을 수행할 수 있는 새로운 가능성을 제시합니다.

**실용적 선택 지침**
상황별 최적 모델 선택의 중요성을 강조합니다. 고비용 Opus는 복잡한 작업에, 경제적인 GPT-5나 mini는 일반 작업에, 온디바이스 모델은 프라이버시가 중요한 작업에 사용하는 전략적 접근이 핵심입니다.

## 주요 화제
- AI 모델 에이전트 아키텍처: 단일 프롬프트 호출이 아닌 다중 도구 체인 연결을 통한 실제 엔지니어링 결과 달성 방법에 대한 설명
- 다중 모델 성능 평가 시스템: GPT-5, Opus 4.1, Sonnet, Haiku 등 여러 AI 모델을 동일한 조건에서 성능, 속도, 비용 측면으로 비교 평가하는 프레임워크
- 온디바이스 로컬 LLM 성능: M4 Max MacBook Pro에서 20억/1200억 파라미터 GPT 오픈소스 모델을 직접 실행하여 에이전트 디코딩 작업 수행 가능성 검증
- Nano Agent MCP 서버 구현: 공정한 평가를 위해 모든 모델이 동일한 컨텍스트와 도구에 접근할 수 있는 마이크로 에이전트 서버 아키텍처
- 프롬프트 오케스트레이션 기법: 상위 차수 프롬프트(HOP)와 하위 차수 프롬프트(LOP)를 활용한 재사용 가능한 프롬프트 엔지니어링 방법론
- Claude Code를 활용한 LLM 판사 패턴: Opus 4.1을 판사 모델로 사용하여 다른 모델들의 성능을 S~F 등급으로 평가하는 시스템
- 에이전트 코딩의 핵심 트레이드오프: 성능, 속도, 비용이라는 세 가지 차원에서 작업에 따른 최적 모델 선택 전략
- 컨텍스트-모델-프롬프트 삼원 구조: AI 에이전트, 벤치마크, 평가 시스템 구축의 기반이 되는 세 가지 핵심 개념

## 부차 화제
- 벤치마크 리뷰의 한계: 기존 기술 유튜버들이 단순히 모델 벤치마크를 재탕하는 것을 비판하며 실제 사용을 통한 심층 분석의 필요성을 강조
- 프롬프트 오케스트레이션 기법: Higher Order Prompt(HOP)와 Lower Order Prompt(LOP)를 활용한 프롬프트 재사용 및 계층적 구성 방법론
- 등급 평가 시스템: S부터 F까지의 단순한 등급 체계로 모델 성능을 평가하는 구체적인 방법
- 로컬 모델의 하드웨어 요구사항: M4 Max MacBook Pro의 128GB 통합 메모리에서 20억/1200억 파라미터 모델을 온디바이스로 실행하는 기술적 환경
- Claude Code의 서브 에이전트 구조: 메인 에이전트가 여러 서브 에이전트를 생성하고 각각이 나노 에이전트 MCP 서버를 호출하는 계층적 아키텍처
- 파일 조작 테스트 사례: README 파일의 첫 10줄과 마지막 10줄을 읽어오는 구체적인 에이전트 작업 예시
- 토큰 사용량과 비용 분석: GPT-5와 Opus 4.1의 실제 토큰 소비량 비교를 통한 비용 효율성 평가
- 컨텍스트-모델-프롬프트 삼요소: 모든 AI 시스템 구축의 기반이 되는 세 가지 핵심 개념
- 성능-속도-비용 트레이드오프: 작업 상황에 따라 적절한 모델을 선택하기 위한 의사결정 프레임워크
- 나노 에이전트 코드베이스 구조: 재사용 가능한 에이전트 평가 시스템의 디렉토리 구성과 명령어 체계

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
