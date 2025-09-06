import asyncio
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

async def test_toc_analysis():
    try:
        # 매우 간단한 목차 분석 요청
        prompt = """다음 목차에서 Part 1과 Chapter 1 사이에 Introduction이 필요한지 분석해주세요:

Part 1: Flexibility (페이지 29-164)
1. Complexity of object-oriented programming (페이지 31)

Part 1은 29페이지, Chapter 1은 31페이지에서 시작합니다. 
29-30페이지에 내용이 있다면 "0 Introduction (페이지 29-30)"을 추가해야 합니다.

분석 결과를 알려주세요."""
        
        print(f"프롬프트 길이: {len(prompt)} 문자")
        
        options = ClaudeCodeOptions(
            max_turns=1,
            system_prompt="책 목차를 분석하는 전문가입니다."
        )
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
                        print(f"Claude 응답:\n{block.text}")
        
        return responses
        
    except Exception as e:
        print(f"오류: {e}")
        print(f"오류 타입: {type(e)}")
        import traceback
        traceback.print_exc()
        return []

async def main():
    print("🔍 목차 분석 테스트 시작...")
    responses = await test_toc_analysis()
    
    if responses:
        print(f"\n✅ 성공! {len(responses)}개 응답 받음")
    else:
        print("\n❌ 실패")

asyncio.run(main())