# Query Answering Service V2 - Comprehensive Design

**생성 시간:** Tue Sep 16 12:32:06 KST 2025

**핵심 내용:** 계층적 질의 응답 시스템 완전 설계 - 목차 매칭, 병렬 응답 생성, 3가지 모드별 처리 로직을 포함한 통합 AI 기반 질의 응답 서비스

**상세 내용:**
- 시스템 개요 (라인 1-80): 전체 시스템 구조, 핵심 기능, 3가지 응답 모드
- 목차 매칭 시스템 (라인 81-150): TocQueryMatcher 기능 및 계층적 매칭
- 병렬 응답 생성 (라인 151-220): 비동기 병렬 처리 아키텍처
- 모드별 처리 로직 (라인 221-350): 3가지 모드의 세부 구현 방안
- 통합 아키텍처 (라인 351-450): 전체 시스템 통합 설계
- 구현 계획 (라인 451-500): 단계별 개발 로드맵

**상태:** active

**참조:** 기존 ai_service_v4.py의 query_single_request 메서드 및 Knowledge_Sherpa v2 파이프라인 시스템

---

## 시스템 개요

### 🎯 전체 시스템 구조

**계층적 질의 응답 시스템** (Hierarchical Query Answering System)

사용자 질의를 받아 책/장/섹션의 계층적 구조를 활용하여 3가지 세분화 수준에서 AI 기반 응답을 생성하는 통합 시스템입니다.

### 📊 핵심 구성 요소

**1. 목차 매칭 시스템** (TOC Matching System)
- 사용자 질의와 목차 항목 간의 관련성 AI 판단
- 책 목차 → 연관 장 식별
- 장 목차 → 연관 섹션 식별

**2. 병렬 응답 생성 시스템** (Parallel Response Generation)
- 여러 데이터 소스에 대한 동시 AI 응답 생성
- AsyncIO 기반 비동기 처리
- 에러 복구 및 부분 실패 처리

**3. 계층적 통합 시스템** (Hierarchical Integration)
- 모드별 처리 로직 분기
- 다중 응답 통합 및 최종 답변 생성
- 3가지 세분화 수준 지원

### 🔄 3가지 응답 모드

**Mode 1: Chapter-based Response** (장 기반 응답)
```
사용자 질의 → 책 목차 매칭 → 연관 장들
                    ↓
각 장 전체 내용 → 장별 응답 생성 (병렬)
                    ↓
            모든 장 응답 → 최종 통합 응답
```

**Mode 2: Unified Section-based Response** (통합 섹션 기반 응답)
```
사용자 질의 → 책 목차 매칭 → 연관 장들
                    ↓
각 장의 목차 매칭 → 연관 섹션들 → 섹션 내용 통합
                    ↓
장별 통합 내용 → 장별 응답 생성 (병렬)
                    ↓
            모든 장 응답 → 최종 통합 응답
```

**Mode 3: Individual Section-based Response** (개별 섹션 기반 응답)
```
사용자 질의 → 책 목차 매칭 → 연관 장들
                    ↓
각 장의 목차 매칭 → 연관 섹션들
                    ↓
각 섹션별 개별 응답 생성 (병렬)
                    ↓
장별 섹션 응답 통합 → 최종 통합 응답
```

### 📁 데이터 구조

```
Data_Oriented_Programming/
├── book_toc.md                           # 책 전체 목차
├── 1_Complexity_of_object_oriented_programming/
│   ├── chapter_toc.md                    # 장 목차
│   ├── 1_Complexity_of_..._content.md    # 장 전체 내용
│   └── node_info_docs/                   # 섹션별 파일들
│       ├── 15_lev1_1_Complexity_of_...info.md
│       ├── 16_lev2_1.1_OOP_design_...info.md
│       └── ...
├── 2_Separation_between_code_and_data/
│   ├── chapter_toc.md
│   ├── 2_Separation_..._content.md
│   └── node_info_docs/
└── ...
```

---

## 목차 매칭 시스템

### 🧠 TocQueryMatcher 설계

**기본 기능:**
- 사용자 질의와 목차 내용의 관련성 AI 판단
- 최대 3개 결과 반환 (엄격한 관련성 기준)
- 관련성 낮으면 빈 결과 반환

**2가지 활용 시나리오:**
1. **책 목차 매칭**: 질의 → 연관 장 이름들 반환
2. **장 목차 매칭**: 질의 → 연관 섹션 이름들 반환

