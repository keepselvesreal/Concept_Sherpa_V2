# 생성 시간: Thu Sep  4 15:40:04 KST 2025
# 핵심 내용: 텍스트 처리 유틸리티 함수들
# 상세 내용:
#   - normalize_title (라인 10-20): 제목 정규화 (특수문자 제거 및 언더스코어 변환)
# 상태: active

import re

def normalize_title(title: str) -> str:
    """
    제목 정규화 함수 - 특수문자 제거 및 언더스코어 변환
    
    Args:
        title: 정규화할 제목
        
    Returns:
        str: 파일명으로 사용 가능한 정규화된 제목
    """
    title_clean = re.sub(r'[^\w\s.-]', '', title)  # 점(.)도 유지
    title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
    return title_clean