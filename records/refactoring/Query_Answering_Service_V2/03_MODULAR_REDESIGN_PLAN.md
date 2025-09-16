# Query Answering Service V2 - 모듈 재구성 구현 계획

**생성 시간:** Tue Sep 16 19:25:32 KST 2025

**핵심 내용:** 조건부 처리 로직 기반 모듈 재구성 - 경로 기반 라우팅, 설정 파일 관리, 4단계 응답 모드를 통한 효율적인 질의 응답 시스템

**상세 내용:**
- 사용자 요청 분석 및 핵심 요구사항 (라인 1-50): 경로 기반 입력, 설정 파일 기반 모드 관리
- 설정 기반 시스템 설계 (라인 51-150): config.yaml 구조, ConfigManager 구현
- 경로 기반 라우팅 시스템 (라인 151-280): 자동 레벨 감지, PathRouter 구현
- 파일 처리 로직 구현 계획 (라인 281-450): 3단계 레벨별 프로세서 설계
- 응답 생성 시스템 (라인 451-550): 모드별 응답 생성 로직
- 최종 통합 아키텍처 (라인 551-750): ConfigurableQueryService 메인 오케스트레이터
- 구현 계획 및 성능 최적화 (라인 751-800): 단계별 개발 로드맵

**상태:** active

**참조:** 02_COMPREHENSIVE_DESIGN.md 기반 모듈 재구성 및 조건부 처리 로직 도입

---

## 🎯 사용자 요구사항 분석

### **핵심 변경 사항**

1. **🏗️ 모듈 재구성**: 서로 다른 수준의 역할을 수행하는 모듈들의 조합 기반 시스템
2. **🚦 조건부 처리**: 특정 장/섹션 여부에 따른 처리 경로 분기
3. **📂 경로 기반 입력**: 책 폴더명 → 장 폴더명 → 섹션 파일명 계층구조
4. **⚙️ 설정 파일 관리**: 기본 경로, 응답 모드를 config.yaml로 관리

### **파레토 법칙 20% 핵심 내용**

1. **📂 경로 기반 라우팅**: 제공된 경로 정보로 처리 범위 자동 결정
2. **⚙️ 설정 기반 모드 관리**: Config 파일로 시스템 동작 방식 제어
3. **🎯 3가지 처리 시나리오**: 책 레벨 → 장 레벨 → 섹션 레벨 입력
4. **⚡ Early Exit 최적화**: 불필요한 과정 완전 스킵으로 70% 성능 향상

### **확장된 응답 모드 시스템**

**1차 구분**: 장 기반 응답 vs 섹션 기반 응답  
**2차 구분** (섹션 기반 시): 결합 섹션 기반 vs 개별 섹션 기반

```
응답 모드 체계:
├── 장 기반 응답 (Chapter-based)
│   └── 각 장의 전체 내용으로 응답 생성
└── 섹션 기반 응답 (Section-based)
    ├── 결합 섹션 기반 (Combined)
    │   └── 장별로 섹션들 결합 → 장별 응답 → 최종 통합
    └── 개별 섹션 기반 (Individual)
        └── 각 섹션별 개별 응답 → 모두 통합
```

---

## ⚙️ 설정 기반 시스템 설계

### **📋 설정 파일 구조 (config.yaml)**

```yaml
# Query Answering Service V2 Configuration
query_service:
  # 🏠 기본 경로 설정
  base_paths:
    data_root: "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output"
    default_book: "Data_Oriented_Programming"
    
  # 🎛️ 응답 모드 설정
  response_modes:
    primary_mode: "section_based"  # "chapter_based" | "section_based"
    section_mode: "combined"       # "combined" | "individual" (섹션 기반 선택 시에만 적용)
    
  # ⚡ 성능 설정
  performance:
    max_concurrent_requests: 5
    cache_enabled: true
    cache_ttl_seconds: 3600
    
  # 📁 파일 패턴 설정
  file_patterns:
    book_toc: "book_toc.md"
    chapter_toc: "chapter_toc.md"
    chapter_content: "{chapter_name}_content.md"
    section_info: "unified_info_docs/{section_file}.md"
    
  # 🔍 매칭 설정
  matching:
    max_matches: 3
    similarity_threshold: 0.7
    fallback_enabled: true

# 🛡️ 로깅 및 모니터링
logging:
  level: "INFO"
  performance_tracking: true
  error_tracking: true
```

