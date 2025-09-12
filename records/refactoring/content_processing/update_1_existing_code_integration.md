# 기존 코드 활용 가이드 (업데이트 1)

## 수정된 engines_v5.py 활용 방법

### 1.1 메모리 기반 데이터 처리에서의 활용

#### 1.1.1 기존 extract_all_info 로직 재사용 (변경사항 없음)
- 프롬프트 패턴 및 응답 파싱 로직 그대로 활용
- ai_service_v4.py 연동 방식 동일하게 사용

#### 1.1.2 수정된 generate_extract_section() 구현
```python
async def generate_extract_section(self, doc: Dict) -> Dict:
    """engines_v5.py extract_all_info 로직 활용 (메모리 기반)"""
    
    # 메모리에서 content_section 추출
    content = self.extract_content_section_from_full_content(doc.get('full_content', ''))
    title = doc.get('title', '')
    
    # engines_v5.py 프롬프트 패턴 동일하게 사용
    prompt = f"""다음 문서에서 5가지 정보를 순서대로 추출해주세요.

문서 제목: {title}
문서 내용:
{content}
[기존과 동일한 프롬프트 패턴]"""
    
    try:
        provider_config = self.config['extract_section_information']
        response = await self.ai_service.query_single_request(
            provider=provider_config['provider'],
            prompt=prompt
        )
        
        # engines_v5.py 파싱 로직 그대로 활용
        sections = self.parse_extraction_response(response)
        
        success_count = sum(1 for content in sections.values() if content.strip() and content.startswith('##'))
        if success_count == 5:
            self.api_calls_counter += 1
            return sections
        else:
            raise Exception("추출 섹션 불완전")
            
    except Exception as e:
        return await self.fallback_extraction(doc)
```

### 1.2 수정된 부모 노드 업데이트 로직

#### 1.2.1 파일 기반 구성 노드 정보 수집 방식 (수정됨)
```python
# 기존: 메모리에서 직접 수집
# 수정: 사용자 지정 경로의 파일에서 수집
async def collect_composition_info_from_files(self, parent_doc: Dict, user_output_path: str):
    """구성 노드들의 내용을 파일에서 수집"""
    composition_info = []
    
    for child_file in parent_doc['composition_files']:
        child_path = os.path.join(user_output_path, child_file)
        
        if os.path.exists(child_path):
            # 파일에서 구성 노드 문서 파싱
            child_doc = await self.parse_unified_document_from_path(child_path)
            child_sections = self.parse_extraction_section(child_doc['extraction_section'])
            
            # engines_v5.py와 동일한 정보 수집 방식
            core_content = child_sections.get('core_content', '').replace('## 핵심 내용', '').strip()
            detailed_core = child_sections.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
            detailed_info = child_sections.get('detailed_content', '').replace('## 상세 정보', '').strip()
            main_topics = child_sections.get('main_topics', '').replace('## 주요 화제', '').strip()
            sub_topics = child_sections.get('sub_topics', '').replace('## 부차 화제', '').strip()
            
            child_info = f"""
구성노드 ({child_doc['title']}):
- 핵심 내용: {core_content}
- 상세 핵심 내용: {detailed_core}
- 상세 정보: {detailed_info}
- 주요 화제: {main_topics}
- 부차 화제: {sub_topics}"""
            
            composition_info.append(child_info)
    
    return composition_info
```

