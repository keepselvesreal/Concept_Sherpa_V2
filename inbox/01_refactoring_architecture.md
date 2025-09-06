# 책 파이프라인 리팩토링 아키텍처 가이드

## 🎯 리팩토링 목표

### 현재 상태
- **book_pipeline_v3.py**: 1000줄 단일 파일
- **강한 결합**: 모든 로직이 하나의 클래스에 집중
- **테스트 어려움**: Mock 없이는 테스트 불가
- **확장성 부족**: 새 기능 추가 시 전체 영향

### 목표 상태
- **도메인별 모듈 분리**: 관심사 분리 원칙 적용
- **인터페이스 기반 설계**: 느슨한 결합 달성
- **TDD 친화적 구조**: 각 도메인별 독립 테스트
- **사용자 기능 확장**: 장 선택 기능 추가

## 🏗️ 도메인 주도 아키텍처

### 전체 시스템 아키텍처 다이어그램
```
                        ┌─────────────────┐
                        │  Application    │
                        │     Layer       │
                        │ BookPipelineAPI │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │   Pipeline      │
                        │  Orchestrator   │
                        │  (Domain Svc)   │
                        └────────┬────────┘
                                 │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
    ┌─────▼──────┐    ┌────────▼────────┐    ┌──────▼──────┐
    │ Chapter    │    │    Document     │    │    TOC      │
    │ Domain     │    │    Domain       │    │   Domain    │
    │            │    │                 │    │             │
    │┌──────────┐│    │┌──────────────┐ │    │┌──────────┐ │
    ││Workspace ││    ││NodeProcessor │ │    ││Extractor │ │
    │└──────────┘│    │└──────────────┘ │    │└──────────┘ │
    │┌──────────┐│    │┌──────────────┐ │    │┌──────────┐ │
    ││Integration││   ││DocumentInteg││    ││EnhancedTOC││
    │└──────────┘│    │└──────────────┘ │    │└──────────┘ │
    └─────┬──────┘    └────────┬────────┘    └──────┬──────┘
          │                    │                    │
          └─────────────────────┼─────────────────────┘
                               │
               ┌───────────────▼───────────────┐
               │     Infrastructure Layer     │
               │ ┌─────────┐ ┌─────────────┐  │
               │ │Logging  │ │AI Providers │  │
               │ │Service  │ │   Claude    │  │
               │ └─────────┘ │   Gemini    │  │
               │ ┌─────────┐ └─────────────┘  │
               │ │FileSystem│ ┌─────────────┐ │
               │ │Manager  │ │Prompt       │  │
               │ └─────────┘ │Manager      │  │
               │             └─────────────┘  │
               └───────────────────────────────┘
```

### 도메인별 상세 구조

#### 1. Pipeline Domain (파이프라인 오케스트레이션)
```
Pipeline Domain
├── Models
│   ├── PipelineResult (값 객체)
│   │   ├── is_success: bool
│   │   ├── step_completed: int  
│   │   ├── progress_percent: float
│   │   └── data: Dict[str, Any]
│   └── PipelineStage (열거형)
│       ├── WORKSPACE_PREP
│       ├── CHAPTER_INTEGRATION
│       ├── NODE_PROCESSING
│       └── ENHANCED_TOC
└── Services
    └── PipelineOrchestrator (도메인 서비스)
        ├── execute(pdf_path, selected_chapters) → PipelineResult
        ├── _execute_stage_1() → WorkspaceResult
        ├── _execute_stage_2() → IntegrationResult  
        ├── _execute_stage_3() → ProcessingResult
        └── _execute_stage_4() → TOCResult
```

#### 2. Chapter Domain (장 관리)
```
Chapter Domain
├── Models
│   ├── ChapterWorkspace (애그리게이트 루트)
│   │   ├── book_title: str
│   │   ├── normalized_title: str
│   │   ├── output_directory: Path
│   │   └── chapters: List[ChapterInfo]
│   ├── ChapterInfo (엔티티)
│   │   ├── chapter_number: int
│   │   ├── title: str
│   │   ├── folder_path: str
│   │   ├── page_range: str
│   │   └── content_file: str
│   └── WorkspaceResult (값 객체)
│       ├── success: bool
│       ├── created_folders: List[Dict]
│       └── total_chapters: int
└── Services
    └── ChapterIntegrationService (도메인 서비스)
        ├── integrate_chapters_sequentially()
        └── integrate_single_chapter()
```

#### 3. TOC Domain (목차 관리)
```
TOC Domain
├── Models
│   ├── TOCItem (엔티티)
│   │   ├── id: int
│   │   ├── title: str
│   │   ├── level: int
│   │   ├── start_page: int
│   │   └── end_page: int
│   └── TOCResult (값 객체)
│       ├── success: bool
│       ├── toc_items: List[TOCItem]
│       └── extraction_info: Dict
└── Services
    ├── TOCExtractor (도메인 서비스)
    │   ├── extract_toc(pdf_path) → TOCResult
    │   ├── _extract_raw_toc_with_pymupdf()
    │   ├── _process_toc_items()
    │   └── _calculate_page_ranges()
    └── EnhancedTOCGenerator (도메인 서비스)
        └── generate_enhanced_toc() → str
```

