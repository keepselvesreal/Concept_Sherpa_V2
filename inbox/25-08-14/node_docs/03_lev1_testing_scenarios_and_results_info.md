# 속성
process_status: true

# 추출

## 핵심 내용
이 섹션은 다중 모델 평가 시스템을 통해 여러 AI 모델의 에이전트 성능을 공정하게 비교하는 과정을 설명합니다. 상위 계층 프롬프트가 하위 프롬프트를 전달하고, 각 모델이 nano agent MCP 서버의 동일한 도구를 사용하여 작업을 수행한 후 결과를 보고하는 구조로 되어 있습니다. 이를 통해 GPT-5, Opus 4.1, 그리고 새로운 오픈소스 GPT 모델들의 성능, 속도, 비용을 객관적으로 평가할 수 있는 벤치마크 환경을 구축했습니다.

## 상세 핵심 내용
### 멀티모델 평가 시스템의 구조

이 텍스트는 Claude Code 환경에서 구축된 **멀티모델 평가 시스템**에 대한 설명입니다. 시스템은 계층적 프롬프트 구조와 공정한 테스트 환경을 통해 다양한 AI 모델들의 성능을 비교 평가합니다.

### 핵심 구성 요소

**프롬프트 계층 구조**
- HOP (Higher Order Prompt): 상위 레벨 제어 프롬프트
- Lower Order Prompt: 하위 레벨 실행 프롬프트  
- Basic Read Test: 기본 읽기 테스트 시나리오

**Nano Agent MCP Server**
- 마이크로 Gemini CLI, 마이크로 codec, 마이크로 Claude Code 서버 역할
- 모든 AI 모델들이 동일한 조건에서 테스트할 수 있는 공정한 환경 제공
- 특정 도구 세트를 통한 표준화된 인터페이스 제공

### 평가 워크플로우

**실행 프로세스**
1. Primary Agent → Higher Order Prompt 실행
2. 다수의 모델들이 Nano Agent MCP Server를 통해 병렬 실행
3. 각 모델의 결과를 Primary Agent로 수집
4. Primary Agent가 최종 결과를 사용자에게 보고

**측정 지표**
- Performance: 작업 수행 품질
- Speed: 응답 속도  
- Cost: 비용 효율성

### 테스트 환경의 특징

**공정성 확보**
- 모든 모델이 동일한 MCP 서버와 도구 세트 사용
- 표준화된 테스트 시나리오 적용
- 동일한 컴퓨팅 환경에서 실행

**확장성**
- 새로운 최신 모델(GPT-5, Opus 4.1 등) 즉시 벤치마크 가능
- OpenAI의 새로운 오픈소스 모델들도 로컬 환경에서 직접 테스트

### 시스템의 목적

이 멀티모델 평가 시스템은 **에이전틱 행동(agentic behavior)**에 대한 객관적 비교 분석을 통해, 각 AI 모델의 강점과 약점, 그리고 성능-속도-비용 간의 트레이드오프를 정확히 파악할 수 있게 설계되었습니다.

## 주요 화제
- **멀티모델 평가 시스템(Multi-model Evaluation System)**: Claude Code 내부에서 실행되는 다양한 AI 모델들의 성능을 비교 평가하는 시스템

- **계층적 프롬프트 구조(Hierarchical Prompt Structure)**: 상위 프롬프트(Higher Order Prompt)와 하위 프롬프트(Lower Order Prompt)로 구성된 계층화된 프롬프트 시스템

- **나노 에이전트 MCP 서버(Nano Agent MCP Server)**: 공정한 평가 환경을 제공하는 마이크로 서버로, Gemini CLI, Codec, Claude Code 서버의 축소판 역할

- **에이전틱 행동 평가(Agentic Behavior Evaluation)**: AI 에이전트들의 자율적 행동 패턴과 성능을 분석하고 비교하는 평가 방법론

- **모델 성능 벤치마킹(Model Performance Benchmarking)**: 성능, 속도, 비용 등의 지표를 통한 AI 모델들 간의 종합적 성능 비교

- **최신 AI 모델 테스팅(State-of-the-art Model Testing)**: GPT-5, Opus 4.1, OpenAI의 새로운 오픈소스 모델 등 최첨단 AI 모델들의 성능 테스트

- **로컬 모델 실행(Local Model Execution)**: 사용자의 로컬 머신에서 직접 실행되는 AI 모델들의 운영 및 테스트 환경

## 부차 화제
- Multi-model evaluation system: Claude Code 내에서 실행되는 다중 모델 평가 시스템의 구조와 작동 방식
- Higher order prompt와 lower order prompt: 계층적 프롬프트 구조를 통한 복잡한 agentic 문제 해결 방식
- Nano agent MCP server: 마이크로 Gemini CLI, 마이크로 codec, 마이크로 Claude code server 역할을 하는 공정한 테스트 환경
- Agentic behavior 평가 지표: 성능(performance), 속도(speed), 비용(cost) 등의 트레이드오프 분석
- 차세대 AI 모델들: GPT-5, Opus 4.1, OpenAI의 새로운 오픈소스 모델들에 대한 벤치마킹 계획
- 로컬 환경에서의 모델 실행: 사용자 기기에서 직접 실행되는 최신 AI 모델들의 성능 테스트

# 내용
## Testing Scenarios and Results

And of course, we're going to scale this up. Let's go ahead and throw a harder, more agentic problem at these models. I'll run that hop. Hop is higher order prompt. We'll break that down in just a second. And then we have this prompt that we're passing into this prompt. Basic read test. Let's fire this off.

We're running a multi-model evaluation system inside of Claude Code. So, we prompt a higher order prompt. We pass in a lower order prompt. We then have our primary agent kick off a slew of respective models running against the nano agent MCP server with a few very specific tools.

You can think of this server as like a micro Gemini CLI, a micro codec, a micro Claude code server that our agents can run against in a fair playing field. You can see our agents are starting to respond here and then they return the results and of course they report back to the primary agent and then our primary agent reports back to us.

So this is the multi-model evaluation workflow. Higher order prompt, lower order prompt. We have models that call our nano agent MCP server and the whole point here is to create a true even playing field. You and I need to evaluate agentic behavior against these models and understand the tradeoffs they all have: performance, speed, cost. All of these mattered.

You can see our results coming in here. Let's go ahead and dive in to this codebase, the nano agent codebase, and understand exactly how this is formatted so that we can benchmark brand new fresh state-of-the-art models like GPT5 against the new Opus 4.1. And ultra excitingly, these brand new GPT open-source models, OpenAI absolutely cooked on these models. Again, these are running right on my machine right now.

# 구성
