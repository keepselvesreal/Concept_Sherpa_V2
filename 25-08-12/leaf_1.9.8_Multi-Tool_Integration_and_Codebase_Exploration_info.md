# 추가 정보

## 핵심 내용
Eric는 Claude Code와 Cursor를 조합하여 사용하며, 일반적으로 Claude Code로 시작한 후 Cursor로 세부 수정을 진행한다고 설명합니다. 새로운 코드베이스 영역을 탐색할 때는 Claude Code를 활용해 인증 처리 위치나 유사 기능들을 파악하고, 관련 파일명과 클래스들을 식별하여 전체적인 구조를 이해한 후 실제 기능 개발에 착수하는 체계적인 접근법을 사용합니다.

## 상세 핵심 내용

## 주요 화제
- **Multi-Tool Workflow 조합 전략**: Claude Code와 Cursor를 함께 사용하는 워크플로우 - Claude Code로 시작하고 Cursor로 세부 수정, 정확한 변경사항이 있을 때는 Cursor로 특정 라인 타겟팅

- **Git 워크트리와 스택 PR 활용**: Git work trees를 활용해 여러 Claude Code를 동시 실행하고 스택 PR을 통해 작업을 병합하는 고급 워크플로우 접근법

- **새로운 코드베이스 탐색 전략**: 생소한 코드베이스에서 빠르고 체계적으로 PR을 작성하기 위한 엔지니어링 접근 방식 - "vibe coding"을 피하고 구조적으로 이해하는 방법

- **코드베이스 이해를 위한 Claude Code 활용**: 특정 기능(인증 등)이 코드베이스 어디에 위치하는지 찾고, 유사한 기능들과 관련 파일명, 클래스들을 파악하여 멘탈 모델 구축

- **기능 구현 전 사전 탐색**: 실제 기능을 작성하기 전에 Claude Code를 사용해 코드베이스를 탐색하고 이해한 후 작업에 착수하는 체계적 접근법

## 부차 화제
- Multi-Tool Workflow Strategy: Claude Code와 Cursor를 조합해서 사용하는 방법 - Claude Code로 작업을 시작하고 Cursor로 세부 수정을 하거나, 정확한 변경사항을 알고 있을 때 Cursor로 특정 라인을 타겟팅하는 전략

- Git Worktrees and Stack PRs: 여러 Claude Code 인스턴스를 git worktrees와 함께 사용하거나 stack PR을 만드는 등의 고급 git 워크플로우 활용 방안

- Codebase Exploration Strategy: 새로운 코드베이스 영역에 익숙하지 않을 때 Claude Code를 활용한 체계적인 탐색 방법 - 인증 로직 위치 파악, 유사한 기능 찾기, 관련 파일명과 클래스 식별 등

- Mental Model Building: "vibe coding"을 피하고 코드베이스의 구조적 이해를 바탕으로 한 체계적인 개발 접근법

- Feature Development Preparation: 실제 기능 개발 전에 코드베이스 이해를 위한 사전 탐색 과정의 중요성

- Engineering Best Practices: 빠른 PR 배송과 코드 품질을 동시에 달성하기 위한 구조적이고 체계적인 엔지니어링 접근 방식
