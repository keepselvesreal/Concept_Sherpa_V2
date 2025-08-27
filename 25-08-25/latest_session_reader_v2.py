# 생성 시간: 25-08-25 21:21:59
# 핵심 내용: 세션 캐시에서 최신 세션 폴더를 찾아 individual 파일들의 내용을 마크다운으로 예쁘게 출력하는 스크립트
# 상세 내용:
#   - load_session_id() (라인 14-23): .session_cache.json에서 session_id 추출
#   - find_latest_session_folder() (라인 25-42): 가장 최신 세션 폴더 검색
#   - read_individual_files() (라인 44-86): individual 파일들 순차 처리 및 마크다운 렌더링
#   - main() (라인 88-97): 메인 실행 함수
# 상태: active
# 주소: latest_session_reader/v2
# 참조: latest_session_reader (마크다운 렌더링 추가)

import json
import os
import glob
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

def load_session_id():
    """세션 캐시 파일에서 session_id 추출"""
    cache_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-25/.session_cache.json"
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('session_id')
    except (FileNotFoundError, json.JSONDecodeError) as e:
        console.print(f"❌ 세션 캐시 파일 읽기 오류: {e}", style="red")
        return None

def find_latest_session_folder(session_id):
    """가장 최신 세션 폴더 찾기"""
    if not session_id:
        return None
    
    base_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-25"
    session_prefix = session_id.split('-')[0]  # cb6a4622 추출
    
    # session_{prefix}_* 패턴으로 폴더 검색
    pattern = os.path.join(base_path, f"session_{session_prefix}_*")
    folders = glob.glob(pattern)
    
    if not folders:
        console.print(f"❌ session_{session_prefix}_* 패턴의 폴더를 찾을 수 없습니다.", style="red")
        return None
    
    # 시간 부분 추출하여 최신 폴더 찾기
    latest_folder = max(folders, key=lambda x: x.split('_')[-1])
    return latest_folder

def read_individual_files(folder_path):
    """individual_ 파일들 순차 처리"""
    if not os.path.exists(folder_path):
        console.print(f"❌ 폴더가 존재하지 않습니다: {folder_path}", style="red")
        return
    
    # individual_로 시작하는 파일들 찾기
    pattern = os.path.join(folder_path, "individual_*.json")
    files = sorted(glob.glob(pattern))  # 파일명 순으로 정렬
    
    if not files:
        console.print(f"❌ individual_ 파일들을 찾을 수 없습니다: {folder_path}", style="red")
        return
    
    # 파일 정보를 패널로 표시
    info_panel = Panel(
        f"📂 대상 폴더: {folder_path}\n📄 찾은 파일 개수: {len(files)}",
        title="📋 파일 정보",
        title_align="left", 
        border_style="bold green"
    )
    console.print(info_panel)
    
    # 메인 섹션 시작을 알리는 구분선
    console.print("\n" + "═" * 80, style="bold yellow")
    console.print("🎯 질의 및 응답 내용", style="bold yellow")
    console.print("═" * 80 + "\n", style="bold yellow")
    
    query_extracted = False
    
    for i, file_path in enumerate(files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_name = os.path.basename(file_path)
            
            # 첫 번째 파일에서만 query 추출
            if not query_extracted and 'query' in data:
                query_panel = Panel(
                    data['query'], 
                    title="🔍 질의 내용", 
                    title_align="left",
                    border_style="bold green"
                )
                console.print(query_panel)
                console.print()
                query_extracted = True
            
            # has_relevant_content가 true인 경우만 model_response 출력
            if data.get('has_relevant_content') == True and 'model_response' in data:
                # 파일명을 작게 표시 (덜 강조)
                console.print(f"📄 {file_name}", style="dim white")
                console.print()
                
                # 응답 내용을 강조된 패널로 표시
                response_panel = Panel(
                    Markdown(data['model_response']),
                    title="💬 응답 내용", 
                    title_align="left",
                    border_style="bold green",
                    padding=(1, 2)
                )
                console.print(response_panel)
                console.print("\n" + "─" * 80 + "\n")
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            console.print(f"❌ 파일 처리 오류 ({file_name}): {e}", style="red")

def main():
    """메인 실행 함수"""
    console.print("🚀 최신 세션 폴더 읽기 시작\n", style="bold yellow")
    
    session_id = load_session_id()
    if not session_id:
        return
    
    latest_folder = find_latest_session_folder(session_id)
    if not latest_folder:
        return
    
    read_individual_files(latest_folder)
    console.print("✅ 작업 완료", style="bold green")

if __name__ == "__main__":
    main()