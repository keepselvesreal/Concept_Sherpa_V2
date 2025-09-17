# 생성 시간: 2025-01-16 13:48 KST
# 핵심 내용: 다중 MD 파일 처리 지원 FastAPI 서버 (URL 목록 관리 방식 적용)
# 상세 내용:
#   - file_queue: 선택된 파일 목록 관리 (라인 21-28)
#   - /upload_files: 다중 MD 파일 업로드 엔드포인트 (라인 83-118)
#   - /get_file_queue: 현재 파일 큐 상태 조회 (라인 120-125)  
#   - /process_file_queue: 큐에 있는 모든 파일 순회 처리 (라인 127-188)
#   - /clear_file_queue: 파일 큐 초기화 (라인 190-195)
# 상태: active
# 참조: server.py → 다중 파일 처리 기능 추가

import os
import re
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Union, List
import asyncio

# 리팩토링된 파이프라인 임포트
from pipeline.youtube_pipeline import YouTubePipeline
from pipeline.md_pipeline import MDPipeline
# from pipeline.book_pipeline import BookPipeline

app = FastAPI()

# uploads 디렉토리 생성
os.makedirs("uploads", exist_ok=True)

# 큐 관리 (메모리 저장)
file_queue = []
url_queue = []

# 파일 큐 관리
def add_files_to_queue(files_info: List[dict]):
    """파일 정보를 큐에 추가"""
    file_queue.extend(files_info)
    return len(file_queue)

def get_file_queue():
    """현재 파일 큐 상태 반환"""
    return file_queue

def clear_file_queue():
    """파일 큐 초기화"""
    file_queue.clear()

# URL 큐 관리  
def add_urls_to_queue(urls_info: List[dict]):
    """URL 정보를 큐에 추가"""
    url_queue.extend(urls_info)
    return len(url_queue)

def get_url_queue():
    """현재 URL 큐 상태 반환"""
    return url_queue

def clear_url_queue():
    """URL 큐 초기화"""
    url_queue.clear()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """메인 페이지 서빙"""
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


def is_youtube_url(url: str) -> bool:
    """YouTube URL 여부 판별"""
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


@app.post("/upload")
async def upload_file(
    file: Union[UploadFile, None] = File(None),
    source_type: Union[str, None] = Form(None),
    source_language: Union[str, None] = Form(None),
    structure_type: Union[str, None] = Form(None),
    content_processing: Union[str, None] = Form(None)
):
    """단일 파일 즉시 처리 엔드포인트"""
    
    # 파일이 없는 경우
    if not file or not file.filename:
        print("⚠️ 첨부된 파일이 없습니다.")
        return {
            "type": "no_file",
            "status": "error",
            "message": "파일을 첨부해주세요."
        }
    
    # 파일 형식 확인
    file_ext = file.filename.lower()
    if not file_ext.endswith(('.md', '.markdown')):
        return {
            "type": "unsupported_file",
            "status": "error", 
            "message": "Markdown 파일(.md)만 지원합니다."
        }
    
    # 임시로 uploads 폴더에 파일 저장
    file_path = f"uploads/{file.filename}"
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        print(f"📁 MD 파일 업로드됨: {file.filename} ({len(contents)} bytes)")
        
        # 메타정보 구성
        metadata_info = {
            "source_type": source_type or "markdown",
            "source_language": source_language or "korean",
            "structure_type": structure_type or "standalone",
            "content_processing": content_processing or "unified"
        }
        
        # 🚀 MD 파이프라인 즉시 실행
        try:
            from pipeline.md_pipeline import MDPipeline
            pipeline = MDPipeline()
            pipeline_result = await pipeline.execute(file_path, metadata_info)
            
            if pipeline_result.is_success:
                print("🎉 MD 파이프라인 완료!")
                result = {
                    "type": "md_pipeline_success",
                    "status": "success",
                    "data": pipeline_result.data,
                    "progress": {
                        "completed_steps": pipeline_result.step_completed,
                        "total_steps": pipeline_result.total_steps,
                        "progress_percent": pipeline_result.progress_percent
                    },
                    "file_info": {
                        "filename": file.filename,
                        "size": len(contents),
                        "content_type": file.content_type
                    }
                }
            else:
                print(f"❌ MD 파이프라인 실패: {pipeline_result.error}")
                result = {
                    "type": "md_pipeline_failed",
                    "status": "failed",
                    "error": pipeline_result.error,
                    "progress": {
                        "completed_steps": pipeline_result.step_completed,
                        "total_steps": pipeline_result.total_steps,
                        "progress_percent": pipeline_result.progress_percent
                    },
                    "file_info": {
                        "filename": file.filename,
                        "size": len(contents),
                        "content_type": file.content_type
                    }
                }
        
        except Exception as e:
            error_msg = f"MD 파이프라인 실행 중 오류: {str(e)}"
            print(f"❌ {error_msg}")
            result = {
                "type": "md_pipeline_error",
                "status": "error",
                "error": error_msg,
                "file_info": {
                    "filename": file.filename,
                    "size": len(contents),
                    "content_type": file.content_type
                }
            }
        
        # 임시 파일 정리
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🧹 임시 파일 정리: {file_path}")
        
        return result
        
    except Exception as e:
        error_msg = f"파일 처리 중 오류: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "type": "file_error",
            "status": "error",
            "error": error_msg
        }


