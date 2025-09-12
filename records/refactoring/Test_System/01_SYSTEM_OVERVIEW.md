# 테스트 데이터 생성 및 관리 체계 - 시스템 개요

## 1. 프로젝트 개요

### 1.1 구현 목표
- **파이프라인 각 단계별 테스트 데이터 생성 체계** 구축
- **conftest, fixture 활용** 실제 데이터 테스트 환경 구현
- **기존 코드 수정 없이** 데이터 기반 테스트 체계 구축

### 1.2 시작 단계
- **`workspace_preparation_v2.py`** 부터 구현 시작
- 기본틀 구축 후 다음 단계 확장
- 실제 PDF → Stage 처리 → 데이터 생성 플로우 검증

## 2. 폴더 구조 설계

### 2.1 전체 구조
```
tests/
├── conftest.py                          # 기본 설정 및 공통 fixture
├── schemas/
│   └── stage_schemas.py                 # 데이터 스키마 정의
├── fixtures/
│   ├── pdfs/                           # 입력용 PDF 파일들
│   └── ai_responses/                   # Mock 데이터 관리
├── data/
│   └── workspace_preparation/          # 생성된 테스트 데이터 저장
├── utils/
│   └── test_data_manager.py            # 데이터 관리 유틸리티
└── test_workspace_preparation_data_generation.py  # 메인 테스트 파일
```

### 2.2 폴더별 역할

#### **fixtures/**: 입력용 고정 데이터
- `pdfs/`: 실제 PDF 파일들 (테스트용 샘플 책)
- `ai_responses/`: Mock AI 응답 데이터 (JSON 파일들)

#### **data/**: 처리 결과/기대값 데이터
- **실제 기능이 생성/출력하는 데이터 형식 그대로 저장**
- 단계별 디렉토리로 구조화
- 다음 단계 입력 데이터도 함께 저장

#### **schemas/**: 데이터 스키마 검증
- 각 단계별 입출력 스키마 클래스 정의
- `validate()` 메서드로 데이터 무결성 검증
- 별도 파일로 버전 관리

#### **utils/**: 테스트 유틸리티
- `TestDataManager`: 데이터 로딩 및 체인 관리
- Mock 관련 유틸리티들

## 3. 데이터 플로우 설계

### 3.1 기본 플로우
```
실제 PDF → Stage 처리 → 스키마 검증 → 저장 → 다음 단계 입력 생성
```

### 3.2 단계간 체인 연결
- **stage1_output → stage2_input** 자동 변환
- `TestDataManager.create_stage_chain_data()` 활용
- 데이터 무결성 유지하며 파이프라인 연결

### 3.3 데이터 변환 방식
- **기존**: 폴더 경로 전달 방식
- **개선**: 실제 데이터 객체 직접 전달
- **장점**: 의존성 감소, 테스트 격리, 데이터 추적 가능

## 4. 테스트 전략 개요

### 4.1 pytest marker 기반 분류
```python
@pytest.mark.unit       # 빠른 단위 테스트 (Mock 사용)
@pytest.mark.integration  # 통합 테스트 (실제 API)
@pytest.mark.expensive    # 비용 발생 테스트 (AI API 등)
@pytest.mark.slow         # 느린 테스트 (대용량 PDF 등)
```

### 4.2 선택적 실행 전략
```bash
# 개발 중: 빠른 피드백
pytest -m "unit"

# 비용 절약: 외부 API 제외
pytest -m "not expensive"

# 전체 검증: 모든 테스트
pytest
```

## 5. 환경별 설정 관리

### 5.1 테스트 환경 분기
- **unit**: Mock AI 서비스 사용 (빠름, 무료)
- **integration**: 실제 API (제한된 호출)
- **full**: 모든 기능 활성화 (전체 검증)

### 5.2 환경 제어 방식
```bash
# 환경변수로 제어
TEST_ENV=unit pytest           # Mock 사용
TEST_ENV=integration pytest    # 실제 API 제한 사용
TEST_ENV=full pytest          # 모든 기능 사용
```

## 6. 검증 및 품질 관리

### 6.1 스키마 검증 원칙
- **expected_data fixture 불필요**: 실제 생성 데이터 기반 검증
- **스키마 검증만으로 데이터 무결성 보장**: 구조, 타입, 필수 필드 검증
- **저장 전 필수 검증**: 잘못된 데이터 저장 방지

### 6.2 데이터 저장 규칙
- **검증 통과한 데이터만 저장**
- **원본 형식 유지**: 실제 기능 출력 형식 그대로
- **단계별 디렉토리 구조**: 체계적인 데이터 관리
- **다음 단계 입력 자동 생성**: 파이프라인 연결성 보장

## 7. 핵심 구현 포인트

### 7.1 workspace_preparation_v2.py 분석 요점
- **AI API 호출 지점**: `analyze_chapters_with_ai()` 메서드
- **PDF 처리**: TocService, ChapterExtractionService 활용
- **출력 데이터**: normalized_book_title, created_folders 등
- **Mock 필요 지점**: AI 서비스 호출 부분

### 7.2 구현 시 주의사항
- **기존 코드 수정 금지**: workspace_preparation_v2.py 변경 불가
- **실제 PDF 필요**: fixtures/pdfs/에 테스트용 PDF 파일 배치
- **uv 의존성 관리**: 새로운 패키지는 uv를 통해 설치
- **비용 관리**: AI API 호출 최소화 전략 필요

이 문서는 테스트 시스템의 전체적인 구조와 개념을 이해하기 위한 개요서입니다. 
구체적인 구현 방법은 `02_IMPLEMENTATION_GUIDE.md`를 참조하세요.