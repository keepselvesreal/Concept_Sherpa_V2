# Claude 응답 생성기

Claude SDK를 사용하여 프롬프트 지침, 사용자 질의, 조회된 문서를 바탕으로 답변을 생성하는 기본 스크립트입니다.

## 파일 구성

- `claude_response_generator.py`: 메인 응답 생성 스크립트
- `usage_example.py`: 다양한 사용 예제
- `README.md`: 이 문서

## 주요 기능

### ClaudeResponseGenerator 클래스
- **단순함**: 복잡한 설정 없이 기본 기능만 제공
- **비동기 처리**: async/await 패턴 사용
- **오류 처리**: Claude SDK 관련 오류 처리 포함

### 입력 인터페이스
```python
async def generate_response(
    prompt_instructions: str,  # 프롬프트 지침
    user_query: str,          # 사용자 질의
    retrieved_documents: str   # 조회된 문서 문자열
) -> ResponseResult
```

### 출력 구조
```python
@dataclass
class ResponseResult:
    content: str              # 생성된 응답
    success: bool             # 성공 여부
    processing_time: float    # 처리 시간 (초)
    error_message: Optional[str] = None  # 오류 메시지
```

## 사용법

### 1. 기본 사용
```python
from claude_response_generator import ClaudeResponseGenerator

async def main():
    generator = ClaudeResponseGenerator()
    
    instructions = "사용자 질문에 대해 정확한 답변을 생성하세요."
    query = "데이터베이스 정규화란 무엇인가요?"
    documents = "데이터베이스 정규화는 중복을 제거하는 과정입니다..."
    
    result = await generator.generate_response(
        instructions, query, documents
    )
    
    if result.success:
        print(result.content)
    else:
        print(f"오류: {result.error_message}")
```

### 2. 검색 시스템과 통합
```python
# 기존 검색 시스템 사용 가정
search_results = await search_engine.search(user_query)
documents_text = "\n".join([doc.content for doc in search_results])

# 응답 생성
result = await generator.generate_response(
    instructions=prompt_template,
    user_query=user_query,
    retrieved_documents=documents_text
)
```

## 테스트 실행

```bash
# 기본 테스트
python claude_response_generator.py

# 사용 예제 실행
python usage_example.py
```

## 의존성

- `claude-code-sdk`: Claude SDK
- Python 3.11+

## 특징

### 장점
- **단순성**: 필요한 기능만 구현
- **재사용성**: 다른 시스템과 쉽게 통합
- **안정성**: 오류 처리 및 로깅 포함

### 제한사항
- 응답 스타일 커스터마이징 불가
- 토큰 수 제한 설정 불가
- 배치 처리 미지원

## 확장 가능성

필요시 다음 기능들을 추가할 수 있습니다:
- 응답 스타일 옵션
- 토큰 수 제한 설정
- 배치 응답 생성
- 캐싱 시스템
- 성능 모니터링

## 사용 예제

### 실행 결과 예시
```
🚀 Claude 응답 생성기 테스트 시작

📊 테스트 결과:
성공: True
처리 시간: 16.39초

💬 생성된 응답:
데이터 지향 프로그래밍(Data-Oriented Programming, DOP)의 주요 원칙은 다음과 같습니다:

## 1. 코드와 데이터의 분리
- 비즈니스 로직과 데이터를 명확히 분리합니다
...
```

## 냉철한 평가

### 실용성 ✅
- 요구사항에 정확히 부합
- 기존 시스템과 통합 용이
- 테스트 완료 및 정상 동작 확인

### 아쉬운 점 ⚠️
- 16초 응답 시간 (Claude API 특성상 불가피)
- 단순한 에러 처리 (세분화 가능)
- 프롬프트 템플릿 하드코딩

### 권장사항 💡
- 현재 상태로 운영 환경 사용 가능
- 필요시 점진적 기능 확장
- 응답 시간 최적화는 Claude API 한계로 제한적