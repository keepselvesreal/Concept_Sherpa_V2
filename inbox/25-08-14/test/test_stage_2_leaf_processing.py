"""
테스트 2단계: 리프 노드 처리 테스트
dialectical_synthesis_processor_v6.py의 리프 노드 처리 파이프라인 검증
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/modules')

from pathlib import Path
from logging_system_v2 import TestLogger
from dialectical_synthesis_processor_v6 import DialecticalSynthesisProcessor
import json
import asyncio


async def test_leaf_node_processing():
    """2단계 테스트: 리프 노드 처리 파이프라인"""
    
    # 테스트 로거 초기화
    test_logger = TestLogger("stage_2_leaf_processing", Path("test/logs"))
    
    test_logger.log_process_start({
        "단계": "2단계",
        "목적": "리프 노드 처리 파이프라인 검증",
        "테스트 대상": "리프 노드 추출 및 처리 과정"
    })
    
    try:
        # 1. 프로세서 초기화
        test_logger.log_test_stage("프로세서_초기화", "DialecticalSynthesisProcessor", "시작")
        
        processor = DialecticalSynthesisProcessor(output_dir="test/logs")
        base_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14")
        nodes_file = base_dir / "test/test_nodes.json"
        
        test_logger.log_test_stage("프로세서_초기화", "DialecticalSynthesisProcessor", "성공")
        
        # 2. 테스트용 노드 데이터 로드
        test_logger.log_test_stage("노드_데이터_로딩", "test_nodes.json", "시작")
        
        with open(nodes_file, 'r', encoding='utf-8') as f:
            loaded_nodes = json.load(f)
        
        # 리프 노드만 필터링
        leaf_nodes = [node for node in loaded_nodes if len(node.get("children_ids", [])) == 0]
        
        test_logger.log_test_stage("노드_데이터_로딩", "test_nodes.json", "성공", {
            "전체_노드": len(loaded_nodes),
            "리프_노드": len(leaf_nodes),
            "리프_노드_IDs": [node["id"] for node in leaf_nodes]
        })
        
        # 3. 각 리프 노드별 개별 처리 테스트
        successful_nodes = 0
        failed_nodes = 0
        
        for leaf_node in leaf_nodes:
            node_id = leaf_node["id"]
            node_title = leaf_node["title"]
            
            test_logger.log_test_stage("리프노드_개별처리", f"노드{node_id}_{node_title}", "시작")
            
            try:
                # 3-1. 파일 경로 확인
                def get_node_file_path(node_data):
                    node_id = node_data["id"]
                    level = node_data["level"]
                    title = node_data["title"].lower().replace(" ", "_")
                    filename = f"{node_id:02d}_lev{level}_{title}_info.md"
                    return base_dir / "node_docs" / filename
                
                node_file = get_node_file_path(leaf_node)
                
                test_logger.log_file_state(
                    file_path=node_file,
                    section="파일_존재",
                    content_length=1 if node_file.exists() else 0,
                    status="존재함" if node_file.exists() else "없음"
                )
                
                if not node_file.exists():
                    test_logger.log_test_stage("리프노드_개별처리", f"노드{node_id}_{node_title}", "실패", 
                                             {"오류": "파일_없음", "경로": str(node_file)})
                    failed_nodes += 1
                    continue
                
                # 3-2. 데이터 로더 테스트 (추출 전용)
                extracted_content = processor.data_loader.load_for_extraction(leaf_node)
                
                test_logger.log_file_state(
                    file_path=node_file,
                    section="추출된_내용",
                    content_length=len(extracted_content),
                    status="추출됨" if extracted_content else "비어있음"
                )
                
                # 3-3. 콘텐츠 분석 및 처리 테스트
                if extracted_content:
                    # DataProcessor를 통한 처리 (실제 AI 처리는 하지 않고 모의 처리)
                    test_analysis_result = f"[모의 분석 결과] {node_title}의 핵심 내용 추출 완료"
                    
                    test_logger.log_file_state(
                        file_path=node_file,
                        section="분석_결과",
                        content_length=len(test_analysis_result),
                        status="분석_완료"
                    )
                
                # 3-4. 상태 업데이트 테스트
                # 실제로는 process_status를 true로 변경하지만, 테스트에서는 확인만
                with open(node_file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                current_status = "false" if "process_status: false" in file_content else "unknown"
                
                test_logger.log_status_change(
                    node=f"노드{node_id}",
                    before=current_status,
                    after="true(모의)",
                    file_path=str(node_file)
                )
                
                test_logger.log_test_stage("리프노드_개별처리", f"노드{node_id}_{node_title}", "성공", {
                    "추출된_내용_길이": len(extracted_content),
                    "처리_결과": "완료",
                    "상태_변경": f"{current_status} → true(모의)"
                })
                
                successful_nodes += 1
                
            except Exception as node_error:
                test_logger.log_error(f"리프노드처리_{node_id}", node_error, {
                    "노드_ID": node_id,
                    "노드_제목": node_title
                })
                failed_nodes += 1
        
        # 4. 레벨별 완료 상태 검증
        test_logger.log_test_stage("레벨별_완료_검증", "레벨1", "시작")
        
        # 모든 리프 노드가 레벨 1이므로 레벨 1 완료 상태 확인
        completion_stats = {
            "total": len(leaf_nodes),
            "completed": successful_nodes,
            "failed": failed_nodes,
            "leaf_nodes": len(leaf_nodes),
            "parent_nodes": 0
        }
        
        all_level_completed = successful_nodes == len(leaf_nodes)
        
        test_logger.log_level_status(
            level=1,
            stats=completion_stats,
            all_completed=all_level_completed
        )
        
        test_logger.log_test_stage("레벨별_완료_검증", "레벨1", "성공" if all_level_completed else "부분완료", 
                                 completion_stats)
        
        # 5. 전체 2단계 결과 검증
        test_logger.log_assertion(
            test_name="리프노드_처리_성공률",
            expected="100%",
            actual=f"{(successful_nodes/len(leaf_nodes)*100):.1f}%",
            passed=successful_nodes == len(leaf_nodes),
            message="모든 리프 노드가 성공적으로 처리되어야 함"
        )
        
        test_logger.log_assertion(
            test_name="처리된_노드_수",
            expected=len(leaf_nodes),
            actual=successful_nodes + failed_nodes,
            passed=(successful_nodes + failed_nodes) == len(leaf_nodes),
            message="모든 리프 노드가 처리 시도되어야 함"
        )
        
        test_logger.log_assertion(
            test_name="레벨1_완료_상태",
            expected=True,
            actual=all_level_completed,
            passed=all_level_completed,
            message="레벨 1의 모든 노드가 완료되어야 함"
        )
        
        overall_success = (successful_nodes == len(leaf_nodes)) and all_level_completed
        
    except Exception as e:
        test_logger.log_error("2단계_테스트_실패", e, {
            "단계": "리프 노드 처리",
            "오류_위치": "테스트 실행 중"
        })
        overall_success = False
    
    # 테스트 완료 요약
    test_logger.log_test_summary(
        test_category="리프노드_처리",
        success=successful_nodes,
        failed=failed_nodes,
        duration=0.1  # 모의 시간
    )
    
    test_logger.log_process_end(overall_success, {
        "완료된_테스트": "2단계 리프 노드 처리",
        "성공한_노드": successful_nodes,
        "실패한_노드": failed_nodes,
        "전체_성공": overall_success
    })
    
    # 테스트 보고서 생성
    report_path = test_logger.create_test_report()
    print(f"\n📊 2단계 테스트 보고서: {report_path}")
    
    return overall_success


if __name__ == "__main__":
    success = asyncio.run(test_leaf_node_processing())
    exit(0 if success else 1)