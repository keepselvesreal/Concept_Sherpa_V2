# 생성 시간: Wed Sep  4 12:35:20 KST 2025
# 핵심 내용: 콘텐츠 문서 생성 서비스 (has_content 결정 + 섹션 추출) - AIService 활용
# 상세 내용:
#   - ContentDocumentService (라인 30-180): 메인 서비스 클래스
#   - determine_has_content_with_gemini (라인 45-85): AIService를 통한 has_content 결정
#   - extract_sections_with_claude (라인 87-125): AIService를 통한 섹션 추출
#   - process_chapter_content (라인 127-170): 통합 처리 메서드
#   - ContentDocumentResult (라인 180-200): 처리 결과 데이터 클래스
# 상태: active
# 참조: extraction-system/pipeline/content_node_analyzer_v2.py 로직 이관, 기존 AIService 활용

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from services.ai_service import AIService

@dataclass
class ContentDocumentResult:
    """콘텐츠 문서 생성 결과 데이터 클래스"""
    success: bool = False
    processed_nodes: int = 0
    has_content_nodes: int = 0
    extracted_sections: int = 0
    errors: List[str] = field(default_factory=list)
    updated_toc: List[Dict[str, Any]] = field(default_factory=list)
    extracted_documents: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리 형태로 변환"""
        return {
            'success': self.success,
            'processed_nodes': self.processed_nodes,
            'has_content_nodes': self.has_content_nodes,
            'extracted_sections': self.extracted_sections,
            'errors': self.errors,
            'updated_toc': self.updated_toc,
            'extracted_documents': self.extracted_documents
        }

class ContentDocumentService:
    """콘텐츠 문서 생성 서비스 - has_content 결정 + 섹션 추출"""
    
    def __init__(self, config_manager=None, logger=None):
        """
        Args:
            config_manager: 설정 관리자 (새 아키텍처 호환)
            logger: 로거 인스턴스 (새 아키텍처 호환)
        """
        self.config_manager = config_manager
        self.logger = logger
        
        # AIService를 사용한 AI 클라이언트 설정
        try:
            self.ai_service = AIService(config_manager, logger, "information_integration")
            if logger:
                logger.info("ContentDocumentService AI 서비스 설정 완료 (information_integration)")
        except Exception as e:
            error_msg = f"AI 서비스 초기화 실패: {e}"
            if logger:
                logger.error(error_msg)
            else:
                print(f"❌ {error_msg}")
            self.ai_service = None
    
    async def determine_has_content(self, toc_nodes: List[Dict[str, Any]], 
                                               markdown_content: str) -> List[Dict[str, Any]]:
        """
        AIService를 통해 각 TOC 노드의 has_content 여부를 결정합니다.
        
        Args:
            toc_nodes: TOC 노드 리스트
            markdown_content: 마크다운 콘텐츠
            
        Returns:
            has_content 필드가 추가된 TOC 노드 리스트
        """
        if not self.ai_service:
            self.logger.error("AI 서비스가 설정되지 않았습니다") if self.logger else print("❌ AI 서비스가 설정되지 않았습니다")
            return toc_nodes
        
        updated_nodes = []
        
        for node in toc_nodes:
            try:
                # 노드별 콘텐츠 분석을 위한 프롬프트 생성
                analysis_prompt = f"""
다음 TOC 노드가 실질적인 내용을 담고 있는지 분석해주세요:

노드 정보:
- ID: {node.get('id')}
- 제목: {node.get('title')}

마크다운 콘텐츠 (처음 2000자):
{markdown_content[:2000]}

판단 기준:
1. 단순 목차나 제목만 있는 경우: false
2. 실질적인 설명, 예제, 코드가 포함된 경우: true
3. "Introduction"이나 "Summary" 같은 구조적 섹션도 내용이 있으면: true

응답 형식: JSON {{ "has_content": true/false, "reason": "판단 이유" }}
"""
                
                # AIService의 process_content 메서드 사용
                result = await self.ai_service.process_content(analysis_prompt, "has_content_analysis")
                
                if result.get('success', False):
                    # AI 응답에서 has_content 값 추출 (간단한 파싱)
                    response_text = result.get('processed_content', '').strip().lower()
                    has_content = 'true' in response_text
                else:
                    # AI 처리 실패시 기본값 false
                    has_content = False
                    if self.logger:
                        self.logger.warning(f"AI 분석 실패 (노드 {node.get('id')}): {result.get('error', '알 수 없는 오류')}")
                
                # 노드에 has_content 필드 추가
                updated_node = node.copy()
                updated_node['has_content'] = has_content
                updated_nodes.append(updated_node)
                
                if self.logger:
                    self.logger.debug(f"노드 {node.get('id')} has_content: {has_content}")
                
            except Exception as e:
                error_msg = f"has_content 분석 실패 (노드 {node.get('id')}): {e}"
                if self.logger:
                    self.logger.error(error_msg)
                else:
                    print(f"❌ {error_msg}")
                
                # 오류 시 기본값으로 false 설정
                updated_node = node.copy()
                updated_node['has_content'] = False
                updated_nodes.append(updated_node)
        
        return updated_nodes
    
    async def extract_sections_with_claude(self, nodes_with_content: List[Dict[str, Any]], 
                                         markdown_content: str) -> List[Dict[str, Any]]:
        """
        AIService를 통해 has_content=True인 노드들의 섹션을 추출합니다.
        
        Args:
            nodes_with_content: has_content 필드가 있는 노드 리스트
            markdown_content: 마크다운 콘텐츠
            
        Returns:
            추출된 섹션 문서 리스트
        """
        if not self.ai_service:
            self.logger.error("AI 서비스가 설정되지 않았습니다") if self.logger else print("❌ AI 서비스가 설정되지 않았습니다")
            return []
        
        extracted_documents = []
        content_nodes = [node for node in nodes_with_content if node.get('has_content', False)]
        
        for node in content_nodes:
            try:
                # 섹션 추출을 위한 프롬프트
                extraction_prompt = f"""
