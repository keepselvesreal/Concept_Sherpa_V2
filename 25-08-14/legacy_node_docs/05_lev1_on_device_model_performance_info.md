# 속성
process_status: true

# 추출

## 핵심 내용
이 시스템은 M4 Max MacBook Pro에서 20억~1,200억 파라미터의 대규모 언어 모델들을 온디바이스로 실행하면서, Claude Code 주 에이전트가 여러 하위 에이전트들을 생성하고 각각이 nano 에이전트 MCP 서버를 통해 작업을 수행하는 계층적 에이전트 아키텍처를 구현했습니다. 시스템은 단순한 질의응답부터 파일 읽기 및 도구 사용과 같은 에이전틱 작업까지 다양한 난이도의 벤치마크를 통해 모델들의 성능을 테스트하며, 명확한 프롬프트 패턴과 구조화된 JSON 응답 형식을 사용해 에이전트 간 통신을 최적화합니다.

## 상세 핵심 내용
### 아키텍처 구조

**계층적 에이전트 시스템**을 통한 온디바이스 모델 성능 테스트 프레임워크입니다. Claude Code의 주 에이전트가 하위 에이전트들을 생성하고, 이들이 다시 nano 에이전트 서버를 호출하는 구조로 설계되었습니다.

- **Primary Agent** (Claude Code) → **Sub-agents** → **Nano Agent Server**
- 각 하위 에이전트는 단일 도구(MCP nano prompt nano agent tool)에만 접근
- 상위 에이전트로부터 전달받은 프롬프트를 그대로 처리

### 지원 모델 범위

**OpenAI 모델군**:
- GPT-5 Nano
- GPT-5 Mini  
- GPT-5 (Full)

**로컬 실행 모델**:
- 20억 파라미터 모델
- 1200억 파라미터 모델
- M4 Max MacBook Pro (128GB 통합 메모리)에서 직접 실행
- 에이전트 디코딩 작업을 온디바이스에서 수행

### 벤치마크 테스트 체계

**기본 테스트 케이스**:
```json
{
  "prompt": "미국의 수도는 무엇인가요? JSON 형식으로 응답해주세요",
  "format": "structured_json",
  "metadata": "auxiliary_data_included"
}
```

**고급 에이전틱 태스크**:
```
Instructions: README 파일을 읽어주세요
Task: 파일의 첫 10줄과 마지막 10줄을 정확히 제공해주세요
Format: 지정된 응답 형식 준수
```

### 성능 평가 차원

**기능적 능력 측정**:
- **도구 사용** (Tool Use): MCP 서버 호출 및 파일 시스템 접근
- **명령 준수** (Instruction Following): 정확한 형식과 구조 요구사항 이행
- **구조화 응답** (Structured Output): JSON 및 지정 형식 생성

**에이전틱 복잡성 단계**:
1. **Level 1**: 단순 질의응답 (더미 테스트)
2. **Level 2**: 도구 활용 + 형식 준수 (파일 읽기 테스트)
3. **Level 3**: 복합 추론 + 다중 단계 실행

### 실행 및 결과 분석

**동시 실행 체계**:
- 9개 nano 에이전트 병렬 실행
- 각 에이전트별 개별 응답 수집
- 실시간 성능 메트릭 모니터링

**결과 검증 프로세스**:
- **Expected Output** 대비 실제 출력 비교
- 명령 준수도 및 정확성 평가
- 응답 시간 및 리소스 사용량 측정

### 에이전트 간 통신 최적화

**명확한 통신 패턴**:
- 주 에이전트 ↔ 하위 에이전트 간 명확한 역할 분담
- 프롬프트 전달 시 컨텍스트 손실 최소화
- 구조화된 응답 형식을 통한 일관된 데이터 흐름

**오케스트레이션 품질**:
- 에이전트 간 통신의 정확성과 효율성
- 병렬 처리를 통한 성능 향상
- 오류 처리 및 복구 메커니즘

이 프레임워크는 온디바이스 AI 모델들의 **실제 에이전트 워크로드에서의 성능**을 객관적으로 평가하며, 특히 **도구 사용 능력**과 **복잡한 명령 처리 능력**에 중점을 둔 벤치마킹 시스템입니다.

## 부차 화제
- 다중 에이전트 아키텍처: Claude code sub agent들이 nano agent server를 호출하는 계층적 구조와 에이전트 간 통신 흐름

- 모델 호환성 및 확장성: GPT-5 nano, mini, GPT-5와 OpenAI 로컬 모델들을 동일한 구조로 교체 가능한 시스템 설계

- 하드웨어 성능 최적화: M4 Max MacBook Pro의 128GB 통합 메모리를 활용한 20B, 120B 파라미터 모델의 온디바이스 실행

- MCP 서버 통합: nano agent MCP 서버를 통한 도구 접근 및 메타데이터 수집 시스템

- 벤치마크 테스트 설계: 단순 질답부터 파일 읽기까지 난이도별 테스트 케이스 구성과 JSON 형식 응답 구조화

- 에이전트 오케스트레이션: 9개의 nano agent 병렬 실행과 명확한 프롬프트 패턴을 통한 에이전트 간 통신 관리

- 도구 사용 능력 평가: 파일 읽기, 특정 라인 추출 등 에이전트의 도구 활용 능력과 지시사항 준수 평가

- 응답 형식 표준화: 기대 출력값 정의와 일관된 응답 형식을 통한 결과 검증 시스템

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
