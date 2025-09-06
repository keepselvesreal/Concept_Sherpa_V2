# 생성 시간: 2025-08-17 17:38:23 KST
# 핵심 내용: has_content=true인 노드의 섹션 텍스트를 개별 파일로 추출하는 스크립트
# 상세 내용:
#   - ContentSectionExtractor 클래스 (라인 20-170): has_content=true 노드 섹션 추출
#   - load_enhanced_nodes 메서드 (라인 35-45): 확장된 노드 JSON 로드
#   - find_node_by_id 메서드 (라인 47-55): ID로 특정 노드 찾기
#   - find_next_node 메서드 (라인 57-90): 다음 노드 찾기 (상위 레벨 포함)
#   - extract_section 메서드 (라인 92-130): 지정된 노드의 섹션 텍스트 추출
#   - get_section_header 메서드 (라인 132-140): 노드 레벨에 맞는 마크다운 헤더 생성
#   - sanitize_filename 메서드 (라인 142-150): 파일명으로 사용 가능한 문자열 정리
#   - extract_content_sections 메서드 (라인 152-170): has_content=true 노드들의 섹션을 개별 파일로 추출
#   - main 함수 (라인 172-200): CLI 인터페이스
# 상태: 활성
# 주소: content_section_extractor
# 참조: batch_section_extractor (섹션 추출 로직)

import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class ContentSectionExtractor:
    """has_content=true인 노드의 섹션을 개별 파일로 추출하는 클래스"""
    
    def __init__(self, enhanced_nodes_file: str, markdown_file: str):
        """
        초기화
        
        Args:
            enhanced_nodes_file: 확장된 노드 정보가 담긴 JSON 파일 경로
            markdown_file: 추출할 마크다운 파일 경로
        """
        self.nodes = self.load_enhanced_nodes(enhanced_nodes_file)
        self.markdown_file = markdown_file
        
        with open(markdown_file, 'r', encoding='utf-8') as f:
            self.content = f.read()
    
    def load_enhanced_nodes(self, nodes_file: str) -> List[Dict]:
        """확장된 노드 JSON 파일 로드"""
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
        현재 노드 다음의 노드 찾기 (같은 레벨 우선, 없으면 상위 레벨)
        
        Args:
            current_node: 현재 노드
            
        Returns:
            다음 노드, 없으면 None
        """
        current_level = current_node['level']
        current_id = current_node['id']
        
        # 현재 노드보다 ID가 큰 노드들 중에서 찾기
        next_candidates = []
        for node in self.nodes:
            if node['id'] > current_id:
                next_candidates.append(node)
        
        if not next_candidates:
            return None
        
        # ID 순으로 정렬해서 가장 가까운 다음 노드 반환
        next_candidates.sort(key=lambda x: x['id'])
        return next_candidates[0]
    
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
                section_text = self.content[start_pos:].rstrip()
        else:
            section_text = self.content[start_pos:].rstrip()
        
        return section_text, current_node
    
    def get_section_header(self, node: Dict) -> str:
        """노드 레벨에 맞는 마크다운 헤더 생성"""
        level = node['level'] + 1  # level 0 = #, level 1 = ##, ...
        return '#' * level + ' ' + node['title']
    
    def sanitize_filename(self, title: str) -> str:
        """파일명으로 사용할 수 있도록 문자열 정리"""
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        return safe_title.strip('_').lower()
    
    def extract_content_sections(self, output_dir: str = "content_sections") -> Dict[str, str]:
        """
        has_content=true인 노드들의 섹션을 개별 파일로 추출
        
        Args:
            output_dir: 출력 디렉토리 경로
            
        Returns:
            {node_id: output_file_path} 딕셔너리
        """
        # 출력 디렉토리 생성
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # has_content=true인 노드들만 필터링
        content_nodes = [node for node in self.nodes if node.get('has_content', False)]
        
        print(f"🚀 has_content=true인 {len(content_nodes)}개 노드의 섹션을 추출합니다...")
        
        extracted_files = {}
        
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
                print(f"   ✅ [{i}/{len(content_nodes)}] {filename}")
                
            except Exception as e:
                print(f"   ❌ [{i}/{len(content_nodes)}] 노드 ID {node['id']} 추출 실패: {e}")
        
        print(f"✅ 추출 완료! {len(extracted_files)}개 파일이 {output_dir}/ 에 생성되었습니다.")
        return extracted_files


def main():
    parser = argparse.ArgumentParser(description='has_content=true인 노드의 섹션을 개별 파일로 추출')
    parser.add_argument('enhanced_nodes_file', help='확장된 노드 JSON 파일 경로')
    parser.add_argument('markdown_file', help='마크다운 파일 경로')
    parser.add_argument('-o', '--output-dir', default='content_sections',
                      help='출력 디렉토리 (기본값: content_sections)')
    
    args = parser.parse_args()
    
    try:
        # 섹션 추출기 초기화 및 실행
        extractor = ContentSectionExtractor(args.enhanced_nodes_file, args.markdown_file)
        extracted_files = extractor.extract_content_sections(args.output_dir)
        
        print(f"\n📊 추출 결과:")
        print(f"   - 추출된 파일 수: {len(extracted_files)}개")
        print(f"   - 출력 디렉토리: {Path(args.output_dir).absolute()}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()