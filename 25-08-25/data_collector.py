# 생성 시간: 25-08-25 21:46:29
# 핵심 내용: individual 파일에서 질의문과 model_response 수집, chat-logs에서 동일 질의의 answer 수집하여 반환하는 스크립트
# 상세 내용:
#   - load_session_id() (라인 15-24): .session_cache.json에서 session_id 추출
#   - collect_individual_data() (라인 26-65): individual 파일들에서 질의문과 응답들 수집
#   - find_chat_log_answer() (라인 67-88): chat-logs에서 매칭되는 질의의 answer 찾기
#   - main() (라인 90-130): 메인 실행 함수 및 결과 출력
# 상태: active
# 주소: data_collector
# 참조: 신규 생성

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
    cache_file = ".session_cache.json"
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('session_id')
    except (FileNotFoundError, json.JSONDecodeError) as e:
        console.print(f"❌ 세션 캐시 파일 읽기 오류: {e}", style="red")
        return None

def collect_individual_data(base_path, session_id):
    """individual 파일들에서 질의문과 응답들 수집"""
    session_prefix = session_id.split('-')[0]
    
    # 최신 세션 폴더 찾기
    pattern = os.path.join(base_path, f"session_{session_prefix}_*")
    folders = glob.glob(pattern)
    
    if not folders:
        console.print(f"❌ session_{session_prefix}_* 폴더를 찾을 수 없습니다.", style="red")
        return None, None
    
    latest_folder = max(folders, key=lambda x: x.split('_')[-1])
    console.print(f"📂 대상 폴더: {latest_folder}", style="dim cyan")
    
    # individual 파일들 처리
    pattern = os.path.join(latest_folder, "individual_*.json")
    files = sorted(glob.glob(pattern))
    
    if not files:
        console.print(f"❌ individual_ 파일들을 찾을 수 없습니다.", style="red")
        return None, None
    
    console.print(f"📄 찾은 파일 개수: {len(files)}", style="dim cyan")
    
    query = None
    responses = []
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 첫 번째 파일에서 질의문 추출
            if query is None and 'query' in data:
                query = data['query']
            
            # has_relevant_content가 true인 경우만 응답 수집
            if data.get('has_relevant_content') == True and 'model_response' in data:
                file_name = os.path.basename(file_path)
                responses.append(data['model_response'])
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            console.print(f"❌ 파일 처리 오류: {e}", style="red")
    
    return query, responses

def find_chat_log_answer(base_path, session_id, query):
    """chat-logs에서 매칭되는 질의의 answer 찾기"""
    session_prefix = session_id.split('-')[0]
    chat_log_file = os.path.join(base_path, "chat-logs", f"session_{session_prefix}.json")
    
    if not os.path.exists(chat_log_file):
        console.print(f"⚠️  chat-log 파일을 찾을 수 없습니다: session_{session_prefix}.json", style="yellow")
        return None
    
    try:
        with open(chat_log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversations = data.get('conversations', [])
        
        for conversation in conversations:
            if conversation.get('query') == query and 'answer' in conversation:
                return conversation['answer']
                
    except (json.JSONDecodeError, FileNotFoundError) as e:
        console.print(f"❌ chat-log 파일 처리 오류: {e}", style="red")
    
    return None

def main():
    """메인 실행 함수"""
    console.print("🚀 데이터 수집기 시작\n", style="bold yellow")
    
    base_path = os.getcwd()
    session_id = load_session_id()
    if not session_id:
        return
    
    # Individual 데이터 수집
    console.print("📄 Individual 파일들에서 데이터 수집 중...", style="cyan")
    query, individual_responses = collect_individual_data(base_path, session_id)
    
    if not query:
        console.print("❌ 질의문을 찾을 수 없습니다.", style="red")
        return
    
    # Chat-log 답변 찾기
    console.print("💬 Chat-log에서 기존 답변 찾는 중...\n", style="cyan")
    chat_log_answer = find_chat_log_answer(base_path, session_id, query)
    
    # 결과 출력
    console.print("═" * 80, style="bold yellow")
    console.print("📊 수집된 데이터", style="bold yellow")
    console.print("═" * 80 + "\n", style="bold yellow")
    
    # 질의문 출력
    query_panel = Panel(query, title="🔍 질의 내용", border_style="bold green")
    console.print(query_panel)
    console.print()
    
    # Individual responses 출력
    if individual_responses:
        combined_responses = "\n\n".join(individual_responses)
        individual_panel = Panel(
            Markdown(combined_responses),
            title=f"📄 Individual 응답들 ({len(individual_responses)}개)", 
            border_style="bold green",
            padding=(1, 2)
        )
        console.print(individual_panel)
        console.print()
    
    # Chat-log answer 출력
    if chat_log_answer:
        chatlog_panel = Panel(
            Markdown(chat_log_answer),
            title="💬 Chat-log 기존 답변", 
            border_style="bold green",
            padding=(1, 2)
        )
        console.print(chatlog_panel)
    else:
        console.print("ℹ️  Chat-log에서 해당 질의에 대한 답변을 찾지 못했습니다.", style="dim yellow")
    
    console.print(f"\n✅ 데이터 수집 완료", style="bold green")

if __name__ == "__main__":
    main()