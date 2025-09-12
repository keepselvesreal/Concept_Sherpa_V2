# 구현 안내 문서 - WorkspacePreparationStage 메모리 기반 테스트 시스템 

## 1. 개요

### 1.1 구현 목표
- WorkspacePreparationStage의 **완전 메모리 기반** 테스트 시스템 구축
- 파일 시스템 의존성 제거 및 실제 데이터 기반 픽스처 활용
- AI 서비스 v4 업그레이드 및 자동 갱신 가능한 테스트 환경

### 1.2 핵심 변경사항
```
기존: PDF → 폴더/파일 생성 → 경로 전달
개선: PDF → 메모리 데이터 처리 → 실제 데이터 전달
```

## 2. 구현 작업 단계

### Phase 1: ChapterExtractionService_v4 생성

#### 작업 내용
1. **파일 복사**: `chapter_extraction_service_v3.py` → `chapter_extraction_service_v4.py`
2. **AI 서비스 업그레이드**:
   ```python
   # 변경 1: 임포트 수정 (라인 21)
   # 기존
   from services.ai_service_v3 import AIService
   # 수정  
   from services.ai_service_v4 import AIService
   
   # 변경 2: 쿼리 메서드 수정 (라인 126)
   # 기존
   response_text = await self.ai_service.query(full_prompt, additional_data)
   # 수정
   response_text = await self.ai_service.query_single_request(full_prompt, additional_data)
   ```

#### 파일 목차 작성 규칙
```
# 생성 시간: Tue Sep  9 17:46:31 KST 2025
# 핵심 내용: 장 추출 및 처리 서비스 v4 (AI 서비스 v4 적용)
# 상세 내용:
#   - ChapterExtractionService (라인 XX-XXX): 메인 장 추출 서비스 클래스
#   - count_chapters_with_ai (라인 XX-XXX): AI 기반 장 분석 메서드 (ai_service_v4 + query_single_request 사용)
#   - [기타 메서드들은 v3과 동일]
# 상태: active
# 참조: chapter_extraction_service_v3.py (AI 서비스 v4 적용)
```

### Phase 2: WorkspacePreparationStage 완전 개편

#### 작업 내용
1. **임포트 변경**: ChapterExtractionService_v4 사용
2. **폴더/파일 생성 로직 완전 제거**:
   - `create_output_directories()` 메서드 제거
   - `save_toc_file()` 메서드 제거  
   - `create_chapter_folders()` 메서드 제거
3. **메모리 기반 데이터 처리 구현**
4. **반환값 구조 변경**: `{success, data, error}` 형태

#### 새로운 process 메서드 구조
```python
async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """메모리 기반 워크스페이스 준비 처리"""
    try:
        pdf_path = input_data.get('pdf_path')
        
        # Step 1: PDF 목차 추출 (메모리에 저장)
        # toc_data 구조: {'extraction_info': {...}, 'toc_structure': [...]}
        toc_data = await self.extract_toc_from_pdf(pdf_path)
        
        # Step 2: AI 기반 장 분석 (실제 목차 데이터 전달)
        chapters_analysis = await self.analyze_chapters_with_ai(toc_data['data'])
        
        # Step 3: 장별 콘텐츠 추출 (메모리에 저장) 
        chapters_data = []
        for chapter_info in chapters_analysis['chapters_info']:
            content_text = self.chapter_extraction_service.extract_pdf_content(
                pdf_path, chapter_info['start_page'], chapter_info['end_page']
            )
            
            # 해당 장의 목차 항목들 추출
            chapter_toc = self._extract_chapter_toc_items(
                toc_data['data']['toc_structure'], 
                chapter_info['title']
            )
            
            chapters_data.append({
                'chapter_title': chapter_info['title'],
                'chapter_toc': chapter_toc,  
                'content_text': content_text,
                'metadata': {
                    'start_page': chapter_info['start_page'],
                    'end_page': chapter_info['end_page']
                }
            })
        
        return {
            'success': True,
            'data': {
                'book_metadata': {
                    'title': self.book_title,  # 🟢 추가: 원본 책 제목
                    'normalized_title': self.normalized_book_title,
                    'total_chapters': len(chapters_analysis['chapters_info'])
                },
                'chapters_data': chapters_data,
                'raw_toc_data': toc_data['data']
                # 🔄 제거: ai_analysis (chapters_analysis 반환값에서 제외)
            },
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'error': str(e)
        }

def _extract_chapter_toc_items(self, full_toc_structure: List[Dict], chapter_title: str) -> List[Dict]:
    """해당 장에 속하는 목차 항목들만 추출"""
    # 장 제목으로 시작하는 항목 및 하위 항목들 필터링
    # 구현 로직 필요
    pass
```

### Phase 3: 테스트 시스템 구현