#### 4. Document Domain (문서 처리)
```
Document Domain
├── Models
│   ├── NodeDocument (엔티티)
│   │   ├── node_id: str
│   │   ├── content: str
│   │   ├── metadata: Dict
│   │   └── processing_status: str
│   └── ProcessingResult (값 객체)
│       ├── success: bool
│       ├── processed_nodes: int
│       └── processing_results: List[Dict]
└── Services
    ├── NodeDocumentProcessor (도메인 서비스)
    │   ├── process_chapter() → ProcessingResult
    │   ├── _generate_node_documents()
    │   ├── _analyze_content_nodes()
    │   └── _process_with_unified_processor()
    └── DocumentIntegrator (도메인 서비스)
        └── integrate_documents_for_chapter()
```

### 의존성 흐름 다이어그램
```
┌─────────────────┐
│PipelineOrchestra│
│                 │
└─────────┬───────┘
          │
          ├─────────────────┐
          │                 │
          ▼                 ▼
┌─────────────┐    ┌─────────────┐
│ChapterWork  │    │TOCExtractor │
│space        │    │             │
└─────────────┘    └─────────────┘
          │                 │
          ▼                 ▼
┌─────────────┐    ┌─────────────┐
│ChapterInteg │    │EnhancedTOC  │
│Service      │    │Generator    │
└─────────────┘    └─────────────┘
          │                 │
          ▼                 │
┌─────────────┐             │
│NodeDocument │             │
│Processor    │             │
└─────────────┘             │
          │                 │
          ▼                 │
┌─────────────┐             │
│DocumentInteg│             │
│rator        │             │
└─────────────┘             │
          │                 │
          └─────────────────┘
                    │
                    ▼
          ┌─────────────────┐
          │Infrastructure   │
          │┌───────────────┐│
          ││LoggingService ││
          │└───────────────┘│
          │┌───────────────┐│
          ││AIProvider     ││
          ││(Claude SDK)   ││
          │└───────────────┘│
          │┌───────────────┐│
          ││PromptManager  ││
          │└───────────────┘│
          │┌───────────────┐│
          ││FileSystem     ││
          ││Manager        ││
          │└───────────────┘│
          └─────────────────┘
```

## 🤖 AI 설정 아키텍처

### Claude SDK vs API 통합 설계
```python
# 단일 Provider로 통합
ClaudeSDKProvider(config: AIConfig, prompt_manager: PromptManager)
  ├── system_prompt_key → prompts/system_prompts.yaml
  ├── allowed_tools → 모듈별 최적화
  └── temperature, max_turns → 용도별 설정
```

### 프롬프트 외부화 전략
```
prompts/
├── system_prompts.yaml      # 시스템 프롬프트들
├── chapter_analysis.yaml    # 장 분석 프롬프트
├── content_processing.yaml  # 콘텐츠 처리 프롬프트
└── toc_generation.yaml     # TOC 생성 프롬프트
```

## 🧪 리팩토링 TDD 전략

### 기본 원칙
1. **설계 비전 + 안전한 이행**: 목표 아키텍처 향해 점진적 진행
2. **현재 동작 보존**: 비즈니스 로직 변경 금지
3. **점진적 추출**: 한 번에 하나씩 인터페이스 분리  
4. **실제 데이터 사용**: Mock 최소화, 실패 기반 학습

### TDD 패턴
```python
# 1. 기존 동작 캡처
def test_existing_behavior():
    old_result = BookPipeline().execute("test.pdf")
    # 현재 동작을 테스트로 기록

# 2. 새 인터페이스로 추출
def test_new_interface_matches_old():
    old_result = old_way()
    new_result = new_way()
    assert_business_results_equivalent(new_result, old_result)

# 3. 점진적 이행
def test_gradual_migration():
    # 단계별로 인터페이스 분리하며 검증
```

## 🚨 주의사항

### 리팩토링 시 지켜야 할 것
- **한 번에 하나씩** 변경 - 여러 인터페이스 동시 추출 금지
- **매 단계 테스트 통과** - Green 상태에서만 다음 단계  
- **비즈니스 결과 동일** - 사용자 관점 결과물은 동일 유지
- **RefactoringLogger 활용** - 모든 변경사항 로그 기록

### 위험 요소
- AI API 의존성 (네트워크, 비용)
- 복잡한 도메인 간 상호작용
- 기존 레거시 모듈과의 호환성
- 파일 시스템 권한 및 경로 문제