```python
class TocQueryMatcher:
    """AI 기반 목차 매칭 서비스"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        
    async def match_query_to_toc(
        self, 
        user_query: str, 
        toc_content: str
    ) -> List[str]:
        """
        질의와 목차 매칭
        
        Returns:
            List[str]: 매칭된 헤더 제목들 (최대 3개, 관련성 없으면 빈 리스트)
        """
        prompt = self._generate_prompt(user_query, toc_content)
        ai_response = await self.ai_service.query_single_request(prompt)
        return self._parse_ai_response(ai_response)
    
    def _generate_prompt(self, query: str, toc_content: str) -> str:
        """AI 매칭용 프롬프트 생성"""
        return f"""
사용자 질의: "{query}"

다음 목차 항목들을 검토하고, 질의와 **밀접하게 관련된** 항목만 선택하세요.
관련성이 낮거나 애매하면 선택하지 마세요.
최대 3개까지만 선택하고, 헤더 제목을 그대로 반환하세요.

목차:
{toc_content}

응답 형식 (관련 항목이 있을 경우만):
1. [헤더제목1]
2. [헤더제목2] 
3. [헤더제목3]

관련 항목이 없으면: "관련 항목 없음"
"""
    
    def _parse_ai_response(self, response: str) -> List[str]:
        """AI 응답 파싱 및 헤더 추출 (최대 3개)"""
        if "관련 항목 없음" in response:
            return []
        
        lines = response.strip().split('\n')
        headers = []
        
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.')):
                # 번호 제거하고 헤더 추출
                header = line.strip()[2:].strip()
                if header:
                    headers.append(header)
        
        return headers[:3]  # 최대 3개 제한
```

---

## 병렬 응답 생성 시스템

### ⚡ 비동기 병렬 처리 아키텍처

```python
import asyncio
from typing import List, Optional
from enum import Enum

class QueryResponseGenerator:
    """기본 질의-응답 생성 서비스"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        
    async def generate_response(
        self, 
        query: str, 
        reference_data: str
    ) -> str:
        """단일 질의-응답 생성"""
        prompt = self._generate_response_prompt(query, reference_data)
        return await self.ai_service.query_single_request(prompt)
    
    def _generate_response_prompt(self, query: str, reference_data: str) -> str:
        """응답 생성용 프롬프트"""
        return f"""
사용자 질의: "{query}"

다음 참조 데이터를 바탕으로 질의에 대한 응답을 생성해주세요:

참조 데이터:
{reference_data}

응답 요구사항:
- 참조 데이터 내용을 기반으로 정확한 답변
- 간결하고 명확한 설명
- 참조 데이터에 없는 내용은 추측하지 말 것
"""

class ParallelQueryProcessor:
    """병렬 질의 처리 시스템"""
    
    def __init__(self, response_generator: QueryResponseGenerator, max_concurrent: int = 5):
        self.response_generator = response_generator
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
    async def process_parallel_queries(
        self, 
        query: str, 
        reference_data_list: List[str]
    ) -> List[str]:
        """여러 데이터에 대해 병렬 응답 생성"""
        
        # 각 데이터별로 비동기 작업 생성 (세마포어로 동시 실행 수 제한)
        tasks = [
            self._limited_generate_response(query, data)
            for data in reference_data_list
        ]
        
        # 모든 작업을 병렬로 실행 (일부 실패해도 계속 진행)
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 성공한 응답들만 필터링
        return [
            response for response in responses 
            if isinstance(response, str)
        ]
    
    async def _limited_generate_response(self, query: str, data: str) -> Optional[str]:
        """세마포어 제한이 적용된 응답 생성"""
        async with self.semaphore:
            try:
                return await self.response_generator.generate_response(query, data)
            except Exception as e:
                logger.warning(f"Response generation failed: {e}")
                return None

class IntegratedQueryService:
    """통합 질의 응답 시스템"""
    
    def __init__(self, parallel_processor: ParallelQueryProcessor):
        self.parallel_processor = parallel_processor
        
    async def generate_integrated_response(
        self, 
        query: str, 
        reference_data_list: List[str]
    ) -> str:
        """병렬 처리 → 통합 응답 생성"""
        
        # 1. 병렬로 각 데이터별 응답 생성
        parallel_responses = await self.parallel_processor.process_parallel_queries(
            query, reference_data_list
        )
        
        # 2. 병렬 생성된 응답들을 통합하여 최종 응답 생성
        return await self._integrate_responses(query, parallel_responses)
    
    async def _integrate_responses(self, query: str, responses: List[str]) -> str:
        """응답들을 통합하여 최종 답변 생성"""
        if not responses:
            return "관련 정보를 찾을 수 없습니다."
        
        if len(responses) == 1:
            return responses[0]
        
        # 여러 응답을 통합하는 AI 프롬프트
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

## 모드별 처리 로직

### 📁 데이터 로더 시스템

```python
import os
from pathlib import Path

