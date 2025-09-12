#!/bin/bash

# 간단한 테스트 훅 - 실행 확인용
echo "[$(date)] TEST HOOK EXECUTED!" >> /tmp/test_hook.log

# 전달받은 데이터도 기록
echo "Data received: $(cat)" >> /tmp/test_hook.log
echo "---" >> /tmp/test_hook.log

exit 0