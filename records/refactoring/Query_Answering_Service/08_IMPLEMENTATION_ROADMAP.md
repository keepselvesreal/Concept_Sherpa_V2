# 구현 단계별 가이드

## 전체 구현 일정
- **총 소요 시간**: 3.5일
- **난이도**: 중급 (비동기 프로그래밍, AI 서비스 연동)
- **핵심 기술**: asyncio, JSON 파싱, 파일 시스템, 정규화

## 1단계: 기본 구조 + 안정성 (1일)

### 1.1 설정 및 기본 클래스 생성 (0.3일)
- [ ] `config/query_answering.yaml` 생성
- [ ] `QueryAnsweringService` 클래스 골격 생성
- [ ] 의존성 주입 구조 구현
- [ ] 기본 로깅 설정

**완료 기준**:
```python
# 기본 초기화가 정상 동작
service = QueryAnsweringService(config_manager, logger, ai_service)
assert service is not None
```

### 1.2 데이터 로더 구현 (0.4일)
- [ ] `WorkspaceDataLoader` 구현
- [ ] 책 목차 파싱 로직
- [ ] 장별 데이터 로딩
- [ ] 파일 존재 검증 로직

**완료 기준**:
```python
# 테스트 데이터 로딩 성공
book_data = loader.load_book_data(TEST_BOOK_PATH)
assert len(book_data['chapters_data']) > 0
```

### 1.3 파일 매핑 및 정규화 (0.3일)
- [ ] `ContentMapper` 구현
- [ ] `normalize_title()` 활용 로직
- [ ] 장 폴더 매핑
- [ ] unified_info_docs 파일 매핑

**완료 기준**:
```python
# 정규화 매핑 정상 동작
mapper = ContentMapper()
folder = mapper.map_chapter_to_folder("Chapter Title", book_data)
assert folder is not None
```

## 2단계: AI 연동 + 재시도 로직 (1.5일)

### 2.1 장 선택기 구현 (0.5일)
- [ ] `ChapterSelector` 클래스
- [ ] AI 서비스 3회 재시도 로직
- [ ] JSON 파싱 실패 시 재요청 로직
- [ ] 목차 포맷팅 유틸리티

**완료 기준**:
```python
# 장 선택 정상 동작
selector = ChapterSelector(ai_service, logger)
chapters = await selector.select_chapters(toc_data, "test query")
assert len(chapters) > 0
assert len(chapters) <= 3
```

### 2.2 섹션 선택기 구현 (0.5일)
- [ ] `SectionSelector` 클래스
- [ ] 장 목차 기반 섹션 선택
- [ ] 동일한 재시도 패턴 적용
- [ ] 장 목차 포맷팅

**완료 기준**:
```python
# 섹션 선택 정상 동작
sections = await selector.select_sections(chapter_toc_data, "test query")
assert len(sections) > 0
```

### 2.3 개별 답변 생성 로직 (0.5일)
- [ ] 장 기반 답변 생성 (`_generate_chapter_answer`)
- [ ] 섹션 기반 답변 생성 (`_generate_section_answer`)
- [ ] 전체 내용 로드 (토큰 제한 없음)
- [ ] AI 서비스 재시도 패턴 적용

**완료 기준**:
```python
# 개별 답변 생성 성공
answer = await generator._generate_chapter_answer(query, chapter_folder)
assert answer != ""
assert "오류" not in answer  # 정상 답변 생성
```

## 3단계: 병렬 처리 + 통합 (1.5일)

### 3.1 병렬 답변 생성기 구현 (0.8일)
- [ ] `ParallelAnswerGenerator` 클래스
- [ ] `asyncio.Semaphore` 최대 4개 제한
- [ ] 개별 실패 격리 로직
- [ ] 성공한 결과만 필터링

**완료 기준**:
```python
# 병렬 처리 정상 동작
answers = await generator.generate_chapter_based_answers_parallel(query, chapter_data_list)
assert len(answers) > 0
assert all(answer['status'] == 'success' for answer in answers)
```

### 3.2 응답 모드별 처리 로직 (0.4일)
- [ ] `_process_chapter_based_response` 구현
- [ ] `_process_section_based_response` 구현
- [ ] 병렬 처리 통합
- [ ] 데이터 준비 로직

**완료 기준**:
```python
# 각 응답 모드 정상 동작
result_chapter = await service._process_chapter_based_response(query, book_data)
result_section = await service._process_section_based_response(query, book_data)
assert result_chapter['response_mode'] == 'chapter_based_response'
assert result_section['response_mode'] == 'section_based_response'
```

