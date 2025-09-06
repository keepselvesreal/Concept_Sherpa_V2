# 속성
process_status: true

# 추출

## 핵심 내용
GPT-5 Agentic Coding with Claude Code는 GPT-5, Opus 4.1, Sonnet, Haiku 등 최신 AI 모델들과 20B, 120B 파라미터 온디바이스 모델들의 에이전트 성능을 공정하게 비교 평가하는 프레임워크입니다. HOP(Higher Order Prompt)과 LOP(Lower Order Prompt)를 활용한 강력한 프롬프트 오케스트레이션 기법을 구현하여, 단순한 프롬프트 호출이 아닌 여러 도구를 연결한 실제 엔지니어링 작업을 수행하는 에이전트 아키텍처를 평가합니다. S~F 등급 시스템과 Claude Code Opus 4.1을 LLM 심사관으로 활용하여 성능, 속도, 비용의 3가지 핵심 지표로 모델들을 종합 평가합니다.

## 상세 핵심 내용

### 에이전트 성능 평가 프레임워크

**평가 대상 모델들**
- **클라우드 모델**: GPT-5, Claude Code Opus 4.1, Sonnet, Haiku
- **온디바이스 모델**: 20B, 120B 파라미터 모델 (M4 Max MacBook Pro에서 직접 실행)
- **혁신적 성능**: 온디바이스 모델들의 예상 외 높은 성능과 향후 모델 선택 전략의 변화

**핵심 평가 지표**
- **성능 (Performance)**: 실제 엔지니어링 작업 완성도
- **속도 (Speed)**: 작업 수행 시간과 응답성
- **비용 (Cost)**: 토큰 사용량과 경제적 효율성

### 프롬프트 오케스트레이션 아키텍처

**HOP & LOP 프롬프트 구조**
- **HOP (Higher Order Prompt)**: 전체적인 실행 흐름과 응답 형식을 정의하는 상위 레벨 프롬프트
- **LOP (Lower Order Prompt)**: 구체적인 평가 세부사항을 포함하는 재사용 가능한 모듈형 프롬프트
- **컨텍스트 엔지니어링**: 효율적 프롬프트 재사용과 동적 교체를 통한 다양한 에이전트 행동 평가

**에이전트 아키텍처의 중요성**
- 단순한 프롬프트 호출을 넘어선 복합적 도구 연결
- 실제 엔지니어링 워크플로우를 모방한 평가 시나리오
- 나노 에이전트 MCP 서버를 활용한 모듈화된 평가 시스템

### 평가 시스템 구현

**grading_system**
- **평가 등급**: S(최고) ~ F(최저)의 직관적이고 간단한 등급 체계
- **LLM Judge**: Claude Code Opus 4.1을 심사관으로 활용한 객관적 평가
- **표준화된 응답**: 일관된 결과 출력을 위한 표준 응답 형식

**evaluation_workflow**
```
1. 나노 에이전트 MCP 서버 기반 평가 환경 구성
2. HOP에 정의된 형식으로 각 모델 실행
3. LOP 세부사항을 동적으로 교체하며 다양한 시나리오 평가
4. 성능-속도-비용 3축 기준으로 종합 분석
5. 표준 응답 형식으로 결과 보고 및 모델 선택 전략 제시
```

### 기술적 구현 및 현재 상태

**코드베이스 구조**
- `/commands/perf/` - 성능 평가 명령어 및 벤치마크 도구
- `/plans/` - 각 모델별 실행 계획 및 평가 시나리오
- `/agents/` - 모델별 에이전트 구현체 및 인터페이스
- `/app_docs/`, `/ai_docs/` - 애플리케이션 사양 및 AI 모델 문서

**실행 상태 모니터링**
- **GPT OSS 20B 모델**: 온디바이스 처리로 인한 완료 대기 중
- **기타 모델들**: 평가 완료 상태
- **최종 단계**: Claude Code가 전체 결과 종합 및 최종 평가 수행 중
- **토큰 최적화**: Opus 모델의 충분한 토큰 확보 및 스트리밍 결과 실시간 모니터링

## 주요 화제
- **Prompt Orchestration Architecture(프롬프트 오케스트레이션 아키텍처)**: HOP(Higher Order Prompt)와 LOP(Lower Order Prompt)를 활용한 계층적 프롬프트 구조 설계 및 재사용 가능한 프롬프트 엔지니어링 기법

- **Agent-Based Evaluation System(에이전트 기반 평가 시스템)**: Claude Code Opus 4.1을 LLM Judge로 활용한 에이전트 행동 평가 및 S-F 등급제 평가 시스템 구현

- **Codebase Structure Analysis(코드베이스 구조 분석)**: Primary agentic directories, plans, application-specific nano agents, commands 및 agents 디렉토리 구조 해부

- **Performance Testing Framework(성능 테스트 프레임워크)**: 다양한 AI 모델들(GPT OSS 20 billion 포함)에 대한 병렬 성능 테스트 및 평가 결과 수집 시스템

- **MCP Server Integration(MCP 서버 통합)**: Nano agent MCP server를 활용한 명령 실행 및 결과 리포팅 시스템 구현

- **Response Format Standardization(응답 형식 표준화)**: 일관된 평가 결과 출력을 위한 구조화된 응답 형식 및 grading scheme 정의

- **Token Management & Evaluation(토큰 관리 및 평가)**: Claude Code 실행 시 토큰 스트리밍 모니터링 및 Opus 모델 토큰 사용량 관리

## 부차 화제
- 프롬프트 오케스트레이션 기법: Higher Order Prompt(HOP)와 Lower Order Prompt(LOP)를 활용한 프롬프트 재사용 및 계층적 구성 방법
- 에이전트 성능 평가 시스템: S~F 등급 체계를 사용한 에이전트 행동 평가 및 채점 방식
- 디렉토리 구조 설계: commands, agents, app docs, AI docs 등으로 구성된 에이전트 코드베이스 조직화 방법
- Claude Code Opus 4.1 활용: LLM을 판사(judge)로 사용하여 에이전트 평가를 자동화하는 접근법
- MCP 서버 통합: nano agent MCP 서버를 활용한 명령 실행 및 결과 처리 방식
- 응답 형식 표준화: 일관된 평가 결과 보고를 위한 구조화된 응답 포맷 정의
- 온디바이스 모델 처리: GPT OSS 20 billion과 같은 로컬 모델의 실행 시간 및 성능 특성
- 토큰 스트리밍: 실시간 응답 생성 및 토큰 사용량 모니터링 방법

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
