"""
생성 시간: 2025-08-15 16:09:50
핵심 내용: DocumentParser 클래스 테스트 스크립트
상세 내용:
    - parse_document 메서드 테스트
    - 섹션별 텍스트 추출 검증
    - 파싱 결과 출력 및 확인
상태: 
주소: test_parser
참조: neon_db_v2
"""

from neon_db_v2 import DocumentParser
import json

def main():
    # 테스트할 문서 경로
    test_file = "00_lev0_gpt_5_agentic_coding_with_claude_code_info.md"
    
    print("=== 문서 파싱 테스트 ===")
    print(f"대상 파일: {test_file}")
    
    try:
        # 문서 파싱
        result = DocumentParser.parse_document(test_file)
        
        # 결과 출력
        print(f"\n제목: {result['title']}")
        print(f"\n추출 정보 길이: {len(result['extracted_info'])} 문자")
        print(f"내용 길이: {len(result['content'])} 문자")
        print(f"구성 정보: {result['child_doc_ids']}")
        
        print(f"\n핵심 내용 길이: {len(result['core_content'])} 문자")
        print(f"상세 핵심 내용 길이: {len(result['detailed_core'])} 문자")
        print(f"주요 화제 길이: {len(result['main_topics'])} 문자")
        print(f"부차 화제 길이: {len(result['sub_topics'])} 문자")
        
        # 각 섹션 미리보기
        print("\n=== 섹션 미리보기 ===")
        
        print("\n핵심 내용:")
        print(result['core_content'][:200] + "..." if len(result['core_content']) > 200 else result['core_content'])
        
        print("\n상세 핵심 내용:")
        print(result['detailed_core'][:200] + "..." if len(result['detailed_core']) > 200 else result['detailed_core'])
        
        print("\n주요 화제:")
        print(result['main_topics'][:200] + "..." if len(result['main_topics']) > 200 else result['main_topics'])
        
        print("\n부차 화제:")
        print(result['sub_topics'][:200] + "..." if len(result['sub_topics']) > 200 else result['sub_topics'])
        
    except Exception as e:
        print(f"파싱 실패: {e}")

if __name__ == "__main__":
    main()