class DataLoader:
    """파일 시스템 데이터 로더"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        
    async def load_book_toc(self) -> str:
        """책 전체 목차 로드"""
        toc_path = self.base_path / "book_toc.md"
        return await self._read_file(toc_path)
        
    async def load_chapter_content(self, chapter_name: str) -> str:
        """장 전체 내용 로드"""
        chapter_path = self.base_path / chapter_name
        content_file = next(chapter_path.glob("*_content.md"), None)
        if content_file:
            return await self._read_file(content_file)
        raise FileNotFoundError(f"Chapter content not found: {chapter_name}")
        
    async def load_chapter_toc(self, chapter_name: str) -> str:
        """장 목차 로드"""
        toc_path = self.base_path / chapter_name / "chapter_toc.md"
        return await self._read_file(toc_path)
        
    async def load_section_content(self, chapter_name: str, section_name: str) -> str:
        """개별 섹션 내용 로드"""
        section_path = self.base_path / chapter_name / "node_info_docs" / f"{section_name}.md"
        return await self._read_file(section_path)
        
    async def load_section_contents(self, chapter_name: str, section_names: List[str]) -> List[str]:
        """여러 섹션 내용 로드"""
        tasks = [
            self.load_section_content(chapter_name, section_name)
            for section_name in section_names
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)
        
    async def combine_section_contents(self, section_contents: List[str]) -> str:
        """섹션 내용들 결합"""
        valid_contents = [
            content for content in section_contents 
            if isinstance(content, str)
        ]
        return "\n\n---\n\n".join(valid_contents)
    
    async def _read_file(self, file_path: Path) -> str:
        """파일 읽기"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise FileNotFoundError(f"Failed to read file {file_path}: {e}")
```

### 🔄 계층적 처리 시스템

```python
from enum import Enum

class ResponseMode(Enum):
    CHAPTER_BASED = "chapter_based"
    UNIFIED_SECTION_BASED = "unified_section_based" 
    INDIVIDUAL_SECTION_BASED = "individual_section_based"

