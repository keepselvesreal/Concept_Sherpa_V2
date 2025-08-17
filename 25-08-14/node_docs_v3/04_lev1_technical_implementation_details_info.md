# 속성
process_status: true

# 추출

## 핵심 내용
이 시스템은 프롬프트 오케스트레이션 기법을 활용한 에이전트 성능 평가 프레임워크로, HOP(Higher Order Prompt)와 LOP(Lower Order Prompt)를 통해 프롬프트를 재사용하고 계층적으로 관리합니다. S부터 F까지의 간단한 등급 체계를 사용하여 다양한 에이전트 행동을 평가하며, Claude Code Opus 4.1을 LLM 판사로 활용해 결과를 분석합니다. 전체 구조는 commands/perf 디렉토리 내에서 nano 에이전트 MCP 서버를 실행하고 결과를 표준화된 응답 형식으로 보고하는 방식으로 동작합니다.

## 상세 핵심 내용
### 코드베이스 구조 및 설정

이 시스템은 에이전트 기반 아키텍처로 구성되어 있으며, 다음과 같은 주요 디렉토리 구조를 가집니다:

- **Primary agentic directories**: 핵심 에이전트 기능을 담당하는 메인 디렉토리들
- **Plans**: 실행 계획 및 전략을 정의하는 영역
- **Application specific nano agent**: 특정 애플리케이션에 특화된 마이크로 에이전트
- **App docs & AI docs**: 애플리케이션 및 AI 관련 문서화
- **Commands & Agents**: 명령어 처리 및 에이전트 관리의 핵심 구성요소

### 프롬프트 오케스트레이션 시스템

#### HOP (Higher Order Prompt) & LOP (Lower Order Prompt) 아키텍처

시스템의 핵심은 강력한 프롬프트 오케스트레이션 기법입니다:

- **HOP (Higher Order Prompt)**: 상위 레벨 프롬프트로 전체 실행 흐름을 제어
- **LOP (Lower Order Prompt)**: 하위 레벨 프롬프트로 세부 구현 내용을 담당
- **재사용성**: 프롬프트들을 모듈화하여 다양한 상황에서 재사용 가능
- **동적 교체**: 평가하려는 에이전트 동작에 따라 LOP를 동적으로 교체하여 다른 세부사항 적용

### 평가 및 채점 시스템

#### 그레이딩 스키마
- **등급 체계**: S부터 F까지의 간단한 등급제 (S가 최고, F가 최저)
- **표준화된 형식**: 일관된 클래식 프롬프트 포맷 사용
- **컴팩트 뷰**: 모든 내용을 접어서 빠른 이해를 위한 개요 제공

#### 실행 흐름
1. **Nano Agent MCP Server 활용**: 마이크로 서비스 기반 에이전트 실행
2. **결과 실행 및 수집**: 정의된 작업을 수행하고 결과 데이터 수집
3. **응답 형식 보고**: 표준화된 그레이딩 스키마에 따른 결과 보고

### AI 심사관 시스템

#### Claude Code Opus 4.1 LLM Judge
- **자동 평가**: Claude Code Opus 4.1을 LLM 심사관으로 활용하여 전체 프로세스 관리
- **지능형 판단**: AI가 에이전트 성능을 객관적으로 평가하고 등급 부여
- **스트리밍 처리**: 실시간 토큰 스트리밍을 통한 즉시 피드백 제공

### 평가 세부사항 및 프로세스

#### LOP 기반 동적 평가
- **세부 프롬프트 주입**: 평가 세부사항에 LOP (Lower Order Prompts) 삽입
- **행동 평가**: 다양한 에이전트 동작을 체계적으로 평가하기 위한 세부 프롬프트 교체
- **맞춤형 평가**: 특정 에이전트 기능에 맞는 맞춤형 평가 기준 적용

