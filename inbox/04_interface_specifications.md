# 🔌 인터페이스 명세서

## 🎯 개요

이 문서는 리팩토링된 책 파이프라인의 모든 인터페이스와 데이터 모델을 정의합니다. 각 인터페이스는 느슨한 결합을 위해 의존성 주입 패턴을 사용하며, 타입 힌트를 통해 명확한 계약을 제공합니다.

## 📋 도메인 모델 정의

### Pipeline Domain

#### PipelineResult (값 객체)
```python
# 생성 시간: 2025-09-03 15:00:00  
# 핵심 내용: 파이프라인 실행 결과를 나타내는 값 객체
# 상세 내용:
#   - PipelineResult 클래스 (15-35): 파이프라인 실행 결과 데이터 저장
#   - PipelineStage 열거형 (37-45): 파이프라인 실행 단계 정의
# 상태: active
# 참조: 신규 생성

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime

@dataclass(frozen=True)
class PipelineResult:
    """파이프라인 실행 결과"""
    is_success: bool
    step_completed: int
    progress_percent: float
    data: Dict[str, Any]
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            object.__setattr__(self, 'warnings', [])
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """실행 시간을 초 단위로 반환"""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

class PipelineStage(Enum):
    """파이프라인 실행 단계"""
    WORKSPACE_PREP = "workspace_preparation"
    CHAPTER_INTEGRATION = "chapter_integration"
    NODE_PROCESSING = "node_processing"
    ENHANCED_TOC = "enhanced_toc_generation"
```

#### IPipelineOrchestrator (인터페이스)
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path

class IPipelineOrchestrator(ABC):
    """파이프라인 오케스트레이터 인터페이스"""
    
    @abstractmethod
    async def execute(
        self,
        pdf_path: Path,
        selected_chapters: Optional[List[int]] = None,
        user_options: Optional[Dict[str, Any]] = None
    ) -> PipelineResult:
        """전체 파이프라인을 실행합니다"""
        pass
    
    @abstractmethod
    async def execute_stage(
        self,
        stage: PipelineStage,
        context: Dict[str, Any]
    ) -> PipelineResult:
        """특정 단계만 실행합니다"""
        pass
    
    @abstractmethod
    async def validate_prerequisites(self, pdf_path: Path) -> bool:
        """실행 전 전제조건을 검증합니다"""
        pass
    
    @abstractmethod
    def get_progress(self) -> float:
        """현재 진행 상황을 반환합니다"""
        pass
```

### Chapter Domain

#### ChapterInfo (엔티티)
```python
@dataclass
class ChapterInfo:
    """장 정보 엔티티"""
    chapter_number: int
    title: str
    folder_path: str
    page_range: str
    content_file: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def start_page(self) -> Optional[int]:
        """시작 페이지 번호"""
        if self.page_range and '-' in self.page_range:
            try:
                return int(self.page_range.split('-')[0])
            except ValueError:
                return None
        return None
    
    @property 
    def end_page(self) -> Optional[int]:
        """끝 페이지 번호"""
        if self.page_range and '-' in self.page_range:
            try:
                return int(self.page_range.split('-')[1])
            except ValueError:
                return None
        return None
```

#### ChapterWorkspace (애그리게이트 루트)
```python
@dataclass
class ChapterWorkspace:
    """장별 워크스페이스 애그리게이트"""
    book_title: str
    normalized_title: str
    output_directory: Path
    chapters: List[ChapterInfo]
    created_at: datetime
    
    def get_chapter_by_number(self, chapter_number: int) -> Optional[ChapterInfo]:
        """장 번호로 장 정보를 조회"""
        for chapter in self.chapters:
            if chapter.chapter_number == chapter_number:
                return chapter
        return None
    
    def get_selected_chapters(self, chapter_numbers: List[int]) -> List[ChapterInfo]:
        """선택된 장들만 반환"""
        return [
            chapter for chapter in self.chapters
            if chapter.chapter_number in chapter_numbers
        ]
    
    def add_chapter(self, chapter: ChapterInfo) -> None:
        """새 장 추가"""
        # 중복 체크
        existing = self.get_chapter_by_number(chapter.chapter_number)
        if existing:
            raise ValueError(f"Chapter {chapter.chapter_number} already exists")
        
        self.chapters.append(chapter)
        # 번호순 정렬
        self.chapters.sort(key=lambda x: x.chapter_number)
