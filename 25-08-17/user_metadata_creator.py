# 생성 시간: 2025-08-17 17:38:23 KST
# 핵심 내용: 사용자로부터 메타데이터 입력을 받아 JSON 파일을 생성하는 모듈
# 상세 내용:
#   - get_user_metadata_input 함수 (라인 15-60): 사용자로부터 메타데이터 입력 받기
#   - create_metadata_json_file 함수 (라인 62-75): 메타데이터 JSON 파일 생성
# 상태: 활성
# 주소: user_metadata_creator
# 참조: 없음

import json
import os
from typing import Dict


def get_default_metadata() -> Dict[str, str]:
    """기본 메타데이터 반환"""
    return {
        "source_type": "youtube",
        "structure_type": "standalone", 
        "document_language": "korean"
    }


def get_user_metadata_input() -> Dict[str, str]:
    """사용자로부터 메타데이터 입력 받기"""
    print("\n📝 문서 메타데이터 입력:")
    
    # source_type 선택
    source_options = ["book", "post", "docs", "youtube"]
    print(f"Source Type 선택: {', '.join(f'{i+1}.{opt}' for i, opt in enumerate(source_options))}")
    while True:
        try:
            choice = int(input("번호를 선택하세요 (1-4): ")) - 1
            if 0 <= choice < len(source_options):
                source_type = source_options[choice]
                break
            else:
                print("❌ 올바른 번호를 선택하세요 (1-4)")
        except ValueError:
            print("❌ 숫자를 입력하세요")
    
    # structure_type 선택  
    structure_options = ["component", "standalone"]
    print(f"\nStructure Type 선택: {', '.join(f'{i+1}.{opt}' for i, opt in enumerate(structure_options))}")
    while True:
        try:
            choice = int(input("번호를 선택하세요 (1-2): ")) - 1
            if 0 <= choice < len(structure_options):
                structure_type = structure_options[choice]
                break
            else:
                print("❌ 올바른 번호를 선택하세요 (1-2)")
        except ValueError:
            print("❌ 숫자를 입력하세요")
    
    # document_language 입력
    document_language = input("\nDocument Language를 입력하세요 (예: korean, english, mixed): ").strip()
    if not document_language:
        document_language = "english"  # 기본값
    
    return {
        "source_type": source_type,
        "structure_type": structure_type, 
        "document_language": document_language
    }


def create_user_input_template(output_dir: str) -> bool:
    """사용자가 직접 값을 입력할 수 있는 템플릿 파일 생성"""
    try:
        template_path = os.path.join(output_dir, "user_input_metadata.json")
        
        template_content = {
            "_instructions": {
                "source_type": "선택 가능: book, post, docs, youtube",
                "structure_type": "선택 가능: component, standalone",
                "document_language": "선택 가능: korean, english, mixed, japanese, chinese"
            },
            "source_type": "",
            "structure_type": "",
            "document_language": ""
        }
        
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template_content, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 사용자 입력 템플릿 파일 생성: user_input_metadata.json")
        print(f"📝 이 파일을 수정하여 메타데이터를 설정하세요.")
        return True
    except Exception as e:
        print(f"❌ 사용자 입력 템플릿 파일 생성 실패: {e}")
        return False

def create_metadata_json_file(metadata: Dict[str, str], output_dir: str) -> bool:
    """메타데이터 JSON 파일 생성"""
    try:
        metadata_path = os.path.join(output_dir, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"✅ 메타데이터 파일 생성: metadata.json")
        return True
    except Exception as e:
        print(f"❌ 메타데이터 파일 생성 실패: {e}")
        return False


if __name__ == "__main__":
    # 직접 실행 시 테스트
    metadata = get_user_metadata_input()
    print(f"\n📋 입력된 메타데이터:")
    for key, value in metadata.items():
        print(f"   {key}: {value}")
    
    test_output = "test_metadata_output"
    os.makedirs(test_output, exist_ok=True)
    create_metadata_json_file(metadata, test_output)