@app.post("/upload_files")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    source_type: Union[str, None] = Form(None),
    source_language: Union[str, None] = Form(None), 
    structure_type: Union[str, None] = Form(None),
    content_processing: Union[str, None] = Form(None)
):
    """다중 MD 파일 업로드 및 큐에 추가"""
    
    if not files:
        return {
            "type": "no_files",
            "status": "error",
            "message": "파일을 첨부해주세요."
        }
    
    valid_files = []
    invalid_files = []
    
    # 파일 검증 및 저장
    for file in files:
        if not file.filename:
            continue
            
        file_ext = file.filename.lower()
        if not file_ext.endswith(('.md', '.markdown')):
            invalid_files.append(file.filename)
            continue
            
        # 파일 저장
        file_path = f"uploads/{file.filename}"
        try:
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            
            # 파일 정보 저장
            file_info = {
                "filename": file.filename,
                "file_path": file_path,
                "size": len(contents),
                "content_type": file.content_type,
                "metadata": {
                    "source_type": source_type or "markdown",
                    "source_language": source_language or "korean",
                    "structure_type": structure_type or "standalone", 
                    "content_processing": content_processing or "unified"
                },
                "status": "queued",
                "processed": False
            }
            valid_files.append(file_info)
            
        except Exception as e:
            invalid_files.append(f"{file.filename} (저장 실패: {str(e)})")
    
    # 큐에 추가
    if valid_files:
        queue_size = add_files_to_queue(valid_files)
        print(f"📁 {len(valid_files)}개 파일이 큐에 추가됨 (총 큐 크기: {queue_size})")
    
    return {
        "type": "files_queued",
        "status": "success" if valid_files else "warning",
        "valid_files": len(valid_files),
        "invalid_files": len(invalid_files),
        "invalid_file_list": invalid_files,
        "queue_size": len(file_queue),
        "message": f"{len(valid_files)}개 파일이 처리 큐에 추가되었습니다."
    }


@app.get("/get_file_queue")
async def get_current_file_queue():
    """현재 파일 큐 상태 조회"""
    return {
        "queue_size": len(file_queue),
        "files": file_queue
    }


@app.post("/process_file_queue")
async def process_file_queue():
    """큐에 있는 모든 파일을 순회하며 처리"""
    
    if not file_queue:
        return {
            "type": "empty_queue",
            "status": "warning",
            "message": "처리할 파일이 큐에 없습니다."
        }
    
    print(f"🚀 파일 큐 처리 시작 - 총 {len(file_queue)}개 파일")
    
    results = []
    processed_count = 0
    failed_count = 0
    
    # 큐의 모든 파일을 순회하며 처리
    for idx, file_info in enumerate(file_queue):
        if file_info.get("processed", False):
            print(f"⏭️ 이미 처리된 파일 스킵: {file_info['filename']}")
            continue
            
        print(f"\n🔄 [{idx+1}/{len(file_queue)}] 처리 중: {file_info['filename']}")
        
        file_info["status"] = "processing"
        
        try:
            # MD 파이프라인 실행
            pipeline = MDPipeline()
            pipeline_result = await pipeline.execute(
                file_info["file_path"], 
                file_info["metadata"]
            )
            
            if pipeline_result.is_success:
                print(f"✅ 성공: {file_info['filename']}")
                file_info["status"] = "completed"
                file_info["processed"] = True
                file_info["result"] = pipeline_result.data
                processed_count += 1
                
                result_entry = {
                    "filename": file_info["filename"],
                    "status": "success",
                    "data": pipeline_result.data,
                    "progress": {
                        "completed_steps": pipeline_result.step_completed,
                        "total_steps": pipeline_result.total_steps,
                        "progress_percent": pipeline_result.progress_percent
                    }
                }
            else:
                print(f"❌ 실패: {file_info['filename']} - {pipeline_result.error}")
                file_info["status"] = "failed"
                file_info["error"] = pipeline_result.error
                failed_count += 1
                
                result_entry = {
                    "filename": file_info["filename"],
                    "status": "failed",
                    "error": pipeline_result.error,
                    "progress": {
                        "completed_steps": pipeline_result.step_completed,
                        "total_steps": pipeline_result.total_steps,
                        "progress_percent": pipeline_result.progress_percent
                    }
                }
            
        except Exception as e:
            error_msg = f"파이프라인 실행 중 오류: {str(e)}"
            print(f"❌ 예외: {file_info['filename']} - {error_msg}")
            file_info["status"] = "error"
            file_info["error"] = error_msg
            failed_count += 1
            
            result_entry = {
                "filename": file_info["filename"],
                "status": "error",
                "error": error_msg
            }
        
        results.append(result_entry)
        
        # 파일 정리
        if os.path.exists(file_info["file_path"]):
            os.remove(file_info["file_path"])
            print(f"🧹 임시 파일 정리: {file_info['filename']}")
    
    print(f"\n🎉 파일 큐 처리 완료!")
    print(f"  ✅ 성공: {processed_count}개")
    print(f"  ❌ 실패: {failed_count}개")
    
    return {
        "type": "queue_processed",
        "status": "completed",
        "summary": {
            "total_files": len(file_queue),
            "processed": processed_count,
            "failed": failed_count
        },
        "results": results
    }