다음 마크다운 콘텐츠에서 특정 노드의 섹션을 정확히 추출해주세요:

추출 대상 노드:
- ID: {node.get('id')}
- 제목: {node.get('title')}
- 레벨: {node.get('level')}
- 페이지 범위: {node.get('page_range', 'N/A')}

마크다운 콘텐츠:
{markdown_content}

추출 요청:
1. 위 노드 제목에 해당하는 섹션의 내용을 정확히 추출
2. 제목, 설명, 예제, 코드 등 모든 관련 내용 포함
3. 마크다운 형식 유지

응답 형식: 추출된 섹션의 마크다운 콘텐츠만 반환
"""
                
                # AIService의 process_content 메서드 사용
                result = await self.ai_service.process_content(extraction_prompt, "section_extraction")
                
                if result.get('success', False):
                    extracted_content = result.get('processed_content', '')
                    
                    # 추출된 문서 정보 생성
                    document = {
                        'node_id': node.get('id'),
                        'node_title': node.get('title'),
                        'node_level': node.get('level'),
                        'extracted_content': extracted_content,
                        'extraction_method': 'ai_service'
                    }
                    
                    extracted_documents.append(document)
                    
                    if self.logger:
                        self.logger.debug(f"섹션 추출 완료: 노드 {node.get('id')}")
                else:
                    if self.logger:
                        self.logger.error(f"섹션 추출 실패 (노드 {node.get('id')}): {result.get('error', '알 수 없는 오류')}")
                
            except Exception as e:
                error_msg = f"섹션 추출 실패 (노드 {node.get('id')}): {e}"
                if self.logger:
                    self.logger.error(error_msg)
                else:
                    print(f"❌ {error_msg}")
        
        return extracted_documents
    
    async def process_chapter_content(self, chapter_folder: str, 
                                    target_chapters: Optional[List[int]] = None) -> ContentDocumentResult:
        """
        특정 장의 콘텐츠를 처리합니다 - has_content 결정 + 섹션 추출
        
        Args:
            chapter_folder: 장별 폴더 경로
            target_chapters: 처리할 장 번호 리스트 (None이면 모든 장)
            
        Returns:
            처리 결과
        """
        result = ContentDocumentResult()
        
        try:
            if self.logger:
                self.logger.info(f"콘텐츠 문서 생성 시작: {os.path.basename(chapter_folder)}")
            
            # TOC 파일 찾기
            toc_files = list(Path(chapter_folder).glob("*_toc.json"))
            if not toc_files:
                result.errors.append(f"TOC 파일을 찾을 수 없음: {chapter_folder}")
                return result
            
            toc_file = str(toc_files[0])
            
            # 마크다운 콘텐츠 파일 찾기  
            content_files = list(Path(chapter_folder).glob("*_content.md"))
            if not content_files:
                result.errors.append(f"콘텐츠 파일을 찾을 수 없음: {chapter_folder}")
                return result
            
            content_file = str(content_files[0])
            
            # 파일 로드
            with open(toc_file, 'r', encoding='utf-8') as f:
                toc_nodes = json.load(f)
                
            with open(content_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            result.processed_nodes = len(toc_nodes)
            
            # 1단계: AIService로 has_content 결정
            updated_nodes = await self.determine_has_content_with_gemini(toc_nodes, markdown_content)
            result.has_content_nodes = len([n for n in updated_nodes if n.get('has_content', False)])
            result.updated_toc = updated_nodes
            
            # 2단계: AIService로 섹션 추출
            extracted_docs = await self.extract_sections_with_claude(updated_nodes, markdown_content)
            result.extracted_sections = len(extracted_docs)
            result.extracted_documents = extracted_docs
            
            result.success = True
            
            if self.logger:
                self.logger.info(f"콘텐츠 문서 생성 완료: 노드 {result.processed_nodes}개 처리, 섹션 {result.extracted_sections}개 추출")
            
            return result
            
        except Exception as e:
            error_msg = f"콘텐츠 문서 생성 중 오류: {e}"
            result.errors.append(error_msg)
            result.success = False
            if self.logger:
                self.logger.error(error_msg)
            return result