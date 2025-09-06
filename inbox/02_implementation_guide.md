# 📋 책 파이프라인 리팩토링 구현 가이드

## 🎯 구현 우선순위

### 1단계: 독립적 도메인부터 시작 (1-2일)
```
TOCExtractor (TOC Domain)
  ├── extract_toc() 메서드 추출
  ├── PyMuPDF 의존성 분리
  └── 단위 테스트 작성

EnhancedTOCGenerator 
  ├── generate_enhanced_toc() 메서드 추출
  ├── AI Provider 의존성 분리
  └── 템플릿 외부화
```

### 2단계: 핵심 도메인 구현 (2-3일)
```
ChapterWorkspace (Chapter Domain)
  ├── 디렉터리 생성 로직 추출
  ├── 파일 시스템 의존성 분리
  └── 워크스페이스 관리 테스트

NodeDocumentProcessor (Document Domain)
  ├── 노드 처리 로직 추출
  ├── AI 분석 부분 분리
  └── 배치 처리 최적화
```

### 3단계: 오케스트레이션 계층 (1-2일)
```
PipelineOrchestrator
  ├── 단계별 실행 흐름 관리
  ├── 오류 처리 및 롤백
  └── 진행 상황 추적
```

### 4단계: 인프라스트럭처 통합 (1-2일)
```
Infrastructure Layer
  ├── AI Provider 통합
  ├── 로깅 시스템 연동
  └── 설정 관리 완성
```

## 🏗️ 프로젝트 구조

```
/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 애플리케이션 진입점
│   │
│   ├── application/           # 애플리케이션 계층
│   │   ├── __init__.py
│   │   └── book_pipeline_api.py
│   │
│   ├── domain/               # 도메인 계층
│   │   ├── __init__.py
│   │   ├── pipeline/         # 파이프라인 도메인
│   │   │   ├── __init__.py
│   │   │   ├── models.py     # PipelineResult, PipelineStage
│   │   │   └── orchestrator.py # PipelineOrchestrator
│   │   │
│   │   ├── chapter/          # 장 관리 도메인
│   │   │   ├── __init__.py
│   │   │   ├── models.py     # ChapterWorkspace, ChapterInfo
│   │   │   └── services.py   # ChapterIntegrationService
│   │   │
│   │   ├── toc/             # 목차 관리 도메인
│   │   │   ├── __init__.py
│   │   │   ├── models.py     # TOCItem
│   │   │   ├── extractor.py  # TOCExtractor
│   │   │   └── generator.py  # EnhancedTOCGenerator
│   │   │
│   │   └── document/        # 문서 처리 도메인
│   │       ├── __init__.py
│   │       ├── models.py     # NodeDocument
│   │       ├── processor.py  # NodeDocumentProcessor
│   │       └── integrator.py # DocumentIntegrator
│   │
│   ├── infrastructure/       # 인프라스트럭처 계층
│   │   ├── __init__.py
│   │   ├── ai/              # AI 프로바이더
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # AIProvider 인터페이스
│   │   │   ├── claude_sdk.py # ClaudeSDKProvider
│   │   │   └── prompt_manager.py # PromptManager
│   │   │
│   │   ├── logging/         # 로깅 시스템
│   │   │   ├── __init__.py
│   │   │   └── service.py   # LoggingService
│   │   │
│   │   └── filesystem/      # 파일 시스템
│   │       ├── __init__.py
│   │       └── manager.py   # FileSystemManager
│   │
│   ├── config/              # 설정 관리
│   │   ├── __init__.py
│   │   ├── ai_config.py     # AI 설정 클래스
│   │   └── settings.py      # 전역 설정
│   │
│   └── refactoring_logger.py # 기존 RefactoringLogger
│
├── tests/                   # 테스트 코드
│   ├── __init__.py
│   ├── conftest.py          # pytest 설정
│   ├── test_data/           # 테스트 데이터
│   │   ├── sample.pdf
│   │   └── expected_results/
│   │
│   ├── unit/                # 단위 테스트
│   │   ├── test_toc_extractor.py
│   │   ├── test_chapter_workspace.py
│   │   ├── test_node_processor.py
│   │   └── test_orchestrator.py
│   │
│   ├── integration/         # 통합 테스트
│   │   ├── test_pipeline_integration.py
│   │   └── test_ai_provider_integration.py
│   │
│   └── characterization/    # 특성화 테스트
│       ├── test_existing_behavior.py
│       └── golden_master/
│           ├── stage_1_results.json
│           ├── stage_2_results.json
│           ├── stage_3_results.json
│           └── stage_4_results.json
│
├── prompts/                 # 외부화된 프롬프트
│   ├── system_prompts.yaml
│   ├── chapter_analysis.yaml
│   ├── content_processing.yaml
│   └── toc_generation.yaml
│
├── config/                  # 설정 파일
│   ├── ai_config.yaml       # AI 설정 템플릿
│   └── logging_config.yaml  # 로깅 설정
│
├── docs/                    # 문서화
│   ├── api_reference.md
│   ├── domain_models.md
│   └── deployment_guide.md
│
├── scripts/                 # 유틸리티 스크립트
│   ├── run_characterization_tests.py
│   ├── generate_golden_master.py
│   └── migrate_from_v3.py
│
├── requirements.txt         # Python 의존성
├── pyproject.toml          # uv 설정
├── pytest.ini             # pytest 설정
└── README.md              # 프로젝트 개요
```

