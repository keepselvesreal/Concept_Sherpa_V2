#!/usr/bin/env python3
import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from claude_code_sdk import query, ClaudeCodeOptions, Message

# .env 파일 로드
def load_env():
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

class RecursiveBookAnalyzer:
    def __init__(self, extracted_content_dir: str = "extracted_content"):
        self.extracted_content_dir = Path(extracted_content_dir)
        self.analysis_results = {}
        
    async def analyze_chapter_1(self) -> Dict[str, Any]:
        """1장에 대한 재귀적 분석 수행"""
        print("1장 재귀적 분석 시작...")
        
        chapter_dir = self.extracted_content_dir / "chapter1"
        if not chapter_dir.exists():
            raise FileNotFoundError(f"Chapter 1 directory not found: {chapter_dir}")
        
        # 단계 1: 원형 작업 방식 (문단→섹션 레벨)
        section_analyses = await self._analyze_sections_recursive(chapter_dir)
        
        # 단계 2: 전체 장 분석 및 종합
        chapter_analysis = await self._analyze_full_chapter(chapter_dir, section_analyses)
        
        # 결과 저장
        await self._save_analysis_results(chapter_dir, {
            "section_analyses": section_analyses,
            "chapter_analysis": chapter_analysis,
            "methodology": "recursive_circular_analysis"
        })
        
        return {
            "section_analyses": section_analyses,
            "chapter_analysis": chapter_analysis
        }
    
    async def _analyze_sections_recursive(self, chapter_dir: Path) -> Dict[str, Any]:
        """섹션별 재귀적 분석 (원형 작업 방식)"""
        print("섹션별 재귀적 분석 수행 중...")
        
        sections = ["section_1_1", "section_1_2"]
        section_results = {}
        
        for section_name in sections:
            section_dir = chapter_dir / section_name
            if section_dir.exists():
                print(f"  {section_name} 분석 중...")
                section_results[section_name] = await self._analyze_single_section(section_dir)
        
        return section_results
    
    async def _analyze_single_section(self, section_dir: Path) -> Dict[str, Any]:
        """단일 섹션에 대한 원형 작업 방식 적용"""
        
        # 1단계: 하위섹션들(문단 수준) 분석
        subsection_analyses = await self._analyze_subsections(section_dir)
        
        # 2단계: 섹션 전체 분석
        section_overview_analysis = await self._analyze_section_overview(section_dir)
        
        # 3단계: 하위섹션 + 섹션 전체 내용 종합
        combined_analysis = await self._combine_subsection_and_section_analysis(
            subsection_analyses, section_overview_analysis
        )
        
        # 4단계: 하위섹션 분석 업데이트
        updated_subsection_analyses = await self._update_subsection_analyses(
            subsection_analyses, combined_analysis
        )
        
        return {
            "initial_subsection_analyses": subsection_analyses,
            "section_overview_analysis": section_overview_analysis,
            "combined_analysis": combined_analysis,
            "updated_subsection_analyses": updated_subsection_analyses
        }
    
    async def _analyze_subsections(self, section_dir: Path) -> Dict[str, str]:
        """하위섹션들(문단 수준) 분석"""
        subsection_files = list(section_dir.glob("subsection_*.md"))
        subsection_analyses = {}
        
        for file in subsection_files:
            subsection_id = file.stem.replace("subsection_", "").replace("_", ".")
            content = file.read_text(encoding="utf-8")
            
            prompt = f"""
다음은 책의 하위섹션 내용입니다. 이 하위섹션의 핵심 내용을 파악해주세요.

**분석 요청:**
- 이 하위섹션의 주요 개념과 아이디어를 3-4개 요점으로 정리
- 각 요점은 간결하고 명확하게 표현
- 전체적인 논리 흐름과 구조 파악

**하위섹션 내용:**
{content}

**응답 형식:**
## 핵심 내용 요약
1. [첫 번째 핵심 개념]
2. [두 번째 핵심 개념]  
3. [세 번째 핵심 개념]
4. [네 번째 핵심 개념]

## 논리 흐름
[이 하위섹션의 논리적 구조와 흐름 설명]
"""
            
            analysis = await self._query_claude(prompt)
            subsection_analyses[subsection_id] = analysis
            print(f"    하위섹션 {subsection_id} 분석 완료")
        
        return subsection_analyses
    
    async def _analyze_section_overview(self, section_dir: Path) -> str:
        """섹션 전체 개요 분석"""
        overview_file = section_dir / "section_overview.md"
        if not overview_file.exists():
            return "섹션 개요 파일이 없습니다."
        
        content = overview_file.read_text(encoding="utf-8")
        
        prompt = f"""
다음은 책의 한 섹션 전체 내용입니다. 이 섹션의 핵심 내용을 파악해주세요.

**분석 요청:**
- 이 섹션의 주요 주제와 목표 파악
- 섹션 전체를 관통하는 핵심 메시지 도출
- 다른 섹션과의 연관성 고려한 위치와 역할 분석

**섹션 내용:**
{content}

**응답 형식:**
## 섹션 핵심 주제
[이 섹션의 중심 주제와 목표]

## 핵심 메시지
[섹션 전체를 관통하는 주요 메시지]

## 논리적 구조
[섹션 내부의 논리적 전개 방식]

## 맥락상 역할
[전체 장에서 이 섹션의 위치와 역할]
"""
        
        return await self._query_claude(prompt)
    
    async def _combine_subsection_and_section_analysis(self, subsection_analyses: Dict[str, str], section_analysis: str) -> str:
        """하위섹션 분석과 섹션 분석을 종합"""
        
        subsection_summary = "\n\n".join([
            f"**{subsection_id}:**\n{analysis}" 
            for subsection_id, analysis in subsection_analyses.items()
        ])
        
        prompt = f"""
다음은 한 섹션에 대한 두 가지 관점의 분석입니다:

1. **하위섹션별 분석** (작은 단위 분석):
{subsection_summary}

2. **섹션 전체 분석** (큰 단위 분석):
{section_analysis}

**종합 분석 요청:**
- 작은 단위(하위섹션)와 큰 단위(섹션 전체) 분석을 종합
- 두 관점이 서로를 보완하는 지점 파악
- 일관된 섹션 핵심 내용으로 통합

**응답 형식:**
## 종합된 섹션 핵심 내용
[하위섹션들과 섹션 전체 분석을 종합한 통합 핵심 내용]

## 상호 보완 지점
[작은 단위와 큰 단위 분석이 서로를 보완하는 부분]

## 최종 핵심 메시지
[이 섹션의 최종적인 핵심 메시지]
"""
        
        return await self._query_claude(prompt)
    
    async def _update_subsection_analyses(self, original_analyses: Dict[str, str], combined_analysis: str) -> Dict[str, str]:
        """섹션 전체 맥락을 고려하여 하위섹션 분석 업데이트"""
        updated_analyses = {}
        
        for subsection_id, original_analysis in original_analyses.items():
            prompt = f"""
다음은 하위섹션에 대한 초기 분석과 섹션 전체를 고려한 종합 분석입니다:

**하위섹션 {subsection_id} 초기 분석:**
{original_analysis}

**섹션 전체 종합 분석:**
{combined_analysis}

**업데이트 요청:**
- 초기 하위섹션 분석을 유지하되, 섹션 전체 맥락을 반영하여 보완
- 하위섹션의 고유한 내용은 보존하면서 전체 맥락 추가
- 섹션 내에서 이 하위섹션의 역할과 의미 명확화

**응답 형식:**
## 업데이트된 핵심 내용
[전체 맥락을 반영한 하위섹션 핵심 내용]

## 섹션 내 역할
[전체 섹션에서 이 하위섹션의 구체적 역할]

## 연결점
[다른 하위섹션들과의 연관성]
"""
            
            updated_analysis = await self._query_claude(prompt)
            updated_analyses[subsection_id] = updated_analysis
            print(f"    하위섹션 {subsection_id} 업데이트 완료")
        
        return updated_analyses
    
    async def _analyze_full_chapter(self, chapter_dir: Path, section_analyses: Dict[str, Any]) -> str:
        """전체 장 분석"""
        print("전체 장 분석 수행 중...")
        
        # 섹션 분석들을 요약
        section_summaries = []
        for section_name, section_data in section_analyses.items():
            final_analysis = section_data.get("combined_analysis", "분석 없음")
            section_summaries.append(f"**{section_name}:**\n{final_analysis}")
        
        sections_summary = "\n\n".join(section_summaries)
        
        prompt = f"""
다음은 책의 1장 "Complexity of object-oriented programming"의 각 섹션별 분석 결과입니다:

{sections_summary}

**전체 장 분석 요청:**
- 1장 전체를 관통하는 핵심 주제와 메시지 도출
- 각 섹션이 전체 논의에 기여하는 바 파악
- 장 전체의 논리적 구조와 흐름 분석
- 이 장이 책 전체에서 담당하는 역할 추론

**응답 형식:**
## 1장 핵심 주제
[1장 전체의 중심 주제]

## 주요 논증
[1장에서 전개하는 핵심 논증과 근거]

## 섹션 간 관계
[1.1과 1.2 섹션이 어떻게 연결되어 전체 논의를 구성하는지]

## 책 전체에서의 위치
[이 장이 전체 책에서 담당하는 역할과 의미]

## 결론
[1장의 최종 결론과 다음 장으로의 연결점]
"""
        
        return await self._query_claude(prompt)
    
    async def _query_claude(self, prompt: str) -> str:
        """Claude Code SDK를 사용하여 분석 수행"""
        try:
            messages: List[Message] = []
            async for message in query(
                prompt=prompt,
                options=ClaudeCodeOptions(max_turns=1)
            ):
                messages.append(message)
            
            # 마지막 메시지에서 result 속성 추출
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'result'):
                    return last_message.result
                elif hasattr(last_message, 'content'):
                    return last_message.content
                else:
                    return str(last_message)
            
            return "Claude 응답을 받을 수 없습니다."
            
        except Exception as e:
            print(f"Claude 쿼리 오류: {e}")
            return f"분석 중 오류 발생: {e}"
    
    async def _save_analysis_results(self, chapter_dir: Path, results: Dict[str, Any]) -> None:
        """분석 결과를 파일로 저장"""
        analysis_dir = chapter_dir / "analysis_results"
        analysis_dir.mkdir(exist_ok=True)
        
        # JSON으로 전체 결과 저장
        with open(analysis_dir / "recursive_analysis.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # 섹션별 분석 결과를 개별 파일로 저장
        for section_name, section_data in results["section_analyses"].items():
            section_file = analysis_dir / f"{section_name}_analysis.md"
            with open(section_file, "w", encoding="utf-8") as f:
                f.write(f"# {section_name} 재귀적 분석 결과\n\n")
                
                if "combined_analysis" in section_data:
                    f.write("## 최종 종합 분석\n")
                    f.write(section_data["combined_analysis"])
                    f.write("\n\n")
                
                if "updated_subsection_analyses" in section_data:
                    f.write("## 업데이트된 하위섹션 분석\n\n")
                    for subsection_id, analysis in section_data["updated_subsection_analyses"].items():
                        f.write(f"### {subsection_id}\n")
                        f.write(analysis)
                        f.write("\n\n")
        
        # 전체 장 분석 저장
        with open(analysis_dir / "chapter_analysis.md", "w", encoding="utf-8") as f:
            f.write("# Chapter 1 전체 분석 결과\n\n")
            f.write(results["chapter_analysis"])
        
        print(f"분석 결과 저장 완료: {analysis_dir}")

async def main():
    """메인 실행 함수"""
    # 환경 변수 로드
    load_env()
    
    # API 키 확인
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        return
    
    print(f"API 키 확인됨: {api_key[:20]}...")
    
    analyzer = RecursiveBookAnalyzer()
    
    try:
        results = await analyzer.analyze_chapter_1()
        print("\n=== 재귀적 분석 완료 ===")
        print("결과 확인: extracted_content/chapter1/analysis_results/")
        
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())