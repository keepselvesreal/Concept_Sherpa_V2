import asyncio
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

async def test():
    try:
        prompt = "안녕하세요"
        print(f"프롬프트: '{prompt}'")
        
        options = ClaudeCodeOptions(max_turns=1)
        
        responses = []
        async for message in query(prompt=prompt, options=options):
            print(f"메시지 타입: {type(message)}")
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        responses.append(block.text)
                        print(f"응답: {block.text}")
        
        print(f"총 응답 수: {len(responses)}")
        
    except Exception as e:
        print(f"오류: {e}")
        print(f"오류 타입: {type(e)}")
        import traceback
        traceback.print_exc()

asyncio.run(test())