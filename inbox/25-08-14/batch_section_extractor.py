# 생성 시간: Thu Aug 14 10:31:41 KST 2025
# 핵심 내용: content node 정보를 기반으로 모든 섹션을 개별 파일로 추출하는 배치 처리 스크립트
# 상세 내용:
#   - BatchSectionExtractor (line 18): 메인 배치 섹션 추출 클래스
#   - load_nodes() (line 25): JSON 파일에서 노드 정보 로드  
#   - find_node_by_id() (line 35): ID로 특정 노드 찾기
#   - find_next_node() (line 45): 같은 레벨의 다음 노드 찾기
#   - extract_section() (line 70): 지정된 노드의 섹션 텍스트 추출
#   - get_section_header() (line 119): 노드 레벨에 맞는 마크다운 헤더 생성
#   - sanitize_filename() (line 127): 파일명으로 사용할 수 있도록 문자열 정리
#   - extract_all_sections() (line 135): 모든 content 노드의 섹션을 개별 파일로 추출
#   - main() (line 167): CLI 인터페이스 및 실행 로직
# 상태: 활성
# 주소: batch_section_extractor
# 참조: section_extractor

import json
import re
from typing import List, Dict, Optional, Tuple
import argparse
import sys
from pathlib import Path
import os


class BatchSectionExtractor:
    """마크다운 파일에서 모든 content node를 개별 파일로 추출하는 클래스"""
    
    def __init__(self, nodes_file: str, markdown_file: str):
        """
        초기화
        
        Args:
            nodes_file: 노드 정보가 담긴 JSON 파일 경로
            markdown_file: 추출할 마크다운 파일 경로
        """
        self.nodes = self.load_nodes(nodes_file)
        self.markdown_file = markdown_file
        
        with open(markdown_file, 'r', encoding='utf-8') as f:
            self.content = f.read()
    
    def load_nodes(self, nodes_file: str) -> List[Dict]:
        """JSON 파일에서 노드 정보 로드"""
        try:
            with open(nodes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"노드 파일을 찾을 수 없습니다: {nodes_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 에러: {e}")
    
    def find_node_by_id(self, node_id: int) -> Optional[Dict]:
        """ID로 특정 노드 찾기"""
        for node in self.nodes:
            if node['id'] == node_id:
                return node
        return None
    
    def find_next_node(self, current_node: Dict) -> Optional[Dict]:
        """
        현재 노드와 같은 레벨의 다음 노드 찾기
        
        Args:
            current_node: 현재 노드
            
        Returns:
            같은 레벨의 다음 노드, 없으면 None
        """
        current_level = current_node['level']
        current_id = current_node['id']
        
        # 같은 레벨의 노드들 중에서 ID가 더 큰 것 중 가장 작은 것 찾기
        next_candidates = []
        for node in self.nodes:
            if (node['level'] == current_level and 
                node['id'] > current_id):
                next_candidates.append(node)
        
        if next_candidates:
            # ID가 가장 작은 것 반환
            return min(next_candidates, key=lambda x: x['id'])
        
        # 같은 레벨의 다음 노드가 없으면 상위 레벨의 다음 노드 찾기
        for level in range(current_level - 1, -1, -1):
            for node in self.nodes:
                if (node['level'] == level and 
                    node['id'] > current_id):
                    next_candidates.append(node)
            if next_candidates:
                return min(next_candidates, key=lambda x: x['id'])
        
        return None
    
    def extract_section(self, node_id: int) -> Tuple[str, Dict]:
        """
        지정된 노드의 섹션 추출
        
        Args:
            node_id: 추출할 노드의 ID
            
        Returns:
            (추출된 섹션 텍스트, 노드 정보)
        """
        current_node = self.find_node_by_id(node_id)
        if not current_node:
            raise ValueError(f"노드 ID {node_id}를 찾을 수 없습니다")
        
        # 현재 노드의 섹션 헤더 생성
        current_header = self.get_section_header(current_node)
        
        # 다음 노드 찾기
        next_node = self.find_next_node(current_node)
        
        # 현재 노드의 섹션 시작 위치 찾기
        current_pattern = re.escape(current_header)
        current_match = re.search(current_pattern, self.content)
        
        if not current_match:
            raise ValueError(f"섹션 헤더를 찾을 수 없습니다: {current_header}")
        
        start_pos = current_match.start()
        
        # 다음 노드가 있으면 그 위치까지, 없으면 파일 끝까지
        if next_node:
            next_header = self.get_section_header(next_node)
            next_pattern = re.escape(next_header)
            next_match = re.search(next_pattern, self.content[start_pos + len(current_header):])
            
            if next_match:
                end_pos = start_pos + len(current_header) + next_match.start()
                section_text = self.content[start_pos:end_pos].rstrip()
            else:
                # 다음 헤더를 찾을 수 없으면 파일 끝까지
                section_text = self.content[start_pos:].rstrip()
        else:
            # 다음 노드가 없으면 파일 끝까지
            section_text = self.content[start_pos:].rstrip()
        
        return section_text, current_node
    
    def get_section_header(self, node: Dict) -> str:
        """
        노드 레벨에 맞는 마크다운 헤더 생성
        
        Args:
            node: 노드 정보
            
        Returns:
            마크다운 헤더 문자열 (예: "## Introduction and Overview")
        """
        level = node['level'] + 1  # level 0 = #, level 1 = ##, ...
        return '#' * level + ' ' + node['title']
    
    def sanitize_filename(self, title: str) -> str:
        """파일명으로 사용할 수 있도록 문자열 정리"""
        # 특수문자 제거 및 공백을 언더스코어로 변환
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        return safe_title.strip('_').lower()
    
    def extract_all_sections(self, output_dir: str = "extracted_sections") -> Dict[str, str]:
        """
        모든 content 노드의 섹션을 개별 파일로 추출
        
        Args:
            output_dir: 출력 디렉토리 경로
            
        Returns:
            {node_id: output_file_path} 딕셔너리
        """
        # 출력 디렉토리 생성
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        extracted_files = {}
        content_nodes = [node for node in self.nodes if node.get('has_content', False)]
        
        print(f"총 {len(content_nodes)}개의 content 노드를 추출합니다...")
        
        for i, node in enumerate(content_nodes, 1):
            try:
                # 섹션 추출
                section_text, node_info = self.extract_section(node['id'])
                
                # 파일명 생성
                safe_title = self.sanitize_filename(node['title'])
                filename = f"{node['id']:02d}_lev{node['level']}_{safe_title}.md"
                file_path = output_path / filename
                
                # 파일 저장
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(section_text)
                
                extracted_files[str(node['id'])] = str(file_path)
                print(f"[{i}/{len(content_nodes)}] 추출 완료: {filename}")
                
            except Exception as e:
                print(f"[{i}/{len(content_nodes)}] 추출 실패 (노드 ID: {node['id']}): {e}")
        
        return extracted_files
    
    @staticmethod
    def main():
        """CLI 인터페이스"""
        parser = argparse.ArgumentParser(description='모든 content 노드의 섹션을 개별 파일로 추출')
        parser.add_argument('--nodes-file', default='nodes.json', 
                          help='노드 정보 JSON 파일 (기본값: nodes.json)')
        parser.add_argument('--markdown-file', 
                          default='GPT5_Agentic_Coding_Claude_Code.md',
                          help='마크다운 파일 (기본값: GPT5_Agentic_Coding_Claude_Code.md)')
        parser.add_argument('--output-dir', '-o', default='extracted_sections',
                          help='출력 디렉토리 (기본값: extracted_sections)')
        parser.add_argument('--single', type=int, metavar='NODE_ID',
                          help='단일 노드만 추출 (노드 ID 지정)')
        
        args = parser.parse_args()
        
        try:
            # 섹션 추출기 초기화
            extractor = BatchSectionExtractor(args.nodes_file, args.markdown_file)
            
            if args.single is not None:
                # 단일 노드 추출
                section_text, node_info = extractor.extract_section(args.single)
                
                safe_title = extractor.sanitize_filename(node_info['title'])
                filename = f"{node_info['id']:02d}_lev{node_info['level']}_{safe_title}.md"
                output_path = Path(args.output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
                file_path = output_path / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(section_text)
                
                print(f"섹션이 추출되어 저장되었습니다: {file_path}")
                print(f"노드 정보: {node_info['title']} (level {node_info['level']})")
            else:
                # 모든 content 노드 추출
                extracted_files = extractor.extract_all_sections(args.output_dir)
                
                print(f"\n추출 완료! 총 {len(extracted_files)}개 파일이 생성되었습니다.")
                print(f"출력 디렉토리: {os.path.abspath(args.output_dir)}")
                
        except Exception as e:
            print(f"오류: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    BatchSectionExtractor.main()