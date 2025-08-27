# 생성 시간: 2025-01-21 21:13 KST  
# 핵심 내용: FastAPI 서버 - 파일 업로드 및 YouTube 스크립트 추출
# 상세 내용:
#   - app = FastAPI(): FastAPI 인스턴스 생성
#   - /: HTML 페이지 서빙 엔드포인트
#   - /upload: 파일 + 텍스트 업로드 처리 엔드포인트
#   - /youtube: YouTube URL 스크립트 추출 엔드포인트
#   - uploads 디렉토리 자동 생성 로직
#   - 터미널 로깅 기능
# 상태: active

import os
import re
import asyncio
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Union
from youtube_extractor import process_youtube_url
from metadata_manager import create_metadata_json, get_existing_folder
from transcript_improver import improve_transcript_with_claude, extract_transcript_content, extract_first_last_sentences
from node_generator import load_metadata, extract_headers_by_type

app = FastAPI()

# uploads 디렉토리 생성
os.makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

def is_youtube_url(url):
    """YouTube URL 여부를 판별합니다."""
    youtube_patterns = [
        r'(?:youtube\.com/watch\?v=)',
        r'(?:youtube\.com/embed/)',
        r'(?:youtu\.be/)',
        r'(?:youtube\.com/v/)'
    ]
    
    for pattern in youtube_patterns:
        if re.search(pattern, url):
            return True
    return False


async def improve_transcript(script_file_path):
    """스크립트 개선 함수"""
    try:
        print(f"✨ 스크립트 개선 시작: {script_file_path}")
        
        # 스크립트 내용 추출
        transcript_content = extract_transcript_content(script_file_path)
        if not transcript_content:
            return {"success": False, "error": "스크립트 내용 추출 실패"}
        
        # 첫/마지막 문장 추출
        first_words, last_words = extract_first_last_sentences(transcript_content)
        
        # Claude로 스크립트 개선
        improved_content = await improve_transcript_with_claude(transcript_content, first_words, last_words)
        if not improved_content:
            return {"success": False, "error": "스크립트 개선 실패"}
        
        # 개선된 내용 저장 (같은 비디오 ID 폴더에 content.md로 저장)
        script_path = Path(script_file_path)
        content_file = script_path.parent / "content.md"
        
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(improved_content)
        
        print(f"✅ 스크립트 개선 완료: {content_file.name}")
        return {
            "success": True,
            "content_file": str(content_file),
            "filename": content_file.name
        }
        
    except Exception as e:
        print(f"❌ 스크립트 개선 오류: {str(e)}")
        return {"success": False, "error": str(e)}