#### 3.1 conftest.py 수정
```python
import pytest
import json
import os
from pathlib import Path

# pytest 커스텀 옵션 정의
def pytest_addoption(parser):
    """--regen-fixtures 옵션 정의"""
    parser.addoption(
        "--regen-fixtures",
        action="store_true",
        default=False,
        help="테스트 픽스처 데이터를 강제로 재생성합니다"
    )

# 기본 픽스처들
@pytest.fixture(scope="session")
def config_manager():
    """ConfigManager fixture"""
    from utils.config_manager import ConfigManager
    return ConfigManager()

@pytest.fixture(scope="session") 
def test_logger():
    """Logger 직접 사용 fixture"""
    from utils.logger_v2 import Logger
    return Logger("test_workspace", logs_base_dir="tests/logs")

@pytest.fixture(scope="session")
def real_pdf_path():
    """실제 PDF 파일 경로"""
    pdf_path = Path("tests/fixtures/pdfs/sample_book.pdf")
    if not pdf_path.exists():
        pytest.skip(f"실제 PDF 파일이 없습니다: {pdf_path}")
    return str(pdf_path)

@pytest.fixture(scope="session")
def toc_data(request):
    """TOC 데이터 (추출 결과이면서 AI 분석 입력)"""
    data_path = Path("tests/data/workspace_preparation/toc_data.json")
    
    # --regen-fixtures 옵션 체크
    if request.config.getoption("--regen-fixtures"):
        regenerate_test_data()
    
    if not data_path.exists():
        pytest.skip(
            "TOC 데이터가 없습니다. 다음 중 하나를 실행하세요:\n"
            "1. pytest test_workspace_preparation_data_generation.py\n"
            "2. pytest --regen-fixtures"
        )
    
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def regenerate_test_data():
    """테스트 데이터 자동 재생성"""
    print("🔄 테스트 데이터 재생성 중...")
    # TODO: 데이터 재생성 로직 구현
    print("✅ 테스트 데이터 재생성 완료")
```

#### 3.2 스키마 정의 파일 생성 (tests/schemas/stage_schemas.py)
```python
# 생성 시간: Tue Sep  9 17:46:31 KST 2025
# 핵심 내용: WorkspacePreparationStage 출력 데이터 스키마 정의
# 상세 내용:
#   - WorkspacePreparationOutput (라인 XX-XXX): 워크스페이스 준비 단계 출력 스키마 클래스
#   - validate 클래스 메서드 (라인 XX-XXX): 출력 데이터 검증 메서드
# 상태: active

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

@dataclass
class WorkspacePreparationOutput:
    """워크스페이스 준비 단계 출력 스키마"""
    schema_version: str = "1.0"
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    
    @classmethod
    def validate(cls, result: Dict[str, Any]) -> bool:
        """출력 데이터 스키마 검증"""
        # 필수 필드 체크
        required_fields = ['success', 'data', 'error']
        if not all(field in result for field in required_fields):
            return False
        
        # success가 True인 경우 data 필드 검증
        if result['success']:
            if not result['data']:
                return False
                
            data = result['data']
            required_data_fields = ['book_metadata', 'chapters_data']
            if not all(field in data for field in required_data_fields):
                return False
                
            # chapters_data 구조 검증
            if not isinstance(data['chapters_data'], list):
                return False
                
            for chapter in data['chapters_data']:
                chapter_required_fields = ['chapter_title', 'toc_structure', 'content_text', 'metadata']
                if not all(field in chapter for field in chapter_required_fields):
                    return False
        
        return True
```

#### 3.3 데이터 생성 테스트 파일 생성
```python
# test_workspace_preparation_data_generation.py
# 생성 시간: Tue Sep  9 17:46:31 KST 2025
# 핵심 내용: WorkspacePreparationStage 실제 데이터 생성 및 픽스처 저장 테스트
# 상태: active

import pytest
import json
import asyncio
from pathlib import Path

class TestWorkspacePreparationDataGeneration:
    """실제 PDF로 데이터 생성 → 픽스처 저장"""
    
    async def test_generate_workspace_data(self, real_pdf_path, config_manager, test_logger):
        """실제 PDF를 사용한 워크스페이스 데이터 생성 및 저장"""
        
        # WorkspacePreparationStage 실행
        from stages.workspace_preparation_v2 import WorkspacePreparationStage
        stage = WorkspacePreparationStage(config_manager, None)  # logger_factory 대신 None
        stage.logger = test_logger
        
        # 실제 PDF 처리
        result = await stage.process({"pdf_path": real_pdf_path})
        
        # 기본 검증
        assert result['success'] is True
        assert 'data' in result
        assert result['data'] is not None
        
        # 픽스처 저장 (개별 데이터 저장)
        self._save_test_data("title", result['data']['book_metadata']['title'])
        self._save_test_data("raw_toc_data", result['data']['raw_toc_data'])
        self._save_test_data("chapters_data", result['data']['chapters_data'])
        
        print(f"✅ 테스트 데이터 생성 완료: {len(result['data']['chapters_data'])}개 장")
    
    def _save_test_data(self, name: str, data, format: str = "json"):
        """테스트 데이터 저장 - 지정된 형식으로 저장"""
        data_dir = Path("tests/data/workspace_preparation")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        if format == "md":
            # Markdown 형식으로 저장
            file_path = data_dir / f"{name}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(data))
        elif format == "json":
            # JSON 형식으로 저장
            file_path = data_dir / f"{name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"지원하지 않는 형식입니다: {format}. 'md' 또는 'json'을 사용하세요.")
        
        print(f"💾 저장: {file_path} (형식: {format})")
```

