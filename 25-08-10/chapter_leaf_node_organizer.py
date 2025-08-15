#!/usr/bin/env python3
"""
# chapter_leaf_node_organizer.py

## 생성 시간: 2025-08-10 15:28:10 KST

## 핵심 내용: 파트 단위 리프 노드 파일을 장별로 분리하여 저장하는 도구

## 상세 내용:
- ChapterLeafNodeOrganizer (라인 29-154): 파트별 리프 노드를 장별로 분리하는 메인 클래스
- load_part_leaf_nodes (라인 39-59): 파트별 리프 노드 JSON 파일 로드
- group_nodes_by_chapter (라인 61-93): 노드를 장별로 그룹화하는 로직
- save_chapter_nodes (라인 95-132): 장별 노드를 개별 파일로 저장
- process_all_parts (라인 134-154): 모든 파트의 리프 노드 처리
- main (라인 157-205): 메인 실행 함수

## 상태: 활성

## 주소: chapter_leaf_node_organizer

## 참조: 
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ChapterLeafNodeOrganizer:
    """파트별 리프 노드를 장별로 분리하는 조직화 도구"""
    
    def __init__(self, input_dir: str, output_dir: str):
        """
        초기화
        
        Args:
            input_dir: 파트별 리프 노드 파일들이 있는 디렉터리
            output_dir: 장별 파일들을 저장할 디렉터리
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_part_leaf_nodes(self, part_file: Path) -> List[Dict[str, Any]]:
        """
        파트별 리프 노드 JSON 파일을 로드합니다.
        
        Args:
            part_file: 파트별 리프 노드 JSON 파일 경로
            
        Returns:
            리프 노드 리스트
        """
        try:
            with open(part_file, 'r', encoding='utf-8') as f:
                nodes = json.load(f)
            print(f"✓ {part_file.name} 로드 완료: {len(nodes)}개 노드")
            return nodes
        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {part_file}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 오류 ({part_file}): {e}")
            return []
    
    def group_nodes_by_chapter(self, nodes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        리프 노드들을 장별로 그룹화합니다.
        
        Args:
            nodes: 리프 노드 리스트
            
        Returns:
            장별로 그룹화된 노드 딕셔너리 {장_이름: [노드들]}
        """
        chapters = {}
        
        for node in nodes:
            title = node.get('title', '')
            
            # 장 번호 추출 (예: "1 Introduction", "7.1 Data validation", "Appendix A Introduction")
            chapter_pattern = r'^(\d+|Appendix [A-Z]|Part \d+)\s'
            match = re.match(chapter_pattern, title)
            
            if match:
                chapter_key = match.group(1)
                
                # 장 이름 정규화
                if chapter_key.startswith('Part'):
                    chapter_name = f"{chapter_key}_Introduction"
                elif chapter_key.startswith('Appendix'):
                    chapter_name = f"{chapter_key}_Principles"
                else:
                    chapter_name = f"Chapter_{chapter_key.zfill(2)}"
                    
                if chapter_name not in chapters:
                    chapters[chapter_name] = []
                chapters[chapter_name].append(node)
            else:
                # 패턴에 맞지 않는 경우 기타로 분류
                if 'Miscellaneous' not in chapters:
                    chapters['Miscellaneous'] = []
                chapters['Miscellaneous'].append(node)
        
        return chapters
    
    def save_chapter_nodes(self, chapter_nodes: Dict[str, List[Dict[str, Any]]], part_name: str) -> List[str]:
        """
        장별 노드를 개별 파일로 저장합니다.
        
        Args:
            chapter_nodes: 장별로 그룹화된 노드 딕셔너리
            part_name: 파트 이름 (파일명에 포함)
            
        Returns:
            저장된 파일 경로 리스트
        """
        saved_files = []
        
        for chapter_name, nodes in chapter_nodes.items():
            filename = f"{part_name}_{chapter_name}_leaf_nodes.json"
            output_path = self.output_dir / filename
            
            try:
                # 메타데이터 추가
                output_data = {
                    "metadata": {
                        "part_name": part_name,
                        "chapter_name": chapter_name,
                        "node_count": len(nodes),
                        "created_at": datetime.now().isoformat(),
                        "description": f"{part_name}의 {chapter_name} 리프 노드들"
                    },
                    "nodes": nodes
                }
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, ensure_ascii=False, indent=2)
                
                saved_files.append(str(output_path))
                print(f"✓ {filename} 저장 완료: {len(nodes)}개 노드")
                
            except Exception as e:
                print(f"❌ {filename} 저장 실패: {e}")
        
        return saved_files
    
    def process_all_parts(self) -> Dict[str, List[str]]:
        """
        모든 파트의 리프 노드를 처리합니다.
        
        Returns:
            파트별 저장된 파일 리스트 딕셔너리
        """
        part_files = {
            "Part1_Flexibility": "part1_flexibility_leaf_nodes.json",
            "Part2_Scalability": "part2_scalability_leaf_nodes.json", 
            "Part3_Maintainability": "part3_maintainability_leaf_nodes.json"
        }
        
        results = {}
        
        for part_name, filename in part_files.items():
            part_file = self.input_dir / filename
            
            if part_file.exists():
                print(f"\n🔄 {part_name} 처리 중...")
                nodes = self.load_part_leaf_nodes(part_file)
                
                if nodes:
                    chapter_nodes = self.group_nodes_by_chapter(nodes)
                    print(f"   {len(chapter_nodes)}개 장으로 분류됨")
                    
                    saved_files = self.save_chapter_nodes(chapter_nodes, part_name)
                    results[part_name] = saved_files
                else:
                    print(f"   ⚠️ {part_name}: 노드가 없습니다")
                    results[part_name] = []
            else:
                print(f"   ❌ {part_name}: 파일이 없습니다 ({filename})")
                results[part_name] = []
        
        return results


def main():
    """메인 실행 함수"""
    print("🚀 파트별 리프 노드 → 장별 분리 도구 시작")
    print("=" * 50)
    
    # 경로 설정
    input_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/chapter_leaf_nodes"
    
    print(f"📂 입력 디렉터리: {input_dir}")
    print(f"📁 출력 디렉터리: {output_dir}")
    
    try:
        # 조직화 도구 생성
        organizer = ChapterLeafNodeOrganizer(input_dir, output_dir)
        
        # 모든 파트 처리
        results = organizer.process_all_parts()
        
        # 결과 요약
        print(f"\n📊 처리 결과 요약:")
        total_files = 0
        for part_name, saved_files in results.items():
            print(f"   - {part_name}: {len(saved_files)}개 장 파일")
            total_files += len(saved_files)
        
        print(f"\n✅ 총 {total_files}개 장별 파일 생성 완료!")
        print(f"   출력 위치: {output_dir}")
        
        # 생성된 파일 목록 출력
        if total_files > 0:
            print(f"\n📝 생성된 파일 목록:")
            for part_name, saved_files in results.items():
                if saved_files:
                    print(f"   {part_name}:")
                    for file_path in saved_files:
                        print(f"     - {Path(file_path).name}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())