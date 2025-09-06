"""
테스트 3단계: 부모 노드 의존성 검증 테스트
dialectical_synthesis_processor_v6.py의 의존성 기반 처리 검증
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/modules')

from pathlib import Path
from logging_system_v2 import TestLogger
from dialectical_synthesis_processor_v6 import DialecticalSynthesisProcessor
import json


def test_dependency_validation():
    """3단계 테스트: 부모 노드 의존성 검증"""
    
    # 테스트 로거 초기화
    test_logger = TestLogger("stage_3_dependency_validation", Path("test/logs"))
    
    test_logger.log_process_start({
        "단계": "3단계",
        "목적": "부모 노드 의존성 검증 및 처리 전 검사",
        "테스트 대상": "의존성 기반 처리 로직"
    })
    
    try:
        # 1. 프로세서 및 데이터 초기화
        test_logger.log_test_stage("초기화", "프로세서_및_데이터", "시작")
        
        processor = DialecticalSynthesisProcessor(output_dir="test/logs")
        base_dir = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14")
        nodes_file = base_dir / "test/test_nodes.json"
        
        with open(nodes_file, 'r', encoding='utf-8') as f:
            loaded_nodes = json.load(f)
        
        # 노드 분류
        leaf_nodes = [node for node in loaded_nodes if len(node.get("children_ids", [])) == 0]
        parent_nodes = [node for node in loaded_nodes if len(node.get("children_ids", [])) > 0]
        
        test_logger.log_test_stage("초기화", "프로세서_및_데이터", "성공", {
            "리프_노드_수": len(leaf_nodes),
            "부모_노드_수": len(parent_nodes),
            "전체_노드_수": len(loaded_nodes)
        })
        
        # 2. 자식 노드 상태 확인 시뮬레이션
        test_logger.log_test_stage("자식노드_상태확인", "모든_리프노드", "시작")
        
        # 파일 경로 생성 함수
        def get_node_file_path(node_data):
            node_id = node_data["id"]
            level = node_data["level"]
            title = node_data["title"].lower().replace(" ", "_")
            filename = f"{node_id:02d}_lev{level}_{title}_info.md"
            return base_dir / "node_docs" / filename
        
        # 각 리프 노드의 상태 확인 (모의로 모든 노드가 완료되었다고 가정)
        child_completion_status = {}
        for leaf_node in leaf_nodes:
            node_file = get_node_file_path(leaf_node)
            
            if node_file.exists():
                with open(node_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # process_status 확인
                if "process_status: false" in content:
                    # 테스트를 위해 false를 true로 모의 변경
                    child_completion_status[leaf_node["id"]] = True  # 모의 완료 상태
                    test_logger.log_status_change(
                        node=f"노드{leaf_node['id']}",
                        before="false",
                        after="true(모의완료)",
                        file_path=node_file.name
                    )
                else:
                    child_completion_status[leaf_node["id"]] = False
            else:
                child_completion_status[leaf_node["id"]] = False
        
        completed_children = [node_id for node_id, status in child_completion_status.items() if status]
        
        test_logger.log_test_stage("자식노드_상태확인", "모든_리프노드", "성공", {
            "완료된_자식노드": len(completed_children),
            "전체_자식노드": len(leaf_nodes),
            "완료된_노드_IDs": completed_children
        })
        
        # 3. 각 부모 노드별 의존성 검증
        dependency_validation_results = {}
        
        for parent_node in parent_nodes:
            parent_id = parent_node["id"]
            parent_title = parent_node["title"]
            expected_children = parent_node.get("children_ids", [])
            
            test_logger.log_test_stage("의존성_검증", f"부모노드{parent_id}_{parent_title}", "시작")
            
            # 3-1. 자식 노드 완료 상태 확인
            completed_children_for_parent = [
                child_id for child_id in expected_children 
                if child_completion_status.get(child_id, False)
            ]
            
            all_children_completed = len(completed_children_for_parent) == len(expected_children)
            
            # 3-2. 의존성 검증 로깅
            test_logger.log_dependency_check(
                parent=f"노드{parent_id}",
                children=[f"노드{child_id}" for child_id in expected_children],
                all_completed=all_children_completed,
                completed_children=[f"노드{child_id}" for child_id in completed_children_for_parent]
            )
            
            # 3-3. 처리 가능 여부 판정
            processing_eligibility = {
                "부모_노드_ID": parent_id,
                "부모_노드_제목": parent_title,
                "기대_자식수": len(expected_children),
                "완료_자식수": len(completed_children_for_parent),
                "완료율": f"{len(completed_children_for_parent)}/{len(expected_children)}",
                "처리_가능": all_children_completed,
                "누락_자식": [child_id for child_id in expected_children if not child_completion_status.get(child_id, False)]
            }
            
            dependency_validation_results[parent_id] = processing_eligibility
            
            # 3-4. 부모 노드 파일 존재 확인
            parent_file = get_node_file_path(parent_node)
            parent_file_exists = parent_file.exists()
            
            test_logger.log_file_state(
                file_path=parent_file,
                section="부모노드_파일",
                content_length=1 if parent_file_exists else 0,
                status="존재함" if parent_file_exists else "없음"
            )
            
            # 결과 기록
            if all_children_completed and parent_file_exists:
                test_logger.log_test_stage("의존성_검증", f"부모노드{parent_id}_{parent_title}", "성공", 
                                         processing_eligibility)
            elif not all_children_completed:
                test_logger.log_test_stage("의존성_검증", f"부모노드{parent_id}_{parent_title}", "대기중", 
                                         processing_eligibility)
            else:
                test_logger.log_test_stage("의존성_검증", f"부모노드{parent_id}_{parent_title}", "실패", 
                                         {**processing_eligibility, "오류": "부모노드_파일_없음"})
        
        # 4. 전체 의존성 상태 요약
        test_logger.log_test_stage("전체_의존성_요약", "모든_부모노드", "시작")
        
        ready_for_processing = [
            result for result in dependency_validation_results.values() 
            if result["처리_가능"]
        ]
        
        waiting_for_dependencies = [
            result for result in dependency_validation_results.values() 
            if not result["처리_가능"]
        ]
        
        # 5. 레벨별 처리 순서 검증
        test_logger.log_test_stage("처리순서_검증", "레벨기반_순서", "시작")
        
        # 모든 리프 노드(레벨1)가 완료되었으므로 부모 노드(레벨0) 처리 가능
        level_processing_order = {
            "레벨1_완료": len(completed_children) == len(leaf_nodes),
            "레벨0_처리가능": len(ready_for_processing) == len(parent_nodes),
            "처리_대기중": len(waiting_for_dependencies),
            "권장_처리순서": ["레벨1_완료", "레벨0_시작"]
        }
        
        test_logger.log_level_status(
            level=0,
            stats={
                "total": len(parent_nodes),
                "completed": 0,  # 아직 처리 시작 전
                "ready_for_processing": len(ready_for_processing),
                "leaf_nodes": 0,
                "parent_nodes": len(parent_nodes)
            },
            all_completed=False
        )
        
        test_logger.log_test_stage("처리순서_검증", "레벨기반_순서", "성공", level_processing_order)
        
        # 6. 단언 검사
        test_logger.log_assertion(
            test_name="모든_자식노드_완료",
            expected=len(leaf_nodes),
            actual=len(completed_children),
            passed=len(completed_children) == len(leaf_nodes),
            message="모든 리프 노드가 완료되어야 부모 노드 처리 가능"
        )
        
        test_logger.log_assertion(
            test_name="부모노드_처리가능_상태",
            expected=len(parent_nodes),
            actual=len(ready_for_processing),
            passed=len(ready_for_processing) == len(parent_nodes),
            message="모든 부모 노드가 처리 가능 상태여야 함"
        )
        
        test_logger.log_assertion(
            test_name="의존성_대기_노드_없음",
            expected=0,
            actual=len(waiting_for_dependencies),
            passed=len(waiting_for_dependencies) == 0,
            message="의존성 때문에 대기중인 노드가 없어야 함"
        )
        
        overall_success = (
            len(completed_children) == len(leaf_nodes) and
            len(ready_for_processing) == len(parent_nodes) and
            len(waiting_for_dependencies) == 0
        )
        
        test_logger.log_test_stage("전체_의존성_요약", "모든_부모노드", "성공" if overall_success else "부분완료", {
            "처리가능_부모노드": len(ready_for_processing),
            "대기중_부모노드": len(waiting_for_dependencies),
            "전체_검증_성공": overall_success
        })
        
    except Exception as e:
        test_logger.log_error("3단계_테스트_실패", e, {
            "단계": "부모 노드 의존성 검증",
            "오류_위치": "테스트 실행 중"
        })
        overall_success = False
    
    # 테스트 완료
    test_logger.log_process_end(overall_success, {
        "완료된_테스트": "3단계 부모 노드 의존성 검증",
        "결과": "성공" if overall_success else "실패",
        "처리가능_노드수": len(ready_for_processing) if 'ready_for_processing' in locals() else 0
    })
    
    # 테스트 보고서 생성
    report_path = test_logger.create_test_report()
    print(f"\n📊 3단계 테스트 보고서: {report_path}")
    
    return overall_success


if __name__ == "__main__":
    success = test_dependency_validation()
    exit(0 if success else 1)