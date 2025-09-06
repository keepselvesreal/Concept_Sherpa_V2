# 목차
# - 생성 시간: 2025-08-07 11:55:30 KST
# - 핵심 내용: Claude Code SDK 기본 동작 테스트 스크립트 - 35+12 계산 예제
# - 상세 내용:
#     - test_basic_calculation(1-20): 간단한 산술 연산을 Claude SDK로 처리하는 테스트
#     - main(22-35): 메인 실행 함수
# - 상태: 활성
# - 주소: claude_sdk_test
# - 참조: claude-code-sdk

import asyncio
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

async def test_basic_calculation():
    """35+12 계산을 Claude SDK로 테스트"""
    print("🧮 Claude Code SDK 기본 계산 테스트...")
    
    try:
        # 간단한 계산 요청
        prompt = "35 + 12는 얼마인가요? 숫자로만 답해주세요."
        
        print("Claude에게 요청 중...")
        
        # 옵션 설정
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="당신은 정확한 계산을 해주는 도우미입니다."
        )
        
        # 응답 처리
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
                        print(f"Claude 응답: {block.text}")
        
        if responses:
            print("✅ Claude SDK 정상 동작!")
            return True
        else:
            print("❌ 응답을 받지 못했습니다.")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print(f"오류 타입: {type(e)}")
        return False

async def main():
    """메인 실행 함수"""
    print("🚀 Claude Code SDK 테스트 시작...")
    
    # 기본 계산 테스트
    success = await test_basic_calculation()
    
    if success:
        print("\n🎉 Claude SDK 테스트 성공! 이제 본격적인 목차 분석 작업이 가능합니다.")
    else:
        print("\n💥 Claude SDK 테스트 실패. 설정을 확인해주세요.")

if __name__ == "__main__":
    asyncio.run(main())