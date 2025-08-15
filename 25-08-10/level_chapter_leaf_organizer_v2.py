#!/usr/bin/env python3
"""
# level_chapter_leaf_organizer_v2.py

## 생성 시간: 2025-08-10 15:40:10 KST

## 핵심 내용: 레벨1은 독립 파일로, 레벨2-4는 장별 통합 파일로 리프 노드 분리 저장

## 상세 내용:
- LevelChapterOrganizerV2 (라인 26-181): 개선된 레벨/장별 리프 노드 분리 클래스
- load_part_leaf_nodes (라인 35-55): 파트별 리프 노드 JSON 파일 로드
- extract_chapter_from_title (라인 57-82): 제목에서 장 번호 추출 로직
- organize_nodes_by_structure (라인 84-139): 레벨1 독립, 레벨2-4 장별 그룹화 로직
- save_level1_nodes (라인 141-158): 레벨1 노드들을 개별 파일로 저장
- save_chapter_nodes (라인 160-179): 장별 통합 노드들을 파일로 저장
- process_all_parts (라인 181-202): 모든 파트 처리
- main (라인 205-242): 메인 실행 함수

## 상태: 활성

## 주소: level_chapter_leaf_organizer_v2

## 참조: level_chapter_leaf_organizer
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict


class LevelChapterOrganizerV2:
    """레벨1 독립, 레벨2-4 장별 통합 리프 노드 분리 도구"""
    
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
    
    def extract_chapter_from_title(self, title: str) -> Optional[str]:
        """
        제목에서 장 번호를 추출합니다.
        
        Args:
            title: 노드 제목
            
        Returns:
            장 번호 (예: "Chapter_01", "Chapter_07", "Appendix_A") 또는 None
        """
        # Part Introduction 처리 (레벨1용)
        if title.startswith('Part'):
            part_match = re.match(r'Part\s+(\d+)', title)
            if part_match:
                return f"Part_{part_match.group(1).zfill(2)}"
        
        # 일반 장 번호 (예: "7 Introduction", "7.1 Data validation")
        chapter_match = re.match(r'^(\d+)', title)
        if chapter_match:
            return f"Chapter_{chapter_match.group(1).zfill(2)}"
        
        # Appendix 처리 (예: "Appendix A Introduction")
        appendix_match = re.match(r'Appendix\s+([A-Z])', title)
        if appendix_match:
            return f"Appendix_{appendix_match.group(1)}"
        
        # Summary 처리
        if title == "Summary":
            return "Summary"
        
        return None
    
    def organize_nodes_by_structure(self, nodes: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
        """
        노드들을 구조에 따라 조직화합니다.
        - 레벨1: 독립 노드들
        - 레벨2-4: 장별로 그룹화된 노드들
        
        Args:
            nodes: 리프 노드 리스트
            
        Returns:
            tuple: (레벨1 노드들, {장: 레벨2-4 노드들})
        """
        level1_nodes = []
        chapter_nodes = defaultdict(list)
        
        for node in nodes:
            level = node.get('level', 0)
            title = node.get('title', '')
            
            # 노드에서 필요한 필드만 추출
            clean_node = {
                'id': node.get('id'),
                'title': node.get('title', ''),
                'level': node.get('level', 0),
                'start_text': node.get('start_text', ''),
                'end_text': node.get('end_text', '')
            }
            
            if level == 1:
                # 레벨1은 독립 저장용
                level1_nodes.append(clean_node)
            else:
                # 레벨2-4는 장별 그룹화
                chapter = self.extract_chapter_from_title(title)
                if not chapter:
                    chapter = "Miscellaneous"
                chapter_nodes[chapter].append(clean_node)
        
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
            chapter = self.extract_chapter_from_title(title) or "Unknown"
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
                # 레벨 순서로 정렬
                sorted_nodes = sorted(nodes, key=lambda x: (x.get('level', 0), x.get('id', 0)))
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(sorted_nodes, f, ensure_ascii=False, indent=2)
                
                saved_files.append(str(output_path))
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
                    level1_nodes, chapter_nodes = self.organize_nodes_by_structure(nodes)
                    
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
    print("🚀 레벨1 독립, 레벨2-4 장별 통합 리프 노드 분리 도구 시작")
    print("=" * 60)
    
    # 경로 설정
    input_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/organized_leaf_nodes"
    
    print(f"📂 입력 디렉터리: {input_dir}")
    print(f"📁 출력 디렉터리: {output_dir}")
    
    try:
        # 조직화 도구 생성
        organizer = LevelChapterOrganizerV2(input_dir, output_dir)
        
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