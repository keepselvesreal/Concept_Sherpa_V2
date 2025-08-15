# 속성
process_status: true

# 추출

## 핵심 내용
GPT-5 Agentic Coding with Claude Code는 GPT-5, Opus 4.1, Sonnet, Haiku 등 최신 AI 모델들과 온디바이스 20B/120B 파라미터 모델의 에이전트 성능을 공정하게 비교 평가하는 프레임워크입니다. 현재 AI 모델 개발의 핵심 트렌드는 단일 프롬프트 성능이 아닌 에이전트 아키텍처로, 여러 도구를 연결하여 실제 엔지니어링 결과를 달성하는 능력이 중요합니다. 성능, 속도, 비용의 3가지 지표로 종합 평가한 결과, 예상과 달리 Claude 3 Haiku가 다른 고성능 모델들을 능가하는 결과를 보였으며, M4 Max MacBook Pro에서 실행되는 온디바이스 모델들의 혁신적 가능성도 확인되었습니다.

## 상세 핵심 내용
### Agent Architecture의 핵심 트렌드와 평가 프레임워크

#### AI 모델 개발의 패러다임 전환
현재 AI 모델 개발에서 가장 중요한 트렌드는 **Agent Architecture**입니다. GPT-5, Anthropic의 차세대 모델, Cursor CLI 등 모든 주요 모델들이 이 방향으로 집중하고 있으며, 단순한 프롬프트 호출에서 **멀티 툴 체이닝**을 통한 실제 엔지니어링 작업 수행 능력으로 평가 기준이 변화하고 있습니다.

#### 공정한 평가 환경과 3가지 핵심 지표
**Nano Agent & MCP Server 활용한 표준화**:
- 모든 모델에게 동일한 컨텍스트와 프롬프트 제공
- 동일한 스캐폴딩 환경에서 순수 성능 비교
- **성능(Performance)**: 실제 엔지니어링 작업 완수 능력
- **속도(Speed)**: 작업 처리 시간과 응답성
- **비용(Cost)**: 운영 효율성과 경제성

### 모델별 성능 평가 결과

#### 예상을 뒤집는 Claude 3 Haiku의 우수 성능
- **일반적 예상**: 고성능 모델(GPT-5, Opus 4.1, Sonnet)이 상위권
- **실제 결과**: Claude 3 Haiku가 다른 모든 모델을 앞서는 종합 성과
- **환경 의존성**: Claude Code 환경과 표준화된 평가 환경 간 성능 편차 확인
- **작업 복잡도 무관성**: 단순한 작업("수도가 무엇인가?")에서도 모델별 현저한 차이 발생

#### 온디바이스 모델의 혁신적 잠재력
**M4 Max MacBook Pro 플랫폼**:
- **20B 파라미터 모델**: 로컬 실행으로 프라이버시와 속도 확보
- **120B 파라미터 모델**: 클라우드급 성능의 온디바이스 구현
- **비용 효율성**: 클라우드 API 호출 비용 대비 경제적 운영
- **향후 전망**: 에이전트 코딩에서 온디바이스 모델의 경쟁력 증대

### 에이전트 아키텍처의 미래 방향

#### 새로운 성능 지표와 평가 기준
1. **도구 연결 및 활용 능력**: 여러 도구를 효율적으로 연결하는 능력
2. **실제 작업 수행 능력**: 단순한 파라미터 수를 넘어선 실무 성과
3. **환경 적응성**: 다양한 개발 환경에서의 일관된 성능 유지
4. **효율성과 경제성**: 성능 대비 비용과 속도의 최적화

#### 모델 선택 전략의 진화
- **컨텍스트 의존성 고려**: 작업 환경과 요구사항에 따른 맞춤형 모델 선택
- **종합 평가 체계**: 성능, 속도, 비용을 균형있게 고려한 의사결정
- **온디바이스 vs 클라우드**: 프라이버시, 비용, 성능을 종합한 플랫폼 전략
- **에이전트 특화 최적화**: 단일 태스크가 아닌 멀티 툴 워크플로우 최적화

