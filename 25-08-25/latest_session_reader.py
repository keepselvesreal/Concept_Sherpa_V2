# 생성 시간: 25-08-25 21:21:59
# 핵심 내용: 세션 캐시에서 최신 세션 폴더를 찾아 individual 파일들의 내용을 조건부 출력하는 스크립트
# 상세 내용:
#   - load_session_id() (라인 12-21): .session_cache.json에서 session_id 추출
#   - find_latest_session_folder() (라인 23-40): 가장 최신 세션 폴더 검색
#   - read_individual_files() (라인 42-74): individual 파일들 순차 처리 및 조건부 출력
#   - main() (라인 76-85): 메인 실행 함수
# 상태: active
# 주소: latest_session_reader
# 참조: 신규 생성

import json
import os
import glob
from pathlib import Path

def load_session_id():
    """세션 캐시 파일에서 session_id 추출"""
    cache_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-25/.session_cache.json"
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('session_id')
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ 세션 캐시 파일 읽기 오류: {e}")
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
        print(f"❌ session_{session_prefix}_* 패턴의 폴더를 찾을 수 없습니다.")
        return None
    
    # 시간 부분 추출하여 최신 폴더 찾기
    latest_folder = max(folders, key=lambda x: x.split('_')[-1])
    return latest_folder

def read_individual_files(folder_path):
    """individual_ 파일들 순차 처리"""
    if not os.path.exists(folder_path):
        print(f"❌ 폴더가 존재하지 않습니다: {folder_path}")
        return
    
    # individual_로 시작하는 파일들 찾기
    pattern = os.path.join(folder_path, "individual_*.json")
    files = sorted(glob.glob(pattern))  # 파일명 순으로 정렬
    
    if not files:
        print(f"❌ individual_ 파일들을 찾을 수 없습니다: {folder_path}")
        return
    
    print(f"📂 처리할 폴더: {folder_path}")
    print(f"📄 찾은 파일 개수: {len(files)}\n")
    
    query_extracted = False
    
    for i, file_path in enumerate(files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_name = os.path.basename(file_path)
            
            # 첫 번째 파일에서만 query 추출
            if not query_extracted and 'query' in data:
                print("🔍 질의 내용:")
                print(f"{data['query']}\n")
                print("="*80 + "\n")
                query_extracted = True
            
            # has_relevant_content가 true인 경우만 model_response 출력
            if data.get('has_relevant_content') == True and 'model_response' in data:
                print(f"📄 파일명: {file_name}")
                print(f"💬 응답 내용:")
                print(f"{data['model_response']}")
                print("\n" + "-"*60 + "\n")
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ 파일 처리 오류 ({file_name}): {e}")

def main():
    """메인 실행 함수"""
    print("🚀 최신 세션 폴더 읽기 시작\n")
    
    session_id = load_session_id()
    if not session_id:
        return
    
    latest_folder = find_latest_session_folder(session_id)
    if not latest_folder:
        return
    
    read_individual_files(latest_folder)
    print("✅ 작업 완료")

if __name__ == "__main__":
    main()