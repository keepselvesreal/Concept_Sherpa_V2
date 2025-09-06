"""
테스트용 conversation_module 사용 스크립트
"""
import asyncio
from conversation_module import ConversationModule
from prompt_loader import PromptLoader

async def test_conversation():
    # 프롬프트 로드
    prompt = PromptLoader.get_prompt("simple_prompt.txt")
    
    # 대화 모듈 초기화
    module = ConversationModule()
    
    # 첫 번째 질문
    print("=== 첫 번째 질문 처리 중 ===")
    result1 = await module.process_query(
        prompt=prompt,
        query="DOP의 핵심이 뭐야?",
        file_path="/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref.md"
    )
    print("첫 번째 결과:")
    print(result1)
    print("\n" + "="*50 + "\n")
    
    # 두 번째 질문
    print("=== 두 번째 질문 처리 중 ===")
    result2 = await module.process_query(
        prompt=prompt,
        query="왜 데이터를 수정하지 않고 새로운 데이터를 만드는 거야?",
        file_path="/home/nadle/projects/Concept_Sherpa_V2/25-08-23/ref.md"
    )
    print("두 번째 결과:")
    print(result2)

if __name__ == "__main__":
    asyncio.run(test_conversation())