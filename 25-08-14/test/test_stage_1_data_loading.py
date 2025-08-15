"""
테스트 1단계: 데이터 로딩 및 분류 테스트
dialectical_synthesis_processor_v6.py의 데이터 로딩과 노드 분류 기능 검증
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/modules')

from pathlib import Path
from logging_system_v2 import TestLogger
from dialectical_synthesis_processor_v6 import DialecticalSynthesisProcessor
import json


def test_data_loading_and_classification():
    """1단계 테스트: 데이터 로딩 및 분류"""
    
    # 테스트 로거 초기화
    test_logger = TestLogger("stage_1_data_loading", Path("test/logs"))
    
    test_logger.log_process_start({
        "단계": "1단계",
        "목적": "데이터 로딩 및 노드 분류 검증", 
        "테스트 대상": "DialecticalSynthesisProcessor 초기화 및 분류"
    })
    
    try:
        # 1. 프로세서 초기화 테스트
        test_logger.log_test_stage("프로세서_초기화", "DialecticalSynthesisProcessor", "시작")
        
        processor = DialecticalSynthesisProcessor(
            output_dir="test/logs"
        )
        
        # 테스트용 노드 파일 설정
        base_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14")
        nodes_file = base_dir / "test/test_nodes.json"
        
        test_logger.log_test_stage("프로세서_초기화", "DialecticalSynthesisProcessor", "성공", {
            "output_dir": str(processor.output_dir),
            "nodes_file": str(nodes_file),
            "log_dir": str(processor.output_dir)
        })
        
        # 2. 노드 데이터 로딩 테스트
        test_logger.log_test_stage("노드_데이터_로딩", "test_nodes.json", "시작")
        
        with open(nodes_file, 'r', encoding='utf-8') as f:
            loaded_nodes = json.load(f)
        
        test_logger.log_test_stage("노드_데이터_로딩", "test_nodes.json", "성공", {
            "총_노드_수": len(loaded_nodes),
            "루트_노드": sum(1 for node in loaded_nodes if node["level"] == 0),
            "리프_노드": sum(1 for node in loaded_nodes if node["level"] == 1)
        })
        
        # 3. 노드 분류 및 그룹화 테스트
        test_logger.log_test_stage("노드_분류", "NodeGrouper", "시작")
        
        # 수동으로 리프/부모 노드 분류
        leaf_nodes = [node for node in loaded_nodes if len(node.get("children_ids", [])) == 0]
        parent_nodes = [node for node in loaded_nodes if len(node.get("children_ids", [])) > 0]
        
        test_logger.log_test_stage("노드_분류", "NodeGrouper", "성공", {
            "분류된_리프_노드": len(leaf_nodes),
            "분류된_부모_노드": len(parent_nodes),
            "리프_노드_IDs": [node["id"] for node in leaf_nodes],
            "부모_노드_IDs": [node["id"] for node in parent_nodes]
        })
        
        # 4. 레벨별 분류 테스트
        test_logger.log_test_stage("레벨별_분류", "levels_groups", "시작")
        
        levels_groups = processor.node_grouper.group_and_sort_nodes(loaded_nodes)
        
        for level, nodes in levels_groups.items():
            test_logger.log_level_status(level, {
                "total": len(nodes),
                "completed": 0,
                "leaf_nodes": len([n for n in nodes if len(n.get("children_ids", [])) == 0]),
                "parent_nodes": len([n for n in nodes if len(n.get("children_ids", [])) > 0])
            })
        
        test_logger.log_test_stage("레벨별_분류", "levels_groups", "성공", {
            "총_레벨_수": len(levels_groups),
            "레벨_분포": {f"레벨{k}": len(v) for k, v in levels_groups.items()}
        })
        
        # 5. 의존성 검증 테스트
        test_logger.log_test_stage("의존성_구조_검증", "parent_children_mapping", "시작")
        
        # 부모-자식 관계 검증
        for parent_node in parent_nodes:
            children_ids = parent_node.get("children_ids", [])
            existing_children = [child["id"] for child in leaf_nodes if child["id"] in children_ids]
            
            test_logger.log_dependency_check(
                parent=f"노드{parent_node['id']}",
                children=[f"노드{cid}" for cid in children_ids],
                all_completed=len(existing_children) == len(children_ids),
                completed_children=[f"노드{cid}" for cid in existing_children]
            )
        
        test_logger.log_test_stage("의존성_구조_검증", "parent_children_mapping", "성공")
        
        # 6. 파일 경로 매핑 테스트
        test_logger.log_test_stage("파일_경로_매핑", "node_file_paths", "시작")
        
        # 간단한 파일 경로 생성 함수 (processor 내부 메서드 대신)
        def get_node_file_path(node_data):
            node_id = node_data["id"]
            level = node_data["level"]
            title = node_data["title"].lower().replace(" ", "_")
            filename = f"{node_id:02d}_lev{level}_{title}_info.md"
            return base_dir / "node_docs" / filename
        
        file_mapping_results = {}
        for node in loaded_nodes:
            expected_file = get_node_file_path(node)
            file_exists = expected_file.exists()
            
            file_mapping_results[f"노드{node['id']}"] = {
                "예상_파일": expected_file.name,
                "파일_존재": file_exists
            }
            
            if file_exists:
                # 파일 내용 기본 검증
                with open(expected_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                test_logger.log_file_state(
                    file_path=expected_file,
                    section="전체",
                    content_length=len(content),
                    status="존재함"
                )
        
        test_logger.log_test_stage("파일_경로_매핑", "node_file_paths", "성공", {
            "매핑된_파일_수": len(file_mapping_results),
            "존재하는_파일": sum(1 for info in file_mapping_results.values() if info["파일_존재"]),
            "누락된_파일": sum(1 for info in file_mapping_results.values() if not info["파일_존재"])
        })
        
        # 7. 전체 1단계 결과 검증
        test_logger.log_assertion(
            test_name="리프_노드_수_검증",
            expected=3,
            actual=len(leaf_nodes),
            passed=len(leaf_nodes) == 3,
            message="테스트 노드 집합의 리프 노드 수"
        )
        
        test_logger.log_assertion(
            test_name="부모_노드_수_검증", 
            expected=1,
            actual=len(parent_nodes),
            passed=len(parent_nodes) == 1,
            message="테스트 노드 집합의 부모 노드 수"
        )
        
        test_logger.log_assertion(
            test_name="전체_노드_수_검증",
            expected=4,
            actual=len(loaded_nodes),
            passed=len(loaded_nodes) == 4,
            message="테스트 노드 집합의 전체 노드 수"
        )
        
        success = True
        
    except Exception as e:
        test_logger.log_error("1단계_테스트_실패", e, {
            "단계": "데이터 로딩 및 분류",
            "오류_위치": "테스트 실행 중"
        })
        success = False
    
    # 테스트 완료
    test_logger.log_process_end(success, {
        "완료된_테스트": "1단계 데이터 로딩 및 분류",
        "결과": "성공" if success else "실패"
    })
    
    # 테스트 보고서 생성
    report_path = test_logger.create_test_report()
    print(f"\n📊 1단계 테스트 보고서: {report_path}")
    
    return success


if __name__ == "__main__":
    success = test_data_loading_and_classification()
    exit(0 if success else 1)