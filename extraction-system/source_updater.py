"""
생성 시간: 2025-08-27 16:56 KST
핵심 내용: source.md의 YAML front matter source 필드를 metadata.json의 source 필드에 삽입하는 스크립트
상세 내용:
    - main(): 메인 실행 함수, 파일 경로 처리 및 전체 플로우 제어 (라인 20-55)
    - extract_source_from_md(md_file): 마크다운 YAML front matter에서 source 필드 추출 (라인 57-85)
    - parse_yaml_frontmatter(content): YAML front matter 파싱 (라인 87-105)
    - update_metadata_source(metadata_file, source_url): metadata.json의 source 필드 업데이트 (라인 107-125)
상태: active
주소: source_updater
참조: 신규 생성
"""

import json
import re
import sys
import yaml
from pathlib import Path
from typing import Optional, Dict, Any


def main():
    """메인 실행 함수"""
    # 기본 경로 설정
    base_path = Path("/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/Post")
    source_md = base_path / "source.md"
    metadata_json = base_path / "metadata.json"
    
    # 파일 존재 확인
    if not source_md.exists():
        print(f"❌ source.md 파일을 찾을 수 없습니다: {source_md}")
        sys.exit(1)
        
    if not metadata_json.exists():
        print(f"❌ metadata.json 파일을 찾을 수 없습니다: {metadata_json}")
        sys.exit(1)
    
    print(f"📁 source.md: {source_md}")
    print(f"📁 metadata.json: {metadata_json}")
    
    try:
        # source.md에서 source 필드 추출
        source_url = extract_source_from_md(source_md)
        
        if not source_url:
            print("⚠️ source.md에서 source 필드를 찾을 수 없습니다.")
            sys.exit(1)
        
        print(f"🔍 추출된 source: {source_url}")
        
        # metadata.json 업데이트
        update_metadata_source(metadata_json, source_url)
        
        print("✅ metadata.json 업데이트 완료!")
        
    except Exception as e:
        print(f"❌ 처리 중 오류 발생: {str(e)}")
        sys.exit(1)


def extract_source_from_md(md_file: Path) -> Optional[str]:
    """마크다운 YAML front matter에서 source 필드 추출"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # YAML front matter 파싱
        yaml_data = parse_yaml_frontmatter(content)
        
        if yaml_data and 'source' in yaml_data:
            source_value = yaml_data['source']
            if isinstance(source_value, str) and source_value.strip():
                return source_value.strip()
        
        return None
        
    except Exception as e:
        raise Exception(f"source.md 파싱 중 오류: {str(e)}")


def parse_yaml_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """YAML front matter 파싱"""
    # YAML front matter 패턴: ---로 시작하고 ---로 끝남
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    yaml_content = match.group(1)
    
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise Exception(f"YAML 파싱 오류: {str(e)}")


def update_metadata_source(metadata_file: Path, source_url: str) -> None:
    """metadata.json의 source 필드 업데이트"""
    try:
        # 기존 metadata.json 로드
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        print(f"📋 기존 source 값: '{metadata.get('source', '')}'")
        
        # source 필드 업데이트
        metadata['source'] = source_url
        
        # 파일 저장
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"💾 새로운 source 값: '{source_url}'")
        
    except Exception as e:
        raise Exception(f"metadata.json 업데이트 중 오류: {str(e)}")


if __name__ == "__main__":
    main()