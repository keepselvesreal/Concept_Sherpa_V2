"""
생성 시간: 2025-08-27 17:28 KST
핵심 내용: 마크다운 파일에서 제목 추출 및 폴더명 생성 유틸리티
상세 내용:
    - extract_title_from_md(md_content): 첫 번째 # 헤더에서 제목 추출 (라인 25-45)
    - create_safe_folder_name(title): 폴더명으로 안전한 문자열 생성 (라인 47-75)
    - truncate_title_to_limit(title, limit=40): 40글자 제한으로 제목 자르기 (라인 77-95)
    - sanitize_filename(text): 폴더/파일명 안전 문자만 유지 (라인 97-115)
    - generate_post_folder_name(md_content): Post_{날짜}/{제목} 형태 폴더명 생성 (라인 117-140)
상태: active
주소: title_extractor
참조: 신규 생성
"""

import re
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


def extract_title_from_md(md_content: str) -> Optional[str]:
    """마크다운 내용에서 첫 번째 # 헤더 제목 추출"""
    lines = md_content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        # 첫 번째 레벨 1 헤더만 찾기
        if line.startswith('# ') and not line.startswith('## '):
            # '# ' 제거하고 제목 추출
            title = line[2:].strip()
            if title:
                return title
    
    return None


def sanitize_filename(text: str) -> str:
    """폴더/파일명으로 사용할 수 없는 문자 제거"""
    # Windows/Linux/macOS에서 폴더명으로 사용할 수 없는 문자들 제거
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    # 잘못된 문자를 빈 문자열로 치환
    clean_text = re.sub(invalid_chars, '', text)
    
    # 연속된 공백을 하나로 줄이기
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    # 앞뒤 공백 제거
    return clean_text.strip()


def truncate_title_to_limit(title: str, limit: int = 40) -> str:
    """제목을 단어 단위로 잘라서 40글자 제한"""
    if not title:
        return ""
    
    # 공백 기준으로 단어 분할
    words = title.split()
    result_words = []
    
    for word in words:
        # 하이픈을 포함한 예상 길이 계산
        # (기존 결과) + (하이픈, 첫 번째가 아닌 경우) + (새 단어)
        if result_words:
            expected_length = len('-'.join(result_words)) + 1 + len(word)  # +1은 하이픈
        else:
            expected_length = len(word)
        
        if expected_length > limit:
            break
            
        result_words.append(word)
    
    return '-'.join(result_words)


def create_safe_folder_name(title: str) -> str:
    """폴더명으로 안전한 문자열 생성"""
    # 1단계: 폴더명으로 안전한 문자만 유지
    clean_title = sanitize_filename(title)
    
    # 2단계: 40글자 제한으로 자르기
    truncated_title = truncate_title_to_limit(clean_title, limit=40)
    
    return truncated_title


def generate_post_folder_name(md_content: str) -> Tuple[str, Optional[str]]:
    """Post_{날짜}/{제목} 형태의 폴더명 생성
    
    Returns:
        Tuple[str, Optional[str]]: (전체_폴더_경로, 추출된_제목)
        제목을 찾을 수 없으면 (None, None) 반환
    """
    # 제목 추출
    title = extract_title_from_md(md_content)
    if not title:
        return None, None
    
    # 날짜 생성 (YYMMDD 형식)
    today = datetime.now()
    date_str = today.strftime("%y%m%d")
    
    # 안전한 폴더명 생성
    safe_title = create_safe_folder_name(title)
    if not safe_title:
        return None, None
    
    # 전체 경로 생성
    folder_path = f"Post_{date_str}/{safe_title}"
    
    return folder_path, title


def check_folder_exists(base_path: Path, folder_path: str) -> bool:
    """폴더가 이미 존재하는지 확인"""
    full_path = base_path / folder_path
    return full_path.exists()


if __name__ == "__main__":
    # 테스트 코드 - test_sample.md 파일로 테스트
    test_file = Path("test_sample.md")
    if test_file.exists():
        with open(test_file, 'r', encoding='utf-8') as f:
            test_content = f.read()
    else:
        test_content = """
# AI 코딩의 미래와 개발자 역할 변화

이것은 테스트 내용입니다.
"""
    
    folder_path, title = generate_post_folder_name(test_content)
    print(f"원본 제목: {title}")
    print(f"제목 길이: {len(title)}글자")
    
    safe_title = create_safe_folder_name(title)
    print(f"안전한 제목: {safe_title}")
    print(f"안전한 제목 길이: {len(safe_title)}글자")
    print(f"생성된 폴더 경로: {folder_path}")