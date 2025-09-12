# ContentProcessingStage 구현 명세서

## 1. 클래스 설계 명세

### 1.1 ContentProcessingStage 클래스 구조
```python
class ContentProcessingStage:
    """콘텐츠 가공 단계 - 통합 문서 처리 및 개선된 목차 생성"""
    
    def __init__(self, config: Dict, ai_service: AIService):
        self.config = config
        self.ai_service = ai_service  
        self.processing_mode = config.get('processing_mode', 'unified_type_processing')
        self.max_parallel = config.get('max_parallel', 4)
```

### 1.2 생성자 및 초기화 파라미터
- **config**: 파이프라인 설정 (ai_config.yaml, pipeline_config.yaml)
- **ai_service**: AIService 인스턴스 (ai_service_v4.py)

### 1.3 인스턴스 변수 정의
- `processing_mode`: "unified_type_processing" 또는 "individual_type_processing"
- `max_parallel`: 병렬 처리 최대 개수 (기본값: 4)

## 2. 메서드별 상세 명세

### 2.1 process() - 메인 처리 로직

#### 2.1.1 메서드 시그니처
```python
async def process(self, book_folder_path: str) -> Dict[str, Any]:
```

#### 2.1.2 처리 단계별 세부 로직
1. **문서 로드 및 정렬**: `load_and_sort_documents()` 호출
2. **그룹별 가공 처리**: `process_document_groups()` 호출  
3. **개선된 장 목차 생성**: `generate_enhanced_toc_file()` 호출

#### 2.1.3 예외 처리 전략
```python
try:
    # 메인 처리 로직
    return {'success': True, 'error': None}
except Exception as e:
    return {'success': False, 'error': str(e)}
```

#### 2.1.4 반환값 구조
```python
{
    "success": bool,      # 처리 성공 여부
    "error": Optional[str] # 오류 메시지 (실패 시만)
}
```

### 2.2 load_and_sort_documents() - 문서 정렬

#### 2.2.1 문서 로딩 로직
```python
# unified_info_docs 디렉터리에서 *_info.md 파일들 검색
for file_path in glob.glob(f"{unified_docs_dir}/*_info.md"):
    doc_data = await self.parse_unified_document(file_path)
    if doc_data:
        documents.append(doc_data)
```

#### 2.2.2 리프/비리프 분리 알고리즘
```python
for doc in documents:
    composition_section = doc.get('composition_section', '').strip()
    if composition_section and composition_section != '---':
        # 구성 노드 파일명들이 있는 경우 (비리프)
        doc['composition_files'] = [line.strip() for line in composition_section.split('\n') 
                                   if line.strip() and not line.startswith('---')]
        non_leaf_nodes.append(doc)
    else:
        # 구성 섹션이 비어있는 경우 (리프)
        doc['composition_files'] = []
        leaf_nodes.append(doc)
```

#### 2.2.3 level별 정렬 규칙
- 비리프 노드들을 level별로 그룹화
- level 내림차순 정렬 (level 큰 것부터 처리)

#### 2.2.4 그룹화 전략
```python
# 최종 정렬된 그룹들
sorted_groups = [leaf_nodes]  # 리프 노드 그룹이 먼저
for level in sorted(level_groups.keys(), reverse=True):
    sorted_groups.append(level_groups[level])

return [group for group in sorted_groups if group]  # 빈 그룹 제거
```

### 2.3 process_document_groups() - 그룹별 처리

#### 2.3.1 병렬 처리 구현 (unified_type_processing)
```python
async def process_group_parallel(self, group: List[Dict]) -> List[Dict]:
    """그룹 내 병렬 처리"""
    semaphore = asyncio.Semaphore(self.max_parallel)
    
    async def process_single_doc(doc):
        async with semaphore:
            return await self.process_single_document(doc)
    
    tasks = [process_single_doc(doc) for doc in group]
    return await asyncio.gather(*tasks)
```

#### 2.3.2 순차 처리 구현 (individual_type_processing)
```python
async def process_group_sequential(self, group: List[Dict]) -> List[Dict]:
    """그룹 내 순차 처리"""
    processed_group = []
    for doc in group:
        processed_doc = await self.process_single_document(doc)
        processed_group.append(processed_doc)
    return processed_group
```

#### 2.3.3 세마포어를 통한 동시성 제어
- `asyncio.Semaphore(self.max_parallel)` 사용
- 최대 4개 동시 처리 제한

#### 2.3.4 진행률 추적
```python
for i, group in enumerate(sorted_groups):
    logging.info(f"🔄 그룹 {i+1}/{len(sorted_groups)} 처리 시작: {len(group)}개 문서")
    # 처리 로직
    logging.info(f"✅ 그룹 {i+1} 처리 완료")
```

### 2.4 process_single_document() - 단일 문서 처리

#### 2.4.1 추출 단계 (extract_section_information)
```python
# 1단계: 내용 섹션 → 추출 섹션 생성
extraction_result = await self.generate_extract_section(doc)
```

