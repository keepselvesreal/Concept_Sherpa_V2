/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/
  ├── src/
  │   ├── core/                          # 핵심 비즈니스 로직
  │   │   ├── __init__.py
  │   │   ├── pipeline_orchestrator.py   # 메인 파이프라인 오케스트레이터
  │   │   └── base/                      # 기본 클래스들
  │   │       ├── __init__.py
  │   │       ├── base_processor.py      # 모든 프로세서의 기본 클래스
  │   │       └── pipeline_result.py     # 결과 클래스들
  │   │
  │   ├── stages/                        # 4단계 프로세서들
  │   │   ├── __init__.py
  │   │   ├── stage_01_workspace.py      # 1단계: 기본 작업 준비
  │   │   ├── stage_02_integration.py    # 2단계: 통합 노드 정보 문서 생성
  │   │   ├── stage_03_processing.py     # 3단계: 가공 작업
  │   │   └── stage_04_toc_generation.py # 4단계: 목차 생성
  │   │
  │   ├── services/                      # 독립적인 서비스들
  │   │   ├── __init__.py
  │   │   ├── ai_service.py              # AI 관련 설정 및 처리
  │   │   ├── pdf_service.py             # PDF 처리
  │   │   ├── toc_service.py             # 목차 관련 처리
  │   │   └── file_service.py            # 파일 시스템 처리
  │   │
  │   ├── utils/                         # 유틸리티들
  │   │   ├── __init__.py
  │   │   ├── logger.py                  # 로깅 시스템
  │   │   ├── config_manager.py          # 설정 관리
  │   │   └── path_utils.py              # 경로 유틸리티
  │   │
  │   └── exceptions/                    # 예외 처리
  │       ├── __init__.py
  │       └── pipeline_exceptions.py    # 커스텀 예외들
  │
  ├── config/                           # 설정 파일들
  │   ├── ai_config.yaml               # AI 설정 (기존)
  │   ├── pipeline_config.yaml         # 파이프라인 설정
  │   └── logging_config.yaml          # 로깅 설정
  │
  ├── logs/                            # 로그 디렉토리
  └── tests/                           # 테스트

  핵심 설계 원칙

  1. 단일 책임 원칙: 각 모듈이 하나의 명확한 책임만 가짐
  2. 의존성 주입: 설정과 서비스들을 주입받아 사용
  3. 인터페이스 기반: 추상화된 인터페이스로 모듈 간 통신
  4. 설정 분리: AI 설정, 파이프라인 설정, 로깅 설정 각각 독립적 관리
  5. 로깅 체계화: 단계별, 용도별로 구조화된 로깅

  주요 개선점

  1. AI 설정 독립화: 각 스크립트마다 독립적인 AI 도구 설정 가능
  2. 로깅 시스템 강화: 디버깅과 문제 추적을 위한 체계적 로그
  3. 재사용성 향상: 각 단계를 독립적으로 실행 가능
  4. 테스트 용이성: 각 모듈을 개별적으로 테스트 가능
  5. 확장성: 새로운 단계나 기능 추가가 쉬움