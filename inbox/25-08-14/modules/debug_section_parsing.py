"""
생성 시간: 2025-08-14 21:20:00 KST
핵심 내용: 자식 노드 내용 섹션 파싱 문제 디버깅 스크립트
상세 내용:
    - DataLoader._extract_section_from_file() 함수 디버깅
    - 실제 파일 내용과 파싱 결과 비교
    - 섹션 헤더 인식 문제 원인 분석
상태: 디버깅용
주소: debug_section_parsing
참조: parent_node_processor.py
"""

from pathlib import Path
import sys
import os

# 상위 디렉토리에서 모듈 임포트 가능하게 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.parent_node_processor import DataLoader
from modules.logging_system_v2 import ProcessLogger

def debug_section_parsing():
    """섹션 파싱 문제 디버깅"""
    
    # 테스트 대상 파일
    test_file = Path("/home/nadle/projects/Knowledge_Sherpa/v2/25-08-14/node_docs/01_lev1_introduction_and_overview_info.md")
    
    print("=" * 60)
    print("섹션 파싱 디버깅")
    print("=" * 60)
    print(f"테스트 파일: {test_file}")
    
    if not test_file.exists():
        print(f"❌ 파일이 존재하지 않습니다: {test_file}")
        return
    
    # 1. 원본 파일 내용 확인
    print("\n1️⃣ 원본 파일 내용:")
    print("-" * 40)
    with open(test_file, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    lines = original_content.split('\n')
    for i, line in enumerate(lines[:20], 1):  # 처음 20줄만 표시
        print(f"{i:2d}: {repr(line)}")
    
    if len(lines) > 20:
        print(f"... (총 {len(lines)}줄 중 처음 20줄만 표시)")
    
    # 2. DataLoader 초기화 및 테스트
    print("\n2️⃣ DataLoader 테스트:")
    print("-" * 40)
    
    logger = ProcessLogger("debug", Path("/tmp"))
    data_loader = DataLoader(test_file.parent, logger)
    
    # 3. 내용 섹션 추출 시도
    print("\n3️⃣ 내용 섹션 추출 결과:")
    print("-" * 40)
    
    content_section = data_loader._extract_section_from_file(test_file, "내용")
    print(f"추출된 내용 길이: {len(content_section)}")
    print(f"추출된 내용 (처음 200자):")
    print(repr(content_section[:200]))
    
    if not content_section.strip():
        print("❌ 내용 섹션이 비어있습니다!")
    else:
        print("✅ 내용 섹션이 정상적으로 추출되었습니다.")
    
    # 4. 섹션 헤더 검색 디버깅
    print("\n4️⃣ 섹션 헤더 검색 디버깅:")
    print("-" * 40)
    
    header_pattern = "# 내용"
    header_start = original_content.find(header_pattern)
    print(f"'{header_pattern}' 패턴 위치: {header_start}")
    
    if header_start != -1:
        # 헤더 주변 내용 확인
        start_line = original_content[:header_start].count('\n')
        print(f"헤더가 있는 줄 번호: {start_line + 1}")
        
        # 헤더 다음 내용 확인
        content_start = header_start + len(header_pattern)
        next_content = original_content[content_start:content_start + 100]
        print(f"헤더 다음 내용 (100자): {repr(next_content)}")
        
        # 다음 섹션 헤더까지의 내용
        lines_after_header = original_content[content_start:].split('\n')
        print(f"헤더 다음 줄들 (처음 10줄):")
        for i, line in enumerate(lines_after_header[:10]):
            print(f"  {i+1}: {repr(line)}")
            if line.strip().startswith('# ') and not line.strip().startswith('##'):
                print(f"    ⚠️ 다음 섹션 헤더 발견: {line.strip()}")
                break
    else:
        print("❌ '# 내용' 헤더를 찾을 수 없습니다!")
        
        # 비슷한 패턴들 검색
        print("\n🔍 유사한 패턴들 검색:")
        patterns_to_check = ["#내용", "# 내용", "##내용", "## 내용", "내용"]
        for pattern in patterns_to_check:
            pos = original_content.find(pattern)
            if pos != -1:
                line_num = original_content[:pos].count('\n') + 1
                print(f"  '{pattern}' 발견: 위치 {pos}, 줄 {line_num}")

if __name__ == "__main__":
    debug_section_parsing()