#### 2.4.2 업데이트 단계 (update_section_information)
```python
# 2단계: 구성 노드가 있는 경우
if doc.get('composition_files'):
    # 비리프 노드: 구성 노드 반영하여 추출 섹션 업데이트
    await self.update_current_extraction_section(doc, extraction_result)
    # 구성 노드들에도 업데이트된 내용 반영
    await self.update_composition_extraction_sections(doc, extraction_result)
```

#### 2.4.3 상태 추적 및 마킹
- 추출 작업: 상태 마킹 없음 (추출된 내용만 삽입)
- 업데이트 작업: `<구성 노드 반영 완료>`, `<부모 노드 반영 완료>` 마킹

### 2.5 파일 조작 메서드들

#### 2.5.1 parse_unified_document() - 정규표현식 기반 파싱
```python
# 섹션 분리 (# 추출, # 내용, # 구성 기준)
extraction_match = re.search(r'# 추출\n---\n(.*?)(?=\n# 내용\n---|$)', content, re.DOTALL)
content_match = re.search(r'# 내용\n---\n(.*?)(?=\n# 구성\n---|$)', content, re.DOTALL)  
composition_match = re.search(r'# 구성\n---\n(.*?)$', content, re.DOTALL)
```

#### 2.5.2 update_extraction_section() - 섹션별 업데이트
```python
# 추출 섹션 내용을 새 내용으로 교체
pattern = r'(# 추출\n---\n)(<[^>]+>\n)?(.*?)(?=\n# 내용\n---|$)'

def replacement(match):
    header = match.group(1)  # # 추출\n---\n
    status_mark = match.group(2) if match.group(2) else ""  # 기존 상태 마킹
    return f"{header}{status_mark}{new_extraction_content}"

updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
```

#### 2.5.3 add_update_status_mark() - 상태 마킹 규칙
```python
# # 추출\n--- 바로 다음에 상태 마킹 삽입 (줄바꿈 없이)
content = re.sub(
    r'(# 추출\n---\n)',
    f'\\1{status_mark}\n',
    content
)
```

### 2.6 generate_enhanced_toc_file() - 목차 생성

#### 2.6.1 TOC 구조 매칭 로직
```python
# 1. 목차 구조 로드
with open(toc_file, 'r') as f:
    toc_structure = json.load(f)

# 2. 모든 통합 문서 로드 및 매칭
all_docs = {}
for file_path in glob.glob(f"{unified_docs_dir}/*_info.md"):
    doc_data = await self.parse_unified_document(file_path)
    if doc_data and doc_data.get('title'):
        all_docs[doc_data['title']] = doc_data
```

#### 2.6.2 level별 헤더 생성 규칙
```python
# level에 따른 헤더 생성
header_prefix = "#" * toc_item['level']
header = f"{header_prefix} {toc_item['title']}"
```

#### 2.6.3 MD 파일 포맷팅
```python
# 헤더 바로 밑에 줄바꿈 없이 내용 삽입
if extraction_content.strip():
    enhanced_lines.append(f"{header}\n{extraction_content}")
else:
    enhanced_lines.append(f"{header}\n[추출 내용 없음]")

# 각 섹션 사이에 빈 줄 2개 추가 (가독성)
enhanced_lines.append("")
enhanced_lines.append("")
```

## 3. 중요 구현 포인트

### 3.1 상태 마킹 위치 (줄바꿈 없이 삽입)
- 추출 섹션 바로 밑: `# 추출\n---\n<상태마킹>\n내용...`
- 마킹과 내용 사이 줄바꿈 없음

### 3.2 주요/부차 화제 보존 로직
- 구성 노드 업데이트 시 핵심 3개 섹션만 업데이트
- 주요 화제, 부차 화제는 각 노드의 고유 내용으로 보존

### 3.3 의존성 순서 보장
- 리프 노드 → 비리프 노드 순서
- level 큰 것부터 처리 (상위 레벨 우선)

### 3.4 fallback 및 재시도 메커니즘
```python
async def ai_request_with_retry(self, prompt: str, provider_config: Dict, max_retries: int = 3):
    """AI 요청 재시도 로직"""
    for attempt in range(max_retries):
        try:
            response = await self.ai_service.query_single_request(
                provider=provider_config['provider'],
                prompt=prompt
            )
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            logging.warning(f"AI 요청 실패 (시도 {attempt + 1}/{max_retries}): {e}")
            await asyncio.sleep(1)  # 재시도 전 대기
```

### 3.5 로깅 전략
```python
import logging

# 주요 체크포인트
logging.info(f"📊 문서 파싱 완료 - 제목: {doc_data.get('title', 'N/A')}")
logging.info(f"🤖 AI 추출 작업 시작...")
logging.info(f"✅ 추출 작업 완료")
logging.info(f"💾 파일 업데이트 완료")
logging.warning(f"⚠️ AI 요청 실패 (시도 {attempt + 1}/{max_retries}): {e}")
logging.error(f"❌ 처리 실패: {e}")
```