### 3.3 최종 답변 종합 (0.3일)
- [ ] `_synthesize_chapter_based_answers` 구현
- [ ] `_synthesize_section_based_answers` 구현
- [ ] AI 기반 답변 통합
- [ ] 단일/복수 답변 처리

**완료 기준**:
```python
# 최종 종합 답변 생성
synthesized = await service._synthesize_chapter_based_answers(query, answers)
assert synthesized != ""
assert len(synthesized) > 100  # 의미있는 길이의 답변
```

## 4단계: 테스트 및 검증 (0.5일)

### 4.1 통합 테스트 (0.3일)
- [ ] `test_query_answering_service.py` 작성
- [ ] chapter_based_response 테스트
- [ ] section_based_response 테스트
- [ ] 에러 시나리오 테스트

**완료 기준**:
```python
# 모든 테스트 통과
pytest refactoring/tests/integration/test_query_answering_service.py -v
# Expected: 모든 테스트 PASSED
```

### 4.2 성능 및 안정성 검증 (0.2일)
- [ ] 병렬 처리 성능 측정
- [ ] AI 서비스 재시도 동작 확인
- [ ] JSON 파싱 실패 시나리오 테스트
- [ ] 메모리 사용량 확인

**완료 기준**:
```python
# 성능 검증
start_time = time.time()
result = await service.answer_query(query, book_path, "chapter_based_response")
processing_time = time.time() - start_time

assert processing_time < 60  # 1분 이내 처리
assert len(result['chapter_based_answers']) > 0
```

## 검증 체크리스트

### 기능 검증
- [ ] chapter_based_response 모드 정상 동작
- [ ] section_based_response 모드 정상 동작
- [ ] AI 서비스 3회 재시도 동작 확인
- [ ] JSON 파싱 실패 시 재요청 동작 확인
- [ ] 병렬 처리 (최대 4개) 동작 확인
- [ ] 개별 실패 격리 동작 확인

### 성능 검증
- [ ] 4개 장 병렬 처리 시 시간 단축 확인 (~75%)
- [ ] 메모리 사용량 적정 수준 유지
- [ ] CPU 사용률 안정적 수준
- [ ] 파일 I/O 효율성 확인

### 안정성 검증
- [ ] AI 서비스 장애 시 재시도 동작
- [ ] 일부 장/섹션 실패 시 정상 응답 생성
- [ ] 파일 누락 시 적절한 에러 메시지
- [ ] 잘못된 입력 시 예외 처리

### 코드 품질 검증
- [ ] 타입 힌트 완전성 확인
- [ ] 로깅 충분성 확인
- [ ] 에러 메시지 명확성 확인
- [ ] 코드 가독성 및 주석 적절성

## 배포 준비

### 환경 설정
```bash
# 필요한 디렉토리 생성
mkdir -p refactoring/src/components
mkdir -p refactoring/config

# 설정 파일 배치
cp query_answering.yaml refactoring/config/

# 권한 설정
chmod 755 refactoring/src/components
chmod 644 refactoring/config/query_answering.yaml
```

### 의존성 확인
```python
# 필수 의존성 import 테스트
from services.ai_service_v4 import AIService  # ✅
from utils.text_utils import normalize_title  # ✅
from utils.config_manager import ConfigManager  # ✅
from utils.logger_v2 import Logger  # ✅
```

### 최종 동작 확인
```python
# End-to-End 테스트
async def test_full_workflow():
    service = QueryAnsweringService(config_manager, logger, ai_service)
    
    result = await service.answer_query(
        user_query="객체지향 프로그래밍의 복잡성은?",
        book_path=TEST_BOOK_PATH,
        response_mode="chapter_based_response"
    )
    
    assert result['synthesized_answer'] != ""
    print("✅ 전체 워크플로우 정상 동작")

# 실행
await test_full_workflow()
```

## 트러블슈팅 가이드

### 일반적인 문제들
1. **AI 서비스 연결 실패** → ai_service_v4.py 설정 확인
2. **파일 경로 오류** → 절대 경로 사용 및 존재 확인
3. **JSON 파싱 실패** → AI 프롬프트 명확성 개선
4. **병렬 처리 오류** → asyncio.Semaphore 설정 확인
5. **메모리 부족** → 동시 처리 수 조정

### 디버깅 팁
```python
# 상세 로깅 활성화
logger.setLevel(logging.DEBUG)

# 개별 컴포넌트 테스트
await chapter_selector.select_chapters(toc_data, query)
await parallel_generator._generate_chapter_answer(query, folder)

# 중간 결과 확인
print(f"Selected chapters: {selected_chapters}")
print(f"Parallel results: {len(parallel_results)}")
```