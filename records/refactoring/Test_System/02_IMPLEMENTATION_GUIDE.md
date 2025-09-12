# 테스트 데이터 생성 및 관리 체계 - 구현 가이드

## 1. 핵심 구현 파일들

### 1.1 메인 테스트 파일: `test_workspace_preparation_data_generation.py`

#### **구현 목적**
- 실제 `WorkspacePreparationStage` 실행
- 생성된 데이터의 스키마 검증
- 검증된 데이터 저장
- 다음 단계 입력 데이터 생성

#### **핵심 구현 패턴**
```python
@pytest.fixture
def sample_pdf_path():
    """실제 PDF 파일 경로만 필요"""
    return Path("tests/fixtures/pdfs/sample_textbook.pdf")

class TestWorkspacePreparationDataGeneration:
    async def test_generate_complete_workspace_data(
        self, sample_pdf_path, config_manager, logger_factory
    ):
        # Given: 실제 Stage 인스턴스
        stage = WorkspacePreparationStage(config_manager, logger_factory)
        input_data = {"pdf_path": str(sample_pdf_path)}
        
        # When: 실제 처리 실행
        result = await stage.process(input_data)
        
        # Then: 스키마 검증
        from tests.schemas.stage_schemas import WorkspacePreparationOutput
        assert WorkspacePreparationOutput.validate(result)
        
        # 검증된 데이터 저장
        self._save_test_data("workspace_preparation_output", result)
        
        # 다음 단계 입력 생성
        next_input = self._create_next_stage_input(result)
        self._save_test_data("content_processing_input", next_input)
```

#### **중요 사항**
- **expected_data fixture 사용 안 함**: 실제 생성 데이터만 사용
- **스키마 검증 필수**: 저장 전 반드시 검증 실행
- **원본 데이터 형식 유지**: JSON 변환 없이 실제 출력 형식 그대로

### 1.2 데이터 매니저: `tests/utils/test_data_manager.py`

#### **축소된 역할 정의**
```python
class TestDataManager:
    """테스트 데이터 로딩 및 체인 관리"""
    
    def __init__(self):
        self.data_dir = Path("tests/data")
        self.fixtures_dir = Path("tests/fixtures")
    
    def load_expected_data(self, stage: str, data_type: str) -> Dict[str, Any]:
        """기대값 데이터 로딩"""
        
    def create_stage_chain_data(self, start_stage: str) -> Dict[str, Any]:
        """단계별 체인 데이터 생성"""
        
    def validate_output_schema(self, stage: str, data: Dict) -> bool:
        """스키마 검증 수행"""
```

#### **PDF 관련 기능 제외 이유**
- PDF는 workspace_preparation에서만 필요
- 단계별 전용 fixture가 더 명확하고 효율적
- TestDataManager는 데이터 체인 관리에만 집중

### 1.3 스키마 정의: `tests/schemas/stage_schemas.py`

#### **WorkspacePreparationOutput 스키마**
```python
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class WorkspacePreparationOutput:
    """워크스페이스 준비 단계 출력 스키마"""
    schema_version: str = "1.0"
    success: bool
    normalized_book_title: str
    total_chapters: int
    output_directory: str
    created_folders: List[Dict[str, Any]]
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        """출력 데이터 스키마 검증"""
        required_fields = [
            'success', 'normalized_book_title', 
            'total_chapters', 'output_directory', 'created_folders'
        ]
        
        # 필수 필드 체크
        if not all(field in data for field in required_fields):
            return False
            
        # 타입 체크
        if not isinstance(data['created_folders'], list):
            return False
            
        return True
```

#### **ContentProcessingInput 스키마**
```python
@dataclass  
class ContentProcessingInput:
    """컨텐츠 처리 단계 입력 스키마"""
    schema_version: str = "1.0" 
    workspace_data: Dict[str, Any]
    book_directory: str
    chapter_folders: List[Dict[str, Any]]
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        """입력 데이터 스키마 검증"""
        # 구현 로직
```

### 1.4 conftest.py 설정

#### **기본 fixture들**
```python
import pytest
from tests.utils.test_data_manager import TestDataManager
from utils.config_manager import ConfigManager

@pytest.fixture(scope="session")
def test_data_manager():
    """테스트 데이터 매니저"""
    return TestDataManager()

@pytest.fixture(scope="session")
def config_manager():
    """테스트용 설정 매니저"""
    config = ConfigManager()
    config.config['test'] = {
        'enabled': True,
        'selected_chapters': [1, 2]  # 빠른 테스트용
    }
    return config

@pytest.fixture(scope="session") 
def logger_factory():
    """테스트용 로거 팩토리"""
    return LoggerFactory()
```

