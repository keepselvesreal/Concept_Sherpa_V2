# 속성
process_status: true

# 추출

## 핵심 내용
Model Evaluation Framework는 AI 모델의 성능을 단일 프롬프트 호출이 아닌 **에이전트 아키텍처** 관점에서 평가하는 체계로, 모델이 여러 도구를 연결하여 실제 엔지니어링 결과를 달성하는 능력에 중점을 둡니다. 이 프레임워크는 MCP 서버를 통해 동일한 컨텍스트와 프롬프트로 모든 모델을 공정하게 비교하며, 성능, 속도, 비용을 종합적으로 고려하여 평가합니다. 흥미롭게도 단순한 작업에서는 Claude 3 Haiku가 더 높은 성능의 모델들을 능가하는 결과를 보여주어, 모델 성능이 컨텍스트와 작업 복잡성에 따라 크게 달라질 수 있음을 시사합니다.

# 내용
## Model Evaluation Framework

There is one trend that matters above all. Right now, it doesn't matter if we're talking about GPT5, whatever Anthropic has cooking next, the cursor CLI or any other model that's getting put out right now, open source, closed source, there is one thing everyone is focused on. If you've been paying any attention, you know exactly what it is. It is the agent architecture.

Why does everyone care so much about agents? First, let's understand how you and I, engineers with our boots on the ground, can have a better, deeper understanding of these models' agentic performance. It's not about a single prompt call anymore. It's about how well your agent chains together multiple tools to accomplish real engineering results on your behalf.

What just happened with this prompt? You can see here we have rankings. Surprisingly, we have Claude 3 Haiku outperforming all of our other models. If you look at this, it looks backward. We would expect these models to be on top and these other models to be on the bottom. What's going on?

We're evaluating all of our models against each other in a fair playing field where we care about performance, speed, and cost as a collective. These agents are operating in a nano agent, a new MCP server to create a fair playing field where every one of these models is scaffolded with the same context and prompt. Two of the big three. And then we get to see how they truly perform.

If we put these models inside Claude Code, I can guarantee you Opus and Sonnet will outperform. But you can see here for this extremely simple task, "what's the capital?" we can see very different results out of the box.

# 구성
