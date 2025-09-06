# 생성 시간: Tue Sep  2 14:57:29 KST 2025
# 핵심 내용: 북 파이프라인 단계별 테스트 (노드 정보 문서 → 콘텐츠 분석 → 통합 → 처리 → 목차 생성)
# 상세 내용:
#   - TestPipelineStages (라인 32-350): 메인 테스트 클래스
#   - setup_method (라인 36-51): 테스트 전 설정 초기화
#   - test_stage_1_node_document_generation (라인 53-85): 노드 정보 문서 생성 테스트
#   - test_stage_2_content_node_analysis (라인 87-120): 콘텐츠 노드 분석 테스트
#   - test_stage_3_document_integration (라인 122-155): 문서 통합 테스트
#   - test_stage_4_unified_node_processing (라인 157-195): 통합 노드 문서 처리 테스트
#   - test_stage_5_chapter_toc_generation (라인 197-230): 장별 목차 생성 테스트
#   - test_error_scenarios (라인 232-280): 에러 시나리오 테스트
#   - helper methods (라인 282-350): 테스트 헬퍼 메서드들
# 상태: active
# 주소: test_pipeline_stages
# 참조: book_pipeline_v3.py

import pytest
import os
import sys
import shutil
import tempfile
import yaml
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

# 필요한 모듈 경로 추가
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-29')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-30')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-31')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/process')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/components')
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/pipeline')

# 테스트 대상 모듈 임포트
from content_node_analyzer_v2 import ContentNodeAnalyzer
from node_document_generator import NodeDocumentGenerator
from document_integrator import DocumentIntegrator
from unified_node_processor_v4 import UnifiedNodeProcessor
from chapter_toc_generator import combine_extracts

