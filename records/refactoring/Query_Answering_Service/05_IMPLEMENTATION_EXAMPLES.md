# 구현 예제 및 테스트 케이스

## 기본 사용 예제

### 초기화 및 기본 호출
```python
# 서비스 초기화
from services.query_answering_service import QueryAnsweringService
from services.ai_service_v4 import AIService
from utils.config_manager import ConfigManager
from utils.logger_v2 import Logger

# 의존성 초기화
config_manager = ConfigManager("config/")
logger = Logger("query_answering")
ai_service = AIService(config_manager, logger)

# 서비스 생성
query_service = QueryAnsweringService(config_manager, logger, ai_service)

# chapter_based_response 예제
result = await query_service.answer_query(
    user_query="객체지향 프로그래밍의 복잡성은 무엇인가요?",
    book_path="/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming",
    response_mode="chapter_based_response"
)

print("선택된 장:", result['selected_chapter_titles'])
print("최종 답변:", result['synthesized_answer'])
```

### section_based_response 예제
```python
result = await query_service.answer_query(
    user_query="데이터베이스 연산을 최적화하는 방법은?",
    book_path="/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming", 
    response_mode="section_based_response"
)

print("섹션별 답변 수:", len(result['section_based_answers']))
for answer in result['section_based_answers']:
    print(f"- {answer['chapter_title']} > {answer['section_title']}")
```

## 컴포넌트별 구현 예제

### ChapterSelector 구현
```python
import json
import asyncio
from typing import List, Dict

class ChapterSelector:
    def __init__(self, ai_service, logger, max_retries: int = 3):
        self.ai_service = ai_service
        self.logger = logger
        self.max_retries = max_retries
    
    async def select_chapters(self, toc_data: List[Dict], user_query: str) -> List[str]:
        toc_text = self._format_toc_for_ai(toc_data)
        
        base_prompt = f"""
사용자 질의: "{user_query}"

책 목차:
{toc_text}

질의에 답변할 수 있는 장을 최대 3개 선택하세요.
"""
        
        prompt = base_prompt + """
응답은 정확히 장 제목만 JSON 배열로 반환: ["장1 제목", "장2 제목"]
"""
        
        # JSON 파싱 재시도 로직
        for attempt in range(1, self.max_retries + 1):
            try:
                response = await self._call_ai_with_retry(prompt)
                parsed_response = json.loads(response.strip())
                
                if isinstance(parsed_response, list):
                    return parsed_response[:3]  # 최대 3개
                    
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON parsing failed (attempt {attempt}): {str(e)}")
                
                if attempt < self.max_retries:
                    prompt = base_prompt + """
이전 응답이 JSON 형태가 아니었습니다. 
반드시 다음과 같은 유효한 JSON 배열로만 응답해주세요:
["장 제목1", "장 제목2"]

다른 설명 없이 JSON 배열만 제공해주세요.
"""
        
        return []  # 모든 시도 실패 시
    
    async def _call_ai_with_retry(self, prompt: str) -> str:
        for attempt in range(1, self.max_retries + 1):
            try:
                response = await self.ai_service.query_single_request(prompt)
                if response and response.strip():
                    return response
            except Exception as e:
                self.logger.error(f"AI service error (attempt {attempt}): {str(e)}")
                if attempt == self.max_retries:
                    raise Exception(f"AI service failed after {self.max_retries} attempts")
                await asyncio.sleep(1 * attempt)
        
        raise Exception("Unexpected error")
    
    def _format_toc_for_ai(self, toc_data: List[Dict]) -> str:
        formatted = []
        for item in toc_data:
            if item.get('level') == 1:  # 1레벨 장만
                formatted.append(f"- {item['title']}")
        return "\n".join(formatted)
```