class HierarchicalQueryService:
    """계층적 질의 응답 시스템"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.toc_matcher = TocQueryMatcher(ai_service)
        self.response_generator = QueryResponseGenerator(ai_service)
        self.parallel_processor = ParallelQueryProcessor(self.response_generator)
        self.integrated_service = IntegratedQueryService(self.parallel_processor)
        
    async def generate_hierarchical_response(
        self,
        user_query: str,
        base_data_path: str,
        mode: ResponseMode
    ) -> str:
        """모드별 계층적 응답 생성"""
        
        self.data_loader = DataLoader(base_data_path)
        
        # 책 목차에서 연관 장들 찾기
        book_toc_content = await self.data_loader.load_book_toc()
        chapter_names = await self.toc_matcher.match_query_to_toc(
            user_query, book_toc_content
        )
        
        if not chapter_names:
            return "질의와 관련된 내용을 찾을 수 없습니다."
        
        # 모드별 처리
        if mode == ResponseMode.CHAPTER_BASED:
            return await self._process_chapter_based(user_query, chapter_names)
        elif mode == ResponseMode.UNIFIED_SECTION_BASED:
            return await self._process_unified_section_based(user_query, chapter_names)
        elif mode == ResponseMode.INDIVIDUAL_SECTION_BASED:
            return await self._process_individual_section_based(user_query, chapter_names)
        else:
            raise ValueError(f"Unknown response mode: {mode}")
    
    async def _process_chapter_based(
        self, 
        user_query: str, 
        chapter_names: List[str]
    ) -> str:
        """Mode 1: 장 기반 응답 처리"""
        
        # 각 장의 전체 내용 로드
        chapter_contents = []
        for chapter_name in chapter_names:
            try:
                content = await self.data_loader.load_chapter_content(chapter_name)
                chapter_contents.append(content)
            except FileNotFoundError:
                continue
        
        # 장별 병렬 응답 생성 후 통합
        return await self.integrated_service.generate_integrated_response(
            user_query, chapter_contents
        )
    
    async def _process_unified_section_based(
        self, 
        user_query: str, 
        chapter_names: List[str]
    ) -> str:
        """Mode 2: 통합 섹션 기반 응답 처리"""
        
        chapter_unified_contents = []
        
        for chapter_name in chapter_names:
            try:
                # 장 목차에서 연관 섹션들 찾기
                chapter_toc = await self.data_loader.load_chapter_toc(chapter_name)
                section_names = await self.toc_matcher.match_query_to_toc(
                    user_query, chapter_toc
                )
                
                if section_names:
                    # 연관 섹션들의 내용을 모두 결합
                    section_contents = await self.data_loader.load_section_contents(
                        chapter_name, section_names
                    )
                    unified_content = await self.data_loader.combine_section_contents(
                        section_contents
                    )
                    chapter_unified_contents.append(unified_content)
                    
            except FileNotFoundError:
                continue
        
        # 장별 통합 내용으로 병렬 응답 생성 후 최종 통합
        return await self.integrated_service.generate_integrated_response(
            user_query, chapter_unified_contents
        )
    
    async def _process_individual_section_based(
        self, 
        user_query: str, 
        chapter_names: List[str]
    ) -> str:
        """Mode 3: 개별 섹션 기반 응답 처리"""
        
        all_section_contents = []
        
        for chapter_name in chapter_names:
            try:
                # 장 목차에서 연관 섹션들 찾기
                chapter_toc = await self.data_loader.load_chapter_toc(chapter_name)
                section_names = await self.toc_matcher.match_query_to_toc(
                    user_query, chapter_toc
                )
                
                if section_names:
                    # 각 섹션별 개별 내용 수집
                    section_contents = await self.data_loader.load_section_contents(
                        chapter_name, section_names
                    )
                    all_section_contents.extend(section_contents)
                    
            except FileNotFoundError:
                continue
        
        # 모든 섹션 내용으로 병렬 응답 생성 후 최종 통합
        return await self.integrated_service.generate_integrated_response(
            user_query, all_section_contents
        )
```

---

## 통합 아키텍처

### 🚀 최종 통합 시스템

```python
class ComprehensiveQuerySystem:
    """완전한 계층적 질의 응답 시스템"""
    
    def __init__(self, ai_service: AIService, base_data_path: str):
        self.hierarchical_service = HierarchicalQueryService(ai_service)
        self.base_data_path = base_data_path
        self.logger = logging.getLogger(__name__)
    
    async def process_query(
        self, 
        user_query: str, 
        mode: ResponseMode = ResponseMode.UNIFIED_SECTION_BASED
    ) -> Dict[str, Any]:
        """전체 질의 처리 파이프라인"""
        
        start_time = time.time()
        
        try:
            response = await self.hierarchical_service.generate_hierarchical_response(
                user_query, self.base_data_path, mode
            )
            
            processing_time = time.time() - start_time
            
            return {
                "query": user_query,
                "mode": mode.value,
                "response": response,
                "processing_info": {
                    "total_processing_time": f"{processing_time:.2f}s",
                    "success": True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {e}")
            return {
                "query": user_query,
                "mode": mode.value,
                "response": f"처리 중 오류가 발생했습니다: {str(e)}",
                "processing_info": {
                    "total_processing_time": f"{time.time() - start_time:.2f}s",
                    "success": False,
                    "error": str(e)
                }
            }
    
    async def process_query_all_modes(self, user_query: str) -> Dict[str, Any]:
        """모든 모드로 질의 처리 (비교 분석용)"""
        
        results = {}
        
        for mode in ResponseMode:
            try:
                result = await self.process_query(user_query, mode)
                results[mode.value] = result
            except Exception as e:
                results[mode.value] = {
                    "error": str(e),
                    "success": False
                }
        
        return {
            "query": user_query,
            "all_mode_results": results,
            "comparison_summary": self._generate_comparison_summary(results)
        }
    
    def _generate_comparison_summary(self, results: Dict) -> Dict[str, Any]:
        """모드별 결과 비교 요약"""
        summary = {
            "successful_modes": [],
            "failed_modes": [],
            "processing_times": {}
        }
        
        for mode, result in results.items():
            if result.get("processing_info", {}).get("success", False):
                summary["successful_modes"].append(mode)
                summary["processing_times"][mode] = result["processing_info"]["total_processing_time"]
            else:
                summary["failed_modes"].append(mode)
        
        return summary
```

### 📊 성능 최적화 전략

```python
class OptimizedQuerySystem(ComprehensiveQuerySystem):
    """성능 최적화된 질의 시스템"""
    
    def __init__(self, ai_service: AIService, base_data_path: str, cache_enabled: bool = True):
        super().__init__(ai_service, base_data_path)
        self.cache_enabled = cache_enabled
        self.response_cache = {}  # 간단한 메모리 캐시
        
    async def process_query_with_cache(
        self, 
        user_query: str, 
        mode: ResponseMode = ResponseMode.UNIFIED_SECTION_BASED
    ) -> Dict[str, Any]:
        """캐시를 활용한 질의 처리"""
        
        if self.cache_enabled:
            cache_key = f"{user_query}_{mode.value}"
            if cache_key in self.response_cache:
                cached_result = self.response_cache[cache_key]
                cached_result["processing_info"]["from_cache"] = True
                return cached_result
        
        result = await self.process_query(user_query, mode)
        
        if self.cache_enabled and result["processing_info"]["success"]:
            cache_key = f"{user_query}_{mode.value}"
            self.response_cache[cache_key] = result.copy()
        
        return result
    
    def clear_cache(self):
        """캐시 초기화"""
        self.response_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """캐시 통계"""
        return {
            "cache_size": len(self.response_cache),
            "cache_enabled": self.cache_enabled
        }
```

---

## 구현 계획

### 📅 단계별 개발 로드맵

**Phase 1: 기본 컴포넌트 구현** (1-2주)
- [ ] `TocQueryMatcher` 클래스 구현 및 테스트
- [ ] `QueryResponseGenerator` 기본 기능 구현
- [ ] `DataLoader` 파일 시스템 접근 구현
- [ ] `ai_service_v4` 연동 검증

**Phase 2: 병렬 처리 시스템** (1주)
- [ ] `ParallelQueryProcessor` 비동기 처리 구현
- [ ] `IntegratedQueryService` 응답 통합 로직
- [ ] 에러 처리 및 부분 실패 복구
- [ ] 세마포어 기반 동시 실행 제한

**Phase 3: 계층적 처리 로직** (2주)
- [ ] `ResponseMode` enum 및 모드별 분기
- [ ] Chapter-based 모드 구현
- [ ] Unified Section-based 모드 구현
- [ ] Individual Section-based 모드 구현
- [ ] `HierarchicalQueryService` 통합

**Phase 4: 최종 시스템 통합** (1주)
- [ ] `ComprehensiveQuerySystem` 완전 통합
- [ ] 성능 최적화 및 캐싱 시스템
- [ ] 에러 처리 강화 및 로깅
- [ ] 전체 시스템 테스트

**Phase 5: 테스트 및 최적화** (1주)
- [ ] 모드별 기능 테스트
- [ ] 성능 벤치마크 (처리 시간, 메모리 사용량)
- [ ] 대용량 데이터 테스트
- [ ] 문서화 완성

### 🎯 성능 목표

**응답 시간 목표:**
- Chapter-based: < 30초
- Unified Section-based: < 60초  
- Individual Section-based: < 90초

**동시 처리 능력:**
- 최대 5개 동시 AI API 호출
- 메모리 사용량 < 1GB
- 에러 복구율 > 95%

### 💡 확장 가능성

**추가 기능 로드맵:**
- **다국어 지원**: 영어/한국어 목차 처리
- **학습 기능**: 사용자 피드백 기반 정확도 개선
- **API 서비스**: REST API 형태로 서비스 제공
- **실시간 스트리밍**: 응답 생성 과정 실시간 스트리밍
- **메타데이터 추출**: 응답 생성 과정의 메타정보 제공

---

## 프로젝트 메타데이터

**개발 환경:** Python 3.8+, async/await, asyncio
**핵심 의존성:** ai_service_v4.py, typing, pathlib, logging
**테스트 데이터:** Data_Oriented_Programming 도서 전체 구조
**예상 개발 기간:** 6-7주 (단계별 개발)
**시스템 복잡도:** 중-고급 (계층적 처리, 병렬 처리, 다중 모드)
**확장성:** 높음 (모듈화된 구조, 인터페이스 기반 설계)