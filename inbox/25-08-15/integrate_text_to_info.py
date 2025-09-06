# 생성 시간: Fri Aug 15 11:01:05 KST 2025
# 핵심 내용: 노드 텍스트 문서를 노드 정보 문서에 통합하는 간단한 스크립트
# 상세 내용:
#   - load_nodes() (line 20): JSON 파일에서 노드 데이터 로드
#   - find_text_document() (line 30): 텍스트 문서 파일 찾기
#   - update_info_file() (line 40): 정보 파일에 텍스트 내용 통합
#   - main() (line 70): 메인 실행 함수
# 상태: 활성
# 주소: integrate_text_to_info
# 참조: node_data_updater (핵심 기능 추출)

#!/usr/bin/env python3

import json
import os
from pathlib import Path

def load_nodes(json_path: str) -> list:
    """JSON 파일에서 노드 데이터를 로드합니다."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        print(f"✅ {len(nodes)}개 노드 로드 완료")
        return nodes
    except Exception as e:
        print(f"❌ 노드 파일 로드 실패: {e}")
        return []

def find_text_document(directory: str) -> str:
    """텍스트 문서 파일을 찾습니다 (md 파일 중 _info.md가 아닌 것)."""
    for file in os.listdir(directory):
        if file.endswith('.md') and not file.endswith('_info.md'):
            return os.path.join(directory, file)
    return None

def update_info_file(info_file: str, text_content: str) -> bool:
    """정보 파일에 텍스트 내용을 통합합니다."""
    try:
        # 기존 info 파일 읽기
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # '# 내용' 섹션 찾기
        lines = content.split('\n')
        content_section_idx = -1
        
        for i, line in enumerate(lines):
            if line.strip() == '# 내용':
                content_section_idx = i
                break
        
        if content_section_idx == -1:
            print(f"⚠️ '# 내용' 섹션을 찾을 수 없음: {os.path.basename(info_file)}")
            return False
        
        # 내용 섹션에 구분선과 텍스트 추가
        new_lines = lines[:content_section_idx + 1]
        new_lines.append('---')  # 구분선
        new_lines.append(text_content.strip())
        
        # 다른 섹션이 있으면 유지
        for i in range(content_section_idx + 1, len(lines)):
            if lines[i].strip().startswith('# ') and lines[i].strip() != '# 내용':
                new_lines.extend(['', ''] + lines[i:])
                break
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ 텍스트 통합 완료: {os.path.basename(info_file)}")
        return True
        
    except Exception as e:
        print(f"❌ 파일 처리 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    # 작업 디렉토리
    work_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-15"
    
    print("🚀 텍스트-정보 파일 통합 시작")
    print("=" * 50)
    
    # 1. 노드 데이터 로드
    json_path = os.path.join(work_dir, "node.json")
    nodes = load_nodes(json_path)
    if not nodes:
        print("❌ 노드 데이터가 없습니다.")
        return
    
    # 2. 텍스트 문서 찾기
    text_file = find_text_document(work_dir)
    if not text_file:
        print("❌ 텍스트 문서를 찾을 수 없습니다.")
        return
    
    print(f"📄 텍스트 문서: {os.path.basename(text_file)}")
    
    # 3. 텍스트 내용 읽기
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        print(f"📝 텍스트 길이: {len(text_content)} 문자")
    except Exception as e:
        print(f"❌ 텍스트 파일 읽기 실패: {e}")
        return
    
    # 4. info 파일 찾기 및 업데이트
    info_files = [f for f in os.listdir(work_dir) if f.endswith('_info.md')]
    
    if not info_files:
        print("❌ 정보 파일을 찾을 수 없습니다.")
        return
    
    print(f"📋 정보 파일: {len(info_files)}개")
    
    success_count = 0
    for info_file in info_files:
        info_path = os.path.join(work_dir, info_file)
        if update_info_file(info_path, text_content):
            success_count += 1
    
    print(f"\n✅ 통합 완료: {success_count}/{len(info_files)}개 성공")

if __name__ == "__main__":
    main()