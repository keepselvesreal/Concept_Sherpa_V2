# 생성 시간: 2025-08-17 17:38:23 KST
# 핵심 내용: MD 파일의 헤더를 파싱하여 노드 JSON 구조 생성 모듈
# 상세 내용:
#   - MarkdownNodeExtractor 클래스 (라인 20-120): MD 파일 헤더 파싱 및 노드 생성
#   - parse_headers 메서드 (라인 30-65): 마크다운 헤더 파싱 및 레벨 분석
#   - generate_node_id 메서드 (라인 67-75): 고유 노드 ID 생성
#   - extract_nodes 메서드 (라인 77-100): 헤더 정보를 노드 JSON으로 변환
#   - save_to_json 메서드 (라인 102-110): JSON 파일 저장
#   - main 함수 (라인 122-140): CLI 인터페이스
# 상태: 활성
# 주소: md_to_nodes
# 참조: 없음

import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any


class MarkdownNodeExtractor:
    def __init__(self):
        self.header_pattern = re.compile(r'^(#{1,6})\s+(.+)', re.MULTILINE)
    
    def parse_headers(self, markdown_content: str) -> List[Dict[str, Any]]:
        """마크다운 헤더를 파싱하여 헤더 정보 리스트 반환"""
        headers = []
        
        matches = self.header_pattern.findall(markdown_content)
        
        for match in matches:
            header_marks, title = match
            level = len(header_marks) - 1  # # -> level 0, ## -> level 1
            
            # 제목에서 불필요한 공백 제거
            title = title.strip()
            
            headers.append({
                'title': title,
                'level': level,
                'header_marks': header_marks
            })
        
        return headers
    
    def generate_node_id(self, index: int) -> int:
        """0부터 시작하는 정수 ID 생성"""
        return index
    
    def extract_nodes(self, file_path: str) -> List[Dict[str, Any]]:
        """MD 파일에서 노드 정보 추출"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
        headers = self.parse_headers(content)
        nodes = []
        
        for i, header in enumerate(headers):
            node = {
                'id': self.generate_node_id(i),
                'title': header['title'],
                'level': header['level']
            }
            nodes.append(node)
        
        return nodes
    
    def save_to_json(self, nodes: List[Dict[str, Any]], output_path: str):
        """노드 리스트를 JSON 파일로 저장"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        print(f"✅ 노드 JSON 파일 저장 완료: {output_path}")
        print(f"📊 총 {len(nodes)}개 노드 생성")


def main():
    parser = argparse.ArgumentParser(description='MD 파일에서 헤더 기반 노드 JSON 생성')
    parser.add_argument('md_file', help='입력 마크다운 파일 경로')
    parser.add_argument('-o', '--output', help='출력 JSON 파일 경로')
    
    args = parser.parse_args()
    
    # 출력 파일 경로 설정
    if args.output:
        output_path = args.output
    else:
        md_path = Path(args.md_file)
        output_path = md_path.parent / f"{md_path.stem}_nodes.json"
    
    extractor = MarkdownNodeExtractor()
    
    try:
        # 노드 추출
        print(f"🚀 MD 파일 분석 시작: {args.md_file}")
        nodes = extractor.extract_nodes(args.md_file)
        
        # 결과 미리보기
        print(f"\n📋 노드 미리보기:")
        for node in nodes[:5]:  # 처음 5개만 출력
            print(f"  - {node['id']} (level {node['level']}): {node['title']}")
        
        if len(nodes) > 5:
            print(f"  ... 및 {len(nodes) - 5}개 추가 노드")
        
        # JSON 저장
        extractor.save_to_json(nodes, output_path)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()