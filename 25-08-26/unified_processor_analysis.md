# unified_processor.py 모듈 분석 문서

## 🎯 모듈 개요와 핵심 이해 포인트

### 핵심 역할
`unified_processor.py`는 **질의응답 시스템의 중앙 오케스트레이터**로, 여러 개의 전문화된 프로세서들을 통합 관리하고 병렬 실행하는 메인 컨트롤러입니다.

### 핵심 특징
- **4단계 처리 파이프라인**: 세션 관리 → 병렬 실행 → 결과 통합 → 출력
- **조건부 프로세서 실행**: query_number에 따른 `supplementary_context_analyzer` 실행 제어
- **완전 병렬 처리**: `asyncio.gather()`를 통한 독립적 프로세서 동시 실행
- **세션 상태 공유**: 모든 프로세서가 동일한 세션 정보로 작업

### 이해의 핵심
1. **세션 관리의 선행성**: 병렬 실행 전에 모든 세션 관리가 완료됨
2. **매개변수 기반 통신**: 각 프로세서는 session_id, query_number를 매개변수로 받음
3. **실패 격리**: 개별 프로세서 실패가 전체 시스템을 중단시키지 않음

---

## 📋 1. 구조적 이해 (Structure Understanding)

### 1.1 의존성 그래프
```
unified_processor.py (메인 오케스트레이터)
├── 직접 의존성 (Direct Dependencies)
│   ├── session_manager.py
│   │   ├── SessionCacheManager (세션 캐시 CRUD)
│   │   └── SessionManager (세션 폴더 관리)
│   ├── output_formatter.py 
│   │   └── OutputFormatter (통합 출력 포맷)
│   ├── session_query_processor.py
│   │   └── SessionQueryProcessor (세션별 질의처리)
│   ├── individual_document_processor.py
│   │   └── IndividualDocumentProcessor (개별 문서처리)
│   └── supplementary_context_analyzer.py
│       └── analyze_supplementary_context() (보충 분석 함수)
└── 간접 의존성 (Indirect Dependencies)
    ├── claude_code_sdk (AI 모델 통신)
    ├── rich (콘솔 출력)
    └── yaml, json, asyncio (시스템 라이브러리)
```

### 1.2 클래스 계층 구조
```
UnifiedProcessor (메인 컨트롤러)
├── __init__() : 모든 컴포넌트 초기화
├── process_query() : 메인 처리 흐름
├── _setup_session_frontend() : 세션 관리
├── _run_parallel_functions() : 병렬 실행 제어
├── _call_session_*() : 개별 프로세서 호출 래퍼
└── _display_integrated_results() : 결과 출력

ResultCollector (결과 통합)
├── integrate_results() : 프로세스 결과 통합
└── _create_summary() : 성공률/시간 통계

setup_logging() : 통합 로깅 시스템
main() : CLI 인터페이스
```

### 1.3 데이터 구조와 흐름
```
Input: 사용자 질의 + 옵션
    ↓
세션 정보: {session_id, query_number, is_new_session}
    ↓
병렬 실행 결과: {
    "session_query_processor": {...},
    "individual_document_processor": {...},
    "supplementary_context_analyzer": {...}  // 조건부
}
    ↓
통합 결과: {
    query, session_id, query_number,
    process_results, summary, timestamp
}
    ↓
Output: 사용자 화면 출력 + 파일 저장
```

---

## 🔄 2. 동적 행동 이해 (Dynamic Behavior)

### 2.1 실행 흐름 (4단계 파이프라인)

#### 1단계: 프론트엔드 세션 관리 (순차 처리)
```python
# _setup_session_frontend()
세션 결정 로직:
├── manual_session_id 존재 → 유효성 검증 후 사용
├── force_new = True → 새 세션 생성
└── 기본 → 캐시에서 로드 또는 새 세션 생성

세션 폴더 생성:
└── session_manager.ensure_session_folder(session_id)

세션 캐싱:
├── 새 세션 → save_current_session()
└── 기존 세션 → update_session_timestamp()
```

#### 2단계: 병렬 함수 실행
```python
# _run_parallel_functions()
함수 목록 구성:
├── session_processor (항상 실행)
│   ├── is_new_session=True → process_first_query()
│   └── is_new_session=False → process_resume_query()
├── individual_processor (항상 실행)
│   └── process_individual_documents()
└── supplementary_analyzer (조건부 실행)
    └── query_number >= 2 → analyze_supplementary_context()

병렬 실행:
└── asyncio.gather(*functions, return_exceptions=True)
```

#### 3단계: 결과 수집 및 통합
```python
# ResultCollector.integrate_results()
통합 데이터 구성:
├── 기본 정보: query, session_id, query_number, timestamp
├── process_results: 각 프로세서별 결과
└── summary: 성공률, 처리 시간, 통계 정보
```

#### 4단계: 통합 결과 출력
```python
# _display_integrated_results()
출력 구성:
├── 기본 정보 패널
├── 프로세스 실행 결과 테이블
└── 성공한 결과들의 상세 내용
```

### 2.2 상태 변화 추적

