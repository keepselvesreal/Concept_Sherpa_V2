"""
생성 시간: 2025-08-14 14:55:00 KST
핵심 내용: 테스트 데이터 백업 및 초기화 스크립트
상세 내용:
    - backup_original_data() (라인 25-): 원본 node_docs 폴더 백업
    - reset_process_status() (라인 45-): 모든 노드의 process_status를 false로 초기화
    - restore_original_data() (라인 70-): 테스트 후 원본 데이터 복원
    - create_test_nodes_subset() (라인 90-): 테스트용 작은 노드 집합 생성
상태: 활성
주소: test_data_backup
참조: -
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Any


class TestDataManager:
    """테스트 데이터 관리 클래스"""
    
    def __init__(self, base_dir: str = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14"):
        self.base_dir = Path(base_dir)
        self.node_docs_dir = self.base_dir / "node_docs"
        self.backup_dir = self.base_dir / "test" / "backup"
        self.test_dir = self.base_dir / "test"
        
        # 백업 디렉토리 생성
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def backup_original_data(self) -> bool:
        """원본 node_docs 폴더 백업"""
        try:
            backup_path = self.backup_dir / "node_docs_original"
            
            # 기존 백업 제거
            if backup_path.exists():
                shutil.rmtree(backup_path)
            
            # 원본 백업
            shutil.copytree(self.node_docs_dir, backup_path)
            
            print(f"✅ 원본 데이터 백업 완료: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ 백업 실패: {e}")
            return False
    
    def reset_process_status(self) -> Dict[str, bool]:
        """모든 노드의 process_status를 false로 초기화"""
        results = {}
        
        try:
            for file_path in self.node_docs_dir.glob("*_info.md"):
                # 파일 읽기
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # process_status 찾기/업데이트
                if "process_status:" in content:
                    # 기존 값 업데이트
                    updated_content = self._update_process_status(content, "false")
                else:
                    # process_status 추가
                    updated_content = self._add_process_status(content, "false")
                
                # 파일 저장
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                results[file_path.name] = True
                print(f"🔄 {file_path.name}: process_status = false")
            
            print(f"✅ 총 {len(results)}개 파일의 process_status 초기화 완료")
            return results
            
        except Exception as e:
            print(f"❌ process_status 초기화 실패: {e}")
            return {}
    
    def restore_original_data(self) -> bool:
        """테스트 후 원본 데이터 복원"""
        try:
            backup_path = self.backup_dir / "node_docs_original"
            
            if not backup_path.exists():
                print("❌ 백업 데이터가 없습니다.")
                return False
            
            # 현재 데이터 제거
            if self.node_docs_dir.exists():
                shutil.rmtree(self.node_docs_dir)
            
            # 백업에서 복원
            shutil.copytree(backup_path, self.node_docs_dir)
            
            print(f"✅ 원본 데이터 복원 완료: {self.node_docs_dir}")
            return True
            
        except Exception as e:
            print(f"❌ 복원 실패: {e}")
            return False
    
    def create_test_nodes_subset(self, node_count: int = 3) -> str:
        """테스트용 작은 노드 집합 생성"""
        try:
            # 원본 nodes.json 읽기
            nodes_file = self.base_dir / "nodes.json"
            with open(nodes_file, 'r', encoding='utf-8') as f:
                all_nodes = json.load(f)
            
            # 테스트용 부분집합 생성 (레벨 1 노드들 중 일부만)
            test_nodes = []
            
            # 루트 노드 (레벨 0) 추가
            root_node = next(node for node in all_nodes if node["level"] == 0)
            
            # 리프 노드들 중 처음 몇 개만 선택
            leaf_nodes = [node for node in all_nodes if node["level"] == 1][:node_count]
            
            # 루트 노드의 children_ids 업데이트
            root_node_copy = root_node.copy()
            root_node_copy["children_ids"] = [node["id"] for node in leaf_nodes]
            
            test_nodes.append(root_node_copy)
            test_nodes.extend(leaf_nodes)
            
            # 테스트용 nodes.json 저장
            test_nodes_file = self.test_dir / "test_nodes.json"
            with open(test_nodes_file, 'w', encoding='utf-8') as f:
                json.dump(test_nodes, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 테스트용 노드 집합 생성 완료: {len(test_nodes)}개 노드")
            print(f"   - 루트 노드: 1개 (레벨 0)")
            print(f"   - 리프 노드: {len(leaf_nodes)}개 (레벨 1)")
            print(f"   - 파일: {test_nodes_file}")
            
            return str(test_nodes_file)
            
        except Exception as e:
            print(f"❌ 테스트 노드 집합 생성 실패: {e}")
            return ""
    
    def _update_process_status(self, content: str, status: str) -> str:
        """기존 process_status 값 업데이트"""
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.strip().startswith("process_status:"):
                updated_lines.append(f"process_status: {status}")
            else:
                updated_lines.append(line)
        
        return '\n'.join(updated_lines)
    
    def _add_process_status(self, content: str, status: str) -> str:
        """process_status 필드 추가"""
        lines = content.split('\n')
        updated_lines = []
        
        attr_section_found = False
        attr_section_ended = False
        
        for line in lines:
            if line.strip() == "# 속성":
                attr_section_found = True
                updated_lines.append(line)
            elif attr_section_found and not attr_section_ended:
                if line.startswith("# ") and line.strip() != "# 속성":
                    # 다음 섹션 시작
                    updated_lines.append(f"process_status: {status}")
                    updated_lines.append("")
                    updated_lines.append(line)
                    attr_section_ended = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # 속성 섹션이 마지막이면 끝에 추가
        if attr_section_found and not attr_section_ended:
            updated_lines.append(f"process_status: {status}")
        
        return '\n'.join(updated_lines)
    
    def check_file_structure(self) -> Dict[str, Any]:
        """파일 구조 검사"""
        results = {
            "total_files": 0,
            "valid_files": 0,
            "files_with_content": 0,
            "files_with_extraction": 0,
            "files_with_status": 0,
            "details": []
        }
        
        try:
            for file_path in self.node_docs_dir.glob("*_info.md"):
                results["total_files"] += 1
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_info = {
                    "name": file_path.name,
                    "has_attributes": "# 속성" in content,
                    "has_extraction": "# 추출" in content,
                    "has_content": "# 내용" in content,
                    "has_status": "process_status:" in content,
                    "content_length": 0,
                    "extraction_length": 0
                }
                
                # 내용 섹션 길이 확인
                if file_info["has_content"]:
                    content_start = content.find("# 내용")
                    if content_start != -1:
                        next_section = content.find("\n# ", content_start + 4)
                        if next_section == -1:
                            content_section = content[content_start:]
                        else:
                            content_section = content[content_start:next_section]
                        file_info["content_length"] = len(content_section.strip())
                        if file_info["content_length"] > 50:  # 최소 내용이 있는 경우
                            results["files_with_content"] += 1
                
                # 추출 섹션 길이 확인
                if file_info["has_extraction"]:
                    extraction_start = content.find("# 추출")
                    if extraction_start != -1:
                        next_section = content.find("\n# ", extraction_start + 4)
                        if next_section == -1:
                            extraction_section = content[extraction_start:]
                        else:
                            extraction_section = content[extraction_start:next_section]
                        file_info["extraction_length"] = len(extraction_section.strip())
                        if file_info["extraction_length"] > 20:  # 최소 추출 내용이 있는 경우
                            results["files_with_extraction"] += 1
                
                if file_info["has_attributes"] and file_info["has_extraction"] and file_info["has_content"]:
                    results["valid_files"] += 1
                
                if file_info["has_status"]:
                    results["files_with_status"] += 1
                
                results["details"].append(file_info)
            
            return results
            
        except Exception as e:
            print(f"❌ 파일 구조 검사 실패: {e}")
            return results


def main():
    """테스트 데이터 관리 실행"""
    manager = TestDataManager()
    
    print("=" * 50)
    print("테스트 데이터 관리 시스템")
    print("=" * 50)
    
    # 1. 파일 구조 검사
    print("\n1. 파일 구조 검사")
    structure_info = manager.check_file_structure()
    print(f"   총 파일: {structure_info['total_files']}개")
    print(f"   유효 파일: {structure_info['valid_files']}개")
    print(f"   내용 있는 파일: {structure_info['files_with_content']}개")
    print(f"   추출 있는 파일: {structure_info['files_with_extraction']}개")
    print(f"   상태 필드 있는 파일: {structure_info['files_with_status']}개")
    
    # 2. 원본 데이터 백업
    print("\n2. 원본 데이터 백업")
    manager.backup_original_data()
    
    # 3. process_status 초기화
    print("\n3. process_status 초기화")
    manager.reset_process_status()
    
    # 4. 테스트용 노드 집합 생성
    print("\n4. 테스트용 노드 집합 생성")
    test_nodes_file = manager.create_test_nodes_subset(3)
    
    print("\n🎯 테스트 준비 완료!")
    print(f"   - 백업 위치: {manager.backup_dir}")
    print(f"   - 테스트 노드: {test_nodes_file}")


if __name__ == "__main__":
    main()