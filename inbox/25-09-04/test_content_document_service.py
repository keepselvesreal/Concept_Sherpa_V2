# 생성 시간: Wed Sep  4 12:20:30 KST 2025
# 핵심 내용: ContentDocumentService TDD 테스트 (2단계: has_content 결정 + 섹션 추출)
# 상세 내용:
#   - TestContentDocumentService (라인 26-200): ContentDocumentService TDD 테스트 클래스
#   - test_has_content_determination_with_gemini (라인 40-80): Gemini 2.0 Flash 기반 has_content 결정 테스트
#   - test_section_extraction_with_claude (라인 82-120): Claude SDK 기반 섹션 추출 테스트
#   - test_content_document_generation_integration (라인 122-180): 통합 테스트
# 상태: active
# 참조: content_node_analyzer_v2.py 로직을 새 아키텍처로 이관

import pytest
import asyncio
import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# 서비스와 설정 클래스들 임포트
from utils.config_manager import ConfigManager
from utils.logger import LoggerFactory
from services.content_document_service import ContentDocumentService, ContentDocumentResult

class TestContentDocumentService:
    """
    테스트 유형: Social Unit Test
    ContentDocumentService TDD 테스트 - has_content 결정 + 섹션 추출
    
    요구사항:
    - Gemini 2.0 Flash 기반 has_content 필드 값 결정
    - Claude SDK 기반 마크다운 섹션 추출
    - 실제 TOC 데이터와 마크다운 콘텐츠 사용
    
    입력: TOC 데이터 + 마크다운 콘텐츠
    출력: has_content 필드가 업데이트된 TOC + 추출된 섹션 문서들
    """
    
    def setup_method(self):
        """각 테스트 메서드 실행 전 설정"""
        self.config_manager = ConfigManager()
        self.logger_factory = LoggerFactory(self.config_manager)
        self.test_logger = self.logger_factory.create_book_logger("content_doc_test", "./logs")
        
        # 테스트 데이터 경로
        self.target_chapters = [1, 6, 9]
        self.workspace_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/output/Data_Oriented_Programming"
        self.result_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/results/content_document_test"
        
        # ContentDocumentService 초기화
        self.content_service = ContentDocumentService(self.config_manager, self.test_logger)
        
    @pytest.mark.anyio
    async def test_has_content_determination_with_gemini(self):
        """
        Gemini 2.0 Flash 기반 has_content 필드 값 결정 테스트
        
        요구사항:
        - TOC 구조에서 각 노드의 has_content 여부를 AI로 판단
        - Gemini 2.0 Flash 모델 사용
        - 마크다운 콘텐츠를 분석하여 실질적 내용 여부 결정
        
        입력: TOC 구조 + 마크다운 콘텐츠
        출력: has_content 필드가 추가된 업데이트된 TOC
        """
        print(f"\n🤖 Gemini 2.0 Flash 기반 has_content 결정 테스트 시작")
        
        # 1. 테스트 데이터 준비 (장 1 사용)
        chapter_num = 1
        chapter_folder = "1_Complexity_of_object_oriented_programming"
        toc_file = os.path.join(self.workspace_path, chapter_folder, f"{chapter_folder}_toc.json")
        content_file = os.path.join(self.workspace_path, chapter_folder, f"{chapter_folder}_content.md")
        
        print(f"   📋 TOC 파일: {os.path.basename(toc_file)}")
        print(f"   📄 콘텐츠 파일: {os.path.basename(content_file)}")
        
        # 2. 파일 존재 확인
        assert os.path.exists(toc_file), f"TOC 파일 없음: {toc_file}"
        assert os.path.exists(content_file), f"콘텐츠 파일 없음: {content_file}"
        
        # 3. 데이터 로드
        with open(toc_file, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
            
        with open(content_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print(f"   📊 TOC 노드 수: {len(toc_data)}")
        print(f"   📝 마크다운 길이: {len(markdown_content):,} 문자")
        
        # 4. Gemini 2.0 Flash로 has_content 결정 실행
        updated_nodes = await self.content_service.determine_has_content_with_gemini(toc_data, markdown_content)
        
        # 5. 결과 검증
        assert len(updated_nodes) == len(toc_data), "노드 수가 일치하지 않음"
        
        has_content_count = sum(1 for node in updated_nodes if node.get('has_content', False))
        print(f"   ✅ has_content=True 노드: {has_content_count}/{len(updated_nodes)}")
        
        # 모든 노드에 has_content 필드가 추가되었는지 확인
        for node in updated_nodes:
            assert 'has_content' in node, f"노드 {node.get('id')}에 has_content 필드가 없음"
            assert isinstance(node['has_content'], bool), f"노드 {node.get('id')}의 has_content가 boolean이 아님"
        
        print(f"   🎯 Gemini 2.0 Flash 기반 has_content 결정 완료!")
        
        # 결과를 다음 테스트에서 사용할 수 있도록 저장
        self.updated_toc_data = updated_nodes
        
    @pytest.mark.anyio 
    async def test_section_extraction_with_claude(self):
        """
        Claude SDK 기반 섹션 추출 테스트
        
        요구사항:
        - has_content=True인 노드들에 대해서만 섹션 추출
        - Claude SDK 사용하여 마크다운에서 해당 섹션 내용 추출
        - 배치 처리로 병렬 추출 수행
        
        입력: has_content=True 노드들 + 마크다운 콘텐츠
        출력: 각 노드별 추출된 섹션 내용
        """
        print(f"\n🔍 Claude SDK 기반 섹션 추출 테스트 시작")
        
        # 1. 이전 테스트에서 has_content가 결정된 데이터 확인
        if not hasattr(self, 'updated_toc_data'):
            # 이전 테스트가 실행되지 않았다면 다시 실행
            await self.test_has_content_determination_with_gemini()
        
        # 2. 마크다운 콘텐츠 로드
        chapter_num = 1
        chapter_folder = "1_Complexity_of_object_oriented_programming"
        content_file = os.path.join(self.workspace_path, chapter_folder, f"{chapter_folder}_content.md")
        
        with open(content_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # 3. Claude SDK로 섹션 추출 실행
        extracted_docs = await self.content_service.extract_sections_with_claude(
            self.updated_toc_data, markdown_content
        )
        
        # 4. 결과 검증
        has_content_nodes = [node for node in self.updated_toc_data if node.get('has_content', False)]
        expected_extractions = len(has_content_nodes)
        
        print(f"   📊 has_content=True 노드: {expected_extractions}개")
        print(f"   📝 추출된 섹션: {len(extracted_docs)}개")
        
        # 추출된 문서 검증
        assert len(extracted_docs) <= expected_extractions, "추출된 섹션이 예상보다 많음"
        
        for doc in extracted_docs:
            assert 'node_id' in doc, "문서에 node_id가 없음"
            assert 'node_title' in doc, "문서에 node_title이 없음"
            assert 'extracted_content' in doc, "문서에 extracted_content가 없음"
            assert 'extraction_method' in doc, "문서에 extraction_method가 없음"
            assert doc['extraction_method'] == 'claude_sdk', "추출 방법이 claude_sdk가 아님"
            assert len(doc['extracted_content'].strip()) > 0, f"노드 {doc['node_id']}의 추출된 내용이 비어있음"
        
        print(f"   🎯 Claude SDK 기반 섹션 추출 완료!")
        
        # 결과를 다음 테스트에서 사용할 수 있도록 저장
        self.extracted_documents = extracted_docs
        
    @pytest.mark.anyio
    async def test_content_document_generation_integration(self):
        """
        전체 통합 테스트: has_content 결정 → 섹션 추출 → 문서 생성
        
        요구사항:
        - 1단계: Gemini로 has_content 결정
        - 2단계: Claude로 섹션 추출
        - 3단계: 추출된 내용으로 문서 생성 및 저장
        
        입력: 실제 장 데이터
        출력: 내용이 포함된 완성된 문서들
        """
        print(f"\n🎯 ContentDocumentService 전체 통합 테스트 시작")
        
        os.makedirs(self.result_dir, exist_ok=True)
        
        # 1. 장별 폴더에서 전체 처리 실행 (장 1 사용)
        chapter_folder = "1_Complexity_of_object_oriented_programming"
        chapter_path = os.path.join(self.workspace_path, chapter_folder)
        
        print(f"   📂 처리 대상: {chapter_folder}")
        
        # 2. process_chapter_content 메서드로 전체 처리 실행
        result = await self.content_service.process_chapter_content(chapter_path)
        
        # 3. 결과 검증
        assert result.success, f"처리 실패: {result.errors}"
        assert result.processed_nodes > 0, "처리된 노드가 없음"
        assert result.has_content_nodes >= 0, "has_content 노드 수가 음수"
        assert result.extracted_sections >= 0, "추출된 섹션 수가 음수"
        assert len(result.updated_toc) == result.processed_nodes, "업데이트된 TOC 노드 수가 일치하지 않음"
        
        print(f"   📊 처리된 노드: {result.processed_nodes}개")
        print(f"   ✅ has_content 노드: {result.has_content_nodes}개")
        print(f"   📝 추출된 섹션: {result.extracted_sections}개")
        
        # 4. 결과를 파일로 저장
        result_file = os.path.join(self.result_dir, f"{chapter_folder}_content_result.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        
        print(f"   💾 결과 저장: {os.path.basename(result_file)}")
        
        # 5. 추출된 문서들을 개별 파일로 저장
        if result.extracted_documents:
            docs_dir = os.path.join(self.result_dir, "extracted_sections")
            os.makedirs(docs_dir, exist_ok=True)
            
            for doc in result.extracted_documents:
                doc_filename = f"node_{doc['node_id']:02d}_{doc['node_title'].replace(' ', '_')}.md"
                doc_path = os.path.join(docs_dir, doc_filename)
                
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {doc['node_title']}\n\n")
                    f.write(f"노드 ID: {doc['node_id']}\n")
                    f.write(f"추출 방법: {doc['extraction_method']}\n\n")
                    f.write("---\n\n")
                    f.write(doc['extracted_content'])
            
            print(f"   📄 추출된 섹션 문서 저장: {len(result.extracted_documents)}개 파일")
        
        print(f"   🎯 ContentDocumentService 전체 통합 테스트 완료!")
        print(f"   📁 결과 확인 경로: {self.result_dir}")