### ParallelAnswerGenerator 병렬 처리 예제
```python
import asyncio
from pathlib import Path

class ParallelAnswerGenerator:
    def __init__(self, ai_service, logger, max_concurrent: int = 4, max_retries: int = 3):
        self.ai_service = ai_service
        self.logger = logger
        self.max_retries = max_retries
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def generate_chapter_based_answers_parallel(self, 
                                                    user_query: str, 
                                                    chapter_data_list: List[Dict]) -> List[Dict]:
        async def process_single_chapter_answer(chapter_data: Dict) -> Dict:
            async with self.semaphore:  # 최대 4개 동시 실행
                try:
                    chapter_title = chapter_data['title']
                    chapter_folder = chapter_data['folder_data']
                    
                    answer = await self._generate_chapter_answer(user_query, chapter_folder)
                    
                    return {
                        'chapter_title': chapter_title,
                        'chapter_answer': answer,
                        'status': 'success'
                    }
                except Exception as e:
                    self.logger.error(f"Chapter answer failed: {str(e)}")
                    return {
                        'chapter_title': chapter_data.get('title', 'Unknown'),
                        'chapter_answer': f"답변 생성 중 오류 발생: {str(e)}",
                        'status': 'error'
                    }
        
        # 병렬 실행
        tasks = [process_single_chapter_answer(data) for data in chapter_data_list]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        # 성공한 답변만 필터링
        return [result for result in results if result['status'] == 'success']
    
    async def _generate_chapter_answer(self, user_query: str, chapter_folder: Dict) -> str:
        chapter_content_file = chapter_folder['folder_path'] / f"{chapter_folder['folder_path'].name}_content.md"
        
        if not chapter_content_file.exists():
            return "해당 장의 내용을 찾을 수 없습니다."
        
        full_content = chapter_content_file.read_text(encoding='utf-8')
        
        prompt = f"""
사용자 질의: "{user_query}"

장 전체 내용:
{full_content}

위 장의 전체 내용을 바탕으로 사용자 질의에 상세히 답변해주세요.
"""
        
        # 3회 재시도 로직
        for attempt in range(1, self.max_retries + 1):
            try:
                response = await self.ai_service.query_single_request(prompt)
                if response and response.strip():
                    return response
            except Exception as e:
                self.logger.error(f"AI service error (attempt {attempt}): {str(e)}")
                if attempt == self.max_retries:
                    return f"AI 서비스 오류로 답변 생성 불가: {str(e)}"
                await asyncio.sleep(1 * attempt)
        
        return "예상하지 못한 오류가 발생했습니다."
```

## 테스트 케이스

### 기본 테스트 데이터
```python
# 테스트 데이터 경로
TEST_BOOK_PATH = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming"

# 테스트 질의들
TEST_QUERIES = [
    "객체지향 프로그래밍의 복잡성은 무엇인가요?",
    "코드와 데이터를 분리하는 방법은?",
    "데이터베이스 연산을 최적화하는 방법은?",
    "함수형 프로그래밍의 장점은?",
    "성능 향상을 위한 디버깅 기법은?"
]

# 예상 결과 검증 포인트
async def test_chapter_based_response():
    result = await query_service.answer_query(
        user_query=TEST_QUERIES[0],
        book_path=TEST_BOOK_PATH,
        response_mode="chapter_based_response"
    )
    
    # 검증 포인트
    assert result['user_query'] == TEST_QUERIES[0]
    assert result['response_mode'] == "chapter_based_response"
    assert len(result['selected_chapter_titles']) > 0
    assert len(result['selected_chapter_titles']) <= 3
    assert len(result['chapter_based_answers']) > 0
    assert result['synthesized_answer'] != ""
    assert result['section_based_answers'] is None
    
    print("✅ chapter_based_response 테스트 통과")

async def test_section_based_response():
    result = await query_service.answer_query(
        user_query=TEST_QUERIES[1], 
        book_path=TEST_BOOK_PATH,
        response_mode="section_based_response"
    )
    
    # 검증 포인트
    assert result['response_mode'] == "section_based_response"
    assert result['section_based_answers'] is not None
    assert result['chapter_based_answers'] is None
    
    for answer in result['section_based_answers']:
        assert 'chapter_title' in answer
        assert 'section_title' in answer
        assert 'section_answer' in answer
        assert 'unified_doc_path' in answer
        assert answer['status'] == 'success'
    
    print("✅ section_based_response 테스트 통과")

# 병렬 처리 성능 테스트
import time

async def test_parallel_performance():
    start_time = time.time()
    
    result = await query_service.answer_query(
        user_query="전반적인 프로그래밍 개념을 설명해주세요",
        book_path=TEST_BOOK_PATH,
        response_mode="chapter_based_response"
    )
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"✅ 처리 시간: {processing_time:.2f}초")
    print(f"✅ 처리된 장 수: {len(result['chapter_based_answers'])}")
    print(f"✅ 평균 장당 처리 시간: {processing_time/len(result['chapter_based_answers']):.2f}초")
```