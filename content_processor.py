"""
chapter1_core_content.md 파일을 파싱하여 
목차 형태 핵심 내용과 상세 핵심 내용을 분리 처리
"""

import re
from typing import Dict, List, Tuple, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentProcessor:
    """
    core_content.md 파일을 파싱하여 임베딩 저장용 데이터 구조로 변환
    """
    
    def __init__(self, content_file_path: str):
        """
        컨텐츠 프로세서 초기화
        
        Args:
            content_file_path: chapter1_core_content.md 파일 경로
        """
        self.content_file_path = content_file_path
        self.raw_content = self._read_file()
        
    def _read_file(self) -> str:
        """파일 내용 읽기"""
        try:
            with open(self.content_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"파일 읽기 완료: {self.content_file_path}")
            return content
        except Exception as e:
            logger.error(f"파일 읽기 실패: {e}")
            raise
    
    def parse_core_content(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        핵심 내용 파싱하여 목차 형태와 상세 내용으로 분리
        
        Returns:
            (core_content_list, detailed_content_list) 튜플
        """
        try:
            # 목차 형태 핵심 내용과 상세 핵심 내용 분리
            toc_section, detailed_section = self._split_main_sections()
            
            # 목차 형태 핵심 내용 파싱
            core_content_list = self._parse_toc_section(toc_section)
            
            # 상세 핵심 내용 파싱  
            detailed_content_list = self._parse_detailed_section(detailed_section)
            
            logger.info(f"파싱 완료 - 핵심: {len(core_content_list)}, 상세: {len(detailed_content_list)}")
            
            return core_content_list, detailed_content_list
            
        except Exception as e:
            logger.error(f"컨텐츠 파싱 실패: {e}")
            raise
    
    def _split_main_sections(self) -> Tuple[str, str]:
        """메인 섹션 분리"""
        # "## 상세 핵심 내용" 기준으로 분리
        parts = self.raw_content.split("## 상세 핵심 내용 (세부사항 검색용)")
        
        if len(parts) != 2:
            raise ValueError("문서 구조가 예상과 다릅니다. '## 상세 핵심 내용' 섹션을 찾을 수 없습니다.")
        
        toc_section = parts[0]
        detailed_section = parts[1]
        
        return toc_section, detailed_section
    
    def _parse_toc_section(self, toc_section: str) -> List[Dict[str, Any]]:
        """목차 형태 핵심 내용 파싱"""
        core_content_list = []
        
        # 각 섹션별로 분리하여 파싱
        sections = self._extract_toc_sections(toc_section)
        
        for section in sections:
            # 상위 섹션인지 하위 섹션인지 판단
            if self._is_composite_section(section):
                # 상위 섹션: 메타데이터 구조체
                core_content_list.append(self._create_composite_section(section))
            else:
                # 하위 섹션: 원문 포함 (실제로는 sections 디렉토리에서 읽어와야 함)
                core_content_list.append(self._create_leaf_section(section))
        
        return core_content_list
    
    def _parse_detailed_section(self, detailed_section: str) -> List[Dict[str, Any]]:
        """상세 핵심 내용 파싱"""
        detailed_content_list = []
        
        # 상세 분석 섹션들 추출
        detailed_analyses = self._extract_detailed_analyses(detailed_section)
        
        for analysis in detailed_analyses:
            detailed_content_list.append(self._create_detailed_analysis(analysis))
        
        return detailed_content_list
    
    def _extract_toc_sections(self, toc_section: str) -> List[Dict[str, str]]:
        """목차 형태 섹션들 추출"""
        sections = []
        
        # 각 섹션별 정규식 패턴
        patterns = [
            (r'### Chapter 1 전체 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|$)', 'chapter1', 'composite'),
            (r'### Chapter Introduction 핵심 내용\s*\n\*\*(.*?)\*\*:(.*?)(?=###|$)', 'chapter_intro', 'composite'),  
            (r'### Section 1\.1 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_1', 'composite'),
            (r'#### Section 1\.1\.1 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_1_1', 'leaf'),
            (r'#### Section 1\.1\.2 핵심 내용\s*\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_1_2', 'leaf'),
            (r'#### Section 1\.1\.3 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_1_3', 'leaf'),
            (r'#### Section 1\.1\.4 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_1_4', 'leaf'),
            (r'### Section 1\.2 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_2', 'composite'),
            (r'#### Section 1\.2\.1 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_2_1', 'leaf'),
            (r'#### Section 1\.2\.2 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_2_2', 'leaf'),
            (r'#### Section 1\.2\.3 핵심 내용\s*\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_2_3', 'leaf'),
            (r'#### Section 1\.2\.4 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|####|$)', 'section_1_2_4', 'leaf'),
            (r'### Summary 핵심 내용\n\*\*(.*?)\*\*:(.*?)(?=###|$)', 'summary', 'leaf')
        ]
        
        for pattern, section_id, section_type in patterns:
            match = re.search(pattern, toc_section, re.DOTALL)
            if match:
                title = match.group(1).strip()
                content = match.group(2).strip()
                sections.append({
                    'id': section_id,
                    'title': title,
                    'content': content,
                    'type': section_type
                })
        
        return sections
    
    def _extract_detailed_analyses(self, detailed_section: str) -> List[Dict[str, str]]:
        """상세 분석 섹션들 추출"""
        analyses = []
        
        # 상세 분석 패턴들
        patterns = [
            (r'### Chapter Introduction 상세 분석(.*?)(?=###|$)', 'chapter_intro_detail'),
            (r'### Section 1\.1 상세 분석(.*?)(?=###|$)', 'section_1_1_detail'), 
            (r'#### 1\.1\.1 The design phase 상세 내용(.*?)(?=###|####|$)', 'section_1_1_1_detail'),
            (r'#### 1\.1\.2 UML 101 상세 내용(.*?)(?=###|####|$)', 'section_1_1_2_detail'),
            (r'#### 1\.1\.3 Explaining each piece 상세 내용(.*?)(?=###|####|$)', 'section_1_1_3_detail'),
            (r'#### 1\.1\.4 Implementation phase 상세 내용(.*?)(?=###|####|$)', 'section_1_1_4_detail'),
            (r'### Section 1\.2 상세 분석(.*?)(?=###|$)', 'section_1_2_detail'),
            (r'#### 1\.2 Introduction 상세 내용(.*?)(?=###|####|$)', 'section_1_2_intro_detail'),
            (r'#### 1\.2\.1 Many relations 상세 내용(.*?)(?=###|####|$)', 'section_1_2_1_detail'),
            (r'#### 1\.2\.2 Unpredictable behavior 상세 내용(.*?)(?=###|####|$)', 'section_1_2_2_detail'),
            (r'#### 1\.2\.3 Data serialization 상세 내용(.*?)(?=###|####|$)', 'section_1_2_3_detail'),
            (r'#### 1\.2\.4 Complex hierarchies 상세 내용(.*?)(?=###|####|$)', 'section_1_2_4_detail'),
            (r'### Summary 상세 분석(.*?)(?=###|$)', 'summary_detail')
        ]
        
        for pattern, analysis_id in patterns:
            match = re.search(pattern, detailed_section, re.DOTALL)
            if match:
                content = match.group(1).strip()
                analyses.append({
                    'id': analysis_id,
                    'content': content,
                    'core_ref': analysis_id.replace('_detail', '')  # detail 제거하여 core_ref 생성
                })
        
        return analyses
    
    def _is_composite_section(self, section: Dict) -> bool:
        """상위 섹션(composite) 여부 판단"""
        return section['type'] == 'composite'
    
    def _create_composite_section(self, section: Dict) -> Dict[str, Any]:
        """상위 섹션 데이터 생성"""
        # 하위 섹션 매핑
        composed_of_map = {
            'chapter1': ['chapter_intro', 'section_1_1', 'section_1_2', 'summary'],
            'chapter_intro': [],  # 말단 섹션
            'section_1_1': ['section_1_1_1', 'section_1_1_2', 'section_1_1_3', 'section_1_1_4'],
            'section_1_2': ['section_1_2_1', 'section_1_2_2', 'section_1_2_3', 'section_1_2_4']
        }
        
        return {
            'id': section['id'],
            'embedding_text': f"{section['title']}: {section['content']}",
            'document': {
                'type': 'composite_section',
                'title': section['title'],
                'composed_of': composed_of_map.get(section['id'], []),
                'content_summary': section['content'],
                'page_range': 'TBD'  # 실제로는 메타데이터에서 가져와야 함
            }
        }
    
    def _create_leaf_section(self, section: Dict) -> Dict[str, Any]:
        """하위 섹션 데이터 생성"""
        # 실제로는 sections 디렉토리에서 원문을 읽어와야 함
        original_text = self._load_original_text(section['id'])
        
        return {
            'id': section['id'],
            'embedding_text': f"{section['title']}: {section['content']}",
            'document': original_text
        }
    
    def _create_detailed_analysis(self, analysis: Dict) -> Dict[str, Any]:
        """상세 분석 데이터 생성"""
        return {
            'id': analysis['id'],
            'embedding_text': analysis['content'],
            'core_ref': analysis['core_ref']
        }
    
    def _load_original_text(self, section_id: str) -> str:
        """원문 텍스트 로딩 (sections 디렉토리에서)"""
        try:
            # sections 디렉토리 경로 구성
            import os
            base_dir = os.path.dirname(self.content_file_path) 
            sections_dir = os.path.join(base_dir, 'content', 'sections')
            
            # 섹션 ID를 파일명으로 변환
            filename = f"{section_id}.md"
            file_path = os.path.join(sections_dir, filename)
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                logger.warning(f"원문 파일을 찾을 수 없음: {file_path}")
                return f"# {section_id}\n\n원문을 찾을 수 없습니다."
                
        except Exception as e:
            logger.error(f"원문 로딩 실패 ({section_id}): {e}")
            return f"# {section_id}\n\n원문 로딩 실패: {e}"

if __name__ == "__main__":
    # 테스트 코드
    processor = ContentProcessor("/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_Manning/Part1_Flexibility/Chapter1/chapter1_core_content.md")
    
    core_content_list, detailed_content_list = processor.parse_core_content()
    
    print(f"핵심 내용 개수: {len(core_content_list)}")
    print(f"상세 내용 개수: {len(detailed_content_list)}")
    
    # 첫 번째 항목들 출력
    if core_content_list:
        print("\n첫 번째 핵심 내용:")
        print(f"ID: {core_content_list[0]['id']}")
        print(f"임베딩 텍스트: {core_content_list[0]['embedding_text'][:100]}...")
    
    if detailed_content_list:
        print("\n첫 번째 상세 내용:")
        print(f"ID: {detailed_content_list[0]['id']}")
        print(f"Core Ref: {detailed_content_list[0]['core_ref']}")
        print(f"임베딩 텍스트: {detailed_content_list[0]['embedding_text'][:100]}...")