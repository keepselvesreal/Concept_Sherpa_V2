# 생성 시간: Mon Sep  1 16:40:25 KST 2025
# 핵심 내용: 노드 정보 문서와 내용 문서 통합 전담 모듈 (메타정보 제외, 매칭 대상만 통합)
# 상세 내용:
#   - DocumentIntegrator (line 15-220): 문서 통합 전담 클래스
#   - normalize_title (line 25-35): 제목 정규화 (node_document_generator 동일 로직)
#   - find_content_file_by_title (line 37-65): title 기반 내용 문서 자동 탐지
#   - get_all_descendants_info (line 67-95): 재귀적 하위 노드 수집
#   - collect_descendant_ids (line 97-125): 재귀적 하위 노드 ID 수집 헬퍼
#   - integrate_single_document (line 127-190): 단일 노드 문서 통합 (메타정보 제외)
#   - integrate_documents_for_chapter (line 192-220): 장별 문서 통합
# 상태: active
# 주소: document_integrator
# 참조: document_integrator_v3.py에서 리팩토링하여 파이프라인용으로 개선

import os
import re
import json
import glob
from typing import Dict, List, Any, Optional, Set
from pathlib import Path

class DocumentIntegrator:
    """노드 정보 문서와 내용 문서 통합 전담 클래스"""
    
    def __init__(self):
        """DocumentIntegrator 초기화"""
        pass
    
    @staticmethod
    def normalize_title(title: str) -> str:
        """
        제목을 정규화합니다 (node_document_generator와 동일한 로직).
        
        Args:
            title: 원본 제목
            
        Returns:
            정규화된 제목
        """
        title_clean = re.sub(r'[^\w\s.-]', '', title)  # 점(.)도 유지
        title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
        return title_clean
    
    def find_content_file_by_title(self, node_title: str, content_dir: str) -> Optional[str]:
        """
        노드 title을 기반으로 내용 문서 파일을 자동으로 찾습니다.
        
        Args:
            node_title: 노드 제목
            content_dir: 내용 문서 디렉토리
            
        Returns:
            매칭된 파일 경로 (없으면 None)
        """
        # 디렉토리 내 모든 .md 파일 탐색
        md_files = glob.glob(os.path.join(content_dir, "*.md"))
        
        # 정규화된 title 생성
        normalized_title = self.normalize_title(node_title)
        
        for file_path in md_files:
            filename = os.path.basename(file_path)
            filename_without_ext = os.path.splitext(filename)[0]
            normalized_filename = self.normalize_title(filename_without_ext)
            
            # 정규화된 제목과 파일명 매칭
            if normalized_title == normalized_filename:
                return file_path
        
        return None
    
    def get_all_descendants_info(self, node: Dict[str, Any], all_nodes: List[Dict[str, Any]]) -> List[str]:
        """
        노드의 모든 하위 노드들의 정보 문서 파일명을 재귀적으로 수집합니다.
        
        Args:
            node: 대상 노드
            all_nodes: 전체 노드 리스트
            
        Returns:
            모든 하위 노드 문서 파일명 리스트 (ID 순서)
        """
        # 모든 하위 노드 ID를 재귀적으로 수집
        descendant_ids = self.collect_descendant_ids(node, all_nodes, set())
        
        # ID로 정렬
        descendant_ids = sorted(descendant_ids)
        
        # 각 노드 ID에 대응하는 파일명 생성
        descendant_files = []
        for node_id in descendant_ids:
            descendant_node = next((n for n in all_nodes if n.get('id') == node_id), None)
            if descendant_node:
                # 파일명 생성
                title_clean = self.normalize_title(descendant_node['title'])
                filename = f"{descendant_node['id']:02d}_lev{descendant_node['level']}_{title_clean}_info.md"
                descendant_files.append(filename)
        
        return descendant_files
    
    def collect_descendant_ids(self, node: Dict[str, Any], all_nodes: List[Dict[str, Any]], visited: Set[int]) -> Set[int]:
        """
        노드의 모든 하위 노드 ID를 재귀적으로 수집합니다.
        
        Args:
            node: 현재 노드
            all_nodes: 전체 노드 리스트
            visited: 이미 방문한 노드 ID 집합 (무한 루프 방지)
            
        Returns:
            하위 노드 ID 집합
        """
        descendant_ids = set()
        
        # 현재 노드가 이미 방문된 경우 무한 루프 방지
        if node.get('id') in visited:
            return descendant_ids
        
        visited.add(node.get('id'))
        
        # 직접 자식 노드들 처리
        for child_id in node.get('children_ids', []):
            child_node = next((n for n in all_nodes if n.get('id') == child_id), None)
            if child_node:
                # 자식 노드 ID 추가
                descendant_ids.add(child_id)
                # 자식 노드의 하위 노드들을 재귀적으로 수집
                grandchildren_ids = self.collect_descendant_ids(child_node, all_nodes, visited.copy())
                descendant_ids.update(grandchildren_ids)
        
        return descendant_ids
    
    def integrate_single_document(self, node: Dict[str, Any], all_nodes: List[Dict[str, Any]], 
                                content_dir: str, node_docs_dir: str) -> bool:
        """
        단일 노드 문서를 통합합니다 (메타정보 제외).
        
        Args:
            node: 대상 노드
            all_nodes: 전체 노드 리스트
            content_dir: 내용 문서 디렉토리
            node_docs_dir: 노드 문서 디렉토리
            
        Returns:
            통합 성공 여부
        """
        try:
            # 노드 문서 파일 경로 생성
            title_clean = self.normalize_title(node['title'])
            node_doc_filename = f"{node['id']:02d}_lev{node['level']}_{title_clean}_info.md"
            node_doc_path = os.path.join(node_docs_dir, node_doc_filename)
            
            # title 기반으로 내용 문서 자동 탐지
            content_file_path = self.find_content_file_by_title(node['title'], content_dir)
            
            # 기존 노드 문서 존재 확인
            if not os.path.exists(node_doc_path):
                print(f"   ❌ 노드 문서 없음: {node_doc_filename}")
                return False
            
            # 내용 문서 로드 (v2 로직: 콘텐츠가 없어도 통합 진행)
            content_text = ""
            if content_file_path:
                try:
                    with open(content_file_path, 'r', encoding='utf-8') as f:
                        content_text = f.read().strip()
                    print(f"   ✅ 매칭된 내용 문서: {os.path.basename(content_file_path)}")
                except Exception as e:
                    print(f"   ⚠️ 내용 문서 로드 실패: {e}")
                    content_text = ""  # 로드 실패시 빈 문자열로 계속 진행
            else:
                print(f"   ⚠️ 매칭되는 내용 문서 없음: {node['title']}")
                # v2 로직: 내용 문서가 없어도 통합 진행 (빈 내용으로)
            
            # 모든 하위 노드 정보 수집 (재귀적)
            descendants_files = self.get_all_descendants_info(node, all_nodes)
            descendants_text = "\n".join(descendants_files) if descendants_files else ""
            
            # 레벨에 따른 헤더 생성
            header_prefix = "#" * node['level']  
            content_header = f"{header_prefix} {node['title']}"
            
            # 새로운 문서 내용 생성 (메타정보 제외)
            new_content = f"""# 속성
---
process_status: false

# 추출
---

# 내용
---
{content_header}

{content_text}

# 구성
---
{descendants_text}
"""
            
            # 파일 저장
            with open(node_doc_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"   ✅ 통합 완료: {node_doc_filename}")
            return True
            
        except Exception as e:
            print(f"   ❌ 통합 실패 (ID: {node.get('id', '?')}): {e}")
            return False
    
    def integrate_documents_for_chapter(self, chapter_folder: str) -> Dict[str, Any]:
        """
        특정 장의 폴더 내에서 노드 정보 문서와 내용 문서를 통합합니다.
        
        일반적인 사용 방식:
        - chapter_folder 안에 노드 정보 문서 폴더(node_info_docs)가 있음
        - chapter_folder 안에 내용 문서들(.md)이 있음
        - TOC 파일을 자동으로 탐지하여 매칭 진행
        
        Args:
            chapter_folder: 장별 폴더 경로 (노드 문서 폴더와 내용 문서들 포함)
            
        Returns:
            통합 결과 딕셔너리
        """
        try:
            print(f"📄 문서 통합 시작: {os.path.basename(chapter_folder)}")
            
            # 필수 디렉토리 확인
            node_docs_dir = os.path.join(chapter_folder, "node_info_docs")
            if not os.path.exists(node_docs_dir):
                return {
                    'success': False,
                    'error': f'노드 문서 디렉토리가 없음: {node_docs_dir}',
                    'integrated_count': 0
                }
            
            # TOC 파일 자동 탐지 (*_toc.json 패턴)
            toc_files = glob.glob(os.path.join(chapter_folder, "*_toc.json"))
            if not toc_files:
                return {
                    'success': False,
                    'error': f'TOC 파일을 찾을 수 없음: {chapter_folder}',
                    'integrated_count': 0
                }
            
            # 첫 번째 TOC 파일 사용
            toc_file = toc_files[0]
            print(f"📊 TOC 파일 탐지: {os.path.basename(toc_file)}")
            
            # TOC 파일 로드
            with open(toc_file, 'r', encoding='utf-8') as f:
                nodes = json.load(f)
            
            # 내용 문서 디렉토리는 장별 폴더 자체
            content_dir = chapter_folder
            
            # 각 노드별 통합 실행
            success_count = 0
            total_nodes = len(nodes)
            
            for node in nodes:
                if self.integrate_single_document(node, nodes, content_dir, node_docs_dir):
                    success_count += 1
            
            print(f"   📊 통합 결과: {success_count}/{total_nodes}개 성공")
            
            return {
                'success': True,
                'integrated_count': success_count,
                'total_nodes': total_nodes,
                'chapter_folder': chapter_folder,
                'toc_file_used': toc_file
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'integrated_count': 0
            }