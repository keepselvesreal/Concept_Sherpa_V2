#!/bin/bash

# 생성 시간: 2025-08-25 10:45 KST
# 핵심 내용: 세션 파일의 마지막 interaction에 모델 응답 누적 저장
# 상세 내용:
#   - extract_agent_response() (라인 15-45): transcript 파일에서 모델 응답 추출
#   - update_session_with_response() (라인 47-65): 세션 파일의 해당 query에 응답 업데이트
#   - main logic (라인 67-95): 임시 파일 정보 기반 세션 파일 업데이트
# 상태: active
# 주소: log-session-response
# 참조: 글로벌 훅 /home/nadle/resources/Claude_Code/Hooks/log-agent-response.sh 참조

# Knowledge Sherpa v2 프로젝트 세션별 모델 응답 로깅 훅
# 기존 세션 파일의 마지막 interaction에 모델 응답을 추가

# Claude Code에서 전달되는 JSON 데이터 읽기
HOOK_DATA=$(cat)

# transcript 파일에서 모델 응답 추출
extract_agent_response() {
    local transcript_path="$1"
    
    if [ ! -f "$transcript_path" ] || [ ! -r "$transcript_path" ]; then
        echo "Response could not be captured - transcript file not accessible"
        return
    fi
    
    # transcript 파일에서 마지막 사용자 prompt 이후의 모든 assistant 응답을 추출
    local agent_response=$(cat "$transcript_path" | jq -s -c '
        . as $data | 
        ([range(length) | select($data[.].type == "user" and ($data[.].message.content | type) == "string")] | last) as $last_user_idx |
        # 그 이후의 모든 assistant 응답에서 텍스트만 추출하여 결합
        [$data[($last_user_idx + 1):] | .[] | select(.type == "assistant") | 
         .message.content[]? | select(.type == "text") | .text] | join("\n\n")
    ' 2>/dev/null)
    
    # 추출 실패 시 기본 메시지
    if [ $? -ne 0 ] || [ -z "$agent_response" ] || [ "$agent_response" = '""' ]; then
        echo "Response could not be captured"
    else
        # JSON 문자열에서 실제 텍스트 추출
        echo "$agent_response" | jq -r '.' 2>/dev/null || echo "Response could not be captured"
    fi
}

# 세션 파일의 마지막 conversation에 응답 업데이트
update_session_with_response() {
    local session_file="$1"
    local query_number="$2"
    local model_response="$3"
    local timestamp="$4"
    
    jq --arg query_number "$query_number" \
       --arg model_response "$model_response" \
       --arg timestamp "$timestamp" \
       '.conversations |= map(
         if .query_number == ($query_number | tonumber) then
           .answer = $model_response |
           .response_timestamp = $timestamp
         else . end
       )' "$session_file" > "${session_file}.tmp" && mv "${session_file}.tmp" "$session_file"
}

# jq를 사용해서 필요한 정보 추출
SESSION_ID=$(echo "$HOOK_DATA" | jq -r '.session_id // "unknown"')
TRANSCRIPT_PATH=$(echo "$HOOK_DATA" | jq -r '.transcript_path // ""')

# 임시 파일에서 세션 정보 읽기
TEMP_SESSION_FILE="/tmp/claude_session_local_${SESSION_ID}.json"

if [ ! -f "$TEMP_SESSION_FILE" ]; then
    echo "[$(date)] Local Response Hook Error: 임시 세션 파일 없음" >> /tmp/claude_hook_debug.log
    exit 1
fi

# 임시 파일에서 정보 추출
SESSION_FILE=$(jq -r '.session_file' "$TEMP_SESSION_FILE")
QUERY_NUMBER=$(jq -r '.query_number' "$TEMP_SESSION_FILE")

if [ ! -f "$SESSION_FILE" ]; then
    echo "[$(date)] Local Response Hook Error: 세션 파일 없음: $SESSION_FILE" >> /tmp/claude_hook_debug.log
    exit 1
fi

# transcript에서 모델 응답 추출
MODEL_RESPONSE=$(extract_agent_response "$TRANSCRIPT_PATH")

# 타임스탬프 생성
TIMESTAMP_KST=$(TZ='Asia/Seoul' date +"%Y-%m-%dT%H:%M:%S%z")

# 세션 파일 업데이트
update_session_with_response "$SESSION_FILE" "$QUERY_NUMBER" "$MODEL_RESPONSE" "$TIMESTAMP_KST"

# 디버깅 로그
echo "[$(date)] Local Response Hook: Updated $SESSION_FILE (query #$QUERY_NUMBER)" >> /tmp/claude_hook_debug.log

# 임시 파일 정리
rm -f "$TEMP_SESSION_FILE"

exit 0