### **🎛️ ConfigManager 구현**

```python
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum

class PrimaryMode(Enum):
    CHAPTER_BASED = "chapter_based"
    SECTION_BASED = "section_based"

class SectionMode(Enum):
    COMBINED = "combined"      # 결합 섹션 기반
    INDIVIDUAL = "individual"  # 개별 섹션 기반

@dataclass
class QueryConfig:
    """질의 처리 설정"""
    base_data_path: str
    default_book: str
    primary_mode: PrimaryMode
    section_mode: SectionMode
    max_concurrent: int
    cache_enabled: bool
    cache_ttl: int
    file_patterns: Dict[str, str]
    matching_config: Dict[str, Any]

class ConfigManager:
    """설정 파일 기반 시스템 관리자"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> QueryConfig:
        """설정 파일 로드 및 검증"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            qs_config = data['query_service']
            
            return QueryConfig(
                base_data_path=qs_config['base_paths']['data_root'],
                default_book=qs_config['base_paths']['default_book'],
                primary_mode=PrimaryMode(qs_config['response_modes']['primary_mode']),
                section_mode=SectionMode(qs_config['response_modes']['section_mode']),
                max_concurrent=qs_config['performance']['max_concurrent_requests'],
                cache_enabled=qs_config['performance']['cache_enabled'],
                cache_ttl=qs_config['performance']['cache_ttl_seconds'],
                file_patterns=qs_config['file_patterns'],
                matching_config=qs_config['matching']
            )
            
        except Exception as e:
            raise ConfigurationError(f"설정 파일 로드 실패: {e}")
    
    def get_file_path(self, pattern_key: str, **kwargs) -> str:
        """파일 패턴 기반 경로 생성"""
        pattern = self.config.file_patterns[pattern_key]
        return pattern.format(**kwargs)
    
    def update_mode(self, primary_mode: PrimaryMode, section_mode: Optional[SectionMode] = None):
        """런타임 모드 변경"""
        self.config.primary_mode = primary_mode
        if section_mode and primary_mode == PrimaryMode.SECTION_BASED:
            self.config.section_mode = section_mode
            
    def reload_config(self):
        """설정 파일 재로드"""
        self.config = self._load_config()

class ConfigurationError(Exception):
    """설정 관련 예외"""
    pass
```

---

## 🚦 경로 기반 라우팅 시스템

### **📂 입력 패턴 자동 감지**

```python
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Union

class InputLevel(Enum):
    """입력 레벨 자동 감지"""
    BOOK_LEVEL = "book_level"      # 책 폴더명만 제공 (질의 + 책명)
    CHAPTER_LEVEL = "chapter_level" # 장 폴더명 제공 (질의 + 책명/장명들)
    SECTION_LEVEL = "section_level" # 섹션 파일명 제공 (질의 + 책명/장명/섹션파일명들)

@dataclass
class QueryInput:
    """경로 기반 질의 입력"""
    user_query: str
    input_paths: List[str]  # 제공된 경로들 (책/장/섹션 구분 없이)
    
    def __post_init__(self):
        """입력 후 자동 레벨 감지"""
        self.input_level = self._detect_input_level()
        self.parsed_paths = self._parse_paths()
    
    def _detect_input_level(self) -> InputLevel:
        """경로 패턴으로 입력 레벨 자동 감지"""
        if not self.input_paths:
            raise ValueError("입력 경로가 없습니다")
            
        # 첫 번째 경로로 레벨 판단
        first_path = self.input_paths[0]
        path_parts = first_path.split('/')
        
        if len(path_parts) == 1:
            # "Data_Oriented_Programming" -> 책 레벨
            return InputLevel.BOOK_LEVEL
        elif len(path_parts) == 2:
            # "Data_Oriented_Programming/1_Complexity_of_..." -> 장 레벨  
            return InputLevel.CHAPTER_LEVEL
        elif len(path_parts) >= 3:
            # "Data_Oriented_Programming/1_Complexity_of_.../15_lev1_1_..." -> 섹션 레벨
            return InputLevel.SECTION_LEVEL
        else:
            raise ValueError(f"알 수 없는 경로 패턴: {first_path}")
    
    def _parse_paths(self) -> Dict[str, Any]:
        """경로 파싱 결과"""
        if self.input_level == InputLevel.BOOK_LEVEL:
            return {
                "book_name": self.input_paths[0],
                "chapters": None,
                "sections": None
            }
        elif self.input_level == InputLevel.CHAPTER_LEVEL:
            book_name = self.input_paths[0].split('/')[0]
            chapters = [path.split('/')[1] for path in self.input_paths]
            return {
                "book_name": book_name,
                "chapters": chapters,
                "sections": None
            }
        elif self.input_level == InputLevel.SECTION_LEVEL:
            book_name = self.input_paths[0].split('/')[0]
            sections_info = []
            for path in self.input_paths:
                parts = path.split('/')
                sections_info.append({
                    "chapter": parts[1],
                    "section_file": parts[2] if len(parts) > 2 else parts[-1]
                })
            return {
                "book_name": book_name,
                "chapters": list(set(s["chapter"] for s in sections_info)),
                "sections": sections_info
            }
```

