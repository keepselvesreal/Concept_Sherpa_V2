# 속성
process_status: true

# 추출

## 핵심 내용
이 시스템은 다중 모델 평가 워크플로우를 통해 여러 AI 모델들의 에이전틱 행동을 공정하게 비교 테스트합니다. 상위 프롬프트와 하위 프롬프트를 사용하여 각 모델이 nano agent MCP 서버의 동일한 도구들에 접근하도록 하여, 성능, 속도, 비용 등의 트레이드오프를 균등한 조건에서 평가할 수 있습니다. 이를 통해 GPT-5, Opus 4.1, OpenAI의 새로운 오픈소스 모델들과 같은 최신 모델들을 체계적으로 벤치마킹할 수 있는 환경을 제공합니다.

## 상세 핵심 내용
### Multi-Model Evaluation System 개요

이 시스템은 Claude Code 내에서 실행되는 고도화된 다중 모델 평가 플랫폼으로, 여러 AI 모델들의 에이전틱 행동을 공정하고 체계적으로 비교 분석하는 것이 목적입니다.

### 계층적 프롬프트 구조

**Higher Order Prompt (HOP)**
- 상위 수준의 명령어로, 전체적인 테스트 시나리오를 정의
- 하위 프롬프트들을 조율하고 관리하는 역할
- 복잡하고 에이전틱한 문제 해결을 위한 프레임워크 제공

**Lower Order Prompt**
- HOP 내부로 전달되는 구체적인 작업 지시사항
- 실제 모델들이 수행해야 할 세부 태스크 정의
- "Basic read test" 등의 구체적인 평가 항목 포함

### Nano Agent MCP Server 아키텍처

**서버 특징**
- 마이크로 서비스 형태의 경량화된 에이전트 서버
- Gemini CLI, Codec, Claude Code의 축소 버전 역할
- 모든 모델이 동일한 도구와 환경에서 작업할 수 있는 공정한 경쟁 환경 제공

**도구 및 기능**
- 특정 도구들로 제한된 환경에서 모델 성능 측정
- 표준화된 인터페이스를 통한 일관된 평가 조건 보장
- 로컬 머신에서 직접 실행 가능한 구조

### 평가 워크플로우

**1단계: 초기 설정**
- Higher Order Prompt 실행
- Lower Order Prompt를 HOP 내부로 전달
- Primary Agent 활성화

**2단계: 모델 실행**
- Primary Agent가 다중 모델 평가 프로세스 시작
- 각 모델이 Nano Agent MCP Server에 대해 동시 실행
- 표준화된 도구 세트를 사용한 작업 수행

**3단계: 결과 수집 및 보고**
- 각 모델의 응답 및 결과 수집
- Primary Agent로 결과 전달
- 최종 사용자에게 종합 보고서 제공

### 평가 기준 및 지표

**성능 측정 요소**
- **Performance**: 작업 정확도 및 품질
- **Speed**: 응답 시간 및 처리 속도
- **Cost**: 리소스 사용량 및 비용 효율성
- **Agentic Behavior**: 자율적 문제 해결 능력

**벤치마킹 대상 모델**
- GPT-5 (차세대 OpenAI 모델)
- Opus 4.1 (Anthropic의 새로운 모델)
- 최신 GPT 오픈소스 모델들
- 기타 최신 상태의 AI 모델들

### 실시간 테스트 환경

**로컬 실행 환경**
- 모든 모델이 사용자의 로컬 머신에서 직접 실행
- 네트워크 지연이나 외부 요인 없는 순수한 성능 측정
- 실시간 결과 모니터링 및 분석 가능

**확장성 및 적응성**
- 새로운 모델 추가 시 기존 프레임워크 재사용 가능
- 다양한 난이도의 테스트 시나리오 적용 가능
- 공정한 비교를 위한 표준화된 평가 환경 유지

이 시스템은 AI 모델의 에이전틱 능력을 객관적이고 체계적으로 평가할 수 있는 포괄적인 플랫폼으로, 차세대 AI 모델들의 실질적인 성능 비교와 최적화를 위한 핵심 도구 역할을 합니다.

