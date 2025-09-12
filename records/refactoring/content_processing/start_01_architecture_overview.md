# ContentProcessingStage 아키텍처 개요

## 1. 개요 및 목적

### 1.1 ContentProcessingStage의 역할
- 통합 문서들의 내용 섹션을 기반으로 추출 섹션 자동 생성
- 의존성 기반 문서 처리 순서 보장 (리프 노드 우선, level별 처리)
- 부모-자식 노드 간 내용 동기화 및 일관성 유지
- 개선된 장 목차 MD 파일 생성

### 1.2 파이프라인 내 위치 및 연동
- 3단계: content_processing (핵심 가공 작업)
- 이전 단계: information_integration (통합 노드 정보 문서 생성)
- 다음 단계: toc_generation (최종 목차 생성)

### 1.3 핵심 가치 제안
- 5가지 정보 타입 자동 추출 (핵심 내용, 상세 핵심 내용, 상세 정보, 주요 화제, 부차 화제)
- 구조화된 지식 체계 구축
- 일관된 품질의 콘텐츠 가공

## 2. 전체 아키텍처

### 2.1 시스템 구성도
```
ContentProcessingStage
├── 문서 로딩 및 정렬
├── 그룹별 병렬 처리
├── 단일 문서 처리
│   ├── 추출 작업 (generate_extract_section)
│   ├── 현재 노드 업데이트 (update_current_extraction_section)
│   └── 구성 노드 업데이트 (update_composition_extraction_sections)
└── 개선된 목차 생성
```

### 2.2 처리 흐름 다이어그램
```
1. 책 폴더 경로 입력
   ↓
2. 통합 문서들 로드 및 파싱
   ↓
3. 문서 정렬 (리프 노드 → 비리프 노드(level 내림차순))
   ↓
4. 그룹별 처리
   ├── 리프 노드 그룹: 병렬 추출 작업
   └── 비리프 노드 그룹: 추출 → 구성 노드 반영 → 자식 노드 업데이트
   ↓
5. 개선된 장 목차 MD 파일 생성
   ↓
6. {success: bool, error: Optional[str]} 반환
```

### 2.3 의존성 관계도
- ai_service_v4.py: AI 호출 레이어
- engines_v5.py: 기존 검증된 프롬프트 및 파싱 로직 활용
- config/*.yaml: AI 설정 및 파이프라인 설정

## 3. 핵심 컴포넌트

### 3.1 ContentProcessingStage (메인 클래스)
```python
class ContentProcessingStage:
    def __init__(self, config: Dict, ai_service: AIService)
    
    # 메인 처리 로직
    async def process(self, book_folder_path: str) -> Dict
    
    # 문서 정렬
    async def load_and_sort_documents(self, book_folder_path: str) -> List[List[Dict]]
    
    # 그룹별 처리
    async def process_document_groups(self, sorted_groups: List[List[Dict]])
    
    # 단일 문서 처리  
    async def process_single_document(self, doc: Dict) -> Dict
    
    # 가공 로직들
    async def generate_extract_section(self, doc: Dict) -> Dict
    async def update_current_extraction_section(self, doc: Dict, extraction: Dict)
    async def update_composition_extraction_sections(self, doc: Dict, parent_extraction: Dict)
    
    # 파일 조작
    async def parse_unified_document(self, file_path: str) -> Optional[Dict]
    async def update_extraction_section(self, file_path: str, content: str)
    async def add_update_status_mark(self, file_path: str, status_mark: str)
    async def generate_enhanced_toc_file(self, book_folder_path: str)
```

### 3.2 ContentProcessingUtils (유틸리티)
```python
def extract_level_from_filename(filename: str) -> int
def parse_extraction_response(response: str) -> Dict[str, str]  
def format_composition_info(composition_files: List[str], base_dir: str) -> str
def clean_section_content(content: str, header: str) -> str
def find_matching_document(docs: List[Dict], toc_item: Dict) -> Optional[Dict]
```

### 3.3 외부 의존성
- AIService (ai_service_v4.py): query_single_request() 메서드 활용
- 설정 파일: ai_config.yaml, pipeline_config.yaml
- 기존 로직 참조: engines_v5.py 프롬프트 패턴

## 4. 입출력 정의

### 4.1 입력 규격
- **book_folder_path** (str): 책 챕터 폴더의 절대 경로
- 필수 하위 구조:
  - `unified_info_docs/`: 통합 문서들
  - `{chapter_name}_toc.json`: 목차 구조 파일

### 4.2 출력 규격
```python
{
    "success": bool,      # 처리 성공 여부
    "error": Optional[str] # 오류 메시지 (실패 시)
}
```

### 4.3 중간 데이터 구조
```python
# 문서 데이터 구조
doc_data = {
    'file_path': str,
    'title': str,
    'level': int,
    'extraction_section': str,
    'content_section': str,
    'composition_files': List[str]  # 구성 노드 파일명들
}

# 추출 결과 구조  
extraction_result = {
    'core_content': str,
    'detailed_core_content': str, 
    'detailed_content': str,
    'main_topics': str,
    'sub_topics': str
}
```

## 5. 성능 및 확장성 고려사항

### 5.1 병렬 처리 전략
- 그룹 내 문서들 병렬 처리 (최대 4개 동시)
- 세마포어를 통한 동시성 제어
- 의존성 순서 보장 (리프 노드 → 부모 노드)

### 5.2 fallback 및 재시도 로직
- AI 작업 실패 시 최대 3회 재시도
- 단계별 독립적 재시도 메커니즘
- 부분 실패 시 오류 격리

### 5.3 확장 포인트
- processing_mode: unified_type_processing, individual_type_processing
- AI 제공자 교체 가능한 추상화 레이어
- 새로운 정보 타입 추가 지원