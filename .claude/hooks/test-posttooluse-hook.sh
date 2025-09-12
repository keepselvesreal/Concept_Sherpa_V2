#!/bin/bash

# PostToolUse 테스트 훅 - 프로젝트 훅 동작 확인용
echo "[$(date)] PROJECT PostToolUse HOOK EXECUTED!" >> /tmp/project_hook_test.log

# 전달받은 데이터 기록
echo "PostToolUse Data: $(cat)" >> /tmp/project_hook_test.log
echo "---" >> /tmp/project_hook_test.log

exit 0