```

#### WorkspaceResult (값 객체)
```python
@dataclass(frozen=True)
class WorkspaceResult:
    """워크스페이스 생성 결과"""
    success: bool
    created_folders: List[Dict[str, str]]
    total_chapters: int
    workspace_path: Path
    error_details: Optional[str] = None
    
    @property
    def created_folder_count(self) -> int:
        """생성된 폴더 수"""
        return len(self.created_folders)
```

#### IChapterIntegrationService (인터페이스)
```python
class IChapterIntegrationService(ABC):
    """장 통합 서비스 인터페이스"""
    
    @abstractmethod
    async def integrate_chapters_sequentially(
        self,
        workspace: ChapterWorkspace,
        selected_chapters: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """장별 정보를 순차적으로 통합"""
        pass
    
    @abstractmethod
    async def integrate_single_chapter(
        self,
        chapter: ChapterInfo,
        workspace_path: Path
    ) -> Dict[str, Any]:
        """단일 장 정보를 통합"""
        pass
    
    @abstractmethod
    async def validate_chapter_data(self, chapter: ChapterInfo) -> bool:
        """장 데이터 유효성 검증"""
        pass
```

### TOC Domain

#### TOCItem (엔티티)
```python
@dataclass
class TOCItem:
    """목차 항목 엔티티"""
    id: int
    title: str
    level: int
    start_page: int
    end_page: Optional[int] = None
    children: List['TOCItem'] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.metadata is None:
            self.metadata = {}
    
    def add_child(self, child: 'TOCItem') -> None:
        """하위 항목 추가"""
        if child.level <= self.level:
            raise ValueError("Child level must be greater than parent level")
        self.children.append(child)
    
    def get_page_count(self) -> int:
        """페이지 수 계산"""
        if self.end_page:
            return self.end_page - self.start_page + 1
        return 1
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'title': self.title,
            'level': self.level,
            'start_page': self.start_page,
            'end_page': self.end_page,
            'children': [child.to_dict() for child in self.children],
            'metadata': self.metadata
        }
```

#### TOCResult (값 객체)
```python
@dataclass(frozen=True)
class TOCResult:
    """목차 추출 결과"""
    success: bool
    toc_items: List[TOCItem]
    extraction_info: Dict[str, Any]
    total_pages: int
    extraction_method: str
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            object.__setattr__(self, 'warnings', [])
    
    @property
    def item_count(self) -> int:
        """전체 항목 수"""
        return len(self.toc_items)
    
    @property
    def max_level(self) -> int:
        """최대 계층 레벨"""
        if not self.toc_items:
            return 0
        return max(item.level for item in self.toc_items)
```

#### ITOCExtractor (인터페이스)
```python
class ITOCExtractor(ABC):
    """목차 추출기 인터페이스"""
    
    @abstractmethod
    async def extract_toc(self, pdf_path: Path) -> TOCResult:
        """PDF에서 목차를 추출합니다"""
        pass
    
    @abstractmethod
    async def validate_toc_structure(self, toc_items: List[TOCItem]) -> bool:
        """목차 구조 유효성 검증"""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """지원하는 파일 형식 목록"""
        pass
```

#### IEnhancedTOCGenerator (인터페이스)
```python
class IEnhancedTOCGenerator(ABC):
    """향상된 목차 생성기 인터페이스"""
    
    @abstractmethod
    async def generate_enhanced_toc(
        self,
        original_toc: TOCResult,
        chapter_data: Dict[str, Any],
        enhancement_options: Optional[Dict[str, Any]] = None
    ) -> str:
        """향상된 목차를 생성합니다"""
        pass
    
    @abstractmethod
    async def validate_generation_input(
        self,
        toc_result: TOCResult,
        chapter_data: Dict[str, Any]
    ) -> bool:
        """생성 입력 데이터 검증"""
        pass
    
    @abstractmethod
    def get_output_formats(self) -> List[str]:
        """지원하는 출력 형식 목록"""
        pass
