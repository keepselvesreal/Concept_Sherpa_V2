# 속성
process_status: true

# 추출

## 핵심 내용
On-Device Model Performance는 M4 Max MacBook Pro에서 20억과 1200억 파라미터 모델을 로컬로 실행하여 에이전트 디코딩 작업을 수행하는 시스템입니다. 이 시스템은 Claude Code 서브 에이전트들이 nano 에이전트 서버를 통해 다양한 모델(GPT5 nano, mini 등)에 프롬프트를 전달하고, 지시 사항 준수와 도구 사용 능력을 테스트하는 벤치마크를 실행합니다. 128GB 통합 메모리를 활용하여 온디바이스에서 직접 AI 모델들을 구동하면서 복잡한 에이전트 간 통신과 작업 오케스트레이션을 수행하는 것이 핵심입니다.

## 상세 핵심 내용
### 아키텍처 개요

On-Device Model Performance는 다층 에이전트 시스템을 통해 로컬 디바이스에서 실행되는 AI 모델들의 성능을 평가하는 시스템입니다. 이 시스템은 Claude Code 서브 에이전트들이 nano 에이전트 서버를 호출하는 계층적 구조로 설계되어 있습니다.

### 시스템 구조 및 데이터 플로우

**Primary Agent → Sub Agents → Nano Agent Server**
- Primary 에이전트가 Claude Code 서브 에이전트들을 실행
- 각 서브 에이전트는 MCP nano prompt nano agent tool에만 접근 가능
- 상위 에이전트에서 전달받은 프롬프트를 그대로 하위 시스템에 전달

### 지원 모델 확장성

현재 시스템은 다양한 모델을 지원하며 쉽게 확장 가능합니다:
- **GPT 시리즈**: GPT5 nano, GPT5 mini, GPT5
- **OpenAI 로컬 모델**: 20억 파라미터, 1200억 파라미터
- **하드웨어 환경**: M4 Max MacBook Pro (128GB 통합 메모리)

### 벤치마크 테스트 구조

**기본 테스트 (Dummy Test)**
- 프롬프트: "미국의 수도는 무엇인가, JSON 형식으로 응답"
- 목적: 기본적인 응답 능력과 형식 준수 확인
- 메타데이터 수집을 통한 성능 분석

**고급 테스트 (Agentic Task)**
- 프롬프트: "README 파일을 읽고 정확히 첫 10줄과 마지막 10줄 제공"
- 평가 요소:
  - **명령어 준수**: 정확한 지시사항 이행
  - **도구 사용**: 파일 읽기 도구 활용
  - **형식 준수**: 지정된 응답 형식 유지

### 실행 결과 및 분석

**에이전트 실행 현황**
- 9개의 nano 에이전트 동시 실행
- 각 에이전트별 개별 응답 수집
- Raw 출력 데이터 전체 기록

**성능 평가 지표**
- 응답 정확성
- 형식 준수도
- 도구 사용 효율성
- 에이전트 간 통신 품질

### 프롬프트 엔지니어링 원칙

**명확성 우선**
- Primary 에이전트와 서브 에이전트 모두에게 명확한 지시사항 제공
- 에이전트 간 통신 플로우의 정밀한 오케스트레이션

**구조화된 접근**
- Instructions와 Variables로 구분된 프롬프트 구조
- 예상 출력 형식의 명시적 정의
- 단계적 난이도 증가를 통한 체계적 평가

### 기술적 혁신 요소

**온디바이스 AI 실행**
- 클라우드 의존성 없는 완전한 로컬 실행
- 128GB 통합 메모리를 활용한 대형 모델 구동
- 실시간 에이전트 디코딩 작업 수행

**확장 가능한 아키텍처**
- 모델별 독립적인 서브 에이전트 구조
- 새로운 모델 추가의 용이성
- 표준화된 MCP 도구 인터페이스

이 시스템은 온디바이스 AI 모델의 실질적 성능을 다각도로 평가하며, 특히 복잡한 에이전트 작업에서의 실행 능력을 중점적으로 검증합니다.

## 주요 화제
- 다중 에이전트 아키텍처(Multi-Agent Architecture): Claude Code 서브 에이전트들이 nano agent server를 호출하는 계층적 구조로, 상위 에이전트가 하위 에이전트들을 조율하는 시스템

- 온디바이스 모델 실행(On-Device Model Execution): M4 Max MacBook Pro(128GB 통합 메모리)에서 20억, 1200억 파라미터 모델들이 직접 실행되어 에이전트 디코딩 작업을 수행하는 능력

- 모델 스위칭 시스템(Model Switching System): GPT5 nano, mini, five 등 다양한 모델들을 쉽게 교체할 수 있는 구조와 OpenAI 로컬 모델들의 통합

- MCP 도구 통합(MCP Tool Integration): 각 서브 에이전트가 단일 MCP nano prompt nano agent 도구에 접근하여 부모 에이전트로부터 받은 프롬프트를 처리하는 방식