#### 실시간 모니터링 및 결과 처리
- **진행 상황 추적**: 터미널을 통한 실시간 평가 진행 상황 모니터링
- **성능 분석**: 각 모델별 완료 시간 및 성능 특성 분석 (예: GPT OSS 20 billion의 온디바이스 처리 시간)
- **결과 종합**: 모든 평가가 완료된 후 Claude Code가 결과를 구체적인 응답으로 종합

### 테스트 및 검증 프레임워크

- **더미 테스트**: 기본적인 기능 검증을 위한 더미 테스트 실행
- **종합 평가**: HOP와 실제 평가(eval one) 실행을 통한 종합적 성능 평가
- **토큰 효율성**: Opus 토큰 사용량 최적화를 통한 효율적인 평가 수행

이 시스템은 모듈화된 프롬프트 엔지니어링, AI 기반 자동 평가, 그리고 실시간 모니터링을 결합한 포괄적인 에이전트 성능 평가 플랫폼입니다.

## 주요 화제
- **프롬프트 오케스트레이션 시스템**: HOP(Higher Order Prompt)와 LOP(Lower Order Prompt)를 활용한 계층적 프롬프트 구조로 프롬프트 재사용성과 모듈화를 구현

- **코드베이스 아키텍처**: 주요 에이전트 디렉토리, 플랜, 애플리케이션별 나노 에이전트, 앱 문서, AI 문서, 명령어 및 에이전트로 구성된 체계적인 디렉토리 구조

- **평가 시스템**: S부터 F까지의 등급 체계를 사용한 에이전트 성능 평가 메커니즘 구현

- **LLM as a Judge**: Claude Code Opus 4.1을 판정자로 활용하여 에이전트 행동 평가 및 관리 자동화

- **나노 에이전트 MCP 서버**: 명령 실행 및 결과 보고를 위한 MCP(Model Context Protocol) 서버 활용

- **컨텍스트 엔지니어링**: 다양한 에이전트 행동 평가를 위해 세부 프롬프트를 교체 가능한 모듈형 프롬프트 설계

- **실시간 평가 모니터링**: GPT OSS 20 billion 모델 등 다양한 모델의 온디바이스 실행 및 완료 상태 추적

- **토큰 스트리밍**: 평가 결과를 실시간으로 스트리밍하여 구체적인 응답 생성

## 부차 화제
- 코드베이스 구조 및 디렉토리 구성: 주요 에이전트 디렉토리들, plans, 애플리케이션별 nano agent, app docs, AI docs, commands, agents 등의 전체적인 프로젝트 구조

- 프롬프트 오케스트레이션 기법: commands 디렉토리 내 perf 폴더의 HOP(Higher Order Prompt)와 LOP(Lower Order Prompt) 구조를 통한 프롬프트 재사용 및 계층적 관리 방식

- 평가 시스템 설계: S부터 F까지의 단순한 등급 체계를 사용한 성능 평가 메커니즘

- 클래식 프롬프트 포맷: 표준화된 프롬프트 구조와 포맷팅 방식

- MCP 서버 통합: nano agent MCP 서버를 사용한 실행 및 결과 보고 체계

- 응답 포맷 표준화: 단순한 등급 체계 기반의 일관된 응답 형식 정의

- LLM as Judge 패턴: Claude Code Opus 4.1을 평가자로 활용하는 AI 기반 판정 시스템

- 컨텍스트 엔지니어링: 다양한 에이전트 행동 평가를 위한 세부 정보가 포함된 LOP를 동적으로 교체하는 방식

- 터미널 기반 모니터링: 실행 진행상황을 터미널을 통해 실시간으로 추적하는 시스템

- 온디바이스 처리 성능: GPT OSS 20 billion과 같은 대규모 모델의 로컬 실행 시간과 성능 특성

- 토큰 스트리밍 처리: 실시간 토큰 스트리밍을 통한 응답 생성 과정 모니터링

- 더미 테스트 환경: 평가 시스템 검증을 위한 테스트 케이스 구성

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