async def generate_nodes(metadata_file_path, script_file_path):
    """노드 정보 생성 함수"""
    try:
        print(f"🌐 노드 생성 시작: {metadata_file_path}, {script_file_path}")
        
        # 메타데이터 로드
        metadata = load_metadata(Path(metadata_file_path))
        if not metadata:
            return {"success": False, "error": "메타데이터 로드 실패"}
        
        # 스크립트 내용 읽기
        with open(script_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 헤더 추출
        nodes = extract_headers_by_type(content, metadata)
        
        # 노드 파일 저장 (같은 비디오 ID 폴더에 nodes.json로 저장)
        script_path = Path(script_file_path)
        nodes_file = script_path.parent / "nodes.json"
        
        import json
        with open(nodes_file, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 노드 생성 완료: {nodes_file.name}")
        return {
            "success": True,
            "nodes_file": str(nodes_file),
            "filename": nodes_file.name,
            "node_count": len(nodes)
        }
        
    except Exception as e:
        print(f"❌ 노드 생성 오류: {str(e)}")
        return {"success": False, "error": str(e)}


async def create_node_info_docs(extraction_folder):
    """노드 정보 문서 생성 함수"""
    try:
        print(f"📄 5단계: 노드 정보 문서 생성 시작...")
        
        # 스크립트 실행 (이미 만든 스크립트 활용)
        import subprocess
        import sys
        
        script_path = os.path.join(os.path.dirname(__file__), 'create_node_info_docs_fixed.py')
        
        result = subprocess.run([
            sys.executable, script_path, extraction_folder
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ 노드 정보 문서 생성 성공")
            return {
                "success": True,
                "output": result.stdout,
                "docs_dir": os.path.join(extraction_folder, "node_info_docs")
            }
        else:
            print(f"❌ 노드 정보 문서 생성 실패: {result.stderr}")
            return {"success": False, "error": result.stderr}
        
    except Exception as e:
        print(f"❌ 노드 정보 문서 생성 오류: {str(e)}")
        return {"success": False, "error": str(e)}


async def integrate_node_docs(extraction_folder):
    """노드 문서 통합 함수"""
    try:
        print(f"🔗 6단계: 노드 문서 통합 시작...")
        
        # 스크립트 실행 (이미 만든 스크립트 활용)
        import subprocess
        import sys
        
        script_path = os.path.join(os.path.dirname(__file__), 'integrate_node_documents_fixed.py')
        
        result = subprocess.run([
            sys.executable, script_path, extraction_folder
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ 노드 문서 통합 성공")
            return {
                "success": True,
                "output": result.stdout,
                "docs_dir": extraction_folder
            }
        else:
            print(f"❌ 노드 문서 통합 실패: {result.stderr}")
            return {"success": False, "error": result.stderr}
        
    except Exception as e:
        print(f"❌ 노드 문서 통합 오류: {str(e)}")
        return {"success": False, "error": str(e)}


async def extract_enhanced_content(extraction_folder):
    """노드 정보 추출 함수"""
    try:
        print(f"📊 7단계: 노드 정보 추출 시작...")
        
        # 스크립트 실행 (extraction-system 폴더의 스크립트 사용)
        import subprocess
        import sys
        
        script_path = os.path.join(os.path.dirname(__file__), 'extract_enhanced_node_content_fixed.py')
        
        result = subprocess.run([
            sys.executable, script_path, extraction_folder
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ 노드 정보 추출 성공")
            return {
                "success": True,
                "output": result.stdout,
                "docs_dir": extraction_folder
            }
        else:
            print(f"❌ 노드 정보 추출 실패: {result.stderr}")
            return {"success": False, "error": result.stderr}
        
    except Exception as e:
        print(f"❌ 노드 정보 추출 오류: {str(e)}")
        return {"success": False, "error": str(e)}





@app.post("/upload")
async def upload_file(
    file: Union[UploadFile, None] = File(None),
    text_data: Union[str, None] = Form(None),
    source_type: Union[str, None] = Form(None),
    source_language: Union[str, None] = Form(None),
    structure_type: Union[str, None] = Form(None),
    content_processing: Union[str, None] = Form(None)
):
    # 결과 정보
    result = {}
    
    # 파일이 있는 경우 처리
    if file and file.filename:
        # 파일 저장
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        
        # 터미널 로깅
        print(f"📁 파일 업로드됨:")
        print(f"  - 파일명: {file.filename}")
        print(f"  - 크기: {len(contents)} bytes")
        print(f"  - 타입: {file.content_type}")
        print(f"  - 저장 위치: {file_path}")
        
        result["file_info"] = {
            "filename": file.filename,
            "size": len(contents),
            "content_type": file.content_type,
            "saved_path": file_path
        }
    
    # 텍스트 데이터가 있는 경우 처리
    if text_data and text_data.strip():
        # YouTube URL인지 확인
        if is_youtube_url(text_data.strip()):
            print(f"🎥 YouTube URL 감지: {text_data}")
            
            # 메타정보 수집
            metadata_info = {
                "source_type": source_type or "youtube",
                "source_language": source_language or "korean", 
                "structure_type": structure_type or "standalone",
                "content_processing": content_processing or "unified"
            }
            
            # 1단계: 메타정보 JSON 파일 생성
            json_result = create_metadata_json(metadata_info, text_data.strip())
            
            if json_result["success"]:
                print(f"📄 메타정보 JSON 생성 성공:")
                print(f"  - 폴더: {json_result['folder_path']}")
                print(f"  - JSON 파일: {json_result['json_path']}")
                
                # 2단계: 생성된 폴더에 스크립트 추출
                print(f"🎥 YouTube 스크립트 추출 시작...")
                youtube_result = process_youtube_url(text_data.strip(), ".", json_result['folder_path'], json_result['metadata'])
                
                if youtube_result["success"]:
                    print(f"✅ YouTube 스크립트 추출 성공:")
                    print(f"  - 제목: {youtube_result['video_info']['title']}")
                    print(f"  - 언어: {youtube_result['video_info']['language']}")
                    print(f"  - 파일: {youtube_result['file_info']['full_path']}")
                    
                    # 3단계: 스크립트 개선
                    print(f"✨ 3단계: 스크립트 개선 시작...")
                    transcript_result = await improve_transcript(youtube_result['file_info']['full_path'])
                    
                    if transcript_result["success"]:
                        print(f"✅ 스크립트 개선 성공: {transcript_result['filename']}")
                        
                        # 4단계: 노드 생성
                        print(f"🌐 4단계: 노드 생성 시작...")
                        nodes_result = await generate_nodes(json_result['json_path'], youtube_result['file_info']['full_path'])
                        
                        if nodes_result["success"]:
                            print(f"✅ 노드 생성 성공: {nodes_result['filename']} ({nodes_result['node_count']}개 노드)")
                            
                            # 5단계: 노드 정보 문서 생성
                            print(f"📄 5단계: 노드 정보 문서 생성 시작...")
                            docs_result = await create_node_info_docs(json_result['folder_path'])
                            
                            if docs_result["success"]:
                                print(f"✅ 노드 정보 문서 생성 성공")
                                
                                # 6단계: 노드 문서 통합
                                print(f"🔗 6단계: 노드 문서 통합 시작...")
                                integration_result = await integrate_node_docs(json_result['folder_path'])
                                
                                if integration_result["success"]:
                                    print(f"✅ 노드 문서 통합 성공!")
                                    
                                    # 7단계: 노드 정보 추출
                                    print(f"📊 7단계: 노드 정보 추출 시작...")
                                    extraction_result = await extract_enhanced_content(json_result['folder_path'])
                                    
                                    if extraction_result["success"]:
                                        print(f"✅ 전체 파이프라인 완료! (7단계)")
                                        
                                        result["json_creation"] = {
                                            "success": True,
                                            "folder_path": json_result['folder_path'],
                                            "json_path": json_result['json_path']
                                        }
                                        result["youtube_extraction"] = youtube_result
                                        result["transcript_improvement"] = transcript_result
                                        result["node_generation"] = nodes_result
                                        result["node_docs_creation"] = docs_result
                                        result["node_docs_integration"] = integration_result
                                        result["node_content_extraction"] = extraction_result
                                        result["type"] = "pipeline_complete_full_enhanced"
                                    else:
                                        print(f"❌ 노드 정보 추출 실패: {extraction_result['error']}")
                                        result["json_creation"] = {
                                            "success": True,
                                            "folder_path": json_result['folder_path'],
                                            "json_path": json_result['json_path']
                                        }
                                        result["youtube_extraction"] = youtube_result
                                        result["transcript_improvement"] = transcript_result
                                        result["node_generation"] = nodes_result
                                        result["node_docs_creation"] = docs_result
                                        result["node_docs_integration"] = integration_result
                                        result["node_content_extraction"] = extraction_result
                                        result["type"] = "pipeline_partial_extraction"
                                else:
                                    print(f"❌ 노드 문서 통합 실패: {integration_result['error']}")
                                    result["json_creation"] = {
                                        "success": True,
                                        "folder_path": json_result['folder_path'],
                                        "json_path": json_result['json_path']
                                    }
                                    result["youtube_extraction"] = youtube_result
                                    result["transcript_improvement"] = transcript_result
                                    result["node_generation"] = nodes_result
                                    result["node_docs_creation"] = docs_result
                                    result["node_docs_integration"] = integration_result
                                    result["type"] = "pipeline_partial_integration"
                            else:
                                print(f"❌ 노드 정보 문서 생성 실패: {docs_result['error']}")
                                result["json_creation"] = {
                                    "success": True,
                                    "folder_path": json_result['folder_path'],
                                    "json_path": json_result['json_path']
                                }
                                result["youtube_extraction"] = youtube_result
                                result["transcript_improvement"] = transcript_result
                                result["node_generation"] = nodes_result
                                result["node_docs_creation"] = docs_result
                                result["type"] = "pipeline_partial_docs"
                        else:
                            print(f"❌ 노드 생성 실패: {nodes_result['error']}")
                            result["json_creation"] = {
                                "success": True,
                                "folder_path": json_result['folder_path'],
                                "json_path": json_result['json_path']
                            }
                            result["youtube_extraction"] = youtube_result
                            result["transcript_improvement"] = transcript_result
                            result["node_generation"] = nodes_result
                            result["type"] = "pipeline_partial_nodes"
                    else:
                        print(f"❌ 스크립트 개선 실패: {transcript_result['error']}")
                        result["json_creation"] = {
                            "success": True,
                            "folder_path": json_result['folder_path'],
                            "json_path": json_result['json_path']
                        }
                        result["youtube_extraction"] = youtube_result
                        result["transcript_improvement"] = transcript_result
                        result["type"] = "pipeline_partial_transcript"
                    
                else:
                    print(f"❌ YouTube 스크립트 추출 실패: {youtube_result['message']}")
                    result["json_creation"] = {
                        "success": True,
                        "folder_path": json_result['folder_path'],
                        "json_path": json_result['json_path']
                    }
                    result["youtube_extraction"] = youtube_result
                    result["type"] = "youtube_partial"
                
            else:
                print(f"❌ 메타정보 JSON 생성 실패: {json_result['error']}")
                result["json_creation"] = {
                    "success": False,
                    "error": json_result['error']
                }
                result["type"] = "youtube_metadata_error"
        else:
            # 일반 텍스트 처리
            print(f"📝 텍스트 데이터 수신: {text_data}")
            result["text_data"] = text_data
            result["type"] = "text"
    
    # 둘 다 없는 경우
    if not file and not text_data:
        print("⚠️ 파일이나 텍스트 데이터가 없습니다.")
        result["message"] = "파일이나 텍스트를 입력해주세요."
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)