- 벤치마킹 및 테스트 프레임워크(Benchmarking and Testing Framework): JSON 형식 응답 요구, 파일 읽기 작업 등 다양한 난이도의 에이전트 작업 테스트 시스템

- 명령 수행 및 도구 사용 테스트(Instruction Following and Tool Use Testing): README 파일의 첫 10줄과 마지막 10줄 추출과 같은 구체적인 형식 요구사항을 통한 에이전트 성능 평가

- 에이전트 간 커뮤니케이션 오케스트레이션(Agent Communication Orchestration): 기본 에이전트와 서브 에이전트 간의 명확한 소통 흐름 관리 및 조율 시스템

## 부차 화제
제공된 텍스트를 분석하여 "On-Device Model Performance"에서 다루는 부차적인 화제들을 추출하겠습니다.

- Claude Code Sub-Agent 아키텍처: Claude code sub agents를 통해 nano agent server를 실행하는 계층적 구조와 각 서브 에이전트가 단일 MCP nano prompt nano agent tool에 접근하는 방식
- 다중 모델 지원 시스템: GPT5 nano, GPT5 mini, GPT5와 같은 다양한 모델들을 쉽게 교체하고 확장할 수 있는 구조 설계
- M4 Max MacBook Pro 하드웨어 성능: 128GB 통합 메모리를 탑재한 MacBook Pro에서 20억 및 1200억 파라미터 모델을 온디바이스로 실행하는 성능
- OpenAI Local Models 실행: 로컬 환경에서 OpenAI 모델들을 직접 실행하는 기술과 그 성능적 우수성
- Agent Decoding Work: 온디바이스 모델들이 수행하는 에이전트 디코딩 작업의 실제 구현과 결과
- Benchmark Testing 방법론: "미국의 수도는 무엇인가"와 같은 더미 테스트부터 JSON 형식 응답 요구까지의 벤치마크 설계
- MCP Server 메타데이터 수집: nano agent MCP server를 통한 보조 메타데이터 추출 및 분석 방법
- 다중 에이전트 실행 결과 분석: 9개의 nano agents 동시 실행과 각각의 응답 결과 수집 및 비교
- 파일 읽기 도구 사용 테스트: README 파일의 처음 10줄과 마지막 10줄을 정확히 추출하는 agentic task 수행
- Instruction Following 평가: 정확한 응답 형식 준수와 지시사항 따르기 능력 측정
- Tool Use 능력 테스트: nano agent MCP server가 호출할 수 있는 도구들의 활용 능력 평가
- Agent Communication Orchestration: 주 에이전트와 서브 에이전트 간의 명확한 커뮤니케이션 흐름 관리 및 최적화
- Prompt Pattern 최적화: 주 에이전트와 서브 에이전트 모두에게 명확하고 효과적인 프롬프트 작성 방법론

# 내용

## On-Device Model Performance

So you can see the structure here. We're firing off Claude code sub agents and we're having our sub agents then fire off our nano agent server. So if we open up GPT5 nano, so this is a Claude code sub agent and all it does is it takes whatever prompt was passed in. It has access to a single tool - our MCP nano prompt nano agent tool - and then we just pass in whatever our parent gives us, whatever the primary agent gives us. So simple enough.

You can imagine that we can just continue doing this along every other model we want to run. So you can see here, here's GPT5 mini. But we can easily just swap this out. You can see here there's nano, here's mini, here's five. And then we repeat the same thing for the correct OpenAI local models, which are absolutely mind-blowing.

We have 20 billion and 120 billion running right on my M4 Max MacBook Pro. This is a 128 GB unified memory machine. This thing is absolutely cracked. These models run on the device and they are doing agent decoding work as you'll see in these results.

Let's go ahead and hop back to the results. Pretty excited to share this with you here. But you can see how these prompts are set up - these are our agents and our lower order prompts just detail the exact benchmark that we want run. So on our dummy test the prompt is "what's the capital of the United States, respond in JSON format structure" so we can get all the auxiliary metadata coming out of the nano agent MCP server.

We have another interesting result here. We have the raw outputs. Here's all of our agents that executed - we had nine nano agents firing off. And then we have the respective responses. You can see here we're looking for first 10 lines and last 10 lines in the specific prompt format.

We can take a look at the result. Let me just quickly show you exactly what that prompt looked like. So this is a lower order prompt basic read. So if we look at this, we have instructions and then we have variables. And the prompt here is the most important. So we're saying read the readme file. Provide exactly the first 10 lines and the last 10 lines of the file.

So this is an agentic task. This is a little more advanced. We're just stepping up the difficulty scale just a little bit from just asking a simple question. We just want it in this exact response format. So we're testing for instruction following. We're testing for tool use. In a second here, I'll show you the exact tools that our nano agent MCP server can call.

Then we fire off all of our agents and we have an expected output. So, we're just sticking to great prompt patterns. We're writing extraordinarily clearly to our agent, both our primary agent and our sub agents, and we're being really clear about the flow of communication between our agents. We need to make sure that we're orchestrating the communication extraordinarily well.

# 구성