### **🧭 조건부 라우팅 엔진**

```python
class PathRouter:
    """경로 기반 자동 라우팅 엔진"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        
    async def route_query(self, query_input: QueryInput) -> 'ProcessingStrategy':
        """입력 레벨에 따른 처리 전략 생성"""
        
        input_level = query_input.input_level
        parsed = query_input.parsed_paths
        
        if input_level == InputLevel.BOOK_LEVEL:
            return await self._route_book_level(query_input.user_query, parsed["book_name"])
        elif input_level == InputLevel.CHAPTER_LEVEL:
            return await self._route_chapter_level(query_input.user_query, parsed)
        elif input_level == InputLevel.SECTION_LEVEL:
            return await self._route_section_level(query_input.user_query, parsed)
    
    async def _route_book_level(self, query: str, book_name: str) -> 'ProcessingStrategy':
        """책 레벨: 연관 장 식별 필요"""
        return ProcessingStrategy(
            needs_chapter_identification=True,
            needs_section_identification=self.config.config.primary_mode == PrimaryMode.SECTION_BASED,
            book_name=book_name,
            target_chapters=None,
            target_sections=None,
            processing_mode=self.config.config.primary_mode,
            section_mode=self.config.config.section_mode
        )
    
    async def _route_chapter_level(self, query: str, parsed: Dict) -> 'ProcessingStrategy':
        """장 레벨: 장은 특정되었고, 모드에 따라 섹션 식별 여부 결정"""
        return ProcessingStrategy(
            needs_chapter_identification=False,
            needs_section_identification=self.config.config.primary_mode == PrimaryMode.SECTION_BASED,
            book_name=parsed["book_name"],
            target_chapters=parsed["chapters"],
            target_sections=None,
            processing_mode=self.config.config.primary_mode,
            section_mode=self.config.config.section_mode
        )
    
    async def _route_section_level(self, query: str, parsed: Dict) -> 'ProcessingStrategy':
        """섹션 레벨: 모든 것이 특정되었음, 식별 과정 불필요"""
        return ProcessingStrategy(
            needs_chapter_identification=False,
            needs_section_identification=False,
            book_name=parsed["book_name"],
            target_chapters=parsed["chapters"],
            target_sections=parsed["sections"],
            processing_mode=PrimaryMode.SECTION_BASED,  # 섹션이 특정되면 강제로 섹션 기반
            section_mode=self.config.config.section_mode
        )

@dataclass
class ProcessingStrategy:
    """처리 전략 정의"""
    needs_chapter_identification: bool
    needs_section_identification: bool
    book_name: str
    target_chapters: Optional[List[str]]
    target_sections: Optional[List[Dict[str, str]]]  # [{"chapter": "...", "section_file": "..."}]
    processing_mode: PrimaryMode
    section_mode: SectionMode
```

---

## 📁 구체적인 파일 처리 로직

### **📚 책 레벨 처리**

