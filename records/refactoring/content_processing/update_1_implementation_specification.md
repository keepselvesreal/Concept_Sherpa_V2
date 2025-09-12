# ContentProcessingStage 구현 명세서 (업데이트 1)

## 수정된 클래스 설계 명세

### 1.1 ContentProcessingStage 클래스 구조 (수정됨)
```python
class ContentProcessingStage:
    """콘텐츠 가공 단계 - 메모리 기반 통합 문서 처리"""
    
    def __init__(self, config: Dict, ai_service: AIService):
        self.config = config
        self.ai_service = ai_service  
        self.processing_mode = "memory_based_processing"  # 고정값
        self.max_parallel = config.get('max_parallel', 4)
```

### 1.2 수정된 생성자 및 초기화 파라미터
- **processing_mode**: "memory_based_processing" 고정 (기존 구분 제거)
- 파이프라인 간 데이터 전달은 메모리 기반으로만 처리

## 메서드별 상세 명세 (수정사항)

### 2.1 process() - 메인 처리 로직 (수정됨)

#### 2.1.1 수정된 메서드 시그니처
```python
async def process(self, prev_result: Dict, user_output_path: str) -> Dict[str, Any]:
    """
    Args:
        prev_result: 이전 단계 결과 (process_result.json 구조)
        user_output_path: 사용자 지정 저장 경로
    """
```

#### 2.1.2 수정된 처리 단계
1. **메모리 데이터 추출**: `prev_result["documents"]["data"]["unified_documents"]`
2. **문서 로드 및 정렬**: `load_and_sort_documents(unified_documents)` 호출
3. **그룹별 가공 처리**: `process_document_groups(sorted_groups, user_output_path)` 호출
4. **결과 JSON 저장**: `load_and_sort_result.json` 자동 생성

### 2.2 load_and_sort_documents() - 메모리 기반 문서 정렬 (대폭 수정)

#### 2.2.1 수정된 메서드 시그니처
```python
async def load_and_sort_documents(self, unified_documents: List[Dict]) -> List[List[Dict]]:
    """
    Args:
        unified_documents: 메모리상의 문서 데이터 리스트
    Returns:
        sorted_groups: 정렬된 문서 그룹들
    Side Effects:
        - load_and_sort_result.json 생성 (결과 저장)
    """
```

#### 2.2.2 메모리 기반 문서 로딩 로직
```python
documents = []

for doc_data in unified_documents:
    # 파일명에서 정보 추출
    file_name = doc_data["file_name"]
    level = self.extract_level_from_filename(file_name)
    
    # 콘텐츠에서 섹션 파싱
    content = doc_data["content"]
    title = self.extract_title_from_content(content)
    composition_files = self.parse_composition_files(content)
    
    doc_info = {
        'file_name': file_name,
        'title': title,
        'level': level,
        'full_content': content,  # 전체 내용 보존
        'composition_files': composition_files,
        'extraction_section': '',
        'process_status': False
    }
    documents.append(doc_info)
```

### 2.3 process_single_document() - 통합된 처리 로직 (대폭 수정)

#### 2.3.1 수정된 메서드 시그니처
```python
async def process_single_document(self, doc: Dict, user_output_path: str) -> Dict:
    """
    Args:
        doc: 문서 정보
        user_output_path: 사용자 지정 저장 경로
    """
```

#### 2.3.2 통합된 처리 단계
```python
# 1. 모든 노드에서 추출 작업 수행
extraction_result = await self.generate_extract_section(doc)

# 2. 추출 결과를 사용자 지정 경로에 저장 (모든 노드 공통)
await self.save_extraction_result(doc, extraction_result, user_output_path)

# 3. 비리프 노드만 업데이트 과정 진행
if doc.get('composition_files'):
    # 현재 노드 업데이트 (파일에서 읽어서 처리)
    updated_current_extraction, used_composition_extractions = await self.update_current_extraction_section(doc, user_output_path)
    
    # 구성 노드들 업데이트 (파일에서 읽어서 처리)  
    await self.update_composition_extraction_sections(doc, updated_current_extraction, used_composition_extractions, user_output_path)
```

### 2.4 새로 추가된 공통 저장 메서드들

#### 2.4.1 save_extraction_result() - 공통 추출 결과 저장
```python
async def save_extraction_result(self, doc: Dict, extraction_result: Dict, user_output_path: str):
    """
    모든 노드의 추출 결과를 사용자 지정 경로에 저장 (공통 로직)
    
    처리 과정:
    1. 파일 경로 구성 및 디렉터리 생성
    2. 추출 섹션 포맷팅
    3. 기존 문서 내용에 추출 섹션 삽입
    4. 파일 저장
    """
```

