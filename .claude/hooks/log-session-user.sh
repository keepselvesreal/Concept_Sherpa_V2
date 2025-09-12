#!/bin/bash

# 생성 시간: 2025-08-25 10:42 KST
# 핵심 내용: 프로젝트별 동적 작업 폴더 감지하여 세션별 누적 사용자 입력 로깅
# 상세 내용:
#   - get_work_dir_from_cwd() (라인 15-30): 현재 작업 디렉토리에서 작업 폴더 추출
#   - get_or_create_session_file() (라인 32-55): 세션 파일 생성 또는 기존 파일 경로 반환
#   - main logging logic (라인 57-95): 사용자 입력을 세션 파일에 누적 저장
# 상태: active
# 주소: log-session-user
# 참조: 글로벌 훅 /home/nadle/resources/Claude_Code/Hooks/log-user-input.sh 참조

# Knowledge Sherpa v2 프로젝트 세션별 사용자 입력 로깅 훅
# 동적 작업 폴더 감지하여 {work_dir}/chat-logs/ 에 세션별 JSON 파일로 누적 저장

# Claude Code에서 전달되는 JSON 데이터 읽기
HOOK_DATA=$(cat)

# jq를 사용해서 현재 작업 디렉토리와 세션 정보 추출
CWD=$(echo "$HOOK_DATA" | jq -r '.cwd // ""')
SESSION_ID=$(echo "$HOOK_DATA" | jq -r '.session_id // "unknown"')
USER_PROMPT=$(echo "$HOOK_DATA" | jq -r '.prompt // ""')

# 현재 작업 디렉토리에서 작업 폴더명 추출 (예: /path/to/25-08-25 -> 25-08-25)
get_work_dir_from_cwd() {
    local cwd="$1"
    # Knowledge_Sherpa/v2/ 이후의 경로에서 첫 번째 디렉토리 추출
    if [[ "$cwd" == *"Knowledge_Sherpa/v2/"* ]]; then
        # v2/ 이후 부분 추출
        local after_v2="${cwd#*Knowledge_Sherpa/v2/}"
        # 첫 번째 슬래시까지 또는 전체 문자열 (슬래시가 없으면)
        local work_dir="${after_v2%%/*}"
        echo "$work_dir"
    else
        # Knowledge_Sherpa/v2/ 패턴이 없으면 현재 디렉토리명만 반환
        basename "$cwd"
    fi
}

# 세션 파일 생성 또는 기존 파일 경로 반환
get_or_create_session_file() {
    local session_id="$1"
    local log_dir="$2"
    
    # 세션 ID에서 앞 8자리 추출
    local session_prefix=$(echo "$session_id" | cut -c1-8)
    
    # 기존 세션 파일 찾기
    local existing_file=$(find "$log_dir" -name "session_${session_prefix}*.json" 2>/dev/null | head -1)
    
    if [ -n "$existing_file" ]; then
        echo "$existing_file"
    else
        # 새 세션 파일 생성
        local new_file="${log_dir}/session_${session_prefix}.json"
        local timestamp_kst=$(TZ='Asia/Seoul' date +"%Y-%m-%dT%H:%M:%S%z")
        
        # 초기 세션 구조 생성
        jq -n \
          --arg session_id "$session_id" \
          --arg created_at "$timestamp_kst" \
          '{
            session_id: $session_id,
            created_at: $created_at,
            conversations: []
          }' > "$new_file"
        
        echo "$new_file"
    fi
}

# 작업 폴더 추출
WORK_DIR=$(get_work_dir_from_cwd "$CWD")

# 로그 디렉토리 설정 및 생성 
PROJECT_ROOT="/home/nadle/projects/Knowledge_Sherpa/v2"
LOG_DIR="${PROJECT_ROOT}/${WORK_DIR}/chat-logs"
mkdir -p "$LOG_DIR"

# 세션 파일 경로 확인/생성
SESSION_FILE=$(get_or_create_session_file "$SESSION_ID" "$LOG_DIR")

# 타임스탬프 생성
TIMESTAMP_KST=$(TZ='Asia/Seoul' date +"%Y-%m-%dT%H:%M:%S%z")

# 현재 파일의 conversations 배열 길이 확인 (query_number용)
QUERY_NUMBER=$(jq '.conversations | length' "$SESSION_FILE" 2>/dev/null || echo "0")
QUERY_NUMBER=$((QUERY_NUMBER + 1))

# 사용자 입력을 세션 파일의 conversations 배열에 추가
jq --arg query_number "$QUERY_NUMBER" \
   --arg timestamp "$TIMESTAMP_KST" \
   --arg query "$USER_PROMPT" \
   '.conversations += [{
     query_number: ($query_number | tonumber),
     timestamp: $timestamp,
     query: $query,
     answer: null
   }]' "$SESSION_FILE" > "${SESSION_FILE}.tmp" && mv "${SESSION_FILE}.tmp" "$SESSION_FILE"

# 세션 정보를 임시 파일에 저장 (응답 훅에서 사용)
echo "{
  \"session_file\": \"$SESSION_FILE\",
  \"query_number\": $QUERY_NUMBER,
  \"session_id\": \"$SESSION_ID\"
}" > "/tmp/claude_session_local_${SESSION_ID}.json"

# 디버깅 로그
echo "[$(date)] Local User Hook: $SESSION_FILE (query #$QUERY_NUMBER)" >> /tmp/claude_hook_debug.log

exit 0