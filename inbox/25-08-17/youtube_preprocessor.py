# 생성 시간: 2025-08-17 17:38:23 KST
# 핵심 내용: 유튜브 스크립트 전처리 모듈 - Claude SDK를 이용해 프롬프트와 스크립트를 받아 정리된 문서를 생성
# 상세 내용:
#   - YoutubePreprocessor 클래스 (라인 20-115): 유튜브 스크립트 전처리 기능
#   - load_prompt 메서드 (라인 25-35): 프롬프트 파일 로드
#   - load_script 메서드 (라인 37-47): 스크립트 파일 로드
#   - process_with_claude 메서드 (라인 49-75): Claude SDK를 이용한 스크립트 전처리
#   - split_and_save_documents 메서드 (라인 78-112): 한국어/원문 2개 파일로 분리 저장
#   - main 함수 (라인 115-140): CLI 인터페이스
# 상태: 활성
# 주소: youtube_preprocessor
# 참조: 없음

import asyncio
import argparse
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions


class YoutubePreprocessor:
    def load_prompt(self, prompt_path: str) -> str:
        """프롬프트 파일을 로드"""
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"프롬프트 파일을 찾을 수 없습니다: {prompt_path}")
    
    def load_script(self, script_path: str) -> str:
        """스크립트 파일을 로드"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"스크립트 파일을 찾을 수 없습니다: {script_path}")

    async def process_with_claude(self, prompt_template: str, script_content: str) -> str:
        """Claude SDK를 이용해 스크립트 전처리"""
        # 프롬프트에 스크립트 내용 삽입
        final_prompt = prompt_template.replace('{script_content}', script_content)
        
        print("🚀 Claude SDK를 이용한 스크립트 전처리 시작...")
        
        try:
            messages = []
            async for message in query(
                prompt=final_prompt,
                options=ClaudeCodeOptions(
                    max_turns=1,
                    system_prompt="유튜브 스크립트 전처리 전문가. 주어진 규칙에 따라 스크립트를 정리하고 구조화하세요.",
                    allowed_tools=[]
                )
            ):
                messages.append(message)
            
            # 응답에서 텍스트 내용 추출
            result = self._extract_content_from_messages(messages)
            print("✅ Claude SDK 전처리 완료")
            return result
            
        except Exception as e:
            print(f"❌ Claude SDK 전처리 실패: {e}")
            return f"전처리 실패: {str(e)}"
    
    def _extract_content_from_messages(self, messages) -> str:
        """메시지에서 텍스트 내용 추출"""
        content = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                else:
                    content += str(message.content)
        return content.strip()
    
    def split_and_save_documents(self, result: str, base_output_path: str):
        """결과를 한국어/원문 2개 파일로 분리하여 저장"""
        base_name = Path(base_output_path).stem
        base_dir = Path(base_output_path).parent
        
        # 구분자로 문서 분리
        documents = result.split('---')
        
        if len(documents) >= 2:
            # 한국어 번역본 저장
            korean_path = base_dir / f"{base_name}_korean.md"
            korean_content = documents[0].strip()
            # "# 문서 1: 한국어 번역본" 헤더 제거
            if korean_content.startswith('# 문서 1: 한국어 번역본'):
                korean_content = '\n'.join(korean_content.split('\n')[2:]).strip()
            
            with open(korean_path, 'w', encoding='utf-8') as f:
                f.write(korean_content)
            print(f"✅ 한국어 번역본 저장: {korean_path}")
            
            # 원문 버전 저장
            original_path = base_dir / f"{base_name}_original.md"
            original_content = documents[1].strip()
            # "# 문서 2: 원문 유지 버전" 헤더 제거
            if original_content.startswith('# 문서 2: 원문 유지 버전'):
                original_content = '\n'.join(original_content.split('\n')[2:]).strip()
            
            with open(original_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"✅ 원문 버전 저장: {original_path}")
        else:
            # 분리 실패시 전체 내용을 하나의 파일로 저장
            with open(base_output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"⚠️ 문서 분리 실패, 전체 내용 저장: {base_output_path}")


async def main():
    parser = argparse.ArgumentParser(description='유튜브 스크립트 전처리 도구 (Claude SDK 사용)')
    parser.add_argument('prompt_path', help='프롬프트 파일 경로')
    parser.add_argument('script_path', help='스크립트 파일 경로')
    parser.add_argument('-o', '--output', help='출력 파일 경로', 
                       default='/home/nadle/projects/Concept_Sherpa_V2/25-08-17/processed_script.md')
    
    args = parser.parse_args()
    
    preprocessor = YoutubePreprocessor()
    try:
        # 파일 로드
        prompt_template = preprocessor.load_prompt(args.prompt_path)
        script_content = preprocessor.load_script(args.script_path)
        
        # Claude SDK로 전처리
        result = await preprocessor.process_with_claude(prompt_template, script_content)
        
        # 결과를 2개 파일로 분리하여 저장
        preprocessor.split_and_save_documents(result, args.output)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    asyncio.run(main())