## 주요 화제
- **Agent Architecture 트렌드**: AI 모델들(GPT5, Anthropic 차세대 모델, cursor CLI 등)이 모두 집중하고 있는 핵심 동향으로서의 에이전트 아키텍처의 중요성

- **Agentic Performance 평가**: 단일 프롬프트 호출을 넘어서 에이전트가 여러 도구를 연결하여 실제 엔지니어링 결과를 달성하는 능력에 대한 성능 평가 방법론

- **모델 성능 순위의 역설**: Claude 3 Haiku가 다른 상위 모델들을 능가하는 예상치 못한 결과와 이에 대한 분석

- **공정한 평가 환경 구축**: MCP 서버와 nano agent를 활용하여 모든 모델에게 동일한 컨텍스트와 프롬프트를 제공하는 공정한 테스트 환경 조성

- **성능-속도-비용 종합 평가**: 단일 지표가 아닌 성능, 속도, 비용을 종합적으로 고려한 모델 평가 프레임워크

- **플랫폼별 성능 차이**: Claude Code 내에서와 일반적인 환경에서의 모델 성능 차이 및 그 원인 분석

- **간단한 작업에서의 모델 비교**: "수도가 무엇인가?"와 같은 기본적인 질문에서도 나타나는 모델 간 성능 차이

## 부차 화제
- Agent Architecture(에이전트 아키텍처): 현재 AI 모델 개발에서 가장 중요한 트렌드로, 단일 프롬프트 호출이 아닌 여러 도구를 연결하여 실제 엔지니어링 결과를 달성하는 방식

- Model Performance Ranking(모델 성능 순위): Claude 3 Haiku가 다른 모델들을 능가하는 예상과 다른 결과를 보여주며, 기존 예상과 역순의 성능을 나타냄

- Performance Evaluation Criteria(성능 평가 기준): 성능, 속도, 비용을 종합적으로 고려한 공정한 평가 방식

- MCP Server and Nano Agent(MCP 서버와 나노 에이전트): 모든 모델이 동일한 컨텍스트와 프롬프트로 스캐폴딩되어 공정한 경쟁 환경을 제공하는 새로운 서버 시스템

- Context-dependent Performance(컨텍스트 의존적 성능): Claude Code 내에서는 Opus와 Sonnet이 더 나은 성능을 보일 것이라는 예측과 실제 단순 작업에서의 다른 결과

- Task Complexity vs Model Performance(작업 복잡도와 모델 성능): "수도가 무엇인가?"와 같은 극단적으로 단순한 작업에서 보이는 모델별 다양한 결과

# 내용
## Model Evaluation Framework

There is one trend that matters above all. Right now, it doesn't matter if we're talking about GPT5, whatever Anthropic has cooking next, the cursor CLI or any other model that's getting put out right now, open source, closed source, there is one thing everyone is focused on. If you've been paying any attention, you know exactly what it is. It is the agent architecture.

Why does everyone care so much about agents? First, let's understand how you and I, engineers with our boots on the ground, can have a better, deeper understanding of these models' agentic performance. It's not about a single prompt call anymore. It's about how well your agent chains together multiple tools to accomplish real engineering results on your behalf.

What just happened with this prompt? You can see here we have rankings. Surprisingly, we have Claude 3 Haiku outperforming all of our other models. If you look at this, it looks backward. We would expect these models to be on top and these other models to be on the bottom. What's going on?

We're evaluating all of our models against each other in a fair playing field where we care about performance, speed, and cost as a collective. These agents are operating in a nano agent, a new MCP server to create a fair playing field where every one of these models is scaffolded with the same context and prompt. Two of the big three. And then we get to see how they truly perform.

If we put these models inside Claude Code, I can guarantee you Opus and Sonnet will outperform. But you can see here for this extremely simple task, "what's the capital?" we can see very different results out of the box.

# 구성