#### **환경별 설정 분기**
```python
@pytest.fixture(scope="session")
def test_environment():
    """테스트 환경 설정"""
    return os.getenv("TEST_ENV", "unit")

@pytest.fixture(scope="session") 
def config_manager(test_environment):
    """환경별 설정"""
    config = ConfigManager()
    
    if test_environment == "unit":
        config.config['ai'] = {'mock_enabled': True}
    elif test_environment == "integration":  
        config.config['ai'] = {'mock_enabled': False, 'max_calls': 5}
    else:  # full
        config.config['ai'] = {'mock_enabled': False}
        
    return config
```

## 2. Mock 데이터 관리 체계

### 2.1 Mock 폴더 구조
```
tests/fixtures/ai_responses/
├── chapters_analysis_simple.json     # 간단한 책 (2-3장)
├── chapters_analysis_complex.json    # 복잡한 책 (10+ 장)
├── chapters_analysis_error.json      # 에러 케이스
└── toc_extraction_responses/
    ├── success_response.json
    └── failure_response.json
```

### 2.2 MockAIResponseLoader 유틸리티
```python
class MockAIResponseLoader:
    """AI 응답 Mock 데이터 로더"""
    
    def get_chapters_analysis_response(self, scenario: str = "simple") -> Dict[str, Any]:
        """장 분석 Mock 응답"""
        
    def get_toc_extraction_response(self, success: bool = True) -> Dict[str, Any]:
        """목차 추출 Mock 응답"""
        
    def create_custom_response(self, chapters_count: int, success: bool = True) -> Dict[str, Any]:
        """동적 Mock 응답 생성"""
```

### 2.3 환경변수 기반 Mock 전환
```bash
# Mock 사용 (기본, 빠름)
USE_AI_MOCK=true pytest -m "unit"

# 실제 AI 사용 (비용 발생)
USE_AI_MOCK=false pytest -m "integration"
```

## 3. 구현 우선순위

### 3.1 1차: 기본틀 구축
1. **conftest.py**: 기본 설정 및 공통 fixture
2. **TestDataManager**: 축소된 역할로 구현  
3. **stage_schemas.py**: WorkspacePreparationOutput 스키마
4. **메인 테스트 파일**: 기본 데이터 생성 테스트

### 3.2 2차: 확장 및 최적화
1. **Mock 데이터 관리**: MockAIResponseLoader 구현
2. **환경별 설정**: 단위/통합 테스트 분기
3. **스키마 확장**: ContentProcessingInput 및 추가 검증
4. **다음 단계 준비**: content_processing 단계 연결

## 4. 주의사항 및 제약조건

### 4.1 구현 제약
- **기존 코드 수정 금지**: `workspace_preparation_v2.py` 변경 불가
- **실제 PDF 파일**: `fixtures/pdfs/`에 테스트용 PDF 배치 필요
- **uv 의존성 관리**: 새로운 패키지는 `uv add` 명령어 사용
- **한국 시간 기록**: 파일 생성 시 한국 시간으로 목차 작성

### 4.2 성능 고려사항
- **AI API 호출 최소화**: 비용 관리를 위한 Mock 활용
- **캐싱 전략**: 동일한 테스트 데이터 재사용
- **병렬 테스트**: 리소스 사용량 고려한 테스트 설계
- **빠른 피드백**: 단위 테스트 우선 실행으로 개발 효율성 확보

### 4.3 파일 작업 규칙
- **목차 작성**: 모든 코드 파일 맨 위에 목차 형식으로 작성
- **파일 상태 관리**: 수정 시 새 파일 생성(_v2 접미사), 삭제 시 상태 필드 표시
- **데이터 형식 유지**: 실제 기능 출력 형식 그대로 저장, JSON 변환 최소화

## 5. 검증 체크리스트

### 5.1 구현 완료 확인 사항
- [ ] conftest.py 기본 설정 구현
- [ ] TestDataManager 축소 버전 구현  
- [ ] WorkspacePreparationOutput 스키마 정의
- [ ] 메인 테스트 파일 기본 구조 구현
- [ ] 실제 PDF 파일 fixtures에 배치
- [ ] 스키마 검증 → 저장 플로우 구현
- [ ] 다음 단계 입력 데이터 생성 로직
- [ ] Mock 전환 기본 구조 (선택사항)

### 5.2 데이터 검증 기준
- [ ] 스키마 검증 통과
- [ ] 필수 필드 모두 존재  
- [ ] 데이터 타입 정확성
- [ ] 다음 단계 호환성
- [ ] 원본 형식 보존

이 가이드를 따라 구현하면 견고하고 확장 가능한 테스트 데이터 관리 체계를 구축할 수 있습니다.