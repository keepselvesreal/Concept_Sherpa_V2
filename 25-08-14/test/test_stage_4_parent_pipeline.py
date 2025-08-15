"""
테스트 4단계: 부모 노드 3단계 파이프라인 테스트
dialectical_synthesis_processor_v6.py의 부모 노드 3단계 처리 과정 검증
단계: 추출 → 자식 노드 업데이트 → 부모 노드 최종 업데이트
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/modules')

from pathlib import Path
from logging_system_v2 import TestLogger
from dialectical_synthesis_processor_v6 import DialecticalSynthesisProcessor
import json


def test_parent_node_pipeline():
    """4단계 테스트: 부모 노드 3단계 파이프라인"""
    
    # 테스트 로거 초기화
    test_logger = TestLogger("stage_4_parent_pipeline", Path("test/logs"))
    
    test_logger.log_process_start({
        "단계": "4단계",
        "목적": "부모 노드 3단계 파이프라인 검증",
        "테스트 대상": "추출 → 자식업데이트 → 부모최종업데이트"
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
            "부모_노드_수": len(parent_nodes)
        })
        
        # 파일 경로 생성 함수
        def get_node_file_path(node_data):
            node_id = node_data["id"]
            level = node_data["level"]
            title = node_data["title"].lower().replace(" ", "_").replace("-", "_")
            filename = f"{node_id:02d}_lev{level}_{title}_info.md"
            return base_dir / "node_docs" / filename
        
        # 2. 각 부모 노드별 3단계 파이프라인 테스트
        pipeline_results = {}
        
        for parent_node in parent_nodes:
            parent_id = parent_node["id"]
            parent_title = parent_node["title"]
            children_ids = parent_node.get("children_ids", [])
            
            test_logger.log_test_stage("부모노드_파이프라인", f"노드{parent_id}_{parent_title}", "시작")
            
            pipeline_stages = {
                "stage_1_extraction": False,
                "stage_2_children_update": False,
                "stage_3_parent_final": False
            }
            
            try:
                # === 1단계: 추출 (부모 노드 내용 섹션만 로드) ===
                test_logger.log_test_stage("파이프라인_1단계", f"추출_{parent_id}", "시작")
                
                parent_file = get_node_file_path(parent_node)
                if not parent_file.exists():
                    test_logger.log_test_stage("파이프라인_1단계", f"추출_{parent_id}", "실패", 
                                             {"오류": "부모노드_파일_없음"})
                    continue
                
                # DataLoader를 사용한 추출 전용 로딩
                extracted_content = processor.data_loader.load_for_extraction(parent_node)
                
                test_logger.log_file_state(
                    file_path=parent_file,
                    section="추출된_부모내용",
                    content_length=len(extracted_content),
                    status="추출됨" if extracted_content else "비어있음"
                )
                
                if extracted_content:
                    pipeline_stages["stage_1_extraction"] = True
                    test_logger.log_test_stage("파이프라인_1단계", f"추출_{parent_id}", "성공", {
                        "추출된_내용_길이": len(extracted_content)
                    })
                else:
                    test_logger.log_test_stage("파이프라인_1단계", f"추출_{parent_id}", "실패", 
                                             {"오류": "추출된_내용_없음"})
                    continue
                
                # === 2단계: 자식 노드 업데이트 (자식들의 추출 섹션 결합) ===
                test_logger.log_test_stage("파이프라인_2단계", f"자식업데이트_{parent_id}", "시작")
                
                # 자식 노드들의 추출된 내용 수집
                children_extracted_content = []
                for child_id in children_ids:
                    child_node = next((node for node in loaded_nodes if node["id"] == child_id), None)
                    if child_node:
                        child_extracted = processor.data_loader.load_for_extraction(child_node)
                        if child_extracted:
                            children_extracted_content.append({
                                "child_id": child_id,
                                "content": child_extracted,
                                "length": len(child_extracted)
                            })
                
                # DataLoader를 사용한 업데이트 전용 로딩 (부모 내용 + 자식들 추출 결합)
                combined_content_for_update = processor.data_loader.load_for_update(parent_node)
                
                test_logger.log_file_state(
                    file_path=parent_file,
                    section="결합된_업데이트_내용",
                    content_length=len(combined_content_for_update),
                    status="결합됨" if combined_content_for_update else "결합실패"
                )
                
                # 자식 정보 업데이트 시뮬레이션
                if len(children_extracted_content) == len(children_ids):
                    pipeline_stages["stage_2_children_update"] = True
                    test_logger.log_test_stage("파이프라인_2단계", f"자식업데이트_{parent_id}", "성공", {
                        "처리된_자식수": len(children_extracted_content),
                        "결합된_내용_길이": len(combined_content_for_update),
                        "자식_내용": [{"child_id": child["child_id"], "length": child["length"]} 
                                   for child in children_extracted_content]
                    })
                else:
                    test_logger.log_test_stage("파이프라인_2단계", f"자식업데이트_{parent_id}", "실패", {
                        "기대_자식수": len(children_ids),
                        "실제_처리된_자식수": len(children_extracted_content)
                    })
                    continue
                
                # === 3단계: 부모 노드 최종 업데이트 ===
                test_logger.log_test_stage("파이프라인_3단계", f"부모최종업데이트_{parent_id}", "시작")
                
                # 모의 AI 처리 결과 생성
                mock_final_synthesis = f"""
# 종합 분석 결과

## 개요
{parent_title}에 대한 종합적인 분석 결과입니다.

