#!/usr/bin/env python3
"""
# level_chapter_leaf_organizer.py

## 생성 시간: 2025-08-10 15:35:10 KST

## 핵심 내용: 파트 단위 리프 노드를 레벨별, 장별로 분리하여 저장

## 상세 내용:
- LevelChapterOrganizer (라인 26-159): 레벨별, 장별 리프 노드 분리 메인 클래스  
- load_part_leaf_nodes (라인 35-55): 파트별 리프 노드 JSON 파일 로드
- extract_chapter_from_title (라인 57-82): 제목에서 장 번호 추출 로직
- organize_by_level_and_chapter (라인 84-117): 레벨과 장별로 노드 조직화
- save_organized_nodes (라인 119-145): 조직화된 노드들을 파일로 저장
- process_all_parts (라인 147-159): 모든 파트 처리
- main (라인 162-199): 메인 실행 함수

## 상태: 활성

## 주소: level_chapter_leaf_organizer

## 참조: 
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class LevelChapterOrganizer:
    """레벨별, 장별 리프 노드 분리 도구"""
    
    def __init__(self, input_dir: str, output_dir: str):
        """
        초기화
        
        Args:
            input_dir: 파트별 리프 노드 파일들이 있는 디렉터리
            output_dir: 레벨별, 장별 파일들을 저장할 디렉터리
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
            장 번호 (예: "01", "07", "Appendix_A") 또는 None
        """
        # Part Introduction 처리
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
    
    def organize_by_level_and_chapter(self, nodes: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        노드들을 레벨별, 장별로 조직화합니다.
        
        Args:
            nodes: 리프 노드 리스트
            
        Returns:
            {level: {chapter: [nodes]}} 형태의 중첩 딕셔너리
        """
        organized = defaultdict(lambda: defaultdict(list))
        
        for node in nodes:
            level = node.get('level', 0)
            title = node.get('title', '')
            
            chapter = self.extract_chapter_from_title(title)
            if not chapter:
                chapter = "Miscellaneous"
            
            # 노드에서 필요한 필드만 추출
            clean_node = {
                'id': node.get('id'),
                'title': node.get('title', ''),
                'level': node.get('level', 0),
                'start_text': node.get('start_text', ''),
                'end_text': node.get('end_text', '')
            }
            
            organized[f"Level_{level}"][chapter].append(clean_node)
        
        return organized
    
    def save_organized_nodes(self, organized_nodes: Dict[str, Dict[str, List[Dict[str, Any]]]], part_name: str) -> List[str]:
        """
        조직화된 노드들을 파일로 저장합니다.
        
        Args:
            organized_nodes: 레벨별, 장별로 조직화된 노드들
            part_name: 파트 이름
            
        Returns:
            저장된 파일 경로 리스트
        """
        saved_files = []
        
        for level_key, chapters in organized_nodes.items():
            for chapter_key, nodes in chapters.items():
                if not nodes:  # 빈 리스트는 건너뛰기
                    continue
                    
                filename = f"{part_name}_{level_key}_{chapter_key}.json"
                output_path = self.output_dir / filename
                
                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(nodes, f, ensure_ascii=False, indent=2)
                    
                    saved_files.append(str(output_path))
                    print(f"✓ {filename}: {len(nodes)}개 노드")
                    
                except Exception as e:
                    print(f"❌ {filename} 저장 실패: {e}")
        
        return saved_files
    
    def process_all_parts(self) -> Dict[str, List[str]]:
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
                    organized = self.organize_by_level_and_chapter(nodes)
                    saved_files = self.save_organized_nodes(organized, part_name)
                    results[part_name] = saved_files
                else:
                    results[part_name] = []
            else:
                print(f"❌ {part_name}: 파일이 없습니다 ({filename})")
                results[part_name] = []
        
        return results


def main():
    """메인 실행 함수"""
    print("🚀 레벨별, 장별 리프 노드 분리 도구 시작")
    print("=" * 50)
    
    # 경로 설정
    input_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-10/level_chapter_nodes"
    
    print(f"📂 입력 디렉터리: {input_dir}")
    print(f"📁 출력 디렉터리: {output_dir}")
    
    try:
        # 조직화 도구 생성
        organizer = LevelChapterOrganizer(input_dir, output_dir)
        
        # 모든 파트 처리
        results = organizer.process_all_parts()
        
        # 결과 요약
        print(f"\n📊 처리 결과 요약:")
        total_files = 0
        for part_name, saved_files in results.items():
            print(f"   - {part_name}: {len(saved_files)}개 파일")
            total_files += len(saved_files)
        
        print(f"\n✅ 총 {total_files}개 레벨/장별 파일 생성 완료!")
        print(f"   출력 위치: {output_dir}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())