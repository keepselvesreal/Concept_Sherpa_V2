#!/usr/bin/env python3
"""
생성 시간: 2025년 8월 9일 15:20 KST
핵심 내용: 기존 마크다운 파일에서 Chapter 7 리프 노드 텍스트 추출 스크립트
상세 내용:
    - extract_text_by_boundaries(): 시작/종료 문자열 기반 텍스트 추출 함수
    - process_leaf_nodes(): 7장 리프 노드별 텍스트 추출 및 저장 함수  
    - create_extraction_report(): 추출 결과 검증 및 보고서 생성 함수
    - main(): 전체 실행 흐름 제어 함수
상태: 작성 완료
주소: chapter7_markdown_extractor
참조: chapter7_leaf_nodes_boundaries.json, Level01_7 Basic data validation.md
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

def load_markdown_text(file_path):
    """
    마크다운 파일에서 텍스트 로드
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 마크다운 파일 로드 실패: {e}")
        return ""

def load_leaf_nodes_boundaries(file_path):
    """
    리프 노드 경계 정보 로드
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # JSON 주석 제거
            json_start = content.find('[')
            return json.loads(content[json_start:])
    except Exception as e:
        print(f"❌ 경계 정보 파일 로드 실패: {e}")
        return []

def extract_text_by_boundaries(full_text, start_text, end_text, title=""):
    """
    시작/종료 문자열 기반으로 텍스트 추출
    
    Args:
        full_text: 전체 마크다운 텍스트
        start_text: 시작 문자열
        end_text: 종료 문자열
        title: 노드 제목 (로깅용)
    
    Returns:
        추출된 텍스트 또는 에러 메시지
    """
    try:
        print(f"  🔍 '{title}' 추출 중...")
        print(f"     시작: '{start_text}'")
        print(f"     종료: '{end_text}'")
        
        # 시작 위치 찾기
        start_idx = full_text.find(start_text)
        if start_idx == -1:
            # 대소문자 구분 없이 재검색
            start_pattern = re.escape(start_text).replace(r'\ ', r'\s+')
            start_match = re.search(start_pattern, full_text, re.IGNORECASE)
            if start_match:
                start_idx = start_match.start()
            else:
                error_msg = f"❌ 시작 문자열 '{start_text}' 찾을 수 없음"
                print(f"     {error_msg}")
                return f"ERROR: {error_msg}"
        
        # 종료 위치 찾기 (시작 위치 이후)
        search_text = full_text[start_idx:]
        end_idx = search_text.find(end_text)
        
        if end_idx == -1:
            # 대소문자 구분 없이 재검색
            end_pattern = re.escape(end_text).replace(r'\ ', r'\s+')
            end_match = re.search(end_pattern, search_text, re.IGNORECASE)
            if end_match:
                end_idx = end_match.end()
            else:
                # 종료 문자열을 찾지 못한 경우, 다음 섹션 시작까지 추출
                print(f"     ⚠️ 종료 문자열 '{end_text}' 찾을 수 없음, 다음 섹션까지 추출")
                
                # 다음 섹션 패턴들
                next_section_patterns = [
                    r'\n\d+\.\d+\s+[A-Z]',  # 7.1, 7.2 등
                    r'\nSummary\s*\n',
                    r'\n8\s+Introduction'
                ]
                
                for pattern in next_section_patterns:
                    next_match = re.search(pattern, search_text[100:])  # 100자 후부터 검색
                    if next_match:
                        end_idx = 100 + next_match.start()
                        print(f"     ✅ 다음 섹션에서 종료점 발견")
                        break
                
                if end_idx == -1:
                    # 최대 5000자까지만 추출
                    end_idx = min(5000, len(search_text))
                    print(f"     ⚠️ 최대 길이로 제한: {end_idx}자")
        else:
            end_idx += len(end_text)  # 종료 문자열 포함
        
        # 텍스트 추출
        extracted_text = search_text[:end_idx].strip()
        
        print(f"     ✅ 추출 완료: {len(extracted_text)}자")
        return extracted_text
        
    except Exception as e:
        error_msg = f"텍스트 추출 중 오류: {str(e)}"
        print(f"     ❌ {error_msg}")
        return f"ERROR: {error_msg}"

def clean_extracted_text(text):
    """
    추출된 텍스트 정리
    """
    if text.startswith("ERROR:"):
        return text
    
    # 페이지 표시 제거
    text = re.sub(r'=== 페이지 \d+ ===\n?', '', text)
    
    # 연속된 공백/줄바꿈 정리
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()

def save_extracted_text(node_info, extracted_text, output_dir):
    """
    추출된 텍스트를 파일로 저장
    """
    # 안전한 파일명 생성
    safe_title = re.sub(r'[^\w\s-]', '', node_info['title'])
    safe_title = re.sub(r'[-\s]+', '_', safe_title)
    filename = f"{node_info['id']:03d}_{safe_title}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 파일 내용 구성
    content = f"# {node_info['title']}\n\n"
    content += f"**ID:** {node_info['id']}\n"
    content += f"**Level:** {node_info['level']}\n"
    content += f"**추출 길이:** {len(extracted_text)} characters\n\n"
    content += "---\n\n"
    content += clean_extracted_text(extracted_text)
    
    # 파일 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def process_leaf_nodes():
    """
    7장 리프 노드별 텍스트 추출 및 저장
    """
    # 파일 경로 설정
    base_dir = Path('/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09')
    markdown_file = base_dir / 'extracted_texts' / 'Level01_7 Basic data validation.md'
    boundaries_file = base_dir / 'chapter7_leaf_nodes_boundaries.json'
    output_dir = base_dir / 'chapter7_leaf_texts'
    
    print("📚 Chapter 7 리프 노드 텍스트 추출 시작")
    print(f"📄 소스 파일: {markdown_file}")
    print(f"📋 경계 정보: {boundaries_file}")
    print(f"📁 출력 폴더: {output_dir}")
    
    # 출력 폴더 생성
    output_dir.mkdir(exist_ok=True)
    
    # 1. 마크다운 텍스트 로드
    full_text = load_markdown_text(markdown_file)
    if not full_text:
        return []
    
    print(f"✅ 마크다운 로드 완료: {len(full_text)}자")
    
    # 2. 리프 노드 경계 정보 로드
    leaf_nodes = load_leaf_nodes_boundaries(boundaries_file)
    if not leaf_nodes:
        return []
    
    print(f"✅ 리프 노드 {len(leaf_nodes)}개 로드")
    
    # 3. 각 리프 노드 텍스트 추출
    extraction_results = []
    
    for i, node in enumerate(leaf_nodes, 1):
        print(f"\n[{i}/{len(leaf_nodes)}] {node['title']} (ID: {node['id']})")
        
        # 텍스트 추출
        extracted_text = extract_text_by_boundaries(
            full_text, 
            node['start_text'], 
            node['end_text'],
            node['title']
        )
        
        # 파일 저장
        if not extracted_text.startswith("ERROR:"):
            filename = save_extracted_text(node, extracted_text, output_dir)
            status = "success"
            print(f"     💾 저장: {filename}")
        else:
            filename = ""
            status = "failed"
            print(f"     ❌ 저장 실패")
        
        # 결과 기록
        result = {
            'id': node['id'],
            'title': node['title'],
            'level': node['level'],
            'start_text': node['start_text'],
            'end_text': node['end_text'],
            'extracted_length': len(extracted_text) if not extracted_text.startswith("ERROR:") else 0,
            'filename': filename,
            'status': status,
            'error_message': extracted_text if extracted_text.startswith("ERROR:") else None
        }
        extraction_results.append(result)
    
    return extraction_results

def create_extraction_report(extraction_results):
    """
    추출 결과 보고서 생성
    """
    # 통계 계산
    total_nodes = len(extraction_results)
    successful = sum(1 for r in extraction_results if r['status'] == 'success')
    failed = total_nodes - successful
    total_chars = sum(r['extracted_length'] for r in extraction_results)
    
    # 보고서 데이터
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_nodes': total_nodes,
            'successful': successful,
            'failed': failed,
            'success_rate': f"{successful/total_nodes*100:.1f}%" if total_nodes > 0 else "0%",
            'total_extracted_chars': total_chars
        },
        'results': extraction_results
    }
    
    # JSON 보고서 저장
    report_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_extraction_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 텍스트 요약 저장
    summary_file = '/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_extraction_summary.md'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Chapter 7 텍스트 추출 결과 요약\n\n")
        f.write(f"**처리 시간:** {report['timestamp']}\n")
        f.write(f"**전체 노드:** {total_nodes}\n")
        f.write(f"**성공:** {successful}\n")
        f.write(f"**실패:** {failed}\n")
        f.write(f"**성공률:** {report['summary']['success_rate']}\n")
        f.write(f"**총 추출 문자수:** {total_chars:,}\n\n")
        
        f.write("## 추출 결과 상세\n\n")
        for result in extraction_results:
            status_icon = "✅" if result['status'] == 'success' else "❌"
            f.write(f"{status_icon} **{result['title']}** (ID: {result['id']})\n")
            f.write(f"   - 레벨: {result['level']}\n")
            if result['status'] == 'success':
                f.write(f"   - 파일: {result['filename']}\n")
                f.write(f"   - 길이: {result['extracted_length']:,} 문자\n")
            else:
                f.write(f"   - 오류: {result['error_message']}\n")
            f.write("\n")
    
    return report

def main():
    """
    전체 실행 흐름 제어
    """
    print("=== Chapter 7 리프 노드 텍스트 추출 ===\n")
    
    try:
        # 리프 노드 텍스트 추출
        extraction_results = process_leaf_nodes()
        
        if not extraction_results:
            print("❌ 추출할 데이터가 없습니다.")
            return False
        
        # 추출 결과 보고서 생성
        report = create_extraction_report(extraction_results)
        
        # 결과 요약 출력
        print("\n" + "="*50)
        print("📊 추출 완료 요약")
        print("="*50)
        print(f"전체 노드: {report['summary']['total_nodes']}")
        print(f"성공: {report['summary']['successful']}")
        print(f"실패: {report['summary']['failed']}")
        print(f"성공률: {report['summary']['success_rate']}")
        print(f"총 추출 문자수: {report['summary']['total_extracted_chars']:,}")
        
        if report['summary']['failed'] > 0:
            print(f"\n⚠️ {report['summary']['failed']}개 노드 추출 실패")
            print("상세 내용은 보고서를 확인하세요.")
        
        print(f"\n📄 보고서: chapter7_extraction_report.json")
        print(f"📄 요약: chapter7_extraction_summary.md")
        print(f"📁 추출 텍스트: chapter7_leaf_texts/")
        
        return True
        
    except Exception as e:
        print(f"❌ 스크립트 실행 중 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)