#### 1.2.2 수정된 부모 노드 업데이트 프롬프트 (engines_v5.py 패턴 재사용)
```python
async def update_parent_with_composition_logic(self, current_doc: Dict, current_extraction: Dict, composition_extractions: List[Dict]) -> Dict:
    """engines_v5.py의 update_parent_extraction_with_composition 로직 활용"""
    
    # 현재 추출 섹션 파싱
    parent_core = current_extraction.get('core_content', '').replace('## 핵심 내용', '').strip()
    parent_detailed_core = current_extraction.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
    # ... 나머지 섹션들
    
    # 구성 정보 포맷팅 (engines_v5.py와 동일)
    composition_info = []
    for comp in composition_extractions:
        comp_sections = self.parse_extraction_section(comp['extraction'])
        # engines_v5.py와 동일한 child_info 구조 생성
        # ...
    
    # engines_v5.py 프롬프트 패턴 그대로 사용
    prompt = f"""다음은 부모 노드의 추출 섹션을 구성 노드들의 내용을 반영하여 업데이트하는 작업입니다.

**부모 노드 ({current_doc['title']})의 현재 내용:**
핵심 내용: {parent_core}
상세 핵심 내용: {parent_detailed_core}
상세 정보: {parent_detailed_info}
주요 화제: {parent_main_topics}
부차 화제: {parent_sub_topics}

**구성 노드들의 내용:**
{chr(10).join(composition_info)}

부모 노드의 각 섹션을 구성 노드들의 내용을 종합적으로 반영하여 개선해주세요. 
부모 노드는 전체적인 개요와 통합적인 관점을 제공하되, 구성 노드들의 세부 내용이 잘 반영되도록 해주세요.
[engines_v5.py와 동일한 프롬프트 패턴]"""
    
    # API 호출 및 파싱 (engines_v5.py와 동일)
    system_prompt = """문서 통합 전문가. 부모-구성 노드 관계를 이해하고 구성 노드들의 세부 내용을 종합하여 부모 노드의 각 섹션을 개선하세요."""
    
    response = await self.ai_service.query_single_request(provider="gemini", prompt=prompt)
    return self.parse_extraction_response(response)
```

### 1.3 수정된 구성 노드 업데이트 로직

#### 1.3.1 파일 기반 구성 노드 업데이트 (수정됨)
```python
async def update_composition_node_core_sections(self, comp_doc: Dict, parent_extraction: Dict, used_composition_extractions: str) -> Dict:
    """engines_v5.py의 update_composition_extractions 로직 활용"""
    
    # 부모 노드 정보 추출 (engines_v5.py와 동일)
    parent_core = parent_extraction.get('core_content', '').replace('## 핵심 내용', '').strip()
    parent_detailed_core = parent_extraction.get('detailed_core_content', '').replace('## 상세 핵심 내용', '').strip()
    parent_detailed_info = parent_extraction.get('detailed_content', '').replace('## 상세 정보', '').strip()
    parent_main_topics = parent_extraction.get('main_topics', '').replace('## 주요 화제', '').strip()
    parent_sub_topics = parent_extraction.get('sub_topics', '').replace('## 부차 화제', '').strip()
    
    # 구성 노드 현재 내용 추출
    comp_sections = self.parse_extraction_section(comp_doc.get('extraction_section', ''))
    comp_core = comp_sections.get('core_content', '').replace('## 핵심 내용', '').strip()
    # ... 나머지 섹션들
    
    # engines_v5.py 프롬프트 패턴 사용
    prompt = f"""다음은 부모 노드의 업데이트된 내용을 바탕으로 구성 노드들의 추출 섹션을 개선하는 작업입니다.

**부모 노드 ({parent_doc['title']})의 업데이트된 내용:**
핵심 내용: {parent_core}
상세 핵심 내용: {parent_detailed_core}
상세 정보: {parent_detailed_info}
주요 화제: {parent_main_topics}
부차 화제: {parent_sub_topics}

**구성 노드 ({comp_doc['title']})의 현재 내용:**
핵심 내용: {comp_core}
상세 핵심 내용: {comp_detailed_core}
상세 정보: {comp_detailed_info}

부모 노드의 업데이트된 내용을 반영하여 구성 노드의 추출 섹션을 개선해주세요.
구성 노드의 고유한 특성은 유지하되, 부모와의 일관성과 연결성을 반영해주세요.
[engines_v5.py와 동일한 프롬프트]"""
    
    response = await self.ai_service.query_single_request(provider="gemini", prompt=prompt)
    parsed_response = self.parse_extraction_response(response)
    
    # 주요/부차 화제 보존 (engines_v5.py 로직)
    preserved_sections = {
        'core_content': parsed_response.get('core_content', comp_sections.get('core_content', '')),
        'detailed_core_content': parsed_response.get('detailed_core_content', comp_sections.get('detailed_core_content', '')),
        'detailed_content': parsed_response.get('detailed_content', comp_sections.get('detailed_content', '')),
        'main_topics': comp_sections.get('main_topics', ''),  # 보존
        'sub_topics': comp_sections.get('sub_topics', '')    # 보존
    }
    
    return preserved_sections
```

## 2. 수정된 ai_service_v4.py 활용

### 2.1 메모리 기반 데이터와 연동 (변경사항 없음)
- query_single_request() 메서드 사용법 동일
- provider 설정 및 예외 처리 방식 그대로 활용

