# -*- coding: utf-8 -*-
"""
생성 시간: 2025-08-22 16:38:04 KST
핵심 내용: Claude Code SDK 기본 동작 테스트용 간단한 스크립트
상세 내용:
    - main() (라인 18-30): 간단한 Claude 쿼리 테스트
상태: active
주소: simple_claude_test
참조: 없음
"""

import asyncio
import sys

try:
    from claude_code_sdk import query, ClaudeCodeOptions
except ImportError:
    print("❌ claude_code_sdk를 찾을 수 없습니다.")
    sys.exit(1)

async def main():
    """간단한 Claude 쿼리 테스트"""
    try:
        messages = []
        async for message in query(
            prompt="안녕하세요, Claude Haiku 3.5로 간단하게 인사말 하나 해주세요.",
            options=ClaudeCodeOptions(
                model="claude-3-haiku-20240307",
                max_turns=1
            )
        ):
            messages.append(message)
        
        if messages:
            print("✅ 성공!")
            print(messages[-1])
        else:
            print("❌ 응답을 받지 못했습니다.")
            
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    asyncio.run(main())