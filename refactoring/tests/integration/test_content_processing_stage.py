# 생성 시간: Thu Sep 12 10:27:33 KST 2025
# 핵심 내용: ContentProcessingStage.load_and_sort_documents level별 그룹화 테스트
# 상세 내용:
#   - TestContentProcessingStage (라인 25-45): 테스트 메인 클래스
#   - test_load_and_sort_documents_level_grouping (라인 27-65): level별 그룹화 정상 동작 테스트
#   - _save_result_data (라인 67-85): 테스트 결과 데이터 저장 유틸리티
# 상태: active

import asyncio
import json
import pytest
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from datetime import datetime

import sys
from pathlib import Path
# refactoring 프로젝트 경로 추가
refactoring_root = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(refactoring_root))

from stages.content_processing_stage import ContentProcessingStage
from utils.logger_v2 import Logger


class TestContentProcessingStage:
    """ContentProcessingStage.load_and_sort_documents level별 그룹화 테스트"""
    
    @pytest.mark.asyncio
    async def test_load_and_sort_documents_level_grouping(self, test_data_manager):
        """
        load_and_sort_documents 메서드가 level별 그룹화를 정상적으로 수행하는지 테스트
        
        테스트 데이터: integrated_node_generation 단계 결과 데이터 사용
        기대 결과: 
        - leaf_nodes: 리스트 형태
        - non_leaf_nodes: 딕셔너리 형태 (level_N 키로 그룹화)
        - level 내림차순 정렬
        """
        print("📋 load_and_sort_documents level별 그룹화 테스트 시작")
        
        # Given - 입력 데이터 로드
        input_data_path = Path(__file__).parent.parent / "data" / "integrated_node_generation_stage" / "process_result.json"
        assert input_data_path.exists(), f"입력 데이터 파일이 없습니다: {input_data_path}"
        
        with open(input_data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # data.unified_documents 필드 추출
        data_result = raw_data.get('data', {})
        unified_documents = data_result.get('unified_documents', [])
        processed_chapters = data_result.get('processed_chapters', [])
        
        # load_and_sort_documents에 필요한 형태로 데이터 구성
        input_data = {
            'unified_documents': unified_documents,
            'processed_chapters': processed_chapters
        }
        assert input_data, "입력 데이터가 비어있습니다"
        
        print(f"📖 입력 데이터 로드 완료: {input_data_path}")
        
        # ContentProcessingStage 초기화
        config = {}
        logger = Logger("test_content_processing_stage")
        stage = ContentProcessingStage(config, logger)
        
        # When - load_and_sort_documents 실행
        result = await stage.load_and_sort_documents(input_data)
        
        # Then - 결과 검증
        assert isinstance(result, dict), "결과는 딕셔너리여야 함"
        assert "output" in result, "output 필드가 있어야 함"
        assert "error" in result, "error 필드가 있어야 함"
        assert result["error"] is None, "성공 시 error는 None이어야 함"
        
        chapters = result["output"]["chapters"]
        assert isinstance(chapters, list), "chapters는 리스트여야 함"
        assert len(chapters) > 0, "결과가 비어있으면 안됨"
        
        # 각 장별 구조 검증
        total_leaf_nodes = 0
        total_non_leaf_groups = 0
        
        for i, chapter in enumerate(chapters):
            print(f"📄 {i+1}장 검증 중...")
            
            # 기본 구조 확인
            assert isinstance(chapter, dict), f"{i+1}장은 딕셔너리여야 함"
            assert "leaf_nodes" in chapter, f"{i+1}장에 leaf_nodes 필드가 있어야 함"
            assert "non_leaf_nodes" in chapter, f"{i+1}장에 non_leaf_nodes 필드가 있어야 함"
            
            # leaf_nodes 검증 (리스트)
            leaf_nodes = chapter["leaf_nodes"]
            assert isinstance(leaf_nodes, list), f"{i+1}장 leaf_nodes는 리스트여야 함"
            total_leaf_nodes += len(leaf_nodes)
            
            for doc in leaf_nodes:
                composition_files = doc.get('composition_files', [])
                assert len(composition_files) == 0, f"리프 노드는 composition_files가 비어있어야 함: {doc.get('title', 'Unknown')}"
            
            # non_leaf_nodes 검증 (딕셔너리)
            non_leaf_nodes = chapter["non_leaf_nodes"]
            assert isinstance(non_leaf_nodes, dict), f"{i+1}장 non_leaf_nodes는 딕셔너리여야 함"
            
            if len(non_leaf_nodes) > 0:
                # level 키 순서 확인 (내림차순)
                level_keys = list(non_leaf_nodes.keys())
                if len(level_keys) > 1:
                    prev_level_num = float('inf')
                    for level_key in level_keys:
                        assert level_key.startswith("level_"), f"level 키는 'level_'로 시작해야 함: {level_key}"
                        current_level_num = int(level_key.split('_')[1])
                        assert current_level_num <= prev_level_num, f"level 키가 내림차순으로 정렬되어야 함"
                        prev_level_num = current_level_num
                
                # 각 level 그룹 내 노드들 검증
                for level_key, nodes in non_leaf_nodes.items():
                    assert isinstance(nodes, list), f"{level_key}의 값은 리스트여야 함"
                    expected_level = int(level_key.split('_')[1])
                    total_non_leaf_groups += len(nodes)
                    
                    for doc in nodes:
                        composition_files = doc.get('composition_files', [])
                        assert len(composition_files) > 0, f"비리프 노드는 composition_files가 있어야 함"
                        actual_level = doc.get('level', 0)
                        assert actual_level == expected_level, f"level이 일치하지 않음: 예상 {expected_level}, 실제 {actual_level}"
        
        print(f"✅ level별 그룹화 테스트 완료:")
        print(f"   - 총 {len(chapters)}개 장 처리")
        print(f"   - 리프 노드: {total_leaf_nodes}개")
        print(f"   - 비리프 노드: {total_non_leaf_groups}개")
        
        # 결과 데이터 저장 (test_data_manager 사용)
        test_data_manager.save_test_result(
            test_method_name="load_and_sort_documents",
            result_data=result
        )
        
        return result

    @pytest.mark.asyncio
    async def test_generate_extract_section(self, test_data_manager):
        """
        generate_extract_section 정상 동작 테스트
        
        테스트 범위: 1장의 리프 노드 1개만 (비용 절약 및 안전성)
        입력: load_and_sort_documents_result.json의 첫 번째 장 첫 번째 리프 노드
        출력: 5개 섹션 추출 결과 (핵심내용, 상세핵심내용, 상세정보, 주요화제, 부차화제)
        """
        print("🤖 generate_extract_section 테스트 시작 (1장 리프노드 1개)")
        
        # 1단계: Config 및 AI 서비스 초기화
        from src.utils.config_manager import ConfigManager
        from src.services.ai_service_v4 import AIService
        
        try:
            config_manager = ConfigManager()
            
            # Logger 초기화
            from src.utils.logger_v2 import Logger
            test_logger = Logger("test_content_processing_stage")
            
            # AIService 초기화 (config_manager, logger, stage_name 필요)
            ai_service = AIService(config_manager, test_logger, "content_processing")
            
            # ContentProcessingStage 초기화 
            ai_config = config_manager.get_ai_config()
            stage = ContentProcessingStage(ai_config, ai_service)
            print("✅ AI 서비스 초기화 완료")
            
        except Exception as e:
            print(f"❌ AI 서비스 초기화 실패: {e}")
            pytest.skip(f"AI 서비스 초기화 실패: {e}")
        
        # 2단계: 테스트 데이터 로드
        input_data_path = Path(__file__).parent.parent / "data" / "content_processing" / "load_and_sort_documents_result.json"
        assert input_data_path.exists(), f"테스트 데이터 파일이 없습니다: {input_data_path}"
        
        with open(input_data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        chapters_data = raw_data["output"]["chapters"]
        assert len(chapters_data) > 0, "테스트용 장 데이터가 비어있습니다"
        print(f"📖 테스트 데이터 로드 완료: {len(chapters_data)}개 장")
        
        
        # 3단계: 1장의 비리프 노드 1개 + 리프 노드 4개 선택
        test_nodes = self._select_test_nodes(
            chapters_data=chapters_data,
            chapter_indices=0,  # 1장만 선택
            leaf_count=4,       # 리프 노드 4개
            non_leaf_count=1    # 비리프 노드 1개
        )
        
        assert len(test_nodes) > 0, "선택된 테스트 노드가 없습니다"
        
        # 4단계: 🔥 실제 generate_extract_section 호출 (모든 선택된 노드에 대해)
        extraction_results = []
        expected_sections = ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']
        
        for i, test_node in enumerate(test_nodes):
            print(f"\n🚀 [{i+1}/{len(test_nodes)}] AI 추출 시작: {test_node.get('title')}")
            
            try:
                extraction_result = await stage.generate_extract_section(test_node)
                
                if extraction_result:
                    print(f"✅ AI 추출 성공: {len(extraction_result)} 섹션")
                    for section_key in extraction_result:
                        section_content = extraction_result[section_key][:100] + "..." if len(extraction_result[section_key]) > 100 else extraction_result[section_key]
                        print(f"   - {section_key}: {section_content}")
                    
                    # 결과 검증
                    valid_sections = [key for key in expected_sections if key in extraction_result and extraction_result[key].strip()]
                    
                    node_result = {
                        "test_node_info": {
                            "title": test_node.get('title'),
                            "level": test_node.get('level'),
                            "node_type": test_node.get('_test_info', {}).get('node_type'),
                            "chapter_index": test_node.get('_test_info', {}).get('chapter_index'),
                            "content_length": len(test_node.get('content_section', ''))
                        },
                        "extraction_result": extraction_result,  # 🔥 실제 AI 응답
                        "test_summary": {
                            "total_sections_expected": len(expected_sections),
                            "valid_sections_found": len(valid_sections),
                            "success": len(valid_sections) > 0
                        }
                    }
                    
                    extraction_results.append(node_result)
                    print(f"📊 검증 완료: {len(valid_sections)}/{len(expected_sections)} 섹션 유효")
                    
                else:
                    print("⚠️ AI 추출 결과가 비어있음")
                    
            except Exception as e:
                print(f"❌ AI 추출 중 오류: {e}")
                raise
        
        # 6단계: 최종 결과 검증
        assert len(extraction_results) > 0, "최소 1개 이상의 추출 결과가 있어야 함"
        successful_results = [r for r in extraction_results if r["test_summary"]["success"]]
        assert len(successful_results) > 0, "최소 1개 이상의 성공적인 추출 결과가 있어야 함"
        
        # 7단계: 실제 결과만 저장 (content_processing 디렉토리)
        final_result = {
            "extraction_results": extraction_results,
            "summary": {
                "total_nodes_processed": len(extraction_results),
                "successful_extractions": len(successful_results),
                "success_rate": len(successful_results) / len(extraction_results) if extraction_results else 0
            }
        }
        
        # 저장 위치: /refactoring/tests/data/content_processing/
        test_data_manager.save_test_result(
            test_method_name="generate_extract_section",
            result_data=final_result
        )
        
        print(f"💾 테스트 결과 저장 완료")
        print(f"🎉 generate_extract_section 테스트 성공!")
        
        return final_result

    @pytest.mark.asyncio
    async def test_save_extraction_result(self):
        """
        save_extraction_result 정상 동작 테스트 - 모든 추출 결과 저장
        
        테스트 시나리오:
        - generate_extract_section_result.json의 모든 extraction_results 사용
        - 각 결과별로 title로 매칭되는 문서 찾기
        - 모든 결과에 대해 save_extraction_result 실행
        - /tests/data/extracted_results/에 파일들 생성 확인
        """
        print("📁 save_extraction_result 테스트 시작 (모든 추출 결과 저장)")
        
        # 1단계: 테스트 데이터 로드 (모든 extraction_results)
        extraction_data_path = Path(__file__).parent.parent / "data" / "content_processing" / "generate_extract_section_result.json"
        assert extraction_data_path.exists(), f"추출 결과 데이터가 없습니다: {extraction_data_path}"
        
        with open(extraction_data_path, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        extraction_results = test_data.get("extraction_results", [])
        assert len(extraction_results) > 0, "추출 결과가 비어있습니다"
        
        print(f"📊 처리할 추출 결과 수: {len(extraction_results)}개")
        
        # 2단계: ContentProcessingStage 초기화 (한 번만)
        sorted_docs_path = Path(__file__).parent.parent / "data" / "content_processing" / "load_and_sort_documents_result.json"
        assert sorted_docs_path.exists(), f"정렬 결과 데이터가 없습니다: {sorted_docs_path}"
        
        # 3단계: ContentProcessingStage 초기화
        from src.utils.config_manager import ConfigManager
        from src.services.ai_service_v4 import AIService
        from src.utils.logger_v2 import Logger
        
        try:
            config_manager = ConfigManager()
            test_logger = Logger("test_save_extraction")
            ai_service = AIService(config_manager, test_logger, "content_processing")
            ai_config = config_manager.get_ai_config()
            stage = ContentProcessingStage(ai_config, ai_service)
            print("✅ ContentProcessingStage 초기화 완료")
        except Exception as e:
            print(f"❌ 초기화 실패: {e}")
            pytest.skip(f"ContentProcessingStage 초기화 실패: {e}")
        
        # 4단계: user_output_path 설정 (/tests/data/)
        user_output_path = Path(__file__).parent.parent / "data"
        
        # 5단계: 🔥 모든 추출 결과에 대해 save_extraction_result 실행
        saved_files = []
        successful_saves = 0
        
        for i, extraction_data in enumerate(extraction_results):
            try:
                print(f"\n🚀 [{i+1}/{len(extraction_results)}] 추출 결과 저장 시작")
                
                # 각 extraction_data에서 정보 추출
                test_node_info = extraction_data.get("test_node_info", {})
                extraction_result = extraction_data.get("extraction_result", {})
                target_title = test_node_info.get("title", "")
                
                if not target_title or not extraction_result:
                    print(f"⚠️ 유효하지 않은 데이터: {i+1}번째 결과 스킵")
                    continue
                
                # 해당 title로 문서 찾기
                matching_doc = self._find_document_by_title(sorted_docs_path, target_title)
                if not matching_doc:
                    print(f"⚠️ 매칭 문서 없음: {target_title}")
                    continue
                
                print(f"🎯 대상 문서: {target_title}")
                print(f"📊 추출 섹션 수: {len(extraction_result)}개")
                
                # save_extraction_result 실행
                saved_file_path = await stage.save_extraction_result(
                    doc=matching_doc,
                    extraction_result=extraction_result,
                    user_output_path=str(user_output_path)
                )
                
                if saved_file_path:
                    saved_files.append(saved_file_path)
                    successful_saves += 1
                    print(f"✅ 저장 성공: {Path(saved_file_path).name}")
                else:
                    print(f"❌ 저장 실패: 반환값 없음")
                    
            except Exception as e:
                print(f"❌ {i+1}번째 결과 저장 실패: {e}")
                continue
        
        # 6단계: 결과 검증
        assert successful_saves > 0, f"최소 1개 이상의 파일이 저장되어야 함 (성공: {successful_saves}/{len(extraction_results)})"
        print(f"\n📊 저장 완료: {successful_saves}/{len(extraction_results)}개 파일")
        
        # 저장된 파일들 검증
        validated_files = []
        for saved_file_path in saved_files:
            saved_file = Path(saved_file_path)
            
            # 파일 존재 확인
            assert saved_file.exists(), f"저장된 파일이 존재해야 함: {saved_file_path}"
            
            # 경로 구조 확인
            assert str(saved_file).startswith(str(user_output_path)), f"파일이 사용자 지정 경로 하위에 저장되어야 함: {user_output_path}"
            
            # 파일 내용 검증
            with open(saved_file, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            
            # 추출 섹션이 포함되어 있는지 확인
            content_valid = (
                "# 추출" in saved_content and 
                "## 핵심 내용" in saved_content and 
                "## 상세 핵심 내용" in saved_content
            )
            
            if content_valid:
                validated_files.append({
                    "path": str(saved_file_path),
                    "name": saved_file.name,
                    "size": saved_file.stat().st_size
                })
                print(f"✅ 검증 완료: {saved_file.name} ({saved_file.stat().st_size} bytes)")
            else:
                print(f"⚠️ 내용 검증 실패: {saved_file.name}")
        
        assert len(validated_files) > 0, "최소 1개 이상의 파일이 내용 검증을 통과해야 함"
        
        print(f"\n🎉 save_extraction_result 테스트 성공!")
        print(f"   - 처리된 추출 결과: {len(extraction_results)}개")
        print(f"   - 성공적으로 저장된 파일: {successful_saves}개") 
        print(f"   - 내용 검증 통과 파일: {len(validated_files)}개")
        
        return {
            "total_extractions": len(extraction_results),
            "successful_saves": successful_saves,
            "validated_files": validated_files,
            "success": True
        }
    
    def _find_document_by_title(self, sorted_docs_path, target_title):
        """정렬된 문서에서 title로 해당 문서 찾기"""
        with open(sorted_docs_path, 'r', encoding='utf-8') as f:
            sorted_data = json.load(f)
        
        # 모든 장의 leaf_nodes와 non_leaf_nodes에서 검색
        for chapter in sorted_data["output"]["chapters"]:
            # 리프 노드에서 검색
            for doc in chapter.get("leaf_nodes", []):
                if doc.get("title") == target_title:
                    return doc
            
            # 비리프 노드에서 검색
            for level_group in chapter.get("non_leaf_nodes", {}).values():
                for doc in level_group:
                    if doc.get("title") == target_title:
                        return doc
        
        return None
    
    def _select_test_nodes(self, chapters_data: List[Dict], 
                          chapter_indices: Union[int, List[int], str] = 0,
                          leaf_count: int = 0, 
                          non_leaf_count: int = 0) -> List[Dict]:
        """
        테스트용 노드들을 선택하는 헬퍼 메서드
        
        Args:
            chapters_data: 전체 장 데이터
            chapter_indices: 선택할 장 인덱스 (int: 특정 장, List[int]: 여러 장, "all": 모든 장)
            leaf_count: 각 장에서 선택할 리프 노드 개수
            non_leaf_count: 각 장에서 선택할 비리프 노드 개수
            
        Returns:
            선택된 테스트 노드들의 리스트
        """
        test_nodes = []
        
        # 장 인덱스 정규화
        if chapter_indices == "all":
            target_chapters = list(range(len(chapters_data)))
        elif isinstance(chapter_indices, int):
            target_chapters = [chapter_indices]
        else:
            target_chapters = chapter_indices
            
        for chapter_idx in target_chapters:
            if chapter_idx >= len(chapters_data):
                print(f"⚠️ 장 인덱스 {chapter_idx}는 범위를 벗어남 (총 {len(chapters_data)}개 장)")
                continue
                
            chapter = chapters_data[chapter_idx]
            chapter_name = f"chapter_{chapter_idx + 1}"
            
            # 비리프 노드 선택 (level별 딕셔너리 구조)
            non_leaf_nodes_dict = chapter.get("non_leaf_nodes", {})
            selected_non_leaf = 0
            
            for level_key in sorted(non_leaf_nodes_dict.keys()):
                if selected_non_leaf >= non_leaf_count:
                    break
                    
                level_nodes = non_leaf_nodes_dict[level_key]
                for i, node in enumerate(level_nodes):
                    if selected_non_leaf >= non_leaf_count:
                        break
                        
                    node_copy = node.copy()
                    node_copy['_test_info'] = {
                        'node_type': 'non_leaf',
                        'chapter_index': chapter_idx,
                        'selected_reason': f'non_leaf_node_{selected_non_leaf+1}_of_{chapter_name}_{level_key}'
                    }
                    test_nodes.append(node_copy)
                    print(f"🔶 [{chapter_name}] 비리프 노드 {selected_non_leaf+1} 선택 ({level_key}): {node_copy.get('title', 'Unknown')}")
                    selected_non_leaf += 1
            
            # 리프 노드 선택
            leaf_nodes = chapter.get("leaf_nodes", [])
            selected_leaf = min(leaf_count, len(leaf_nodes))
            for i in range(selected_leaf):
                node = leaf_nodes[i].copy()
                node['_test_info'] = {
                    'node_type': 'leaf',
                    'chapter_index': chapter_idx,
                    'selected_reason': f'leaf_node_{i+1}_of_{chapter_name}'
                }
                test_nodes.append(node)
                print(f"🔸 [{chapter_name}] 리프 노드 {i+1} 선택: {node.get('title', 'Unknown')}")
        
        print(f"🎯 총 선택된 테스트 노드 수: {len(test_nodes)}")
        return test_nodes