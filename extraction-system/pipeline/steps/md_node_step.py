# 생성 시간: 2025-08-27 17:36 KST
# 핵심 내용: MD 파일 노드 생성 단계
# 상세 내용:
#   - MDNodeGenerationStep (라인 15-100): MD 파일에서 노드 정보 생성
#   - execute() (라인 20-75): node_generator.py 로직을 파이프라인에 통합
#   - _extract_headers_by_type() (라인 77-95): 메타데이터 조건에 따른 헤더 추출
#   - _extract_all_headers() (라인 97-125): 모든 헤더 추출
#   - _extract_first_header_only() (라인 127-150): 첫 번째 헤더만 추출
# 상태: active
# 주소: pipeline/steps/md_node_step
# 참조: node_generator.py → 파이프라인 단계로 변환

import json
import re
from pathlib import Path
from typing import Dict, Any, List
from pipeline.steps.base import PipelineStep
from pipeline.models import StepResult


class MDNodeGenerationStep(PipelineStep):
    """MD 파일 노드 생성 단계 (3/7)"""
    
    def __init__(self):
        super().__init__("노드 생성")
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """MD 파일에서 헤더를 추출하여 nodes.json 생성"""
        self._log_step_start()
        
        try:
            # 이전 단계에서 전달된 정보
            folder_path = context.get("folder_path")
            md_content = context.get("md_content")
            
            if not all([folder_path, md_content]):
                return StepResult(success=False, error="필요한 정보가 없습니다 (folder_path, md_content)")
            
            # metadata.json 로드
            metadata_file = Path(folder_path) / "metadata.json"
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # 헤더 추출
            nodes = self._extract_headers_by_type(md_content, metadata)
            
            if not nodes:
                print("⚠️ 추출된 헤더가 없습니다.")
            
            # nodes.json 저장
            nodes_file = Path(folder_path) / "nodes.json"
            with open(nodes_file, 'w', encoding='utf-8') as f:
                json.dump(nodes, f, ensure_ascii=False, indent=2)
            
            print(f"📊 노드 추출 완료: {len(nodes)}개 헤더")
            print(f"💾 노드 파일 저장: {nodes_file}")
            
            self._log_step_success()
            
            return StepResult(
                success=True,
                data={
                    "nodes_file": str(nodes_file),
                    "nodes_count": len(nodes),
                    "nodes": nodes
                }
            )
            
        except Exception as e:
            error_msg = f"노드 생성 중 오류: {str(e)}"
            self._log_step_error(error_msg)
            return StepResult(success=False, error=error_msg)
    
    def _extract_headers_by_type(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """메타데이터 조건에 따른 헤더 추출"""
        structure_type = metadata.get("structure_type", "")
        content_processing = metadata.get("content_processing", "")
        
        print(f"📋 구조 타입: {structure_type}")
        print(f"📋 콘텐츠 처리: {content_processing}")
        
        # standalone + unified 조건 확인
        if structure_type == "standalone" and content_processing == "unified":
            print("🎯 조건 만족: standalone + unified -> 첫 번째 헤더만 추출")
            return self._extract_first_header_only(content)
        else:
            print("🎯 기본 조건: 모든 헤더 추출")
            return self._extract_all_headers(content)
    
    def _extract_all_headers(self, content: str) -> List[Dict[str, Any]]:
        """모든 헤더 추출"""
        nodes = []
        node_id = 0
        
        lines = content.split('\n')
        
        for line in lines:
            if line.strip().startswith('#'):
                # 헤더 레벨과 텍스트 추출
                match = re.match(r'^(#+)\s*(.+)', line.strip())
                if match:
                    header_level = len(match.group(1))  # # 개수
                    header_text = match.group(2).strip()
                    cleaned_title = self._clean_title(header_text)
                    
                    node = {
                        "id": node_id,
                        "level": header_level - 1,  # 헤더 레벨 - 1
                        "title": cleaned_title
                    }
                    nodes.append(node)
                    node_id += 1
        
        return nodes
    
    def _extract_first_header_only(self, content: str) -> List[Dict[str, Any]]:
        """첫 번째 헤더만 추출 (standalone + unified 조건)"""
        lines = content.split('\n')
        
        for line in lines:
            if line.strip().startswith('#'):
                # 헤더 레벨과 텍스트 추출
                match = re.match(r'^(#+)\s*(.+)', line.strip())
                if match:
                    header_level = len(match.group(1))  # # 개수
                    header_text = match.group(2).strip()
                    cleaned_title = self._clean_title(header_text)
                    
                    node = {
                        "id": 0,
                        "level": header_level - 1,  # 헤더 레벨 - 1
                        "title": cleaned_title
                    }
                    return [node]  # 첫 번째 헤더만 반환
        
        return []  # 헤더가 없는 경우
    
    def _clean_title(self, title: str) -> str:
        """헤더 텍스트 정제"""
        # 맨 앞의 숫자와 점/공백 제거 (예: "1. Title" -> "Title")
        cleaned = re.sub(r'^\d+\.?\s*', '', title)
        cleaned = cleaned.strip()
        return cleaned