"""
# 목차
- 생성 시간: 2025년 08월 24일 00:01:57 KST
- 핵심 내용: 이해 부족 분석 결과 JSON 파일을 원본 내용 그대로 유지하되 가독성만 개선하여 텍스트 파일로 저장하는 스크립트
- 상세 내용:
    - format_and_save_analysis 함수 (라인 16-65): JSON 파일을 읽어서 원본 내용 그대로 가독성만 개선하여 저장하는 함수
    - main 함수 (라인 67-73): 실행 가능한 메인 함수
- 상태: active
- 참조: format_analysis_result.py에서 원본 내용 보존 방식으로 개선
"""

import json
import sys
import re

def format_and_save_analysis(json_file_path, output_file_path):
    """JSON 파일을 읽어서 원본 내용 그대로 가독성만 개선하여 저장하는 함수"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append("이해 부족 분석 결과")
        output_lines.append("=" * 80)
        output_lines.append("")
        
        output_lines.append("previous_question:")
        output_lines.append(data['previous_question'])
        output_lines.append("")
        
        output_lines.append("previous_answer:")
        # \n을 실제 줄바꿈으로 변환
        prev_answer = data['previous_answer'].replace('\\n', '\n')
        output_lines.append(prev_answer)
        output_lines.append("")
        
        output_lines.append("current_question:")
        output_lines.append(data['current_question'])
        output_lines.append("")
        
        output_lines.append("analysis_response:")
        # analysis_response도 \n을 실제 줄바꿈으로 변환
        analysis_response = data['analysis_response'].replace('\\n', '\n')
        output_lines.append(analysis_response)
        output_lines.append("")
        
        output_lines.append("=" * 80)
        
        # 파일로 저장
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        
        print(f"가독성 개선된 결과가 저장되었습니다: {output_file_path}")
        
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON 파일 파싱 오류: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python3 format_analysis_result_v2.py <input_json_file> <output_txt_file>")
        sys.exit(1)
    
    format_and_save_analysis(sys.argv[1], sys.argv[2])