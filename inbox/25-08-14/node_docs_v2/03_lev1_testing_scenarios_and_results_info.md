# 속성
process_status: true

# 추출

## 핵심 내용
GPT-5 Agentic Coding with Claude Code는 GPT-5, Opus 4.1, Sonnet, Haiku 등 최신 AI 모델들과 M4 Max MacBook Pro에서 직접 실행되는 20B, 120B 파라미터 온디바이스 모델들의 에이전트 성능을 공정하게 비교 평가하는 프레임워크입니다. 단순한 프롬프트 호출이 아닌 여러 도구를 연결하여 실제 엔지니어링 작업을 수행하는 에이전트 아키텍처를 통해, 고차원 프롬프트(HOP)와 저차원 프롬프트를 사용한 다중 모델 평가 시스템을 구현하여 성능, 속도, 비용의 3가지 핵심 지표로 모델들을 벤치마킹합니다.

## 상세 핵심 내용
### 에이전트 기반 모델 평가 프레임워크

**평가 철학:**
- **단순 프롬프트 vs 에이전트**: 단순한 프롬프트 호출을 넘어선 실제 엔지니어링 작업 수행 능력 평가
- **도구 연결 능력**: 여러 도구를 연결하여 복잡한 작업을 완수하는 에이전트 아키텍처 중시
- **실무 중심 벤치마킹**: 실제 개발 환경에서의 실용성과 효율성 측정

### 멀티모델 평가 시스템 아키텍처

**시스템 구성 요소:**
- **Higher Order Prompt (HOP)**: 상위 레벨 프롬프트 시스템으로 복잡한 작업 분해
- **Lower Order Prompt**: 하위 레벨 프롬프트 (예: Basic read test)
- **Primary Agent**: 전체 평가 과정을 조율하고 최종 결과를 통합하는 메인 에이전트
- **Nano Agent MCP Server**: 공정한 테스트 환경을 제공하는 마이크로 서버 집합

### 공정한 평가 환경 구축

**Nano Agent MCP Server 특징:**
- **마이크로 서비스 집합**: Gemini CLI, Codec, Claude Code의 축소 버전들
- **동일한 도구 세트**: 모든 모델이 identical한 도구와 제약 조건 하에서 테스트
- **공정한 경쟁 환경**: 모델별 고유 도구가 아닌 표준화된 도구 세트 사용
- **통제된 테스트 환경**: 외부 변수를 최소화한 일관된 평가 조건

### 3대 핵심 성능 지표

**Performance (성능):**
- 작업 완료도와 정확성
- 복잡한 엔지니어링 문제 해결 능력
- 도구 연결 및 활용 효율성

**Speed (속도):**
- 응답 속도와 처리 시간
- 에이전트 워크플로우 실행 속도
- 실시간 작업 수행 능력

**Cost (비용):**
- 토큰 사용량과 비용 효율성
- 온디바이스 모델의 무료 실행 vs 클라우드 모델 비용
- ROI 기반 모델 선택 기준

### 혁신적 온디바이스 모델 평가

**M4 Max MacBook Pro 온디바이스 실행:**
- **20B 파라미터 모델**: 로컬에서 직접 실행되는 소형 모델
- **120B 파라미터 모델**: 대형 모델의 온디바이스 실행 가능성 검증
- **혁신적 성능**: 기존 클라우드 모델들과 경쟁 가능한 수준의 에이전트 능력
- **비용 혁명**: 무료 로컬 실행을 통한 비용 구조 변화

### 평가 워크플로우 프로세스

**단계별 실행 구조:**
1. **프롬프트 계층화**: Higher order prompt에서 구체적 작업으로 분해
2. **에이전트 활성화**: Primary agent가 다수 모델에게 동일한 작업 분배
3. **통합 테스트 환경**: 모든 모델이 nano agent MCP server 도구 세트 사용
4. **실시간 모니터링**: 로컬 머신에서 각 모델의 실행 과정 관찰
5. **결과 수집 및 분석**: 3대 지표 기반 성능 비교 및 트레이드오프 분석
6. **최종 보고**: Primary agent가 통합 벤치마킹 결과 제시

### 모델 선택 전략 및 미래 전망

