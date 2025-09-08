# 프로젝트 구조 및 파일 배치

## 새로 생성할 파일들

### 서비스 레이어
```
refactoring/src/services/
└── query_answering_service.py    # 메인 서비스 클래스
    ├── QueryAnsweringService      # 메인 서비스 클래스
    ├── answer_query()             # 메인 API 메서드
    ├── _process_chapter_based_response()   # chapter_based_response 처리
    ├── _process_section_based_response()   # section_based_response 처리
    ├── _synthesize_chapter_based_answers() # 장 기반 답변 종합
    └── _synthesize_section_based_answers() # 섹션 기반 답변 종합
```

### 컴포넌트 레이어
```
refactoring/src/components/
├── chapter_selector.py           # AI 기반 장 선택
│   ├── ChapterSelector
│   ├── select_chapters()         # JSON 파싱 재시도 포함
│   ├── _call_ai_with_retry()     # 3회 재시도 로직
│   └── _format_toc_for_ai()      # 목차 포맷팅
│
├── section_selector.py           # AI 기반 섹션 선택  
│   ├── SectionSelector
│   ├── select_sections()         # JSON 파싱 재시도 포함
│   ├── _call_ai_with_retry()     # 3회 재시도 로직
│   └── _format_chapter_toc_for_ai() # 장 목차 포맷팅
│
├── parallel_answer_generator.py  # 병렬 답변 생성
│   ├── ParallelAnswerGenerator
│   ├── generate_chapter_based_answers_parallel()  # 장 기반 병렬 처리
│   ├── generate_section_based_answers_parallel()  # 섹션 기반 병렬 처리
│   ├── _generate_chapter_answer() # 개별 장 답변 생성 (재시도 포함)
│   └── _generate_section_answer() # 개별 섹션 답변 생성 (재시도 포함)
│
├── workspace_data_loader.py      # 데이터 로더
│   ├── WorkspaceDataLoader
│   ├── load_book_data()          # 책 데이터 로딩
│   ├── _parse_book_toc()         # 책 목차 파싱
│   └── _load_chapter_data()      # 장별 데이터 로딩
│
└── content_mapper.py             # 파일 매핑
    ├── ContentMapper  
    ├── map_chapter_to_folder()   # 장 제목 → 폴더 매핑
    ├── map_section_to_unified_doc() # 섹션 → unified_info_docs 매핑
    └── _normalize_and_match()    # 정규화 기반 매칭
```

### 설정 파일
```
refactoring/config/
└── query_answering.yaml         # 질의 응답 서비스 설정
    ├── default_response_mode     # 기본 응답 모드
    ├── max_chapters             # 최대 선택 장 수
    ├── parallel_processing      # 병렬 처리 설정
    ├── retry_settings           # 재시도 설정
    └── json_parsing             # JSON 파싱 설정
```

## 기존 파일 의존성

### 필수 의존성
```
refactoring/src/
├── services/
│   └── ai_service_v4.py         # AI 서비스 (query_single_request 사용)
├── utils/
│   ├── text_utils.py            # 정규화 함수 (normalize_title)
│   ├── config_manager.py        # 설정 관리
│   └── logger_v2.py             # 로깅
└── core/
    └── base/
        └── service_base.py      # 서비스 기본 클래스 (선택사항)
```

### 임포트 구조
```python
# 메인 서비스
from services.ai_service_v4 import AIService
from utils.config_manager import ConfigManager  
from utils.logger_v2 import Logger
from utils.text_utils import normalize_title

# 컴포넌트들
from components.chapter_selector import ChapterSelector
from components.section_selector import SectionSelector
from components.parallel_answer_generator import ParallelAnswerGenerator
from components.workspace_data_loader import WorkspaceDataLoader
from components.content_mapper import ContentMapper
```

## 테스트 파일 구조

### 통합 테스트
```
refactoring/tests/integration/
└── test_query_answering_service.py
    ├── TestQueryAnsweringService
    ├── test_chapter_based_response()    # chapter_based_response 테스트
    ├── test_section_based_response()    # section_based_response 테스트
    ├── test_parallel_processing()       # 병렬 처리 성능 테스트
    └── test_error_scenarios()           # 에러 시나리오 테스트
```

### 단위 테스트
```
refactoring/tests/unit/
├── test_chapter_selector.py
│   ├── test_select_chapters()
│   ├── test_json_parsing_retry()
│   └── test_ai_service_retry()
│
├── test_parallel_answer_generator.py
│   ├── test_parallel_chapter_processing()
│   ├── test_parallel_section_processing()
│   ├── test_semaphore_limiting()
│   └── test_individual_failure_isolation()
│
├── test_workspace_data_loader.py
│   ├── test_load_book_data()
│   ├── test_parse_book_toc()
│   └── test_load_chapter_data()
│
└── test_content_mapper.py
    ├── test_map_chapter_to_folder()
    ├── test_map_section_to_unified_doc()
    └── test_normalize_and_match()
```

### 테스트 데이터
```
refactoring/tests/data/
└── Data_Oriented_Programming/    # 기존 테스트 데이터
    ├── Data_Oriented_Programming_ToC.md
    ├── 1_Complexity_of_object_oriented_programming/
    │   ├── 1_Complexity_of_object_oriented_programming_content.md
    │   ├── 1_Complexity_of_object_oriented_programming_ToC.md
    │   └── unified_info_docs/
    └── ...
```

## 실행 환경 및 배포

### 개발 환경 설정
```bash
# 필요한 패키지 (이미 설치되어 있음)
uv add asyncio  # 병렬 처리
uv add pathlib  # 파일 경로 처리
uv add json     # JSON 파싱

# 기존 의존성 확인
ls refactoring/src/services/ai_service_v4.py
ls refactoring/src/utils/text_utils.py
```

### 설정 파일 배치
```python
# config_manager 초기화 시 자동 로드
config_manager = ConfigManager("refactoring/config/")
query_config = config_manager.get_config('query_answering')
```

## 파일 생성 순서

### 1단계: 기본 구조
1. `config/query_answering.yaml` - 설정 파일
2. `components/workspace_data_loader.py` - 데이터 로더
3. `components/content_mapper.py` - 파일 매핑
4. `services/query_answering_service.py` - 메인 서비스 골격

### 2단계: AI 연동
1. `components/chapter_selector.py` - 장 선택 (재시도 로직 포함)
2. `components/section_selector.py` - 섹션 선택 (재시도 로직 포함)
3. `components/parallel_answer_generator.py` - 병렬 답변 생성

### 3단계: 통합 및 테스트
1. `services/query_answering_service.py` - 완성
2. `tests/integration/test_query_answering_service.py` - 통합 테스트
3. `tests/unit/test_*.py` - 단위 테스트들

## 디렉토리 권한 및 보안
```bash
# 디렉토리 생성
mkdir -p refactoring/src/components
mkdir -p refactoring/config  
mkdir -p refactoring/tests/integration
mkdir -p refactoring/tests/unit

# 권한 설정 (읽기/쓰기)
chmod 755 refactoring/src/components
chmod 644 refactoring/config/query_answering.yaml
```