@app.post("/clear_file_queue")  
async def clear_queue():
    """파일 큐 초기화"""
    queue_size = len(file_queue)
    clear_file_queue()
    
    return {
        "type": "queue_cleared",
        "status": "success", 
        "message": f"파일 큐가 초기화되었습니다. ({queue_size}개 파일 제거)"
    }


# ============= URL 큐 관리 엔드포인트 =============

@app.post("/add_urls")
async def add_multiple_urls(
    urls: List[str] = Form(...),
    source_type: Union[str, None] = Form(None),
    source_language: Union[str, None] = Form(None),
    structure_type: Union[str, None] = Form(None),
    content_processing: Union[str, None] = Form(None)
):
    """다중 URL을 큐에 추가"""
    
    if not urls:
        return {
            "type": "no_urls",
            "status": "error",
            "message": "URL을 입력해주세요."
        }
    
    valid_urls = []
    invalid_urls = []
    
    # URL 검증
    for url in urls:
        url = url.strip()
        if not url:
            continue
            
        if not is_youtube_url(url):
            invalid_urls.append(url)
            continue
            
        # URL 정보 저장
        url_info = {
            "url": url,
            "metadata": {
                "source_type": source_type or "youtube",
                "source_language": source_language or "korean",
                "structure_type": structure_type or "standalone",
                "content_processing": content_processing or "unified"
            },
            "status": "queued",
            "processed": False
        }
        valid_urls.append(url_info)
    
    # 큐에 추가
    if valid_urls:
        queue_size = add_urls_to_queue(valid_urls)
        print(f"🎥 {len(valid_urls)}개 URL이 큐에 추가됨 (총 큐 크기: {queue_size})")
    
    return {
        "type": "urls_queued",
        "status": "success" if valid_urls else "warning",
        "valid_urls": len(valid_urls),
        "invalid_urls": len(invalid_urls),
        "invalid_url_list": invalid_urls,
        "queue_size": len(url_queue),
        "message": f"{len(valid_urls)}개 URL이 처리 큐에 추가되었습니다."
    }


@app.get("/get_url_queue")
async def get_current_url_queue():
    """현재 URL 큐 상태 조회"""
    return {
        "queue_size": len(url_queue),
        "urls": url_queue
    }


