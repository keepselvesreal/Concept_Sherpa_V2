# 생성 시간: Fri Sep 12 20:08:41 KST 2025
# 핵심 내용: ContentProcessingStage 전용 유틸리티 함수 모음
# 상세 내용:
#   - extract_level_from_filename (라인 30-38): 파일명에서 레벨 추출 (경로 지원)
#   - parse_extraction_response (라인 40-94): AI 응답을 5개 섹션으로 파싱
#   - format_composition_info (라인 96-113): 구성 정보 포맷팅
#   - clean_section_content (라인 115-127): 섹션 내용 정리
#   - find_matching_document (라인 129-141): 문서 매칭 찾기
#   - extract_title_from_content (라인 143-155): 메모리 콘텐츠에서 제목 추출
#   - extract_content_section_from_full_content (라인 157-167): # 내용 섹션만 추출
#   - parse_composition_files_from_content (라인 169-185): 구성 파일들 추출
#   - update_extraction_section_in_content (라인 187-205): 메모리 내용에서 추출 섹션 업데이트
#   - add_update_status_mark_to_content (라인 207-217): 메모리 내용에 상태 마킹 추가
# 상태: active

import os
import re
import logging
from typing import Dict, List, Optional

# 로거 설정
logger = logging.getLogger(__name__)

def extract_level_from_filename(filename: str) -> int:
    """
    파일명에서 level 추출 (경로 포함 파일명 지원)
    
    Args:
        filename: 파일명 또는 경로 포함 파일명
        
    Returns:
        int: 레벨 번호 (찾지 못하면 0)
    """
    # 경로에서 파일명만 추출
    base_filename = os.path.basename(filename)
    level_match = re.search(r'lev(\d+)', base_filename)
    return int(level_match.group(1)) if level_match else 0

def parse_extraction_response(response: str) -> Dict[str, str]:
    """
    AI 응답을 5개 섹션으로 파싱 (engines_v5.py 로직 활용)
    
    Args:
        response: AI 응답 텍스트
        
    Returns:
        Dict: 5개 섹션별 내용
    """
    sections = {
        'core_content': '',
        'detailed_core_content': '',
        'detailed_content': '',
        'main_topics': '',
        'sub_topics': ''
    }
    
    # 섹션 헤더 매핑 (engines_v5.py와 동일)
    section_headers = {
        '## 핵심 내용': 'core_content',
        '## 상세 핵심 내용': 'detailed_core_content', 
        '## 상세 정보': 'detailed_content',
        '## 주요 화제': 'main_topics',
        '## 부차 화제': 'sub_topics'
    }
    
    lines = response.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 섹션 헤더 확인
        if line_stripped in section_headers:
            # 이전 섹션 저장 (헤더 포함)
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # 새 섹션 시작 (헤더부터 시작)
            current_section = section_headers[line_stripped]
            current_content = [line_stripped]  # 헤더 포함
        elif current_section and line.strip():  # 빈 줄이 아닌 경우만 추가
            current_content.append(line)
        elif current_section and not line.strip() and current_content:  # 빈 줄도 포함 (단, 시작이 아닌 경우)
            current_content.append(line)
    
    # 마지막 섹션 저장
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

def format_composition_info(composition_files: List[str]) -> str:
    """
    구성 정보를 마크다운 형식으로 포맷팅
    
    Args:
        composition_files: 구성 파일 목록
        
    Returns:
        str: 포맷된 구성 정보
    """
    if not composition_files:
        return "구성 파일이 없습니다."
    
    formatted_files = []
    for file in composition_files:
        if file.strip() and not file.startswith('---'):
            formatted_files.append(f"- {file}")
    
    return '\n'.join(formatted_files) if formatted_files else "구성 파일이 없습니다."

def clean_section_content(content: str) -> str:
    """
    섹션 내용에서 불필요한 구분선 제거 및 정리
    
    Args:
        content: 원본 섹션 내용
        
    Returns:
        str: 정리된 내용
    """
    if not content:
        return content
    
    # 연속된 구분선 제거
    cleaned = re.sub(r'-{3,}', '', content)
    # 연속된 빈 줄 제거
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    
    return cleaned.strip()

def find_matching_document(documents: List[Dict], file_name: str) -> Optional[Dict]:
    """
    파일명으로 문서 찾기
    
    Args:
        documents: 문서 리스트
        file_name: 찾을 파일명
        
    Returns:
        Optional[Dict]: 매칭된 문서 (없으면 None)
    """
    for doc in documents:
        if doc.get('file_name') == file_name:
            return doc
    return None

