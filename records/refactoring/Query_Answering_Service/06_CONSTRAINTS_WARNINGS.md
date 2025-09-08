# 주의사항 및 제약조건

## 파일 처리 주의사항

### 인코딩 및 파일 존재 검증
```python
# 필수 패턴: 파일 읽기 전 검증
if not file_path.exists():
    return "해당 파일을 찾을 수 없습니다."

# 필수 패턴: UTF-8 인코딩 사용
content = file_path.read_text(encoding='utf-8')
```

### 정규화된 파일 매핑
```python
# 정확한 매핑을 위한 패턴
from utils.text_utils import normalize_title

def find_chapter_folder(chapter_title: str, chapters_data: Dict) -> Optional[Dict]:
    normalized = normalize_title(chapter_title)
    
    for folder_name, chapter_data in chapters_data.items():
        # 폴더명에서 번호_ 제거 후 비교
        folder_normalized = folder_name.split('_', 1)[1] if '_' in folder_name else folder_name
        
        if normalized.lower() in folder_normalized.lower():
            return chapter_data
    
    return None
```

## AI 서비스 안정성 강화

### 필수 재시도 로직
```python
# 표준 재시도 패턴 (모든 AI 호출에 적용)
async def call_ai_with_retry(self, prompt: str) -> str:
    for attempt in range(1, self.max_retries + 1):
        try:
            response = await self.ai_service.query_single_request(prompt)
            if response and response.strip():
                return response
            else:
                self.logger.warning(f"Empty response (attempt {attempt})")
                
        except Exception as e:
            self.logger.error(f"AI service error (attempt {attempt}): {str(e)}")
            
            if attempt == self.max_retries:
                raise Exception(f"AI service failed after {self.max_retries} attempts: {str(e)}")
            
            # 점진적 대기 (1s, 2s, 3s)
            await asyncio.sleep(1 * attempt)
    
    raise Exception("Unexpected error in AI service retry logic")
```

### JSON 파싱 실패 처리
```python
# JSON 파싱 재시도 패턴
for attempt in range(1, self.max_retries + 1):
    try:
        response = await self._call_ai_with_retry(prompt)
        parsed_response = json.loads(response.strip())
        
        # 타입 검증
        if isinstance(parsed_response, expected_type):
            return parsed_response
            
    except json.JSONDecodeError as e:
        self.logger.error(f"JSON parsing failed (attempt {attempt}): {str(e)}")
        self.logger.debug(f"Raw response: {response[:200]}...")
        
        if attempt < self.max_retries:
            # 더 명확한 프롬프트로 재시도
            prompt = base_prompt + """
이전 응답이 JSON 형태가 아니었습니다.
반드시 유효한 JSON 형태로만 응답해주세요:
["항목1", "항목2"]

다른 텍스트 없이 JSON만 제공해주세요.
"""

# 최종 실패 시 안전한 기본값 반환
return [] if expected_type == list else {}
```

## 병렬 처리 주의사항

### 동시 실행 수 제한
```python
# 필수: Semaphore를 통한 리소스 보호
class ParallelAnswerGenerator:
    def __init__(self, ai_service, logger, max_concurrent: int = 4):
        self.semaphore = asyncio.Semaphore(max_concurrent)  # 최대 4개
    
    async def process_item(self, item):
        async with self.semaphore:  # 반드시 사용
            # 실제 처리 로직
            pass
```

### 개별 실패 격리
```python
# 개별 작업 실패가 전체에 영향 주지 않도록
async def process_single_item(item) -> Dict:
    try:
        result = await self._process_item(item)
        return {'status': 'success', 'data': result}
    except Exception as e:
        # 로그 기록 후 에러 상태 반환
        self.logger.error(f"Individual processing failed: {str(e)}")
        return {'status': 'error', 'error': str(e)}

# 성공한 결과만 사용
results = await asyncio.gather(*tasks, return_exceptions=False)
successful_results = [r for r in results if r['status'] == 'success']
```

## 성능 고려사항

### 메모리 관리 (현재 버전)
- **대용량 파일**: 현재 고려 불필요 (전체 장 내용 로드 허용)
- **메모리 사용량**: 현재 고려 불필요 (동시 처리 수 4개 제한으로 충분)
- **가비지 컬렉션**: Python의 자동 메모리 관리에 의존

### 응답 시간 최적화
```python
# 병렬 처리로 대폭 개선
# 4개 장 순차 처리: 4 * 평균응답시간
# 4개 장 병렬 처리: 1 * 평균응답시간 (약 75% 시간 단축)

# 예상 성능
시나리오 = {
    "1개 장": "~10초",
    "2개 장 병렬": "~10초 (vs 순차 20초)", 
    "3개 장 병렬": "~10초 (vs 순차 30초)",
    "4개 장 병렬": "~10초 (vs 순차 40초)"
}
```

## 확장성 고려사항

### 캐싱 준비
```python
# 향후 캐싱을 위한 설계 고려사항
class QueryAnsweringService:
    def __init__(self, config_manager, logger, ai_service):
        # 캐싱이 필요할 때 추가할 수 있는 구조
        self.cache_enabled = config_manager.get('cache_enabled', False)
        # self.cache_store = CacheStore() if self.cache_enabled else None
```

### 로깅 및 모니터링
```python
# 상세한 디버깅을 위한 로깅
self.logger.info(f"Processing query: {user_query[:50]}...")
self.logger.debug(f"Selected chapters: {selected_chapter_titles}")
self.logger.info(f"Parallel processing {len(chapter_data_list)} chapters")
self.logger.info(f"Successfully processed {len(successful_answers)} chapters")
```

## 에러 시나리오별 대응

### 일반적인 실패 시나리오
1. **AI 서비스 일시 장애** → 3회 재시도 → 개별 작업 실패로 격리
2. **JSON 파싱 실패** → 더 명확한 프롬프트로 재시도 → 빈 결과 반환
3. **파일 누락** → 안전한 기본 메시지 반환
4. **네트워크 타임아웃** → 재시도 후 최종 실패 시 명확한 에러 메시지

### 복구 불가능한 상황
```python
# 모든 장/섹션 처리 실패 시
if not successful_answers:
    return {
        'user_query': user_query,
        'response_mode': response_mode,
        'selected_chapter_titles': selected_chapter_titles,
        'chapter_based_answers': [],
        'section_based_answers': [],
        'synthesized_answer': "죄송합니다. 시스템 오류로 인해 답변을 생성할 수 없습니다. 잠시 후 다시 시도해주세요."
    }
```

## 보안 고려사항

### 입력 검증
```python
# 사용자 입력 기본 검증
def validate_inputs(user_query: str, book_path: str, response_mode: str):
    if not user_query or not user_query.strip():
        raise ValueError("사용자 질의가 비어있습니다.")
    
    if not book_path or not Path(book_path).exists():
        raise ValueError("유효하지 않은 책 경로입니다.")
    
    if response_mode not in ["chapter_based_response", "section_based_response"]:
        raise ValueError("지원하지 않는 응답 모드입니다.")
```

### 경로 보안
```python
# 경로 조작 방지
def secure_path_join(base_path: Path, relative_path: str) -> Path:
    full_path = base_path / relative_path
    # base_path 외부로 벗어나지 않도록 검증
    if not str(full_path.resolve()).startswith(str(base_path.resolve())):
        raise ValueError("경로 조작 시도가 감지되었습니다.")
    return full_path
```