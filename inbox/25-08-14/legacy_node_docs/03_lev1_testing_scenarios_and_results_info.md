# 속성
process_status: true

# 추출

## 핵심 내용
고차 프롬프트(higher order prompt)와 저차 프롬프트(lower order prompt)를 활용한 다중 모델 평가 시스템을 Claude Code 내에서 구현하여, 여러 AI 모델들의 에이전트 행동을 공정한 환경에서 비교 분석했습니다. 이 시스템은 nano agent MCP 서버를 통해 각 모델이 동일한 도구와 조건에서 작업을 수행하도록 하여, 성능, 속도, 비용 등의 트레이드오프를 객관적으로 평가할 수 있는 벤치마크 환경을 제공합니다. 특히 GPT-5, Opus 4.1, 그리고 새로운 오픈소스 GPT 모델들과 같은 최신 모델들을 로컬 환경에서 실시간으로 테스트하고 비교할 수 있는 프레임워크를 구축했습니다.

## 상세 핵심 내용
### 멀티모델 평가 시스템 구조

이 테스트 시나리오는 **Higher Order Prompt (HOP)** 기반의 계층적 평가 시스템을 구축합니다. 시스템의 핵심은 상위 프롬프트가 하위 프롬프트를 제어하여 여러 AI 모델을 동시에 평가하는 구조입니다.

```
Higher Order Prompt → Lower Order Prompt → Multiple AI Models → Nano Agent MCP Server
```

### Nano Agent MCP 서버의 역할

**공정한 평가 환경 제공**이 핵심 목표입니다:
- **Micro Gemini CLI**: Gemini 모델 전용 경량화 인터페이스
- **Micro Codec**: 코드 처리 및 변환 도구
- **Micro Claude Code**: Claude 모델 전용 실행 환경

이 서버는 모든 모델이 동일한 도구와 환경에서 작업할 수 있도록 **균등한 조건**을 보장합니다.

### 실시간 평가 워크플로우

1. **프롬프트 계층 실행**: HOP가 기본 읽기 테스트 프롬프트를 각 모델에 전달
2. **병렬 모델 실행**: 여러 AI 모델이 동시에 동일한 작업 수행
3. **결과 수집 및 보고**: 각 모델의 응답이 Primary Agent로 집계
4. **통합 분석**: Primary Agent가 최종 비교 분석 결과 제공

### 평가 대상 모델 범위

**차세대 최신 모델들**:
- **GPT-5**: OpenAI의 차세대 모델
- **Opus 4.1**: Anthropic의 새로운 버전
- **GPT 오픈소스 모델들**: 로컬 실행 가능한 OpenAI 오픈소스 버전

### 핵심 평가 지표

**성능 (Performance)**: 작업 완료 품질 및 정확성
**속도 (Speed)**: 응답 시간 및 처리 효율성  
**비용 (Cost)**: 리소스 사용량 및 경제적 효율성

### 기술적 구현 특징

**Claude Code 통합**: 전체 평가 시스템이 Claude Code 환경에서 실행
**로컬 실행**: 오픈소스 모델들이 사용자 머신에서 직접 실행
**실시간 모니터링**: 각 모델의 실행 상태와 결과를 실시간으로 추적

이 시스템은 **에이전트 행동 평가**를 위한 표준화된 벤치마킹 환경을 제공하여, 새로운 모델들의 실질적인 성능 비교를 가능하게 합니다.

## 부차 화제
- 다중 모델 평가 시스템(Multi-model evaluation system): Claude Code 내에서 여러 모델을 동시에 평가하는 시스템 구축 및 운영

- 계층적 프롬프트 구조(Higher/Lower order prompts): 상위 프롬프트와 하위 프롬프트를 조합한 계층적 프롬프트 설계 방법론

- Nano Agent MCP 서버(Nano Agent MCP server): 공정한 평가 환경을 위한 마이크로 서비스 형태의 평가 서버 개발

- 공정한 평가 환경 구축(Fair playing field): 다양한 AI 모델들을 동일한 조건에서 비교 평가할 수 있는 환경 설계

- 에이전트 행동 평가(Agentic behavior evaluation): AI 에이전트의 자율적 행동 패턴과 성능을 측정하고 분석하는 방법론

- 모델 성능 지표 분석(Performance metrics analysis): 성능, 속도, 비용 등 다차원적 평가 지표를 통한 모델 비교 분석

- 마이크로 CLI 도구(Micro CLI tools): Gemini CLI, Codec, Claude Code 등을 모방한 소규모 명령줄 인터페이스 도구 개발

- 최신 모델 벤치마킹(State-of-the-art model benchmarking): GPT-5, Opus 4.1 등 차세대 모델들의 성능 벤치마킹 방법론

- 오픈소스 모델 평가(Open-source model evaluation): OpenAI의 새로운 오픈소스 모델들에 대한 로컬 환경 평가

- 실시간 결과 수집(Real-time results collection): 에이전트들이 작업을 수행하고 결과를 실시간으로 수집하는 워크플로우

# 내용
## Testing Scenarios and Results

And of course, we're going to scale this up. Let's go ahead and throw a harder, more agentic problem at these models. I'll run that hop. Hop is higher order prompt. We'll break that down in just a second. And then we have this prompt that we're passing into this prompt. Basic read test. Let's fire this off.

We're running a multi-model evaluation system inside of Claude Code. So, we prompt a higher order prompt. We pass in a lower order prompt. We then have our primary agent kick off a slew of respective models running against the nano agent MCP server with a few very specific tools.

You can think of this server as like a micro Gemini CLI, a micro codec, a micro Claude code server that our agents can run against in a fair playing field. You can see our agents are starting to respond here and then they return the results and of course they report back to the primary agent and then our primary agent reports back to us.

So this is the multi-model evaluation workflow. Higher order prompt, lower order prompt. We have models that call our nano agent MCP server and the whole point here is to create a true even playing field. You and I need to evaluate agentic behavior against these models and understand the tradeoffs they all have: performance, speed, cost. All of these mattered.

You can see our results coming in here. Let's go ahead and dive in to this codebase, the nano agent codebase, and understand exactly how this is formatted so that we can benchmark brand new fresh state-of-the-art models like GPT5 against the new Opus 4.1. And ultra excitingly, these brand new GPT open-source models, OpenAI absolutely cooked on these models. Again, these are running right on my machine right now.

# 구성
