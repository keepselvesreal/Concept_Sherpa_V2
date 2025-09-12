# 생성 시간: Wed Sep 10 21:12:31 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage 결과를 실제 폴더/파일로 생성하는 시뮬레이터
# 상세 내용:
#   - IntegratedNodeGenerationSimulator (라인 22-150): 메인 시뮬레이터 클래스
#   - load_json_data (라인 32-50): JSON 결과 데이터 로드
#   - extract_chapter_info (라인 52-70): 파일명에서 장 정보 추출
#   - group_data_by_chapter (라인 72-95): 장별 데이터 그룹핑
#   - get_versioned_folder_name (라인 97-110): 버전 관리된 폴더명 생성
#   - create_files_for_chapter (라인 112-140): 장별 파일 생성
#   - run_simulation (라인 142-150): 메인 시뮬레이션 실행
# 상태: active

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple

class IntegratedNodeGenerationSimulator:
    """IntegratedNodeGenerationStage 결과를 실제 폴더/파일로 생성하는 시뮬레이터"""
    
    def __init__(self):
        self.base_path = Path("tests/simulations/Data_Oriented_Programming")
        self.data_path = Path("tests/data/integrated_node_generation")
        
    def load_json_data(self) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        3개의 JSON 결과 데이터 로드
        
        Returns:
            Tuple: (node_documents, content_documents, integrated_documents)
        """
        try:
            # 노드 문서 데이터 (새로운 구조 처리)
            with open(self.data_path / "generate_node_documents_result.json", 'r', encoding='utf-8') as f:
                node_data = json.load(f)
                node_documents = node_data["documents"] if "documents" in node_data else node_data
                node_selected_chapters = node_data.get("selected_chapters", []) if "documents" in node_data else []
                
            # 콘텐츠 문서 데이터 (새로운 구조 처리)
            with open(self.data_path / "generate_content_documents_result.json", 'r', encoding='utf-8') as f:
                content_data = json.load(f)
                content_documents = content_data["documents"] if "documents" in content_data else content_data
                
            # 통합 문서 데이터 (새로운 구조 처리)
            with open(self.data_path / "integrate_documents_result.json", 'r', encoding='utf-8') as f:
                integrated_data = json.load(f)
                integrated_documents = integrated_data["documents"] if "documents" in integrated_data else integrated_data
                
            # selected_chapters 정보 출력
            if node_selected_chapters:
                chapter_titles = [ch.get("chapter_title", "Unknown") for ch in node_selected_chapters]
                print(f"📋 선택된 장: {chapter_titles}")
                
            return node_documents, content_documents, integrated_documents
            
        except Exception as e:
            print(f"❌ JSON 데이터 로드 실패: {str(e)}")
            return [], [], []
    
    def extract_chapter_info(self, file_name: str) -> Tuple[str, str, str]:
        """
        파일명에서 장 정보 추출
        
        Args:
            file_name: "1_Complexity_of_object_oriented_programming/info_docs/filename.md"
            
        Returns:
            Tuple: (chapter_name, folder_type, filename)
        """
        try:
            parts = file_name.split('/')
            if len(parts) >= 3:
                chapter_name = parts[0]  # "1_Complexity_of_object_oriented_programming"
                folder_type = parts[1]   # "info_docs", "sections", "unified_info_docs"
                filename = parts[2]      # "15_lev1_1_Complexity_of_object_oriented_programming_info.md"
                return chapter_name, folder_type, filename
            else:
                print(f"⚠️ 파일명 형식 오류: {file_name}")
                return "", "", ""
        except Exception as e:
            print(f"❌ 파일명 파싱 실패: {file_name} - {str(e)}")
            return "", "", ""
    
    def filter_integrated_docs_by_chapter(self, integrated_docs: List[Dict]) -> List[Dict]:
        """
        통합 문서를 각 장별로 필터링 (각 장은 자신의 통합 문서만 포함)
        
        Args:
            integrated_docs: 모든 통합 문서
            
        Returns:
            List[Dict]: 각 장별로 필터링된 통합 문서
        """
        filtered_docs = []
        
        for doc in integrated_docs:
            file_name = doc['file_name']
            chapter_name, folder_type, filename = self.extract_chapter_info(file_name)
            
            # unified_info_docs만 처리
            if folder_type == 'unified_info_docs' and chapter_name and filename:
                # 파일명에서 노드 번호 추출 (예: 15_lev1_... → 15)
                try:
                    node_number = int(filename.split('_')[0])
                    
                    # 장별 노드 번호 범위 정의
                    if chapter_name == '1_Complexity_of_object_oriented_programming':
                        # 1장: 15~26번 노드만
                        if 15 <= node_number <= 26:
                            filtered_docs.append(doc)
                    elif chapter_name == '2_Separation_between_code_and_data':
                        # 2장: 27~33번 노드만
                        if 27 <= node_number <= 33:
                            filtered_docs.append(doc)
                except ValueError:
                    # 노드 번호를 파싱할 수 없는 경우 그대로 포함
                    filtered_docs.append(doc)
        
        print(f"🔍 통합 문서 필터링: {len(integrated_docs)}개 → {len(filtered_docs)}개")
        return filtered_docs
    
    def group_data_by_chapter(self, all_documents: List[Dict]) -> Dict[str, Dict[str, List[Dict]]]:
        """
        장별로 데이터 그룹핑
        
        Args:
            all_documents: 모든 문서 데이터
            
        Returns:
            Dict: {
                "1_Complexity_of_object_oriented_programming": {
                    "info_docs": [doc1, doc2, ...],
                    "sections": [doc1, doc2, ...],
                    "unified_info_docs": [doc1, doc2, ...]
                }
            }
        """
        chapter_data = {}
        
        for doc in all_documents:
            chapter_name, folder_type, filename = self.extract_chapter_info(doc['file_name'])
            
            if chapter_name and folder_type and filename:
                if chapter_name not in chapter_data:
                    chapter_data[chapter_name] = {}
                if folder_type not in chapter_data[chapter_name]:
                    chapter_data[chapter_name][folder_type] = []
                    
                chapter_data[chapter_name][folder_type].append({
                    'filename': filename,
                    'content': doc['content']
                })
        
        return chapter_data
    
    def get_versioned_folder_name(self, base_folder: Path, folder_name: str) -> str:
        """
        버전 관리된 폴더명 생성
        
        Args:
            base_folder: 기본 폴더 경로
            folder_name: 원본 폴더명 (info_docs, sections, unified_info_docs)
            
        Returns:
            str: 버전 관리된 폴더명
        """
        target_folder = base_folder / folder_name
        if not target_folder.exists():
            return folder_name
        else:
            return f"{folder_name}_v2"
    
    def create_files_for_chapter(self, chapter_name: str, chapter_data: Dict[str, List[Dict]]):
        """
        특정 장에 대한 파일 생성
        
        Args:
            chapter_name: 장 이름
            chapter_data: 해당 장의 문서 데이터
        """
        chapter_path = self.base_path / chapter_name
        
        if not chapter_path.exists():
            print(f"⚠️ 장 폴더가 존재하지 않음: {chapter_path}")
            return
        
        print(f"📖 {chapter_name} 처리 중...")
        
        for folder_type, documents in chapter_data.items():
            # 버전 관리된 폴더명 결정
            versioned_folder_name = self.get_versioned_folder_name(chapter_path, folder_type)
            target_folder = chapter_path / versioned_folder_name
            
            # 폴더 생성
            target_folder.mkdir(exist_ok=True)
            
            # 파일들 생성
            for doc in documents:
                file_path = target_folder / doc['filename']
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(doc['content'])
                except Exception as e:
                    print(f"❌ 파일 생성 실패: {file_path} - {str(e)}")
            
            print(f"   ✅ {versioned_folder_name}: {len(documents)}개 파일")
    
    def run_simulation(self):
        """메인 시뮬레이션 실행"""
        print("🚀 IntegratedNodeGeneration 시뮬레이션 시작")
        
        # 1. JSON 데이터 로드
        node_docs, content_docs, integrated_docs = self.load_json_data()
        
        if not node_docs and not content_docs and not integrated_docs:
            print("❌ 로드할 데이터가 없습니다")
            return
            
        print(f"📊 데이터 로드 완료: 노드({len(node_docs)}), 콘텐츠({len(content_docs)}), 통합({len(integrated_docs)})")
        
        # 2. 통합 문서를 장별로 필터링 
        filtered_integrated_docs = self.filter_integrated_docs_by_chapter(integrated_docs)
        
        # 3. 모든 문서 합치기 
        all_documents = node_docs + content_docs + filtered_integrated_docs
        
        # 4. 장별 데이터 그룹핑
        chapter_grouped_data = self.group_data_by_chapter(all_documents)
        
        print(f"📚 처리할 장: {list(chapter_grouped_data.keys())}")
        
        # 4. 각 장별 파일 생성
        for chapter_name, chapter_data in chapter_grouped_data.items():
            self.create_files_for_chapter(chapter_name, chapter_data)
        
        print("✅ 시뮬레이션 완료")

if __name__ == "__main__":
    simulator = IntegratedNodeGenerationSimulator()
    simulator.run_simulation()