#### 3.4 메인 로직 테스트 파일 생성
```python
# test_workspace_preparation.py
# 생성 시간: Tue Sep  9 17:46:31 KST 2025
# 핵심 내용: WorkspacePreparationStage 개별 메서드 로직 검증 (픽스처 활용)
# 상태: active

import pytest
from schemas.stage_schemas import WorkspacePreparationOutput

class TestWorkspacePreparationLogic:
    """픽스처 데이터 활용한 개별 메서드 로직 검증"""
    
    async def test_extract_toc_from_pdf_logic(self, real_pdf_path, toc_data, config_manager, test_logger):
        """실제 PDF → TOC 추출 결과가 픽스처와 동일한지 검증"""
        from stages.workspace_preparation_v2 import WorkspacePreparationStage
        
        stage = WorkspacePreparationStage(config_manager, None)
        stage.logger = test_logger
        
        # 실제 PDF로 TOC 추출
        result = await stage.extract_toc_from_pdf(real_pdf_path)
        
        # 픽스처 데이터와 비교
        assert result['success'] is True
        assert result['data']['toc_structure'] == toc_data['toc_structure']
        assert len(result['data']['toc_structure']) == len(toc_data['toc_structure'])
    
    async def test_analyze_chapters_with_ai_logic(self, toc_data, config_manager, test_logger):
        """실제 목차 데이터 → AI 분석 결과 구조 검증"""
        from stages.workspace_preparation_v2 import WorkspacePreparationStage
        
        stage = WorkspacePreparationStage(config_manager, None)
        stage.logger = test_logger
        
        # 실제 목차 데이터로 AI 분석
        result = await stage.analyze_chapters_with_ai(toc_data)
        
        # 결과 구조 검증
        assert result['success'] is True
        assert 'chapters_info' in result
        assert isinstance(result['chapters_info'], list)
        assert len(result['chapters_info']) > 0
        
        # 각 장 정보 구조 검증
        for chapter_info in result['chapters_info']:
            assert 'title' in chapter_info
            assert 'start_page' in chapter_info
            assert 'end_page' in chapter_info
    
    def test_workspace_preparation_output_schema(self, toc_data):
        """워크스페이스 준비 출력 스키마 검증"""
        # 테스트용 결과 데이터 구성
        test_result = {
            'success': True,
            'data': {
                'book_metadata': {'title': 'Test Book', 'normalized_title': 'Test_Book', 'total_chapters': 2},
                'chapters_data': [
                    {
                        'chapter_title': 'Chapter 1',
                        'toc_structure': toc_data['toc_structure'],
                        'content_text': 'Sample content',
                        'metadata': {'start_page': 1, 'end_page': 10}
                    }
                ]
            },
            'error': None
        }
        
        # 스키마 검증
        assert WorkspacePreparationOutput.validate(test_result)
```

## 3. 실행 방법

### 구현 완료 후 테스트 실행 순서
```bash
# 1단계: 데이터 생성 (PDF 파일 준비 후)
pytest test_workspace_preparation_data_generation.py

# 2단계: 로직 테스트
pytest test_workspace_preparation.py

# 자동 갱신
pytest --regen-fixtures
```

### 디렉토리 생성 필요
```bash
# 테스트 디렉토리 구조 생성
mkdir -p tests/fixtures/pdfs
mkdir -p tests/data/workspace_preparation
mkdir -p tests/schemas
mkdir -p tests/logs
```

## 4. 주의사항

### 4.1 파일 작업 규칙
- **목차 작성**: 모든 코드 파일 맨 위에 목차 형식으로 작성
- **한국 시간 기록**: `date` 명령어로 확인한 한국 시간 사용
- **파일 연속성**: 기존 파일 수정 시 _v2, _v4 등 접미사 사용

### 4.2 구현 제약사항  
- **기존 코드 최대한 활용**: v3 → v4 변경 시 핵심 로직 유지
- **메모리 기반 처리**: 파일 시스템 의존성 완전 제거
- **실제 데이터 기반**: Mock 대신 실제 PDF 처리 결과 활용

### 4.3 성능 고려사항
- **AI API 호출 최소화**: 테스트 시 비용 관리
- **메모리 사용량**: 대용량 PDF 처리 시 메모리 효율성
- **테스트 실행 속도**: 픽스처 기반 빠른 로직 검증

## 5. 구현 검증 체크리스트

- [ ] ChapterExtractionService_v4.py 생성 및 AI 서비스 v4 적용
- [ ] WorkspacePreparationStage 메모리 기반 구조로 완전 개편
- [ ] conftest.py 픽스처 및 --regen-fixtures 옵션 구현
- [ ] 스키마 정의 파일 작성
- [ ] 데이터 생성 테스트 파일 구현
- [ ] 메인 로직 테스트 파일 구현
- [ ] 실제 PDF 파일 배치 (fixtures/pdfs/)
- [ ] 전체 테스트 실행 및 검증

이 문서를 참고하여 단계별로 구현을 진행하시면 됩니다.