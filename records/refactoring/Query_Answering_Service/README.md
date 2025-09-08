# Query Answering Service - AI 구현자 안내 문서

## 📋 문서 개요

이 폴더는 **질의 응답 시스템(Query Answering Service)** 구현을 담당할 AI를 위한 완전한 안내 문서 패키지입니다.

## 📁 문서 구조 및 읽기 순서

### 🔥 즉시 필요 (High Priority - 구현 시작 전 필독)
1. **[01_PROJECT_OVERVIEW.md](01_PROJECT_OVERVIEW.md)** - 프로젝트 전체 이해
2. **[02_ARCHITECTURE_GUIDE.md](02_ARCHITECTURE_GUIDE.md)** - 설계 패턴과 구조 파악
3. **[03_DATA_STRUCTURE_SPEC.md](03_DATA_STRUCTURE_SPEC.md)** - 파일 구조 및 데이터 명세

### ⚡ 구현 시작 후 (Medium Priority - 개발 중 참조)
4. **[04_API_INTERFACE_GUIDE.md](04_API_INTERFACE_GUIDE.md)** - 기존 서비스 연동 방법
5. **[05_IMPLEMENTATION_EXAMPLES.md](05_IMPLEMENTATION_EXAMPLES.md)** - 구체적 구현 예제
6. **[06_CONSTRAINTS_WARNINGS.md](06_CONSTRAINTS_WARNINGS.md)** - 주의사항 및 함정 회피

### 📋 완료 단계 (Low Priority - 완성도 향상)
7. **[07_PROJECT_STRUCTURE.md](07_PROJECT_STRUCTURE.md)** - 파일 배치 및 구조
8. **[08_IMPLEMENTATION_ROADMAP.md](08_IMPLEMENTATION_ROADMAP.md)** - 단계별 구현 가이드

## 🎯 핵심 요구사항 요약

### 필수 기술 제약
- **AI 서비스**: `ai_service_v4.py`의 `query_single_request` **만** 사용
- **정규화**: `text_utils.py`의 `normalize_title()` 함수 **필수 활용**
- **독립성**: 기존 파이프라인과 완전 독립적 동작
- **병렬 처리**: 최대 4개 장/섹션 동시 처리
- **재시도 로직**: AI 서비스 장애 시 3회 자동 재시도

### 응답 모드
- **chapter_based_response**: 장 전체 내용 기반 답변
- **section_based_response**: 섹션별 unified_info_docs 기반 답변

### 성능 목표
- **안정성**: 일부 실패 시에도 성공한 답변으로 종합 응답
- **속도**: 병렬 처리로 ~75% 시간 단축
- **품질**: JSON 파싱 실패 시 재요청으로 응답 품질 보장

## 🚀 구현 시작 가이드

### 1단계: 환경 파악
```bash
# 기존 의존성 확인
ls refactoring/src/services/ai_service_v4.py  # ✅ 있어야 함
ls refactoring/src/utils/text_utils.py        # ✅ 있어야 함
```

### 2단계: 테스트 데이터 확인
```bash
# 테스트용 책 데이터
ls refactoring/tests/data/Data_Oriented_Programming/
```

### 3단계: 문서 순서대로 읽기
1. PROJECT_OVERVIEW → ARCHITECTURE_GUIDE → DATA_STRUCTURE_SPEC
2. API_INTERFACE_GUIDE → IMPLEMENTATION_EXAMPLES
3. 구현 시작!

## ⚠️ 중요 주의사항

### 절대 하지 말 것
- ❌ `ai_service.query_single_request` 외 다른 AI 메서드 사용
- ❌ 별도의 AI 래퍼 클래스 생성
- ❌ 기존 파이프라인 Stage 구조 따라하기 (독립 서비스)
- ❌ 토큰 제한 적용 (전체 장 내용 로드)

### 반드시 할 것
- ✅ 3회 재시도 로직 모든 AI 호출에 적용
- ✅ JSON 파싱 실패 시 더 명확한 프롬프트로 재시도
- ✅ 병렬 처리 시 `asyncio.Semaphore` 최대 4개 제한
- ✅ 개별 실패가 전체 실패로 이어지지 않게 격리
- ✅ `normalize_title()` 함수로 파일명 매칭

## 🔍 트러블슈팅

### 문서 관련 문제
- **이해 안 되는 부분**: IMPLEMENTATION_EXAMPLES.md의 코드 예제 참조
- **에러 처리 문의**: CONSTRAINTS_WARNINGS.md의 에러 시나리오 섹션
- **성능 문제**: ARCHITECTURE_GUIDE.md의 병렬 처리 설계 섹션

### 구현 관련 문제
- **AI 서비스 연동**: API_INTERFACE_GUIDE.md 정독
- **파일 매핑 오류**: DATA_STRUCTURE_SPEC.md의 정규화 규칙 확인
- **병렬 처리 오류**: IMPLEMENTATION_EXAMPLES.md의 ParallelAnswerGenerator 예제

## 📊 성공 기준

### 기능적 완성도
- [ ] chapter_based_response 모드 정상 동작
- [ ] section_based_response 모드 정상 동작
- [ ] 최대 3개 장 선택, 최대 4개 병렬 처리
- [ ] AI 서비스 3회 재시도 + JSON 파싱 재시도

### 비기능적 품질
- [ ] 일부 실패 시에도 성공한 답변들로 종합 응답
- [ ] 4개 장 병렬 처리 시 ~75% 시간 단축
- [ ] 명확한 에러 메시지와 로깅
- [ ] 메모리 사용량 예측 가능한 수준

## 📞 지원

이 문서들로 해결되지 않는 문제가 있다면:
1. **CONSTRAINTS_WARNINGS.md** 의 트러블슈팅 섹션 확인
2. **IMPLEMENTATION_EXAMPLES.md** 의 유사 사례 검색
3. **API_INTERFACE_GUIDE.md** 의 재시도 패턴 재검토

---

**구현 성공을 기원합니다!** 🚀

이 문서들은 실제 프로덕션에서 안정적으로 동작하는 견고한 시스템을 구축할 수 있도록 설계되었습니다.