```python
class BookLevelProcessor:
    """책 레벨 입력 처리 (질의 + 책 폴더명)"""
    
    def __init__(self, config_manager: ConfigManager, toc_matcher: TocQueryMatcher):
        self.config = config_manager
        self.toc_matcher = toc_matcher
        
    async def process(self, query: str, strategy: ProcessingStrategy) -> List[str]:
        """책 레벨 처리: book_toc.md → 연관 장 식별"""
        
        # 📖 책 목차 파일 경로 생성
        book_toc_path = Path(self.config.config.base_data_path) / strategy.book_name / \
                       self.config.get_file_path("book_toc")
        
        # 📋 목차 내용 로드
        book_toc_content = await self._load_file(book_toc_path)
        
        # 🎯 AI 매칭으로 연관 장들 식별
        matched_chapters = await self.toc_matcher.match_query_to_toc(query, book_toc_content)
        
        if not matched_chapters:
            raise NoMatchFoundError("질의와 관련된 장을 찾을 수 없습니다")
            
        return matched_chapters
    
    async def _load_file(self, file_path: Path) -> str:
        """파일 로드 with 에러 처리"""
        try:
            return await asyncio.to_thread(file_path.read_text, encoding='utf-8')
        except Exception as e:
            raise FileProcessingError(f"파일 로드 실패 {file_path}: {e}")
```

### **📖 장 레벨 처리**

```python
class ChapterLevelProcessor:
    """장 레벨 입력 처리 (질의 + 장 폴더명들)"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        
    async def process_chapter_based(
        self, 
        query: str, 
        strategy: ProcessingStrategy
    ) -> List[str]:
        """장 기반 모드: {장이름}_content.md 파일들 로드"""
        
        chapter_contents = []
        base_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        for chapter_name in strategy.target_chapters:
            # 📖 장 내용 파일 경로 생성
            content_file = self.config.get_file_path("chapter_content", chapter_name=chapter_name)
            content_path = base_path / chapter_name / content_file
            
            try:
                content = await self._load_file(content_path)
                chapter_contents.append(content)
            except FileNotFoundError:
                continue  # 해당 장 파일이 없으면 스킵
                
        return chapter_contents
    
    async def process_section_based(
        self, 
        query: str, 
        strategy: ProcessingStrategy,
        toc_matcher: TocQueryMatcher
    ) -> Dict[str, List[str]]:
        """섹션 기반 모드: chapter_toc.md → 연관 섹션들 식별"""
        
        chapter_sections = {}
        base_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        for chapter_name in strategy.target_chapters:
            # 📋 장 목차 파일 로드
            chapter_toc_path = base_path / chapter_name / self.config.get_file_path("chapter_toc")
            
            try:
                chapter_toc_content = await self._load_file(chapter_toc_path)
                
                # 🎯 AI 매칭으로 연관 섹션들 식별
                matched_sections = await toc_matcher.match_query_to_toc(query, chapter_toc_content)
                
                if matched_sections:
                    chapter_sections[chapter_name] = matched_sections
                    
            except FileNotFoundError:
                continue
                
        return chapter_sections
    
    async def _load_file(self, file_path: Path) -> str:
        """파일 로드"""
        return await asyncio.to_thread(file_path.read_text, encoding='utf-8')
```

### **📄 섹션 레벨 처리**

```python
class SectionLevelProcessor:
    """섹션 레벨 입력 처리 (질의 + 섹션 파일명들)"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        
    async def process(
        self, 
        query: str, 
        strategy: ProcessingStrategy
    ) -> Dict[str, List[str]]:
        """섹션 레벨 처리: 직접 제공된 섹션 파일들 로드"""
        
        section_contents = {}
        base_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        # 📄 섹션 정보를 장별로 그룹화
        chapters_sections = {}
        for section_info in strategy.target_sections:
            chapter = section_info["chapter"]
            if chapter not in chapters_sections:
                chapters_sections[chapter] = []
            chapters_sections[chapter].append(section_info["section_file"])
        
        # 📂 장별로 섹션 파일들 로드
        for chapter_name, section_files in chapters_sections.items():
            chapter_path = base_path / chapter_name
            section_contents[chapter_name] = []
            
            for section_file in section_files:
                # 📄 섹션 파일 경로 생성 (unified_info_docs 폴더 안에 있음)
                section_path = chapter_path / "unified_info_docs" / f"{section_file}.md"
                
                try:
                    content = await self._load_file(section_path)
                    section_contents[chapter_name].append(content)
                except FileNotFoundError:
                    continue
                    
        return section_contents
    
    async def _load_file(self, file_path: Path) -> str:
        """파일 로드"""
        return await asyncio.to_thread(file_path.read_text, encoding='utf-8')
```

