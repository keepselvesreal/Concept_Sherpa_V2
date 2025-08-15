#!/usr/bin/env python3
"""
Part 3 Maintainability 리프 노드 텍스트 추출 스크립트
JSON 경계 정보를 활용하여 각 리프 노드의 텍스트를 추출하고 개별 파일로 저장합니다.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class LeafTextExtractor:
    def __init__(self, md_file_path: str, boundaries_json_path: str, output_dir: str):
        """
        Args:
            md_file_path: 원본 마크다운 파일 경로
            boundaries_json_path: 텍스트 경계 정보 JSON 파일 경로
            output_dir: 추출된 텍스트를 저장할 디렉토리
        """
        self.md_file_path = md_file_path
        self.boundaries_json_path = boundaries_json_path
        self.output_dir = Path(output_dir)
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 원본 텍스트와 경계 정보 로드
        self.full_text = self._load_markdown_file()
        self.leaf_nodes = self._load_boundaries_json()
        
    def _load_markdown_file(self) -> str:
        """마크다운 파일을 읽어서 전체 텍스트 반환"""
        try:
            with open(self.md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ 마크다운 파일 로드 완료: {len(content):,} 문자")
            return content
        except Exception as e:
            raise Exception(f"마크다운 파일 읽기 실패: {e}")
    
    def _load_boundaries_json(self) -> List[Dict]:
        """경계 정보 JSON 파일을 읽어서 리프 노드 정보 반환"""
        try:
            with open(self.boundaries_json_path, 'r', encoding='utf-8') as f:
                nodes = json.load(f)
            print(f"✅ 경계 정보 로드 완료: {len(nodes)}개 리프 노드")
            return nodes
        except Exception as e:
            raise Exception(f"경계 정보 JSON 파일 읽기 실패: {e}")
    
    def _find_text_positions(self, start_text: str, end_text: str) -> Tuple[Optional[int], Optional[int]]:
        """시작과 끝 텍스트의 위치를 찾아서 반환"""
        if not start_text or not end_text:
            return None, None
            
        # 시작 위치 찾기
        start_pos = self.full_text.find(start_text)
        if start_pos == -1:
            return None, None
            
        # 끝 위치 찾기 (시작 위치 이후부터 검색)
        end_pos = self.full_text.find(end_text, start_pos + len(start_text))
        if end_pos == -1:
            return None, None
            
        # 끝 텍스트의 끝까지 포함
        end_pos += len(end_text)
        
        return start_pos, end_pos
    
    def _extract_node_text(self, node: Dict) -> Optional[str]:
        """개별 리프 노드의 텍스트 추출"""
        start_text = node.get('start_text', '').strip()
        end_text = node.get('end_text', '').strip()
        
        if not start_text or not end_text:
            print(f"⚠️  경계 텍스트 누락: {node['title']} (ID: {node['id']})")
            return None
        
        start_pos, end_pos = self._find_text_positions(start_text, end_text)
        
        if start_pos is None or end_pos is None:
            print(f"❌ 텍스트 위치를 찾을 수 없음: {node['title']} (ID: {node['id']})")
            return None
        
        extracted_text = self.full_text[start_pos:end_pos].strip()
        
        # 추출된 텍스트 검증
        if len(extracted_text) < 10:  # 너무 짧은 텍스트는 오류일 가능성
            print(f"⚠️  추출된 텍스트가 너무 짧음: {node['title']} ({len(extracted_text)} 문자)")
            return None
            
        return extracted_text
    
    def _sanitize_filename(self, title: str, node_id: int) -> str:
        """파일명으로 사용할 수 있도록 제목을 정리"""
        # 특수문자 제거 및 공백을 언더스코어로 변경
        clean_title = re.sub(r'[^\w\s-]', '', title)
        clean_title = re.sub(r'[\s]+', '_', clean_title).strip('_')
        
        # 파일명이 너무 길면 자르기
        if len(clean_title) > 50:
            clean_title = clean_title[:50]
        
        return f"{node_id:03d}_{clean_title}.md"
    
    def extract_all_texts(self) -> Dict[str, str]:
        """모든 리프 노드의 텍스트 추출"""
        extracted_texts = {}
        success_count = 0
        
        print(f"\n🚀 {len(self.leaf_nodes)}개 리프 노드 텍스트 추출 시작...")
        
        for i, node in enumerate(self.leaf_nodes, 1):
            node_id = node['id']
            title = node['title']
            
            print(f"\n[{i}/{len(self.leaf_nodes)}] 추출 중: {title} (ID: {node_id})")
            
            extracted_text = self._extract_node_text(node)
            
            if extracted_text:
                extracted_texts[str(node_id)] = extracted_text
                success_count += 1
                print(f"✅ 성공 - {len(extracted_text):,} 문자 추출")
            else:
                print(f"❌ 실패 - 텍스트 추출 불가")
        
        print(f"\n📊 추출 완료: {success_count}/{len(self.leaf_nodes)}개 성공")
        return extracted_texts
    
    def save_extracted_texts(self, extracted_texts: Dict[str, str]) -> None:
        """추출된 텍스트를 개별 파일로 저장"""
        if not extracted_texts:
            print("❌ 저장할 텍스트가 없습니다.")
            return
        
        print(f"\n💾 {len(extracted_texts)}개 파일 저장 중...")
        
        # 통계 정보
        total_chars = 0
        saved_count = 0
        
        for node in self.leaf_nodes:
            node_id = str(node['id'])
            
            if node_id not in extracted_texts:
                continue
            
            # 파일명 생성
            filename = self._sanitize_filename(node['title'], node['id'])
            file_path = self.output_dir / filename
            
            # 파일 저장
            try:
                text_content = extracted_texts[node_id]
                
                # 메타데이터 추가
                content = f"""# {node['title']}

**ID:** {node['id']}  
**Level:** {node['level']}  
**추출 시간:** {self._get_timestamp()}  

---

{text_content}
"""
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                total_chars += len(text_content)
                saved_count += 1
                print(f"✅ {filename} - {len(text_content):,} 문자")
                
            except Exception as e:
                print(f"❌ {filename} 저장 실패: {e}")
        
        print(f"\n📁 저장 완료:")
        print(f"   - 저장된 파일: {saved_count}개")
        print(f"   - 총 문자 수: {total_chars:,}자")
        print(f"   - 저장 위치: {self.output_dir}")
    
    def _get_timestamp(self) -> str:
        """현재 시간 문자열 반환"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def run(self) -> None:
        """전체 추출 프로세스 실행"""
        print("=" * 60)
        print("🔍 Part 3 Maintainability 리프 노드 텍스트 추출 스크립트")
        print("=" * 60)
        
        try:
            # 텍스트 추출
            extracted_texts = self.extract_all_texts()
            
            # 파일로 저장
            if extracted_texts:
                self.save_extracted_texts(extracted_texts)
            
            print("\n🎉 추출 작업 완료!")
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            raise


def main():
    """메인 함수"""
    # 파일 경로 설정
    md_file_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-07/extracted_parts/Part_03_Part_3_Maintainability.md"
    boundaries_json_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/part3_maintainability_leaf_nodes_with_boundaries.json"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_leaf_texts"
    
    # 추출기 생성 및 실행
    extractor = LeafTextExtractor(md_file_path, boundaries_json_path, output_dir)
    extractor.run()


if __name__ == "__main__":
    main()