@app.post("/process_url_queue")
async def process_url_queue():
    """큐에 있는 모든 URL을 순회하며 처리"""
    
    if not url_queue:
        return {
            "type": "empty_queue",
            "status": "warning",
            "message": "처리할 URL이 큐에 없습니다."
        }
    
    print(f"🚀 URL 큐 처리 시작 - 총 {len(url_queue)}개 URL")
    
    results = []
    processed_count = 0
    failed_count = 0
    
    # 큐의 모든 URL을 순회하며 처리
    for idx, url_info in enumerate(url_queue):
        if url_info.get("processed", False):
            print(f"⏭️ 이미 처리된 URL 스킵: {url_info['url']}")
            continue
            
        print(f"\n🔄 [{idx+1}/{len(url_queue)}] 처리 중: {url_info['url']}")
        
        url_info["status"] = "processing"
        
        try:
            # YouTube 파이프라인 실행
            pipeline = YouTubePipeline()
            pipeline_result = await pipeline.execute(
                url_info["url"], 
                url_info["metadata"]
            )
            
            if pipeline_result.is_success:
                print(f"✅ 성공: {url_info['url']}")
                url_info["status"] = "completed"
                url_info["processed"] = True
                url_info["result"] = pipeline_result.data
                processed_count += 1
                
                result_entry = {
                    "url": url_info["url"],
                    "status": "success",
                    "data": pipeline_result.data,
                    "progress": {
                        "completed_steps": pipeline_result.step_completed,
                        "total_steps": pipeline_result.total_steps,
                        "progress_percent": pipeline_result.progress_percent
                    }
                }
            else:
                print(f"❌ 실패: {url_info['url']} - {pipeline_result.error}")
                url_info["status"] = "failed"
                url_info["error"] = pipeline_result.error
                failed_count += 1
                
                result_entry = {
                    "url": url_info["url"],
                    "status": "failed",
                    "error": pipeline_result.error,
                    "progress": {
                        "completed_steps": pipeline_result.step_completed,
                        "total_steps": pipeline_result.total_steps,
                        "progress_percent": pipeline_result.progress_percent
                    }
                }
            
        except Exception as e:
            error_msg = f"파이프라인 실행 중 오류: {str(e)}"
            print(f"❌ 예외: {url_info['url']} - {error_msg}")
            url_info["status"] = "error"
            url_info["error"] = error_msg
            failed_count += 1
            
            result_entry = {
                "url": url_info["url"],
                "status": "error",
                "error": error_msg
            }
        
        results.append(result_entry)
    
    print(f"\n🎉 URL 큐 처리 완료!")
    print(f"  ✅ 성공: {processed_count}개")
    print(f"  ❌ 실패: {failed_count}개")
    
    return {
        "type": "queue_processed",
        "status": "completed",
        "summary": {
            "total_urls": len(url_queue),
            "processed": processed_count,
            "failed": failed_count
        },
        "results": results
    }


@app.post("/clear_url_queue")
async def clear_url_queue_endpoint():
    """URL 큐 초기화"""
    queue_size = len(url_queue)
    clear_url_queue()
    
    return {
        "type": "queue_cleared",
        "status": "success",
        "message": f"URL 큐가 초기화되었습니다. ({queue_size}개 URL 제거)"
    }


# 기존 YouTube URL 처리는 그대로 유지
@app.post("/process_url")
async def process_url(
    text_data: str = Form(...),
    source_type: Union[str, None] = Form(None),
    source_language: Union[str, None] = Form(None),
    structure_type: Union[str, None] = Form(None),
    content_processing: Union[str, None] = Form(None)
):
    """URL 입력 전용 엔드포인트 (YouTube URL 처리)"""
    
    if not text_data or not text_data.strip():
        print("⚠️ URL이 입력되지 않았습니다.")
        return {
            "type": "no_url", 
            "status": "error",
            "message": "URL을 입력해주세요."
        }
    
    url = text_data.strip()
    
    if is_youtube_url(url):
        print(f"🎥 YouTube URL 감지: {url}")
        
        # 메타정보 구성
        metadata_info = {
            "source_type": source_type or "youtube",
            "source_language": source_language or "korean",
            "structure_type": structure_type or "standalone", 
            "content_processing": content_processing or "unified"
        }
        
        # 🚀 YouTube 파이프라인 실행
        try:
            pipeline = YouTubePipeline()
            pipeline_result = await pipeline.execute(url, metadata_info)
            
            if pipeline_result.is_success:
                print("🎉 YouTube 파이프라인 완료!")
                return {
                    "type": "youtube_pipeline_success",
                    "status": "success",
                    "data": pipeline_result.data,
                    "progress": {
                        "completed_steps": pipeline_result.step_completed,
                        "total_steps": pipeline_result.total_steps,
                        "progress_percent": pipeline_result.progress_percent
                    }
                }
            else:
                print(f"❌ YouTube 파이프라인 실패: {pipeline_result.error}")
                return {
                    "type": "youtube_pipeline_failed",
                    "status": "failed",
                    "error": pipeline_result.error,
                    "progress": {
                        "completed_steps": pipeline_result.step_completed,
                        "total_steps": pipeline_result.total_steps,
                        "progress_percent": pipeline_result.progress_percent
                    }
                }
        
        except Exception as e:
            error_msg = f"YouTube 파이프라인 실행 중 오류: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "type": "youtube_pipeline_error",
                "status": "error",
                "error": error_msg
            }
    
    else:
        print(f"❌ 지원되지 않는 URL: {url}")
        return {
            "type": "unsupported_url",
            "status": "error",
            "message": "현재 YouTube URL만 지원됩니다."
        }


if __name__ == "__main__":
    import uvicorn
    print("🚀 다중 파일 처리 지원 서버 시작")
    print("📊 새로운 기능:")
    print("  - 다중 MD 파일 업로드 지원")
    print("  - 파일 큐 관리 시스템")
    print("  - 순차적 파일 처리")
    print("  - 처리 결과 일괄 관리")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)