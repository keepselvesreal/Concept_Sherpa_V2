# API 인터페이스 가이드

## 기존 서비스 활용

### AIService (ai_service_v4.py)
```python
# 임포트
from services.ai_service_v4 import AIService

# 초기화 (의존성 주입)
ai_service = AIService(config_manager, logger)

# 사용법 - 반드시 이 메서드만 사용
response = await ai_service.query_single_request(prompt, additional_data=None)

# 재시도 로직 패턴 (필수 구현)
for attempt in range(1, max_retries + 1):
    try:
        response = await ai_service.query_single_request(prompt)
        if response and response.strip():
            return response
    except Exception as e:
        if attempt == max_retries:
            raise Exception(f"AI service failed after {max_retries} attempts: {str(e)}")
        await asyncio.sleep(1 * attempt)  # 1s, 2s, 3s
```

### 정규화 함수 (text_utils.py)
```python
# 임포트
from utils.text_utils import normalize_title

# 사용 예시
normalized = normalize_title("1.1 OOP design: Classic or classical?")
# 결과: "1_1_OOP_design_Classic_or_classical"

# 파일 매핑에 활용
def find_chapter_folder(chapter_title: str, workspace_path: str) -> Optional[Path]:
    normalized = normalize_title(chapter_title)
    for folder in Path(workspace_path).glob(f"*{normalized}*"):
        if folder.is_dir():
            return folder
    return None
```

### 설정 관리 (config_manager)
```yaml
# config/query_answering.yaml 추가 필요
query_answering:
  default_response_mode: "chapter_based_response"
  max_chapters: 3
  max_sections_per_chapter: 5
  ai_provider: "claude"
  
  # 병렬 처리 설정
  parallel_processing:
    max_concurrent_answers: 4
    enable_parallel: true
  
  # 재시도 설정
  retry_settings:
    max_retries: 3
    retry_delay_seconds: [1, 2, 3]
    
  # JSON 파싱 설정
  json_parsing:
    enable_fallback: true
    max_parsing_retries: 3
```

## 메인 API 명세

### QueryAnsweringService 생성자
```python
def __init__(self, config_manager, logger, ai_service: AIService):
    self.config_manager = config_manager
    self.logger = logger  
    self.ai_service = ai_service  # 직접 사용
    
    # 컴포넌트 초기화
    self.parallel_generator = ParallelAnswerGenerator(ai_service, logger, max_concurrent=4, max_retries=3)
    self.chapter_selector = ChapterSelector(ai_service, logger, max_retries=3)
    self.section_selector = SectionSelector(ai_service, logger, max_retries=3)
```

### 메인 메서드
```python
async def answer_query(
    self,
    user_query: str, 
    book_path: str, 
    response_mode: str = "chapter_based_response"
) -> Dict[str, Any]:
    """
    질의 응답 메인 메서드
    
    Args:
        user_query: 사용자 질의
        book_path: 완료된 책 workspace 경로  
        response_mode: "chapter_based_response" | "section_based_response"
        
    Returns:
        응답 딕셔너리 (DATA_STRUCTURE_SPEC.md 참조)
    """
```

## JSON 파싱 재시도 패턴
```python
# ChapterSelector, SectionSelector에서 사용할 패턴
base_prompt = "기본 프롬프트"
prompt = base_prompt + "JSON 배열로 응답: [\"항목1\", \"항목2\"]"

for attempt in range(1, max_retries + 1):
    try:
        response = await self._call_ai_with_retry(prompt)
        parsed_response = json.loads(response.strip())
        
        if isinstance(parsed_response, list):
            return parsed_response
    except json.JSONDecodeError as e:
        if attempt < max_retries:
            # 더 명확한 프롬프트로 재시도
            prompt = base_prompt + """
이전 응답이 JSON 형태가 아니었습니다. 
반드시 유효한 JSON 배열로만 응답해주세요: ["항목1", "항목2"]
다른 텍스트 없이 JSON만 제공해주세요.
"""

# 최종 실패 시 빈 리스트 반환
return []
```

## 병렬 처리 패턴
```python
# ParallelAnswerGenerator에서 사용할 패턴
async def process_items_parallel(self, items: List) -> List[Dict]:
    async def process_single_item(item) -> Dict:
        async with self.semaphore:  # 최대 4개 제한
            try:
                result = await self._process_item(item)
                return {'status': 'success', 'data': result}
            except Exception as e:
                return {'status': 'error', 'error': str(e)}
    
    tasks = [process_single_item(item) for item in items]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    
    # 성공한 결과만 필터링
    return [result for result in results if result['status'] == 'success']
```