def extract_title_from_content(content: str) -> str:
    """
    메모리 콘텐츠에서 제목 추출 (# 내용 섹션의 첫 번째 헤더에서)
    
    Args:
        content: 전체 통합 문서 내용
        
    Returns:
        str: 추출된 제목
    """
    content_match = re.search(r'# 내용\n---\n(.*?)(?=\n---|\n#|$)', content, re.DOTALL)
    if content_match:
        lines = content_match.group(1).split('\n')
        for line in lines:
            if line.strip() and line.startswith('#'):
                return line.replace('#', '').strip()
    return "Unknown Title"

def extract_content_section_from_full_content(full_content: str) -> str:
    """
    전체 내용에서 # 내용 섹션만 추출
    
    Args:
        full_content: 전체 통합 문서 내용
        
    Returns:
        str: # 내용 섹션 내용
    """
    content_match = re.search(r'# 내용\n---\n(.*?)(?=\n# 구성\n---|$)', full_content, re.DOTALL)
    return content_match.group(1).strip() if content_match else ""

def parse_composition_files_from_content(content: str) -> List[str]:
    """
    전체 내용에서 구성 파일들 추출
    
    Args:
        content: 전체 통합 문서 내용
        
    Returns:
        List[str]: 구성 파일명들
    """
    composition_match = re.search(r'# 구성\n---\n(.*?)$', content, re.DOTALL)
    if composition_match:
        composition_section = composition_match.group(1).strip()
        if composition_section and composition_section != '---':
            return [line.strip() for line in composition_section.split('\n') 
                   if line.strip() and not line.startswith('---')]
    return []

def update_extraction_section_in_content(original_content: str, new_extraction_content: str) -> str:
    """
    메모리 내용에서 추출 섹션 업데이트
    
    Args:
        original_content: 원본 내용
        new_extraction_content: 새로운 추출 섹션 내용
        
    Returns:
        str: 업데이트된 내용
    """
    pattern = r'(# 추출\n---\n)(<[^>]+>\n)?(.*?)(?=\n# 내용\n---|$)'
    
    def replacement(match):
        header = match.group(1)  # # 추출\n---\n
        status_mark = match.group(2) if match.group(2) else ""  # 기존 상태 마킹
        return f"{header}{status_mark}{new_extraction_content}"
    
    return re.sub(pattern, replacement, original_content, flags=re.DOTALL)

def add_update_status_mark_to_content(content: str, status_mark: str) -> str:
    """
    메모리 내용에 상태 마킹 추가
    
    Args:
        content: 원본 내용
        status_mark: 추가할 상태 마킹 (예: "<구성 노드 반영 완료>")
        
    Returns:
        str: 상태 마킹이 추가된 내용
    """
    pattern = r'(# 추출\n---\n)(?!<)'  # 이미 마킹이 없는 경우만
    replacement = f'\\1{status_mark}\n'
    return re.sub(pattern, replacement, content)

def format_extraction_content(extraction_result: Dict[str, str]) -> str:
    """
    추출 결과를 마크다운 형식으로 포맷팅
    
    Args:
        extraction_result: 5개 섹션별 추출 내용
        
    Returns:
        str: 포맷된 마크다운 내용
    """
    if not extraction_result:
        return ""
    
    formatted_parts = []
    
    # 섹션 순서대로 포맷팅
    section_keys = ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']
    
    for key in section_keys:
        if key in extraction_result and extraction_result[key].strip():
            formatted_parts.append(extraction_result[key])
            formatted_parts.append("")  # 섹션 간 빈 줄
    
    return "\n".join(formatted_parts)

def build_extraction_prompt(content: str, title: str) -> str:
    """
    추출용 프롬프트 생성
    
    Args:
        content: 문서 내용
        title: 문서 제목
        
    Returns:
        str: AI 추출용 프롬프트
    """
    return f"""다음 문서에서 5가지 정보를 순서대로 추출해주세요.

문서 제목: {title}
문서 내용:
{content}

다음 순서로 각 정보를 추출하고, 반드시 다음 형식을 정확히 지켜서 출력해주세요:

## 핵심 내용
문서의 핵심 내용을 2-3문장으로 간결하게 요약

## 상세 핵심 내용
주요 개념과 중요한 세부사항을 포함하여 5-7문장으로 정리

## 상세 정보
문서의 모든 중요한 정보를 빠뜨리지 않고 체계적으로 정리

## 주요 화제
문서에서 다루는 핵심 주제들을 불렛 포인트로 나열

## 부차 화제
주요 주제 외에 언급되는 부차적인 주제들을 불렛 포인트로 나열

**중요 규칙**: 
1. 각 섹션 제목(## 핵심 내용, ## 상세 핵심 내용 등)을 한 번만 출력하고 바로 다음 줄에 내용을 작성하세요.
2. 빈 헤더 라인을 출력하지 마세요.
3. 섹션 내용을 작성할 때 헤더가 필요한 경우에는 반드시 ### (해시 3개) 이상의 헤더만 사용하세요.
4. ## 헤더는 섹션 제목과 구분하기 위해 절대 중복 사용하지 마세요."""

