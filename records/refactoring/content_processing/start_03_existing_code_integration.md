# 기존 코드 활용 가이드

## 1. engines_v5.py 활용

### 1.1 extract_all_info 로직 재사용

#### 1.1.1 프롬프트 패턴 (라인 37-64)

**5개 섹션 추출 구조**:
```python
prompt = f"""다음 문서에서 5가지 정보를 순서대로 추출해주세요.

문서 제목: {title}
문서 내용:
{content}

다음 순서로 각 정보를 추출하고, 반드시 다음 형식을 정확히 지켜서 출력해주세요:

## 핵심 내용
문서의 핵심 내용을 2-3문장으로 간결하게 요약

## 상세 핵심 내용
주요 개념과 중요한 세부사항을 포함하여 5-7문장으로 정리

## 상세 정보
문서의 모든 중요한 정보를 빠뜨리지 않고 체계적으로 정리

## 주요 화제
문서에서 다루는 핵심 주제들을 불렛 포인트로 나열

## 부차 화제
주요 주제 외에 언급되는 부차적인 주제들을 불렛 포인트로 나열

**중요 규칙**: 
1. 각 섹션 제목(## 핵심 내용, ## 상세 핵심 내용 등)을 한 번만 출력하고 바로 다음 줄에 내용을 작성하세요.
2. 빈 헤더 라인을 출력하지 마세요.
3. 섹션 내용을 작성할 때 헤더가 필요한 경우에는 반드시 ### (해시 3개) 이상의 헤더만 사용하세요.
4. ## 헤더는 섹션 제목과 구분하기 위해 절대 중복 사용하지 마세요."""

system_prompt = """문서 분석 전문가. 주어진 5가지 정보 타입을 순서대로 정확하게 추출하세요.
- 핵심 내용: 간결하고 정확한 요약
- 상세 핵심 내용: 상세하면서도 핵심적인 내용
- 상세 정보: 체계적이고 포괄적인 정리
- 주요 화제: 핵심 주제들
- 부차 화제: 부차적이지만 의미있는 주제들

정확한 형식을 지켜서 출력하세요."""
```

#### 1.1.2 응답 파싱 로직 (라인 120-150)

**섹션 분리 알고리즘**:
```python
def parse_extraction_response(self, response: str) -> Dict[str, str]:
    """AI 응답을 5개 섹션으로 파싱"""
    sections = {
        'core_content': '',
        'detailed_core_content': '',
        'detailed_content': '',
        'main_topics': '',
        'sub_topics': ''
    }
    
    # 섹션 헤더 매핑
    section_headers = {
        '## 핵심 내용': 'core_content',
        '## 상세 핵심 내용': 'detailed_core_content', 
        '## 상세 정보': 'detailed_content',
        '## 주요 화제': 'main_topics',
        '## 부차 화제': 'sub_topics'
    }
    
    lines = response.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 섹션 헤더 확인
        if line_stripped in section_headers:
            # 이전 섹션 저장 (헤더 포함)
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # 새 섹션 시작 (헤더부터 시작)
            current_section = section_headers[line_stripped]
            current_content = [line_stripped]  # 헤더 포함
        elif current_section and line.strip():  # 빈 줄이 아닌 경우만 추가
            current_content.append(line)
        elif current_section and not line.strip() and current_content:  # 빈 줄도 포함 (단, 시작이 아닌 경우)
            current_content.append(line)
    
    # 마지막 섹션 저장
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections
```

**성공 판정 기준**:
```python
# 5개 모두 추출되었으면 성공 (헤더 확인)
success_count = sum(1 for content in sections.values() if content.strip() and content.startswith('##'))
success = success_count == 5
```

**섹션 헤더 매핑 필요 이유**: 
AI 응답에서 "## 핵심 내용" 등의 헤더를 찾아 'core_content' 등의 키로 매핑하여 구조화된 데이터로 변환하기 위함

#### 1.1.3 활용 코드 블록

**generate_extract_section() 구현**:
```python
async def generate_extract_section(self, doc: Dict) -> Dict:
    """engines_v5.py extract_all_info 로직 활용"""
    content = doc.get('content_section', '')
    title = doc.get('title', '')
    
    # engines_v5.py 프롬프트 패턴 활용
    prompt = f"""다음 문서에서 5가지 정보를 순서대로 추출해주세요.

문서 제목: {title}
문서 내용:
{content}
[위의 프롬프트 패턴 사용]"""
    
    try:
        # 기본 AI 호출 (단일 요청)
        provider_config = self.config['extract_section_information']
        response = await self.ai_service.query_single_request(
            provider=provider_config['provider'],
            prompt=prompt
        )
        
        # engines_v5.py 파싱 로직 활용
        sections = self.parse_extraction_response(response)
        
        # 성공 판정 (5개 모두 추출되었는지 확인)
        success_count = sum(1 for content in sections.values() if content.strip() and content.startswith('##'))
        if success_count == 5:
            self.api_calls_counter += 1
            return sections
        else:
            logging.warning(f"추출 섹션 불완전 ({success_count}/5), fallback 실행")
            raise Exception("추출 섹션 불완전")
            
    except Exception as e:
        logging.error(f"기본 추출 실패: {e}, fallback 모드 실행")
        return await self.fallback_extraction(doc)
```