---

## 🔄 모드별 응답 생성 시스템

### **⚙️ 응답 모드 관리자**

```python
class ModeBasedResponseGenerator:
    """설정 기반 모드별 응답 생성"""
    
    def __init__(self, config_manager: ConfigManager, parallel_processor: ParallelQueryProcessor):
        self.config = config_manager
        self.parallel_processor = parallel_processor
        
    async def generate_response(
        self, 
        query: str, 
        strategy: ProcessingStrategy,
        processed_data: Union[List[str], Dict[str, List[str]]]
    ) -> str:
        """전략에 따른 응답 생성"""
        
        if strategy.processing_mode == PrimaryMode.CHAPTER_BASED:
            return await self._generate_chapter_based_response(query, processed_data)
        elif strategy.processing_mode == PrimaryMode.SECTION_BASED:
            if strategy.section_mode == SectionMode.COMBINED:
                return await self._generate_combined_section_response(query, processed_data)
            elif strategy.section_mode == SectionMode.INDIVIDUAL:
                return await self._generate_individual_section_response(query, processed_data)
    
    async def _generate_chapter_based_response(
        self, 
        query: str, 
        chapter_contents: List[str]
    ) -> str:
        """장 기반 응답: 각 장 내용으로 병렬 응답 생성 → 통합"""
        
        # 🔄 각 장별 병렬 응답 생성
        responses = await self.parallel_processor.process_parallel_queries(query, chapter_contents)
        
        # 📋 응답 통합
        return await self._integrate_responses(query, responses)
    
    async def _generate_combined_section_response(
        self, 
        query: str, 
        chapter_sections: Dict[str, List[str]]
    ) -> str:
        """결합 섹션 기반 응답: 장별로 섹션들 결합 → 장별 응답 생성 → 통합"""
        
        combined_contents = []
        
        # 📂 장별로 섹션들 결합
        for chapter_name, section_contents in chapter_sections.items():
            if section_contents:
                # 🔗 해당 장의 모든 섹션 내용 결합
                combined_content = "\n\n---\n\n".join(section_contents)
                combined_contents.append(combined_content)
        
        # 🔄 결합된 내용으로 병렬 응답 생성
        responses = await self.parallel_processor.process_parallel_queries(query, combined_contents)
        
        # 📋 최종 응답 통합
        return await self._integrate_responses(query, responses)
    
    async def _generate_individual_section_response(
        self, 
        query: str, 
        chapter_sections: Dict[str, List[str]]
    ) -> str:
        """개별 섹션 기반 응답: 각 섹션별 개별 응답 생성 → 모두 통합"""
        
        all_section_contents = []
        
        # 📄 모든 섹션을 개별 리스트로 수집
        for chapter_name, section_contents in chapter_sections.items():
            all_section_contents.extend(section_contents)
        
        # 🔄 각 섹션별 개별 병렬 응답 생성
        responses = await self.parallel_processor.process_parallel_queries(query, all_section_contents)
        
        # 📋 모든 섹션 응답 통합
        return await self._integrate_responses(query, responses)
    
    async def _integrate_responses(self, query: str, responses: List[str]) -> str:
        """응답 통합 (기존 IntegratedQueryService 로직 활용)"""
        if not responses:
            return "관련 정보를 찾을 수 없습니다."
        
        if len(responses) == 1:
            return responses[0]
        
        # 🤖 AI 기반 응답 통합
        integration_prompt = f"""
사용자 질의: "{query}"

다음은 동일한 질의에 대해 서로 다른 참조 데이터로 생성된 응답들입니다:

{chr(10).join([f"응답 {i+1}: {resp}" for i, resp in enumerate(responses)])}

이 응답들을 종합하여 사용자 질의에 대한 통합된 최종 답변을 생성해주세요:

요구사항:
- 모든 응답의 핵심 내용을 통합
- 상충되는 내용이 있다면 명시
- 포괄적이면서도 일관성 있는 답변
"""
        
        return await self.parallel_processor.response_generator.ai_service.query_single_request(
            integration_prompt
        )
```

---

## 🏗️ 최종 통합 아키텍처

