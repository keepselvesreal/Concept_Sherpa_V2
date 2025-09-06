#!/usr/bin/env python3
"""
# improved_leaf_organizer.py

## 생성 시간: 2025-08-10 15:45:10 KST

## 핵심 내용: Summary, Moving forward 등을 해당 장에 포함하는 개선된 리프 노드 조직화 도구

## 상세 내용:
- ImprovedLeafOrganizer (라인 26-256): 컨텍스트 기반 리프 노드 조직화 메인 클래스
- load_part_leaf_nodes (라인 35-55): 파트별 리프 노드 JSON 파일 로드
- get_chapter_context (라인 57-89): 노드 순서를 기반으로 장 컨텍스트 파악
- assign_chapter_with_context (라인 91-146): 컨텍스트를 고려한 장 할당 로직
- organize_nodes_intelligently (라인 148-201): 지능적 노드 조직화
- save_level1_nodes (라인 203-220): 레벨1 노드들을 개별 파일로 저장
- save_chapter_nodes (라인 222-254): 장별 노드들을 파일로 저장
- process_all_parts (라인 256-277): 모든 파트 처리
- main (라인 280-317): 메인 실행 함수

## 상태: 활성

## 주소: improved_leaf_organizer

## 참조: level_chapter_leaf_organizer_v2
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict


class ImprovedLeafOrganizer:
    """컨텍스트를 고려한 지능적 리프 노드 조직화 도구"""
    
    def __init__(self, input_dir: str, output_dir: str):
        """
        초기화
        
        Args:
            input_dir: 파트별 리프 노드 파일들이 있는 디렉터리
            output_dir: 분리된 파일들을 저장할 디렉터리
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
    
    def get_chapter_context(self, nodes: List[Dict[str, Any]], current_index: int) -> Optional[str]:
        """
        노드의 순서를 고려해 장 컨텍스트를 파악합니다.
        Summary, Moving forward 등은 이전 장 번호 노드를 찾아서 해당 장으로 할당합니다.
        
        Args:
            nodes: 전체 노드 리스트
            current_index: 현재 노드의 인덱스
            
        Returns:
            장 번호 (예: "Chapter_01") 또는 None
        """
        current_node = nodes[current_index]
        title = current_node.get('title', '')
        
        # 직접 장 번호가 있는 경우
        chapter_match = re.match(r'^(\d+)', title)
        if chapter_match:
            return f"Chapter_{chapter_match.group(1).zfill(2)}"
        
        # Summary, Moving forward 등은 이전 장 번호 노드를 찾기
        if title in ['Summary', 'Moving forward', 'Farewell']:
            # 역순으로 탐색해서 가장 최근 장 번호 찾기
            for i in range(current_index - 1, -1, -1):
                prev_node = nodes[i]
                prev_title = prev_node.get('title', '')
                prev_chapter_match = re.match(r'^(\d+)', prev_title)
                if prev_chapter_match:
                    return f"Chapter_{prev_chapter_match.group(1).zfill(2)}"
        
        # Appendix 처리
        appendix_match = re.match(r'Appendix\s+([A-Z])', title)
        if appendix_match:
            return f"Appendix_{appendix_match.group(1)}"
        
        # Part 처리 (레벨1용)
        if title.startswith('Part'):
            part_match = re.match(r'Part\s+(\d+)', title)
            if part_match:
                return f"Part_{part_match.group(1).zfill(2)}"
        
        return None
    
    def assign_chapter_with_context(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        컨텍스트를 고려해 각 노드에 장 정보를 할당합니다.
        
        Args:
            nodes: 리프 노드 리스트
            
        Returns:
            장 정보가 추가된 노드 리스트
        """
        enhanced_nodes = []
        current_chapter = None
        
        for i, node in enumerate(nodes):
            title = node.get('title', '')
            
            # 장 컨텍스트 파악
            chapter = self.get_chapter_context(nodes, i)
            
            # 장 정보 업데이트
            if chapter:
                current_chapter = chapter
            elif current_chapter is None:
                current_chapter = "Miscellaneous"
            
            # 노드에 장 정보 추가
            enhanced_node = {
                'id': node.get('id'),
                'title': node.get('title', ''),
                'level': node.get('level', 0),
                'start_text': node.get('start_text', ''),
                'end_text': node.get('end_text', ''),
                'assigned_chapter': current_chapter
            }
            enhanced_nodes.append(enhanced_node)
            
            # 디버그 정보 (특별한 경우만)
            if title in ['Summary', 'Moving forward', 'Farewell']:
                print(f"   📍 '{title}' → {current_chapter}")
        
        return enhanced_nodes
    
    def organize_nodes_intelligently(self, nodes: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
        """
        노드들을 지능적으로 조직화합니다.
        - 레벨1: 독립 노드들
        - 레벨2-4: 장별로 그룹화된 노드들 (컨텍스트 고려)
        
        Args:
            nodes: 리프 노드 리스트
            
        Returns:
            tuple: (레벨1 노드들, {장: 레벨2-4 노드들})
        """
        # 1단계: 컨텍스트 기반 장 할당
        enhanced_nodes = self.assign_chapter_with_context(nodes)
        
        # 2단계: 레벨별 분리
        level1_nodes = []
        chapter_nodes = defaultdict(list)
        
        for node in enhanced_nodes:
            level = node.get('level', 0)
            assigned_chapter = node.get('assigned_chapter', 'Miscellaneous')
            
            # assigned_chapter 필드 제거 (최종 출력에서는 불필요)
            clean_node = {
                'id': node.get('id'),
                'title': node.get('title', ''),
                'level': node.get('level', 0),
                'start_text': node.get('start_text', ''),
                'end_text': node.get('end_text', '')
            }
            
            if level == 1:
                level1_nodes.append(clean_node)
            else:
                chapter_nodes[assigned_chapter].append(clean_node)
        
        return level1_nodes, dict(chapter_nodes)
    
    def save_level1_nodes(self, level1_nodes: List[Dict[str, Any]], part_name: str) -> List[str]:
        """
        레벨1 노드들을 개별 파일로 저장합니다.
        
        Args:
            level1_nodes: 레벨1 노드들
            part_name: 파트 이름
            
        Returns:
            저장된 파일 경로 리스트
        """
        saved_files = []
        
        for node in level1_nodes:
            title = node.get('title', 'Unknown')
            if title.startswith('Part'):
                part_match = re.match(r'Part\s+(\d+)', title)
                if part_match:
                    chapter = f"Part_{part_match.group(1).zfill(2)}"
                else:
                    chapter = "Unknown"
            else:
                chapter = "Unknown"
            
            filename = f"{part_name}_Level1_{chapter}.json"
            output_path = self.output_dir / filename
            
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump([node], f, ensure_ascii=False, indent=2)
                
                saved_files.append(str(output_path))
                print(f"✓ {filename}: 1개 노드")
                
            except Exception as e:
                print(f"❌ {filename} 저장 실패: {e}")
        
        return saved_files
    
    def save_chapter_nodes(self, chapter_nodes: Dict[str, List[Dict[str, Any]]], part_name: str) -> List[str]:
        """
        장별 노드들을 파일로 저장합니다 (레벨2-4 통합).
        
        Args:
            chapter_nodes: 장별로 그룹화된 노드들
            part_name: 파트 이름
            
        Returns:
            저장된 파일 경로 리스트
        """
        saved_files = []
        
        for chapter, nodes in chapter_nodes.items():
            if not nodes:  # 빈 리스트는 건너뛰기
                continue
                
            filename = f"{part_name}_{chapter}.json"
            output_path = self.output_dir / filename
            
            try:
                # ID 순서로 정렬 (원래 순서 유지)
                sorted_nodes = sorted(nodes, key=lambda x: x.get('id', 0))
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(sorted_nodes, f, ensure_ascii=False, indent=2)
                
                saved_files.append(str(output_path))
                
                # 통계 정보
                level_counts = {}
                for node in sorted_nodes:
                    level = node.get('level', 0)
                    level_counts[level] = level_counts.get(level, 0) + 1
                
                level_info = ", ".join([f"L{level}: {count}" for level, count in sorted(level_counts.items())])
                print(f"✓ {filename}: {len(sorted_nodes)}개 노드 ({level_info})")
                
            except Exception as e:
                print(f"❌ {filename} 저장 실패: {e}")
        
        return saved_files
    
    def process_all_parts(self) -> Dict[str, Dict[str, List[str]]]:
        """모든 파트의 리프 노드를 처리합니다."""
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
                    level1_nodes, chapter_nodes = self.organize_nodes_intelligently(nodes)
                    
                    level1_files = self.save_level1_nodes(level1_nodes, part_name)
                    chapter_files = self.save_chapter_nodes(chapter_nodes, part_name)
                    
                    results[part_name] = {
                        'level1_files': level1_files,
                        'chapter_files': chapter_files
                    }
                else:
                    results[part_name] = {'level1_files': [], 'chapter_files': []}
            else:
                print(f"❌ {part_name}: 파일이 없습니다 ({filename})")
                results[part_name] = {'level1_files': [], 'chapter_files': []}
        
        return results


def main():
    """메인 실행 함수"""
    print("🚀 컨텍스트 기반 지능적 리프 노드 조직화 도구 시작")
    print("=" * 60)
    
    # 경로 설정
    input_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/smart_organized_nodes"
    
    print(f"📂 입력 디렉터리: {input_dir}")
    print(f"📁 출력 디렉터리: {output_dir}")
    
    try:
        # 조직화 도구 생성
        organizer = ImprovedLeafOrganizer(input_dir, output_dir)
        
        # 모든 파트 처리
        results = organizer.process_all_parts()
        
        # 결과 요약
        print(f"\n📊 처리 결과 요약:")
        total_level1_files = 0
        total_chapter_files = 0
        
        for part_name, part_results in results.items():
            level1_count = len(part_results['level1_files'])
            chapter_count = len(part_results['chapter_files'])
            total_level1_files += level1_count
            total_chapter_files += chapter_count
            print(f"   - {part_name}: 레벨1 {level1_count}개, 장별 {chapter_count}개")
        
        total_files = total_level1_files + total_chapter_files
        print(f"\n✅ 총 {total_files}개 파일 생성 완료!")
        print(f"   - 레벨1 독립 파일: {total_level1_files}개")
        print(f"   - 장별 통합 파일: {total_chapter_files}개")
        print(f"   출력 위치: {output_dir}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())