## 🔧 핵심 인터페이스 정의

### AI Provider 인터페이스
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class AIProvider(ABC):
    """AI 프로바이더 기본 인터페이스"""
    
    @abstractmethod
    async def analyze_content(
        self, 
        content: str, 
        system_prompt_key: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """콘텐츠 분석 수행"""
        pass
    
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """응답 생성"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """프로바이더 사용 가능 여부 확인"""
        pass
```

### 도메인 서비스 인터페이스
```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class DomainService(Generic[T], ABC):
    """도메인 서비스 기본 인터페이스"""
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> T:
        """도메인 서비스 실행"""
        pass
    
    @abstractmethod
    def validate_input(self, *args, **kwargs) -> bool:
        """입력 검증"""
        pass
```

## 📝 TDD 구현 패턴

### 특성화 테스트 패턴
```python
class TestExistingBehavior:
    """기존 동작을 캡처하는 특성화 테스트"""
    
    def test_complete_pipeline_golden_master(self, sample_pdf):
        """전체 파이프라인의 기존 동작 캡처"""
        # Given: 실제 PDF 파일
        old_pipeline = BookPipelineV3()
        
        # When: 기존 파이프라인 실행
        result = old_pipeline.execute(sample_pdf)
        
        # Then: 결과를 골든 마스터로 저장
        self.save_golden_master('complete_pipeline', result)
        
    def test_stage_by_stage_comparison(self, sample_pdf):
        """단계별 결과 비교"""
        old_pipeline = BookPipelineV3()
        
        # 각 단계별 결과 캡처
        stage_1_result = old_pipeline.prepare_chapter_workspace(sample_pdf)
        stage_2_result = old_pipeline.integrate_chapter_information_sequentially(...)
        stage_3_result = old_pipeline.process_node_documents(...)
        stage_4_result = old_pipeline.generate_enhanced_toc(...)
        
        # 골든 마스터 저장
        self.save_stage_results(stage_1_result, stage_2_result, 
                               stage_3_result, stage_4_result)
```

### 점진적 교체 패턴
```python
class TestGradualMigration:
    """점진적 이행 테스트"""
    
    def test_toc_extractor_equivalence(self, sample_pdf):
        """TOCExtractor가 기존 동작과 동일한지 검증"""
        # Given
        old_way = extract_toc_old_way(sample_pdf)
        new_extractor = TOCExtractor()
        
        # When
        new_way = new_extractor.extract_toc(sample_pdf)
        
        # Then: 비즈니스 결과가 동일해야 함
        assert_business_results_equivalent(new_way, old_way)
        
    def test_chapter_workspace_equivalence(self, sample_pdf):
        """ChapterWorkspace가 기존 동작과 동일한지 검증"""
        # 유사한 패턴으로 각 컴포넌트 검증
        pass
```

## 🚀 구현 시퀀스

### Day 1-2: TOC Domain 구현
1. **TOCExtractor 추출**
   ```bash
   # 1. 인터페이스 정의
   touch src/domain/toc/extractor.py
   
   # 2. 기존 코드에서 extract_toc 로직 추출
   # 3. PyMuPDF 의존성 분리
   # 4. 단위 테스트 작성
   ```

2. **EnhancedTOCGenerator 추출**
   ```bash
   # 1. 생성기 클래스 정의
   touch src/domain/toc/generator.py
   
   # 2. AI Provider 의존성 주입
   # 3. 프롬프트 외부화
   ```

### Day 3-4: Chapter Domain 구현
1. **ChapterWorkspace 모델 정의**
2. **ChapterIntegrationService 구현**
3. **파일 시스템 의존성 분리**

### Day 5-6: Document Domain 구현
1. **NodeDocumentProcessor 추출**
2. **배치 처리 로직 최적화**
3. **DocumentIntegrator 구현**

### Day 7-8: Pipeline Orchestration
1. **PipelineOrchestrator 구현**
2. **단계별 실행 흐름 정의**
3. **오류 처리 및 롤백 로직**

## ⚠️ 주의사항

### 리팩토링 중 반드시 지킬 것
1. **한 번에 하나씩**: 여러 컴포넌트 동시 추출 금지
2. **테스트 우선**: 추출 전 반드시 특성화 테스트 작성
3. **비즈니스 로직 보존**: 사용자 관점 결과물 동일 유지
4. **RefactoringLogger 활용**: 모든 변경사항 로그 기록

### 위험 요소 및 대응
- **AI API 의존성**: 네트워크 오류, 비용 초과 → 재시도 로직, 비용 모니터링
- **복잡한 상호작용**: 도메인 간 coupling → 인터페이스 명확 정의
- **파일 시스템 권한**: 경로 문제 → 절대 경로 사용, 권한 확인

### 성공 기준
- [ ] 모든 특성화 테스트 통과
- [ ] 코드 커버리지 85% 이상
- [ ] 성능 저하 없음 (기존 대비 ±10% 이내)
- [ ] RefactoringLogger를 통한 변경사항 추적 완료