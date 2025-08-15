# 생성 시간: Thu Aug 14 10:52:34 KST 2025
# 핵심 내용: 현재 노드 정보를 기반으로 info 파일에 데이터를 추가하는 스크립트 (새로운 파일명 형식 반영)
# 상세 내용:
#   - NodeDataUpdater (line 18): 메인 노드 데이터 업데이터 클래스
#   - load_nodes() (line 25): JSON 파일에서 노드 정보 로드
#   - find_info_files() (line 35): node_docs 디렉토리에서 *_info.md 파일 검색  
#   - find_corresponding_section_file() (line 45): info 파일에 대응하는 섹션 파일 검색
#   - extract_node_info_from_filename() (line 65): 파일명에서 노드 정보 추출
#   - generate_section_filename() (line 85): 노드 정보를 기반으로 섹션 파일명 생성
#   - update_info_file_content() (line 95): info 파일의 내용 섹션 업데이트
#   - process_all_info_files() (line 155): 모든 info 파일 처리
#   - main() (line 185): CLI 인터페이스 및 실행 로직
# 상태: 활성
# 주소: node_data_updater
# 참조: node_info_updater (25-08-13)

import json
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


class NodeDataUpdater:
    """현재 노드 정보를 기반으로 info 파일에 데이터를 추가하는 클래스"""
    
    def __init__(self, nodes_file: str, info_dir: str, sections_dir: str):
        """
        초기화
        
        Args:
            nodes_file: 노드 정보 JSON 파일 경로
            info_dir: info 파일들이 있는 디렉토리 경로
            sections_dir: 추출된 섹션 파일들이 있는 디렉토리 경로
        """
        self.nodes = self.load_nodes(nodes_file)
        self.info_dir = info_dir
        self.sections_dir = sections_dir
    
    def load_nodes(self, nodes_file: str) -> List[Dict[str, Any]]:
        """JSON 파일에서 노드 정보 로드"""
        try:
            with open(nodes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 노드 파일 로드 오류: {e}")
            return []
    
    def find_info_files(self) -> List[str]:
        """info 디렉토리에서 *_info.md 파일들 찾기"""
        info_files = []
        if os.path.exists(self.info_dir):
            for file in os.listdir(self.info_dir):
                if file.endswith('_info.md'):
                    info_files.append(os.path.join(self.info_dir, file))
        return sorted(info_files)
    
    def find_corresponding_section_file(self, node_id: int, node_level: int, node_title: str) -> Optional[str]:
        """
        노드 정보에 대응하는 섹션 파일 찾기
        
        Args:
            node_id: 노드 ID
            node_level: 노드 레벨  
            node_title: 노드 제목
            
        Returns:
            대응하는 섹션 파일 경로, 없으면 None
        """
        if not os.path.exists(self.sections_dir):
            return None
        
        # 새로운 파일명 형식: lev{level}_{id:02d}_{title}.md
        section_filename = self.generate_section_filename(node_id, node_level, node_title)
        section_path = os.path.join(self.sections_dir, section_filename)
        
        if os.path.exists(section_path):
            return section_path
        return None
    
    def extract_node_info_from_filename(self, filename: str) -> Optional[Tuple[int, str]]:
        """
        info 파일명에서 노드 정보 추출 (새로운 형식: lev{level}_{id:02d}_{title}_info.md)
        
        Args:
            filename: info 파일명 (예: lev1_01_introduction_and_overview_info.md)
            
        Returns:
            (node_id, title) 튜플, 추출 실패시 None
        """
        if not filename.endswith('_info.md'):
            return None
        
        # _info.md 제거
        base_name = filename[:-8]
        
        # 새로운 형식: {id:02d}_lev{level}_{title}
        # 예: 01_lev1_introduction_and_overview
        parts = base_name.split('_', 2)  # id, lev{level}, title로 분리
        
        if len(parts) < 3:
            return None
        
        try:
            node_id = int(parts[0])
            # parts[1]은 lev{level} 형식이어야 함
            if not parts[1].startswith('lev'):
                return None
            level = int(parts[1][3:])  # 'lev' 제거 후 숫자 추출
            title = parts[2].replace('_', ' ')
            return node_id, title
        except ValueError:
            return None
    
    def generate_section_filename(self, node_id: int, node_level: int, node_title: str) -> str:
        """
        노드 정보를 기반으로 섹션 파일명 생성
        
        Args:
            node_id: 노드 ID
            node_level: 노드 레벨
            node_title: 노드 제목
            
        Returns:
            섹션 파일명 (예: 01_lev1_introduction_and_overview.md)
        """
        # 제목을 파일명에 적합하게 변환
        safe_title = re.sub(r'[^\w\s-]', '', node_title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        safe_title = safe_title.strip('_').lower()
        
        return f"{node_id:02d}_lev{node_level}_{safe_title}.md"
    
    def update_info_file_content(self, info_file: str) -> bool:
        """
        info 파일의 내용 섹션 업데이트
        
        Args:
            info_file: info 파일 경로
            
        Returns:
            업데이트 성공 여부
        """
        try:
            # info 파일 읽기
            with open(info_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 파일명에서 노드 정보 추출
            filename = os.path.basename(info_file)
            node_info = self.extract_node_info_from_filename(filename)
            
            if not node_info:
                print(f"⚠️  파일명에서 노드 정보 추출 실패: {filename}")
                return False
            
            node_id, title = node_info
            
            # 노드 정보 찾기
            target_node = None
            for node in self.nodes:
                if node['id'] == node_id:
                    target_node = node
                    break
            
            if not target_node:
                print(f"⚠️  노드 ID {node_id}를 찾을 수 없음: {filename}")
                return False
            
            # 대응하는 섹션 파일 찾기
            section_file = self.find_corresponding_section_file(
                target_node['id'], 
                target_node['level'], 
                target_node['title']
            )
            
            # 내용 섹션 찾기 및 업데이트
            lines = content.split('\n')
            content_section_start = -1
            
            for i, line in enumerate(lines):
                if line.strip() == '# 내용':
                    content_section_start = i
                    break
            
            if content_section_start == -1:
                print(f"⚠️  '# 내용' 섹션을 찾을 수 없음: {filename}")
                return False
            
            # 내용 섹션 업데이트
            if section_file and os.path.exists(section_file):
                # 섹션 파일이 있는 경우
                with open(section_file, 'r', encoding='utf-8') as f:
                    section_content = f.read().strip()
                
                # 내용 섹션 바로 다음에 섹션 내용 삽입
                new_lines = lines[:content_section_start + 1] + [section_content]
                print(f"✅ 섹션 파일 삽입: {os.path.basename(section_file)} → {filename}")
            else:
                # 섹션 파일이 없는 경우, 노드 정보로 헤더 생성
                header_level = target_node['level'] + 1  # level 0 = #, level 1 = ##
                header = '#' * header_level + ' ' + target_node['title']
                new_lines = lines[:content_section_start + 1] + [header]
                print(f"✅ 노드 헤더 삽입: {header} → {filename}")
            
            # 다른 섹션이 있으면 유지
            other_sections_start = -1
            for i in range(content_section_start + 1, len(lines)):
                if lines[i].strip().startswith('# ') and lines[i].strip() != '# 내용':
                    other_sections_start = i
                    break
            
            if other_sections_start != -1:
                new_lines.extend([''] + lines[other_sections_start:])
            
            # 파일 저장
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            return True
            
        except Exception as e:
            print(f"❌ {os.path.basename(info_file)} 처리 오류: {e}")
            return False
    
    def process_all_info_files(self) -> None:
        """모든 info 파일 처리"""
        info_files = self.find_info_files()
        
        if not info_files:
            print("📋 처리할 *_info.md 파일이 없습니다.")
            return
        
        print(f"🔍 발견된 info 파일: {len(info_files)}개")
        for info_file in info_files:
            print(f"   - {os.path.basename(info_file)}")
        
        print(f"\n🚀 info 파일 내용 업데이트 시작...")
        
        success_count = 0
        for info_file in info_files:
            if self.update_info_file_content(info_file):
                success_count += 1
        
        print(f"\n✅ 처리 완료: {success_count}/{len(info_files)}개 성공")

    @staticmethod
    def main():
        """CLI 인터페이스"""
        if len(sys.argv) < 4:
            print("사용법: python node_data_updater.py <노드파일> <info디렉토리> <섹션디렉토리>")
            print("예시: python node_data_updater.py nodes.json node_docs extracted_sections_lev")
            print()
            print("기능: 노드 정보 문서(*_info.md)의 내용 섹션에 추출된 섹션 데이터를 추가")
            print("새로운 파일명 형식: lev{level}_{id:02d}_{title}.md")
            return
        
        nodes_file = sys.argv[1]
        info_dir = sys.argv[2]
        sections_dir = sys.argv[3]
        
        print("📄 노드 데이터 업데이터 (새 파일명 형식)")
        print("=" * 60)
        print(f"📋 노드 파일: {nodes_file}")
        print(f"📁 Info 디렉토리: {info_dir}")
        print(f"📁 섹션 디렉토리: {sections_dir}")
        
        # 파일/디렉토리 존재 확인
        if not os.path.exists(nodes_file):
            print(f"❌ 노드 파일을 찾을 수 없습니다: {nodes_file}")
            return
        
        if not os.path.isdir(info_dir):
            print(f"❌ Info 디렉토리를 찾을 수 없습니다: {info_dir}")
            return
        
        if not os.path.isdir(sections_dir):
            print(f"⚠️  섹션 디렉토리를 찾을 수 없습니다: {sections_dir}")
            print("섹션 파일 없이 노드 헤더만 삽입됩니다.")
        
        # 업데이터 초기화 및 실행
        updater = NodeDataUpdater(nodes_file, info_dir, sections_dir)
        
        if not updater.nodes:
            print("❌ 노드 데이터를 로드할 수 없습니다.")
            return
        
        print(f"📊 로드된 노드: {len(updater.nodes)}개")
        print("\n" + "=" * 60)
        
        # 모든 info 파일 처리
        updater.process_all_info_files()
        
        print(f"\n✨ 작업 완료!")


if __name__ == "__main__":
    NodeDataUpdater.main()