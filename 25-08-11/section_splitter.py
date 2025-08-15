#!/usr/bin/env python3
"""
생성 시간: 2025-08-11 20:54:32 KST
핵심 내용: 범용 섹션 분할기 - JSON 구조 정보를 기반으로 마크다운 파일을 섹션별로 분할
상세 내용:
    - parse_markdown_content (20-45행): 마크다운 콘텐츠를 헤더 기준으로 파싱
    - extract_section_content (47-85행): 특정 섹션의 콘텐츠 추출
    - create_section_files (87-125행): 개별 섹션 파일들 생성
    - main (127-165행): CLI 인터페이스 및 메인 실행 로직
상태: active
주소: section_splitter
참조: parallel_section_extractor (구조 참고)
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple


def parse_markdown_content(content: str) -> List[Dict[str, Any]]:
    """
    마크다운 콘텐츠를 헤더 기준으로 파싱
    
    Args:
        content: 마크다운 텍스트 콘텐츠
    
    Returns:
        List of dicts with header info and content
    """
    sections = []
    lines = content.split('\n')
    current_section = None
    
    for i, line in enumerate(lines):
        # 헤더 라인 체크 (# ## ### ...)
        header_match = re.match(r'^(#{1,6})\s+(.+)', line.strip())
        
        if header_match:
            # 이전 섹션 마무리
            if current_section:
                sections.append(current_section)
            
            # 새 섹션 시작
            level = len(header_match.group(1)) - 1  # # = 0, ## = 1, ### = 2
            title = header_match.group(2).strip()
            
            current_section = {
                'title': title,
                'level': level,
                'start_line': i,
                'content_lines': [line]
            }
        else:
            # 기존 섹션에 라인 추가
            if current_section:
                current_section['content_lines'].append(line)
    
    # 마지막 섹션 추가
    if current_section:
        sections.append(current_section)
    
    return sections


def extract_section_content(parsed_sections: List[Dict[str, Any]], target_title: str) -> str:
    """
    파싱된 섹션들에서 특정 제목의 섹션 콘텐츠 추출
    
    Args:
        parsed_sections: parse_markdown_content의 결과
        target_title: 찾을 섹션 제목
    
    Returns:
        해당 섹션의 마크다운 콘텐츠
    """
    target_section = None
    target_level = None
    
    # 타겟 섹션 찾기
    for section in parsed_sections:
        if section['title'] == target_title:
            target_section = section
            target_level = section['level']
            break
    
    if not target_section:
        return ""
    
    # 같은 레벨 또는 상위 레벨의 다음 섹션 찾기 (종료 지점 결정)
    start_idx = parsed_sections.index(target_section)
    content_lines = target_section['content_lines'][:]
    
    for i in range(start_idx + 1, len(parsed_sections)):
        next_section = parsed_sections[i]
        
        # 같은 레벨이거나 상위 레벨 섹션이면 여기서 종료
        if next_section['level'] <= target_level:
            break
        
        # 하위 레벨 섹션이면 포함
        content_lines.extend(next_section['content_lines'])
    
    return '\n'.join(content_lines)


def create_section_files(source_file: str, sections_json: str, output_dir: str) -> Dict[str, Any]:
    """
    섹션 정보를 기반으로 개별 파일들 생성
    
    Args:
        source_file: 원본 마크다운 파일 경로
        sections_json: 섹션 구조 정보 JSON 파일 경로
        output_dir: 출력 디렉토리 경로
    
    Returns:
        작업 결과 요약
    """
    # 원본 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 섹션 정보 읽기
    with open(sections_json, 'r', encoding='utf-8') as f:
        section_data = json.load(f)
    
    # 마크다운 파싱
    parsed_sections = parse_markdown_content(content)
    
    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 리프 노드만 추출 (children_ids가 빈 배열인 섹션들)
    leaf_sections = [
        section for section in section_data['sections'] 
        if not section['children_ids']
    ]
    
    successful = 0
    failed = 0
    results = []
    
    for section_info in leaf_sections:
        section_title = section_info['title']
        
        try:
            # 섹션 콘텐츠 추출
            section_content = extract_section_content(parsed_sections, section_title)
            
            if section_content.strip():
                # 안전한 파일명 생성
                safe_filename = re.sub(r'[<>:"/\\|?*]', '_', section_title)
                safe_filename = re.sub(r'\s+', '_', safe_filename)
                filename = f"leaf_{safe_filename}.md"
                
                # 파일 저장
                filepath = output_path / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(section_content)
                
                successful += 1
                results.append({
                    'section_title': section_title,
                    'filename': filename,
                    'status': 'success',
                    'length': len(section_content)
                })
                
                print(f"✅ {filename} ({len(section_content):,}자)")
            else:
                failed += 1
                results.append({
                    'section_title': section_title,
                    'filename': None,
                    'status': 'empty',
                    'length': 0
                })
                print(f"⚠️  {section_title}: 빈 콘텐츠")
        
        except Exception as e:
            failed += 1
            results.append({
                'section_title': section_title,
                'filename': None,
                'status': 'error',
                'error': str(e),
                'length': 0
            })
            print(f"❌ {section_title}: {e}")
    
    return {
        'total_sections': len(leaf_sections),
        'successful': successful,
        'failed': failed,
        'results': results
    }


def main():
    """CLI 인터페이스 및 메인 실행 로직"""
    parser = argparse.ArgumentParser(
        description='마크다운 문서를 JSON 구조 정보에 따라 섹션별로 분할',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python section_splitter.py source.md sections.json output/
  python section_splitter.py -s document.md -j structure.json -o sections/
        """
    )
    
    parser.add_argument('source', nargs='?', help='원본 마크다운 파일 경로')
    parser.add_argument('sections_json', nargs='?', help='섹션 구조 JSON 파일 경로')
    parser.add_argument('output_dir', nargs='?', help='출력 디렉토리 경로')
    
    parser.add_argument('-s', '--source', dest='source_alt', help='원본 마크다운 파일 경로 (대안)')
    parser.add_argument('-j', '--json', dest='json_alt', help='섹션 구조 JSON 파일 경로 (대안)')
    parser.add_argument('-o', '--output', dest='output_alt', help='출력 디렉토리 경로 (대안)')
    
    args = parser.parse_args()
    
    # 인수 처리 (위치 인수 또는 옵션 인수 우선순위)
    source_file = args.source or args.source_alt
    sections_json = args.sections_json or args.json_alt
    output_dir = args.output_dir or args.output_alt
    
    if not all([source_file, sections_json, output_dir]):
        parser.print_help()
        return
    
    # 파일 존재 확인
    if not Path(source_file).exists():
        print(f"❌ 원본 파일을 찾을 수 없습니다: {source_file}")
        return
    
    if not Path(sections_json).exists():
        print(f"❌ JSON 파일을 찾을 수 없습니다: {sections_json}")
        return
    
    print("🎯 섹션 분할기")
    print("=" * 50)
    print(f"📁 원본: {source_file}")
    print(f"📋 구조: {sections_json}")
    print(f"📂 출력: {output_dir}")
    print()
    
    try:
        # 섹션 분할 실행
        summary = create_section_files(source_file, sections_json, output_dir)
        
        print(f"\n📊 작업 완료:")
        print(f"   - 총 섹션: {summary['total_sections']}개")
        print(f"   - 성공: {summary['successful']}개")
        print(f"   - 실패: {summary['failed']}개")
        
        # 실패한 섹션 상세 정보
        failed_results = [r for r in summary['results'] if r['status'] != 'success']
        if failed_results:
            print(f"\n⚠️  문제가 있는 섹션들:")
            for result in failed_results:
                status_msg = f"({result['status']})"
                if 'error' in result:
                    status_msg += f" {result['error']}"
                print(f"   - {result['section_title']}: {status_msg}")
        
        print(f"\n✨ 섹션 파일들이 '{output_dir}'에 저장되었습니다!")
        
    except Exception as e:
        print(f"❌ 작업 실패: {e}")


if __name__ == "__main__":
    main()