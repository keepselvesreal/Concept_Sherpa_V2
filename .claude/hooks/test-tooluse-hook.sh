#!/bin/bash

# PostToolUse 테스트 훅 - 프로젝트 훅 도구 사용 확인용
echo "[$(date)] 🔧 PROJECT PostToolUse HOOK 실행됨!" >> /tmp/project_tooluse_test.log

# 전달받은 도구 사용 데이터 기록
echo "Tool Data: $(cat)" >> /tmp/project_tooluse_test.log
echo "====================" >> /tmp/project_tooluse_test.log

exit 0