#### 세션 상태 변화
```
[시작] 사용자 질의 입력
    ↓
[세션 결정] session_id, query_number, is_new_session 확정
    ↓
[캐시 업데이트] .session_cache.json 파일 갱신
    ↓
[병렬 실행] 모든 프로세서가 동일한 세션 정보로 작업
    ↓
[결과 통합] 개별 결과를 하나로 집약
    ↓
[종료] 사용자에게 통합 결과 출력
```

#### 프로세서별 상태
- **독립적 실행**: 각 프로세서는 독립적으로 성공/실패
- **실패 격리**: 하나의 프로세서 실패가 다른 프로세서에 영향 없음
- **결과 보존**: 실패한 프로세서도 오류 정보와 함께 결과에 포함

### 2.3 이벤트와 콜백

#### 프로세서 호출 패턴
```python
# 래퍼 함수를 통한 표준화된 호출
async def _call_session_first_query():
    start_time = time.time()
    try:
        result = await self.session_processor.process_first_query(...)
        result['elapsed_time'] = time.time() - start_time
        return result
    except Exception as e:
        return {'success': False, 'error': str(e), 'elapsed_time': ...}
```

#### 에러 처리 체계
- **개별 프로세서 레벨**: 각 프로세서가 자체적으로 try-catch 처리
- **래퍼 함수 레벨**: `_call_*()` 함수들이 표준화된 에러 응답 생성
- **통합 시스템 레벨**: `process_query()`가 전체 시스템 오류 처리

---

## 🔧 3. 설정과 환경 (Configuration & Environment)

### 3.1 설정 시스템 구조
```yaml
# config.yaml 구조 (추정)
logging:
  level: INFO
  file_path: ./logs/unified_processor.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

session:
  id_separator: "-"
  file_prefix: "collective" 
  initial_query_number: 1

output:
  enable_progress: true
  enable_console: true

error_handling:
  detailed_errors: true

references:
  folder_path: ./references
  supported_extensions: ['.md', '.txt']
  exclude_patterns: ['.*']

parallel:
  max_concurrent: 5

query:
  claude:
    max_turns: 10
```

### 3.2 설정 분배 패턴
```
unified_processor.py
├── logging → setup_logging() → 전역 로거 설정
├── session → SessionManager → 세션 관리 설정
├── output → OutputFormatter → 출력 형식 설정
└── [전체 설정] → 각 프로세서 초기화 시 전달
    ├── session_query_processor(config_path)
    ├── individual_document_processor(config_path)
    └── analyze_supplementary_context(config_path=...)
```

### 3.3 외부 시스템 연동
- **Claude SDK**: `claude_code_sdk` 모듈을 통한 AI 모델 통신
- **파일 시스템**: 세션 폴더, 캐시 파일, 참조 문서 관리
- **프로세스 통신**: 각 프로세서와 매개변수 기반 통신

---

## 🚀 추가 권장 분석 정보

### A. 성능 특성 분석
```markdown
## 성능 메트릭
- **병목 지점**: Claude SDK API 호출 시간 (각 프로세서별로 독립적)
- **메모리 사용**: 문서 내용 로드 시 peak memory 사용량
- **확장성**: 참조 문서 수에 비례한 처리 시간 증가
- **동시성**: 최대 3개 프로세서 병렬 실행 (query_number >= 2일 때)

## 최적화 포인트
- 문서 캐싱으로 중복 읽기 방지 가능
- Claude SDK 연결 풀링으로 응답 시간 단축 가능
- 큰 문서 청크 분할로 메모리 사용량 최적화 가능
```

### B. 확장성 고려사항
```markdown
## 새로운 프로세서 추가 방법
1. `_run_parallel_functions()`에 함수 추가
2. 해당 프로세서용 `_call_*()` 래퍼 함수 구현
3. 실행 조건 로직 추가 (query_number 기반 등)
4. 결과 통합 로직에 새 프로세서 결과 처리 추가

## 설정 확장
- 프로세서별 개별 설정 섹션 추가 가능
- 실행 조건 설정 외부화 가능
- 병렬 처리 옵션 세분화 가능
```

### C. 디버깅과 모니터링
```markdown
## 로깅 포인트
- 각 단계별 처리 시간 측정
- 프로세서별 성공/실패 상태
- 세션 상태 변화 추적
- 메모리 사용량 모니터링

## 디버깅 도구
- `--verbose` 플래그로 상세 로그 출력
- 개별 프로세서 독립 실행 모드
- 세션 캐시 상태 검사 도구
- 결과 파일 구조 검증 도구
```

### D. 에러 복구 전략
```markdown
## 복구 가능한 오류
- 개별 프로세서 실패 → 다른 프로세서 결과로 부분 응답
- 네트워크 일시 장애 → 재시도 로직 추가 가능
- 세션 캐시 손상 → 새 세션으로 fallback

## 치명적 오류
- 설정 파일 파싱 실패 → 시스템 종료
- 모든 프로세서 실패 → 전체 실패 처리
- 디스크 공간 부족 → 저장 실패
```

이 문서를 통해 `unified_processor.py`의 전체적인 구조와 동작 방식을 체계적으로 이해할 수 있을 것입니다.