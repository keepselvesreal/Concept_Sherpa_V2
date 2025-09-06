#!/usr/bin/env python3
"""
Part-Chapter 관계 디버깅 스크립트
"""

import sys
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/TOC_Normalization')
from toc_normalizer import TOCNormalizer, TOCItem

def debug_part_chapter_relationships():
    """Part-Chapter 관계 디버깅"""
    normalizer = TOCNormalizer()
    
    # 현재 TOC 파싱
    normalizer.parse_toc_markdown('/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_TOC.md')
    
    print("=== Part-Chapter 관계 디버깅 ===\n")
    
    # Part 항목들 찾기
    part_items = []
    chapter_items = []
    
    for item in normalizer.toc_items:
        if 'flexibility' in item.title.lower() or 'scalability' in item.title.lower() or 'maintainability' in item.title.lower():
            part_items.append(item)
            print(f"Part 발견: {item}")
        elif len(item.number_parts) == 1 and item.number_parts[0][0] == 'num' and 1 <= item.number_parts[0][1] <= 15:
            chapter_items.append(item)
    
    print(f"\nPart 항목 수: {len(part_items)}")
    print(f"Chapter 항목 수: {len(chapter_items)}")
    
    # Part-Chapter 관계 테스트
    print("\n=== Part-Chapter 관계 테스트 ===")
    for part in part_items:
        print(f"\nPart: {part.number} '{part.title}'")
        print(f"  number_parts: {part.number_parts}")
        
        for chapter in chapter_items:
            is_parent = part.is_direct_parent_of(chapter)
            print(f"  Chapter {chapter.number}: {is_parent}")
            
            if is_parent:
                print(f"    → Part {part.number} is parent of Chapter {chapter.number}")

if __name__ == "__main__":
    debug_part_chapter_relationships()