### 1.2 update_parent_extraction_with_composition 활용

#### 1.2.1 프롬프트 패턴 (라인 496-528)

**구성 노드 정보 수집 방식**:
```python
# 구성 노드들의 내용 수집
composition_info = []
for child_file in parent_doc['composition_files']:
    child_path = f"unified_info_docs/{child_file}"
    child_doc = await self.parse_unified_document(child_path)
    child_sections = self.parse_extraction_section(child_doc['extraction_section'])
    
    # 모든 5개 섹션 내용 수집 (헤더 제거)
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
```

**부모 노드 업데이트 프롬프트**:
```python
prompt = f"""다음은 부모 노드의 추출 섹션을 구성 노드들의 내용을 반영하여 업데이트하는 작업입니다.

**부모 노드 ({parent_node['title']})의 현재 내용:**
핵심 내용: {parent_core}
상세 핵심 내용: {parent_detailed_core}
상세 정보: {parent_detailed_info}
주요 화제: {parent_main_topics}
부차 화제: {parent_sub_topics}

**구성 노드들의 내용:**
{chr(10).join(composition_info)}

부모 노드의 각 섹션을 구성 노드들의 내용을 종합적으로 반영하여 개선해주세요. 
부모 노드는 전체적인 개요와 통합적인 관점을 제공하되, 구성 노드들의 세부 내용이 잘 반영되도록 해주세요.

반드시 다음 형식을 정확히 지켜서 출력해주세요:

## 핵심 내용
[구성 노드들의 내용을 종합한 개선된 핵심 내용]

## 상세 핵심 내용
[구성 노드들의 내용을 종합한 개선된 상세 핵심 내용]

## 상세 정보
[구성 노드들의 내용을 종합한 개선된 상세 정보]

## 주요 화제
[구성 노드들의 주요 화제를 종합한 개선된 주요 화제]

## 부차 화제
[구성 노드들의 부차 화제를 종합한 개선된 부차 화제]

**중요**: 각 섹션은 반드시 "## " (해시 2개 + 공백)으로 시작하는 제목을 포함해야 하고, 제목 다음 줄부터 내용을 작성해주세요."""
```

#### 1.2.2 구성 정보 포맷팅 (라인 470-478)

**child_info 구조화 방법**:
```python
child_info = f"""
구성노드 ({child_node['title']}):
- 핵심 내용: {core_content}
- 상세 핵심 내용: {detailed_core}
- 상세 정보: {detailed_info}  
- 주요 화제: {main_topics}
- 부차 화제: {sub_topics}"""
```

### 1.3 update_composition_extractions 활용

#### 1.3.1 프롬프트 패턴 (라인 256-269)

**구성 노드 업데이트**:
```python
prompt = f"""다음은 부모 노드의 업데이트된 내용을 바탕으로 구성 노드들의 추출 섹션을 개선하는 작업입니다.

**부모 노드 ({parent_node['title']})의 업데이트된 내용:**
핵심 내용: {parent_core}
상세 핵심 내용: {parent_detailed_core}
상세 정보: {parent_detailed_info}
주요 화제: {parent_main_topics}
부차 화제: {parent_sub_topics}

**구성 노드들의 현재 내용:**
{chr(10).join(composition_info)}

부모 노드의 업데이트된 내용을 반영하여 각 구성 노드의 추출 섹션을 개선해주세요.
각 구성 노드의 고유한 특성은 유지하되, 부모와의 일관성과 연결성을 반영해주세요."""
```

#### 1.3.2 상태 마킹 패턴 (라인 431)

**업데이트 완료 표시 방법**:
```python
# 구성 노드에 부모 노드 반영 완료 상태 표시 추가
await self.add_update_status_mark(child_file, "<부모 노드 반영 완료>")
logging.info(f"✅ 구성노드 상태 표시 추가: <부모 노드 반영 완료>")
```

## 2. ai_service_v4.py 활용

### 2.1 query_single_request() 메서드

#### 2.1.1 메서드 시그니처 및 사용법
```python
async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
    """
    일회성 AI 쿼리 - 세션을 사용하지 않는 단발성 요청
    
    Args:
        prompt: 질의 프롬프트
        additional_data: 추가 입력 데이터 (파일 경로, 구조화된 데이터 등)
    """
```

#### 2.1.2 provider 설정 방법
```python
# ai_config.yaml에서 provider 설정 로드
provider_config = self.config['extract_section_information']
provider = provider_config['provider']  # "gemini"
model = provider_config['model']        # "gemini-2.0-flash-lite"

# AI 서비스 호출
response = await self.ai_service.query_single_request(
    provider=provider,
    prompt=prompt
)
```


#### 2.1.3 예외 처리 패턴
```python
try:
    response = await self.ai_service.query_single_request(
        provider=provider,
        prompt=prompt
    )
    return response
except Exception as e:
    logging.error(f"AI 서비스 호출 실패: {e}")
    raise
```

### 2.2 AI 제공자별 특성

