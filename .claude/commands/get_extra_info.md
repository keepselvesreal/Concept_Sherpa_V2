---
description: 사용자 질의에 대한 개별 참조 문서 응답 생성
argument-hint: [사용자 질의]
allowed-tools: Bash(python query_processor.py:*)
---

사용자 질의: "$ARGUMENTS"

uv로 @25-08-25/query_processor.py를 백그라운드에서 실행해 사용자 질문과 참조 문서 폴더 경로(@25-08-25/references)를 전달해 각 참조 문서에 기반한 개별 응답이 생성되게 해줘

!cd /home/nadle/projects/Knowledge_Sherpa/v2/25-08-25 && python query_processor.py "$ARGUMENTS" "./references"