### **🎛️ 메인 오케스트레이터**

```python
class ConfigurableQueryService:
    """설정 기반 통합 질의 응답 시스템"""
    
    def __init__(self, ai_service: AIService, config_path: str = "config.yaml"):
        # 🎛️ 설정 관리
        self.config_manager = ConfigManager(config_path)
        
        # 🧠 AI 기반 컴포넌트들
        self.toc_matcher = TocQueryMatcher(ai_service)
        self.response_generator = QueryResponseGenerator(ai_service)
        self.parallel_processor = ParallelQueryProcessor(self.response_generator)
        
        # 🚦 라우팅 및 처리 컴포넌트들
        self.path_router = PathRouter(self.config_manager)
        self.book_processor = BookLevelProcessor(self.config_manager, self.toc_matcher)
        self.chapter_processor = ChapterLevelProcessor(self.config_manager)
        self.section_processor = SectionLevelProcessor(self.config_manager)
        self.response_generator_manager = ModeBasedResponseGenerator(
            self.config_manager, self.parallel_processor
        )
        
        # 📊 성능 모니터링
        self.performance_tracker = PerformanceTracker()
        
    async def process_query(
        self, 
        user_query: str, 
        input_paths: List[str],
        override_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """메인 질의 처리 파이프라인"""
        
        start_time = time.time()
        
        try:
            # 🔧 설정 오버라이드 적용 (임시)
            if override_config:
                self._apply_config_override(override_config)
            
            # 📂 입력 파싱 및 라우팅
            query_input = QueryInput(user_query, input_paths)
            processing_strategy = await self.path_router.route_query(query_input)
            
            # 🔍 단계별 데이터 처리
            processed_data = await self._process_data_by_level(
                user_query, query_input, processing_strategy
            )
            
            # 🤖 응답 생성
            final_response = await self.response_generator_manager.generate_response(
                user_query, processing_strategy, processed_data
            )
            
            # 📊 성능 추적
            processing_time = time.time() - start_time
            self.performance_tracker.record_success(processing_time, query_input.input_level)
            
            return self._build_success_response(
                user_query, input_paths, final_response, processing_strategy, processing_time
            )
            
        except Exception as e:
            # 🚨 에러 처리 및 추적
            processing_time = time.time() - start_time
            self.performance_tracker.record_failure(processing_time, str(e))
            
            return self._build_error_response(
                user_query, input_paths, str(e), processing_time
            )
        finally:
            # 🔄 설정 오버라이드 복원
            if override_config:
                self.config_manager.reload_config()
```

### **🚀 사용 예시**