## 주요 화제
- 다중 모델 평가 시스템(Multi-Model Evaluation System): Claude Code 내에서 운영되는 시스템으로, 여러 AI 모델들의 성능을 동등한 조건에서 비교 평가하는 방법론

- 계층적 프롬프트 구조(Hierarchical Prompt Structure): 고차 프롬프트(Higher Order Prompt)와 저차 프롬프트(Lower Order Prompt)로 구성된 HOP(Higher Order Prompt) 시스템을 통한 복잡한 에이전트 문제 해결 방식

- Nano Agent MCP 서버: 공정한 평가 환경을 제공하는 마이크로 서버로, Gemini CLI, Codec, Claude Code 서버의 축소판 역할을 하며 에이전트들이 동일한 도구셋으로 작업할 수 있는 환경 제공

- 에이전트 행동 벤치마킹(Agentic Behavior Benchmarking): AI 모델들의 에이전트적 행동을 평가하고 성능, 속도, 비용 등의 트레이드오프를 분석하는 방법론

- 최신 모델 비교 평가: GPT-5, Opus 4.1, OpenAI의 새로운 오픈소스 모델들과 같은 최신 AI 모델들의 성능을 로컬 환경에서 직접 비교하는 실시험 결과

- 실시간 결과 수집 및 보고: 여러 모델이 동시에 실행되어 결과를 수집하고, 주 에이전트를 통해 통합 보고하는 실시간 평가 워크플로우

## 부차 화제
제공된 "Testing Scenarios and Results" 내용을 분석하여 부차적인 화제들을 추출하겠습니다.

- 고차 프롬프트(Higher Order Prompt) 시스템: 기본 프롬프트와 하위 프롬프트를 계층적으로 구성하여 복잡한 에이전트 문제를 처리하는 방법론
- 다중 모델 평가 시스템: Claude Code 내에서 여러 AI 모델들을 동시에 평가하고 비교하는 시스템 구조
- 나노 에이전트 MCP 서버: 공정한 평가 환경을 제공하는 마이크로 서비스 형태의 테스트 서버 (Gemini CLI, Codec, Claude Code 서버의 축소판)
- 에이전트 행동 평가 메트릭스: 성능(performance), 속도(speed), 비용(cost) 등 AI 모델의 다차원적 평가 기준
- 최신 AI 모델 벤치마킹: GPT-5, Opus 4.1, OpenAI 오픈소스 모델 등 차세대 모델들의 성능 비교 테스트
- 공정한 평가 환경 구축: 모든 모델이 동일한 조건에서 테스트받을 수 있는 표준화된 테스트 플랫폼
- 로컬 모델 실행 환경: 사용자 머신에서 직접 실행되는 AI 모델들의 성능 테스트 시나리오
- 에이전트 워크플로우 구조: 1차 에이전트가 복수의 모델들을 조율하고 결과를 취합하는 계층적 처리 구조

# 내용

## Testing Scenarios and Results

And of course, we're going to scale this up. Let's go ahead and throw a harder, more agentic problem at these models. I'll run that hop. Hop is higher order prompt. We'll break that down in just a second. And then we have this prompt that we're passing into this prompt. Basic read test. Let's fire this off.

We're running a multi-model evaluation system inside of Claude Code. So, we prompt a higher order prompt. We pass in a lower order prompt. We then have our primary agent kick off a slew of respective models running against the nano agent MCP server with a few very specific tools.

You can think of this server as like a micro Gemini CLI, a micro codec, a micro Claude code server that our agents can run against in a fair playing field. You can see our agents are starting to respond here and then they return the results and of course they report back to the primary agent and then our primary agent reports back to us.

So this is the multi-model evaluation workflow. Higher order prompt, lower order prompt. We have models that call our nano agent MCP server and the whole point here is to create a true even playing field. You and I need to evaluate agentic behavior against these models and understand the tradeoffs they all have: performance, speed, cost. All of these mattered.

You can see our results coming in here. Let's go ahead and dive in to this codebase, the nano agent codebase, and understand exactly how this is formatted so that we can benchmark brand new fresh state-of-the-art models like GPT5 against the new Opus 4.1. And ultra excitingly, these brand new GPT open-source models, OpenAI absolutely cooked on these models. Again, these are running right on my machine right now.

# 구성