#### 2.2.1 GeminiProvider 활용 방법
- model: "gemini-2.0-flash-lite"
- temperature: 0.0 (일관성 중요)
- max_tokens: 8192 (flash-lite 모델에 적합)


## 3. 통합 시 주의사항

### 3.1 API 호출 횟수 추적
```python
class ContentProcessingStage:
    def __init__(self, config, ai_service):
        self.api_calls_counter = 0
        
    def log_api_usage(self):
        logging.info(f"📊 총 API 호출 횟수: {self.api_calls_counter}")
```

### 3.2 응답 품질 검증
```python
def validate_extraction_response(self, sections: Dict[str, str]) -> bool:
    """추출 응답 품질 검증"""
    # 필수 섹션 확인
    required_sections = ['core_content', 'detailed_core_content', 'detailed_content']
    for section in required_sections:
        if not sections.get(section, '').strip():
            return False
    
    # 헤더 포함 여부 확인
    for section_content in sections.values():
        if section_content.startswith('##'):
            continue
        else:
            return False
    
    return True
```

### 3.3 AI 요청 재시도 로직
```python
async def ai_request_with_retry(self, prompt: str, provider_config: Dict, max_retries: int = 3) -> str:
    """AI 요청 재시도 로직"""
    for attempt in range(max_retries):
        try:
            self.api_calls_counter += 1
            response = await self.ai_service.query_single_request(
                provider=provider_config['provider'],
                prompt=prompt
            )
            logging.info(f"✅ AI 요청 성공 (시도 {attempt + 1})")
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                logging.error(f"❌ AI 요청 최종 실패: {e}")
                raise e
            else:
                logging.warning(f"⚠️ AI 요청 실패, 재시도 {attempt + 1}/{max_retries}: {e}")
                await asyncio.sleep(1)
```

### 3.4 fallback 전략 (재시도 포함)
```python
async def fallback_extraction(self, doc: Dict) -> Dict:
    """추출 실패 시 3회 재시도 + 간단한 형태로 fallback"""
    logging.warning("기본 추출 실패, fallback 모드 실행 (3회 재시도 포함)")
    
    # 간단한 프롬프트로 추출 시도 (전체 내용 사용)
    simplified_prompt = f"""다음 문서의 핵심 내용을 간단히 추출해주세요:

제목: {doc['title']}
내용: {doc['content_section']}

다음 형식으로 출력해주세요:
## 핵심 내용
[문서의 핵심을 2-3문장으로 요약]

## 상세 핵심 내용  
[중요한 세부사항을 포함하여 설명]

## 상세 정보
[문서의 주요 정보들을 정리]

## 주요 화제
[핵심 주제들]

## 부차 화제
[부차적인 주제들]"""
    
    # 3회 재시도 로직
    for attempt in range(3):
        try:
            self.api_calls_counter += 1
            response = await self.ai_service.query_single_request(
                provider="gemini",
                prompt=simplified_prompt
            )
            
            # fallback 응답 파싱 시도
            sections = self.parse_extraction_response(response)
            
            # 파싱 성공 확인 (5개 모두 추출되었는지)
            success_count = sum(1 for content in sections.values() if content.strip() and content.startswith('##'))
            if success_count == 5:
                logging.info(f"✅ Fallback 추출 성공 (시도 {attempt + 1})")
                return sections
            else:
                logging.warning(f"⚠️ Fallback 파싱 실패 ({success_count}/5), 재시도 필요")
                if attempt == 2:  # 마지막 시도라면 최소 구조라도 반환
                    logging.warning("❌ 최종 시도에서도 파싱 실패, 기본 구조로 반환")
                    return {
                        'core_content': f"## 핵심 내용\n{response}",
                        'detailed_core_content': f"## 상세 핵심 내용\n{response}",
                        'detailed_content': f"## 상세 정보\n{response}",
                        'main_topics': f"## 주요 화제\n{response}",
                        'sub_topics': f"## 부차 화제\n{response}"
                    }
                else:
                    raise Exception(f"Fallback 파싱 실패: {success_count}/5 섹션만 추출됨")
        except Exception as e:
            if attempt == 2:  # 마지막 시도
                logging.error(f"❌ Fallback 추출도 최종 실패: {e}")
                raise
            else:
                logging.warning(f"⚠️ Fallback 추출 실패, 재시도 {attempt + 1}/3: {e}")
                await asyncio.sleep(1)

## 4. 코드 이식 체크리스트

### 4.1 필수 수정 포인트
- [ ] engines_v5.py 프롬프트 패턴 복사
- [ ] 응답 파싱 로직 이식
- [ ] ai_service_v4.py 호출 방식 적용
- [ ] 재시도 로직 구현
- [ ] 상태 마킹 로직 이식

### 4.2 선택적 개선 사항
- [ ] 프롬프트 품질 개선
- [ ] 응답 검증 강화
- [ ] 로깅 세분화

### 4.3 테스트 검증 방법
- [ ] engines_v5.py와 동일한 결과 생성 확인
- [ ] 상태 마킹 위치 정확성 검증
- [ ] 주요/부차 화제 보존 확인
- [ ] fallback 로직 동작 확인