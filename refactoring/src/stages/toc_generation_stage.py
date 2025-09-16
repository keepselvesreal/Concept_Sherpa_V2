# 생성 시간: Mon Sep 15 22:29:53 KST 2025
# 핵심 내용: 목차 생성 단계 프로세서 (장 수준 및 책 수준 목차 생성)
# 상세 내용:
#   - ToCGenerationStage (라인 28-250): 메인 목차 생성 클래스
#   - process (라인 42-80): 메인 처리 로직 (장/책 목차 생성)
#   - generate_chapter_toc (라인 82-140): 장 수준 목차 생성
#   - generate_book_toc (라인 142-180): 책 수준 목차 생성 
#   - extract_section_from_file (라인 182-210): 파일에서 추출 섹션 추출
#   - parse_level_from_filename (라인 212-230): 파일명에서 레벨 파싱
#   - get_lowest_level_docs (라인 232-250): 가장 낮은 레벨 문서 필터링
# 상태: active

import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import re

# 기본 클래스 임포트
sys.path.append(str(Path(__file__).parent.parent))
from core.base.base_processor import BaseProcessor

# 유틸리티 임포트
from utils.logger_v2 import Logger
from utils.text_utils import normalize_title

class ToCGenerationStage(BaseProcessor):
    """목차 생성 단계 프로세서 (장 수준 및 책 수준 목차 생성)"""
    
    def __init__(self, config_manager, logger_factory=None):
        super().__init__(config_manager, logger_factory, "toc_generation")
        
        # 새로운 통합 Logger 사용
        self.logger = Logger(
            project_name="toc_generation_stage",
            base_dir="./results",
            logs_base_dir="./logs"
        )
        
        # 설정에서 base_dir 가져오기
        self.base_dir = Path(self.config_manager.get('toc_generation.base_dir', '/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data'))
        
    async def process(self, prev_stage_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        메인 목차 생성 처리
        
        Args:
            prev_stage_result: 이전 단계(content_processing_stage)의 출력 결과
            
        Returns:
            Dict: 목차 생성 결과
        """
        try:
            self.logger.info("ToCGenerationStage 시작")
            
            # 이전 단계 결과에서 데이터 추출
            data = prev_stage_result.get('data', {})
            book_title = data.get('book_title', '')
            chapter_info_docs = data.get('chapter_info_docs', {})
            
            self.logger.info(f"책 제목: {book_title}")
            self.logger.info(f"장 개수: {len(chapter_info_docs)}")
            
            # 정규화된 책 이름
            normalized_book_title = normalize_title(book_title)
            
            chapter_toc_results = {}
            book_toc_content = ""
            
            # 1. 각 장별 목차 생성
            for chapter_name, chapter_files in chapter_info_docs.items():
                self.logger.info(f"장 '{chapter_name}' 목차 생성 시작")
                
                chapter_toc_result = await self.generate_chapter_toc(
                    chapter_name, chapter_files, normalized_book_title
                )
                chapter_toc_results[chapter_name] = chapter_toc_result
                
            # 2. 책 수준 목차 생성
            self.logger.info("책 수준 목차 생성 시작")
            book_toc_result = await self.generate_book_toc(
                book_title, chapter_info_docs, normalized_book_title
            )
            
            result = {
                "book_title": book_title,
                "normalized_book_title": normalized_book_title,
                "chapter_tocs": chapter_toc_results,
                "book_toc": book_toc_result
            }
            
            self.logger.info("ToCGenerationStage 완료")
            return {"data": result, "error": None}
            
        except Exception as e:
            error_msg = f"ToCGenerationStage 처리 중 오류 발생: {str(e)}"
            self.logger.error(error_msg)
            return {"data": None, "error": error_msg}

    async def generate_chapter_toc(self, chapter_name: str, chapter_files: List[str], normalized_book_title: str) -> Dict[str, Any]:
        """
        장 수준 목차 생성
        
        Args:
            chapter_name: 장 이름
            chapter_files: 장에 속한 정보 문서 파일 경로 리스트
            normalized_book_title: 정규화된 책 제목
            
        Returns:
            Dict: 장 목차 생성 결과
        """
        try:
            # 정규화된 장 이름
            normalized_chapter_name = normalize_title(chapter_name)
            
            chapter_toc_content = ""
            
            # 각 파일에서 추출 섹션 수집 및 개별 헤더 생성
            extracted_sections = []
            for file_path in chapter_files:
                self.logger.debug(f"파일 처리 중: {file_path}")
                
                full_file_path = self.base_dir / file_path
                if full_file_path.exists():
                    section_content = self.extract_section_from_file(full_file_path)
                    if section_content:
                        # 파일명에서 레벨 파싱
                        file_level = self.parse_level_from_filename(file_path)
                        # 파일명만 추출 (경로 제거)
                        file_name = Path(file_path).name
                        header_prefix = "#" * file_level
                        
                        # 개별 문서 헤더와 추출 섹션 결합 (헤더 바로 밑에 내용)
                        section_with_header = f"{header_prefix} {file_name}\n{section_content}"
                        extracted_sections.append(section_with_header)
                else:
                    self.logger.warning(f"파일을 찾을 수 없음: {full_file_path}")
            
            # 추출된 섹션들을 결합 (섹션 간 2줄 간격)
            if extracted_sections:
                chapter_toc_content = "\n\n\n".join(extracted_sections)
            
            # 파일 저장 경로 생성
            chapter_dir = self.base_dir / normalized_book_title / normalized_chapter_name
            chapter_dir.mkdir(parents=True, exist_ok=True)
            
            toc_file_path = chapter_dir / "chapter_toc.md"
            
            # 파일 저장
            with open(toc_file_path, 'w', encoding='utf-8') as f:
                f.write(chapter_toc_content)
            
            self.logger.info(f"장 목차 저장 완료: {toc_file_path}")
            
            return {
                "chapter_name": chapter_name,
                "normalized_chapter_name": normalized_chapter_name,
                "toc_file_path": str(toc_file_path),
                "sections_count": len(extracted_sections)
            }
            
        except Exception as e:
            error_msg = f"장 '{chapter_name}' 목차 생성 중 오류: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}

    async def generate_book_toc(self, book_title: str, chapter_info_docs: Dict[str, List[str]], normalized_book_title: str) -> Dict[str, Any]:
        """
        책 수준 목차 생성
        
        Args:
            book_title: 책 제목
            chapter_info_docs: 장별 정보 문서 딕셔너리
            normalized_book_title: 정규화된 책 제목
            
        Returns:
            Dict: 책 목차 생성 결과
        """
        try:
            # 책 헤더
            book_toc_content = f"# {book_title}\n\n"
            
            # 각 장에서 가장 낮은 레벨(lev1) 문서의 추출 섹션만 사용
            for chapter_name, chapter_files in chapter_info_docs.items():
                lowest_level_docs = self.get_lowest_level_docs(chapter_files)
                
                if lowest_level_docs:
                    # 정규화된 장 제목을 헤더로 사용 (헤더 바로 밑에 간격 없이)
                    normalized_chapter_name = normalize_title(chapter_name)
                    book_toc_content += f"## {normalized_chapter_name}\n"
                    
                    # 해당 장의 가장 낮은 레벨 문서에서 추출 섹션 가져오기
                    for file_path in lowest_level_docs:
                        full_file_path = self.base_dir / file_path
                        if full_file_path.exists():
                            section_content = self.extract_section_from_file(full_file_path)
                            if section_content:
                                book_toc_content += f"{section_content}\n\n\n"
                        else:
                            self.logger.warning(f"파일을 찾을 수 없음: {full_file_path}")
            
            # 파일 저장 경로 생성
            book_dir = self.base_dir / normalized_book_title
            book_dir.mkdir(parents=True, exist_ok=True)
            
            book_toc_file_path = book_dir / "book_toc.md"
            
            # 파일 저장
            with open(book_toc_file_path, 'w', encoding='utf-8') as f:
                f.write(book_toc_content)
            
            self.logger.info(f"책 목차 저장 완료: {book_toc_file_path}")
            
            return {
                "book_title": book_title,
                "normalized_book_title": normalized_book_title,
                "toc_file_path": str(book_toc_file_path),
                "chapters_count": len(chapter_info_docs)
            }
            
        except Exception as e:
            error_msg = f"책 '{book_title}' 목차 생성 중 오류: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}

    def extract_section_from_file(self, file_path: Path) -> Optional[str]:
        """
        파일에서 추출 섹션(# 추출 이후 모든 내용) 추출
        
        Args:
            file_path: 파일 경로
            
        Returns:
            str: 추출된 섹션 내용 (없으면 None)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # "# 추출" 섹션 찾기
            extract_match = re.search(r'^# 추출\s*\n---\n(.*?)(?=^# [^추]|\Z)', content, re.MULTILINE | re.DOTALL)
            if extract_match:
                return extract_match.group(1).strip()
            
            self.logger.warning(f"추출 섹션을 찾을 수 없음: {file_path}")
            return None
            
        except Exception as e:
            self.logger.error(f"파일 읽기 오류 {file_path}: {str(e)}")
            return None

    def parse_level_from_filename(self, filename: str) -> int:
        """
        파일명에서 레벨 추출 (예: 27_lev1_... -> 1)
        
        Args:
            filename: 파일명
            
        Returns:
            int: 레벨 번호 (기본값: 1)
        """
        try:
            # lev 패턴 찾기
            level_match = re.search(r'lev(\d+)', filename)
            if level_match:
                return int(level_match.group(1))
            
            self.logger.warning(f"파일명에서 레벨을 찾을 수 없음: {filename}")
            return 1  # 기본값
            
        except Exception as e:
            self.logger.error(f"레벨 파싱 오류 {filename}: {str(e)}")
            return 1

    def get_lowest_level_docs(self, file_paths: List[str]) -> List[str]:
        """
        파일 목록에서 가장 낮은 레벨(lev1이 가장 낮음) 문서들 필터링
        
        Args:
            file_paths: 파일 경로 리스트
            
        Returns:
            List[str]: 가장 낮은 레벨 문서들
        """
        try:
            # 각 파일의 레벨 파싱
            file_levels = []
            for file_path in file_paths:
                level = self.parse_level_from_filename(file_path)
                file_levels.append((file_path, level))
            
            # 가장 낮은 레벨 찾기
            if not file_levels:
                return []
            
            min_level = min(level for _, level in file_levels)
            
            # 가장 낮은 레벨의 파일들만 반환
            lowest_level_files = [file_path for file_path, level in file_levels if level == min_level]
            
            self.logger.debug(f"가장 낮은 레벨 {min_level}: {len(lowest_level_files)}개 파일")
            return lowest_level_files
            
        except Exception as e:
            self.logger.error(f"최저 레벨 문서 필터링 오류: {str(e)}")
            return []