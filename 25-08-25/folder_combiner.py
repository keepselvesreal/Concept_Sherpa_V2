# 목차
# 생성 시간: Mon Aug 25 10:23:39 KST 2025
# 핵심 내용: 지정 폴더의 모든 MD 파일을 하나의 문자열로 결합하는 스크립트
# 상세 내용:
#   - combine_md_files(folder_path: str) -> str (12-47): 메인 함수로 MD 파일들을 구분자와 함께 결합
#   - main() (49-65): CLI 인터페이스 및 실행 예제
# 상태: active
# 주소: folder_combiner
# 참조: 

import os
from pathlib import Path
from typing import Optional

def combine_md_files(folder_path: str) -> str:
    """
    지정된 폴더의 모든 .md 파일을 하나의 문자열로 결합
    
    Args:
        folder_path: 대상 폴더 경로
        
    Returns:
        결합된 문자열 (파일별 구분자 포함)
    """
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"폴더가 존재하지 않습니다: {folder_path}")
    
    # .md 파일들만 찾기 (하위 폴더 제외)
    md_files = list(folder.glob("*.md"))
    
    if not md_files:
        return f"# {folder_path} 폴더에 MD 파일이 없습니다.\n"
    
    # 파일명 기준으로 정렬
    md_files.sort(key=lambda x: x.name.lower())
    
    combined_content = []
    
    for md_file in md_files:
        try:
            # 파일 구분 헤더
            separator = f"\n{'='*80}\n# 📁 파일: {md_file.name}\n{'='*80}\n"
            combined_content.append(separator)
            
            # 파일 내용 읽기
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                combined_content.append(content)
                
        except UnicodeDecodeError:
            # 인코딩 에러 시 다른 인코딩으로 시도
            try:
                with open(md_file, 'r', encoding='cp949') as f:
                    content = f.read()
                    combined_content.append(content)
            except Exception as e:
                error_msg = f"❌ 파일 읽기 실패: {e}\n"
                combined_content.append(error_msg)
        except Exception as e:
            error_msg = f"❌ 파일 처리 실패: {e}\n"
            combined_content.append(error_msg)
    
    return '\n'.join(combined_content)

def main():
    """CLI 실행 예제"""
    import sys
    
    if len(sys.argv) < 2:
        print("사용법: python folder_combiner.py <폴더_경로>")
        print("예시: python folder_combiner.py ./25-08-24")
        return
    
    folder_path = sys.argv[1]
    
    try:
        result = combine_md_files(folder_path)
        print(result)
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    main()