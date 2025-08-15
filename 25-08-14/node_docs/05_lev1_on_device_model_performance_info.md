# 속성
process_status: true

# 추출

## 핵심 내용
이 섹션은 Claude Code의 계층적 에이전트 시스템을 통해 다양한 온디바이스 AI 모델들의 성능을 벤치마크하는 방법을 설명합니다. M4 Max MacBook Pro에서 20억 및 1200억 파라미터 모델을 포함한 다양한 로컬 모델들을 실행하며, 각 모델은 MCP 나노 에이전트 서버를 통해 도구 사용과 지시사항 준수 능력을 테스트받습니다. 시스템은 주 에이전트가 서브 에이전트들을 조율하고, 각 서브 에이전트가 특정 모델에 연결되어 구조화된 프롬프트와 JSON 형태의 응답을 통해 성능을 측정하는 구조로 되어 있습니다.

## 주요 화제
- On-Device Model Architecture(온디바이스 모델 아키텍처): Claude Code 서브 에이전트가 nano 에이전트 서버를 호출하는 계층적 구조와 GPT5 nano, mini 등 다양한 모델 지원 구조

- Local Model Performance(로컬 모델 성능): M4 Max MacBook Pro에서 20억, 1200억 파라미터 모델을 온디바이스로 실행하며 에이전트 디코딩 작업 수행

- Agent Benchmarking System(에이전트 벤치마킹 시스템): "미국의 수도" 같은 더미 테스트부터 README 파일 읽기까지 난이도별 프롬프트 테스트 구조

- Multi-Agent Orchestration(멀티 에이전트 오케스트레이션): 9개의 nano 에이전트 동시 실행과 주 에이전트-서브 에이전트 간 명확한 통신 흐름 관리

- Instruction Following Testing(명령어 수행 테스트): JSON 형식 응답, 파일의 첫 10줄과 마지막 10줄 추출 등 정확한 명령어 수행 및 도구 사용 능력 평가

- Tool Integration Framework(도구 통합 프레임워크): MCP nano 에이전트 도구를 통한 단일 도구 접근 구조와 보조 메타데이터 수집 시스템

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