class TestPipelineStages:
    """파이프라인 단계별 테스트"""
    
    def setup_method(self):
        """각 테스트 전 실행되는 설정"""
        self.test_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/tests")
        self.config_path = self.test_dir / "test_extraction_config.yaml"
        self.fixtures_dir = self.test_dir / "fixtures"
        self.logs_dir = self.test_dir / "logs"
        
        # 로그 디렉토리 정리 및 생성
        if self.logs_dir.exists():
            shutil.rmtree(self.logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # 테스트 출력 디렉토리 정리
        test_outputs = self.test_dir / "outputs"
        if test_outputs.exists():
            shutil.rmtree(test_outputs)
        test_outputs.mkdir(parents=True, exist_ok=True)
    
    def test_stage_1_node_document_generation(self):
        """1단계: 노드 정보 문서 생성 테스트"""
        print("🔄 1단계: 노드 정보 문서 생성 테스트 시작")
        
        # 테스트 데이터 경로
        test_chapters = ["chapter_1", "chapter_6", "chapter_9"]
        
        for chapter in test_chapters:
            chapter_dir = self.fixtures_dir / chapter
            toc_files = list(chapter_dir.glob("*_toc.json"))
            
            if not toc_files:
                pytest.fail(f"❌ {chapter}: toc.json 파일을 찾을 수 없음")
            
            toc_file = str(toc_files[0])
            
            # NodeDocumentGenerator 초기화 및 실행
            generator = NodeDocumentGenerator()
            
            try:
                result = generator.generate_documents_for_chapter(
                    toc_file=toc_file,
                    chapter_folder=str(chapter_dir)
                )
                
                assert result.success, f"❌ {chapter}: 노드 문서 생성 실패 - {result.error}"
                assert result.created_count > 0, f"❌ {chapter}: 생성된 문서가 없음"
                
                print(f"✅ {chapter}: 노드 문서 {result.created_count}개 생성 성공")
                
                # 생성된 파일 확인
                node_info_dir = chapter_dir / "node_info_docs"
                assert node_info_dir.exists(), f"❌ {chapter}: node_info_docs 폴더 미생성"
                
            except Exception as e:
                pytest.fail(f"❌ {chapter}: 노드 문서 생성 중 예외 발생 - {str(e)}")
    
    def test_stage_2_content_node_analysis(self):
        """2단계: 콘텐츠 노드 분석 테스트"""
        print("🔄 2단계: 콘텐츠 노드 분석 테스트 시작")
        
        # 1단계가 완료되어야 함
        self.test_stage_1_node_document_generation()
        
        test_chapters = ["chapter_1", "chapter_6", "chapter_9"]
        
        for chapter in test_chapters:
            chapter_dir = self.fixtures_dir / chapter
            toc_files = list(chapter_dir.glob("*_toc.json"))
            content_files = list(chapter_dir.glob("*_content.md"))
            
            if not toc_files or not content_files:
                pytest.fail(f"❌ {chapter}: 필요한 파일이 없음")
            
            toc_file = str(toc_files[0])
            content_file = str(content_files[0])
            
            # ContentNodeAnalyzer 초기화 및 실행
            analyzer = ContentNodeAnalyzer(
                config_path=str(self.config_path)
            )
            
            try:
                result = asyncio.run(
                    analyzer.analyze_chapter_toc(toc_file, content_file)
                )
                
                assert result.get('success', False), f"❌ {chapter}: 콘텐츠 분석 실패 - {result.get('error', '알 수 없는 오류')}"
                assert len(result.get('extracted_files', [])) > 0, f"❌ {chapter}: 추출된 파일이 없음"
                
                print(f"✅ {chapter}: 콘텐츠 분석 완료, {len(result.get('extracted_files', []))}개 파일 생성")
                
            except Exception as e:
                pytest.fail(f"❌ {chapter}: 콘텐츠 분석 중 예외 발생 - {str(e)}")
    
    def test_stage_3_document_integration(self):
        """3단계: 문서 통합 테스트"""
        print("🔄 3단계: 문서 통합 테스트 시작")
        
        # 2단계가 완료되어야 함
        self.test_stage_2_content_node_analysis()
        
        test_chapters = ["chapter_1", "chapter_6", "chapter_9"]
        
        for chapter in test_chapters:
            chapter_dir = self.fixtures_dir / chapter
            
            # DocumentIntegrator 초기화 및 실행
            integrator = DocumentIntegrator()
            
            try:
                result = integrator.integrate_documents_for_chapter(str(chapter_dir))
                
                assert result.get('success', False), f"❌ {chapter}: 문서 통합 실패 - {result.get('error', '알 수 없는 오류')}"
                assert result.get('integrated_count', 0) > 0, f"❌ {chapter}: 통합된 문서가 없음"
                
                print(f"✅ {chapter}: 문서 통합 완료, {result.get('integrated_count', 0)}개 문서 통합")
                
            except Exception as e:
                pytest.fail(f"❌ {chapter}: 문서 통합 중 예외 발생 - {str(e)}")
    
    def test_stage_4_unified_node_processing(self):
        """4단계: 통합 노드 문서 처리 테스트"""
        print("🔄 4단계: 통합 노드 문서 처리 테스트 시작")
        
        # 3단계가 완료되어야 함
        self.test_stage_3_document_integration()
        
        test_chapters = ["chapter_1", "chapter_6", "chapter_9"]
        
        for chapter in test_chapters:
            chapter_dir = self.fixtures_dir / chapter
            toc_files = list(chapter_dir.glob("*_toc.json"))
            
            if not toc_files:
                pytest.fail(f"❌ {chapter}: toc.json 파일을 찾을 수 없음")
            
            # 임시 설정 파일 생성 (각 장별 동적 설정)
            temp_config = self._create_chapter_config(chapter_dir, toc_files[0])
            
            try:
                # UnifiedNodeProcessor 초기화 및 실행
                processor = UnifiedNodeProcessor(temp_config)
                result = asyncio.run(processor.process_all_nodes())
                
                assert result.get('success', False), f"❌ {chapter}: 노드 처리 실패"
                assert result.get('processed_nodes', 0) > 0, f"❌ {chapter}: 처리된 노드가 없음"
                
                print(f"✅ {chapter}: 노드 처리 완료, {result.get('processed_nodes', 0)}개 노드 처리")
                
            except Exception as e:
                pytest.fail(f"❌ {chapter}: 노드 처리 중 예외 발생 - {str(e)}")
            finally:
                # 임시 설정 파일 정리
                if os.path.exists(temp_config):
                    os.unlink(temp_config)
    
    def test_stage_5_chapter_toc_generation(self):
        """5단계: 장별 목차 생성 테스트"""
        print("🔄 5단계: 장별 목차 생성 테스트 시작")
        
        # 4단계가 완료되어야 함
        self.test_stage_4_unified_node_processing()
        
        test_chapters = ["chapter_1", "chapter_6", "chapter_9"]
        
        for chapter in test_chapters:
            chapter_dir = self.fixtures_dir / chapter
            node_info_dir = chapter_dir / "node_info_docs"
            
            if not node_info_dir.exists():
                pytest.fail(f"❌ {chapter}: node_info_docs 폴더가 없음")
            
            try:
                # combine_extracts 실행
                combined_content = combine_extracts(str(node_info_dir))
                
                assert combined_content.strip(), f"❌ {chapter}: 결합된 내용이 없음"
                
                # enhanced_toc 파일 생성
                chapter_name = chapter.replace('chapter_', '')
                output_file = node_info_dir / f"enhanced_{chapter_name}_toc.md"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(combined_content)
                
                assert output_file.exists(), f"❌ {chapter}: enhanced_toc 파일 미생성"
                
                print(f"✅ {chapter}: enhanced_toc 생성 완료, 파일 크기: {len(combined_content)} 문자")
                
            except Exception as e:
                pytest.fail(f"❌ {chapter}: 목차 생성 중 예외 발생 - {str(e)}")
    
    def test_error_scenarios(self):
        """에러 시나리오 테스트"""
        print("🔄 에러 시나리오 테스트 시작")
        
        # 존재하지 않는 파일 경로 테스트
        generator = NodeDocumentGenerator()
        result = generator.generate_documents_for_chapter(
            toc_file="/nonexistent/path/toc.json",
            chapter_folder="/nonexistent/path"
        )
        assert not result.success, "❌ 존재하지 않는 파일에 대해 성공 반환"
        print("✅ 존재하지 않는 파일 경로 에러 처리 확인")
        
        # 잘못된 JSON 파일 테스트
        temp_json = self.logs_dir / "invalid.json"
        with open(temp_json, 'w') as f:
            f.write("invalid json content")
        
        result = generator.generate_documents_for_chapter(
            toc_file=str(temp_json),
            chapter_folder=str(self.logs_dir)
        )
        assert not result.success, "❌ 잘못된 JSON에 대해 성공 반환"
        print("✅ 잘못된 JSON 파일 에러 처리 확인")
        
        # 빈 폴더 테스트
        empty_dir = self.logs_dir / "empty"
        empty_dir.mkdir(exist_ok=True)
        
        integrator = DocumentIntegrator()
        result = integrator.integrate_documents_for_chapter(str(empty_dir))
        # 빈 폴더는 성공할 수도 있지만 통합된 문서는 0개여야 함
        assert result.get('integrated_count', 0) == 0, "❌ 빈 폴더에서 문서 통합됨"
        print("✅ 빈 폴더 처리 확인")
    
    def _create_chapter_config(self, chapter_dir: Path, toc_file: Path) -> str:
        """장별 동적 설정 파일 생성"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 동적 경로 설정
        config['unified_node_processor']['nodes_json_path'] = str(toc_file)
        config['unified_node_processor']['node_docs_dir'] = str(chapter_dir / "node_info_docs")
        config['unified_node_processor']['debug_dir'] = str(self.logs_dir)
        
        # 임시 설정 파일 저장
        temp_config_path = str(self.logs_dir / f"temp_config_{chapter_dir.name}.yaml")
        with open(temp_config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, ensure_ascii=False, indent=2)
        
        return temp_config_path
    
    def _check_log_files(self):
        """로그 파일 생성 확인"""
        log_files = list(self.logs_dir.glob("**/*.txt"))
        print(f"ℹ️ 생성된 로그 파일: {len(log_files)}개")
        for log_file in log_files:
            print(f"  - {log_file}")
        return len(log_files) > 0

if __name__ == "__main__":
    # 개별 테스트 실행 시
    pytest.main([__file__, "-v"])