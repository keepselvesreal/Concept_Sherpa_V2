# 속성
process_status: true

# 추출

## 핵심 내용
이 문서는 GPT-5, Opus 4.1, Sonnet, Haiku 등 최신 AI 모델들과 M4 Max MacBook Pro에서 직접 구동되는 20B, 120B 파라미터 온디바이스 모델들의 에이전트 성능을 종합적으로 측정하는 시스템을 설명합니다. Claude Code 주 에이전트가 하위 에이전트들을 실행하고, 이들이 nano 에이전트 서버를 통해 GPT 모델들과 OpenAI 로컬 모델들을 직접 구동하여 벤치마크 테스트를 수행합니다. 시스템은 간단한 질문부터 파일 읽기와 같은 에이전트 작업까지 단계적으로 난이도를 높여가며 모델들의 지시 수행 능력과 도구 사용 능력을 평가하며, 성능, 속도, 비용의 3가지 핵심 지표로 모델 비교 분석을 제공합니다.

## 상세 핵심 내용
이 벤치마킹 시스템은 단순한 프롬프트 호출이 아닌 실제 에이전트 아키텍처에서 여러 도구를 연결하여 엔지니어링 작업을 수행하는 능력을 측정합니다. Claude Code를 기반으로 한 계층적 에이전트 구조에서 주 에이전트가 하위 에이전트들을 관리하고, nano 에이전트 서버를 통해 다양한 모델들과 통신합니다. 특히 M4 Max MacBook Pro에서 직접 실행되는 20B, 120B 파라미터 온디바이스 모델들의 혁신적 성능을 측정하여, 클라우드 기반 모델들과의 성능 비교를 통해 향후 에이전트 코딩에서의 최적 모델 선택 전략을 도출합니다. 평가 과정은 기본적인 질의응답부터 복잡한 파일 조작과 도구 사용까지 점진적으로 복잡도를 증가시키며, 각 모델의 실제 업무 환경에서의 실용성을 종합적으로 검증합니다.

## 주요 화제
- On-Device AI Model Architecture(온디바이스 AI 모델 아키텍처): Claude Code sub agents가 nano agent server를 호출하는 구조적 설계 및 다중 에이전트 시스템 구축 방법

- Hardware Performance Capabilities(하드웨어 성능 역량): M4 Max MacBook Pro 128GB 통합 메모리에서 20억/1200억 파라미터 모델의 온디바이스 실행 성능

- Multi-Model Integration Strategy(다중 모델 통합 전략): GPT-5 nano, mini, OpenAI 로컬 모델들을 동일한 아키텍처로 교체 가능한 모듈식 설계

- Agent Benchmarking Methodology(에이전트 벤치마킹 방법론): JSON 형식 응답, 파일 읽기, 지시사항 준수 등 다양한 난이도의 작업을 통한 성능 측정

- Prompt Engineering and Communication Flow(프롬프트 엔지니어링 및 통신 흐름): 명확한 지시사항, 변수 설정, 예상 출력 형식을 통한 에이전트 간 효과적인 의사소통 구조

- Tool Integration and MCP Server(도구 통합 및 MCP 서버): nano agent MCP 서버를 통한 도구 사용 능력 및 구조화된 응답 처리

- Instruction Following and Task Complexity(지시사항 준수 및 작업 복잡성): 단순 질문부터 고급 에이전틱 작업까지 점진적 난이도 증가를 통한 모델 능력 평가

## 부차 화제

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
