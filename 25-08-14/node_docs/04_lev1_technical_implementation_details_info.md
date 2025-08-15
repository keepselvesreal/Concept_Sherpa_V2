# 속성
process_status: true

# 추출

## 핵심 내용
이 코드베이스는 프롬프트 오케스트레이션 기법을 사용하여 AI 에이전트 성능을 평가하는 시스템을 구현합니다. HOP(Higher Order Prompt)와 LOP(Lower Order Prompt) 구조를 통해 프롬프트를 재사용하고 계층적으로 관리하며, Claude Code Opus 4.1을 LLM 판사로 사용해 S부터 F까지의 등급 체계로 에이전트 행동을 평가합니다. 현재 GPT OSS 20 billion 모델을 포함한 여러 모델들의 성능 테스트를 진행하고 있으며, 온디바이스 모델은 처리 시간이 더 오래 걸리는 특징을 보입니다.

## 상세 핵심 내용
### 프로젝트 구조와 디렉토리 구성

프로젝트는 표준적인 에이전트 기반 구조를 가지고 있으며, 다음과 같은 핵심 디렉토리들로 구성됩니다:

- **Primary agentic directories**: 에이전트 관련 핵심 디렉토리들
- **Plans**: 계획 및 전략 관련 파일들
- **Application specific nano agent**: 애플리케이션 특화 나노 에이전트
- **App docs & AI docs**: 애플리케이션 및 AI 관련 문서
- **Commands & Agents**: 명령어 및 에이전트 실행 파일들

### 프롬프트 오케스트레이션 시스템

**Commands 디렉토리 내 Perf 구조**:
- **HOP (Higher Order Prompt)**: 상위 레벨 프롬프트
- **LOPs (Lower Order Prompts)**: 하위 레벨 세부 프롬프트

이는 프롬프트를 재사용하고 계층적으로 관리할 수 있는 강력한 **프롬프트 오케스트레이션 기법**입니다.

### 평가 시스템 구조

**평가 등급 시스템**:
- **S등급**: 최고 성능
- **F등급**: 최저 성능
- 클래식한 등급 기반 평가 방식 사용

**프롬프트 포맷**:
- 표준화된 클래식 프롬프트 형식
- 빠른 이해를 위한 접이식 구조
- 나노 에이전트 MCP 서버 활용
- 실행 후 응답 형식으로 결과 리포트

### LLM 평가 시스템

**Claude Code Opus 4.1**을 **LLM as a Judge**로 사용하여:
- 전체 평가 프로세스 관리
- 다양한 에이전트 행동 평가
- 자동화된 성능 측정

### 동적 프롬프트 교체 메커니즘

**LOPs 활용**:
- 평가 세부사항에 LOPs 삽입
- 다양한 에이전트 행동 평가 시 프롬프트 동적 교체
- 세부 내용을 포함한 프롬프트를 필요에 따라 스왑

### 실행 및 평가 과정

**실시간 처리 현황**:
- GPT OSS 20 billion 모델 처리 대기 (온디바이스 실행으로 인한 지연)
- 다른 모델들은 완료 상태
- Claude Code가 결과를 구체적인 응답으로 포뮬레이션
- 토큰 스트리밍을 통한 실시간 평가 진행

### 테스트 및 검증 구조

**평가 실행 구조**:
- Higher Order Prompt와 Lower Order Prompt의 계층적 연동
- Dummy test를 통한 초기 검증
- 실제 평가 실행 (eval one)

이 시스템은 프롬프트 엔지니어링과 컨텍스트 엔지니어링을 통한 효율적인 AI 에이전트 평가 프레임워크를 구현하고 있습니다.

## 주요 화제
- 코드베이스 구조(Codebase Structure): agentic directories, plans, application specific nano agent, app docs, AI docs, commands, agents 등의 디렉토리 구성

- 프롬프트 오케스트레이션(Prompt Orchestration): HOP(Higher Order Prompt)와 LOP(Lower Order Prompt)를 활용한 프롬프트 엔지니어링 및 컨텍스트 엔지니어링 기법

- 평가 시스템(Evaluation System): S부터 F까지의 등급제 평가 시스템과 classic prompt format을 통한 성능 평가

- LLM as Judge: Claude Code Opus 4.1을 LLM 판사로 활용하여 agentic behavior 평가 및 결과 관리

- 모델 성능 테스트(Model Performance Testing): GPT OSS 20 billion 등 다양한 모델들의 성능 테스트 및 on-device 모델의 실행 시간

- Nano Agent MCP Server: MCP 서버를 통한 nano agent 실행 및 결과 보고 시스템

- Response Format: 구조화된 응답 형식과 평가 결과의 구체적인 보고 방식

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