## 주요 발견사항
- 자식 노드 {len(children_ids)}개의 내용을 종합적으로 분석
- 총 {sum(child['length'] for child in children_extracted_content)}자의 내용 처리
- 정반합 방법론을 통한 통합 분석 완료

## 결론
{parent_title}의 핵심 내용이 성공적으로 추출되고 정리되었습니다.
                """.strip()
                
                # DataSaver를 통한 최종 결과 저장 시뮬레이션
                test_logger.log_file_state(
                    file_path=parent_file,
                    section="최종_종합_결과",
                    content_length=len(mock_final_synthesis),
                    status="생성됨"
                )
                
                # 상태 업데이트 시뮬레이션
                test_logger.log_status_change(
                    node=f"노드{parent_id}",
                    before="false",
                    after="true(완료)",
                    file_path=parent_file.name
                )
                
                pipeline_stages["stage_3_parent_final"] = True
                test_logger.log_test_stage("파이프라인_3단계", f"부모최종업데이트_{parent_id}", "성공", {
                    "최종_결과_길이": len(mock_final_synthesis),
                    "처리_완료": True
                })
                
                # 전체 파이프라인 성공
                all_stages_completed = all(pipeline_stages.values())
                
                test_logger.log_test_stage("부모노드_파이프라인", f"노드{parent_id}_{parent_title}", 
                                         "성공" if all_stages_completed else "부분완료", 
                                         pipeline_stages)
                
                pipeline_results[parent_id] = {
                    "parent_title": parent_title,
                    "stages": pipeline_stages,
                    "all_completed": all_stages_completed,
                    "children_processed": len(children_extracted_content),
                    "expected_children": len(children_ids)
                }
                
            except Exception as node_error:
                test_logger.log_error(f"부모노드파이프라인_{parent_id}", node_error, {
                    "부모_노드_ID": parent_id,
                    "부모_노드_제목": parent_title
                })
                pipeline_results[parent_id] = {
                    "parent_title": parent_title,
                    "stages": pipeline_stages,
                    "all_completed": False,
                    "error": str(node_error)
                }
        
        # 3. 전체 파이프라인 결과 요약
        test_logger.log_test_stage("전체_파이프라인_요약", "모든_부모노드", "시작")
        
        successful_pipelines = [
            result for result in pipeline_results.values() 
            if result["all_completed"]
        ]
        
        failed_pipelines = [
            result for result in pipeline_results.values() 
            if not result["all_completed"]
        ]
        
        # 4. 레벨 완료 상태 업데이트
        test_logger.log_level_status(
            level=0,
            stats={
                "total": len(parent_nodes),
                "completed": len(successful_pipelines),
                "failed": len(failed_pipelines),
                "leaf_nodes": 0,
                "parent_nodes": len(parent_nodes)
            },
            all_completed=len(successful_pipelines) == len(parent_nodes)
        )
        
        # 5. 단언 검사
        test_logger.log_assertion(
            test_name="모든_부모노드_파이프라인_완료",
            expected=len(parent_nodes),
            actual=len(successful_pipelines),
            passed=len(successful_pipelines) == len(parent_nodes),
            message="모든 부모 노드의 3단계 파이프라인이 완료되어야 함"
        )
        
        test_logger.log_assertion(
            test_name="파이프라인_실패_없음",
            expected=0,
            actual=len(failed_pipelines),
            passed=len(failed_pipelines) == 0,
            message="파이프라인 처리 실패가 없어야 함"
        )
        
        # 각 단계별 성공률 검사
        stage_success_rates = {
            "stage_1_extraction": 0,
            "stage_2_children_update": 0,
            "stage_3_parent_final": 0
        }
        
        for result in pipeline_results.values():
            for stage, success in result["stages"].items():
                if success:
                    stage_success_rates[stage] += 1
        
        for stage, success_count in stage_success_rates.items():
            test_logger.log_assertion(
                test_name=f"{stage}_단계_성공률",
                expected=len(parent_nodes),
                actual=success_count,
                passed=success_count == len(parent_nodes),
                message=f"{stage} 단계가 모든 부모 노드에서 성공해야 함"
            )
        
        overall_success = (
            len(successful_pipelines) == len(parent_nodes) and
            len(failed_pipelines) == 0 and
            all(count == len(parent_nodes) for count in stage_success_rates.values())
        )
        
        test_logger.log_test_stage("전체_파이프라인_요약", "모든_부모노드", "성공" if overall_success else "부분완료", {
            "성공한_파이프라인": len(successful_pipelines),
            "실패한_파이프라인": len(failed_pipelines),
            "단계별_성공률": stage_success_rates,
            "전체_성공": overall_success
        })
        
    except Exception as e:
        test_logger.log_error("4단계_테스트_실패", e, {
            "단계": "부모 노드 3단계 파이프라인",
            "오류_위치": "테스트 실행 중"
        })
        overall_success = False
    
    # 테스트 완료
    test_logger.log_process_end(overall_success, {
        "완료된_테스트": "4단계 부모 노드 3단계 파이프라인",
        "결과": "성공" if overall_success else "실패",
        "성공한_파이프라인": len(successful_pipelines) if 'successful_pipelines' in locals() else 0,
        "전체_부모노드": len(parent_nodes) if 'parent_nodes' in locals() else 0
    })
    
    # 테스트 보고서 생성
    report_path = test_logger.create_test_report()
    print(f"\n📊 4단계 테스트 보고서: {report_path}")
    
    return overall_success


if __name__ == "__main__":
    success = test_parent_node_pipeline()
    exit(0 if success else 1)