#### 2.4.2 save_updated_content_with_marking() - 공통 업데이트 저장
```python
async def save_updated_content_with_marking(self, file_path: str, updated_extraction: Dict, status_mark: str):
    """
    파일 읽기 → 마킹 추가 → 업데이트된 내용 저장 (공통 패턴)
    
    Args:
        file_path: 업데이트할 파일 경로
        updated_extraction: 업데이트된 추출 섹션
        status_mark: 추가할 상태 마킹 ("<구성 노드 반영 완료>" 등)
    
    처리 과정:
    1. 파일에서 기존 내용 읽기
    2. 추출 섹션 업데이트
    3. 상태 마킹 추가
    4. 파일 저장
    """
```

### 2.5 수정된 업데이트 메서드들

#### 2.5.1 update_current_extraction_section() - 파일 기반 현재 노드 업데이트
```python
async def update_current_extraction_section(self, doc: Dict, user_output_path: str) -> Tuple[Dict, str]:
    """
    현재 노드의 추출 섹션 업데이트 (파일에서 읽어서 처리)
    
    Returns:
        Tuple[Dict, str]: (업데이트된_현재_추출_섹션, 사용된_구성_노드들의_결합된_추출_섹션)
    
    처리 과정:
    1. 사용자 지정 경로에서 현재 노드 파일 읽기
    2. 구성 노드들의 추출 섹션 수집 (파일에서 읽기)
    3. engines_v5.py 로직으로 부모 노드 업데이트
    4. save_updated_content_with_marking 호출 (공통 패턴)
    """
```

#### 2.5.2 update_composition_extraction_sections() - 파일 기반 구성 노드 업데이트
```python
async def update_composition_extraction_sections(self, parent_doc: Dict, 
                                               parent_extraction: Dict,
                                               used_composition_extractions: str,
                                               user_output_path: str):
    """
    구성 노드들 업데이트 (파일에서 읽어서 처리)
    
    처리 과정:
    1. 각 구성 노드 파일을 사용자 지정 경로에서 읽기
    2. engines_v5.py 로직으로 핵심 3개 섹션만 업데이트
    3. save_updated_content_with_marking 호출 (공통 패턴)
    """
```

## 중요 구현 포인트 (수정사항)

### 3.1 메모리 기반 데이터 처리
- process_result.json의 unified_documents 필드 직접 활용
- 파일 스캔 없이 메모리에서 문서 정보 추출
- 중간 결과를 load_and_sort_result.json으로 저장

### 3.2 공통 저장 로직 통합
- 모든 파일 저장 작업을 공통 메서드로 통합
- 일관성 있는 상태 마킹 처리
- 오류 처리 및 로깅 통일

### 3.3 명시적 반환값 패턴
```python
# update_current_extraction_section에서 명시적으로 두 값 반환
updated_current_extraction, used_composition_extractions = await self.update_current_extraction_section(...)

# 구성 노드들의 추출 섹션은 단순 텍스트 결합
combined_composition_text = "\n".join([f"=== {comp['title']} ===\n{comp['extraction']}\n" for comp in composition_extractions])
```

### 3.4 engines_v5.py 로직 재사용
- update_parent_extraction_with_composition 프롬프트 패턴 활용
- 구성 노드 정보 수집 방식 재사용
- 주요/부차 화제 보존 로직 적용

## 파일 조작 메서드들 (수정사항)

### 4.1 parse_unified_document_from_path() - 새로 추가
```python
async def parse_unified_document_from_path(self, file_path: str) -> Dict:
    """사용자 지정 경로에서 통합 문서 파싱"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return self.parse_unified_document_content(content)
```

### 4.2 extract_title_from_content() - 새로 추가
```python
def extract_title_from_content(self, content: str) -> str:
    """콘텐츠에서 제목 추출 (# 내용 섹션에서)"""
    content_match = re.search(r'# 내용\n---\n(.*?)(?=\n---|\n#|$)', content, re.DOTALL)
    if content_match:
        first_line = content_match.group(1).split('\n')[0].strip()
        return first_line.replace('#', '').strip()
    return "Unknown Title"
```

### 4.3 기존 메서드들은 경로 기반으로 수정
- update_extraction_section_in_content(): 메모리 내용 기반 업데이트
- add_update_status_mark_to_content(): 메모리 내용 기반 마킹 추가

## 로깅 전략 (업데이트)

### 5.1 메모리 기반 처리 로깅
```python
logger.info(f"📊 메모리에서 {len(unified_documents)}개 문서 로드")
logger.info(f"💾 추출 결과 저장 완료: {output_file_path}")
logger.info(f"🔄 파일에서 읽기 → 업데이트 → 저장: {file_path}")
```

### 5.2 공통 로직 통합 로깅
```python
logger.info(f"💾 업데이트된 내용 저장 완료: {file_path} (마킹: {status_mark})")
logger.info(f"📁 load_and_sort_result.json 저장: {result_path}")
```

### 5.3 성능 및 효율성 로깅
```python
logger.info(f"⚡ 메모리 기반 처리로 파일 I/O {reduction_percentage}% 감소")
logger.info(f"🔄 공통 로직 활용으로 코드 중복 제거")
```