```

### Document Domain

#### NodeDocument (엔티티)
```python
@dataclass
class NodeDocument:
    """노드 문서 엔티티"""
    node_id: str
    content: str
    metadata: Dict[str, Any]
    processing_status: str = "pending"
    created_at: datetime = None
    processed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def mark_processing_started(self) -> None:
        """처리 시작 마킹"""
        self.processing_status = "processing"
    
    def mark_processing_completed(self) -> None:
        """처리 완료 마킹"""
        self.processing_status = "completed"
        self.processed_at = datetime.now()
    
    def mark_processing_failed(self, error_message: str) -> None:
        """처리 실패 마킹"""
        self.processing_status = "failed"
        self.metadata["error_message"] = error_message
        self.processed_at = datetime.now()
    
    @property
    def is_completed(self) -> bool:
        """처리 완료 여부"""
        return self.processing_status == "completed"
    
    @property
    def processing_duration(self) -> Optional[float]:
        """처리 시간 (초)"""
        if self.processed_at and self.created_at:
            return (self.processed_at - self.created_at).total_seconds()
        return None
```

#### ProcessingResult (값 객체)
```python
@dataclass(frozen=True)
class ProcessingResult:
    """노드 처리 결과"""
    success: bool
    processed_nodes: int
    processing_results: List[Dict[str, Any]]
    total_processing_time: float
    failed_nodes: List[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.failed_nodes is None:
            object.__setattr__(self, 'failed_nodes', [])
        if self.warnings is None:
            object.__setattr__(self, 'warnings', [])
    
    @property
    def success_rate(self) -> float:
        """성공률 계산"""
        total = self.processed_nodes + len(self.failed_nodes)
        if total == 0:
            return 0.0
        return self.processed_nodes / total
    
    @property
    def average_processing_time(self) -> float:
        """평균 처리 시간"""
        if self.processed_nodes == 0:
            return 0.0
        return self.total_processing_time / self.processed_nodes
```

#### INodeDocumentProcessor (인터페이스)
```python
class INodeDocumentProcessor(ABC):
    """노드 문서 처리기 인터페이스"""
    
    @abstractmethod
    async def process_chapter(
        self,
        chapter_info: ChapterInfo,
        processing_options: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        """장의 노드 문서들을 처리합니다"""
        pass
    
    @abstractmethod
    async def process_single_node(
        self,
        node: NodeDocument,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """단일 노드를 처리합니다"""
        pass
    
    @abstractmethod
    async def process_batch(
        self,
        nodes: List[NodeDocument],
        batch_size: int = 5
    ) -> ProcessingResult:
        """노드들을 배치로 처리합니다"""
        pass
    
    @abstractmethod
    def validate_node_content(self, node: NodeDocument) -> bool:
        """노드 내용 유효성 검증"""
        pass
```

#### IDocumentIntegrator (인터페이스)
```python
class IDocumentIntegrator(ABC):
    """문서 통합기 인터페이스"""
    
    @abstractmethod
    async def integrate_documents_for_chapter(
        self,
        chapter: ChapterInfo,
        processed_results: ProcessingResult
    ) -> Dict[str, Any]:
        """장별 문서들을 통합합니다"""
        pass
    
    @abstractmethod
    async def generate_chapter_summary(
        self,
        chapter: ChapterInfo,
        integration_data: Dict[str, Any]
    ) -> str:
        """장 요약을 생성합니다"""
        pass
    
    @abstractmethod
    def validate_integration_data(
        self,
        data: Dict[str, Any]
    ) -> bool:
        """통합 데이터 유효성 검증"""
        pass
```

## 🔧 인프라스트럭처 인터페이스

### AI Provider Interface

#### IAIProvider (인터페이스)
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, AsyncGenerator
import asyncio

class IAIProvider(ABC):
    """AI 프로바이더 기본 인터페이스"""
    
    @abstractmethod
    async def analyze_content(
        self,
        content: str,
        system_prompt_key: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """콘텐츠를 분석합니다"""
        pass
    
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """응답을 생성합니다"""
        pass
    
    @abstractmethod
    async def stream_response(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """스트리밍 응답을 생성합니다"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """프로바이더 사용 가능 여부"""
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """연결 상태 검증"""
        pass
    
    @abstractmethod
    def get_provider_info(self) -> Dict[str, Any]:
        """프로바이더 정보 반환"""
        pass
```

#### IPromptManager (인터페이스)
```python
class IPromptManager(ABC):
    """프롬프트 관리자 인터페이스"""
    
    @abstractmethod
    def load_prompts(self, prompt_file: str) -> Dict[str, Any]:
        """프롬프트 파일을 로드합니다"""
        pass
    
    @abstractmethod
    def get_system_prompt(self, key: str) -> Optional[str]:
        """시스템 프롬프트를 반환합니다"""
        pass
    
    @abstractmethod
    def get_domain_prompt(self, domain: str, prompt_key: str) -> Optional[str]:
        """도메인별 프롬프트를 반환합니다"""
        pass
    
    @abstractmethod
    def format_prompt(
        self,
        template: str,
        variables: Dict[str, Any]
    ) -> str:
        """프롬프트 템플릿을 포맷팅합니다"""
        pass
    
    @abstractmethod
    def validate_prompt_template(self, template: str) -> bool:
        """프롬프트 템플릿 유효성 검증"""
        pass
```

### Logging Interface

#### ILoggingService (인터페이스)
```python
class ILoggingService(ABC):
    """로깅 서비스 인터페이스"""
    
    @abstractmethod
    def log_operation_start(
        self,
        operation_name: str,
        context: Dict[str, Any]
    ) -> str:
        """작업 시작 로깅, 작업 ID 반환"""
        pass
    
    @abstractmethod
    def log_operation_success(
        self,
        operation_id: str,
        result: Dict[str, Any]
    ) -> None:
        """작업 성공 로깅"""
        pass
    
    @abstractmethod
    def log_operation_error(
        self,
        operation_id: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """작업 오류 로깅"""
        pass
    
    @abstractmethod
    def log_metric(
        self,
        metric_name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """메트릭 로깅"""
        pass
    
    @abstractmethod
    def get_operation_logs(
        self,
        operation_id: str
    ) -> List[Dict[str, Any]]:
        """작업 로그 조회"""
        pass
```

### File System Interface

#### IFileSystemManager (인터페이스)
```python
class IFileSystemManager(ABC):
    """파일 시스템 관리자 인터페이스"""
    
    @abstractmethod
    async def create_directory(
        self,
        path: Path,
        exist_ok: bool = True
    ) -> bool:
        """디렉터리 생성"""
        pass
    
    @abstractmethod
    async def write_file(
        self,
        path: Path,
        content: str,
        encoding: str = "utf-8"
    ) -> bool:
        """파일 쓰기"""
        pass
    
    @abstractmethod
    async def read_file(
        self,
        path: Path,
        encoding: str = "utf-8"
    ) -> Optional[str]:
        """파일 읽기"""
        pass
    
    @abstractmethod
    async def copy_file(
        self,
        source: Path,
        destination: Path
    ) -> bool:
        """파일 복사"""
        pass
    
    @abstractmethod
    async def delete_path(
        self,
        path: Path,
        recursive: bool = False
    ) -> bool:
        """경로 삭제"""
        pass
    
    @abstractmethod
    def path_exists(self, path: Path) -> bool:
        """경로 존재 여부 확인"""
        pass
    
    @abstractmethod
    def get_file_info(self, path: Path) -> Optional[Dict[str, Any]]:
        """파일 정보 조회"""
        pass
```

## 📱 애플리케이션 인터페이스

#### IBookPipelineAPI (인터페이스)
```python
class IBookPipelineAPI(ABC):
    """책 파이프라인 API 인터페이스"""
    
    @abstractmethod
    async def process_book(
        self,
        pdf_path: Path,
        selected_chapters: Optional[List[int]] = None,
        processing_options: Optional[Dict[str, Any]] = None
    ) -> PipelineResult:
        """책 전체 처리"""
        pass
    
    @abstractmethod
    async def process_chapters(
        self,
        pdf_path: Path,
        chapter_numbers: List[int],
        processing_options: Optional[Dict[str, Any]] = None
    ) -> PipelineResult:
        """선택된 장들만 처리"""
        pass
    
    @abstractmethod
    async def get_book_info(self, pdf_path: Path) -> Dict[str, Any]:
        """책 기본 정보 조회"""
        pass
    
    @abstractmethod
    async def get_available_chapters(self, pdf_path: Path) -> List[ChapterInfo]:
        """사용 가능한 장 목록 조회"""
        pass
    
    @abstractmethod
    async def validate_input(self, pdf_path: Path) -> bool:
        """입력 파일 검증"""
        pass
    
    @abstractmethod
    def get_processing_status(self) -> Dict[str, Any]:
        """처리 상태 조회"""
        pass
```

## 🔗 의존성 주입 컨테이너

#### IDependencyContainer (인터페이스)
```python
from typing import TypeVar, Type, Callable, Any

T = TypeVar('T')

class IDependencyContainer(ABC):
    """의존성 주입 컨테이너 인터페이스"""
    
    @abstractmethod
    def register(
        self,
        interface: Type[T],
        implementation: Type[T],
        singleton: bool = False
    ) -> None:
        """서비스 등록"""
        pass
    
    @abstractmethod
    def register_factory(
        self,
        interface: Type[T],
        factory: Callable[[], T],
        singleton: bool = False
    ) -> None:
        """팩토리 함수로 서비스 등록"""
        pass
    
    @abstractmethod
    def register_instance(
        self,
        interface: Type[T],
        instance: T
    ) -> None:
        """인스턴스 직접 등록"""
        pass
    
    @abstractmethod
    def resolve(self, interface: Type[T]) -> T:
        """서비스 해결"""
        pass
    
    @abstractmethod
    def is_registered(self, interface: Type[T]) -> bool:
        """등록 여부 확인"""
        pass

## 🧪 테스트용 인터페이스

#### ITestDataProvider (인터페이스)
```python
class ITestDataProvider(ABC):
    """테스트 데이터 제공자 인터페이스"""
    
    @abstractmethod
    def get_sample_pdf_path(self) -> Path:
        """샘플 PDF 경로 반환"""
        pass
    
    @abstractmethod
    def get_expected_toc_result(self) -> TOCResult:
        """예상되는 TOC 결과 반환"""
        pass
    
    @abstractmethod
    def get_sample_chapter_info(self) -> List[ChapterInfo]:
        """샘플 장 정보 반환"""
        pass
    
    @abstractmethod
    def create_mock_node_document(self, node_id: str) -> NodeDocument:
        """모의 노드 문서 생성"""
        pass
    
    @abstractmethod
    def get_golden_master_data(self, test_name: str) -> Dict[str, Any]:
        """골든 마스터 데이터 반환"""
        pass
```

## 💡 사용 예제

### 의존성 주입 설정 예제
```python
# 컨테이너 설정
container = DependencyContainer()

# 인프라스트럭처 서비스 등록
container.register(IAIProvider, ClaudeSDKProvider, singleton=True)
container.register(IPromptManager, PromptManager, singleton=True)
container.register(ILoggingService, LoggingService, singleton=True)
container.register(IFileSystemManager, FileSystemManager, singleton=True)

# 도메인 서비스 등록
container.register(ITOCExtractor, TOCExtractor)
container.register(IEnhancedTOCGenerator, EnhancedTOCGenerator)
container.register(IChapterIntegrationService, ChapterIntegrationService)
container.register(INodeDocumentProcessor, NodeDocumentProcessor)
container.register(IDocumentIntegrator, DocumentIntegrator)

# 오케스트레이터 등록
container.register(IPipelineOrchestrator, PipelineOrchestrator)

# API 레이어 등록
container.register(IBookPipelineAPI, BookPipelineAPI)
```

### 서비스 사용 예제
```python
# API 사용
api = container.resolve(IBookPipelineAPI)
result = await api.process_book(
    pdf_path=Path("sample.pdf"),
    selected_chapters=[1, 2, 3],
    processing_options={
        "ai_temperature": 0.3,
        "batch_size": 5,
        "enable_caching": True
    }
)

print(f"Processing success: {result.is_success}")
print(f"Progress: {result.progress_percent}%")
```

이 인터페이스 명세서는 실제 구현 시 타입 안전성과 계약의 명확성을 보장하며, 테스트 가능하고 유지보수가 용이한 코드를 작성하는 데 필수적인 가이드라인을 제공합니다.