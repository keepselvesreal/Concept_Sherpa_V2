"""
# 목차
- 생성 시간: 2025년 08월 23일 23:59:33 KST
- 핵심 내용: 이해 부족 분석 결과 JSON 파일을 가독성 좋게 포맷팅하여 출력하는 스크립트
- 상세 내용:
    - format_analysis_result 함수 (라인 16-65): JSON 파일을 읽어서 가독성 좋게 포맷팅하는 메인 함수
    - main 함수 (라인 67-73): 실행 가능한 메인 함수
- 상태: active
- 참조: understanding_analysis_20250823_235251.json의 가독성 개선을 위해 생성
"""

import json
import sys
import re

def format_analysis_result(json_file_path):
    """JSON 파일을 읽어서 가독성 좋게 포맷팅하는 메인 함수"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("=" * 60)
        print("📊 DOP 이해 부족 분석 결과")
        print("=" * 60)
        
        print("\n📋 대화 컨텍스트")
        print("-" * 30)
        print(f"이전 질문: {data['previous_question']}")
        print(f"현재 질문: {data['current_question']}")
        
        print("\n📝 이전 답변")
        print("-" * 30)
        # \n을 실제 줄바꿈으로 변환
        prev_answer = data['previous_answer'].replace('\\n', '\n')
        print(prev_answer)
        
        print("\n🔍 분석 결과")
        print("-" * 30)
        
        # analysis_response에서 JSON 부분과 텍스트 부분 분리
        analysis_response = data['analysis_response']
        
        # JSON 부분 추출 (```json으로 시작하는 부분)
        json_match = re.search(r'```json\n(.*?)\n```', analysis_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            try:
                analysis_json = json.loads(json_str)
                
                print("\n⚠️  발견된 이해 부족 영역")
                print("-" * 30)
                
                for i, deficiency in enumerate(analysis_json['understanding_deficiencies'], 1):
                    category_map = {
                        'insufficient_details': '세부 설명 부족',
                        'lack_of_examples': '실무 예시 부족', 
                        'unclear_connections': '원리간 연관성 부족',
                        'unexplained_concepts': '미설명 개념'
                    }
                    
                    category_korean = category_map.get(deficiency['category'], deficiency['category'])
                    
                    print(f"\n{i}. {category_korean} ({deficiency['category']})")
                    print(f"   문제점: {deficiency['description']}")
                    print(f"   생성된 질문: \"{deficiency['generated_question']}\"")
            
            except json.JSONError as e:
                print(f"JSON 파싱 오류: {e}")
                print("원본 analysis_response:")
                print(analysis_response)
        
        # JSON 뒤의 텍스트 부분 (클로드의 추가 피드백)
        text_after_json = re.search(r'```.*?태수야,(.*)', analysis_response, re.DOTALL)
        if text_after_json:
            feedback_text = "태수야," + text_after_json.group(1)
            print(f"\n💡 클로드의 피드백")
            print("-" * 30)
            print(feedback_text.strip())
        
        print("\n" + "=" * 60)
        
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON 파일 파싱 오류: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 format_analysis_result.py <json_file_path>")
        sys.exit(1)
    
    format_analysis_result(sys.argv[1])