```python
async def main():
    """사용 예시"""
    
    # 🤖 AI 서비스 초기화
    ai_service = AIService()  # 기존 ai_service_v4 사용
    
    # 🎛️ 설정 기반 질의 서비스 초기화
    query_service = ConfigurableQueryService(ai_service, "config.yaml")
    
    # 📚 시나리오 1: 책 레벨 입력 (연관 장 식별 필요)
    response1 = await query_service.process_query(
        user_query="객체지향 프로그래밍의 복잡성에 대해 설명해주세요",
        input_paths=["Data_Oriented_Programming"]
    )
    
    # 📖 시나리오 2: 장 레벨 입력 (특정 장들 지정)
    response2 = await query_service.process_query(
        user_query="데이터와 코드 분리에 대해 알려주세요", 
        input_paths=[
            "Data_Oriented_Programming/1_Complexity_of_object_oriented_programming",
            "Data_Oriented_Programming/2_Separation_between_code_and_data"
        ]
    )
    
    # 📄 시나리오 3: 섹션 레벨 입력 (특정 섹션들 지정)  
    response3 = await query_service.process_query(
        user_query="UML 다이어그램에 대해 설명해주세요",
        input_paths=[
            "Data_Oriented_Programming/1_Complexity_of_object_oriented_programming/18_lev3_1.1.2_UML_101_info"
        ]
    )
    
    # 🔧 임시 설정 오버라이드 사용
    response4 = await query_service.process_query(
        user_query="데이터 구조에 대해 알려주세요",
        input_paths=["Data_Oriented_Programming"],
        override_config={
            "primary_mode": "section_based",
            "section_mode": "individual"
        }
    )
    
    # 📊 성능 통계 확인
    performance_stats = query_service.performance_tracker.get_performance_summary()
    print(f"성능 통계: {performance_stats}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📅 구현 단계별 계획

### **Phase 1: 핵심 인프라** (1.5주)
**🔧 우선순위**: 최고
- [x] `config.yaml` 설정 파일 스키마 정의
- [x] `ConfigManager`, `QueryInput`, `ProcessingStrategy` 데이터 구조
- [x] `PathRouter` 경로 기반 자동 라우팅 로직
- [x] 기존 `ai_service_v4` 인터페이스 호환성 검증

### **Phase 2: 레벨별 프로세서** (2주)
**📂 우선순위**: 높음
- [ ] `BookLevelProcessor` - book_toc.md 기반 장 식별
- [ ] `ChapterLevelProcessor` - 장 내용/목차 기반 처리
- [ ] `SectionLevelProcessor` - unified_info_docs 폴더 파일 처리
- [ ] 에러 처리 및 파일 존재 여부 검증

### **Phase 3: 응답 생성 시스템** (1.5주)
**🤖 우선순위**: 높음
- [ ] `ModeBasedResponseGenerator` - 설정 기반 모드별 처리
- [ ] 병렬 처리 최적화 (기존 `ParallelQueryProcessor` 활용)
- [ ] 응답 통합 로직 개선
- [ ] 성능 모니터링 (`PerformanceTracker`) 구현

### **Phase 4: 통합 및 테스트** (1주)
**🚀 우선순위**: 높음
- [ ] `ConfigurableQueryService` 메인 오케스트레이터 완성
- [ ] 3가지 시나리오별 통합 테스트
- [ ] 설정 오버라이드 기능 검증
- [ ] 성능 벤치마크 (기존 대비 50% 이상 향상 목표)

---

## ⚡ 핵심 성능 최적화 포인트

### **🎯 Early Exit 전략**
- **책 레벨**: 연관 장이 없으면 즉시 종료
- **장 레벨**: 모드가 장 기반이면 섹션 식별 스킵
- **섹션 레벨**: 모든 식별 과정 스킵으로 최대 70% 시간 단축

### **📦 캐싱 전략**  
- **설정 캐싱**: config.yaml 메모리 캐싱
- **목차 캐싱**: book_toc.md, chapter_toc.md LRU 캐싱
- **AI 응답 캐싱**: 동일한 질의-참조데이터 조합 캐싱

### **⚡ 병렬 처리 최적화**
- **동적 배치 크기**: 처리할 데이터 양에 따른 최적 동시 실행 수 조정
- **장별 병렬**: 여러 장을 동시에 처리
- **섹션별 병렬**: 개별 섹션 모드에서 섹션별 동시 처리

---

## 🎯 기대 효과

### **📈 성능 향상**
- **70% 처리 시간 단축**: Early Exit 전략으로 불필요한 과정 완전 제거
- **50% 메모리 사용량 감소**: 효율적인 데이터 로딩 및 캐싱
- **3배 처리량 증가**: 최적화된 병렬 처리

### **🔧 유지보수성**
- **모듈화된 구조**: 각 처리 단계별 독립적인 모듈
- **설정 기반 관리**: 코드 변경 없이 동작 방식 제어
- **확장 가능성**: 새로운 응답 모드 쉽게 추가 가능

### **🎛️ 사용자 경험**
- **단순한 입력 방식**: 경로만 제공하면 자동 처리
- **유연한 모드 설정**: 상황에 맞는 최적 응답 모드 선택
- **실시간 설정 변경**: 오버라이드를 통한 임시 모드 변경

---

## 프로젝트 메타데이터

**개발 환경:** Python 3.8+, async/await, asyncio, yaml  
**핵심 의존성:** ai_service_v4.py, typing, pathlib, logging, pyyaml  
**테스트 데이터:** Data_Oriented_Programming 도서 전체 구조  
**예상 개발 기간:** 6주 (단계별 개발)  
**시스템 복잡도:** 중급 (조건부 처리, 설정 기반 관리, 경로 기반 라우팅)  
**확장성:** 매우 높음 (모듈화된 구조, 플러그인 가능, API 서비스화 가능)  
**성능 목표:** 기존 대비 70% 시간 단축, 50% 메모리 절약, 3배 처리량 증가