def get_system_prompt() -> str:
    """
    시스템 프롬프트 반환
    
    Returns:
        str: AI 시스템 프롬프트
    """
    return """문서 분석 전문가. 주어진 5가지 정보 타입을 순서대로 정확하게 추출하세요.
- 핵심 내용: 간결하고 정확한 요약
- 상세 핵심 내용: 상세하면서도 핵심적인 내용
- 상세 정보: 체계적이고 포괄적인 정리
- 주요 화제: 핵심 주제들
- 부차 화제: 부차적이지만 의미있는 주제들

정확한 형식을 지켜서 출력하세요."""

def update_file_extraction_section(file_path: str, formatted_content: str) -> bool:
    """
    파일의 추출 섹션 업데이트
    
    Args:
        file_path: 업데이트할 파일 경로
        formatted_content: 포맷된 추출 내용
        
    Returns:
        bool: 업데이트 성공 여부
    """
    if not formatted_content.strip():
        logger.warning(f"⚠️ 업데이트할 내용이 비어있음: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 추출 섹션 패턴 찾기
        extraction_pattern = r'(# 추출\n---\n)(.*?)(?=\n# 내용|$)'
        
        if re.search(extraction_pattern, content, re.DOTALL):
            # 기존 추출 섹션 업데이트
            new_content = re.sub(
                extraction_pattern,
                f'\\1{formatted_content}\n',
                content,
                flags=re.DOTALL
            )
        else:
            # 추출 섹션이 없으면 # 내용 앞에 추가
            content_pattern = r'(\n# 내용)'
            if re.search(content_pattern, content):
                new_content = re.sub(
                    content_pattern,
                    f'\n# 추출\n---\n{formatted_content}\n\\1',
                    content
                )
            else:
                # # 내용 섹션도 없으면 끝에 추가
                new_content = content + f'\n\n# 추출\n---\n{formatted_content}\n'
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logger.info(f"✅ 추출 섹션 업데이트 완료: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ 추출 섹션 업데이트 실패: {file_path} - {e}")
        return False

def update_file_process_status(file_path: str, status: bool) -> bool:
    """
    파일의 process_status 업데이트
    
    Args:
        file_path: 업데이트할 파일 경로
        status: 설정할 상태 값
        
    Returns:
        bool: 업데이트 성공 여부
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        status_value = 'true' if status else 'false'
        
        # 속성 섹션이 있는지 확인
        attributes_pattern = r'(# 속성\n)(.*?)(?=\n# |$)'
        attributes_match = re.search(attributes_pattern, content, re.DOTALL)
        
        if attributes_match:
            # 기존 속성 섹션 업데이트
            attributes_content = attributes_match.group(2)
            
            # process_status가 이미 있는지 확인
            if 'process_status:' in attributes_content:
                # 기존 process_status 값 업데이트
                updated_attributes = re.sub(
                    r'process_status:\s*(true|false)',
                    f'process_status: {status_value}',
                    attributes_content
                )
            else:
                # process_status 추가
                updated_attributes = attributes_content.strip() + f'\nprocess_status: {status_value}'
            
            new_content = re.sub(
                attributes_pattern,
                f'\\1{updated_attributes}\n',
                content,
                flags=re.DOTALL
            )
        else:
            # 속성 섹션이 없으면 추가 (# 내용 앞에)
            content_pattern = r'(\n# 내용)'
            if re.search(content_pattern, content):
                new_content = re.sub(
                    content_pattern,
                    f'\n# 속성\n---\nprocess_status: {status_value}\n\\1',
                    content
                )
            else:
                # # 내용 섹션도 없으면 파일 시작에 추가
                new_content = f'# 속성\n---\nprocess_status: {status_value}\n\n{content}'
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logger.info(f"✅ process_status 업데이트 완료: {file_path} -> {status_value}")
        return True
        
    except Exception as e:
        logger.error(f"❌ process_status 업데이트 실패: {file_path} - {e}")
        return False