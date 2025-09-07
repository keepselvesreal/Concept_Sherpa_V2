# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 리팩토링된 FastAPI 서버 - 4단계 개선 적용 (extraction-system 적용)
# 상세 내용:
#   - app = FastAPI(): FastAPI 인스턴스 생성 (라인 22)
#   - /: HTML 페이지 서빙 엔드포인트 (라인 27-30)
#   - /upload: 리팩토링된 업로드 처리 엔드포인트 (라인 45-85)
#   - is_youtube_url(): YouTube URL 검증 함수 (라인 32-43)
#   - YouTubePipeline 통합: 단순화된 파이프라인 실행
# 상태: active
# 주소: server (리팩토링 적용)
# 참조: server_old.py → 4단계 리팩토링 적용

import os
import re
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Union

# 리팩토링된 파이프라인 임포트
from pipeline.youtube_pipeline import YouTubePipeline
from pipeline.md_pipeline import MDPipeline
# from pipeline.book_pipeline import BookPipeline

app = FastAPI()

# uploads 디렉토리 생성
os.makedirs("uploads", exist_ok=True)


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
    """파일 첨부 전용 엔드포인트 (MD 파일 처리)"""
    
    result = {}
    
    # 파일이 없는 경우
    if not file or not file.filename:
        print("⚠️ 첨부된 파일이 없습니다.")
        return {
            "type": "no_file",
            "status": "error",
            "message": "파일을 첨부해주세요."
        }
    
    # 파일 형식 확인 (MD, PDF, EPUB 지원)
    file_ext = file.filename.lower()
    
    # 지원되지 않는 파일 형식 체크
    if not file_ext.endswith(('.md', '.markdown', '.pdf', '.epub')):
        print(f"❌ 지원되지 않는 파일 형식: {file.filename}")
        return {
            "type": "unsupported_file",
            "status": "error", 
            "message": "현재 마크다운(.md), PDF(.pdf), EPUB(.epub) 파일을 지원합니다."
        }
    
    # PDF/EPUB 파일인 경우 책 파이프라인으로 리다이렉트
    if file_ext.endswith(('.pdf', '.epub')):
        print(f"📚 책 파일 감지: {file.filename} - 책 파이프라인으로 처리")
        
        # 임시로 uploads 폴더에 파일 저장
        file_path = f"uploads/{file.filename}"
        try:
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            
            print(f"📁 책 파일 업로드됨: {file.filename} ({len(contents)} bytes)")
            
            # 메타정보 구성
            metadata_info = {
                "source_type": source_type or "book",
                "source_language": source_language or "korean",
                "structure_type": structure_type or "book", 
                "content_processing": content_processing or "unified"
            }
            
            # 🚀 책 파이프라인 실행
            try:
                pipeline = BookPipeline()
                pipeline_result = await pipeline.execute(file_path, metadata_info)
                
                if pipeline_result.is_success:
                    print("🎉 책 파이프라인 완료!")
                    result = {
                        "type": "book_pipeline_success",
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
                    print(f"❌ 책 파이프라인 실패: {pipeline_result.error}")
                    result = {
                        "type": "book_pipeline_failed",
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
                error_msg = f"책 파이프라인 실행 중 오류: {str(e)}"
                print(f"❌ {error_msg}")
                result = {
                    "type": "book_pipeline_error",
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
            error_msg = f"책 파일 처리 중 오류: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "type": "file_error",
                "status": "error",
                "error": error_msg
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
        
        # 🚀 MD 파이프라인 실행
        try:
            pipeline = MDPipeline()
            pipeline_result = await pipeline.execute(file_path, metadata_info)
            
            if pipeline_result.is_success:
                # ✅ 성공 응답
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
                # ❌ 실패 응답
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
            # 예상치 못한 오류
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
                # ✅ 성공 응답
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
                # ❌ 실패 응답
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
            # 예상치 못한 오류
            error_msg = f"YouTube 파이프라인 실행 중 오류: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "type": "youtube_pipeline_error",
                "status": "error", 
                "error": error_msg
            }
    
    else:
        # YouTube URL이 아닌 경우
        print(f"❌ 지원되지 않는 URL: {url}")
        return {
            "type": "unsupported_url",
            "status": "error",
            "message": "현재 YouTube URL만 지원됩니다."
        }


@app.post("/upload_book")
async def upload_book(
    file: Union[UploadFile, None] = File(None),
    source_type: Union[str, None] = Form(None),
    source_language: Union[str, None] = Form(None),
    structure_type: Union[str, None] = Form(None),
    content_processing: Union[str, None] = Form(None)
):
    """책 파일 첨부 전용 엔드포인트 (PDF/EPUB 파일 처리)"""
    
    result = {}
    
    # 파일이 없는 경우
    if not file or not file.filename:
        print("⚠️ 첨부된 파일이 없습니다.")
        return {
            "type": "no_file",
            "status": "error",
            "message": "파일을 첨부해주세요."
        }
    
    # PDF/EPUB 파일 확인
    file_ext = file.filename.lower()
    if not file_ext.endswith(('.pdf', '.epub')):
        print(f"❌ 지원되지 않는 파일 형식: {file.filename}")
        return {
            "type": "unsupported_file",
            "status": "error", 
            "message": "현재 PDF(.pdf), EPUB(.epub) 파일만 지원됩니다."
        }
    
    # 임시로 uploads 폴더에 파일 저장
    file_path = f"uploads/{file.filename}"
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        print(f"📁 책 파일 업로드됨: {file.filename} ({len(contents)} bytes)")
        
        # 메타정보 구성
        metadata_info = {
            "source_type": source_type or "book",
            "source_language": source_language or "korean",
            "structure_type": structure_type or "book",
            "content_processing": content_processing or "unified"
        }
        
        # 🚀 책 파이프라인 실행
        try:
            pipeline = BookPipeline()
            pipeline_result = await pipeline.execute(file_path, metadata_info)
            
            if pipeline_result.is_success:
                # ✅ 성공 응답
                print("🎉 책 파이프라인 완료!")
                result = {
                    "type": "book_pipeline_success",
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
                # ❌ 실패 응답
                print(f"❌ 책 파이프라인 실패: {pipeline_result.error}")
                result = {
                    "type": "book_pipeline_failed",
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
            # 예상치 못한 오류
            error_msg = f"책 파이프라인 실행 중 오류: {str(e)}"
            print(f"❌ {error_msg}")
            result = {
                "type": "book_pipeline_error",
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


if __name__ == "__main__":
    import uvicorn
    print("🚀 리팩토링된 서버 시작")
    print("📊 개선 사항:")
    print("  - subprocess 제거 → 직접 함수 호출")
    print("  - 복잡한 에러 처리 → 단순한 성공/실패")
    print("  - 동기/비동기 혼재 → async/await 통일") 
    print("  - 모놀리식 구조 → 파이프라인 클래스화")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)