# 생성 시간: Thu Sep  4 11:26:52 KST 2025
# 핵심 내용: 통합 노드 정보 문서 생성 단계 프로세서 (book_pipeline_v3의 process_node_documents + 2단계 통합 로직 분리)
# 상세 내용:
#   - IntegratedNodeGenerationStage (라인 XX-XX): 메인 통합 노드 생성 클래스
#   - process (라인 XX-XX): 메인 처리 로직 (3단계 순차 진행)
#   - generate_node_documents (라인 XX-XX): 1단계 - 노드 정보 문서 생성
#   - extract_content_nodes (라인 XX-XX): 2단계 - has_content 할당 및 콘텐츠 노드 추출  
#   - integrate_documents (라인 XX-XX): 3단계 - 문서 통합
# 상태: active
# 참조: book_pipeline_v3.py의 process_node_documents 메서드

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# 기본 클래스 임포트
sys.path.append(str(Path(__file__).parent.parent))
from core.base.base_processor import BaseProcessor

# 새 아키텍처 서비스 임포트  
from services.node_document_service import NodeDocumentService

class IntegratedNodeGenerationStage(BaseProcessor):
    """통합 노드 정보 문서 생성 단계 프로세서 (3단계: 노드정보문서생성 → 콘텐츠노드추출 → 문서통합)"""
    
    def __init__(self, config_manager, logger_factory):
        super().__init__(config_manager, logger_factory, "integrated_node_generation")
        # 기본 로거 초기화
        self.logger = logger_factory.create_book_logger("integrated_node_stage", "./logs")
        self.result_logger = None
        # 새 아키텍처 NodeDocumentService 초기화 (로거 초기화 후)
        self.node_document_service = NodeDocumentService(config_manager, self.logger)
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        메인 통합 노드 생성 처리
        
        Args:
            input_data: {
                'integration_results': List[Dict], # 2단계에서 전달된 장별 통합 결과
                'book_info': Dict,
                'output_dir': str
            }
            
        Returns:
            Dict: 처리 결과
        """
        try:
            self.logger.info("=== 통합 노드 정보 문서 생성 시작 ===")
            
            integration_results = input_data.get('integration_results', [])
            if not integration_results:
                return {
                    'success': False,
                    'error': '처리할 통합 결과가 없습니다',
                    'processed_chapters': 0
                }
                
            book_info = input_data.get('book_info', {})
            output_dir = input_data.get('output_dir', '')
            
            processed_chapters = 0
            node_processing_results = []
            
            # 성공한 장들만 처리
            successful_chapters = [r for r in integration_results if r.get('success', False)]
            
            for chapter_result in successful_chapters:
                chapter_number = chapter_result.get('chapter_number')
                chapter_title = chapter_result.get('chapter_title', '')
                
                self.logger.info(f"장 {chapter_number} 통합 노드 생성 시작: {chapter_title}")
                
                try:
                    # 1단계: 노드 정보 문서 생성
                    node_docs_result = await self.generate_node_documents(
                        chapter_result, book_info, output_dir
                    )
                    
                    if not node_docs_result.get('success', False):
                        raise Exception(f"노드 정보 문서 생성 실패: {node_docs_result.get('error', '')}")
                    
                    # 2단계: 콘텐츠 노드 추출
                    content_nodes_result = await self.extract_content_nodes(
                        chapter_result, node_docs_result, output_dir
                    )
                    
                    if not content_nodes_result.get('success', False):
                        raise Exception(f"콘텐츠 노드 추출 실패: {content_nodes_result.get('error', '')}")
                    
                    # 3단계: 문서 통합
                    integration_result = await self.integrate_documents(
                        chapter_result, content_nodes_result, output_dir
                    )
                    
                    if not integration_result.get('success', False):
                        raise Exception(f"문서 통합 실패: {integration_result.get('error', '')}")
                    
                    # 성공 처리
                    processed_chapters += 1
                    node_processing_results.append({
                        'chapter_number': chapter_number,
                        'chapter_title': chapter_title,
                        'success': True,
                        'node_docs': node_docs_result,
                        'content_nodes': content_nodes_result,
                        'integration': integration_result
                    })
                    
                    self.logger.info(f"장 {chapter_number} 통합 노드 생성 완료")
                    
                except Exception as e:
                    error_msg = str(e)
                    node_processing_results.append({
                        'chapter_number': chapter_number,
                        'chapter_title': chapter_title,
                        'success': False,
                        'error': error_msg
                    })
                    
                    self.logger.error(f"장 {chapter_number} 통합 노드 생성 실패: {error_msg}")
            
            success_count = len([r for r in node_processing_results if r.get('success', False)])
            total_count = len(successful_chapters)
            success_rate = (success_count / total_count * 100) if total_count > 0 else 0
            
            self.logger.info(f"통합 노드 정보 문서 생성 완료: {success_count}/{total_count} 장 성공")
            
            return {
                'success': True,
                'processed_chapters': success_count,
                'total_chapters': total_count,
                'success_rate': success_rate,
                'node_processing_results': node_processing_results
            }
            
        except Exception as e:
            error_msg = f"통합 노드 정보 문서 생성 실패: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    async def generate_node_documents(self, chapter_result: Dict[str, Any], 
                                    book_info: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """1단계: 노드 정보 문서 생성 (NodeDocumentService 사용)"""
        chapter_number = chapter_result.get('chapter_number')
        chapter_title = chapter_result.get('chapter_title', '')
        folder_path = chapter_result.get('folder_path', '')
        toc_file = chapter_result.get('toc_file', '')
        
        try:
            self.logger.info(f"장 {chapter_number} 노드 정보 문서 생성 시작: {chapter_title}")
            
            # 필수 파일 존재 검증
            if not os.path.exists(toc_file):
                error_msg = f"TOC 파일이 존재하지 않습니다: {toc_file}"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            if not os.path.exists(folder_path):
                error_msg = f"장 폴더가 존재하지 않습니다: {folder_path}"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            # NodeDocumentService를 사용한 노드 정보 문서 생성
            self.logger.info(f"NodeDocumentService.generate_documents_for_chapter() 호출...")
            node_docs_result = self.node_document_service.generate_documents_for_chapter(
                chapter_folder=folder_path,
                toc_file=toc_file
            )
            
            self.logger.info(f"NodeDocumentService 완료, 결과 확인 중...")
            
            if node_docs_result.success:
                created_count = node_docs_result.created_count
                self.logger.info(f"장 {chapter_number} 노드 정보 문서 생성 완료: {created_count}개 파일")
                
                # NodeDocumentResult를 dict로 변환하여 반환
                return node_docs_result.to_dict()
            else:
                error_msg = f"노드 정보 문서 생성 실패: {node_docs_result.error or '알 수 없는 오류'}"
                self.logger.error(f"장 {chapter_number} {error_msg}")
                return node_docs_result.to_dict()
                
        except Exception as e:
            error_msg = f"노드 정보 문서 생성 중 예외: {str(e)}"
            self.logger.error(f"장 {chapter_number} {error_msg}")
            return {'success': False, 'error': error_msg}
    
    async def extract_content_nodes(self, chapter_result: Dict[str, Any], 
                                  node_docs_result: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """2단계: has_content 할당 및 콘텐츠 노드 추출"""
        # TODO: ContentNodeAnalyzer를 사용한 콘텐츠 노드 추출 로직
        return {'success': True, 'placeholder': True}
    
    async def integrate_documents(self, chapter_result: Dict[str, Any], 
                                content_nodes_result: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """3단계: 문서 통합"""
        # TODO: DocumentIntegrator를 사용한 문서 통합 로직
        return {'success': True, 'placeholder': True}