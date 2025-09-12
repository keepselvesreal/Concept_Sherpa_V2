# 생성 시간: Wed Sep 10 09:54:08 KST 2025
# 핵심 내용: WorkspacePreparationStage 결과 시뮬레이션 함수
# 상세 내용:
#   - simulate_workspace_preparation (라인 18-75): workspace_result.json 데이터로 원래 파일/폴더 구조 재현
#   - create_chapter_folder_structure (라인 77-115): 장별 폴더 및 파일 생성
#   - save_chapter_toc_json (라인 117-135): 장 목차 JSON 파일 저장
#   - save_chapter_content_md (라인 137-155): 장 내용 마크다운 파일 저장 (제목, 생성일시, 내용만 포함)
# 상태: active

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# 💡 정규화 함수 import 추가
from refactoring.src.utils.text_utils import normalize_title


def simulate_workspace_preparation(workspace_result_path: str, output_base_path: str) -> Dict[str, Any]:
    """
    workspace_result.json 데이터를 사용하여 원래 워크스페이스 준비 단계 결과 재현
    
    Args:
        workspace_result_path: workspace_result.json 파일 경로
        output_base_path: 시뮬레이션 결과를 저장할 기본 경로
        
    Returns:
        Dict: 시뮬레이션 결과 정보
        
    생성 구조:
    output_base_path/
    └── {normalized_book_title}/
        ├── chapter_01/
        │   ├── toc.json
        │   └── content.md
        ├── chapter_02/
        │   ├── toc.json
        │   └── content.md
        └── ...
    """
    
    try:
        # workspace_result.json 데이터 로드
        with open(workspace_result_path, 'r', encoding='utf-8') as f:
            workspace_data = json.load(f)
            
        if not workspace_data.get('success'):
            return {
                'success': False,
                'error': f"workspace_result.json 데이터가 성공 상태가 아닙니다: {workspace_data.get('error')}"
            }
            
        data = workspace_data['data']
        book_metadata = data['book_metadata']
        chapters_data = data['chapters_data']
        
        # 기존에 저장된 normalized_title 사용
        normalized_title = book_metadata['normalized_title']
        book_folder = Path(output_base_path) / normalized_title
        book_folder.mkdir(parents=True, exist_ok=True)
        
        # 책 전체 목차 저장 (book_toc.json)
        book_toc_result = save_book_toc_json(book_folder, data)
        
        # 각 장별 폴더 및 파일 생성
        created_chapters = []
        for idx, chapter_data in enumerate(chapters_data, 1):
            # 🔥 정규화된 장 제목으로 폴더명 생성 (기존: chapter_01 형태)
            chapter_title = chapter_data.get('chapter_title', f'Chapter_{idx}')
            chapter_folder_name = normalize_title(chapter_title)
            
            chapter_result = create_chapter_folder_structure(
                book_folder, 
                chapter_folder_name, 
                chapter_data
            )
            created_chapters.append(chapter_result)
            
        return {
            'success': True,
            'data': {
                'book_title': book_metadata['title'],
                'normalized_title': normalized_title,
                'book_folder': str(book_folder),
                'total_chapters': len(chapters_data),
                'created_chapters': created_chapters,
                'simulation_time': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"시뮬레이션 실행 중 오류 발생: {str(e)}"
        }


def create_chapter_folder_structure(book_folder: Path, chapter_folder_name: str, chapter_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    장별 폴더 구조 생성 (toc.json, content.md)
    
    Args:
        book_folder: 책 폴더 경로
        chapter_folder_name: 장 폴더명 (예: chapter_01)
        chapter_data: 장 데이터 (chapter_title, chapter_toc, content_text, metadata)
        
    Returns:
        Dict: 생성된 장 정보
    """
    try:
        # 장 폴더 생성
        chapter_folder = book_folder / chapter_folder_name
        chapter_folder.mkdir(exist_ok=True)
        
        # chapter_toc.json 파일 생성
        toc_result = save_chapter_toc_json(chapter_folder, chapter_data)
        
        # content.md 파일 생성  
        content_result = save_chapter_content_md(chapter_folder, chapter_data)
        
        return {
            'success': True,
            'chapter_folder': str(chapter_folder),
            'chapter_title': chapter_data['chapter_title'],
            'toc_file': toc_result,
            'content_file': content_result,
            'toc_items_count': len(chapter_data.get('chapter_toc', [])),
            'content_length': len(chapter_data.get('content_text', ''))
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"장 폴더 생성 실패 ({chapter_folder_name}): {str(e)}"
        }


def save_book_toc_json(book_folder: Path, workspace_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    책 전체 목차 JSON 파일 저장 (book_toc.json)
    
    Args:
        book_folder: 책 폴더 경로
        workspace_data: 전체 워크스페이스 데이터 (raw_toc_data 포함)
        
    Returns:
        Dict: 저장 결과 정보
    """
    try:
        book_toc_file = book_folder / "book_toc.json"
        raw_toc_data = workspace_data.get('raw_toc_data', {})
        
        book_toc_data = {
            'book_metadata': workspace_data.get('book_metadata', {}),
            'toc_structure': raw_toc_data.get('toc_structure', []),
            'extraction_info': raw_toc_data.get('extraction_info', {}),
            'generated_at': datetime.now().isoformat()
        }
        
        with open(book_toc_file, 'w', encoding='utf-8') as f:
            json.dump(book_toc_data, f, ensure_ascii=False, indent=2)
            
        return {
            'success': True,
            'file_path': str(book_toc_file),
            'file_size': book_toc_file.stat().st_size,
            'toc_items_count': len(raw_toc_data.get('toc_structure', []))
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Book TOC JSON 저장 실패: {str(e)}"
        }


def save_chapter_toc_json(chapter_folder: Path, chapter_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    장 목차 JSON 파일 저장 (chapter_toc.json)
    
    Args:
        chapter_folder: 장 폴더 경로
        chapter_data: 장 데이터
        
    Returns:
        Dict: 저장 결과 정보
    """
    try:
        toc_file = chapter_folder / "chapter_toc.json"
        toc_data = {
            'chapter_title': chapter_data['chapter_title'],
            'chapter_toc': chapter_data.get('chapter_toc', []),
            'metadata': chapter_data.get('metadata', {}),
            'generated_at': datetime.now().isoformat()
        }
        
        with open(toc_file, 'w', encoding='utf-8') as f:
            json.dump(toc_data, f, ensure_ascii=False, indent=2)
            
        return {
            'success': True,
            'file_path': str(toc_file),
            'file_size': toc_file.stat().st_size
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"TOC JSON 저장 실패: {str(e)}"
        }


def save_chapter_content_md(chapter_folder: Path, chapter_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    장 내용 마크다운 파일 저장 (장 제목, 생성일시, 내용만 포함)
    
    Args:
        chapter_folder: 장 폴더 경로  
        chapter_data: 장 데이터
        
    Returns:
        Dict: 저장 결과 정보
    """
    try:
        content_file = chapter_folder / "content.md"
        
        # 마크다운 형식으로 내용 구성 (제목, 생성일시, 내용만)
        md_content = f"""# {chapter_data['chapter_title']}
(생성일시: {datetime.now().isoformat()})

{chapter_data.get('content_text', '내용이 없습니다.')}
"""
        
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        return {
            'success': True,
            'file_path': str(content_file),
            'file_size': content_file.stat().st_size
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Content MD 저장 실패: {str(e)}"
        }


if __name__ == "__main__":
    """모듈 직접 실행 시 시뮬레이션 수행"""
    import sys
    
    if len(sys.argv) >= 3:
        workspace_result_path = sys.argv[1]
        output_base_path = sys.argv[2]
    else:
        # 기본 경로 사용
        workspace_result_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/workspace_preparation/workspace_result.json"
        output_base_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/simulations"
    
    print("🔄 WorkspacePreparation 시뮬레이션 시작...")
    print(f"📁 입력: {workspace_result_path}")
    print(f"📂 출력: {output_base_path}")
    
    # 시뮬레이션 실행
    result = simulate_workspace_preparation(workspace_result_path, output_base_path)
    
    if result['success']:
        print("\n✅ 시뮬레이션 성공!")
        print(f"📖 책 제목: {result['data']['book_title']}")
        print(f"📁 정규화된 제목: {result['data']['normalized_title']}")
        print(f"📂 책 폴더: {result['data']['book_folder']}")
        print(f"📋 총 챕터 수: {result['data']['total_chapters']}")
        print(f"⏰ 시뮬레이션 시간: {result['data']['simulation_time']}")
        
        # 생성된 파일들 확인
        book_folder = Path(result['data']['book_folder'])
        if book_folder.exists():
            # 🔥 정규화된 장 제목 폴더 찾기 (기존: chapter_ prefix 찾기)
            chapter_folders = [f for f in book_folder.iterdir() if f.is_dir() and f.name != 'book_toc.json']
            print(f"\n📂 생성된 챕터 폴더: {len(chapter_folders)}개")
            
            # 책 전체 목차 확인
            book_toc_file = book_folder / "book_toc.json"
            if book_toc_file.exists():
                size_kb = round(book_toc_file.stat().st_size / 1024, 1)
                print(f"📖 book_toc.json: {size_kb}KB")
            
            # 처음 3개 챕터 확인
            for chapter_folder in sorted(chapter_folders)[:3]:
                print(f"  🔍 {chapter_folder.name}:")
                
                chapter_toc_file = chapter_folder / "chapter_toc.json"
                content_file = chapter_folder / "content.md"
                
                if chapter_toc_file.exists():
                    size_kb = round(chapter_toc_file.stat().st_size / 1024, 1)
                    print(f"    - chapter_toc.json: {size_kb}KB")
                if content_file.exists():
                    size_kb = round(content_file.stat().st_size / 1024, 1)
                    print(f"    - content.md: {size_kb}KB")
                    
            if len(chapter_folders) > 3:
                print(f"  ... 및 {len(chapter_folders) - 3}개 추가 챕터")
                
        print(f"\n🎯 시뮬레이션 완료!")
        
    else:
        print("\n❌ 시뮬레이션 실패:")
        print(result['error'])