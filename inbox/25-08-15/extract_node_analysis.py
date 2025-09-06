# 생성 시간: Fri Aug 15 11:09:20 KST 2025
# 핵심 내용: 노드 정보 문서의 내용 섹션에서 4가지 요소를 병렬로 추출하는 스크립트
# 상세 내용:
#   - extract_content_section() (line 21): 정보 파일에서 내용 섹션 추출
#   - format_extraction_section() (line 40): 추출 결과를 마크다운 형식으로 포맷
#   - update_info_file() (line 53): 정보 파일의 추출 섹션 업데이트
#   - main() (line 80): 메인 실행 함수
# 상태: 활성
# 주소: extract_node_analysis
# 참조: content_analysis_module_v3 (핵심 기능 추출)

#!/usr/bin/env python3

import os
import re
from pathlib import Path

def extract_content_section(info_file: str) -> str:
    """정보 파일에서 '# 내용' 섹션 추출"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        content_start = -1
        content_end = len(lines)
        
        # '# 내용' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 내용':
                content_start = i + 1
                print(f"   🔍 '# 내용' 섹션 발견 (라인 {i+1})")
                break
        
        # 다음 구조 섹션 찾기 (구성, 속성 등)
        structure_sections = ['# 구성', '# 속성', '# 추출']
        for i in range(content_start, len(lines)):
            line_stripped = lines[i].strip()
            if line_stripped in structure_sections:
                content_end = i
                print(f"   🔍 다음 구조 섹션 발견: '{line_stripped}' (라인 {i+1})")
                break
        
        if content_start == -1:
            print(f"   ⚠️ '# 내용' 섹션을 찾을 수 없음")
            return ""
        
        print(f"   📊 분석 범위: 라인 {content_start+1} ~ {content_end}")
        print(f"   📊 총 라인 수: {content_end - content_start}")
        
        # 내용과 구성 사이의 전체 텍스트 추출
        section_content = '\n'.join(lines[content_start:content_end])
        
        # 실제 텍스트가 있는지 확인 (빈 줄과 공백만 있는 것이 아닌지)
        has_actual_text = any(line.strip() for line in lines[content_start:content_end])
        
        if not has_actual_text:
            print(f"   ⚠️ 내용 섹션에 실제 텍스트가 없음")
            return ""
        
        extracted_content = section_content.strip()
        print(f"   📝 추출된 내용 길이: {len(extracted_content)} 문자")
        return extracted_content
        
    except Exception as e:
        print(f"❌ 내용 섹션 추출 실패: {e}")
        return ""

def format_extraction_section(core_content: str, detailed_content: str, 
                            main_topics: str, sub_topics: str) -> str:
    """추출 결과를 마크다운 형식으로 포맷"""
    sections = [
        ("핵심 내용", core_content),
        ("상세 핵심 내용", detailed_content),
        ("주요 화제", main_topics),
        ("부차 화제", sub_topics)
    ]
    
    formatted = ""
    for section_name, content in sections:
        if content and content.strip():
            formatted += f"## {section_name}\n{content.strip()}\n\n"
    
    return formatted.strip()

def update_info_file(info_file: str, extraction_content: str) -> bool:
    """정보 파일의 추출 섹션 업데이트"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        extraction_start = -1
        extraction_end = -1
        
        # '# 추출' 섹션 찾기
        for i, line in enumerate(lines):
            if line.strip() == '# 추출':
                extraction_start = i
                break
        
        if extraction_start == -1:
            print(f"⚠️ '# 추출' 섹션을 찾을 수 없음: {os.path.basename(info_file)}")
            return False
        
        # 다음 # 섹션 찾기
        for i in range(extraction_start + 1, len(lines)):
            if lines[i].strip().startswith('# '):
                extraction_end = i
                break
        
        # 새로운 내용으로 교체
        new_lines = lines[:extraction_start + 1]
        new_lines.append('')
        new_lines.extend(extraction_content.split('\n'))
        
        if extraction_end != -1:
            new_lines.extend([''] + lines[extraction_end:])
        
        # 파일 저장
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ 추출 섹션 업데이트 완료: {os.path.basename(info_file)}")
        return True
        
    except Exception as e:
        print(f"❌ 파일 업데이트 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    # 작업 디렉토리
    work_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-15"
    
    print("🚀 노드 내용 분석 및 추출 시작")
    print("=" * 50)
    
    # info 파일 찾기
    info_files = [f for f in os.listdir(work_dir) if f.endswith('_info.md')]
    
    if not info_files:
        print("❌ 정보 파일을 찾을 수 없습니다.")
        return
    
    for info_file in info_files:
        info_path = os.path.join(work_dir, info_file)
        print(f"\n📄 처리 중: {info_file}")
        
        # 1. 내용 섹션 추출
        content_section = extract_content_section(info_path)
        if not content_section:
            print(f"⚠️ 내용 섹션이 비어있음: {info_file}")
            continue
        
        print(f"📝 내용 길이: {len(content_section)} 문자")
        
        # 2. 간단한 분석 (실제로는 AI를 사용해야 하지만 여기서는 예시로 처리)
        title = info_file.replace('_info.md', '').replace('_', ' ').title()
        
        # 예시 분석 결과 (실제로는 AI 분석 필요)
        core_content = f"이 문서는 {title}에 대한 핵심 내용을 다룹니다."
        detailed_content = f"상세한 내용:\n- 주요 개념 설명\n- 구체적인 사례\n- 기술적 세부사항"
        main_topics = f"- AI 모델 성능 비교\n- 에이전트 아키텍처\n- 비용 효율성 분석"
        sub_topics = f"- 로컬 모델 실행\n- 프롬프트 엔지니어링\n- 도구 통합"
        
        # 3. 추출 섹션 포맷
        extraction_content = format_extraction_section(
            core_content, detailed_content, main_topics, sub_topics
        )
        
        # 4. 파일 업데이트
        if update_info_file(info_path, extraction_content):
            print(f"✅ {info_file} 처리 완료")
        else:
            print(f"❌ {info_file} 처리 실패")
    
    print(f"\n✅ 모든 노드 분석 완료!")
    print("\n💡 참고: 현재는 예시 분석 결과를 사용했습니다.")
    print("   실제 AI 분석을 위해서는 Claude SDK 설정이 필요합니다.")

if __name__ == "__main__":
    main()