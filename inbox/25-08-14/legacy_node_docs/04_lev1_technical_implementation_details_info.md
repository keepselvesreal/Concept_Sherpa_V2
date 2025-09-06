# 속성
process_status: true

# 추출

## 핵심 내용
이 시스템은 Higher Order Prompts(HOPs)와 Lower Order Prompts(LOPs)를 활용한 강력한 프롬프트 오케스트레이션 기술을 구현하여 프롬프트 재사용과 계층적 관리를 가능하게 합니다. Claude Code Opus 4.1을 LLM 판사로 사용하여 S-F 등급제 평가 시스템을 통해 다양한 에이전트 행동을 체계적으로 평가하며, nano agent MCP 서버를 통해 실행 결과를 구조화된 응답 형식으로 보고합니다. 전체 아키텍처는 commands, agents, app docs 등의 모듈화된 디렉토리 구조로 구성되어 있어 확장 가능하고 체계적인 AI 시스템 관리를 제공합니다.

# 내용
## Technical Implementation Details

Let's open up this codebase and understand the setup. As usual, we have our primary agentic directories. We have our plans. We have our application specific nano agent here. We have our app docs, AI docs, and most importantly, our commands and our agents.

So, if we open up commands, you can see we have this directory perf. So inside of Perf you can see we have a hop - a higher order prompt - and we have lops - lower order prompts.

So this is a powerful prompt orchestration or prompt engineering or context engineering, whatever you want to call it. This is a powerful prompt orchestration technique you can use to reuse prompts and pass in prompts as a lower level. We've covered this on the channel.

But you can see here we have a simple grading system. S through F where S is the best and F is the worst. We have a classic prompt format. We can collapse everything to quickly understand it. Use the nano agent MCP server, execute and then report the results in the response format. And so you can see the response format is a simple grading scheme.

We are using Claude code Opus 4.1 as an LLM as a judge to manage all this for us. And then inside the evaluation details, we're just passing in the lops, the lower order prompts - the prompts that contain the detail that we want to swap in and out as we evaluate different agentic behavior.

If we open up the terminal again, we can see how we're doing here. Looks like we are waiting on GPT OSS 20 billion and everyone else has completed. Not a ton of surprises there. On device does take some time to run. There we go. We just got that completed and now Claude code is going to formulate these results into a concrete response for us. It's going to do the evaluation.

So you can see those tokens streaming in there. Hopefully I still have enough Opus for a great evaluation here. Let's see how that goes. But so we have a higher order prompt here and then here's our eval one that we ran. This is our dummy test.

# 구성