### 2.2 수정된 API 호출 패턴
```python
# 메모리 데이터 활용한 AI 호출
async def generate_extract_section(self, doc: Dict) -> Dict:
    content = self.extract_content_section_from_full_content(doc.get('full_content', ''))
    title = doc.get('title', '')
    
    # ai_service_v4.py 활용 (기존과 동일)
    provider_config = self.config['extract_section_information']
    response = await self.ai_service.query_single_request(
        provider=provider_config['provider'],
        prompt=prompt
    )
    return response
```

## 3. 수정된 통합 시 주의사항

### 3.1 메모리 기반 데이터 처리
```python
class ContentProcessingStage:
    def __init__(self, config, ai_service):
        self.api_calls_counter = 0
        self.memory_cache = {}  # 메모리 기반 캐싱 추가
        
    def extract_content_section_from_full_content(self, full_content: str) -> str:
        """전체 내용에서 # 내용 섹션만 추출"""
        content_match = re.search(r'# 내용\n---\n(.*?)(?=\n# 구성\n---|$)', full_content, re.DOTALL)
        return content_match.group(1).strip() if content_match else ""
```

### 3.2 파일 기반 업데이트 처리
```python
async def parse_unified_document_from_path(self, file_path: str) -> Optional[Dict]:
    """사용자 지정 경로에서 통합 문서 파싱 (새로 추가)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse_unified_document_content(content)
    except Exception as e:
        logging.error(f"파일 파싱 실패: {file_path} - {e}")
        return None
```

### 3.3 공통 로직 통합 검증
```python
def validate_extraction_response(self, sections: Dict[str, str]) -> bool:
    """engines_v5.py와 동일한 검증 로직"""
    required_sections = ['core_content', 'detailed_core_content', 'detailed_content']
    for section in required_sections:
        if not sections.get(section, '').strip():
            return False
    
    # 헤더 포함 여부 확인
    for section_content in sections.values():
        if not section_content.startswith('##'):
            return False
    
    return True
```

### 3.4 수정된 fallback 전략
```python
async def fallback_extraction(self, doc: Dict) -> Dict:
    """메모리 기반 fallback 처리"""
    
    content = self.extract_content_section_from_full_content(doc.get('full_content', ''))
    title = doc.get('title', '')
    
    simplified_prompt = f"""다음 문서의 핵심 내용을 간단히 추출해주세요:
    
제목: {title}
내용: {content}
[engines_v5.py와 동일한 fallback 프롬프트]"""
    
    # 3회 재시도 로직 (engines_v5.py와 동일)
    for attempt in range(3):
        try:
            self.api_calls_counter += 1
            response = await self.ai_service.query_single_request(
                provider="gemini",
                prompt=simplified_prompt
            )
            
            sections = self.parse_extraction_response(response)
            success_count = sum(1 for content in sections.values() if content.strip() and content.startswith('##'))
            
            if success_count == 5:
                return sections
            elif attempt == 2:
                # 기본 구조라도 반환 (engines_v5.py와 동일)
                return self.generate_basic_structure(response)
                
        except Exception as e:
            if attempt == 2:
                raise
            await asyncio.sleep(1)
```

## 4. 수정된 코드 이식 체크리스트

### 4.1 메모리 기반 처리 수정 포인트
- [x] process_result.json 구조 파싱 로직 구현
- [x] 메모리 데이터에서 문서 정보 추출 로직 구현  
- [x] 사용자 지정 경로 기반 파일 저장 로직 구현
- [x] 공통 저장 로직 통합 구현

### 4.2 기존 로직 재사용 포인트 (변경사항 없음)
- [x] engines_v5.py 프롬프트 패턴 복사
- [x] 응답 파싱 로직 이식
- [x] ai_service_v4.py 호출 방식 적용
- [x] 재시도 로직 구현
- [x] 상태 마킹 로직 이식

### 4.3 새로운 개선 사항
- [x] 파일 기반 구성 노드 처리 로직 구현
- [x] 명시적 반환값 패턴 구현
- [x] 공통 업데이트 저장 메서드 구현

### 4.4 테스트 검증 방법 (수정됨)
- [x] 메모리 데이터 처리 동작 확인
- [x] 사용자 지정 경로 저장 결과 확인
- [x] engines_v5.py와 동일한 결과 생성 확인
- [x] 상태 마킹 위치 정확성 검증
- [x] 주요/부차 화제 보존 확인
- [x] 공통 로직 동작 확인