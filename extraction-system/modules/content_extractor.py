# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: subprocess 제거된 노드 정보 추출 모듈
# 상세 내용:
#   - extract_enhanced_node_content() (라인 15-65): 메인 노드 정보 추출 함수
#   - find_node_info_files() (라인 67-78): 노드 정보 파일 검색 함수
#   - process_single_node() (라인 80-120): 개별 노드 정보 처리 함수
#   - extract_key_insights() (라인 122-145): 핵심 인사이트 추출 함수
# 상태: active
# 주소: modules/content_extractor
# 참조: extract_enhanced_node_content_fixed.py → 함수화

import asyncio
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


def extract_enhanced_node_content(video_folder: str) -> Dict[str, Any]:
    """노드 정보 추출 (subprocess 제거된 버전)"""
    try:
        if not os.path.exists(video_folder):
            return {"success": False, "error": f"비디오 폴더가 존재하지 않습니다: {video_folder}"}
        
        print("📊 노드 정보 추출 시작")
        print(f"📁 처리 폴더: {os.path.abspath(video_folder)}")
        
        # 1. 노드 정보 파일들 찾기
        info_files = find_node_info_files(video_folder)
        if not info_files:
            return {"success": False, "error": "처리할 노드 정보 파일이 없습니다"}
        
        print(f"📄 발견된 정보 파일: {len(info_files)}개")
        
        # 2. 각 노드 정보 처리
        processed_nodes = []
        for info_file in info_files:
            node_data = process_single_node(info_file)
            if node_data:
                processed_nodes.append(node_data)
        
        # 3. 추출된 정보를 JSON으로 저장
        output_file = os.path.join(video_folder, "extracted_nodes.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_nodes, f, ensure_ascii=False, indent=2)
        
        # 4. 핵심 인사이트 추출
        insights = extract_key_insights(processed_nodes)
        insights_file = os.path.join(video_folder, "key_insights.json")
        with open(insights_file, 'w', encoding='utf-8') as f:
            json.dump(insights, f, ensure_ascii=False, indent=2)
        
        print("=" * 50)
        print(f"🎉 노드 정보 추출 완료")
        print(f"📄 추출된 노드: {len(processed_nodes)}개")
        print(f"📄 출력 파일: {output_file}")
        print(f"💡 인사이트 파일: {insights_file}")
        
        return {
            "success": True,
            "output_file": output_file,
            "insights_file": insights_file,
            "processed_count": len(processed_nodes),
            "insights_count": len(insights.get("insights", []))
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_node_info_files(video_folder: str) -> List[Path]:
    """노드 정보 파일들 검색"""
    docs_dir = os.path.join(video_folder, "node_info_docs")
    if not os.path.exists(docs_dir):
        return []
    
    docs_path = Path(docs_dir)
    info_files = list(docs_path.glob("*_info.md"))
    info_files.sort(key=lambda x: x.name)  # 파일명으로 정렬
    
    return info_files


def process_single_node(info_file: Path) -> Optional[Dict[str, Any]]:
    """개별 노드 정보 문서 처리"""
    try:
        with open(info_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 파일명에서 정보 추출
        filename = info_file.name
        parts = filename.replace('_info.md', '').split('_')
        
        node_index = parts[0] if parts else "000"
        node_type = parts[-1] if len(parts) > 2 else "unknown"
        title = "_".join(parts[1:-1]) if len(parts) > 2 else "untitled"
        
        # 내용에서 핵심 정보 추출
        lines = content.split('\n')
        extracted_content = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('## '):
                current_section = line[3:].strip()
            elif line and current_section == "내용" and not line.startswith('#'):
                extracted_content.append(line)
        
        # 핵심 키워드 추출 (간단한 방식)
        full_text = ' '.join(extracted_content)
        keywords = extract_keywords(full_text)
        
        return {
            "index": node_index,
            "title": title.replace('_', ' '),
            "type": node_type,
            "filename": filename,
            "content": '\n'.join(extracted_content),
            "keywords": keywords,
            "word_count": len(full_text.split()),
            "processed_at": info_file.stat().st_mtime
        }
        
    except Exception as e:
        print(f"⚠️ 노드 파일 {info_file.name} 처리 실패: {e}")
        return None


def extract_key_insights(nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """핵심 인사이트 추출"""
    try:
        # 전체 키워드 빈도 분석
        all_keywords = []
        for node in nodes:
            all_keywords.extend(node.get("keywords", []))
        
        # 키워드 빈도 계산
        keyword_freq = {}
        for keyword in all_keywords:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        
        # 빈도 순으로 정렬
        top_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 타입별 분포
        type_dist = {}
        for node in nodes:
            node_type = node.get("type", "unknown")
            type_dist[node_type] = type_dist.get(node_type, 0) + 1
        
        return {
            "total_nodes": len(nodes),
            "top_keywords": top_keywords,
            "type_distribution": type_dist,
            "average_word_count": sum(node.get("word_count", 0) for node in nodes) / len(nodes),
            "insights": [
                f"총 {len(nodes)}개의 노드가 처리되었습니다",
                f"가장 빈번한 키워드는 '{top_keywords[0][0]}'입니다" if top_keywords else "키워드가 발견되지 않았습니다",
                f"주요 노드 타입은 {max(type_dist.items(), key=lambda x: x[1])[0]}입니다" if type_dist else "타입 정보가 없습니다"
            ]
        }
        
    except Exception as e:
        print(f"⚠️ 인사이트 추출 중 오류: {e}")
        return {"error": str(e)}


def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """간단한 키워드 추출 (빈도 기반)"""
    try:
        # 한글, 영어 단어만 추출 (최소 2글자)
        words = re.findall(r'[가-힣]{2,}|[A-Za-z]{2,}', text.lower())
        
        # 불용어 제거 (간단한 버전)
        stop_words = {'이것', '그것', '저것', '이런', '그런', '저런', '어떤', '무엇', 'the', 'is', 'at', 'which', 'on'}
        words = [word for word in words if word not in stop_words]
        
        # 빈도 계산
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 빈도 순으로 정렬하여 상위 키워드 반환
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in top_words[:max_keywords]]
        
    except Exception:
        return []