**벤치마킹 대상 모델들:**
- **GPT-5**: 차세대 OpenAI 모델의 에이전트 능력
- **Opus 4.1**: Anthropic의 최신 모델 성능
- **Sonnet & Haiku**: 다양한 크기별 모델 비교
- **OpenAI 오픈소스 모델들**: 새로운 오픈소스 에이전트 모델들
- **온디바이스 20B/120B**: 로컬 실행 모델의 혁신적 가능성

**향후 에이전트 코딩 전략:**
- 작업 특성에 따른 최적 모델 선택 가이드라인
- 비용 효율성을 고려한 온디바이스 vs 클라우드 모델 선택
- 성능-속도-비용 트레이드오프 기반 의사결정 프레임워크
- 실제 개발 워크플로우에서의 모델 활용 최적화 전략

## 주요 화제
다음은 "03_lev1_testing_scenarios_and_results"에서 다루는 주요 화제들입니다:

- Multi-model evaluation system: Claude Code 내에서 여러 AI 모델들을 동시에 평가하는 시스템 구축 및 운영

- Higher order prompt (HOP) architecture: 상위 프롬프트가 하위 프롬프트를 관리하는 계층적 프롬프트 구조 설계

- Nano agent MCP server: 마이크로 Gemini CLI, 코덱, Claude code 서버와 같은 기능을 제공하는 경량화된 에이전트 서버 개발

- Fair testing environment: 모든 AI 모델들이 동일한 조건에서 테스트받을 수 있는 공정한 평가 환경 구성

- Agentic behavior evaluation: AI 에이전트들의 행동 패턴과 성능을 체계적으로 평가하는 방법론

- Performance metrics assessment: 성능, 속도, 비용 등 다양한 지표를 통한 모델 간 트레이드오프 분석

- State-of-the-art model benchmarking: GPT5, Opus 4.1, OpenAI의 새로운 오픈소스 모델들에 대한 벤치마킹 프로세스

- Local model execution: 최신 AI 모델들을 로컬 머신에서 직접 실행하고 테스트하는 방법

## 부차 화제
- Multi-model evaluation system: Claude Code 내에서 여러 모델을 동시에 평가하는 시스템 구축 및 운영

- Higher order prompt와 lower order prompt: 계층적 프롬프트 구조를 통한 복잡한 에이전트 작업 처리 방식

- Nano agent MCP server: 공정한 평가 환경을 위한 마이크로 서버 구축 (Gemini CLI, codec, Claude code server의 경량화 버전)

- 에이전트 성능 평가 지표: 성능(performance), 속도(speed), 비용(cost) 등 다차원적 평가 기준

- 차세대 AI 모델 벤치마킹: GPT-5, Opus 4.1, GPT 오픈소스 모델 등 최신 모델들에 대한 성능 비교 테스트

- 로컬 환경에서의 오픈소스 모델 실행: 사용자 기기에서 직접 구동되는 OpenAI 오픈소스 모델들의 활용

- 에이전트 행동 분석: 다양한 모델들의 에이전트적 행동 패턴과 트레이드오프 분석

# 내용
## Testing Scenarios and Results

And of course, we're going to scale this up. Let's go ahead and throw a harder, more agentic problem at these models. I'll run that hop. Hop is higher order prompt. We'll break that down in just a second. And then we have this prompt that we're passing into this prompt. Basic read test. Let's fire this off.

We're running a multi-model evaluation system inside of Claude Code. So, we prompt a higher order prompt. We pass in a lower order prompt. We then have our primary agent kick off a slew of respective models running against the nano agent MCP server with a few very specific tools.

You can think of this server as like a micro Gemini CLI, a micro codec, a micro Claude code server that our agents can run against in a fair playing field. You can see our agents are starting to respond here and then they return the results and of course they report back to the primary agent and then our primary agent reports back to us.

So this is the multi-model evaluation workflow. Higher order prompt, lower order prompt. We have models that call our nano agent MCP server and the whole point here is to create a true even playing field. You and I need to evaluate agentic behavior against these models and understand the tradeoffs they all have: performance, speed, cost. All of these mattered.

You can see our results coming in here. Let's go ahead and dive in to this codebase, the nano agent codebase, and understand exactly how this is formatted so that we can benchmark brand new fresh state-of-the-art models like GPT5 against the new Opus 4.1. And ultra excitingly, these brand new GPT open-source models, OpenAI absolutely cooked on these models. Again, these are running right on my machine right now.

# 구성
